"""Validate cookiecutter inputs before project generation."""

import re

PROJECT_SLUG = "{{cookiecutter.project_slug}}"
GITHUB_REPO_NAME = "{{cookiecutter.github_repo_name}}"
AUTHOR_EMAIL = "{{cookiecutter.author_email}}"


if not re.match(r"^[a-z][a-z0-9_]+$", PROJECT_SLUG):
    raise ValueError(
        f"Invalid project_slug '{PROJECT_SLUG}'. "
        "Must start with a lowercase letter and contain only lowercase letters, digits, and underscores."
    )

if not re.match(r"^[a-z][a-z0-9-]+$", GITHUB_REPO_NAME):
    raise ValueError(
        f"Invalid github_repo_name '{GITHUB_REPO_NAME}'. "
        "Must start with a lowercase letter and contain only lowercase letters, digits, and hyphens."
    )

if "@" not in AUTHOR_EMAIL:
    raise ValueError(f"Invalid author_email '{AUTHOR_EMAIL}'.")
