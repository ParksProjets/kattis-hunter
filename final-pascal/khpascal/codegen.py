"""

Generate Pascal code.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import os.path as path
import re
import textwrap
from functools import partial
from typing import Text, List, Dict, Any

from .sections import gen_directions, gen_species, gen_hashes, gen_target_scores


# Sections to replace.
SECTIONS = {
    "TARGET SCORES": gen_target_scores,
    "HASHES": gen_hashes,
    "DIRECTIONS": gen_directions,
    "SPECIES": gen_species
}


# Regex for replacing sections.
RE_SECTION = re.compile(r"^( *){\(([A-Z _-]+)\)} *\n", re.M)


def replace_section(kargs: Dict, match):
    "Function that replace a section header by its contents."

    (name, indent) = (match.group(2), match.group(1))
    section = SECTIONS.get(name)

    if section is None:
        return ""  # Section not found, delete the header.
    if section and not isinstance(section, str):
        section = section(**kargs)

    section = textwrap.dedent(section).strip()
    return textwrap.indent(section, indent) + "\n"



def codegen(infile: Text, outfile: Text, kargs: Dict):
    "Generate a single source file."

    with open(infile) as file:
        content = file.read()

    subfunc = partial(replace_section, kargs)
    content = RE_SECTION.sub(subfunc, content)

    with open(outfile, "w") as file:
        file.write(content)
