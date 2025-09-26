# =============================================================================
# FLEXT-PLUGIN - Plugin Management System Makefile
# =============================================================================
# Python 3.13+ Plugin Framework - Clean Architecture + DDD + Zero Tolerance
# =============================================================================

# Project Configuration
PROJECT_NAME := flext-plugin
PYTHON_VERSION := 3.13
POETRY := poetry
SRC_DIR := src
TESTS_DIR := tests
COV_DIR := flext_plugin

# Quality Standards
MIN_COVERAGE := 85

# Plugin Configuration
FLEXT_PLUGIN_HOT_RELOAD := true
FLEXT_PLUGIN_WATCH_INTERVAL := 2
FLEXT_PLUGIN_DISCOVERY_PATHS := plugins:~/.flext/plugins:/opt/flext/plugins
FLEXT_PLUGIN_CACHE_DIR := .plugin_cache

# Export Configuration
export PROJECT_NAME PYTHON_VERSION MIN_COVERAGE FLEXT_PLUGIN_HOT_RELOAD FLEXT_PLUGIN_WATCH_INTERVAL FLEXT_PLUGIN_DISCOVERY_PATHS FLEXT_PLUGIN_CACHE_DIR

# =============================================================================
# HELP & INFORMATION
# =============================================================================

.PHONY: help
help: ## Show available commands
	@echo "FLEXT-PLUGIN - Plugin Management System"
	@echo "======================================="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \\033[36m%-15s\\033[0m %s\\n", $$1, $$2}'

.PHONY: info
info: ## Show project information
	@echo "Project: $(PROJECT_NAME)"
	@echo "Python: $(PYTHON_VERSION)+"
	@echo "Poetry: $(POETRY)"
	@echo "Coverage: $(MIN_COVERAGE)% minimum (MANDATORY)"
	@echo "Plugin Hot Reload: $(FLEXT_PLUGIN_HOT_RELOAD)"
	@echo "Watch Interval: $(FLEXT_PLUGIN_WATCH_INTERVAL)s"
	@echo "Discovery Paths: $(FLEXT_PLUGIN_DISCOVERY_PATHS)"
	@echo "Architecture: Clean Architecture + DDD + Plugin System"

# =============================================================================
# SETUP & INSTALLATION
# =============================================================================

.PHONY: install
install: ## Install dependencies
	$(POETRY) install

.PHONY: install-dev
install-dev: ## Install dev dependencies
	$(POETRY) install --with dev,test,docs

.PHONY: setup
setup: install-dev ## Complete project setup
	$(POETRY) run pre-commit install

# =============================================================================
# QUALITY GATES (MANDATORY - ZERO TOLERANCE)
# =============================================================================

.PHONY: validate
validate: lint type-check security test ## Run all quality gates (MANDATORY ORDER)

.PHONY: check
check: lint type-check ## Quick health check

.PHONY: lint
lint: ## Run linting (ZERO TOLERANCE)
	$(POETRY) run ruff check .

.PHONY: format
format: ## Format code
	$(POETRY) run ruff format .

.PHONY: type-check
type-check: ## Run type checking with Pyrefly (ZERO TOLERANCE)
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pyrefly check .

.PHONY: security
security: ## Run security scanning
	$(POETRY) run bandit -r $(SRC_DIR)
	$(POETRY) run pip-audit

.PHONY: fix
fix: ## Auto-fix issues
	$(POETRY) run ruff check . --fix
	$(POETRY) run ruff format .

# =============================================================================
# TESTING (MANDATORY - 100% COVERAGE)
# =============================================================================

.PHONY: test
test: ## Run tests with 100% coverage (MANDATORY)
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -q --maxfail=10000 --cov=$(COV_DIR) --cov-report=term-missing:skip-covered --cov-fail-under=$(MIN_COVERAGE)

.PHONY: test-unit
test-unit: ## Run unit tests
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -m "not integration" -v

.PHONY: test-integration
test-integration: ## Run integration tests with Docker
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -m integration -v

.PHONY: test-plugin
test-plugin: ## Run plugin specific tests
	$(POETRY) run pytest $(TESTS_DIR) -m plugin -v

.PHONY: test-hot-reload
test-hot-reload: ## Run hot reload tests
	$(POETRY) run pytest $(TESTS_DIR) -m hot_reload -v

.PHONY: test-discovery
test-discovery: ## Run plugin discovery tests
	$(POETRY) run pytest $(TESTS_DIR) -k discovery -v

.PHONY: test-e2e
test-e2e: ## Run end-to-end tests
	$(POETRY) run pytest $(TESTS_DIR) -m e2e -v

.PHONY: test-fast
test-fast: ## Run tests without coverage
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -v

.PHONY: coverage-html
coverage-html: ## Generate HTML coverage report
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest --cov=$(COV_DIR) --cov-report=html

# =============================================================================
# BUILD & DISTRIBUTION
# =============================================================================

.PHONY: build
build: ## Build package
	$(POETRY) build

.PHONY: build-clean
build-clean: clean build ## Clean and build

# =============================================================================
# PLUGIN OPERATIONS
# =============================================================================

.PHONY: plugin-test
plugin-test: ## Test plugin system core functionality
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c "from flext_plugin import FlextPluginPlatform; platform = FlextPluginPlatform(); print('Plugin platform test passed')"

.PHONY: plugin-validate
plugin-validate: ## Validate plugin system
	@echo "⚠️  PluginManager import requires CLI implementation - see CLAUDE.md"
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c "from flext_plugin import FlextPluginPlatform; platform = FlextPluginPlatform(); print('Plugin system validated via FlextPluginPlatform')"

.PHONY: plugin-create
plugin-create: ## Create plugin (usage: make plugin-create NAME=my-plugin TYPE=extractor)
	@echo "⚠️  CLI not implemented - see CLAUDE.md GAP 1"
	@if [ -z "$(NAME)" ] || [ -z "$(TYPE)" ]; then \
		echo "Usage: make plugin-create NAME=my-plugin TYPE=extractor|loader|transformer"; \
		echo "Note: Requires CLI implementation in src/flext_plugin/cli.py"; \
		exit 1; \
	fi
	@echo "Would run: flext-plugin create $(NAME) --type $(TYPE)"
	@echo "To implement: Create src/flext_plugin/cli.py with main() entry point"

.PHONY: plugin-install
plugin-install: ## Install plugin (usage: make plugin-install NAME=tap-github)
	@echo "⚠️  CLI not implemented - see CLAUDE.md GAP 1"
	@if [ -z "$(NAME)" ]; then \
		echo "Usage: make plugin-install NAME=plugin-name"; \
		echo "Note: Requires CLI implementation in src/flext_plugin/cli.py"; \
		exit 1; \
	fi
	@echo "Would run: flext-plugin install $(NAME)"

.PHONY: plugin-list
plugin-list: ## List available plugins
	@echo "⚠️  CLI not implemented - see CLAUDE.md GAP 1"
	@echo "Would run: flext-plugin list"
	@echo "To implement: Create plugin discovery and listing functionality"

.PHONY: plugin-watch
plugin-watch: ## Watch plugins with hot reload
	@echo "⚠️  CLI not implemented - see CLAUDE.md GAP 1"
	@echo "Would run: flext-plugin watch --enable-hot-reload"
	@echo "Hot reload configuration: FLEXT_PLUGIN_HOT_RELOAD=$(FLEXT_PLUGIN_HOT_RELOAD)"

.PHONY: plugin-reload
plugin-reload: ## Hot reload all plugins
	@echo "⚠️  hot_reload_all function not implemented - see CLAUDE.md GAP 2"
	@echo "To implement: Complete hot_reload.py integration with plugin platform"

.PHONY: plugin-discovery
plugin-discovery: ## Test plugin discovery
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c "from flext_plugin.application.services import FlextPluginDiscoveryService; service = FlextPluginDiscoveryService(); print('Plugin discovery service OK')"

.PHONY: plugin-operations
plugin-operations: plugin-test plugin-validate plugin-discovery ## Run all plugin validations

# =============================================================================
# DOCUMENTATION
# =============================================================================

.PHONY: docs
docs: ## Build documentation
	$(POETRY) run mkdocs build

.PHONY: docs-serve
docs-serve: ## Serve documentation
	$(POETRY) run mkdocs serve

# =============================================================================
# DEPENDENCIES
# =============================================================================

.PHONY: deps-update
deps-update: ## Update dependencies
	$(POETRY) update

.PHONY: deps-show
deps-show: ## Show dependency tree
	$(POETRY) show --tree

.PHONY: deps-audit
deps-audit: ## Audit dependencies
	$(POETRY) run pip-audit

# =============================================================================
# DEVELOPMENT
# =============================================================================

.PHONY: shell
shell: ## Open Python shell
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks
	$(POETRY) run pre-commit run --all-files

# =============================================================================
# MAINTENANCE
# =============================================================================

.PHONY: clean
clean: ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ htmlcov/ .coverage .mypy_cache/ .pyrefly_cache/ .ruff_cache/
	rm -rf $(FLEXT_PLUGIN_CACHE_DIR)/ plugins/ plugin_cache/ dev_plugins/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

.PHONY: clean-all
clean-all: clean ## Deep clean including venv
	rm -rf .venv/

.PHONY: reset
reset: clean-all setup ## Reset project

# =============================================================================
# DIAGNOSTICS
# =============================================================================

.PHONY: diagnose
diagnose: ## Project diagnostics
	@echo "Python: $$(python --version)"
	@echo "Poetry: $$($(POETRY) --version)"
	@echo "Plugin System: $$(PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c 'import flext_plugin; print(getattr(flext_plugin, \"__version__\", \"dev\"))' 2>/dev/null || echo 'Not available')"
	@echo "Watchdog: $$(PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c 'import watchdog; print(watchdog.__version__)' 2>/dev/null || echo 'Not available')"
	@$(POETRY) env info

.PHONY: doctor
doctor: diagnose check ## Health check

# =============================================================================

# =============================================================================

.PHONY: t l f tc c i v
t: test
l: lint
f: format
tc: type-check
c: clean
i: install
v: validate

# =============================================================================
# CONFIGURATION
# =============================================================================

.DEFAULT_GOAL := help
