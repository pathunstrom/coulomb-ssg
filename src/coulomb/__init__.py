"""
Coulomb is a static site generator.
"""

from coulomb.types import Artifact
from coulomb.configurations import Site, TemplatedView, StaticFolderView
from coulomb.types import PathComponent, ForEach, Content

__all__ = [
    "Artifact",
    "Content",
    "ForEach",
    "PathComponent",
    "Site",
    "StaticFolderView",
    "TemplatedView",
]
