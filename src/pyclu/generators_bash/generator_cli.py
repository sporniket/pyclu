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
from typing import List
from ..types import CluRes


def generateCliLines(context: CluRes) -> List[str]:
    content = f"""#!/usr/bin/env bash

ap_help() {{
  cli_name=${{0##*/}}
  echo -e "
\e[90m${{cli_name}}\e[0m
\e[90m---===<{{\e[93m{context.cli.metadata.command}\e[96m, {context.cli.metadata.name} -- version {context.cli.metadata.version}\e[90m}}>===---\e[0m

\e[96mUsage:\e[0m ${{cli_name}} \e[93m[command]\e[0m
\e[96mCommands:\e[0m
  \e[93m*\e[0m         Help
"
  exit 1
}}

case "$1" in
  *)
    ap_help
    ;;
esac
"""
    return content.splitlines()
