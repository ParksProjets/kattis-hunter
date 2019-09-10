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


# Sections to replace.
SECTIONS = {
    "HASHES": 
}


# Regex for replacing sections.
RE_SECTION = re.compile(r"^( *)/\*{([A-Z _-]+)}\*/ *\n", re.M)


def replace_section(stepsec: Dict, kargs: Dict, match):
    "Function that replace a section header by its contents."

    (name, indent) = (match.group(2), match.group(1))
    section = SECTIONS.get(name)

    if section is None:
        return ""  # Section not found, delete the header.
    if section and not isinstance(section, str):
        section = section(**kargs)

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
