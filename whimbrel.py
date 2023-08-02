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
        self.filename = ""

        self.paint_screen()
        self.run()

    def paint_screen(self, show_info=True):
        """Repaint the screen."""

        # Clear the screen.
        cmd = "cls" if os.name == "nt" else "clear"
        subprocess.call(cmd)

        if show_info:
            print(f"WHIMBREL   |   mode: {self.mode}   |   [Esc] command mode   [T] enter Text   [Q] Quit\n")
        print(self.buffer, end="", flush=True)

    def run(self):
        """Wait for input."""
        while True:
            new_char = self._get_char()

            if new_char == "\x1b":
                # Process escape character.
                self.mode = "COMMAND"
            elif new_char.lower() == "t" and self.mode == "COMMAND":
                # This needs to be processed here, otherwise "t" will
                #   become part of the buffer.
                self.mode = "TEXT"
                self.paint_screen()
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
        if char.lower() == "q":
            self._quit()
        elif char.lower() == "s":
            self._save_file()

    def _save_file(self):
        """Write the current buffer to a file."""
        if not self.filename:
            self.filename = "my_file.txt"

        path = Path(self.filename)
        path.write_text(self.buffer)


    def _quit(self):
        # Log buffer, for diagnostic purposes.
        self.logfile.write_text(self.buffer)

        self.buffer = "Goodbye, and thank you for trying Whimbrel!\n\n"
        self.paint_screen(show_info=False)

        sys.exit()


if __name__ == "__main__":
    whimbrel = Whimbrel()
