"""
---
(c) 2023 David SPORN
---
This is part of pyclu by sporniket.

pyclu by sporniket is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

pyclu by sporniket is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with pyclu by sporniket.
If not, see <https://www.gnu.org/licenses/>. 
---
"""

import filecmp
import os
import shutil
import sys
import time

from typing import List
from unittest.mock import patch


def makeTmpDirOrDie(suffix: str = None) -> str:
    newdir = os.path.join(".", f"tmp.{suffix}" if suffix != None else "tmp")
    if os.path.exists(newdir):
        if os.path.isdir(newdir):
            return newdir
        raise (ResourceWarning(f"{newdir} is not a directory"))
    os.mkdir(newdir)
    return newdir


def initializeTmpWorkspace(source_dir, files) -> str:
    tmp_dir = makeTmpDirOrDie(time.time())
    for file in files:
        file_name = file["name"]
        file_source = os.path.join(source_dir, file_name)
        target_dir = (
            os.path.join(tmp_dir, file["target_subdir"])
            if "target_subdir" in file
            else tmp_dir
        )
        shutil.copy(file_source, target_dir)
    return tmp_dir


def assert_that_source_is_converted_as_expected(pathActual: str, pathExpected: str):
    assert filecmp.cmp(pathActual, pathExpected, shallow=False)


def pathFromFileSpec(base_dir, file_specs):
    return (
        os.path.join(base_dir, file_specs["target_subdir"], file_specs["name"])
        if "target_subdir" in file_specs
        else os.path.join(base_dir, file_specs["name"])
    )
