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
from typing import Dict, List

from .variable import CluResVariable


class CluResEnv:
    def __init__(self, variables: Dict[str, CluResVariable], pathes: List[str]):
        self.variables = variables
        self.pathes = pathes
        self.orderOfVariables = self.computeOrderOfVariables()

    def accumulateDependencies(
        self, known: List[str], requested: str, *, pending: List[str] = []
    ) -> List[str]:
        unknown = ()
        if requested in known:
            # nothing to do
            return known
        elif requested in pending:
            # cyclic dependency detected, break the cycle
            return known + [requested]
        else:
            subrequest = self.variables[requested].required
            result = known.copy()
            for subrequested in subrequest:
                subpending = (
                    pending
                    + [requested]
                    + [p for p in subrequest if p != subrequested and p not in pending]
                )
                result = self.accumulateDependencies(
                    result, subrequested, pending=subpending
                )
            return result if requested in result else result + [requested]

    def computeOrderOfVariables(self) -> List[str]:
        """Assess the order in which variables SHOULD be declared.

        Returns:
            List[str]: the ordered list of variables.
        """
        result = []
        for v in self.variables:
            result = self.accumulateDependencies(result, v)

        return result
