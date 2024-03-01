import pathlib

import coulomb.processors


def test_gold_project():
    """Runs against tests/test-project which excercises a bit of every feature."""
    project_path = pathlib.Path(__file__).parent / "projects" / "test-project"
    site_configuration = coulomb.processors.get_configuration_object(path=project_path)

    assert site_configuration
