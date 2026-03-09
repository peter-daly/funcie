.PHONY: typecheck lint format test ci publish

UV := env -u VIRTUAL_ENV uv
UV_RUN := $(UV) run

typecheck:
	@echo "Typechecking"
	@$(UV_RUN) ty check .

lint:
	@echo "Linting with Ruff..."
	@$(UV_RUN) ruff check .

format:
	@echo "Checking format with Ruff..."
	@$(UV_RUN) ruff format --check .

test:
	@echo "Running tests..."
	@$(UV_RUN) pytest .

ci: lint format typecheck test

publish:
	@echo "Publishing to PyPI..."
	@$(UV) build
	@$(UV) publish --token $$PYPI_TOKEN
