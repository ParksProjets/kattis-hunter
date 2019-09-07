"""

Generate C++ code.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import os.path as path
import re
import textwrap
from functools import partial
from typing import Text, List, Dict, Any

from .general import HEADERS, ATTRIBUTES, STATIC_CODE
from .birds import (num_birds_shoot, species_guess, species_reveal,
    directions_shoot)
from .envskip import (envhash_shoot, envhash_static, ENVSKIP_STATIC,
    ENVSKIP_SHOOT, ENVSKIP_GUESS, ENVSKIP_REVEAL)


# All general sections that can be generated.
GENERAL_SECTIONS = {
    "HEADERS": HEADERS,
    "ATTRIBUTES": ATTRIBUTES,
    "STATIC_CODE": STATIC_CODE,
    "STATIC_CODE_ENVHASH": envhash_static,
    "STATIC_CODE_SKIP": ENVSKIP_STATIC,
    "SHOOT_SKIP": ENVSKIP_SHOOT,
    "GUESS_SKIP": ENVSKIP_GUESS,
    "REVEAL_SKIP": ENVSKIP_REVEAL
}

# Sections for all steps.
STEP_SECTIONS = {
    "number-birds": {
        "SHOOT": num_birds_shoot,
    },
    "species": {
        "GUESS": species_guess,
        "REVEAL": species_reveal,
    },
    "env-hash": {
        "SHOOT": envhash_shoot,
    },
    "directions": {
        "SHOOT": directions_shoot,
    },
    "answer": {
        "STATIC_CODE_SKIP": None,  # Don't use env skip in final code.
        "SHOOT_SKIP": None,
        "GUESS_SKIP": None,
        "REVEAL_SKIP": None
    }
}


# Source files to use.
SOURCES = ("Player.hpp", "Player.cpp")

# Regex for replacing sections.
RE_SECTION = re.compile(r"^( *)/\*{([A-Z _-]+)}\*/ *\n", re.M)



def replace_section(stepsec: Dict, kargs: Dict, match):
    "Function that replace a section header by its contents."

    (name, indent) = (match.group(2), match.group(1))

    if name in stepsec:
        section = stepsec.get(name)
    else:
        section = GENERAL_SECTIONS.get(name)

    if section and not isinstance(section, str):
        section = section(**kargs)

    if section is None:
        return ""  # Section not found, delete the header.

    section = textwrap.dedent(section).strip()
    return textwrap.indent(section, indent) + "\n"



def gen_source(infile: Text, outfile: Text, stepsec: Dict, kargs: Dict):
    "Generate a single source file."

    with open(infile) as file:
        content = file.read()

    subfunc = partial(replace_section, stepsec, kargs)
    content = RE_SECTION.sub(subfunc, content)

    with open(outfile, "w") as file:
        file.write(content)



def codegen(outdir: Text, step: Text, kargs: Dict):
    "Generate source files for the given step."

    assets = path.join(path.dirname(__file__), "..", "assets")
    stepsec = STEP_SECTIONS[step]

    for source in SOURCES:
        infile = path.join(assets, source)
        outfile = path.join(outdir, source)
        gen_source(infile, outfile, stepsec, kargs)
