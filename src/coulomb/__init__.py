"""
Coulomb is a static site generator.
"""

from coulomb.types import Artifact
from coulomb.configurations import Site, TemplatedView, StaticFolderView
from coulomb.types import PathComponent, ForEach, Content, Dynamic

__all__ = [
    "Artifact",
    "Content",
    "Dynamic",
    "ForEach",
    "PathComponent",
    "Site",
    "StaticFolderView",
    "TemplatedView",
]
