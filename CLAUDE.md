# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `flext-plugin`, an enterprise-grade plugin management system for the FLEXT data platform. It implements dynamic plugin loading, lifecycle management, and hot-reload capabilities using Clean Architecture and Domain-Driven Design patterns.

**Key Features:**

- Dynamic plugin discovery and loading
- Plugin lifecycle management (activate, deactivate, enable, disable)
- Clean Architecture with strict layer separation
- Domain-driven design with plugin entities and value objects
- Type-safe implementation with Python 3.13
- Enterprise-grade quality gates and testing

## Architecture

The project follows Clean Architecture with these layers:

### Core Layer (`src/flext_plugin/core/`)
- **`types.py`**: Core plugin types re-exports from centralized type modules
- **`discovery.py`**: Plugin discovery logic and protocols

### Domain Layer (`src/flext_plugin/domain/`)
- **`entities.py`**: Core business entities (`FlextPlugin`, `FlextPluginConfig`, `FlextPluginMetadata`, `FlextPluginRegistry`)
- **`ports.py`**: Domain interfaces/contracts and abstract protocols

### Application Layer (`src/flext_plugin/application/`)
- **`services.py`**: Application services (`FlextPluginService`, `FlextPluginDiscoveryService`)
- **`handlers.py`**: Command/query handlers (`FlextPluginHandler`, `FlextPluginRegistrationHandler`)

### Infrastructure Layer (Root Level)
- **`platform.py`**: Main platform class (`FlextPluginPlatform`) providing unified API access
- **`simple_api.py`**: Simplified factory functions for plugin creation
- **`hot_reload.py`**: Hot-reload functionality with state management
- **`loader.py`**: Plugin loading mechanisms and adapters  
- **`discovery.py`**: High-level plugin discovery (facade over core)
- **`simple_plugin.py`**: Simple plugin interface and registry
- **`models.py`**: Pydantic models for type definitions (`PluginStatus`, `PluginType`)
- **`real_adapters.py`**: Real implementation adapters for testing
- **`cli.py`**: Command-line interface using Click framework

## Development Commands

All commands use Poetry for dependency management and follow zero-tolerance quality gates.

### Essential Quality Checks (Zero Tolerance)

```bash
make validate          # Complete validation (lint + type + security + test) - MUST PASS
make check             # Quick health check (lint + type)
make lint              # Ruff linting with comprehensive rules
make type-check        # MyPy strict mode (zero errors tolerated)
make security          # Security scans (bandit + pip-audit) 
make fix               # Auto-fix linting and formatting issues
make format            # Format code with ruff
```

### Testing (85% coverage target, comprehensive test categories)

```bash
make test              # Full test suite with 85% coverage requirement
make test-unit         # Unit tests only (excludes integration tests)
make test-integration  # Integration tests only
make test-plugin       # Plugin-specific tests  
make test-hot-reload   # Hot reload functionality tests
make test-discovery    # Plugin discovery tests
make test-e2e          # End-to-end tests
make test-fast         # Run tests without coverage for quick feedback
make coverage-html     # Generate HTML coverage report
```

### Development Setup

```bash
make setup             # Complete development setup with pre-commit hooks
make install           # Install dependencies only
make install-dev       # Install with dev dependencies
make pre-commit        # Run pre-commit hooks on all files
```

### Plugin Management Commands

```bash
# Direct CLI usage (preferred method)
flext-plugin create --name my-plugin --type tap     # Create new plugin
flext-plugin install plugin-name                    # Install plugin from registry
flext-plugin list --format json                     # List plugins with JSON output
flext-plugin validate --all                         # Validate all plugins
flext-plugin watch --directory ./plugins            # Monitor with hot reload
flext-plugin platform --status                      # Check platform status

# Makefile shortcuts (delegate to CLI)
make plugin-validate                                 # Validate plugin system
make plugin-test                                     # Test plugin platform
make plugin-discovery                               # Test discovery service
make plugin-operations                              # Run all validations
```

### Build & Cleanup

```bash
make build             # Build distribution packages
make build-clean       # Clean then build
make clean             # Remove build artifacts and caches
make clean-all         # Deep clean including virtual environment
make format            # Format code with ruff
```

### Documentation & Dependencies

```bash
make docs              # Build documentation with mkdocs
make docs-serve        # Serve documentation locally
make deps-update       # Update all dependencies
make deps-show         # Show dependency tree
make deps-audit        # Audit dependencies for security issues
```

### Diagnostics & Maintenance

```bash
make diagnose          # Show project diagnostics (Python, Poetry, versions)
make doctor            # Complete health check (diagnose + check)
make shell             # Open Python shell with project environment
make reset             # Reset project (clean-all + setup)
```

### Quick Aliases

```bash
make t                 # Alias for test
make l                 # Alias for lint
make f                 # Alias for format
make tc                # Alias for type-check
make c                 # Alias for clean
make i                 # Alias for install
make v                 # Alias for validate
```

## Key Domain Concepts

### Plugin Types

The system supports multiple plugin types defined in `PluginType` enum:

- **Singer ETL**: `TAP`, `TARGET`, `TRANSFORM` (for Meltano integration)
- **Architecture**: `EXTENSION`, `SERVICE`, `MIDDLEWARE`, `TRANSFORMER`
- **Integration**: `API`, `DATABASE`, `NOTIFICATION`, `AUTHENTICATION`
- **Utility**: `UTILITY`, `TOOL`, `HANDLER`, `PROCESSOR`

### Plugin Status Lifecycle

Plugins progress through states defined in `PluginStatus`:

- `DISCOVERED` → `LOADED` → `ACTIVE`/`INACTIVE`
- Error states: `ERROR`, `DISABLED`
- Health states: `HEALTHY`, `UNHEALTHY`

### Core Entities

- **`FlextPlugin`**: Main plugin entity with lifecycle management
- **`FlextPluginConfig`**: Plugin configuration with update tracking
- **`FlextPluginMetadata`**: Additional plugin information (tags, URLs, license)
- **`FlextPluginRegistry`**: Collection of registered plugins

## Dependencies

**Core Dependencies:**

- `flext-core`: Foundation patterns, `FlextResult`, DI container
- `flext-observability`: Monitoring and health checks
- Standard libraries: `pydantic`, `watchdog`, `psutil`, `aiofiles`

**Development Dependencies:**

- Testing: `pytest` with full plugin suite, `factory-boy`, `hypothesis`
- Quality: `ruff` (ALL rules), `mypy` (strict mode), `bandit`, `pip-audit`
- Tools: `black`, `isort`, `pre-commit`

## Testing Strategy

The project uses a comprehensive testing approach with real implementations (no mocks) targeting 85% coverage:

```bash
# Run specific test categories with pytest markers
pytest -m unit              # Isolated unit tests
pytest -m integration       # Cross-layer integration tests
pytest -m plugin            # Plugin system tests
pytest -m hot_reload        # Hot-reload functionality tests
pytest -m discovery         # Plugin discovery tests
pytest -k "test_name"       # Run specific test by name pattern

# Run specific test files for development
pytest tests/test_core_types.py -v                    # Core type system tests
pytest tests/test_domain_entities.py -v               # Entity behavior tests
pytest tests/test_application_handlers.py -v          # Handler integration tests
pytest tests/test_discovery.py -v                     # Discovery functionality
pytest tests/test_hot_reload_coverage.py -v           # Hot reload implementation tests
pytest tests/test_manager_comprehensive.py -v         # Manager integration tests

# Run single test methods for focused development
pytest tests/test_domain_entities.py::TestFlextPlugin::test_create -v
pytest tests/test_hot_reload_coverage.py::TestHotReloadManager::test_manager_initialization -v
pytest "tests/test_application_handlers.py::test_handler_creation" -v

# Coverage for specific modules during development
pytest --cov=flext_plugin.domain tests/test_domain_entities.py -v
pytest --cov=flext_plugin.application tests/test_application_handlers.py -v
```

**Test Structure:**

- `tests/unit/`: Isolated unit tests for each layer (actual directory)
- `tests/integration/`: Cross-layer integration tests (actual directory)
- `tests/e2e/`: End-to-end plugin lifecycle tests (actual directory) 
- `tests/fixtures/`: Shared test data and fixtures (actual directory)
- `tests/conftest.py`: Real fixtures without mocks - creates actual plugin files

**Key Test Files (Real Implementation Focus):**

- `test_core_types.py`: Core plugin types and enums
- `test_domain_entities.py`: Domain entities (FlextPlugin, etc.)
- `test_domain_ports.py`: Domain interfaces and protocols
- `test_application_handlers.py`: Application layer handlers  
- `test_discovery*.py`: Plugin discovery with real file operations
- `test_hot_reload*.py`: Hot-reload with real file watching
- `test_manager*.py`: Plugin management with real adapters
- `test_plugin_basic.py`: Basic plugin functionality
- `test_imports.py`: Import validation and module loading

**Testing Philosophy:**
- **Real Over Mocks**: Uses `real_adapters.py` and actual plugin files (see `conftest.py`)
- **Functional Testing**: Tests actual plugin discovery, loading, and execution
- **Coverage Strategy**: Targets 85% with focus on business logic validation

## Configuration

The plugin system uses environment variables and Makefile configuration:

```bash
# Makefile configuration (in Makefile)
MIN_COVERAGE=85                    # Minimum test coverage required
FLEXT_PLUGIN_HOT_RELOAD=true      # Enable hot reload
FLEXT_PLUGIN_WATCH_INTERVAL=2     # File watch interval in seconds

# Runtime environment variables (when implemented)
FLEXT_PLUGIN_DISCOVERY_PATHS=plugins:~/.flext/plugins:/opt/flext/plugins
FLEXT_PLUGIN_CACHE_DIR=.plugin_cache
FLEXT_PLUGIN_MAX_WORKERS=10
```

## Common Development Patterns

### Key Implementation Patterns

**Clean Architecture Implementation:**
- **Core Layer**: Pure domain types and business logic (PluginType, PluginStatus enums)
- **Domain Layer**: Business entities (FlextPlugin, FlextPluginConfig) with behavior
- **Application Layer**: Services and handlers coordinating business logic
- **Platform Layer**: Unified facade (FlextPluginPlatform) for external integration

**Result Pattern Usage:**
All operations return `FlextResult[T]` for consistent error handling:
```python
from flext_core import FlextResult

def create_plugin(...) -> FlextResult[FlextPlugin]:
    try:
        # Implementation
        return FlextResult[None].ok(plugin)
    except Exception as e:
        return FlextResult[None].fail(f"Creation failed: {e}")
```

**Dependency Injection Pattern:**
The platform uses FlextContainer for dependency management:
```python
from flext_core import FlextContainer
from flext_plugin import FlextPluginPlatform

container = FlextContainer()
platform = FlextPluginPlatform(container)
```

### Working with Plugin Entities

```python
# Creating a FlextPlugin entity
from flext_plugin import FlextPlugin, create_flext_plugin
from flext_plugin.core.types import PluginStatus, PluginType

# Using entity directly
plugin = FlextPlugin(
    name="my-plugin",
    version="0.9.0",
    config={
        "description": "My custom plugin",
        "author": "Developer",
        "status": PluginStatus.INACTIVE
    }
)

# Using factory function
plugin = create_flext_plugin(
    name="my-plugin",
    version="0.9.0",
    plugin_type=PluginType.EXTRACTOR
)
```

### Using the Plugin Platform

```python
from flext_plugin import FlextPluginPlatform, FlextContainer

# Create platform with dependency injection
container = FlextContainer()
platform = FlextPluginPlatform(container)

# Or use the factory function
from flext_plugin import create_flext_plugin_platform
platform = create_flext_plugin_platform(config={"debug": True})
```

### Working with Plugin Discovery

```python
from flext_plugin.application.services import FlextPluginDiscoveryService
from flext_plugin.core.discovery import PluginDiscovery

# Use discovery service
discovery = FlextPluginDiscoveryService()
plugins = await discovery.discover_plugins(path="./plugins")

# Direct discovery usage
direct_discovery = PluginDiscovery()
found_plugins = direct_discovery.discover_in_directory("./plugins")
```

## Key Architectural Patterns (Critical for Understanding)

### FlextResult Pattern (Consistent Error Handling)
All operations return `FlextResult[T]` for railway-oriented programming:
```python
from flext_core import FlextResult

def discover_plugins(path: str) -> FlextResult[list[FlextPlugin]]:
    try:
        plugins = self._scan_directory(path)
        return FlextResult[list[FlextPlugin]].ok(plugins)
    except Exception as e:
        return FlextResult[list[FlextPlugin]].fail(f"Discovery failed: {e}")
```

### Clean Architecture Layers (Strict Separation)
- **Core**: Types and discovery protocols (no dependencies)
- **Domain**: Business entities and ports (depends only on core)
- **Application**: Services and handlers (depends on domain + core)
- **Infrastructure**: Platform, CLI, adapters (depends on all layers)

### Domain Entity Pattern (Business Logic Encapsulation)
```python
# Domain entities encapsulate business rules and validation
from flext_plugin.domain.entities import FlextPlugin

plugin = FlextPlugin.create(
    name="my-plugin",
    version="1.0.0", 
    plugin_type=PluginType.TAP
)
# Entity validates name format, version constraints, type compatibility
```

### Real Adapter Pattern (No Mocks in Tests)
```python
# Tests use real implementations, not mocks
from flext_plugin.real_adapters import RealPluginDiscoveryAdapter

adapter = RealPluginDiscoveryAdapter(plugin_directory)
result = adapter.discover_plugins()  # Actually scans filesystem
```

### Quality Gate Workflow

1. Make code changes following Clean Architecture patterns
2. Run `make fix` to auto-format and fix linting issues  
3. Run `make validate` - ALL checks must pass (lint + type + security + test)
4. Add comprehensive tests using real adapters (no mocks)
5. Verify single test execution: `pytest tests/test_module.py::TestClass::test_method -v`
6. Commit only after validation succeeds

### Testing New Features

1. Add unit tests in `tests/unit/` following existing patterns
2. Add integration tests in `tests/integration/` for cross-layer functionality
3. Use pytest markers: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.plugin`
4. Run specific tests: `pytest tests/test_your_feature.py -v`
5. Verify coverage: `make coverage-html` and check report

## Integration with FLEXT Ecosystem

This plugin system integrates with the larger FLEXT platform:

- **FlexCore**: Runtime container service (Go) on port 8080
- **FLEXT Service**: Data platform service (Go/Python) on port 8081
- **Singer Integration**: Supports tap/target/transform plugins for Meltano
- **Clean Architecture**: Follows platform-wide architectural patterns

The plugin system is designed to be platform-agnostic while providing deep integration with FLEXT's data processing pipeline.

## Implementation Status

### ✅ IMPLEMENTED: CLI System
**Status**: COMPLETE - Full CLI implementation with Click framework
- ✅ Complete CLI at `src/flext_plugin/cli.py` with all major commands  
- ✅ Commands: create, install, uninstall, list, validate, watch, platform
- ✅ FlextResult integration for consistent error handling
- ✅ JSON and text output formats
- ✅ Entry point configured in pyproject.toml

### ✅ IMPLEMENTED: Hot Reload System
**Status**: COMPLETE - Full hot reload implementation with real testing
- ✅ Complete implementation in `hot_reload.py` with state management
- ✅ Watchdog integration for file monitoring
- ✅ Comprehensive test coverage in `test_hot_reload_*.py` files
- ✅ Real adapter implementations for testing without mocks
- ✅ Plugin state management, rollback, and event handling

### ✅ IMPLEMENTED: Core Architecture  
**Status**: COMPLETE - Clean Architecture with comprehensive domain layer
- ✅ Domain entities with full lifecycle management
- ✅ Application services and handlers
- ✅ Platform facade with dependency injection
- ✅ Real adapter implementations for infrastructure layer

### 🔄 IN PROGRESS: Test Coverage
**Status**: ACTIVE - Systematic improvement from current state to 85% target
- ✅ Comprehensive test structure (unit/integration/e2e)
- ✅ Real testing approach without mocks (see `conftest.py`)
- ✅ Plugin-specific test markers and categories
- 🔄 Coverage improvement: targeting 85% (current state varies by module)

### 🚨 GAPS: Singer/Meltano Integration  
**Status**: TYPES ONLY - Deep integration missing
**Current State**:
- ✅ `PluginType` enum defines TAP, TARGET, TRANSFORM
- ❌ No Singer SDK integration or Meltano project support
- ❌ Missing Singer-specific plugin discovery and execution

**Required for Production**:
- [ ] Singer tap/target plugin interfaces and execution
- [ ] Meltano project configuration integration  
- [ ] Singer ecosystem plugin discovery and validation
- [ ] Examples for Singer plugin development workflows

## Development Priorities

1. **Immediate**: Achieve 85% test coverage across all modules
2. **Short-term**: Implement Singer/Meltano integration for data pipeline support
3. **Medium-term**: Platform method implementations (install, uninstall from registry)
4. **Long-term**: Production examples and comprehensive documentation

## Troubleshooting Common Issues

### CLI Issues

```bash
# CLI not found after installation
pip install -e .  # Reinstall in development mode
poetry install     # Or reinstall with poetry

# Permission issues with plugin creation
chmod +x $(which flext-plugin)  # Make CLI executable

# Platform initialization failures
python -c "from flext_plugin import FlextPluginPlatform; FlextPluginPlatform()"  # Test platform
```

### Test Issues

```bash
# MyPy type errors during development
poetry run mypy src --show-error-codes  # See specific error codes
poetry run mypy src --strict             # Run in strict mode

# Test failures due to missing dependencies
poetry install --with dev,test          # Install all test dependencies
poetry run pytest tests/ -v             # Run with verbose output

# Coverage issues
pytest --cov=flext_plugin --cov-report=html  # Generate detailed coverage report
```

### Plugin Development Issues

```bash
# Plugin discovery not working
export FLEXT_PLUGIN_DISCOVERY_PATHS="./plugins:~/.flext/plugins"  # Set paths
flext-plugin validate --all                                        # Validate system

# Hot reload not responding
flext-plugin watch --directory ./plugins --interval 1  # Reduce interval
ps aux | grep flext-plugin                              # Check running processes
```
