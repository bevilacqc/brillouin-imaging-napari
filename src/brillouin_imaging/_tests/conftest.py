"""Pytest configuration for brillouin_imaging tests."""
import pytest


def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line(
        "markers", "qt: marks tests as requiring Qt (deselect with '-m \"not qt\"')"
    )


@pytest.fixture(scope="session")
def qapp_cls():
    """Use a custom QApplication class that doesn't require a display."""
    import os
    # Set QT_QPA_PLATFORM to offscreen for headless testing
    os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
