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

def test_run_whimbrel():
    """Test that I can run Whimbrel, and see expected output."""
    whimbrel_path = Path(__file__).parent.parent.parent / "whimbrel.py"
    child = pexpect.spawn(f'python {whimbrel_path}')
    child.expect("WHIMBREL", timeout=0.1)

@pytest.mark.xfail
def test_run_whimbrel_expect_fail():
    """Test that I can run Whimbrel, and fail to see unexpected output."""
    whimbrel_path = Path(__file__).parent.parent.parent / "whimbrel.py"
    child = pexpect.spawn(f'python {whimbrel_path}')
    child.expect("WHIMBRELLLL", timeout=0.1)

def test_open_file():
    """Test I can open a file:
    - Without crashing;
    - See contents of file in buffer;
    - Verify that contents of file are unchanged.
    """
    whimbrel_path = Path(__file__).parent.parent.parent / "whimbrel.py"
    reference_file = Path(__file__).parent / "reference_files" / "great_birds.txt"

    # A saved file has a different line ending than what's used in the buffer.
    expected_text = reference_file.read_text().strip().replace('\n', '\r\n')

    child = pexpect.spawn(f"python {whimbrel_path} {reference_file}")
    child.expect(expected_text, timeout=0.1)