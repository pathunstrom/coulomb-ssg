from pathlib import Path
from typing import Protocol


class Artifact(Protocol):
    route: Path
    name: str  #: Name to notify user of status.

    def write(self, absolute_path: Path) -> None:
        pass
