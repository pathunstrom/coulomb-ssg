import dataclasses
import pathlib
from typing import Iterable

import jinjax

import coulomb
import coulomb.build


@dataclasses.dataclass
class HTMLWriter:
    route: pathlib.Path
    content: str

    def write(self, path: pathlib.Path):
        path.write_text(self.content)

    @property
    def name(self) -> str:
        return f"HTMLPath - {self.route}"


@dataclasses.dataclass
class JinjaxRoute:
    route: pathlib.Path
    template: str
    name: str


@dataclasses.dataclass
class Site:
    views: list[JinjaxRoute] = dataclasses.field(default_factory=list)
    discover_html: bool = False
    component_path: pathlib.Path = pathlib.Path.cwd() / "components"
    # data models
    #

    def generate_artifacts(
        self, source_dir: pathlib.Path
    ) -> Iterable[coulomb.build.Artifact]:
        catalog = jinjax.Catalog()
        catalog.add_folder(self.component_path)
        for view in self.views:
            rendered = catalog.render(view.template, name=view.name)
            yield HTMLWriter(route=view.route, content=rendered)
        if self.discover_html:
            for file_path in source_dir.glob("**/*.html"):
                output_path = file_path.relative_to(source_dir)
                static_html = file_path.read_text()
                yield HTMLWriter(output_path, static_html)
