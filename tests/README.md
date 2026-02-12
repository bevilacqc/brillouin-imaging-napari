# Tests for brillouin-imaging-napari

This directory contains pytest tests for the brillouin-imaging-napari plugin, following napari's official testing guidelines.

## Testing Guidelines

This test suite follows the [napari plugin testing guidelines](https://napari.org/stable/plugins/testing_and_publishing/test.html) which recommend:

### Key Practices

1. **Use napari fixtures**: Use `make_napari_viewer` fixture provided by napari for viewer instances (ensures proper cleanup)
2. **Use pytest fixtures**: Use `tmp_path` for temporary files instead of `tempfile` module
3. **Use qtbot for Qt widgets**: Use `qtbot.addWidget()` for proper Qt widget cleanup
4. **Mock external dependencies**: Mock file I/O and external services when possible
5. **Test plugin contributions**: Test reader plugins and widget plugins with proper integration

## Test Structure

Tests are located in the root `tests/` directory (not inside the `src/` package), following standard Python project conventions and napari plugin templates.

## Running Tests

### Install test dependencies

```bash
pip install -e ".[testing]"
```

### Run all tests

```bash
pytest
```

or explicitly:

```bash
pytest tests/
```

### Run tests with verbose output

```bash
pytest tests/ -v
```

### Run specific test files

```bash
# Test reader functionality
pytest tests/test_reader.py

# Test sample data functionality
pytest tests/test_sample_data.py

# Test spectra viewer functionality
pytest tests/test_spectra_viewer.py
```

### Run tests with coverage

```bash
pytest tests/ --cov=brillouin_imaging --cov-report=html
```

### Skip Qt-dependent tests

Some tests require Qt and may not work in headless environments. To skip them:

```bash
pytest tests/ -m "not qt"
```

## Test Files

- **test_reader.py**: Tests for the napari reader plugin functionality
  - Tests for `napari_get_reader()` function (file format detection)
  - Tests for `reader_function()` (widget creation and viewer integration)
  - Tests for `create_brim_widget()` helper (Qt-dependent)
  - **Follows napari guidelines**: Uses `tmp_path` fixture for temporary files

- **test_sample_data.py**: Tests for sample data loading functionality
  - Tests for `load_sample_data()` function
  - Tests for individual sample data functions (drosophila, zfeye, zfSBS, beadsFTBM)
  - Tests for both EMBL and Google Cloud Storage URLs
  - **Follows napari guidelines**: Uses appropriate mocking for external services

- **test_spectra_viewer.py**: Tests for the spectra viewer widget (Qt-dependent)
  - Tests for `ShowSpectrum` widget initialization
  - Tests for spectrum loading and plotting functionality
  - **Follows napari guidelines**: Uses `make_napari_viewer` fixture and `qtbot.addWidget()`

- **conftest.py**: Pytest configuration following napari guidelines
  - Qt offscreen mode configuration for CI/CD
  - Custom markers for Qt-dependent tests
  - **Note**: `make_napari_viewer` fixture is provided by napari itself (from `napari.utils._testsupport`)

## Napari-Specific Features

### make_napari_viewer Fixture

The `make_napari_viewer` fixture is **provided by napari** and ensures proper viewer cleanup after tests:

```python
def test_something(make_napari_viewer):
    viewer = make_napari_viewer()
    # viewer is automatically closed after test
```

This fixture is available from `napari.utils._testsupport` and does not need to be redefined.

### qtbot Integration

For Qt widget tests, use `qtbot.addWidget()` for proper cleanup:

```python
@pytest.mark.qt
def test_widget(qtbot):
    widget = create_some_widget()
    qtbot.addWidget(widget.native)  # Ensures proper cleanup
    # test widget
```

### Temporary Files

Use pytest's `tmp_path` fixture instead of `tempfile`:

```python
def test_with_file(tmp_path):
    test_file = tmp_path / "test.brim.zarr"
    test_file.mkdir()
    # test_file is automatically cleaned up
```

## Notes

- Qt-dependent tests require a display or offscreen Qt platform
- Tests use mocking extensively to avoid dependencies on external files
- The conftest.py file configures pytest with napari-recommended practices
- All tests follow napari's plugin testing guidelines for reliability and maintainability
