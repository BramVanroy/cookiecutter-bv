.PHONY: quality style typecheck test docs

PACKAGE = src/{{cookiecutter.project_slug}}

quality:
	uv run ruff check $(PACKAGE) tests/ scripts/
	uv run ruff format --check $(PACKAGE) tests/ scripts/

style:
	uv run ruff check $(PACKAGE) tests/ scripts/ --fix
	uv run ruff format $(PACKAGE) tests/ scripts/

typecheck:
	uv run mypy $(PACKAGE) tests/ scripts/

test:
	uv run pytest --cov=$(PACKAGE) --cov-report=term-missing --cov-report=xml

docs:
	uv run mkdocs serve
