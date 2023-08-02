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
        self.buffer = ""
        self.paint_screen()
        self.run()

    def paint_screen(self):
        """Repaint the screen."""
        # Clear the screen.
        cmd = "cls" if os.name == "nt" else "clear"
        subprocess.call(cmd)

        # Always show the name of the program on the first line.
        print("WHIMBREL\n")
        
        # Display the current buffer.
        if not self.buffer:
            return

        # We have some data, so show it.
        # if self.buffer[-1] == "\r":
        #     print(self.buffer)
        # else:
        #     print(self.buffer, end="", flush=True)

        # if self.buffer[-2:] == "\r\n":
        #     print(self.buffer, end="", flush=True)
        # else:
        #     print(self.buffer, end="", flush=True)

        print(self.buffer, end="", flush=True)


    def run(self):
        """Wait for input."""
        new_char = "p"
        while new_char != "q":
            new_char = self._get_char()

            if new_char == "\r":
                # print('here1')
                # time.sleep(1)
                new_char = "\r\n"
            # if new_char == "\r\n":
            #     print('here2')
            #     time.sleep(1)

            self.buffer += new_char
            self.paint_screen()

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
        sys.exit()



if __name__ == "__main__":
    whimbrel = Whimbrel()
