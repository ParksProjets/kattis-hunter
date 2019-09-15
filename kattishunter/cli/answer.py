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

    parser.add_argument("--dont-shoot", action="store_true",
        help="do not shoot birds")
    parser.add_argument("--dont-guess", action="store_true",
        help="do not guess birds")

    parser.add_argument("-o", "--output", metavar="<folder>", default=".",
        help="output folder (default=.)")



def parse_scores(text: Text, config: Dict):
    "Parse given scores."

    scores = text.split(",")
    L = int(config["problem"]["number-of-env"])

    if len(scores) != L:
        logger.critical("You must give %d scores (comma separated).", L)

    (result, offset) = ([], 0)
    for i, s in enumerate(scores):
        try:
            num = int(s)
        except ValueError:
            logger.critical(f"Score {i+1} is not a number.")

        same_as = config["results"][i].get("same-as")
        if same_as != None:
            if num != result[same_as - offset]:
                logger.critical(f"Environment {i+1} is the same as {same_as+1}, "
                    "you must give it the same score.")
            offset += 1
        else:
            result.append(num)

    return result



def call(args: Namespace, config: Dict):
    "Call the command."

    # Ensure output directory exists.
    if not path.isdir(args.output):
        logger.critical("Output directory '%s' doesn't exist.", args.output)

    # Parse scores and create args dict.
    scores = parse_scores(args.scores, config)
    kargs = dict(
        R = config["results"], Scores = scores,
        Se = (not args.dont_shoot), Ge = (not args.dont_guess)
    )

    # Now generate the code.
    codegen(args.output, "answer", kargs)
