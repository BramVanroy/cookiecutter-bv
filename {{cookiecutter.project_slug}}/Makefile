.PHONY: quality style test{% if cookiecutter.enable_mypy == "yes" %} typecheck{% endif %}{% if cookiecutter.enable_docs == "yes" %} docs serve-docs{% endif %}

PACKAGE = src/{{cookiecutter.project_slug}}

quality:
{%- if cookiecutter.enable_interrogate == "yes" %}
	uv run interrogate -vv
{%- endif %}
	uv run ruff check $(PACKAGE) tests/ scripts/
	uv run ruff format --check $(PACKAGE) tests/ scripts/

style:
	uv run ruff check $(PACKAGE) tests/ scripts/ --fix
	uv run ruff format $(PACKAGE) tests/ scripts/

test:
	uv run pytest --cov=$(PACKAGE) --cov-report=term-missing --cov-report=xml
{%- if cookiecutter.enable_mypy == "yes" %}

typecheck:
	uv run mypy $(PACKAGE) tests/ scripts/
{%- endif %}
{%- if cookiecutter.enable_docs == "yes" %}

docs:
	uv run mkdocs serve

DOCS_BRANCH ?= tmp-gh-pages
DOCS_VERSION ?= 0.0.0
DOCS_ALIAS ?= latest
DOCS_ADDR ?= 127.0.0.1:8000
DOCS_SOURCE_REF ?= main

serve-docs:
	DOCS_SOURCE_REF=$(DOCS_SOURCE_REF) uv run mike deploy --branch $(DOCS_BRANCH) --update-aliases $(DOCS_VERSION) $(DOCS_ALIAS)
	uv run mike set-default --branch $(DOCS_BRANCH) $(DOCS_ALIAS)
	uv run mike serve -b $(DOCS_BRANCH) -a $(DOCS_ADDR)
{%- endif %}

