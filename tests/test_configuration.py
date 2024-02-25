import pathlib

import pytest

import coulomb


def test_get_configuration_object__directory():
    """
    Simulates calling get_configuration_object when the provided path is a directory.

    Will be the basic operation when calling `coulomb build` without a settings flag.
    """
    project_path = pathlib.Path(__file__).parent / "projects" / "just-settings"

    site_object = coulomb.configurations.get_configuration_object(project_path)
    assert site_object == coulomb.Site()


def test_get_configuration_object__default_file():
    """
    Simulates calling get_configuration_object when the provided path is a file.

    `coulomb build` will provide a full path when provided via a flag.
    """
    project_path = pathlib.Path(__file__).parent / "projects" / "just-settings" / "settings.py"

    site_object = coulomb.configurations.get_configuration_object(project_path)
    assert site_object == coulomb.Site()


def test_get_configuration_object__no_file():
    """
    Simulates calling get_configuration_object when the provided path is a file that doesn't exist.

    `coulomb build` will provide a full path when provided via a flag.
    Should raise a helpful error.
    """
    project_path = pathlib.Path(__file__).parent / "projects" / "just-settings" / "no-file.py"

    with pytest.raises(ValueError):
        coulomb.configurations.get_configuration_object(project_path)


def test_get_configuration_object__custom_object_name():
    """
    Simulates calling get_configuration_object when the provided path is a file and a custom object name.

    `coulomb build` will provide a full path when provided via a flag.
    Provides an object name using the `dotted.path:object` syntax.
    """
    project_path = pathlib.Path(__file__).parent / "projects" / "just-settings-blog-object" / "settings.py"

    site_object = coulomb.configurations.get_configuration_object(project_path, "blog")
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
        coulomb.configurations.get_configuration_object(project_path)