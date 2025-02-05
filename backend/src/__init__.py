import importlib.metadata as _importlib_metadata
import pathlib as _pathlib
import tomllib as _tomllib

_source_location = _pathlib.Path(__file__).parent
_pyproject = _source_location.parent / "pyproject.toml"
if _pyproject.exists():
    with _pyproject.open("rb") as _f:
        data = _tomllib.load(_f)
        __version__ = data["tool"]["poetry"]["version"]
        __description__: str = data["tool"]["poetry"]["description"]
else:
    __version__ = _importlib_metadata.version("package")
    __description__ = "Mailing Service for your applications"

__all__ = ["__description__", "__version__"]
