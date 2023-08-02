"""A simple, terminal-based text editor.

Current functions:
- Open file
- Close file
- Save file
"""

import os, sys, subprocess, time, termios, tty
from pathlib import Path


class Whimbrel:

    def __init__(self, filename=""):
        """Initialize the editor."""
        self.mode = "TEXT"
        self.logfile = Path('logs/log.txt')
        self.buffer = ""
        self.filename = filename

        note = ""
        if self.filename:
            note = self._read_file()

        self.paint_screen(note=note)
        self.run()

    def paint_screen(self, show_info=True, note=""):
        """Repaint the screen."""

        # Clear the screen.
        cmd = "cls" if os.name == "nt" else "clear"
        subprocess.call(cmd)

        # Add space to note if it exists.
        #   If no current note, show filename if it's set.
        if note:
            note = f"   {note}"
        elif self.filename:
            note = f"   {self.filename}"

        if show_info:
            print(f"WHIMBREL   |   mode: {self.mode}{note}   |   [Esc] command mode   [T] enter Text   [R] Read file   [S] Save buffer   [Q] Quit\n")
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
            elif new_char == "\x7f":
                # Process backspace character.
                self.buffer = self.buffer[:-1]
                self.paint_screen()
                continue

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
        elif char.lower() == "r":
            self._get_filename()
            self._read_file()
            self.paint_screen()
        elif char.lower() == "s":
            self._save_file()


    def _get_filename(self):
        """Get a new filename."""
        self.filename = input("\n\n\nFilename: ")


    def _read_file(self):
        """Read a file into the buffer."""
        path = Path(self.filename)
        try:
            self.buffer = path.read_text()
        except FileNotFoundError:
            self.filename = ""
            return f"{path} not found."


    def _save_file(self):
        """Write the current buffer to a file."""
        if not self.filename:
            self.filename = input("\n\n\nFilename: ")

        path = Path(self.filename)
        path.write_text(self.buffer)

        self.paint_screen(note="Saved file.", show_info=True)


    def _quit(self):
        # Log buffer, for diagnostic purposes.
        self.logfile.write_text(self.buffer)

        self.buffer = "Goodbye, and thank you for trying Whimbrel!\n\n"
        self.paint_screen(show_info=False)

        sys.exit()


if __name__ == "__main__":
    # Get filename if one has been passed.
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = ""

    # Start the Whimbrel editor.
    whimbrel = Whimbrel(filename=filename)
