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

- **`types.py`**: Core plugin types, enums (`PluginStatus`, `PluginType`), result objects, and error classes
- **`discovery.py`**: Plugin discovery logic

### Domain Layer (`src/flext_plugin/domain/`)

- **`entities.py`**: Core business entities (`FlextPlugin`, `FlextPluginConfig`, `FlextPluginMetadata`, `FlextPluginRegistry`)
- **`ports.py`**: Domain interfaces/contracts

### Application Layer (`src/flext_plugin/application/`)

- **`services.py`**: Application services (`FlextPluginService`, `FlextPluginDiscoveryService`)
- **`handlers.py`**: Command/query handlers (`FlextPluginHandler`, `FlextPluginRegistrationHandler`)

### Root Level APIs

- **`platform.py`**: Main platform class (`FlextPluginPlatform`) providing unified API access
- **`simple_api.py`**: Simplified factory functions for plugin creation
- **`hot_reload.py`**: Hot-reload functionality
- **`loader.py`**: Plugin loading mechanisms
- **`discovery.py`**: High-level plugin discovery
- **`simple_plugin.py`**: Simple plugin interface

## Development Commands

All commands use Poetry for dependency management and follow zero-tolerance quality gates.

### Essential Quality Checks

```bash
make validate          # Complete validation (lint + type + security + test) - MUST PASS
make check             # Essential checks (lint + type + test)
make lint              # Ruff linting with comprehensive rules
make type-check        # MyPy strict mode (zero errors tolerated)
make security          # Security scans (bandit + pip-audit)
make fix               # Auto-fix linting and formatting issues
```

### Testing (Current: 33% coverage, systematic improvement ongoing)

```bash
make test              # Full test suite with coverage validation
make test-unit         # Unit tests only (excludes integration tests)
make test-integration  # Integration tests only
make test-plugin       # Plugin-specific tests
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
# Plugin operations (⚠️  CLI IMPLEMENTATION REQUIRED - THESE COMMANDS WILL FAIL)
# make plugin-create NAME=my-plugin TYPE=extractor    # TODO: Requires flext-plugin CLI
# make plugin-install NAME=tap-github                 # TODO: Requires flext-plugin CLI
# make plugin-list                                    # TODO: Requires flext-plugin CLI
# make plugin-watch                                   # TODO: Requires flext-plugin CLI
# make plugin-validate                                # Works - uses FlextPluginPlatform
# make plugin-reload                                  # BROKEN: hot_reload_all function missing

# Currently working plugin validation:
make plugin-validate                                 # Validate plugin system
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

The project currently has 33% test coverage (83/253 tests passing) with comprehensive test categories:

```bash
# Run specific test categories with pytest markers
pytest -m unit              # Isolated unit tests
pytest -m integration       # Cross-layer integration tests
pytest -m plugin            # Plugin system tests
pytest -m hot_reload        # Hot-reload functionality tests
pytest -k "test_name"       # Run specific test by name pattern
```

**Test Structure:**

- `tests/unit/`: Isolated unit tests for each layer
- `tests/integration/`: Cross-layer integration tests
- `tests/e2e/`: End-to-end plugin lifecycle tests
- `tests/fixtures/`: Shared test data and fixtures
- `tests/conftest.py`: Pytest configuration and shared fixtures

**Actual Test Files:**

- `test_core_types.py`: Core plugin types and enums
- `test_domain_entities.py`: Domain entities (FlextPlugin, etc.)
- `test_domain_ports.py`: Domain interfaces
- `test_application_handlers.py`: Application layer handlers
- `test_discovery.py`, `test_discovery_simple.py`: Plugin discovery
- `test_hot_reload_package.py`: Hot-reload functionality
- `test_manager.py`, `test_manager_comprehensive.py`: Plugin management
- `test_plugin_basic.py`: Basic plugin functionality
- `test_imports.py`: Import validation

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

### Working with Plugin Entities

```python
# Creating a FlextPlugin entity
from flext_plugin import FlextPlugin, create_flext_plugin
from flext_plugin.core.types import PluginStatus, PluginType

# Using entity directly
plugin = FlextPlugin(
    name="my-plugin",
    version="1.0.0",
    config={
        "description": "My custom plugin",
        "author": "Developer",
        "status": PluginStatus.INACTIVE
    }
)

# Using factory function
plugin = create_flext_plugin(
    name="my-plugin",
    version="1.0.0",
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

### Quality Gate Workflow

1. Make code changes following Clean Architecture patterns
2. Run `make fix` to auto-format and fix linting issues
3. Run `make validate` - ALL checks must pass (lint + type + security + test)
4. Add comprehensive tests for new functionality following established patterns
5. Commit only after validation succeeds

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

## Critical Implementation Gaps

### 🚨 GAP 1: CLI Implementation Missing

**Status**: HIGH PRIORITY - CLI entry point defined but not implemented
**Issue**:

- `pyproject.toml` defines `flext-plugin = "flext_plugin.cli:main"`
- No `cli.py` file exists in the codebase
- Makefile plugin commands reference non-existent CLI

**Required Actions**:

- [ ] Create `src/flext_plugin/cli.py` with main() entry point
- [ ] Implement plugin management commands (create, install, list, watch, validate)
- [ ] Add CLI argument parsing and help documentation
- [ ] Update Makefile commands to work with actual CLI implementation

### 🚨 GAP 2: Hot Reload Implementation Incomplete

**Status**: MEDIUM PRIORITY - Framework exists but needs completion
**Issue**:

- `hot_reload.py` exists at root level but integration unclear
- Test files reference hot reload functionality
- Makefile has hot reload configuration but no working implementation

**Required Actions**:

- [ ] Complete hot reload integration with plugin platform
- [ ] Implement file watching with watchdog library integration
- [ ] Add hot reload testing and validation
- [ ] Document hot reload usage patterns and limitations

### 🚨 GAP 3: Meltano/Singer Integration Superficial

**Status**: MEDIUM PRIORITY - Types defined but integration missing
**Issue**:

- `PluginType` enum defines TAP, TARGET, TRANSFORM for Singer/Meltano
- No actual Singer SDK or Meltano integration code
- Missing plugin discovery for Singer ecosystem

**Required Actions**:

- [ ] Implement Singer tap/target plugin interfaces
- [ ] Add Meltano project configuration integration
- [ ] Create Singer plugin discovery mechanisms
- [ ] Add comprehensive examples for Singer plugin development

### 🚨 GAP 4: Documentation and Examples

**Status**: LOW PRIORITY - Foundation exists but needs practical examples  
**Issue**:

- Strong architectural foundation but missing practical examples
- `examples/real_plugins/` directory exists but may be empty
- Integration patterns need concrete implementation examples

**Required Actions**:

- [ ] Create practical plugin examples in `examples/` directory
- [ ] Add end-to-end integration examples
- [ ] Document common plugin development workflows
- [ ] Add troubleshooting guide for common issues

## Next Steps for Development

1. **Immediate**: Implement CLI functionality to enable plugin management commands
2. **Short-term**: Complete hot reload system integration and testing
3. **Medium-term**: Add Singer/Meltano plugin support for data pipeline integration
4. **Long-term**: Expand examples and documentation for broader ecosystem adoption
