"""

View results from cache.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import os.path as path
from argparse import Namespace, ArgumentParser, _SubParsersAction
from typing import Dict, Text, Optional, List
import logging

from ..codegen import codegen

logger = logging.getLogger(__name__)


def subparser(subparser: _SubParsersAction):
    "Get CLI sub-parser for handling this command."

    parser: ArgumentParser = subparser.add_parser("results",
        description="Run the script nd find what we want.")

    parser.add_argument("-d", "--details", action="store_true",
        help="get more details on results (like rounds)")



def dump_species(species: Optional[List[Text]]):
    "Write bird species."

    models = ["Pg", "Rv", "Sk", "Sw", "Sp", "Bs"]
    return ", ".join(models[s] for s in (species or []))


def dump_directions(directions: Optional[List[Text]]):
    "Write bird species."

    models = ["🡔", "🡑", "🡕", "🡐", "•", "🡒", "🡗", "🡓", "🡖"]
    return ", ".join(models[d] for d in (directions or []))



def call(args: Namespace, config: Dict):
    "Call the command."

    envs = config["results"]
    print("\nNumber of environments: %d" % len(envs))

    for i, e in enumerate(envs):
        print("\nEnvirnoment %d:" % i)
        print("   Done: %s" % ("no", "yes")[e["done"]])
        print("   Number of birds: %d" % e["num-birds"])
        print("   Hash: %d" % e.get("hash", 0))

        if not args.details:
            continue

        for j, r in enumerate(e["rounds"]):
            print("   Round %d:" % j)
            print("      Number of birds: %d" % r["num-birds"])
            print("      Species: %s" % dump_species(r["species"]))
            print("      Directions: %s" % dump_directions(r["directions"]))

    print()
