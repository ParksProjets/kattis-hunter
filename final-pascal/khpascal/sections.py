"""

Pascal sections to be inserted in code.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

from typing import List


def gen_bird_array(envs: List, name: Text, etype: Text):
    "Generate a static array for bird directions / species."

    upper = name.capitalize()
    result = "k%s: array[0..5, 0..9, 0..19] of integer = (\n" % upper

    for i, e in enumerate(envs):
        result += " " * 4 + "(  // Environment %d.\n" % (i+1)
        for r in e["rounds"]:
            array = r[name] or []
            result += " " * 8 + "( " + ", ".join(map(str, r[name])) + " ),\n"
        result += " " * 4 + "),\n"

    result += ");\n"
    return result


def gen_species(R: List):
    "Generate envirnoment hashes."

    # TODO.


def gen_directions(R: List):
    "Generate envirnoment hashes."

    # TODO.



def gen_hashes(R: List):
    "Generate envirnoment hashes."

    # TODO.


def gen_target_scores(R: List):
    "Generate target scores."

    # TODO.
