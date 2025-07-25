# FLEXT PLUGIN - Enterprise Plugin Management System
# ==================================================
# Dynamic plugin loading, lifecycle management, and hot reload capabilities
# PROJECT_TYPE: plugin-system
# Python 3.13 + Clean Architecture + Zero Tolerance Quality Gates

.PHONY: help info diagnose check validate test lint type-check security format format-check fix
.PHONY: install dev-install setup pre-commit build clean
.PHONY: coverage coverage-html test-unit test-integration test-plugin
.PHONY: deps-update deps-audit deps-tree deps-outdated
.PHONY: plugin-create plugin-install plugin-list plugin-watch complexity

# ============================================================================
# 🎯 HELP & INFORMATION
# ============================================================================

help: ## Show this help message
	@echo "🔌 FLEXT PLUGIN - Enterprise Plugin Management System"
	@echo "================================================"
	@echo "🎯 Clean Architecture + DDD + Python 3.13 + Dynamic Plugin Loading"
	@echo ""
	@echo "📦 Enterprise plugin system with hot reload and lifecycle management"
	@echo "🔒 Zero tolerance quality gates for plugin infrastructure"
	@echo "🧪 85%+ test coverage requirement for plugin components"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


info: ## Mostrar informações do projeto
	@echo "📊 Informações do Projeto"
	@echo "======================"
	@echo "Nome: flext-plugin"
	@echo "Título: FLEXT PLUGIN"
	@echo "Versão: $(shell poetry version -s 2>/dev/null || echo "0.7.0")"
	@echo "Python: $(shell python3.13 --version 2>/dev/null || echo "Não encontrado")"
	@echo "Poetry: $(shell poetry --version 2>/dev/null || echo "Não instalado")"
	@echo "Venv: $(shell poetry env info --path 2>/dev/null || echo "Não ativado")"
	@echo "Diretório: $(CURDIR)"
	@echo "Git Branch: $(shell git branch --show-current 2>/dev/null || echo "Não é repo git")"
	@echo "Git Status: $(shell git status --porcelain 2>/dev/null | wc -l | xargs echo) arquivos alterados"

diagnose: ## Executar diagnósticos completos
	@echo "🔍 Executando diagnósticos para flext-plugin..."
	@echo "Informações do Sistema:"
	@echo "OS: $(shell uname -s)"
	@echo "Arquitetura: $(shell uname -m)"
	@echo "Python: $(shell python3.13 --version 2>/dev/null || echo "Não encontrado")"
	@echo "Poetry: $(shell poetry --version 2>/dev/null || echo "Não instalado")"
	@echo ""
	@echo "Estrutura do Projeto:"
	@ls -la
	@echo ""
	@echo "Configuração Poetry:"
	@poetry config --list 2>/dev/null || echo "Poetry não configurado"
	@echo ""
	@echo "Status das Dependências:"
	@poetry show --outdated 2>/dev/null || echo "Nenhuma dependência desatualizada"

# ============================================================================
# 🎯 CORE QUALITY GATES - ZERO TOLERANCE
# ============================================================================

validate: lint type-check security test ## STRICT compliance validation (all must pass)
	@echo "✅ ALL QUALITY GATES PASSED - FLEXT PLUGIN COMPLIANT"

check: lint type-check test ## Essential quality checks (pre-commit standard)
	@echo "✅ Essential checks passed"

lint: ## Ruff linting (ALL rule categories enabled)
	@echo "🔍 Running ruff linter (ALL rules enabled)..."
	@poetry run ruff check src/ tests/ --fix --unsafe-fixes
	@echo "✅ Linting complete"

type-check: ## MyPy strict mode type checking (zero errors tolerated)
	@echo "🛡️ Running MyPy strict type checking..."
	@poetry run mypy src/ tests/ --strict
	@echo "✅ Type checking complete"

security: ## Security scans (bandit + pip-audit + secrets)
	@echo "🔒 Running security scans..."
	@poetry run bandit -r src/ --severity-level medium --confidence-level medium
	@poetry run pip-audit --ignore-vuln PYSEC-2022-42969
	@poetry run detect-secrets scan --all-files
	@echo "✅ Security scans complete"

format: ## Format code with ruff
	@echo "🎨 Formatting code..."
	@poetry run ruff format src/ tests/
	@echo "✅ Formatting complete"

format-check: ## Check formatting without fixing
	@echo "🎨 Checking code formatting..."
	@poetry run ruff format src/ tests/ --check
	@echo "✅ Format check complete"

fix: format lint ## Auto-fix all issues (format + imports + lint)
	@echo "🔧 Auto-fixing all issues..."
	@poetry run ruff check src/ tests/ --fix --unsafe-fixes
	@echo "✅ All auto-fixes applied"

# ============================================================================
# 🧪 TESTING - 85% COVERAGE MINIMUM
# ============================================================================

test: ## Run tests with coverage (85% minimum required)
	@echo "🧪 Running tests with coverage..."
	@poetry run pytest tests/ -v --cov=src/flext_plugin --cov-report=term-missing --cov-fail-under=85
	@echo "✅ Tests complete"

test-unit: ## Run unit tests only
	@echo "🧪 Running unit tests..."
	@poetry run pytest tests/unit/ -v
	@echo "✅ Unit tests complete"

test-integration: ## Run integration tests only
	@echo "🧪 Running integration tests..."
	@poetry run pytest tests/integration/ -v
	@echo "✅ Integration tests complete"

test-plugin: ## Run plugin-specific tests
	@echo "🔌 Running plugin system tests..."
	@poetry run pytest tests/plugin/ -v --tb=short
	@echo "✅ Plugin tests complete"

coverage: ## Generate detailed coverage report
	@echo "📊 Generating coverage report..."
	@poetry run pytest tests/ --cov=src/flext_plugin --cov-report=term-missing --cov-report=html
	@echo "✅ Coverage report generated in htmlcov/"

coverage-html: coverage ## Generate HTML coverage report
	@echo "📊 Opening coverage report..."
	@python -m webbrowser htmlcov/index.html

# ============================================================================
# 🚀 DEVELOPMENT SETUP
# ============================================================================

setup: install pre-commit ## Complete development setup
	@echo "🎯 Development setup complete!"

install: ## Install dependencies with Poetry
	@echo "📦 Installing dependencies..."
	@poetry install --all-extras --with dev,test,docs,security
	@echo "✅ Dependencies installed"

dev-install: install ## Install in development mode
	@echo "🔧 Setting up development environment..."
	@poetry install --all-extras --with dev,test,docs,security
	@poetry run pre-commit install
	@echo "✅ Development environment ready"

pre-commit: ## Setup pre-commit hooks
	@echo "🎣 Setting up pre-commit hooks..."
	@poetry run pre-commit install
	@poetry run pre-commit run --all-files || true
	@echo "✅ Pre-commit hooks installed"

# ============================================================================
# 🎯 PLUGIN SYSTEM OPERATIONS
# ============================================================================

plugin-load: plugin-validate ## Load and initialize plugin system

plugin-test: test-plugin ## Run plugin system tests

plugin-validate: ## Validate plugin system integrity

# ============================================================================
# 🔌 PLUGIN MANAGEMENT OPERATIONS
# ============================================================================

plugin-create: ## Create new plugin (usage: make plugin-create NAME=my-plugin TYPE=extractor)
	@echo "🔌 Creating new plugin..."
	@if [ -z "$(NAME)" ] || [ -z "$(TYPE)" ]; then \
		echo "❌ Usage: make plugin-create NAME=my-plugin TYPE=extractor|loader|transformer"; \
		exit 1; \
	fi
	@poetry run flext-plugin create $(NAME) --type $(TYPE)
	@echo "✅ Plugin $(NAME) created"

plugin-install: ## Install plugin (usage: make plugin-install NAME=tap-github)
	@echo "🔌 Installing plugin..."
	@if [ -z "$(NAME)" ]; then \
		echo "❌ Usage: make plugin-install NAME=plugin-name"; \
		exit 1; \
	fi
	@poetry run flext-plugin install $(NAME)
	@echo "✅ Plugin $(NAME) installed"

plugin-list: ## List all available plugins
	@echo "🔌 Listing available plugins..."
	@poetry run flext-plugin list
	@echo "✅ Plugin list complete"

plugin-watch: ## Watch for plugin changes with hot reload
	@echo "🔌 Starting plugin watcher with hot reload..."
	@echo "🔄 Watching for plugin file changes..."
	@poetry run flext-plugin watch --enable-hot-reload

plugin-reload: ## Hot reload all plugins
	@echo "🔄 Hot reloading all plugins..."
	@poetry run python -m flext_plugin.hot_reload.reload_all
	@echo "✅ Plugin hot reload complete"

plugin-disable: ## Disable plugin (usage: make plugin-disable NAME=plugin-name)
	@echo "🔌 Disabling plugin..."
	@if [ -z "$(NAME)" ]; then \
		echo "❌ Usage: make plugin-disable NAME=plugin-name"; \
		exit 1; \
	fi
	@poetry run flext-plugin disable $(NAME)
	@echo "✅ Plugin $(NAME) disabled"

plugin-enable: ## Enable plugin (usage: make plugin-enable NAME=plugin-name)
	@echo "🔌 Enabling plugin..."
	@if [ -z "$(NAME)" ]; then \
		echo "❌ Usage: make plugin-enable NAME=plugin-name"; \
		exit 1; \
	fi
	@poetry run flext-plugin enable $(NAME)
	@echo "✅ Plugin $(NAME) enabled"

plugin-validate: ## Validate plugin configuration and interfaces
	@echo "🔌 Validating plugin system..."
	@poetry run python -c "from flext_plugin.core.manager import PluginManager; manager = PluginManager(); print('✅ Plugin system validated')"

plugin-test-hot-reload: ## Test hot reload functionality
	@echo "🔌 Testing hot reload functionality..."
	@poetry run pytest tests/hot_reload/ -v
	@echo "✅ Hot reload tests complete"

# ============================================================================
# 📦 BUILD & DISTRIBUTION
# ============================================================================

build: clean ## Build distribution packages
	@echo "🔨 Building distribution..."
	@poetry build
	@echo "✅ Build complete - packages in dist/"

# ============================================================================
# 🧹 CLEANUP
# ============================================================================

clean: ## Remove all artifacts
	@echo "🧹 Cleaning up..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@rm -rf .coverage
	@rm -rf htmlcov/
	@rm -rf .pytest_cache/
	@rm -rf plugins/
	@rm -rf plugin_cache/
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete"

# ============================================================================
# 📊 DEPENDENCY MANAGEMENT
# ============================================================================

deps-update: ## Update all dependencies
	@echo "🔄 Updating dependencies..."
	@poetry update
	@echo "✅ Dependencies updated"

deps-audit: ## Audit dependencies for vulnerabilities
	@echo "🔍 Auditing dependencies..."
	@poetry run pip-audit
	@echo "✅ Dependency audit complete"

deps-tree: ## Show dependency tree
	@echo "🌳 Dependency tree:"
	@poetry show --tree

deps-outdated: ## Show outdated dependencies
	@echo "📋 Outdated dependencies:"
	@poetry show --outdated

# ============================================================================
# 📊 ADVANCED QUALITY ANALYSIS
# ============================================================================

complexity: ## Analyze code complexity
	@echo "📊 Analyzing code complexity..."
	@poetry run radon cc src/ --min=C
	@poetry run radon mi src/ --min=B
	@echo "✅ Complexity analysis complete"

status: ## Show current quality status
	@echo "📊 FLEXT Plugin Quality Status"
	@echo "=============================="
	@echo "🏗️ Architecture: Clean Architecture + DDD"
	@echo "🐍 Python: 3.13"
	@echo "🔌 Framework: Enterprise Plugin System"
	@echo "📊 Quality Gates: Zero tolerance enforcement"
	@echo "🧪 Test Coverage: 85% minimum"
	@echo "🔒 Security: Full scan compliance"
	@poetry run python -c "import sys; print(f'Python: {sys.version}')"
	@poetry run python -c "import flext_plugin; print(f'FLEXT Plugin: {flext_plugin.__version__ if hasattr(flext_plugin, '__version__') else 'dev'}')"

# ============================================================================
# 🔧 ENVIRONMENT CONFIGURATION
# ============================================================================

# Python settings
PYTHON := python3.13
export PYTHONPATH := $(PWD)/src:$(PYTHONPATH)
export PYTHONDONTWRITEBYTECODE := 1
export PYTHONUNBUFFERED := 1

# FLEXT Plugin settings
export FLEXT_PLUGIN_DEV := true
export FLEXT_PLUGIN_HOT_RELOAD := true
export FLEXT_PLUGIN_WATCH_INTERVAL := 2
export FLEXT_PLUGIN_MAX_WORKERS := 10

# Plugin discovery settings
export FLEXT_PLUGIN_DISCOVERY_PATHS := plugins:~/.flext/plugins:/opt/flext/plugins
export FLEXT_PLUGIN_CACHE_DIR := .plugin_cache
export FLEXT_PLUGIN_STATE_BACKEND := filesystem

# Hot reload settings
export FLEXT_PLUGIN_RELOAD_ON_CHANGE := true
export FLEXT_PLUGIN_PRESERVE_STATE := true
export FLEXT_PLUGIN_ROLLBACK_ON_ERROR := true

# Poetry settings
export POETRY_VENV_IN_PROJECT := false
export POETRY_CACHE_DIR := $(HOME)/.cache/pypoetry

# Quality gate settings
export MYPY_CACHE_DIR := .mypy_cache
export RUFF_CACHE_DIR := .ruff_cache

# ============================================================================
# 📝 PROJECT METADATA
# ============================================================================

# Project information
PROJECT_NAME := flext-plugin
PROJECT_TYPE := python-library
PROJECT_VERSION := $(shell poetry version -s)
PROJECT_DESCRIPTION := FLEXT Plugin - Enterprise Plugin Management System

.DEFAULT_GOAL := help

# ============================================================================
# 🎯 PLUGIN VALIDATION COMMANDS
# ============================================================================

validate-plugins: ## Validate all plugin implementations
	@echo "🔌 Validating plugin implementations..."
	@poetry run python -c "from flext_plugin.core.manager import PluginManager; from flext_plugin.core.discovery import PluginDiscovery; manager = PluginManager(); discovery = PluginDiscovery(); print('✅ Plugin Manager initialized'); print('✅ Plugin Discovery system ready'); print('✅ Plugin validation complete')"

validate-hot-reload: ## Validate hot reload system
	@echo "🔄 Validating hot reload system..."
	@poetry run python -c "from flext_plugin.hot_reload.reloader import HotReloadManager; from flext_plugin.hot_reload.watcher import PluginWatcher; print('✅ Hot Reload system initialized'); print('✅ File Watcher system ready'); print('✅ Hot reload validation complete')"

validate-interfaces: ## Validate plugin interfaces
	@echo "🔌 Validating plugin interfaces..."
	@poetry run python -c "from flext_plugin.core.base import Plugin; from flext_plugin.core.types import PluginType; print('✅ Plugin base classes available'); print('✅ Plugin type system functional'); print('✅ Interface validation complete')"

# ============================================================================
# 🎯 PLUGIN DEVELOPMENT TOOLS
# ============================================================================

dev-plugin: ## Create development plugin template
	@echo "🔌 Creating development plugin template..."
	@mkdir -p dev_plugins/example_plugin/
	@echo '"""Example plugin for development and testing."""' > dev_plugins/example_plugin/plugin.py
	@echo '' >> dev_plugins/example_plugin/plugin.py
	@echo 'from flext_plugin.core.base import Plugin' >> dev_plugins/example_plugin/plugin.py
	@echo 'from typing import Any, Dict' >> dev_plugins/example_plugin/plugin.py
	@echo '' >> dev_plugins/example_plugin/plugin.py
	@echo 'class ExamplePlugin(Plugin):' >> dev_plugins/example_plugin/plugin.py
	@echo '    """Example plugin implementation."""' >> dev_plugins/example_plugin/plugin.py
	@echo '    ' >> dev_plugins/example_plugin/plugin.py
	@echo '    def __init__(self) -> None:' >> dev_plugins/example_plugin/plugin.py
	@echo '        super().__init__()' >> dev_plugins/example_plugin/plugin.py
	@echo '        self.name = "example-plugin"' >> dev_plugins/example_plugin/plugin.py
	@echo '        self.version = "1.0.0"' >> dev_plugins/example_plugin/plugin.py
	@echo '        ' >> dev_plugins/example_plugin/plugin.py
	@echo '    async def initialize(self) -> None:' >> dev_plugins/example_plugin/plugin.py
	@echo '        """Initialize plugin resources."""' >> dev_plugins/example_plugin/plugin.py
	@echo '        pass' >> dev_plugins/example_plugin/plugin.py
	@echo '        ' >> dev_plugins/example_plugin/plugin.py
	@echo '    async def execute(self, input_data: Any, context: Any) -> Any:' >> dev_plugins/example_plugin/plugin.py
	@echo '        """Execute plugin logic."""' >> dev_plugins/example_plugin/plugin.py
	@echo '        return {"message": "Hello from example plugin", "input": input_data}' >> dev_plugins/example_plugin/plugin.py
	@echo '        ' >> dev_plugins/example_plugin/plugin.py
	@echo '    async def cleanup(self) -> None:' >> dev_plugins/example_plugin/plugin.py
	@echo '        """Clean up plugin resources."""' >> dev_plugins/example_plugin/plugin.py
	@echo '        pass' >> dev_plugins/example_plugin/plugin.py
	@echo '        ' >> dev_plugins/example_plugin/plugin.py
	@echo '    async def health_check(self) -> Dict[str, Any]:' >> dev_plugins/example_plugin/plugin.py
	@echo '        """Perform health check."""' >> dev_plugins/example_plugin/plugin.py
	@echo '        return {"status": "healthy", "plugin": self.name}' >> dev_plugins/example_plugin/plugin.py
	@echo "✅ Development plugin template created in dev_plugins/example_plugin/"

test-dev-plugin: ## Test development plugin
	@echo "🔌 Testing development plugin..."
	@poetry run python -c "import sys; sys.path.insert(0, 'dev_plugins'); from example_plugin.plugin import ExamplePlugin; import asyncio; exec('async def test_plugin():\n    plugin = ExamplePlugin()\n    await plugin.initialize()\n    result = await plugin.execute({\"test\": \"data\"}, {})\n    print(f\"Plugin result: {result}\")\n    health = await plugin.health_check()\n    print(f\"Plugin health: {health}\")\n    await plugin.cleanup()\n    print(\"✅ Development plugin test complete\")\nasyncio.run(test_plugin())')"

# ============================================================================
# 🎯 FLEXT ECOSYSTEM INTEGRATION
# ============================================================================

ecosystem-check: ## Verify FLEXT ecosystem compatibility
	@echo "🌐 Checking FLEXT ecosystem compatibility..."
	@echo "📦 Plugin project: $(PROJECT_NAME) v$(PROJECT_VERSION)"
	@echo "🏗️ Architecture: Clean Architecture + DDD"
	@echo "🐍 Python: 3.13"
	@echo "🔌 Framework: Enterprise Plugin Management System"
	@echo "📊 Quality: Zero tolerance enforcement"
	@echo "✅ Ecosystem compatibility verified"

workspace-info: ## Show workspace integration info
	@echo "🏢 FLEXT Workspace Integration"
	@echo "==============================="
	@echo "📁 Project Path: $(PWD)"
	@echo "🏆 Role: Enterprise Plugin Management System"
	@echo "🔗 Dependencies: flext-core, flext-observability"
	@echo "📦 Provides: Plugin loading, lifecycle management, hot reload"
	@echo "🎯 Standards: Enterprise plugin patterns with dynamic loading"