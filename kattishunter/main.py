"""

Duck Hunter.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import sys, os.path as path
import argparse
from configparser import ConfigParser
import logging
from typing import Dict, Text

from . import logger
from .cli import create_subparsers, call_subcmd

logger = logging.getLogger(__name__)


def read_config(args: argparse.Namespace) -> Dict:
    "Read an parse configuration file."

    if not path.isfile(args.config):
        logger.critical("Can't read config file '%s'.", args.config)

    parser = ConfigParser()
    parser.read(args.config)
    config = {n: dict(parser[n]) for n in parser.sections()}

    return config



def main():
    "Entry point of this script."

    parser = argparse.ArgumentParser(prog="kattishunter")

    parser.add_argument("--config", metavar="<file>", default="config.ini",
        help="configuration file to use (default=config.ini)")
    parser.add_argument("--cache", metavar="<file>", default="cache.pickle",
        help="cache file to use, if existing (default=cache.pickle)")

    create_subparsers(parser)
    args = parser.parse_args()

    # TODO: read cache file if existing.
    config = read_config(args)

    call_subcmd(args, config)


if __name__ == "__main__":
    main()
