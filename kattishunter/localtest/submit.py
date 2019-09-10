"""

Submit a test and return CPU time.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import os.path as path
import re
from typing import Dict, List, Text
import logging

from .compile import copyfiles, compile
from .run import runtest

logger = logging.getLogger(__name__)


def submit(config: Dict, files: List[Text]):
    "Submit a test and return CPU time."

    # First, copy files to submit to source folder.
    folder = config["local-test"]["sources"]
    copyfiles(files, folder)

    # Then compile the sources.
    exe = compile(folder)

    # Now run a test on each environnement.
    envs = re.split(",\s*", config["local-test"]["envs"])
    (sumrtime, numok) = (0, 0)

    for envname in envs:
        infile = path.join(folder, "%s.in" % envname)
        if not path.isfile(infile):
            logger.critical("Environnement file '%s' doesn't exist.", envname)

        (status, rtime) = runtest(infile, exe)
        sumrtime += rtime

        if status != 0:
            break  # We got a runtime error.
        sumrtime -= 0.015
        numok += 1

    sumrtime = round(sumrtime * 100)
    logger.debug("Submission done (cpu=%s, numok=%s).", sumrtime, numok)
    return (sumrtime, numok)
