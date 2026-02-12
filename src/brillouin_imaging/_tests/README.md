# Tests for brillouin-imaging-napari

This directory contains pytest tests for the brillouin-imaging-napari plugin.

## Running Tests

### Install test dependencies

```bash
pip install -e ".[testing]"
```

### Run all tests

```bash
pytest src/brillouin_imaging/_tests/
```

### Run tests with verbose output

```bash
pytest src/brillouin_imaging/_tests/ -v
```

### Run specific test files

```bash
# Test reader functionality
pytest src/brillouin_imaging/_tests/test_reader.py

# Test sample data functionality
pytest src/brillouin_imaging/_tests/test_sample_data.py

# Test spectra viewer functionality
pytest src/brillouin_imaging/_tests/test_spectra_viewer.py
```

### Run tests with coverage

```bash
pytest src/brillouin_imaging/_tests/ --cov=brillouin_imaging --cov-report=html
```

### Skip Qt-dependent tests

Some tests require Qt and may not work in headless environments. To skip them:

```bash
pytest src/brillouin_imaging/_tests/ -m "not qt"
```

## Test Structure

- **test_reader.py**: Tests for the napari reader plugin functionality
  - Tests for `napari_get_reader()` function
  - Tests for `reader_function()` 
  - Tests for `create_brim_widget()` helper (Qt-dependent)

- **test_sample_data.py**: Tests for sample data loading functionality
  - Tests for `load_sample_data()` function
  - Tests for individual sample data functions (drosophila, zfeye, zfSBS, beadsFTBM)
  - Tests for both EMBL and Google Cloud Storage URLs

- **test_spectra_viewer.py**: Tests for the spectra viewer widget (Qt-dependent)
  - Tests for `ShowSpectrum` widget initialization
  - Tests for spectrum loading and plotting functionality

## Notes

- Qt-dependent tests require a display or offscreen Qt platform
- Tests use mocking extensively to avoid dependencies on external files
- The conftest.py file configures pytest with custom markers and Qt setup
