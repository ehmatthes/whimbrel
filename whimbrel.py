"""A simple, terminal-based text editor.

Current functions:
- Open file
- Close file
- Save file
"""

import os, sys, subprocess, time, termios, tty


class Whimbrel:

    def __init__(self):
        """Initialize the editor."""
        # Clear terminal screen.
        self.mode = "COMMAND"
        self.paint_screen()
        self.run()

    def paint_screen(self):
        """Repaint the screen."""
        cmd = "cls" if os.name == "nt" else "clear"
        subprocess.call(cmd)
        print("WHIMBREL\n")

    def run(self):
        """Wait for input."""
        new_char = "p"
        while new_char != "q":
            new_char = self.get_char()
            self.paint_screen()
            print(new_char)

    def get_char(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)



if __name__ == "__main__":
    whimbrel = Whimbrel()
