# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A Cookiecutter template (not a Python package itself). There is no build, lint, or
test setup at the repo root. Everything under `{{cookiecutter.github_repo_name}}/` is
Jinja-rendered output that becomes the generated project. `README.md` documents the
*generated* project's tooling for end users, so update it whenever you change
template behavior.

## Testing the template

The only way to validate a change is to generate a project and exercise it:

```bash
# Quick sanity check with defaults (write output outside the repo)
uvx cookiecutter . --no-input --output-dir <scratch-dir>

# Exercise the optional-feature branches
uvx cookiecutter . --no-input --output-dir <scratch-dir> \
    enable_mypy=no enable_docs=no enable_interrogate=no license=Proprietary python_requires=3.13
```

Then, inside the generated project:

```bash
uv sync --locked                      # uv.lock is created by the post-gen hook
make quality && make test && make typecheck
uv run pre-commit run --all-files     # what the CI quality job runs
uv run mkdocs build                   # docs builds in strict mode
uv build
uvx --from actionlint-py actionlint   # validate the rendered workflows
```

Run a single generated test with `uv run pytest tests/test_<slug>.py::test_name`.
Also grep the output for leftover `{{`/`{%`. Workflows should contain only GitHub's
own `${{ }}` expressions.

## How generation works

- **`cookiecutter.json`** defines the variables. `project_slug` and
  `github_repo_name` are derived from `project_name`. For list values the first item
  is the default. `python_requires` is the **single source of truth** for supported
  Python versions: `pyproject.toml` (classifiers) and `ci.yml` (test matrix) read the
  full list via `_cookiecutter.python_requires` (note: `_cookiecutter` at the top
  level, not `cookiecutter._cookiecutter`), sort it, and keep versions `>=` the
  chosen minimum.
- **Jinja in template files** handles feature toggles inline, via
  `{% if cookiecutter.enable_* == "yes" %}` blocks in `pyproject.toml`, `Makefile`,
  `README.md`, `.pre-commit-config.yaml`, `ci.yml`, and others.
- **`hooks/pre_gen_project.py`** validates the slug, repo name, and email, and exits
  non-zero on bad input.
- **`hooks/post_gen_project.py`**:
  - copies the selected `licenses/LICENSE_*` file to `LICENSE`;
  - deletes the files of disabled features. They are listed in `OPTIONAL_PATHS`, so
    adding an optional file means adding it there;
  - runs `uv lock` (best effort);
  - runs `git init -b main` and makes the initial commit.

## Jinja escaping gotchas

- Every GitHub Actions `${{ ... }}` in `.github/workflows/*.yml` must be wrapped in
  `{% raw %}...{% endraw %}`. If one isn't, generation fails with
  `'github' is undefined`.
- `_copy_without_render` lists `docs/overrides` (Material theme overrides) and
  `docs/templates` (mkdocstrings templates). These folders hold MkDocs Jinja and are
  copied verbatim. The patterns are matched against paths relative to the template
  folder. Don't add broad globs such as `*.yaml`: they silently stop
  cookiecutter variables from rendering.

## Generated-project design points

- `src/` layout. The version comes from git tags via hatch-vcs, and `__version__`
  comes from `importlib.metadata`.
- pytest uses the native `[tool.pytest]` table (pytest 9+, `strict = true`) and
  collects doctests from `src/`. Coverage flags live only in the Makefile `test`
  target, with settings in `[tool.coverage]`.
- The CI `quality` job runs `pre-commit run --all-files`, not `make quality`. The
  `test` job runs `make test`. A `ci-ok` job aggregates both for branch protection.
- The pre-commit ruff and mypy hooks are `local` and use `uv run`, so the tool
  versions come from the uv lock.
- Actions are pinned to exact versions, and `dependabot.yml` keeps the actions and
  `uv.lock` current. Use exact release tags: some actions (for example `setup-uv`) no
  longer publish floating major tags.
- Docs: MkDocs Material, mkdocstrings, and `mike` versioned deploys.
  `docs/hooks.py` does two things:
  - re-highlights doctest `pycon` blocks as plain Python;
  - rewrites the source links that come from `docs/templates`, so they point at
    `DOCS_SOURCE_REF`, the release tag that `docs.yml` sets.

  `exclude_docs` in `mkdocs.yml` keeps this tooling out of the built site.
- Publishing uses `pypa/gh-action-pypi-publish` with trusted publishing (OIDC) and
  attestations, through the `release` environment.
