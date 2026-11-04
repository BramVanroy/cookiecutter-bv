"""Validate cookiecutter inputs before project generation."""

import keyword
import re
import sys

PROJECT_SLUG = "{{cookiecutter.project_slug}}"
GITHUB_REPO_NAME = "{{cookiecutter.github_repo_name}}"
AUTHOR_EMAIL = "{{cookiecutter.author_email}}"

errors = []

if not re.fullmatch(r"[a-z][a-z0-9_]*", PROJECT_SLUG) or keyword.iskeyword(
    PROJECT_SLUG
):
    errors.append(
        f"Invalid project_slug {PROJECT_SLUG!r}: must be a valid Python "
        "identifier of lowercase letters, digits and underscores, starting "
        "with a letter."
    )

if not re.fullmatch(r"[a-z][a-z0-9_-]*", GITHUB_REPO_NAME):
    errors.append(
        f"Invalid github_repo_name {GITHUB_REPO_NAME!r}: must start with a "
        "lowercase letter and contain only lowercase letters, digits, "
        "underscores and hyphens."
    )

if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", AUTHOR_EMAIL):
    errors.append(f"Invalid author_email {AUTHOR_EMAIL!r}.")

if errors:
    print("\n".join(f"ERROR: {e}" for e in errors), file=sys.stderr)
    sys.exit(1)
