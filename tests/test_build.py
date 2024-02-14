import pathlib

import coulomb


def test_build(tmp_path: pathlib.Path):
    output_dir = tmp_path / "my-site"  # Pretend this comes from configuration
    output_dir.mkdir(parents=True, exist_ok=True)  # Must exist for the builder.

    coulomb.main.build(output_dir)

    expected_file = output_dir / "index.html"
    assert expected_file.exists()
