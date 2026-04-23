# {{cookiecutter.project_name}}

[![CI](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.github_repo_name}}/actions/workflows/ci.yml/badge.svg)](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.github_repo_name}}/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/{{cookiecutter.github_username}}/{{cookiecutter.github_repo_name}}/branch/main/graph/badge.svg)](https://codecov.io/gh/{{cookiecutter.github_username}}/{{cookiecutter.github_repo_name}})
[![PyPI version](https://badge.fury.io/py/{{cookiecutter.github_repo_name}}.svg)](https://badge.fury.io/py/{{cookiecutter.github_repo_name}})
[![Python versions](https://img.shields.io/pypi/pyversions/{{cookiecutter.github_repo_name}}.svg)](https://pypi.org/project/{{cookiecutter.github_repo_name}}/)
[![License](https://img.shields.io/github/license/{{cookiecutter.github_username}}/{{cookiecutter.github_repo_name}})](LICENSE)

{{cookiecutter.project_description}}

## Documentation

Full documentation is available at [{{cookiecutter.github_username}}.github.io/{{cookiecutter.github_repo_name}}](https://{{cookiecutter.github_username}}.github.io/{{cookiecutter.github_repo_name}}).

## Installation

```bash
pip install {{cookiecutter.github_repo_name}}
```

## Development

```bash
git clone https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.github_repo_name}}.git
cd {{cookiecutter.github_repo_name}}
uv sync
uv run pre-commit install
uv run pytest
```

## License

{{cookiecutter.license}}
