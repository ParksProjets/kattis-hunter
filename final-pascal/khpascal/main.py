"""

Generate the final code in Pascal.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import sys
import os.path as path
import argparse
import json
from typing import Text, Dict

from .codegen import codegen


def parse_scores(text: Text, cache: Dict):
    "Parse given scores."

    scores = text.split(",")
    L = int(cache["problem"]["number-of-env"])

    if len(scores) != L:
        print("You must give %d scores (comma separated).", L)
        sys.exit(1)

    try:
        return [int(s) for s in scores]
    except ValueError:
        print("Given scores are not numbers.")
        sys.exit(1)



def main():
    "Entry point of this script."

    # Create CLI argument parser.
    parser = argparse.ArgumentParser(prog="khpascal")

    parser.add_argument("scores", metavar="<score list>",
        help="the number of steps to execute")

    parser.add_argument("-c", "--cache", metavar="<file>", default="../cache.json",
        help="cache file to use (default=../cache.json)")
    parser.add_argument("-i", "--input", metavar="<input file>", default="base.pas",
        help="base Pascal file to use (default=base.pas)")
    parser.add_argument("-o", "--output", metavar="<out file>", default="answer.pas",
        help="Pascal file to generate (default=answer.pas)")

    # Parse CLI arguments and read cache.
    args = parser.parse_args()
    with open(args.cache) as file:
        cache = json.load(file)

    # Parse scores and create args dict.
    scores = parse_scores(args.scores, cache)
    kargs = dict(R = cache["results"], Scores = scores)

    # Now generate the code.
    codegen(args.input, args.output, kargs)
