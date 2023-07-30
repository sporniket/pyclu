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
    pathFromFileSpec,
)

source_dir = os.path.join(".", "tests", "data")
source_dir_expected = os.path.join(".", "tests", "data.expected")

source_files = [{"name": "ap-specs.json"}]

dest_files = [{"name": "environment"}, {"name": "ap.bash", "target_subdir": "zz_cli"}]


def test_that_it_generate_the_environment_file_to_source():
    tmp_dir = initializeTmpWorkspace(source_dir, source_files)

    baseArgs = ["prog"] + [pathFromFileSpec(tmp_dir, source_files[0])]
    with patch.object(sys, "argv", baseArgs):
        with redirect_stdout(io.StringIO()) as out:
            returnCode = PycluCli().run()
        assert returnCode == 0
        for f in dest_files:
            f_name = f["name"]
            pathActual = pathFromFileSpec(tmp_dir, f)
            assert os.path.exists(pathActual) and os.path.isfile(pathActual)
            assert filecmp.cmp(
                pathActual,
                os.path.join(source_dir_expected, f_name),
                shallow=False,
            )
        capturedOut = out.getvalue()
        print(capturedOut)
        assert capturedOut == f"File '{baseArgs[1]}' is deserializable.\n"
    shutil.rmtree(tmp_dir)


def test_that_it_reject_specification_files_without_json_extension():
    # prepare
    tmp_dir = makeTmpDirOrDie(time.time())
    spec_file = os.path.join(tmp_dir, "whatever")
    with open(spec_file, "w") as outfile:
        outfile.writelines(["whatever\n"])
    baseArgs = ["prog", spec_file]
    with patch.object(sys, "argv", baseArgs):
        # execute
        with redirect_stdout(io.StringIO()) as out:
            returnCode = PycluCli().run()
        # verify
        assert returnCode == 1
        capturedOut = out.getvalue()
        print(capturedOut)
        assert capturedOut == f"File '{baseArgs[1]}' is not deserializable.\n"
