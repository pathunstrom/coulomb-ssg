import dataclasses
import os
import pathlib
import typing
from typing import Any, Iterable, Union, overload, Callable, Optional, Tuple, cast

import jinjax

import coulomb.utils
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
GenericModel = typing.TypeVar("GenericModel", bound=type)
PathLike = Union[str, os.PathLike]


@dataclasses.dataclass
class Site:
    views: list[coulomb.types.ViewProtocol] = dataclasses.field(default_factory=list)
    models: list[Tuple[type, PathLike]] = dataclasses.field(default_factory=list)
    context: dict[str, Any] = dataclasses.field(default_factory=dict)
    discover_html: bool = False
    component_path: pathlib.Path = pathlib.Path.cwd() / "components"
    base_path: PathLike = pathlib.Path(".")  # Creates no folder in the output path.

    def generate_artifacts(
        self, source_dir: pathlib.Path
    ) -> Iterable[coulomb.types.Artifact]:
        catalog = jinjax.Catalog()
        catalog.add_folder(self.component_path)

        for view in self.views:
            yield from view.generate_artifacts(self.context, catalog)

        if self.discover_html:
            yield from HTMLDiscoveryView(path=str(source_dir)).generate_artifacts(
                self.context, catalog
            )

    def register_view(self, view: GenericView) -> GenericView:
        self.views.append(typing.cast(coulomb.types.ViewProtocol, view))
        return view

    @overload
    def register_model(self, model_or_path: GenericModel) -> GenericModel:
        """Decorator without path form."""

    @overload
    def register_model(
        self, model_or_path: PathLike
    ) -> Callable[[GenericModel], GenericModel]:
        """Register a model with a custom path as a decorator."""

    @overload
    def register_model(
        self, model_or_path: GenericModel, path: PathLike
    ) -> GenericModel:
        """Register a model post instantiation with a custom path."""

    def register_model(
        self,
        model_or_path: Union[GenericModel, PathLike],
        path: Optional[PathLike] = None,
    ) -> Union[GenericModel, Callable[[GenericModel], GenericModel]]:
        if isinstance(model_or_path, (os.PathLike, str, bytes)):
            if path is not None:
                raise ValueError("Cannot pass path as both arguments.")
            path = model_or_path

            def register_model_closure(model: GenericModel) -> GenericModel:
                self.models.append((model, cast(PathLike, path)))
                return model

            return register_model_closure
        elif isinstance(model_or_path, type):
            model = model_or_path
            if path is None:
                path = coulomb.utils.camel_to_snake(model.__name__)

            self.models.append((model, path))
            return model
        raise ValueError("Model or path required.")
