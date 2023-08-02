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
        cmd = "cls" if os.name == "nt" else "clear"
        subprocess.call(cmd)

        # Always show the name of the program on the first line.
        print("WHIMBREL | [T] write Text [Esc] command mode [Q] Quit\n")
        print(self.buffer, end="", flush=True)

    def run(self):
        """Wait for input."""
        new_char = "p"
        while new_char != "q":
            new_char = self._get_char()

            if new_char == "q" and self.mode == "COMMAND":
                break
            elif new_char == "\x1b":
                # Process escape character.
                self.mode = "COMMAND"
            elif new_char.lower() == "t" and self.mode == "COMMAND":
                self.mode = "TEXT"
                continue
            elif new_char == "\r":
                # Convert Enter to proper newline.
                #   This is almost certainly macOS-specific.
                new_char = "\r\n"

            if self.mode == "COMMAND":
                self._process_command(new_char)
            elif self.mode == "TEXT":
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

    def _process_command(self, char):
        """Process commands entered while in COMMAND mode."""
        pass

    def _quit(self):
        self.buffer = "Goodbye, and thank you for trying Whimbrel!"
        self.paint_screen()

        sys.exit()


if __name__ == "__main__":
    whimbrel = Whimbrel()
