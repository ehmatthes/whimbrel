Whimbrel
---

A simple text editor, mostly for fun and learning.

(I've always wanted to write my own editor, and it really is fun and enlightening! This README was first drafted using Whimbrel!)

Installation
---

```sh
$ git clone https://github.com/ehmatthes/whimbrel.git
$ cd whimbrel
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ python whimbrel.py
```

You can also specify a file to open at startup:

```sh
$ python whimbrel.py shorebirds.txt
```

**Note: Whimbrel is an experimental project, and may corrupt any files you access while using it.**

Getting started
---

- Opens in text mode, so you can start typing immediately.
- Press Esc to enter command mode. In command mode:
    - T: Return to text mode
    - R: Read a file into the buffer
    - S: Save current buffer to the current file. If a file has not been specified, you'll be prompted to enter a filename/ file path.
    - Q: Quit.