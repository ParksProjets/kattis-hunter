"""

Run Kattis Hunter.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import os, os.path as path
import shutil
import subprocess as sp
from typing import Dict
import logging

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

    # Run Kattis Hunter.
    os.chdir(rfolder)
    ps = sp.Popen(["/usr/bin/python3", "kattishunter", "--cache", "cache-local.json", "-v", "run", "1", "--local"])
    logger.info("Kattis Hunter is running for a single step.")

    try:
        ps.communicate(timeout=60)
        logger.info("Kattis Hunter stopped successfully.")
    except sp.TimeoutExpired:
        logger.warning("Kattis Hunter was killed after timeout.")
