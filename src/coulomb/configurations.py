import dataclasses
import pathlib
import typing
from typing import Any, Iterable, Union

import jinjax

import coulomb.types


@dataclasses.dataclass
class TemplatedView:
    path: str
    template: str
    context: dict[str, Any] = dataclasses.field(default_factory=dict)
    for_each: Union[coulomb.types.ForEach, None] = None

    def generate_artifacts(
        self, context: dict[str, Any], templating_engine
    ) -> Iterable[coulomb.types.Artifact]:
        merged_context = context | self.context
        if self.for_each is None:
            content = templating_engine.render(self.template, **merged_context)
            yield HTMLWriter(
                pathlib.Path(self.path.format(**merged_context)), content=content
            )


@dataclasses.dataclass
class HTMLDiscoveryView:
    path: str
    context: dict[str, Any] = dataclasses.field(default_factory=dict)
    for_each = None

    def generate_artifacts(
        self, context: dict[str, Any], templating_engine
    ) -> Iterable[coulomb.types.Artifact]:
        source_dir = pathlib.Path(self.path)
        for file_path in source_dir.glob("**/*.html"):
            output_path = file_path.relative_to(source_dir)
            static_html = file_path.read_text()
            yield HTMLWriter(output_path, static_html)


@dataclasses.dataclass
class StaticFolderView:
    path: str
    src_dir: pathlib.Path
    context: dict[str, Any] = dataclasses.field(default_factory=dict)
    for_each = None

    def generate_artifacts(
        self, context: dict[str, Any], templating_engine: Any
    ) -> Iterable[coulomb.types.Artifact]:
        return NotImplemented


@dataclasses.dataclass
class HTMLWriter:
    route: pathlib.Path
    content: str

    def write(self, path: pathlib.Path):
        path.write_text(self.content)

    @property
    def name(self) -> str:
        return f"HTMLPath - {self.route}"


GenericView = typing.TypeVar("GenericView", bound=coulomb.types.ViewProtocol)


@dataclasses.dataclass
class Site:
    views: list[coulomb.types.ViewProtocol] = dataclasses.field(default_factory=list)
    discover_html: bool = False
    component_path: pathlib.Path = pathlib.Path.cwd() / "components"

    def generate_artifacts(
        self, source_dir: pathlib.Path
    ) -> Iterable[coulomb.types.Artifact]:
        catalog = jinjax.Catalog()
        catalog.add_folder(self.component_path)

        for view in self.views:
            yield from view.generate_artifacts({}, catalog)

        if self.discover_html:
            yield from HTMLDiscoveryView(path=str(source_dir)).generate_artifacts(
                {}, catalog
            )

    def register_view(self, view: GenericView) -> GenericView:
        self.views.append(typing.cast(coulomb.types.ViewProtocol, view))
        return view
