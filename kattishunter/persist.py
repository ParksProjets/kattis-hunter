"""

Persist data received after a submit.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

from math import floor
from typing import Dict, List, Text


def decode_base(value: int, size: int, base = 10):
    "Decode a value with the given base."

    result = []
    for _ in range(size):
        result.append(floor(value % base))
        value //= base

    return result


def write_slice(rounds: List, key: Text, values: List, N: int):
    "Write an array of values in a slice."

    index = 0
    for r in rounds:
        index += r["num-birds"]
        if index <= N:
            continue

        if r[key] is None:
            r[key] = [0] * r["num-birds"]
        for i in range(N - index + r["num-birds"], len(r[key])):
            r[key][i] = values.pop(0)
            if len(values) == 0:
                return
            N += 1



def persist_number_birds(config: Dict, rtime: int, N: int, E: int):
    "Persist data received for the number of birds."

    rounds = config["results"][E]["rounds"]
    values = decode_base(rtime // 4, 2, 20)

    rounds[N]["num-birds"] = values[0] + 1
    rounds[N+1]["num-birds"] = values[1] + 1


def persist_species(config: Dict, rtime: int, N: int, E: int):
    "Persist bird species."

    rounds = config["results"][E]["rounds"]
    values = decode_base(rtime // 4, 3, 6)
    write_slice(rounds, "species", values, N)


def persist_directions(config: Dict, rtime: int, N: int, E: int):
    "Persist bird directions."

    rounds = config["results"][E]["rounds"]
    values = decode_base(rtime // 2, 3, 9)
    write_slice(rounds, "directions", values, N)


def persist_envhash(config: Dict, rtime: int, N: int, E: int):
    "Persist environment hash."

    env = config["results"][E]
    if env.get("hash", 0) == 0:
        env["hash"] = env["rounds"][0]["num-birds"]

    values = decode_base(rtime // 10, 2, 9)
    for i, v in enumerate(values):
        env["hash"] += v << ((i+N) * 4 + 5)

    if (N+2) >= env["rounds"][0]["num-birds"]:
        env["done"] = True
