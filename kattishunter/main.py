"""

Kattis Hunter.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import sys, os.path as path
import argparse
import json
from configparser import ConfigParser
from typing import Dict, Text
import logging

from .logger import set_looger_level, set_logger_file
from .cli import create_subparsers, call_subcmd

logger = logging.getLogger(__name__)


def read_config(filename: Text) -> Dict:
    "Read an parse configuration file."

    if not path.isfile(filename):
        logger.critical("Can't read config file '%s'.", filename)

    parser = ConfigParser()
    parser.read(filename)
    config = {n: dict(parser[n]) for n in parser.sections()}

    return config


def read_cache(filename: Text) -> Dict:
    "Read the cache file."

    with open(filename) as file:
        return json.load(file)



def main():
    "Entry point of this script."

    # Create CLI argument parser.
    parser = argparse.ArgumentParser(prog="kattishunter")

    parser.add_argument("--config", metavar="<file>", default="config.ini",
        help="configuration file to use (default=config.ini)")
    parser.add_argument("--cache", metavar="<file>", default="cache.json",
        help="cache file to read and write (default=cache.json)")

    parser.add_argument("-v", "--verbose", action="store_true",
        help="show debug messages")
    parser.add_argument("--log-file", metavar="<file>", default=None,
        help="log file to use (default=STDOUT)")

    create_subparsers(parser)

    # Parse CLI arguments and set logging level.
    args = parser.parse_args()
    set_looger_level(("INFO", "DEBUG")[args.verbose])
    set_logger_file(args.log_file)

    # Read cache or config file if cache doesn't exist.
    if path.isfile(args.cache):
        config = read_cache(args.cache)
    else:
        config = read_config(args.config)

    # Now execute the given sub-command.
    call_subcmd(args, config)
