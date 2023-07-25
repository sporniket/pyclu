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
import time
import sys
import io
from typing import List, Union, Optional

from unittest.mock import patch
from contextlib import redirect_stdout

from pyclu import PycluCli

from .utils import (
    makeTmpDirOrDie,
    assert_that_source_is_converted_as_expected,
    initializeTmpWorkspace,
)

source_dir = os.path.join(".", "tests", "data")
source_dir_expected = os.path.join(".", "tests", "data.expected")

source_files = ["ap-specs.json"]

dest_files = ["environment"]


def test_that_it_generate_the_environment_file_to_source():
    tmp_dir = initializeTmpWorkspace(
        [os.path.join(source_dir, f) for f in source_files]
    )
    baseArgs = ["prog"] + [os.path.join(tmp_dir, source) for source in source_files]
    with patch.object(sys, "argv", baseArgs):
        with redirect_stdout(io.StringIO()) as out:
            returnCode = PycluCli().run()
        assert returnCode == 0
        assert (
            out.getvalue()
            == f"File '{os.path.join(tmp_dir, source_files[0])}' is deserializable.\n"
        )
        for f in dest_files:
            pathActual = os.path.join(tmp_dir, f)
            assert os.path.exists(pathActual) and os.path.isfile(pathActual)
            assert filecmp.cmp(
                pathActual,
                os.path.join(source_dir_expected, f),
                shallow=False,
            )
    shutil.rmtree(tmp_dir)
