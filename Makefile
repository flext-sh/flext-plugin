# FLEXT-PLUGIN Makefile
PROJECT_NAME := flext-plugin
PYTHON_VERSION := 3.13
POETRY := poetry
SRC_DIR := src
TESTS_DIR := tests

# Quality standards
MIN_COVERAGE := 85

# Plugin configuration
FLEXT_PLUGIN_HOT_RELOAD := true
FLEXT_PLUGIN_WATCH_INTERVAL := 2

# Help
help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

# Installation
install: ## Install dependencies
	$(POETRY) install

install-dev: ## Install dev dependencies
	$(POETRY) install --with dev,test,docs

setup: install-dev ## Complete project setup
	$(POETRY) run pre-commit install

# Quality gates
validate: lint type-check security test ## Run all quality gates

check: lint type-check ## Quick health check

lint: ## Run linting
	$(POETRY) run ruff check $(SRC_DIR) $(TESTS_DIR)

format: ## Format code
	$(POETRY) run ruff format $(SRC_DIR) $(TESTS_DIR)

type-check: ## Run type checking
	$(POETRY) run mypy $(SRC_DIR) --strict

security: ## Run security scanning
	$(POETRY) run bandit -r $(SRC_DIR)
	$(POETRY) run pip-audit

fix: ## Auto-fix issues
	$(POETRY) run ruff check $(SRC_DIR) $(TESTS_DIR) --fix
	$(POETRY) run ruff format $(SRC_DIR) $(TESTS_DIR)

# Testing
test: ## Run tests with coverage
	$(POETRY) run pytest $(TESTS_DIR) --cov=$(SRC_DIR) --cov-report=term-missing --cov-fail-under=$(MIN_COVERAGE)

test-unit: ## Run unit tests
	$(POETRY) run pytest $(TESTS_DIR) -m "not integration" -v

test-integration: ## Run integration tests
	$(POETRY) run pytest $(TESTS_DIR) -m integration -v

test-plugin: ## Run plugin specific tests
	$(POETRY) run pytest $(TESTS_DIR) -m plugin -v

test-fast: ## Run tests without coverage
	$(POETRY) run pytest $(TESTS_DIR) -v

coverage-html: ## Generate HTML coverage report
	$(POETRY) run pytest $(TESTS_DIR) --cov=$(SRC_DIR) --cov-report=html

# Plugin operations
plugin-create: ## Create plugin (usage: make plugin-create NAME=my-plugin TYPE=extractor)
	@if [ -z "$(NAME)" ] || [ -z "$(TYPE)" ]; then \
		echo "Usage: make plugin-create NAME=my-plugin TYPE=extractor|loader|transformer"; \
		exit 1; \
	fi
	$(POETRY) run flext-plugin create $(NAME) --type $(TYPE)

plugin-install: ## Install plugin (usage: make plugin-install NAME=tap-github)
	@if [ -z "$(NAME)" ]; then \
		echo "Usage: make plugin-install NAME=plugin-name"; \
		exit 1; \
	fi
	$(POETRY) run flext-plugin install $(NAME)

plugin-list: ## List available plugins
	$(POETRY) run flext-plugin list

plugin-watch: ## Watch plugins with hot reload
	$(POETRY) run flext-plugin watch --enable-hot-reload

plugin-validate: ## Validate plugin system
	$(POETRY) run python -c "from flext_plugin import PluginManager; PluginManager(); print('Plugin system validated')"

plugin-reload: ## Hot reload all plugins
	$(POETRY) run python -c "from flext_plugin import hot_reload_all; hot_reload_all()"

# Build
build: ## Build package
	$(POETRY) build

build-clean: clean build ## Clean and build

# Documentation
docs: ## Build documentation
	$(POETRY) run mkdocs build

docs-serve: ## Serve documentation
	$(POETRY) run mkdocs serve

# Dependencies
deps-update: ## Update dependencies
	$(POETRY) update

deps-show: ## Show dependency tree
	$(POETRY) show --tree

deps-audit: ## Audit dependencies
	$(POETRY) run pip-audit

# Development
shell: ## Open Python shell
	$(POETRY) run python

pre-commit: ## Run pre-commit hooks
	$(POETRY) run pre-commit run --all-files

# Maintenance
clean: ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ htmlcov/ .coverage .mypy_cache/ .ruff_cache/
	rm -rf plugins/ plugin_cache/ dev_plugins/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

clean-all: clean ## Deep clean including venv
	rm -rf .venv/

reset: clean-all setup ## Reset project

# Diagnostics
diagnose: ## Project diagnostics
	@echo "Python: $$(python --version)"
	@echo "Poetry: $$($(POETRY) --version)"
	@echo "Plugin System: $$($(POETRY) run python -c 'import flext_plugin; print(getattr(flext_plugin, \"__version__\", \"dev\"))' 2>/dev/null || echo 'Not available')"
	@$(POETRY) env info

doctor: diagnose check ## Health check

# Aliases
t: test
l: lint
f: format
tc: type-check
c: clean
i: install
v: validate

.DEFAULT_GOAL := help
.PHONY: help install install-dev setup validate check lint format type-check security fix test test-unit test-integration test-plugin test-fast coverage-html plugin-create plugin-install plugin-list plugin-watch plugin-validate plugin-reload build build-clean docs docs-serve deps-update deps-show deps-audit shell pre-commit clean clean-all reset diagnose doctor t l f tc c i v