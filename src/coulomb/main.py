import pathlib
import coulomb


def build(
    build_dir: pathlib.Path, source_dir: pathlib.Path, site_configuration: coulomb.Site
):
    """"""
    artifact: coulomb.Artifact
    for artifact in site_configuration.generate_artifacts(source_dir):
        output_path = build_dir / artifact.route
        output_path.parent.mkdir(parents=True, exist_ok=True)
        artifact.write(output_path)


def run():
    build_dir = "_build"
    site_name = "my-site"

    output_path = pathlib.Path.cwd() / build_dir / site_name
    output_path.mkdir(parents=True, exist_ok=True)

    source_path = pathlib.Path.cwd() / "project"

    site = coulomb.Site(
        discover_html=True,
        component_path=pathlib.Path("project/components/").absolute(),
        views=[coulomb.configurations.JinjaxRoute("index.html", "Layout", "Piper")],
    )
    build(output_path, source_path, site)
