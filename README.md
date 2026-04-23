# cookiecutter-bv

A Cookiecutter template for modern Python projects.

## Features

- **[uv](https://docs.astral.sh/uv/)** for dependency management and virtual environments
- **[hatch-vcs](https://github.com/ofek/hatch-vcs)** for dynamic versioning from git tags
- **[ruff](https://docs.astral.sh/ruff/)** for linting and formatting (Google docstring convention)
- **[mypy](https://mypy.readthedocs.io/)** for static type checking
- **[pytest](https://docs.pytest.org/)** with doctest support and [codecov](https://codecov.io/) integration
- **[pre-commit](https://pre-commit.com/)** hooks for ruff, mypy, and standard checks
- **[MkDocs Material](https://squidfunk.github.io/mkdocs-material/)** documentation with `mkdocstrings`
- **GitHub Actions**: CI on every push/PR, compatibility testing + docs deploy + PyPI publish on release
- **`src/` layout** with `scripts/` and `tests/` directories

## Usage

```bash
uvx cookiecutter https://github.com/BramVanroy/cookiecutter-bv
```

Extra context can be passed as `key=value` pairs to pre-fill specific prompts:

```bash
uvx cookiecutter https://github.com/BramVanroy/cookiecutter-bv project_name="My Awesome Library"
```

### Local test run

To test the template from a local clone, pass the directory path instead of a URL.
Use `--output-dir` to avoid generating the project inside the template folder itself:

```bash
# Interactive — prompts shown with defaults pre-filled
uvx cookiecutter . --output-dir /tmp/cc-test

# Non-interactive — accept all defaults immediately (useful for a quick sanity check)
uvx cookiecutter . --no-input --output-dir /tmp/cc-test
```

`--replay` re-uses the answers from the last run, which is handy when iterating on
the template without re-entering every prompt each time:

```bash
uvx cookiecutter . --replay --output-dir /tmp/cc-test
```

### Persistent personal defaults

Set your name, email, and GitHub username once in `~/.cookiecutterrc` and they become
the default for every invocation of this (and any other) cookiecutter template:

```yaml
# ~/.cookiecutterrc
default_context:
  author_name: "Your Name"
  author_email: "you@example.com"
  github_username: "your-github-username"
```

See the [cookiecutter user config docs](https://cookiecutter.readthedocs.io/en/stable/advanced/user_config.html) for details.

## Post-generation

The hook automatically:

1. Runs `git init -b main` and creates an initial commit.
2. Prints the exact `gh repo create` command to create the GitHub repo and push in one step.

## Prompts

| Variable | Description | Default |
| --- | --- | --- |
| `project_name` | Human-readable project name | `My Python Project` |
| `project_slug` | Python package name (snake_case) | derived from `project_name` |
| `github_repo_name` | GitHub repository name (kebab-case) | derived from `project_slug` |
| `project_description` | One-line description | — |
| `author_name` | Your full name | from `~/.cookiecutterrc` |
| `author_email` | Your email address | from `~/.cookiecutterrc` |
| `github_username` | GitHub username / org | from `~/.cookiecutterrc` |
| `python_requires` | Minimum Python version | `3.10` |
| `license` | License type | `MIT` |

## What's built in

### Project layout

```text
<github_repo_name>/
├── src/<project_slug>/   # importable package
│   ├── __init__.py
│   └── py.typed          # PEP 561 marker — declares the package as typed
├── tests/                # pytest test suite
├── scripts/              # one-off helper scripts (not part of the package)
├── docs/                 # MkDocs source
└── pyproject.toml
```

The `src/` layout keeps the installed package strictly separate from the repo
root, which prevents accidentally importing an uninstalled version and makes
editable installs behave identically to regular ones.

### Versioning

Versioning is fully automatic via **[hatch-vcs](https://github.com/ofek/hatch-vcs)**,
which reads the version from git tags at build time. There is no version string to
maintain manually in any source file.

The workflow:

1. Create an annotated tag: `git tag -a v1.2.3 -m "v1.2.3"`
2. Push the tag: `git push origin v1.2.3`
3. Create a GitHub release from that tag.

The release CI picks up the tag, builds the package (version = `1.2.3`), and
publishes it to PyPI automatically.

During development, `importlib.metadata.version()` is used to expose `__version__`
at runtime, so no generated `_version.py` file needs to be committed.

### Linting and formatting — ruff

**[ruff](https://docs.astral.sh/ruff/)** handles both linting and formatting with a
single tool. The enabled rule sets are:

| Prefix | Rule set |
| --- | --- |
| `E`/`W` | pycodestyle errors and warnings |
| `F` | Pyflakes (undefined names, unused imports, …) |
| `I` | isort-compatible import ordering |
| `B` | flake8-bugbear (likely bugs and design issues) |
| `C4` | flake8-comprehensions (unnecessary list/dict/set constructions) |
| `UP` | pyupgrade (modernise syntax for the target Python version) |
| `SIM` | flake8-simplify (simplifiable expressions) |
| `RUF` | Ruff-native rules |
| `D` | pydocstyle — enforces **Google-style docstrings** |

Line length is 79 (CPython default). Docstring code examples are also formatted
by `ruff format` (`docstring-code-format = true`).

The `D` rules are suppressed for `tests/` (no docstrings required on test
functions) and for the auto-generated `_version.py` file.

### Type checking — mypy

**[mypy](https://mypy.readthedocs.io/)** runs in strict mode against
`src/<project_slug>/`. Strict mode enables all optional error codes, including
`disallow_untyped_defs`, `warn_return_any`, and `disallow_any_unimported`.
The auto-generated `_version.py` is excluded from the mypy run.

### Testing — pytest

**[pytest](https://docs.pytest.org/)** is configured with two test sources:

- `tests/` — conventional unit/integration tests
- `src/` — **doctest collection** (`--doctest-modules`)

Doctests are run automatically from every docstring in the package. The
recommended format (enforced by ruff's `D` rules) is Google style with an
`Example:` section:

```python
def add(a: int, b: int) -> int:
    """Add two integers.

    Args:
        a: First operand.
        b: Second operand.

    Returns:
        The sum of ``a`` and ``b``.

    Example:
        >>> add(1, 2)
        3
    """
    return a + b
```

Coverage is measured by **[pytest-cov](https://pytest-cov.readthedocs.io/)** and
reported both to the terminal and to `coverage.xml` for upload to
**[codecov](https://codecov.io/)**.

### pre-commit hooks

**[pre-commit](https://pre-commit.com/)** runs the following hooks on every commit:

| Hook | What it does |
| --- | --- |
| `check-added-large-files` | Rejects files above the size threshold |
| `check-case-conflict` | Catches filename case conflicts (Windows/macOS vs Linux) |
| `check-merge-conflict` | Rejects files containing unresolved merge conflict markers |
| `check-toml` | Validates TOML syntax |
| `check-yaml` | Validates YAML syntax |
| `end-of-file-fixer` | Ensures every file ends with a single newline |
| `trailing-whitespace` | Strips trailing whitespace |
| `ruff` (lint) | Runs `ruff check --fix`; fails if unfixable violations remain |
| `ruff-format` | Runs `ruff format` |
| `mypy` (local) | Runs `uv run mypy` against the full project |

Install once per clone with `uv run pre-commit install`.

### Documentation — MkDocs Material

Documentation lives in `docs/` and is built with
**[MkDocs Material](https://squidfunk.github.io/mkdocs-material/)**.
The **[mkdocstrings](https://mkdocstrings.github.io/)** plugin auto-generates API
reference pages directly from the source docstrings (Google style). The
`docs/api.md` page uses the `:::` directive to render the full package API.

Build and preview locally:

```bash
uv run mkdocs serve
```

### GitHub Actions

Two workflows are included.

#### `ci.yml` — runs on every push to `main` and on every pull request

| Job | What it does |
| --- | --- |
| `quality` | Installs dependencies, runs all pre-commit hooks (ruff lint, ruff format, mypy, and the standard file checks) |
| `test` | Runs `pytest` (unit tests + doctests + coverage) on the project's minimum Python version; uploads `coverage.xml` to Codecov |

Both jobs use `astral-sh/setup-uv` for fast, cached installs.

#### `release.yml` — runs when a GitHub release is published

| Job | What it does |
| --- | --- |
| `compatibility-tests` | Matrix job: runs `pytest` on **every supported Python version** from `python_requires` up to 3.13; uploads per-version coverage flags to Codecov |
| `deploy-docs` | Runs after all matrix tests pass; builds the MkDocs site and deploys it to GitHub Pages via `mkdocs gh-deploy` |
| `publish` | Runs after all matrix tests pass; builds the wheel and sdist with `uv build` and publishes to PyPI using **trusted publishing** (OIDC) — no `PYPI_TOKEN` secret is required |

The `deploy-docs` and `publish` jobs both `need: compatibility-tests`, so a
release is never published or documented if any test leg fails.

### PyPI trusted publishing setup

Trusted publishing uses OIDC to authenticate directly from GitHub Actions to
PyPI — no long-lived API token needs to be stored as a secret. One-time setup:

1. Create the project on PyPI (or reserve the name via a manual upload first).
2. Go to the project's **Publishing** settings on PyPI and add a trusted
   publisher with:
   - **Owner**: your GitHub username / org
   - **Repository**: your repo name
   - **Workflow**: `release.yml`
   - **Environment**: `pypi`
3. Create the `pypi` environment in your GitHub repository settings
   (Settings → Environments) — no secrets needed, but you can add protection
   rules (e.g. require a reviewer before publishing).
