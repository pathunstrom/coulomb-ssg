import pathlib


def build(build_dir: pathlib.Path, source_dir: pathlib.Path):
    """"""
    for file_path in source_dir.glob("**/*.html"):
        output_path = build_dir/file_path.relative_to(source_dir)
        output_path.write_bytes(file_path.read_bytes())


def run():  # Not testable due to: output dir is real.
    build_dir = "_build"
    site_name = "my-site"

    output_path = pathlib.Path.cwd() / build_dir / site_name
    output_path.mkdir(parents=True, exist_ok=True)

    source_path = pathlib.Path.cwd() / "project"
    build(output_path, source_path)
