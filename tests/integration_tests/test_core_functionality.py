"""Tests for core functionality of Whimbrel.

This means tests like can it run, and will it not destroy or corrupt files it opens.

It's important to run the first two tests, because they work in combination.
  For example if the path to whimbrel.py is not correct, the second test will
  fail for the wrong reason, and due to xfail it will pass. But, the first test 
  indicates an issue.
"""

from pathlib import Path

import pexpect
import pytest

def test_run_whimbrel(whimbrel_path):
    """Test that I can run Whimbrel, and see expected output."""
    child = pexpect.spawn(f'python {whimbrel_path}')
    child.expect("WHIMBREL", timeout=0.1)

@pytest.mark.xfail
def test_run_whimbrel_expect_fail(whimbrel_path):
    """Test that I can run Whimbrel, and fail to see unexpected output."""
    child = pexpect.spawn(f'python {whimbrel_path}')
    child.expect("WHIMBRELLLL", timeout=0.1)

file_extensions = [".txt", ".json", ".yaml", ".md"]
@pytest.mark.parametrize("file_ext", file_extensions)
def test_open_file(whimbrel_path, file_ext):
    """Test I can open a file:
    - Without crashing;
    - See contents of file in buffer;
    - Verify that contents of file are unchanged.
    """
    reference_file = Path(__file__).parent / "reference_files" / f"great_birds{file_ext}"

    # Read reference file text before opening it.
    original_reference_file_text = reference_file.read_text()

    # A saved file has a different line ending than what's used in the buffer.
    expected_text = reference_file.read_text().strip().replace('\n', '\r\n')

    child = pexpect.spawn(f"python {whimbrel_path} {reference_file}")
    child.expect(expected_text, timeout=0.1)

    # Make sure reference file is unchanged.
    reference_file_text = reference_file.read_text()
    assert reference_file_text == original_reference_file_text
