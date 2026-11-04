"""{{cookiecutter.project_description}}"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("{{cookiecutter.github_repo_name}}")
except PackageNotFoundError:
    __version__ = "unknown"


__all__ = ["__version__"]
