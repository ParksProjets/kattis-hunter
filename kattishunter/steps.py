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
    "Get the step to execute next after getting species."

    env = config["results"][E]
    if (N+3) >= env["num-birds"]:  # Go to step 3.
        return directions(config, E)
    else:
        return ("species", dict(N = N+3, E = E))



def directions(config: Dict, E = 0):
    "Step for getting bird directions."

    return ("directions", dict(N = 0, E = E))


def directions_next(config: Dict, N = 0, E = 0):
    "Get the step to execute next after getting directions."

    env = config["results"][E]
    if (N+3) >= env["num-birds"]:  # Go to step 4.
        return envhash(config, E)
    else:
        return ("directions", dict(N = N+3, E = E))



def envhash(config: Dict, E = 0):
    "Step for getting environment hash."

    return ("env-hash", dict(N = 0, E = E))


def envhash_next(config: Dict, N = 0, E = 0):
    "Get the step to execute next after getting environment hash."

    env = config["results"][E]
    nenv = int(config["problem"]["number-of-env"])

    if (N+2) < env["rounds"][0]["num-birds"]:
        return ("env-hash", dict(N = N+2, E = E))
    elif (E+1) < nenv:  # Go to step 1 of next env.
        return number_birds(config, E = E+1)
    else:  # Done!
        return None
