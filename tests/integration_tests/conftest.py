"""Fixtures for integration tests."""

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def whimbrel_path():
    return Path(__file__).parent.parent.parent / "whimbrel.py"