import nox

nox.options.default_venv_backend = "venv"

py_versions = ["3.9", "3.10", "3.11", "3.12"]


@nox.session(tags=["styles"], python=py_versions[0])
def linter(session):
    """Auto fix linter issues."""
    session.install('ruff')
    session.install('.')
    session.run('ruff', 'check', 'src', '--fix')


@nox.session(tags=["styles"], python=py_versions[0])
def formatter(session):
    """Format the source code."""
    session.install('ruff')
    session.install('.')
    session.run('ruff', 'format', 'src')


@nox.session(python=py_versions)
def mypy(session):
    """Run mypy against the source."""
    session.install('mypy')
    session.install('.')
    session.run('mypy', 'src')


@nox.session(python=py_versions)
def tests(session):
    """Run the test suite."""
    session.install('pytest')
    session.install('.')
    session.run('pytest')
