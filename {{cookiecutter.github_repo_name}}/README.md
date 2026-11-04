# {{cookiecutter.project_name}}

[![CI](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.github_repo_name}}/actions/workflows/ci.yml/badge.svg)](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.github_repo_name}}/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/{{cookiecutter.github_username}}/{{cookiecutter.github_repo_name}}/branch/main/graph/badge.svg)](https://codecov.io/gh/{{cookiecutter.github_username}}/{{cookiecutter.github_repo_name}})
[![PyPI version](https://badge.fury.io/py/{{cookiecutter.github_repo_name}}.svg)](https://badge.fury.io/py/{{cookiecutter.github_repo_name}})
[![Python versions](https://img.shields.io/pypi/pyversions/{{cookiecutter.github_repo_name}}.svg)](https://pypi.org/project/{{cookiecutter.github_repo_name}}/)
[![License](https://img.shields.io/github/license/{{cookiecutter.github_username}}/{{cookiecutter.github_repo_name}})](LICENSE)
![GitHub tag](https://img.shields.io/github/v/tag/{{cookiecutter.github_username}}/{{cookiecutter.github_repo_name}})


{{cookiecutter.project_description}}

{% if cookiecutter.enable_docs == "yes" %}
## Documentation

Full documentation is available at [{{cookiecutter.github_username}}.github.io/{{cookiecutter.github_repo_name}}](https://{{cookiecutter.github_username}}.github.io/{{cookiecutter.github_repo_name}}).
{% endif %}

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
```

| Command | What it does |
| --- | --- |
| `make test` | Run tests and doctests with coverage |
| `make quality` | Lint and format checks (no changes) |
| `make style` | Auto-fix lint issues and reformat |
{%- if cookiecutter.enable_mypy == "yes" %}
| `make typecheck` | Run mypy |
{%- endif %}
{%- if cookiecutter.enable_docs == "yes" %}
| `make docs` | Live preview of the documentation |
{%- endif %}

Releases are cut by pushing a `vX.Y.Z` tag and publishing a GitHub release from
it; the version is derived from the tag.

## License

{{cookiecutter.license}}. See [LICENSE](LICENSE).
