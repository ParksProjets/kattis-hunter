"""

Pascal sections to be inserted in code.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

from typing import List, Text


def gen_bird_array(envs: List, name: Text):
    "Generate a static array for bird directions / species."

    upper = name.capitalize()
    count = sum(int("same-as" not in e) for e in envs)

    result = "k%s: array[0..%d, 0..9, 0..19] of integer = (" % (
        upper, count-1)

    for i, e in enumerate(envs):
        if e.get("same-as"): continue
        result += "\n" + " " * 4 + "(  // Environment %d. " % (i+1)

        for r in e["rounds"]:
            array = r[name] or []
            array += [9] * (20 - len(array))
            result += "\n" + " " * 8 + "(" + ", ".join(map(str, array)) + "),"
        result = result[:-1] + "\n"        
        result += " " * 4 + "),"

    return result[:-1] + "\n);\n"


def gen_species(R: List, **kargs):
    "Generate envirnoment hashes."

    return gen_bird_array(R, "directions")


def gen_directions(R: List, **kargs):
    "Generate envirnoment hashes."

    return gen_bird_array(R, "species")



def gen_hashes(R: List, **kargs):
    "Generate envirnoment hashes."

    count = sum(int("same-as" not in e) for e in R)
    hashes = (str(e.get("hash", 0)) for e in R if "same-as" not in e)

    result = "kEnvHashes: array[0..%d] of uint64 = (\n    " % (count-1)
    result += ", ".join(hashes)
    result += "\n);"

    return result


def gen_target_scores(R: List, Scores: List[int], **kargs):
    "Generate target scores."

    count = sum(int("same-as" not in e) for e in R)

    result = "kTargetScores: array[0..%d] of integer = (" % (count-1)
    result += ", ".join(str(s) for s in Scores)
    result += ");"

    return result
