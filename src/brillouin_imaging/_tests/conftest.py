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

