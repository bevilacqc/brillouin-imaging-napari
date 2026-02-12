"""Pytest configuration for brillouin_imaging tests."""
import os
import pytest


# Set QT_QPA_PLATFORM to offscreen for headless testing
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')


def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line(
        "markers", "qt: marks tests as requiring Qt (deselect with '-m \"not qt\"')"
    )


@pytest.fixture
def make_napari_viewer():
    """
    Fixture to create a napari viewer for testing.
    
    This follows napari's testing guidelines to ensure proper viewer cleanup.
    See: https://napari.org/stable/plugins/testing_and_publishing/test.html
    
    Yields
    ------
    function
        Factory function that creates and returns a napari Viewer instance.
        The viewer is automatically closed after the test.
    """
    viewers = []
    
    def _make_viewer(*args, **kwargs):
        import napari
        viewer = napari.Viewer(*args, **kwargs)
        viewers.append(viewer)
        return viewer
    
    yield _make_viewer
    
    # Cleanup: close all viewers created during the test
    for viewer in viewers:
        viewer.close()

