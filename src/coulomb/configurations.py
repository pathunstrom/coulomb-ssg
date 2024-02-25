import contextlib
import dataclasses
import importlib.util
import os
import pathlib
import sys
from typing import Iterable

import jinjax

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


def get_configuration_object(path: pathlib.Path, settings_object: str = "site") -> Site:
    if not path.exists():
        raise ValueError("Configuration path must exist.")
    if path.is_dir():
        directory = path
        path = path / "settings.py"
    elif path.is_file():
        directory = path.parent
    else:
        raise RuntimeError(
            "Your path is neither a file or directory. This seems unlikely."
        )

    @contextlib.contextmanager
    def temporarily_change_directories(_path):
        current_directory = pathlib.Path.cwd()
        os.chdir(_path)
        yield
        os.chdir(current_directory)

    with temporarily_change_directories(directory):
        spec = importlib.util.spec_from_file_location("coulomb_user_settings", path)
        if spec is None:
            raise RuntimeError("Importlib error - spec failed")
        module = importlib.util.module_from_spec(spec)
        if module is None:
            raise RuntimeError("Could not import user settings module.")

        sys.modules["coulomb_user_settings"] = module

        loader = spec.loader
        if loader is None:
            raise RuntimeError("Module loader doesn't exist.")
        loader.exec_module(module)
        try:
            return getattr(module, settings_object)
        except AttributeError as err:
            message = f"Configuration object {settings_object} does not exist in settings file."
            raise ValueError(message) from err
