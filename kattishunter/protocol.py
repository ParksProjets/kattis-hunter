"""

Run the script and find what we want.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import os, os.path as path
from tempfile import TemporaryDirectory
from typing import Text, Dict, Callable

from .steps import number_birds, number_birds_next
from .codegen import codegen


# Functions related to steps.
STEPS_FUNCTIONS = {
    "number-birds": (number_birds_next, None)
}

# First step to exexute.
FIRST_STEP = number_birds


def find_files(tmpdir: Text):
    "Find source files to submit."

    files = os.listdir(tmpdir)
    return [path.join(tmpdir, file) for file in files]



def save_cache(config: Dict):
    "Save the current config to the cache file."

    # TODO.



def step(config: Dict, submit: Callable):
    "Execute one single step and persist data."

    if "step" not in config:
        config["step"] = FIRST_STEP(config)

    (name, kargs) = config["step"]
    (nextstep, persist) = STEPS_FUNCTIONS[name]

    with TemporaryDirectory() as tmpdir:
        codegen(tmpdir, name, kargs)
        (rtime, numok) = submit(config, find_files(tmpdir))

    persist(config, rtime, **kargs)
    config["step"] = nextstep(config, **kargs)
    save_cache(config)
