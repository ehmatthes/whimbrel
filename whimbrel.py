"""A simple, terminal-based text editor.

Current functions:
- Open file
- Close file
- Save file
"""

import os, sys, subprocess, time, termios, tty
from pathlib import Path


class Whimbrel:

    def __init__(self):
        """Initialize the editor."""
        self.mode = "COMMAND"
        self.logfile = Path('logs/log.txt')
        self.buffer = ""

        self.paint_screen()
        self.run()

    def paint_screen(self):
        """Repaint the screen."""

        # Clear the screen.
        # cmd = "cls" if os.name == "nt" else "clear"
        # subprocess.call(cmd)

        # Always show the name of the program on the first line.
        print("WHIMBREL\n")
        print(self.buffer, end="", flush=True)

    def run(self):
        """Wait for input."""
        new_char = "p"
        lf = 0
        while new_char != "q":
            new_char = self._get_char()
            path = Path(f"logs/logfile_{lf}.txt")
            # path.write_text(new_char)
            lf += 1

            # Break on quit character.
            if new_char == "q":
                # print('BBB')
                break
            else:
                # print('CCC')
                pass

            # Convert Enter to proper newline.
            #   This is almost certainly macOS-specific.
            if new_char == "\r":
                new_char = "\r\n"

            self.buffer += new_char
            self.paint_screen()

        print("Writing to log file...")
        self.logfile.write_text(self.buffer)

        # Quit cleanly.
        self._quit()

    def _get_char(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def _quit(self):
        self.buffer = "Goodbye, and thank you for trying Whimbrel!"
        self.paint_screen()
        print("\n\n")
        print('EXIT_MARKER', flush=True)
        sys.exit()


if __name__ == "__main__":
    whimbrel = Whimbrel()
