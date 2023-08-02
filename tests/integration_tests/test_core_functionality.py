import pexpect
import pytest

def test_run_whimbrel():
    """Test that I can run Whimbrel, and see expected output."""
    child = pexpect.spawn('python whimbrel.py')
    child.expect("WHIMBREL", timeout=0.1)

@pytest.mark.xfail
def test_run_whimbrel_expect_fail():
    """Test that I can run Whimbrel, and fail to see unexpected output."""
    child = pexpect.spawn('python whimbrel.py')
    child.expect("WHIMBRELLLL", timeout=0.1)

