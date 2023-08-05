"""
Classes that are merely structs for now.
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

from .environment import CluResEnv


class CluResMetadata:
    def __init__(self, command: str, name: str, version: str):
        self.command = command
        self.name = name
        self.version = version


class CluResCli:
    def __init__(self, metadata: CluResMetadata, env: CluResEnv):
        self.metadata = metadata
        self.env = env


class CluRes:
    def __init__(self, cli: CluResCli):
        self.cli = cli
