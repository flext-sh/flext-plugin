# FLEXT-PLUGIN Makefile - Enterprise Plugin System
# ===============================================

.PHONY: help install test clean lint format build docs plugin-test discover hot-reload watch

# Default target
help: ## Show this help message
	@echo "🔌 FLEXT-PLUGIN - Enterprise Plugin System"
	@echo "=========================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\\033[36m%-20s\\033[0m %s\\n", $$1, $$2}'

# Installation & Setup
install: ## Install dependencies with Poetry
	@echo "📦 Installing dependencies for flext-plugin..."
	poetry install --all-extras

install-dev: ## Install with dev dependencies
	@echo "🛠️  Installing dev dependencies..."
	poetry install --all-extras --group dev --group test

# Plugin Discovery & Management
discover: ## Discover available plugins
	@echo "🔍 Discovering plugins..."
	poetry run python -c "
from flext_plugin.discovery import PluginDiscovery
discovery = PluginDiscovery()
plugins = discovery.discover_plugins()
print(f'Found {len(plugins)} plugins:')
for plugin in plugins:
    print(f'  - {plugin.name} v{plugin.version} ({plugin.type})')
"

plugin-list: ## List installed plugins
	@echo "📋 Listing installed plugins..."
	poetry run python -c "
from flext_plugin.manager import PluginManager
manager = PluginManager()
plugins = manager.list_plugins()
if plugins:
    print('Installed plugins:')
    for plugin in plugins:
        status = '✅' if plugin.is_active else '❌'
        print(f'  {status} {plugin.name} v{plugin.version}')
else:
    print('No plugins installed')
"

plugin-validate: ## Validate plugin configurations
	@echo "🔍 Validating plugin configurations..."
	poetry run python -c "
from flext_plugin.validators import PluginValidator
from flext_plugin.discovery import PluginDiscovery
discovery = PluginDiscovery()
validator = PluginValidator()
plugins = discovery.discover_plugins()
for plugin in plugins:
    try:
        validator.validate(plugin)
        print(f'✅ {plugin.name} - Valid')
    except Exception as e:
        print(f'❌ {plugin.name} - Invalid: {e}')
"

# Plugin Testing
plugin-test: ## Test plugin functionality
	@echo "🧪 Testing plugin functionality..."
	poetry run python -c "
from flext_plugin.loader import PluginLoader
loader = PluginLoader()
try:
    # Test basic plugin loading
    plugins = loader.load_plugins()
    print(f'✅ Successfully loaded {len(plugins)} plugins')
    
    # Test plugin lifecycle
    for plugin in plugins[:1]:  # Test first plugin only
        plugin.initialize()
        print(f'✅ {plugin.name} initialized')
        plugin.cleanup()
        print(f'✅ {plugin.name} cleaned up')
except Exception as e:
    print(f'❌ Plugin test failed: {e}')
"

plugin-create: ## Create example plugin
	@echo "🎨 Creating example plugin..."
	@mkdir -p examples/test_plugin
	poetry run python -c "
import os
from pathlib import Path

plugin_code = '''
from flext_plugin.base import Plugin
from flext_plugin.types import PluginMetadata

class TestPlugin(Plugin):
    \"\"\"Example test plugin.\"\"\"
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name=\"test-plugin\",
            version=\"1.0.0\",
            author=\"Test Author\",
            description=\"Example plugin for testing\"
        )
    
    async def initialize(self):
        self.logger.info(\"Test plugin initialized\")
    
    async def cleanup(self):
        self.logger.info(\"Test plugin cleaned up\")
'''

plugin_path = Path('examples/test_plugin/plugin.py')
plugin_path.parent.mkdir(parents=True, exist_ok=True)
plugin_path.write_text(plugin_code)
print(f'✅ Example plugin created at {plugin_path}')
"

# Hot Reload Development
hot-reload-test: ## Test hot reload functionality
	@echo "🔥 Testing hot reload functionality..."
	poetry run python -c "
try:
    from flext_plugin.hot_reload import HotReloadManager
    manager = HotReloadManager()
    print('✅ Hot reload manager initialized')
    
    # Test state preservation
    if hasattr(manager, 'save_state'):
        print('✅ State preservation available')
    else:
        print('⚠️  State preservation not implemented')
        
    # Test file watching
    if hasattr(manager, 'watch_files'):
        print('✅ File watching available')
    else:
        print('⚠️  File watching not implemented')
        
except ImportError:
    print('⚠️  Hot reload module not found - needs implementation')
except Exception as e:
    print(f'❌ Hot reload test failed: {e}')
"

watch: ## Watch for plugin changes (if hot reload available)
	@echo "👀 Watching for plugin changes..."
	@if [ -f src/flext_plugin/hot_reload/watcher.py ]; then \
		poetry run python -c "
from flext_plugin.hot_reload.watcher import PluginWatcher
import asyncio

async def main():
    watcher = PluginWatcher(['examples/', 'src/'])
    print('🔥 Hot reload watcher started...')
    print('  Watching: examples/, src/')
    print('  Press Ctrl+C to stop')
    await watcher.watch()

asyncio.run(main())
"; \
	else \
		echo "⚠️  Hot reload watcher not implemented yet"; \
		echo "📋 To implement: create src/flext_plugin/hot_reload/watcher.py"; \
	fi

# Development Tools
sandbox: ## Run plugin in sandboxed environment
	@echo "🏖️  Running plugin sandbox..."
	poetry run python -c "
import sys
import subprocess
from pathlib import Path

sandbox_script = '''
import sys
import os
import resource

# Set resource limits
try:
    # Limit memory to 512MB
    resource.setrlimit(resource.RLIMIT_AS, (512*1024*1024, 512*1024*1024))
    
    # Limit CPU time to 30 seconds
    resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
    
    print(\"📦 Sandbox environment configured\")
    print(\"  Memory limit: 512MB\")
    print(\"  CPU limit: 30 seconds\")
    
    # Import and run plugin
    from flext_plugin.manager import PluginManager
    manager = PluginManager()
    plugins = manager.list_plugins()
    
    if plugins:
        plugin = plugins[0]
        print(f\"🔌 Running plugin: {plugin.name}\")
        plugin.initialize()
        print(\"✅ Plugin executed successfully in sandbox\")
    else:
        print(\"⚠️  No plugins available to test\")
        
except Exception as e:
    print(f\"❌ Sandbox execution failed: {e}\")
'''

print(sandbox_script)
exec(sandbox_script)
"

# Performance Testing
benchmark: ## Benchmark plugin performance
	@echo "⚡ Benchmarking plugin performance..."
	poetry run python -c "
import time
from flext_plugin.discovery import PluginDiscovery
from flext_plugin.loader import PluginLoader

# Benchmark discovery
start = time.time()
discovery = PluginDiscovery()
plugins = discovery.discover_plugins()
discovery_time = time.time() - start
print(f'🔍 Plugin discovery: {discovery_time:.3f}s ({len(plugins)} plugins)')

# Benchmark loading
start = time.time()
loader = PluginLoader()
loaded_plugins = loader.load_plugins()
load_time = time.time() - start
print(f'📦 Plugin loading: {load_time:.3f}s ({len(loaded_plugins)} plugins)')

# Performance targets
if discovery_time < 0.1:
    print('✅ Discovery performance: EXCELLENT')
elif discovery_time < 0.5:
    print('⚠️  Discovery performance: ACCEPTABLE')
else:
    print('❌ Discovery performance: NEEDS IMPROVEMENT')

if load_time < 1.0:
    print('✅ Loading performance: EXCELLENT')
elif load_time < 3.0:
    print('⚠️  Loading performance: ACCEPTABLE')
else:
    print('❌ Loading performance: NEEDS IMPROVEMENT')
"

# Testing
test: ## Run plugin system tests
	@echo "🧪 Running plugin system tests..."
	poetry run pytest tests/ -v --tb=short

test-coverage: ## Run tests with coverage
	@echo "📊 Running tests with coverage..."
	poetry run pytest tests/ --cov=src/flext_plugin --cov-report=html:reports/coverage --cov-report=xml:reports/coverage.xml --cov-fail-under=85

test-integration: ## Run integration tests
	@echo "🔗 Running integration tests..."
	poetry run pytest tests/integration/ -v --tb=short

# Code Quality - Maximum Strictness
lint: ## Run all linters with maximum strictness
	@echo "🔍 Running maximum strictness linting for plugin system..."
	poetry run ruff check . --output-format=verbose
	@echo "✅ Ruff linting complete"

format: ## Format code with strict standards
	@echo "🎨 Formatting plugin system code..."
	poetry run black .
	poetry run ruff check --fix .
	@echo "✅ Code formatting complete"

type-check: ## Run strict type checking
	@echo "🎯 Running strict MyPy type checking..."
	poetry run mypy src/flext_plugin --strict --show-error-codes
	@echo "✅ Type checking complete"

check: lint type-check test ## Run all quality checks
	@echo "✅ All quality checks complete for flext-plugin!"

# Build & Distribution
build: ## Build the plugin system package
	@echo "🔨 Building flext-plugin package..."
	poetry build
	@echo "📦 Package built successfully"

# Documentation
docs: ## Generate plugin system documentation
	@echo "📚 Generating plugin documentation..."
	@mkdir -p docs/generated
	poetry run python -c "
import inspect
from flext_plugin.base import Plugin
from flext_plugin.types import PluginMetadata

# Generate plugin interface documentation
doc = '''# Plugin System Documentation

## Plugin Base Class

'''
doc += inspect.getdoc(Plugin) or 'No documentation available'

doc += '''

## Plugin Metadata

'''
doc += inspect.getdoc(PluginMetadata) or 'No documentation available'

with open('docs/generated/plugin_interface.md', 'w') as f:
    f.write(doc)

print('✅ Plugin documentation generated')
"

# Development Workflow
dev-setup: install-dev plugin-create ## Complete development setup
	@echo "🎯 Setting up plugin development environment..."
	poetry run pre-commit install
	mkdir -p reports logs examples plugins
	@echo "🔌 Run 'make discover' to discover plugins"
	@echo "🧪 Run 'make plugin-test' to test plugin functionality"
	@echo "🔥 Run 'make hot-reload-test' to test hot reload"
	@echo "✅ Development setup complete!"

# Cleanup
clean: ## Clean build artifacts and generated files
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf build/ dist/ *.egg-info/
	@rm -rf reports/ logs/ .coverage htmlcov/
	@rm -rf docs/generated/
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@find . -name "*.pyo" -delete 2>/dev/null || true

# Environment variables
export PYTHONPATH := $(PWD)/src:$(PYTHONPATH)
export FLEXT_PLUGIN_DEV := true
export FLEXT_PLUGIN_DEBUG := true
export PLUGIN_DIRECTORY := $(PWD)/examples