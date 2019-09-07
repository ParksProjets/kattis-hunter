"""

Run the script and find what we want.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import os, os.path as path
import json
from tempfile import TemporaryDirectory
from typing import Text, Dict, Callable
import logging

from .steps import (number_birds, number_birds_next, species_next,
    directions_next, envhash_next)
from .persist import (persist_number_birds, persist_species,
    persist_directions, persist_envhash)
from .codegen import codegen

logger = logging.getLogger(__name__)


# Functions related to steps.
STEP_FUNCTIONS = {
    "number-birds": (number_birds_next, persist_number_birds),
    "species": (species_next, persist_species),
    "directions": (directions_next, persist_directions),
    "env-hash": (envhash_next, persist_envhash)
}

# First step to exexute.
FIRST_STEP = number_birds


def find_files(tmpdir: Text):
    "Find source files to submit."

    files = os.listdir(tmpdir)
    return [path.join(tmpdir, file) for file in files]



def setup_results(config: Dict):
    "Setup result field from config."

    NumE = int(config["problem"]["number-of-env"])
    EnvObj = [{
        "done": False,
        "num-birds": 0,
        "hash": 0,
        "rounds": [{
            "num-birds": 0,
            "directions": None,
            "species": None
        }] * 10
    }] * NumE

    config["results"] = json.loads(json.dumps(EnvObj))



def save_cache(config: Dict, cachefile: Text):
    "Save the current config to the cache file."

    with open(cachefile, "w") as file:
        json.dump(config, file, indent=4)



def step(config: Dict, cachefile: Text, submit: Callable):
    "Execute one single step and persist data."

    # First, initalize cache if its the first time we run the script.
    if "step" not in config:
        config["step"] = FIRST_STEP(config)
    if "results" not in config:
        setup_results(config)

    # If "step" is None, quit the script now.
    if config["step"] is None:
        logger.critical("No step to execute next, STOP.")

    # Retrieve the current step.
    (name, kargs) = config["step"]
    (nextstep, persist) = STEP_FUNCTIONS[name]

    # Generate and submit new code for target step.
    with TemporaryDirectory() as tmpdir:
        codegen(tmpdir, name, dict(**kargs, R=config["results"]))
        (rtime, numok) = submit(config, find_files(tmpdir))

    # Save data to cache and go to next step.
    persist(config, rtime, **kargs)
    config["step"] = nextstep(config, **kargs)
    save_cache(config, cachefile)
