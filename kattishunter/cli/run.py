"""

Run the script and find what we want.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

from argparse import Namespace, ArgumentParser, _SubParsersAction
from typing import Dict

from ..localtest import submit as submit_local
from ..kattis import submit as submit_kattis
from ..protocol import step


def subparser(subparser: _SubParsersAction):
    "Get CLI sub-parser for handling this command."

    parser: ArgumentParser = subparser.add_parser("run",
        description="Run the script nd find what we want.")

    parser.add_argument("--tos", action="store_true",
        help="use an user agent that complies with Terms of Service")

    parser.add_argument("--local", action="store_true",
        help="run the script with a local server")



def call(args: Namespace, config: Dict):
    "Call the command."

    # Create some config keys if they don't exist.
    config.setdefault("cache", {})

    # Select the right user agent to use now.
    user_agent = ("human", "tos")[args.tos]
    config["cache"]["user-agent"] = config["user-agent"][user_agent]

    # TODO: many steps?

    # Run one step.
    submit = (submit_kattis, submit_local)[args.local]
    step(config, submit)
