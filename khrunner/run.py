"""

Run Kattis Hunter.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import os, os.path as path
import shutil
import time
import subprocess as sp
from typing import Dict
import logging

from .logger import handler as log_handler

logger = logging.getLogger(__name__)


# Backup the cacje every 5 steps.
BACKUP_AFTER = 5
BACKUP_COUNTER = 0


def backup_cache(config: Dict):
    "Backup the cache file."

    # Ensure backup folder is existing.
    bfolder = config["backup-dir"]
    rfolder = config["kh-dir"]
    if not path.isdir(bfolder):
        logger.critical("Backup folder '%s' doesn't exist.", bfolder)

    # Increment backup counter.
    global BACKUP_COUNTER
    BACKUP_COUNTER += 1

    # Counter is a multiple of 5, backup the cache file.
    if (BACKUP_COUNTER % BACKUP_AFTER) == 0:
        name = "cache-%s.json" % time.strftime("%Y.%m.%d-%H:%M")
        shutil.copyfile(path.join(rfolder, "cache.json"), path.join(bfolder, name))



def runkh(config: Dict):
    "Run Kattis Hunter."

    # Ensure Kattis Hunter is existing.
    rfolder = config["kh-dir"]
    if not path.isdir(rfolder):
        logger.critical("Kattis Hunter folder '%s' doesn't exist.", rfolder)

    # Extra parameters to use when running Kattis Hunter.
    extra = ["-v"]
    if log_handler.file:
        extra.append("--log-file=%s" % log_handler.file)

    # Run Kattis Hunter.
    os.chdir(rfolder)
    ps = sp.Popen(["/usr/bin/python3", "kattishunter", *extra, "run", "1"])
    logger.info("Kattis Hunter is running (%d-th time)." % (BACKUP_COUNTER + 1))

    try:
        ps.communicate(timeout=60)
        logger.info("Kattis Hunter stopped successfully.")
    except sp.TimeoutExpired:
        ps.kill()
        logger.warning("Kattis Hunter was killed after timeout.")
