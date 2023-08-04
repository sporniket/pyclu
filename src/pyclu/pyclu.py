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
from argparse import ArgumentParser, RawDescriptionHelpFormatter, FileType
from typing import List

import json
import os
from pathlib import Path


from .pyclu_types import CluRes, CluResCli, CluResMetadata, CluResVariable, CluResEnv
from .generators_bash import generateEnvironmentLines


def createArgParser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="python3 -m pyclu",
        description="Generate a custom command line.",
        epilog="""---
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
""",
        formatter_class=RawDescriptionHelpFormatter,
        allow_abbrev=False,
    )

    # Add the arguments
    parser.add_argument(
        "source",
        metavar="<source file>",
        type=FileType(),
        help="a JSON file describing a command-line to generate",
    )

    return parser


class PycluCli:
    def run(self) -> int:
        self.args = args = createArgParser().parse_args()
        s = args.source
        if s.name.endswith(".json"):
            print(f"File '{s.name}' is deserializable.")
        else:
            print(f"File '{s.name}' is not deserializable.")
            return 1
        serialized = "".join(s.readlines())
        clu = self.deserialize(serialized)
        outdir = os.path.dirname(s.name)
        clu.cli.env.variables["BASEDIR"] = CluResVariable(
            "BASEDIR", outdir, actualValue=outdir
        )
        for var in clu.cli.env.variables:
            clu.cli.env.variables[var].expand(clu.cli.env.variables)
        Path(clu.cli.env.variables["CLI_DIR"].actualValue).mkdir(
            parents=True, exist_ok=True
        )
        outfile_script_main = os.path.join(
            clu.cli.env.variables["CLI_DIR"].actualValue,
            f"{clu.cli.metadata.command}.bash",
        )
        with open(outfile_script_main, "w") as outfile:
            self.writeLinesWithSeparator(
                outfile,
                [
                    "#!/usr/bin/bash",
                    "",
                    f'echo "this will be the command {clu.cli.metadata.name}"',
                ],
            )
        outfile_env = os.path.join(outdir, "environment")
        with open(outfile_env, "w") as outfile:
            self.writeLinesWithSeparator(
                outfile,
                generateEnvironmentLines(clu),
            )
        # do stuff...
        return 0

    def deserialize(self, jsonSource: str) -> CluRes:
        tree = json.loads(jsonSource)
        tree_metadata = tree["cli"]["metadata"]
        tree_env = tree["cli"]["env"]
        tree_vars = {
            name: CluResVariable(name, tree_env["variables"][name])
            for name in tree_env["variables"]
        }
        list_pathes = [] if tree_env["pathes"] is None else tree_env["pathes"]
        return CluRes(
            CluResCli(
                CluResMetadata(
                    tree_metadata["command"],
                    tree_metadata["name"],
                    tree_metadata["version"],
                ),
                CluResEnv(tree_vars, list_pathes),
            )
        )

    def writeLinesWithSeparator(self, out, lines: List[str]):
        """
        This utilities wraps ``out.writelines(line + '\n' for line in lines)``.

        Python breaks my expectations regarding semantics of what is a line of text.

        As a Java developper, I expect line separator to be NOT part of a line (noise). Python expect line separator to be part of a line (signal).
        """
        out.writelines(line + "\n" for line in lines)
