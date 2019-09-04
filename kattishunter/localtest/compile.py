"""

Synchronize changes and compile the program.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import os.path as path
import glob
import shutil
import subprocess as sp
import logging

logger = logging.getLogger(__name__)


def copyfiles(files, folder):
    "Copy given files to target folder."

    if not path.isdir(folder):
        logger.critical("Can't find target folder '%s'.", folder)

    for file in files:
        shutil.copyfile(file, path.join(folder, path.basename(file)))



def compile(folder):
    "Compile all C++ files in the given folder."

    if not path.isdir(folder):
        logger.critical("Can't find source folder '%s'.", folder)

    files = glob.glob(path.join(folder, "*pp"))
    out = path.join(folder, "kattishunter")
    cmd = ["g++", "-o", out, "-g", "-O2", "-std=gnu++17"]

    logger.debug("Compiling source files.")
    ps = sp.Popen(cmd + files)
    ps.communicate()

    if ps.returncode != 0:
        logger.critical("GCC returned an error when compiling.")
    logger.debug("Compilation done!")

    return out
