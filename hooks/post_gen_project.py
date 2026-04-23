"""Post-generation hook: install correct license, initialize git repo."""

import os
import shutil
import subprocess

LICENSE = "{{cookiecutter.license}}"
PROJECT_NAME = "{{cookiecutter.project_name}}"
GITHUB_USERNAME = "{{cookiecutter.github_username}}"
GITHUB_REPO_NAME = "{{cookiecutter.github_repo_name}}"

# ── License ──────────────────────────────────────────────────────────────────

LICENSE_FILES = {
    "MIT": "licenses/LICENSE_MIT",
    "Apache-2.0": "licenses/LICENSE_APACHE_2.0",
    "GPL-3.0": "licenses/LICENSE_GPL_3.0",
    "Proprietary": "licenses/LICENSE_PROPRIETARY",
}

shutil.copy(os.path.join(os.getcwd(), LICENSE_FILES[LICENSE]), "LICENSE")
shutil.rmtree(os.path.join(os.getcwd(), "licenses"))


# ── Git ───────────────────────────────────────────────────────────────────────

def _run(*cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(list(cmd), capture_output=True, text=True)


git_ok = False
try:
    # Prefer explicit 'main' branch; fall back for Git < 2.28
    if _run("git", "init", "-b", "main").returncode != 0:
        _run("git", "init")

    _run("git", "add", "-A")
    result = _run("git", "commit", "-m", "chore: initial project scaffold")
    if result.returncode != 0:
        # Likely no user.name / user.email configured globally — still usable
        print(f"\nNote: initial commit skipped ({result.stderr.strip()}).")
        print("      Run `git config --global user.name/email` and commit manually.")
    else:
        git_ok = True
except FileNotFoundError:
    print("\nNote: git not found; skipping repository initialization.")


# ── Summary ───────────────────────────────────────────────────────────────────

print(f"\n✔  Project '{PROJECT_NAME}' created successfully.")

print("\nNext steps:")
print(f"\n  cd {GITHUB_REPO_NAME}")
print("  uv sync")
print("  uv run pre-commit install")

if not git_ok:
    print("\n  # Initialize git (skipped above):")
    print("  git init -b main && git add -A && git commit -m 'chore: initial project scaffold'")

print("\n  # Create the GitHub repository and push in one step (requires gh CLI):")
print(f"  gh repo create {GITHUB_REPO_NAME} --public --source=. --remote=origin --push")
print("\n  # Or manually:")
print(f"  git remote add origin git@github.com:{GITHUB_USERNAME}/{GITHUB_REPO_NAME}.git")
print("  git push -u origin main")
print()
