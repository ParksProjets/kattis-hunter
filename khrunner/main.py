"""

Kattis Hunter runner.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import os.path as path
import argparse
import json
from typing import Text, Dict
import logging

from .logger import set_looger_level, set_logger_file
from .intervals import decode_intervals, wait_interval
from .run import runkh, backup_cache

logger = logging.getLogger(__name__)


def read_config(filename: Text) -> Dict:
    "Read the configuration file."

    if not path.isfile(filename):
        logger.critical("Can't read config file '%s'.", filename)

    with open(filename) as file:
        return json.load(file)



def wait_and_run(config: Dict):
    "Loop indefinitely and run Kattis Hunter."

    intervals = decode_intervals(config["intervals"])

    while True:
        wait_interval(intervals)
        runkh(config)
        backup_cache(config)



def main():
    "Entry point of this script."

    # Create CLI argument parser.
    parser = argparse.ArgumentParser(prog="khrunner")

    parser.add_argument("-c", "--config", metavar="<file>", default="khrunner.json",
        help="configuration file to use (default=khrunner.json)")

    parser.add_argument("-v", "--verbose", action="store_true",
        help="show debug messages")
    parser.add_argument("--log-file", metavar="<file>", default=None,
        help="log file to use (default=STDOUT)")

    # Parse CLI arguments and set logging level.
    args = parser.parse_args()
    set_looger_level(("INFO", "DEBUG")[args.verbose])
    set_logger_file(args.log_file)

    # Read configuration file and loop indefinitely.
    config = read_config(args.config)
    wait_and_run(config)
