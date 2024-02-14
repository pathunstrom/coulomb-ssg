import pathlib

import coulomb


def test_build(tmp_path: pathlib.Path):
    output_dir = tmp_path / "my-site"  # Pretend this comes from configuration
    output_dir.mkdir(parents=True, exist_ok=True)  # Must exist for the builder.
    input_dir = tmp_path / "project"
    input_dir.mkdir(parents=True, exist_ok=True)
    good_path = input_dir / "index.html"
    bad_path = input_dir / "project.py"
    good_path.touch()
    bad_path.touch()

    coulomb.main.build(output_dir, input_dir)

    expected_file = output_dir / "index.html"
    assert expected_file.exists()
