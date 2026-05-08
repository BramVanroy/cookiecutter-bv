# cookiecutter-bv

A Cookiecutter template for modern Python projects.

## Features

- **[uv](https://docs.astral.sh/uv/)** for dependency management and virtual environments
- **[hatch-vcs](https://github.com/ofek/hatch-vcs)** for dynamic versioning from git tags
- **[ruff](https://docs.astral.sh/ruff/)** for linting and formatting (Google docstring convention)
- Optional **[mypy](https://mypy.readthedocs.io/)** integration for static type checking
- **[pytest](https://docs.pytest.org/)** with doctest support and [codecov](https://codecov.io/) integration
- **[pre-commit](https://pre-commit.com/)** hooks for ruff and standard checks, with optional mypy hook
- Optional docs stack: **[MkDocs Material](https://squidfunk.github.io/mkdocs-material/)** + `mkdocstrings` + lychee link checking workflows
- Optional **interrogate** integration with docstring coverage badge workflow
- **Makefile** with targets for quality checks and tests; optional type-checking and docs targets
- **GitHub Actions**: CI matrix across all supported Python versions (3.10–3.14) on every push/PR, release publish, and optional docs/interrogate workflows
- **`src/` layout** with `scripts/` and `tests/` directories

## Usage

```bash
uvx cookiecutter https://github.com/BramVanroy/cookiecutter-bv
```

By calling the `uvx` command above, an interactive installation will start. But you can
override or set variables already during installation. Extra context can be passed as
`key=value` pairs to pre-fill specific prompts:

```bash
uvx cookiecutter https://github.com/BramVanroy/cookiecutter-bv project_name="My Awesome Library"
```

### Local test run

To test the template from a local clone, pass the directory path instead of a URL.
Use `--output-dir` to avoid generating the project inside the template folder itself:

```bash
# Interactive — prompts shown with defaults pre-filled
uvx cookiecutter . --output-dir example-project

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
| `enable_interrogate` | Include interrogate integration (docstring coverage checks + badge workflow) | `yes` |
| `enable_mypy` | Include mypy integration (Makefile, pyproject, pre-commit, CI) | `yes` |
| `enable_docs` | Include docs integration (MkDocs + Pages deploy + lychee checks) | `yes` |
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
├── docs/                 # MkDocs source (optional)
├── Makefile              # dev workflow commands (also used by CI)
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

### Type checking — mypy (optional)

When enabled, **[mypy](https://mypy.readthedocs.io/)** checks `src/`, `tests/`,
and `scripts/` using the template defaults in `pyproject.toml`.

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

### Developer workflow — Makefile

A `Makefile` provides short commands for the most common dev tasks:

| Target | What it does |
| --- | --- |
| `make quality` | `ruff check` + `ruff format --check` (and `interrogate` when enabled) |
| `make style` | `ruff check --fix` + `ruff format` — fix lint and formatting in-place |
| `make typecheck` | `mypy` against `src/`, `tests/`, and `scripts/` (optional) |
| `make test` | `pytest` with terminal coverage summary **and** `coverage.xml` for Codecov |
| `make docs` | `mkdocs serve` — live-preview the docs locally (optional) |

`make test` is the **single source of truth** for the pytest invocation. The CI `test`
job calls `make test` directly, so coverage flags only ever need changing in one place.

The `quality` CI job does _not_ use the Makefile — it runs
`pre-commit run --all-files`, which covers a broader set of checks (YAML/TOML
validation, whitespace, ruff, mypy) and mirrors what the git commit hook enforces.

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
| `ruff-lint` (local) | Runs `uv run ruff check --fix`; fails if unfixable violations remain |
| `ruff-format` (local) | Runs `uv run ruff format` |
| `mypy` (local) | Runs `uv run mypy` against the full project (optional) |

All tool hooks are **local** — they use the ruff/mypy versions installed by
uv, so there is no separate hook environment to download and no risk of version drift
between your dev dependencies and the hooks.

Install once per clone with `uv run pre-commit install`.

### Documentation — MkDocs Material (optional)

Documentation lives in `docs/` and is built with
**[MkDocs Material](https://squidfunk.github.io/mkdocs-material/)**.
The **[mkdocstrings](https://mkdocstrings.github.io/)** plugin auto-generates API
reference pages directly from the source docstrings (Google style). The
`docs/api.md` page uses the `:::` directive to render the full package API.

MkDocs packages live in the optional `docs` dependency group. When docs support is
enabled, `uv sync --group dev` already includes them (the `dev` group includes `docs`).
Build and preview locally:

```bash
uv run mkdocs serve
```

### GitHub Actions

Core workflows included by default:

- `ci.yml`
- `publish.yml`

Optional workflows:

- `interrogate-badge.yml` (only when `enable_interrogate = yes`)
- `docs.yml`, `links-md.yml`, and `links-html-scheduled.yml` (only when `enable_docs = yes`)

#### `ci.yml` — runs on every push to `main` and on every pull request

| Job | What it does |
| --- | --- |
| `quality` | Installs dev dependencies, then runs `pre-commit run --all-files` (skipped if `.pre-commit-config.yaml` is absent) |
| `test` | Matrix across all supported Python versions (from the chosen minimum up to 3.14); runs `make test` on each (skipped if `tests/` is empty or absent); `fail-fast: false` so every version is reported; uploads `coverage.xml` to Codecov (skipped if the file was not generated) |

Both jobs use `astral-sh/setup-uv` (with caching) and a `concurrency` group that
cancels superseded runs on the same branch, saving CI minutes on rapid pushes.

#### `docs.yml` (optional) — runs on published releases or manual dispatch

This workflow resolves a release tag, checks out that tag, installs the `docs` group,
and deploys versioned docs to GitHub Pages via `mike`.

`links-md.yml` (optional) checks Markdown links on docs/README changes with lychee.
`links-html-scheduled.yml` (optional) checks links in rendered `gh-pages` HTML on a schedule.

#### `publish.yml` — runs when a GitHub release is published

| Job | What it does |
| --- | --- |
| `pypi-publish` | Checks out the repo, builds the wheel and sdist with `uv build`, and publishes to PyPI using **trusted publishing** (OIDC) — no `PYPI_TOKEN` secret is required |

> **Note:** Trusted publishing requires a one-time configuration on PyPI's side
> before the first release. See [PyPI trusted publishing setup](#pypi-trusted-publishing-setup) below.

### PyPI trusted publishing setup

Trusted publishing uses OIDC to authenticate directly from GitHub Actions to
PyPI — no long-lived API token needs to be stored as a secret. One-time setup:

1. Create the project on PyPI (or reserve the name via a manual upload first).
2. Go to the project's **Publishing** settings on PyPI and add a trusted
   publisher with:
    - **Owner**: your GitHub username / org
    - **Repository**: your repo name
    - **Workflow**: `publish.yml`
    - **Environment**: `release`
3. Create the `release` environment in your GitHub repository settings
   (Settings → Environments) — no secrets needed, but you can add protection
   rules (e.g. require a reviewer before publishing).
