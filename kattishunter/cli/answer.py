"""

Generate the answer code.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import os.path as path
from argparse import Namespace, ArgumentParser, _SubParsersAction
from typing import Dict, Text
import logging

from ..codegen import codegen

logger = logging.getLogger(__name__)


def subparser(subparser: _SubParsersAction):
    "Get CLI sub-parser for handling this command."

    parser: ArgumentParser = subparser.add_parser("answer",
        description="Run the script nd find what we want.")

    parser.add_argument("scores", metavar="<score list>",
        help="the number of steps to execute")

    parser.add_argument("-o", "--output", metavar="<folder>", default=".",
        help="output folder (default=.)")



def parse_scores(text: Text, config: Dict):
    "Parse given scores."

    scores = text.split(",")
    L = int(config["problem"]["number-of-env"])

    if len(scores) != L:
        logger.critical("You must give %d scores (comma separated).", L)

    try:
        return [int(s) for s in scores]
    except ValueError:
        logger.critical("Given scores are not numbers.")



def call(args: Namespace, config: Dict):
    "Call the command."

    # Ensure output directory exists.
    if not path.isdir(args.output):
        logger.critical("Output directory '%s' doesn't exist.", args.output)

    # Parse scores and create args dict.
    scores = parse_scores(args.scores, config)
    kargs = dict(R = config["results"], Scores = scores)

    # Now generate the code..
    codegen(args.output, "answer", kargs)
