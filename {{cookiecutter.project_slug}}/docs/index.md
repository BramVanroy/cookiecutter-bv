# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

## Installation

```bash
pip install {{cookiecutter.github_repo_name}}
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add {{cookiecutter.github_repo_name}}
```

## Quickstart

...

## Development

Clone the repository and install with [uv](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.github_repo_name}}.git
cd {{cookiecutter.github_repo_name}}
uv sync
uv run pre-commit install
```

Run tests:

```bash
uv run pytest
```
