"""
Coulomb is a static site generator.
"""

from coulomb.types import Artifact
from coulomb.configurations import Site, TemplatedView, StaticFolderView
from coulomb.types import PathComponent, ForEach

__all__ = [
    "Artifact",
    "ForEach",
    "PathComponent",
    "Site",
    "StaticFolderView",
    "TemplatedView",
]
