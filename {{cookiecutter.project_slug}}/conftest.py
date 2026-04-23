"""Pytest configuration: exclude auto-generated files from doctest collection."""

collect_ignore_glob = ["src/{{cookiecutter.project_slug}}/_version.py"]
