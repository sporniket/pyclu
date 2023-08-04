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
from ..pyclu_types import CluRes


def generateExportVariables(context: CluRes) -> str:
    result = []
    for v in context.cli.env.orderOfVariables:
        result += [
            f"""{v}="$(get_real_path "{context.cli.env.variables[v].relativeValue}")\"""",
            f"""export {v}""",
        ]
    return "\n".join(result)


def generateEnvironmentLines(context: CluRes) -> List[str]:
    content = f"""#!/usr/bin/bash
if [ "${{BASH_SOURCE-}}" = "$0" ]; then
    echo "You must source this script: \$ source $0" >&2
    exit 1
fi

########[BEGIN PATH management]########

## Get the absolute path of the given filename.
#
# Use `realpath` command if it exists, else use a combination of `cd` and `pwd`.
# see https://stackoverflow.com/a/21188136/8918845 for the source of the later.
#
# $1 : relative filename
#
# Returns : the absolute path of the file name.
get_real_path() {{
  filename=$1
  parentdir=$(dirname "${{filename}}")
  actual_realpath=$(which realpath)
  if [ -n "$actual_realpath" ]; then
    realpath "${{filename}}"
  elif [ -d "${{filename}}" ]; then
    echo "$(cd "${{filename}}" && pwd)"
  elif [ -d "${{parentdir}}" ]; then
    echo "$(cd "${{parentdir}}" && pwd)/$(basename "${{filename}}")"
  fi
}}

## Utility to restore previous path.
#
# It is expected that the previous value for $PATH is stored into $_OLD_ENVIRONMENT_PATH
deactivate () {{
    # reset old environment variables
    # ! [ -z ${{VAR+_}} ] returns true if VAR is declared at all
    if ! [ -z "${{_OLD_ENVIRONMENT_PATH:+_}}" ] ; then
        PATH="$_OLD_ENVIRONMENT_PATH"
        export PATH
        unset _OLD_ENVIRONMENT_PATH
    fi

    # This should detect bash and zsh, which have a hash command that must
    # be called to get it to forget past commands.  Without forgetting
    # past commands the $PATH changes we made may not be respected
    if [ -n "${{BASH-}}" ] || [ -n "${{ZSH_VERSION-}}" ] ; then
        hash -r 2>/dev/null
    fi

    if [ ! "${{1-}}" = "nondestructive" ] ; then
    # Self destruct!
        unset -f deactivate
    fi
}}

# restore initial PATH
deactivate nondestructive

# add CLI_DIR into the path
{generateExportVariables(context)}
_OLD_ENVIRONMENT_PATH="$PATH"
export _OLD_ENVIRONMENT_PATH
PATH="${{CLI_DIR}}:{":".join(context.cli.env.pathes)}:${{PATH}}"
export PATH

# remove utility functions
unset -f deactivate
unset -f get_real_path

#-------[END PATH management]-------#

alias {context.cli.metadata.command}='{context.cli.metadata.command}.bash'
"""
    return content.splitlines()
