"""

Functions for getting step data.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

from typing import Dict


def number_birds(config: Dict, E = 0):
    "Step for getting the number of birds."

    return ("number-birds", dict(N = 0, E = E))


def number_birds_next(config: Dict, N = 0, E = 0):
    "Get the step to execute next after getting the number of birds."

    if N == 8:  # Go to step 2.
        return species(config, E)
    else:
        return ("number-birds", dict(N = N+2, E = E))



def species(config: Dict, E = 0):
    "Step for getting species of all birds of env."

    env = config["results"][E]
    env["num-birds"] = sum(r["num-birds"] for r in env["rounds"])

    return ("species", dict(N = 0, E = E))


def species_next(config: Dict, N = 0, E = 0):
    "Step for getting species of all birds of env."

    if N == 8:  # Go to step 2.
        return None  # TODO.
    else:
        return ("species", dict(N = N+3, E = E))
