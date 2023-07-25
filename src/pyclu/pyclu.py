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


from .pyclu_types import CluRes, CluResCli, CluResMetadata


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
        serialized = "".join(s.readlines())
        clu = self.deserialize(serialized)
        outdir = os.path.dirname(s.name)
        outfile_env = os.path.join(outdir, "environment")
        with open(outfile_env, "w") as outfile:
            self.writeLinesWithSeparator(
                outfile,
                [
                    "#!/usr/bin/bash",
                    "",
                    f"alias {clu.cli.metadata.command}='echo \"this will be the command {clu.cli.metadata.name}\"'",
                ],
            )
        # do stuff...
        return 0

    def deserialize(self, jsonSource: str) -> CluRes:
        tree = json.loads(jsonSource)
        tree_metadata = tree["cli"]["metadata"]
        return CluRes(
            CluResCli(
                CluResMetadata(
                    tree_metadata["command"],
                    tree_metadata["name"],
                    tree_metadata["version"],
                )
            )
        )

    def writeLinesWithSeparator(self, out, lines: List[str]):
        """
        This utilities wraps ``out.writelines(line + '\n' for line in lines)``.

        Python breaks my expectations regarding semantics of what is a line of text.

        As a Java developper, I expect line separator to be NOT part of a line (noise). Python expect line separator to be part of a line (signal).
        """
        out.writelines(line + "\n" for line in lines)
