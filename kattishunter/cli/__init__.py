"""

Manage Command Line Interface (CLI).

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

from argparse import ArgumentParser, Namespace
from typing import Dict
import logging

from .run import subparser as sp_run, call as call_run
from .answer import subparser as sp_answer, call as call_answer

logger = logging.getLogger(__name__)


# All available sub-commands.
SUB_COMMANDS = {
    "run": (sp_run, call_run),
    "answer": (sp_answer, call_answer)
}


def create_subparsers(parser: ArgumentParser):
    "Create all CLI sub-parsers."

    subparser = parser.add_subparsers(dest="action",
        help="command to run")

    for (sp, _) in SUB_COMMANDS.values():
        sp(subparser)


def call_subcmd(args: Namespace, config: Dict):
    "Call the right sub-command."

    if not args.action:
        logger.critical("You must specify a sub-command to run.")

    (_, call) = SUB_COMMANDS[args.action]
    call(args, config)
