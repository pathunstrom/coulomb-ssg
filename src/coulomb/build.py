from pathlib import Path
from typing import Protocol


class Artifact(Protocol):
    route: Path

    @property
    def name(self) -> str:
        pass

    def write(self, absolute_path: Path) -> None:
        pass
