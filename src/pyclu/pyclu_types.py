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
from typing import Dict


class CluResMetadata:
    def __init__(self, command: str, name: str, version: str):
        self.command = command
        self.name = name
        self.version = version


class CluResVariable:
    def __init__(self, name: str, definition: str, *, actualValue=None):
        self.name = name
        self.definition = definition
        self.actualValue = actualValue
        self.relativeValue = definition.replace("${BASEDIR}", ".")
        self.expanded = False if self.actualValue is None else True
        # print("new", self.dump())
        # TODO spot '${xxx}' and register 'xxx' as required variable
        # TODO checks whether a list of names contains all of the requirements
        # TODO apply all the required values to the definition to get the actual value

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


class CluResCli:
    def __init__(self, metadata: CluResMetadata, variables: Dict[str, CluResVariable]):
        self.metadata = metadata
        self.variables = variables


class CluRes:
    def __init__(self, cli: CluResCli):
        self.cli = cli
