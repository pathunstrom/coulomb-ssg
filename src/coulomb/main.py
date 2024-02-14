import pathlib


def build(build_dir: pathlib.Path, source_dir: pathlib.Path):
    """"""

    index = '<!DOCTYPE html><html lang="en"><head><title>My Cool Site</title></head><body><h1>Hello World!</h1></body>'
    with open(build_dir / "index.html", "w") as output_file:
        output_file.write(index)


def run():  # Not testable due to: output dir is real.
    build_dir = "_build"
    site_name = "my-site"

    output_path = pathlib.Path.cwd() / build_dir / site_name
    output_path.mkdir(parents=True, exist_ok=True)

    build(output_path)
