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
from typing import Dict, List, Tuple
import re


class CluResVariable:
    def __init__(self, name: str, definition: str, *, actualValue=None):
        self.name = name
        self.definition = definition
        self.actualValue = actualValue
        # all variables SHOULD be expressed as a relative to base directory
        # BASEDIR = location (dirname) of the spec file
        self.relativeValue = definition.replace("${BASEDIR}", ".")
        self.expanded = False if self.actualValue is None else True
        self.required = self.computeRequirements()
        # print("new", self.dump())
        # TODO spot '${xxx}' and register 'xxx' as required variable
        # TODO checks whether a list of names contains all of the requirements
        # TODO apply all the required values to the definition to get the actual value

    def computeRequirements(self) -> Tuple[str]:
        """Compute the list of variables depended upon.

        Except BASEDIR that will be a builtin, this will allow to order the output of variables declarations.

        Returns:
            Tuple[str]: the list of variables except "BASEDIR" that MUST be declared before this variable
        """
        result = ()
        variableMatcher = re.compile("[$][{]([_0-9A-Za-z]+)[}]")
        searchFrom = 0
        while searchFrom < len(self.definition):
            match = variableMatcher.search(self.definition, searchFrom)
            if match:
                found = match.group(1)
                if found != "BASEDIR":
                    result += (found,)
                searchFrom = match.endpos
            else:
                searchFrom = len(self.definition)
        return result

    def dump(self) -> str:
        return f"var: '{self.name}':='{self.definition}', expanded:{self.expanded} <- '{self.actualValue}' ; '{self.relativeValue}'"

    def isExpanded(self) -> bool:
        return self.expanded

    def expand(self, vars) -> bool:
        # print("calling expand on", self.dump())
        if self.isExpanded():
            # print("already expanded")
            return self.isExpanded()
        if "BASEDIR" in vars:
            self.actualValue = self.definition.replace(
                "${BASEDIR}", vars["BASEDIR"].actualValue
            )
            self.expanded = True
            # print("expanded ", self.dump())
        return self.isExpanded()
