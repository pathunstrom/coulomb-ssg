"""
Coulomb is a static site generator.
"""

import coulomb.configurations
import coulomb.build

from coulomb.build import Artifact
from coulomb.configurations import Site


__all__ = [
    "Artifact",
    "Site",
]
