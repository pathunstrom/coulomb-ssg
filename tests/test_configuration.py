import dataclasses
import pathlib
import typing
from typing import Any, Iterable

import pytest

import coulomb.processors
from coulomb import Artifact


def test_get_configuration_object__directory():
    """
    Simulates calling get_configuration_object when the provided path is a directory.

    Will be the basic operation when calling `coulomb build` without a settings flag.
    """
    project_path = pathlib.Path(__file__).parent / "projects" / "just-settings"

    site_object = coulomb.processors.get_configuration_object(project_path)
    assert site_object == coulomb.Site()


def test_get_configuration_object__default_file():
    """
    Simulates calling get_configuration_object when the provided path is a file.

    `coulomb build` will provide a full path when provided via a flag.
    """
    project_path = pathlib.Path(__file__).parent / "projects" / "just-settings" / "settings.py"

    site_object = coulomb.processors.get_configuration_object(project_path)
    assert site_object == coulomb.Site()


def test_get_configuration_object__no_file():
    """
    Simulates calling get_configuration_object when the provided path is a file that doesn't exist.

    `coulomb build` will provide a full path when provided via a flag.
    Should raise a helpful error.
    """
    project_path = pathlib.Path(__file__).parent / "projects" / "just-settings" / "no-file.py"

    with pytest.raises(ValueError):
        coulomb.processors.get_configuration_object(project_path)


def test_get_configuration_object__custom_object_name():
    """
    Simulates calling get_configuration_object when the provided path is a file and a custom object name.

    `coulomb build` will provide a full path when provided via a flag.
    Provides an object name using the `dotted.path:object` syntax.
    """
    project_path = pathlib.Path(__file__).parent / "projects" / "just-settings-blog-object" / "settings.py"

    site_object = coulomb.processors.get_configuration_object(project_path, "blog")
    assert site_object == coulomb.Site()


def test_get_configuration_object__settings_object_does_not_exist():
    """
    Simulates calling get_configuration_object when the provided path is a file
    and a custom object name but does not exist.

    `coulomb build` will provide a full path when provided via a flag.
    Provides an object name using the `dotted.path:object` syntax.
    """
    project_path = pathlib.Path(__file__).parent / "projects" / "just-settings-blog-object" / "settings.py"

    with pytest.raises(ValueError):
        coulomb.processors.get_configuration_object(project_path)


def test_site_register_view__call_after_definition():
    site = coulomb.Site()

    assert not site.views

    view = coulomb.TemplatedView(
        path="/some/path",
        template="foo"
    )

    site.register_view(view)
    assert site.views[0] == view


def test_site_register_view__decorator():
    site = coulomb.Site()

    assert not site.views

    @site.register_view
    class MyView(coulomb.TemplatedView):
        path = "/some/path"
        template = "foo"

    assert site.views[0] == MyView


def test_site_register_model__decorator_with_path():
    site = coulomb.Site()

    assert not site.models

    @site.register_model("./my_cool_path")
    @dataclasses.dataclass
    class DataObject:
        data: str
        date: int

    assert site.models[0] == (DataObject, "./my_cool_path")


def test_site_register_model__decorator_no_path():
    site = coulomb.Site()

    assert not site.models

    @site.register_model
    @dataclasses.dataclass
    class DataObject:
        data: str
        date: int

    assert site.models[0] == (DataObject, "data_object")


def test_site_register_model__call_after_definition_with_path():
    @dataclasses.dataclass
    class DataObject:
        data: str
        date: int

    site = coulomb.Site()

    assert not site.models

    site.register_model(DataObject, "./my_cool_path")

    assert site.models[0] == (DataObject, "./my_cool_path")


def test_site_register_model__call_after_definition_without_path():
    @dataclasses.dataclass
    class DataObject:
        data: str
        date: int

    site = coulomb.Site()

    assert not site.models

    site.register_model(DataObject)

    assert site.models[0] == (DataObject, "data_object")


@pytest.mark.parametrize(
    "first_path, second_path",
    (
        ("foo", "bar"),
        (pathlib.Path("foo"), "bar"),
        (pathlib.Path("foo"), b"bar"),
        (b"bad", "foo"),
        (b"first", b"second"),
        (pathlib.Path("red"), pathlib.Path("green"))
    )
)
def test_site_register_model__call_with_two_pathlikes(first_path, second_path):
    site = coulomb.Site()

    with pytest.raises(ValueError) as err:
        site.register_model(first_path, second_path)  # type: ignore

    assert str(err.value) == "Cannot pass path as both arguments."


def test_site_accepts_site_wide_context():
    example_context = {
        "site_name": "Coulomb Static Site Generator"
    }

    site = coulomb.Site(context=example_context)
    assert site.context == example_context


def test_site_passes_site_context_to_views():

    @dataclasses.dataclass
    class TestView(coulomb.types.ViewProtocol):
        context: dict[str, typing.Any]
        path: str
        for_each: None

        @classmethod
        def generate_artifacts(
            cls, context: dict[str, Any], templating_engine: Any
        ) -> Iterable[Artifact]:
            yield TestArtifact(context=context)

    @dataclasses.dataclass
    class TestArtifact(coulomb.types.Artifact):
        context: dict[str, typing.Any]
        route: pathlib.Path = pathlib.Path('foo')

        @property
        def name(self) -> str:
            return "test"

        def write(self, path):
            pass

    site = coulomb.Site(
        context={
            "foo": "bar"
        }
    )

    site.register_view(TestView)

    artifacts = list(site.generate_artifacts(pathlib.Path("/")))
    assert len(artifacts) == 1
    assert typing.cast(TestArtifact, artifacts[0]).context == {"foo": "bar"}


def test_site_has_base_path():

    site = coulomb.Site(base_path="./foo")

    assert site.base_path == "./foo"
