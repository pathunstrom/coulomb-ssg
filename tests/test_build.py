import pathlib

import coulomb
import coulomb.main


def test_build(tmp_path: pathlib.Path):
    output_dir = tmp_path / "my-site"  # Pretend this comes from configuration
    output_dir.mkdir(parents=True, exist_ok=True)  # Must exist for the builder.
    input_dir = tmp_path / "project"
    input_dir.mkdir(parents=True, exist_ok=True)
    good_path = input_dir / "index.html"
    bad_path = input_dir / "project.py"
    good_path.touch()
    bad_path.touch()

    site = coulomb.Site(discover_html=True)
    coulomb.main.build(output_dir, input_dir, site)

    expected_file = output_dir / "index.html"
    assert expected_file.exists()


def test_build_no_discover_html(tmp_path: pathlib.Path):
    output_dir = tmp_path / "my-site"  # Pretend this comes from configuration
    output_dir.mkdir(parents=True, exist_ok=True)  # Must exist for the builder.
    input_dir = tmp_path / "project"
    input_dir.mkdir(parents=True, exist_ok=True)
    good_path = input_dir / "index.html"
    bad_path = input_dir / "project.py"
    good_path.touch()
    bad_path.touch()

    site = coulomb.Site(discover_html=False)
    coulomb.main.build(output_dir, input_dir, site)

    expected_file = output_dir / "index.html"
    assert not expected_file.exists()


def test_build__site_not_at_root(tmp_path: pathlib.Path):
    output_dir = tmp_path / "my-site"  # Pretend this comes from configuration
    output_dir.mkdir(parents=True, exist_ok=True)  # Must exist for the builder.
    input_dir = tmp_path / "project"
    input_dir.mkdir(parents=True, exist_ok=True)
    good_path = input_dir / "index.html"
    bad_path = input_dir / "project.py"
    good_path.touch()
    bad_path.touch()

    site = coulomb.Site(discover_html=True, base_path="./testing")
    coulomb.main.build(output_dir, input_dir, site)

    expected_file = output_dir / "testing" / "index.html"
    assert expected_file.exists()
