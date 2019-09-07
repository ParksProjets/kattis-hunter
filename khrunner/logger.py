"""

Overwrite Python logger for a more beautiful one.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import os, sys
import logging
import ctypes
from typing import Text


# Check if we are on Windows.
is_win32 = (os.name == "nt")
if is_win32:
    handle = ctypes.windll.kernel32.GetStdHandle(-11)
    last_fg = 7


# Terminal colors to use.
COLORS = {  # (ansi, win32)
    "RESET": ("\033[0m", 7),
    "DEBUG": ("\033[39m", 7),
    "INFO": ("\033[36m", 3),
    "WARNING": ("\033[93m", 14),
    "ERROR": ("\033[91m", 12),
    "CRITICAL": ("\033[91m\033[1m", 12),
}


class LogHandler(logging.Handler):
    "Overwrite Python logger for a more beautiful one."

    def __init__(self, level=logging.NOTSET):
        super().__init__(level)
        self.file = None


    def colorize(self, color, stream):
        "Colorize the console."

        colors = COLORS.get(color)
        if colors is None:
            return  # Color not found.

        if is_win32:
            ctypes.windll.kernel32.SetConsoleTextAttribute(handle, colors[1])
        else:
            print(colors[0], end="", file=stream)


    def print(self, record, stream):
        "Print a record to the console."

        self.colorize(record.levelname, stream)
        print("%s - %s" % (record.levelname, self.format(record)), file=stream)
        self.colorize("RESET", stream)


    def emit(self, record):
        "Called when we need to output a log to the console."

        if self.file:
            stream = open(self.file, "a+")
        elif record.levelname in ("CRITICAL", "ERROR", "WARNING"):
            stream = sys.stderr
        else:
            stream = sys.stdout

        self.print(record, stream)

        if record.levelname == "CRITICAL":  # Stop the script on critical error.
            logging.shutdown()
            sys.exit(1)
        elif self.file:
            stream.close()


# Bind the handler to the logger.
handler = LogHandler()
logging.getLogger().handlers = []
logging.getLogger().addHandler(handler)


def set_looger_level(level: Text):
    "Set logging level of the logger."

    level = os.environ.get("LOGLEVEL") or level
    logging.getLogger("khrunner").setLevel(level)


def set_logger_file(filename: Text):
    "Set the log file."

    handler.file = filename
