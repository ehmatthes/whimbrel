"""Tests for core functionality of Whimbrel.

This means tests like can it run, and will it not destroy or corrupt files it opens.

It's important to run the first two tests, because they work in combination.
  For example if the path to whimbrel.py is not correct, the second test will
  fail for the wrong reason, and due to xfail it will pass. But, the first test 
  indicates an issue.
"""

from pathlib import Path
from time import sleep

import pexpect
import pytest


# --- Validate testing approach ---

def test_run_whimbrel(whimbrel_path):
    """Test that I can run Whimbrel, and see expected output."""
    child = pexpect.spawn(f'python {whimbrel_path}')
    child.expect("WHIMBREL", timeout=0.1)

@pytest.mark.xfail
def test_run_whimbrel_expect_fail(whimbrel_path):
    """Test that I can run Whimbrel, and fail to see unexpected output."""
    child = pexpect.spawn(f'python {whimbrel_path}')
    child.expect("WHIMBRELLLL", timeout=0.1)

def test_send_text(whimbrel_path):
    """Test I can send a character to Whimbrel, and see it in the buffer."""
    child = pexpect.spawn(f'python {whimbrel_path}')
    child.expect("WHIMBREL", timeout=0.1)

    child.send("E")
    expected_text = 'Quit\r\n\r\nE'
    child.expect(expected_text, timeout=0.1)

def test_enter_command_mode(whimbrel_path):
    """Test I can enter command mode.

    I'm not sure what to look for right after entering escape.
    So:
    - enter text
    - verify text
    - enter command mode
    - enter text
    - exit command mode
    - verify command mode text not present
    - enter text
    - verify new text added to old text
    """
    child = pexpect.spawn(f'python {whimbrel_path}')
    child.expect("WHIMBREL", timeout=0.1)

    # Send a couple characters first, to make sure no issue with 
    #   sending simple characters.
    child.send("A")
    expected_text = 'Quit\r\n\r\nA'
    child.expect(expected_text, timeout=0.1)

    child.send("B")
    expected_text = 'Quit\r\n\r\nAB'
    child.expect(expected_text, timeout=0.1)

    # Esc to command mode.
    child.send("\x1b")

    # Send C, which should not be added to buffer.
    child.send("C")

    # Return to text mode.
    child.send("T")

    # Send D, which should be added to buffer.
    child.send("D")
    expected_text = 'Quit\r\n\r\nABD'
    child.expect(expected_text, timeout=0.1)



# --- Core functionality tests ---

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

def test_open_save_file(whimbrel_path, tmp_path):
    """Test I can open a file and then save it without affecting file contents."""
    file_ext = ".txt"
    reference_file = Path(__file__).parent / "reference_files" / f"great_birds{file_ext}"
    reference_file_text = reference_file.read_text()

    # Make a copy of the reference file, so we're not acting directly on it.
    test_file = tmp_path / f"great_birds{file_ext}"
    test_file.write_text(reference_file_text)
    assert test_file.read_text() == reference_file.read_text()
    # sleep(0.1)

    # A saved file has a different line ending than what's used in the buffer.
    expected_text = reference_file_text.strip().replace('\n', '\r\n')

    # Start Whimbrel, passing the temp file.
    child = pexpect.spawn(f"python {whimbrel_path} {test_file}")
    child.expect(expected_text, timeout=0.1)

    # Save file in Whimbrel.
    child.send("\x1b")
    child.send("S")

    # This sleep is necessary to allow time for saving to complete.
    sleep(0.1)

    # Make sure test file is unchanged.
    assert test_file.read_text() == reference_file.read_text()