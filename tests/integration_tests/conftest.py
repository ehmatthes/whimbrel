"""Fixtures for integration tests."""

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def whimbrel_path():
    """Get the path to the whimbrel.py file."""
    return Path(__file__).parent.parent.parent / "whimbrel.py"