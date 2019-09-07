"""

Kattis Hunter runner.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import os.path as path
import sys


# If this module is not installed: push it to sys.path.
parent = path.realpath(path.join(path.dirname(__file__), ".."))

if not parent.lower().endswith("lib/site-packages"):
	sys.path.insert(0, parent)


# Now, launch the CLI.
from khrunner.main import main

if __name__ == "__main__":
    main()
