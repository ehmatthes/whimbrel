import pexpect
import time

import pyte


screen = pyte.Screen(80, 24)
stream = pyte.Stream(screen)

child = pexpect.spawn('python whimbrel.py')

child.expect("WHIMBREL", timeout=3)
stream.feed(child.before.decode() + child.after.decode())

child.send('H')
child.expect("WHIMBREL\r\n\r\nH", timeout=3)
stream.feed(child.before.decode() + child.after.decode())

child.send('q')
child.expect("EXIT_MARKER", timeout=3)
stream.feed(child.before.decode() + child.after.decode())
