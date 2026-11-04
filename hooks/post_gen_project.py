"""Post-generation hook: install the license, prune disabled features, init git."""

import shutil
import subprocess
from pathlib import Path

LICENSE = "{{cookiecutter.license}}"
PROJECT_NAME = "{{cookiecutter.project_name}}"
GITHUB_USERNAME = "{{cookiecutter.github_username}}"
GITHUB_REPO_NAME = "{{cookiecutter.github_repo_name}}"
ENABLE_INTERROGATE = "{{cookiecutter.enable_interrogate}}" == "yes"
ENABLE_DOCS = "{{cookiecutter.enable_docs}}" == "yes"

LICENSE_FILES = {
    "MIT": "LICENSE_MIT",
    "Apache-2.0": "LICENSE_APACHE_2.0",
    "GPL-3.0": "LICENSE_GPL_3.0",
    "Proprietary": "LICENSE_PROPRIETARY",
}

# Files and directories that only exist for an optional feature.
OPTIONAL_PATHS = {
    "interrogate": (
        ENABLE_INTERROGATE,
        [".github/workflows/interrogate-badge.yml"],
    ),
    "docs": (
        ENABLE_DOCS,
        [
            ".github/workflows/docs.yml",
            ".github/workflows/links-md.yml",
            ".github/workflows/links-html-scheduled.yml",
            ".lychee.toml",
            "mkdocs.yml",
            "docs",
        ],
    ),
}


def _remove(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def _run(*cmd: str) -> subprocess.CompletedProcess[str] | None:
    """Run a command, returning None if the executable is not installed."""
    try:
        return subprocess.run(cmd, capture_output=True, text=True, check=False)
    except FileNotFoundError:
        return None


# License
shutil.copy(Path("licenses") / LICENSE_FILES[LICENSE], "LICENSE")
shutil.rmtree("licenses")

# Optional features
for enabled, paths in OPTIONAL_PATHS.values():
    if not enabled:
        for p in paths:
            _remove(Path(p))

# Lock file: best effort (needs uv and network access). CI uses `--locked`,
# so committing uv.lock from the start keeps the first push green.
lock = _run("uv", "lock", "--quiet")
locked = lock is not None and lock.returncode == 0
if not locked:
    print("\nNote: could not create uv.lock; run `uv lock` and commit it.")

# Git: best effort, never fail generation.
committed = False
init = _run("git", "init", "-b", "main")
if init is None:
    print("\nNote: git not found; skipping repository initialization.")
else:
    _run("git", "add", "-A")
    commit = _run("git", "commit", "-m", "chore: initial project scaffold")
    committed = commit is not None and commit.returncode == 0
    if not committed:
        print("\nNote: initial commit skipped; configure git user.name/email")
        print("      and commit manually.")

# Summary
print(f"\n✔  Project '{PROJECT_NAME}' created successfully.\n")
print("Next steps:\n")
print(f"  cd {GITHUB_REPO_NAME}")
print("  uv sync")
print("  uv run pre-commit install")
if not committed:
    print("  git add -A && git commit -m 'chore: initial project scaffold'")
print("\n  # Create the GitHub repository and push (requires the gh CLI):")
print(
    f"  gh repo create {GITHUB_USERNAME}/{GITHUB_REPO_NAME} --public "
    "--source=. --remote=origin --push"
)
print()
