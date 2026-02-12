"""Tests for the reader module."""
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pytest
from brillouin_imaging._reader import (
    napari_get_reader,
    reader_function,
    create_brim_widget,
)


class TestNapariGetReader:
    """Tests for napari_get_reader function."""

    def test_returns_none_for_list_of_paths(self):
        """Test that napari_get_reader returns None for list of paths."""
        paths = ["file1.brim.zarr", "file2.brim.zarr"]
        result = napari_get_reader(paths)
        assert result is None

    def test_returns_none_for_invalid_extension(self):
        """Test that napari_get_reader returns None for invalid extension."""
        result = napari_get_reader("file.txt")
        assert result is None

    def test_returns_none_for_nonexistent_zarr_directory(self):
        """Test that napari_get_reader returns None for non-existent zarr directory."""
        result = napari_get_reader("nonexistent.brim.zarr")
        assert result is None

    @patch('brillouin_imaging._reader.brim.File')
    def test_returns_reader_function_for_valid_zarr(self, mock_brim_file):
        """Test that napari_get_reader returns reader function for valid zarr."""
        # Create a temporary directory to simulate a zarr file
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            zarr_path = os.path.join(tmpdir, "test.brim.zarr")
            os.makedirs(zarr_path)
            
            # Mock the brim.File to not raise an exception
            mock_brim_file.return_value = MagicMock()
            
            result = napari_get_reader(zarr_path)
            assert result is not None
            assert result == reader_function

    @patch('brillouin_imaging._reader.brim.File')
    def test_returns_reader_function_for_valid_zip(self, mock_brim_file):
        """Test that napari_get_reader returns reader function for valid zip."""
        # Create a temporary zip file
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".brim.zip", delete=False) as tmpfile:
            zip_path = tmpfile.name
            
        try:
            # Mock the brim.File to not raise an exception
            mock_brim_file.return_value = MagicMock()
            
            result = napari_get_reader(zip_path)
            assert result is not None
            assert result == reader_function
        finally:
            os.unlink(zip_path)

    @patch('brillouin_imaging._reader.brim.File')
    def test_returns_none_when_brim_file_raises_exception(self, mock_brim_file):
        """Test that napari_get_reader returns None when brim.File raises exception."""
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".brim.zip", delete=False) as tmpfile:
            zip_path = tmpfile.name
            
        try:
            # Mock the brim.File to raise an exception
            mock_brim_file.side_effect = Exception("Cannot read file")
            
            result = napari_get_reader(zip_path)
            assert result is None
        finally:
            os.unlink(zip_path)


class TestReaderFunction:
    """Tests for reader_function."""

    @patch('brillouin_imaging._reader.napari.current_viewer')
    @patch('brillouin_imaging._reader.brim.File')
    @patch('brillouin_imaging._reader.create_brim_widget')
    def test_reader_function_returns_none_tuple(
        self, mock_create_widget, mock_brim_file, mock_viewer
    ):
        """Test that reader_function returns a tuple with None."""
        # Setup mocks
        mock_file = MagicMock()
        mock_brim_file.return_value = mock_file
        
        mock_widget = MagicMock()
        mock_create_widget.return_value = mock_widget
        
        mock_dock = MagicMock()
        mock_viewer_instance = MagicMock()
        mock_viewer_instance.window.add_dock_widget.return_value = mock_dock
        mock_viewer.return_value = mock_viewer_instance
        
        # Call the function
        result = reader_function("test.brim.zarr")
        
        # Verify the result
        assert result == [(None,)]
        
        # Verify that the widget was created and added
        mock_create_widget.assert_called_once_with(mock_file)
        mock_viewer_instance.window.add_dock_widget.assert_called_once()

    @patch('brillouin_imaging._reader.napari.current_viewer')
    @patch('brillouin_imaging._reader.brim.File')
    @patch('brillouin_imaging._reader.create_brim_widget')
    def test_reader_function_connects_close_callback(
        self, mock_create_widget, mock_brim_file, mock_viewer
    ):
        """Test that reader_function connects close callback to widget."""
        # Setup mocks
        mock_file = MagicMock()
        mock_brim_file.return_value = mock_file
        
        mock_widget = MagicMock()
        mock_create_widget.return_value = mock_widget
        
        mock_dock = MagicMock()
        mock_viewer_instance = MagicMock()
        mock_viewer_instance.window.add_dock_widget.return_value = mock_dock
        mock_viewer.return_value = mock_viewer_instance
        
        # Call the function
        reader_function("test.brim.zarr")
        
        # Verify that the close callback was connected
        mock_dock.destroyed.connect.assert_called_once()


class TestCreateBrimWidget:
    """Tests for create_brim_widget function."""

    @pytest.mark.qt
    def test_create_brim_widget_returns_container(self, qtbot):
        """Test that create_brim_widget returns a Container."""
        from magicgui.widgets import Container
        
        # Create a mock file object
        mock_file = MagicMock()
        mock_file.list_data_groups.return_value = [
            {'custom_name': 'Data Group 1', 'index': 0}
        ]
        
        # Call the function
        widget = create_brim_widget(mock_file)
        
        # Verify the result
        assert isinstance(widget, Container)

    @pytest.mark.qt
    def test_create_brim_widget_has_expected_widgets(self, qtbot):
        """Test that create_brim_widget creates expected widgets."""
        # Create a mock file object
        mock_file = MagicMock()
        mock_file.list_data_groups.return_value = [
            {'custom_name': 'Data Group 1', 'index': 0},
            {'custom_name': 'Data Group 2', 'index': 1}
        ]
        
        # Call the function
        widget = create_brim_widget(mock_file)
        
        # Verify the widget has the expected components
        assert len(widget) == 5  # 4 combo boxes + 1 button
        assert hasattr(widget, 'data_groups')
        
    @pytest.mark.qt
    def test_create_brim_widget_initializes_combo_boxes(self, qtbot):
        """Test that create_brim_widget initializes combo boxes with data."""
        # Create a mock file object
        mock_file = MagicMock()
        mock_file.list_data_groups.return_value = [
            {'custom_name': 'Data Group 1', 'index': 0},
            {'custom_name': 'Data Group 2', 'index': 1}
        ]
        
        # Call the function
        widget = create_brim_widget(mock_file)
        
        # Check that data_groups combo box has the right choices
        data_combo = widget[0]  # First widget should be data_groups
        assert len(data_combo.choices) == 2
        assert 'Data Group 1' in data_combo.choices
        assert 'Data Group 2' in data_combo.choices
