import dataclasses
from pathlib import Path
from typing import (
    Any,
    Callable,
    Protocol,
    Iterable,
    Union,
    NewType,
    TypeVar,
    Generic,
    Type,
    Optional,
)


class Artifact(Protocol):
    """
    An object that can be written to a path.

    route: Sub-path from project root.
           (Most useful for views that produce more than one artifact.)
           Should not include file name
    """

    route: Path

    @property
    def name(self) -> str:
        """The name of the artifact, used for notifying the user of the status."""
        return ""  # This is useless, but makes PyCharm happier.

    def write(self, absolute_path: Path) -> None:
        """Write the data to the file given by absolute_path"""
        pass


class ArtifactGenerator(Protocol):
    """An object that can generate artifacts."""

    def generate_artifacts(
        self, context: dict[str, Any], templating_engine: Any
    ) -> Iterable[Artifact]:
        pass


@dataclasses.dataclass
class ForEach:
    resource: Union[Iterable[Any], "Dynamic"]
    key: str


class ViewProtocol(ArtifactGenerator, Protocol):
    context: dict[str, Any]
    path: str
    for_each: Union[ForEach, None]


@dataclasses.dataclass
class PathComponent:
    resource_field: str
    format_field: Union[str, None] = None
    transform: Union[Callable[[Any], str], None] = None


Content = NewType("Content", str)


QueryType = TypeVar("QueryType", bound=Union[type, str])


@dataclasses.dataclass
class Dynamic(Generic[QueryType]):
    model: Type[QueryType]
    filter: Callable[[QueryType], bool] = lambda x: True  # noqa: E731
    sort_key: Optional[Callable[[QueryType], Any]] = None
    single: bool = False
