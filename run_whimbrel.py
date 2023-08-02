import pexpect
import time

child = pexpect.spawn('python whimbrel.py')

child.expect("WHIMBREL", timeout=3)

# No longer needed, because Whimbrel starts in text mode.
# child.send('T')
# child.expect("WHIMBREL", timeout=3)

child.send('H')
child.expect("Quit\r\n\r\nH", timeout=3)

child.send('e')
child.expect("Quit\r\n\r\nHe", timeout=3)

child.send('l')
child.expect("Quit\r\n\r\nHel", timeout=3)

child.send('q')
