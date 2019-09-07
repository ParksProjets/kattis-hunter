"""

Generate C++ code for the final code.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

from typing import List, Text


def gen_bird_array(envs: List, name: Text, etype: Text):
    "Generate a static array for birds."

    upper = name.capitalize()
    result = "using Env%s = std::vector<%s>[10];\n" % (upper, etype)
    result += "Env%s kAll%s[%d] = {\n" % (upper, upper, len(envs))

    for i, e in enumerate(envs):
        result += " " * 4 + "{  // Environment %d.\n" % (i+1)
        for r in e["rounds"]:
            result += " " * 8 + "{" + ", ".join(r[name]) + "},\n"
        result += " " * 4 + "},\n"

    result += "}\n"


def answer_static(R: List, **kargs):
    "Static code for the final code."

    result = gen_bird_array(R, "directions", "EMovement") + "\n"
    result += gen_bird_array(R, "species", "ESpecies")



def answer_guess(R: List, **kargs):
    "Guess function for the final code."

    # TODO.
