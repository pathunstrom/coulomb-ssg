import contextlib
import importlib.util
import os
import pathlib
import sys

import coulomb.configurations


def get_configuration_object(
    path: pathlib.Path, settings_object: str = "site"
) -> coulomb.configurations.Site:
    if not path.exists():
        raise ValueError("Configuration path must exist.")
    if path.is_dir():
        directory = path
        path = path / "settings.py"
    elif path.is_file():
        directory = path.parent
    else:
        raise RuntimeError(
            "Your path is neither a file or directory. This seems unlikely."
        )

    @contextlib.contextmanager
    def temporarily_change_directories(_path):
        current_directory = pathlib.Path.cwd()
        os.chdir(_path)
        yield
        os.chdir(current_directory)

    with temporarily_change_directories(directory):
        spec = importlib.util.spec_from_file_location("coulomb_user_settings", path)
        if spec is None:
            raise RuntimeError("Importlib error - spec failed")
        module = importlib.util.module_from_spec(spec)
        if module is None:
            raise RuntimeError("Could not import user settings module.")

        sys.modules["coulomb_user_settings"] = module

        loader = spec.loader
        if loader is None:
            raise RuntimeError("Module loader doesn't exist.")
        loader.exec_module(module)
        try:
            return getattr(module, settings_object)
        except AttributeError as err:
            message = f"Configuration object {settings_object} does not exist in settings file."
            raise ValueError(message) from err
