# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

**FLEXT-Plugin** is the enterprise-grade plugin management system and extensibility foundation for the entire FLEXT ecosystem. It provides comprehensive plugin lifecycle management with hot-reload capabilities, security validation, and Clean Architecture patterns.

**Version**: 0.9.0 | **Python**: 3.13+ Exclusive | **Coverage Target**: 90% | **Lines of Code**: 9,767 | **Test Files**: 24
**Status**: Production-ready plugin system with Clean Architecture, FLEXT-core integration, and comprehensive API

---

## Essential Commands

```bash
# Setup
make setup                    # Install deps + pre-commit hooks

# Quality gates (MANDATORY before commit)
make validate                 # Full validation: lint + type + security + test
make check                    # Quick check: lint + type only

# Individual checks
make lint                     # Ruff linting (ZERO violations)
make type-check              # Pyrefly type checking (ZERO errors)
make test                    # Full test suite (90% coverage minimum)
make format                  # Auto-format code with Ruff

# Plugin-specific operations
make plugin-test             # Test plugin system functionality
make plugin-validate         # Validate plugin system integrity
make plugin-discovery        # Test plugin discovery mechanisms
make plugin-operations       # Run all plugin validations

# Testing
PYTHONPATH=src poetry run pytest tests/unit/test_api.py -v
pytest -m unit              # Unit tests only
pytest -m integration       # Integration tests
pytest --cov=flext_plugin --cov-report=html
```

---

## Architecture Overview

### Core Classes and API

```python
from flext_plugin import (
    FlextPluginApi,           # Unified plugin API facade
    FlextPluginPlatform,      # Main plugin platform
    FlextPluginConfig,        # Plugin configuration
    FlextPluginEntities,      # Domain entities
    FlextPluginHandlers,      # Event handlers
    FlextPluginHotReload,     # Hot reload system
    FlextPluginLoader,        # Plugin loading
    FlextPluginService,       # Application services
    FlextPluginTypes,         # Type definitions
    FlextPluginProtocols,     # Structural typing
    FlextPluginModels,        # Pydantic models
    FlextPluginConstants,     # System constants
    FlextPluginExceptions,    # Exception hierarchy
)
```

### Module Organization

```
src/flext_plugin/
├── api.py                   # FlextPluginApi - Unified facade (588 lines)
├── platform.py              # FlextPluginPlatform - Main platform (259+ lines)
├── config.py                # FlextPluginConfig - Configuration management
├── entities.py              # FlextPluginEntities - Domain entities
├── handlers.py              # FlextPluginHandlers - Event handling
├── hot_reload.py            # FlextPluginHotReload - File monitoring
├── loader.py                # FlextPluginLoader - Plugin loading
├── services.py              # FlextPluginService - Application services
├── discovery.py             # FlextPluginDiscovery - Plugin discovery
├── models.py                # FlextPluginModels - Pydantic models
├── constants.py             # FlextPluginConstants - System constants
├── types.py                 # FlextPluginTypes - Type aliases
├── protocols.py             # FlextPluginProtocols - Protocol definitions
├── exceptions.py            # FlextPluginExceptions - Error hierarchy
├── adapters.py              # FlextPluginAdapters - Infrastructure adapters
├── ports.py                 # Plugin ports/interfaces
├── implementations.py       # Concrete implementations
├── utilities.py             # Helper utilities
└── __init__.py              # Public API exports (19 classes)

Total: 20 modules, 9,767 lines of production code
```

### Design Patterns

**Railway-Oriented Programming:**
All operations return `FlextResult[T]` for composable error handling:

```python
from flext_plugin import FlextPluginPlatform
from flext_core import FlextResult

platform = FlextPluginPlatform()

# All operations return FlextResult
result = platform.discover_plugins(["./plugins"])
if result.is_success:
    plugins = result.unwrap()
else:
    print(f"Discovery failed: {result.error}")
```

**Clean Architecture Layers:**
```
Interface/API Layer    → FlextPluginApi (facade pattern)
Application Layer     → FlextPluginServices (use cases)
Domain Layer          → FlextPluginEntities (business logic)
Infrastructure Layer  → FlextPluginAdapters (external systems)
```

**Domain-Driven Design:**
```python
from flext_plugin import FlextPluginEntities

# Plugin entity with business rules
plugin = FlextPluginEntities.Plugin.create(
    name="my-plugin",
    plugin_version="1.0.0",
    config={"type": "extension"}
)

# Business rule validation
validation_result = plugin.validate_business_rules()
```

---

## Critical Patterns

### MANDATORY: FlextResult[T] Railway Pattern

ALL operations that can fail MUST return `FlextResult[T]`:

```python
from flext_core import FlextResult
from flext_plugin import FlextPluginPlatform

async def execute_plugin_safely(
    platform: FlextPluginPlatform,
    plugin_name: str,
    context: dict[str, object]
) -> FlextResult[object]:
    """All plugin operations use FlextResult for error handling."""

    # Chain operations with railway pattern
    return (
        platform.discover_plugins(["./plugins"])
        .flat_map(lambda plugins: platform.load_plugin(plugin_name))
        .flat_map(lambda plugin: platform.execute_plugin(plugin_name, context))
        .map(lambda execution: execution.result)
    )
```

### MANDATORY: Clean Architecture Separation

```python
# ✅ CORRECT - Domain layer has no infrastructure dependencies
from flext_plugin.entities import FlextPluginEntities

class PluginBusinessLogic:
    """Domain service with pure business logic only."""

    def validate_plugin_rules(self, plugin: FlextPluginEntities.Plugin) -> FlextResult[bool]:
        # Business rules only - no file I/O, no external APIs
        if not plugin.name:
            return FlextResult.fail("Plugin name required")
        return FlextResult.ok(True)

# ❌ FORBIDDEN - Infrastructure leakage into domain
import os  # Infrastructure concern

class PluginBusinessLogic:
    def validate_plugin_file(self, path: str) -> bool:
        return os.path.exists(path)  # Infrastructure in domain layer!
```

### MANDATORY: Single Class Per Module Pattern

Following flext-core ecosystem standard:

```python
# ✅ CORRECT - Each module exports exactly ONE main class
class FlextPluginPlatform:
    """Main plugin platform - single class per module."""
    pass

# ❌ FORBIDDEN - Multiple classes in one module
class FlextPluginPlatform: pass
class PluginHelper: pass  # Second class - VIOLATION
```

### MANDATORY: Root Module Imports

```python
# ✅ CORRECT - Root-level imports (ecosystem standard)
from flext_plugin import FlextPluginPlatform, FlextPluginConfig

# ❌ FORBIDDEN - Internal module imports (breaks ecosystem)
from flext_plugin.platform import FlextPluginPlatform
from flext_plugin.config import FlextPluginConfig
```

---

## Quality Standards

### Type Safety (ZERO TOLERANCE)

- **Pyrefly strict mode** required for all `src/` code
- **100% type annotations** - no `Any` types allowed
- All return types must be explicit
- All function parameters must be typed

```python
from flext_core import FlextResult
from flext_plugin import FlextPluginEntities

def create_plugin(
    name: str,
    version: str,
    config: dict[str, object]
) -> FlextResult[FlextPluginEntities.Plugin]:
    """Complete type safety required."""
    return FlextPluginEntities.Plugin.create(name=name, plugin_version=version, config=config)
```

### Testing Standards

- **Coverage Target**: 90% minimum with real plugin operations
- **Test Structure**: Unit, integration, e2e tests
- **Test Fixtures**: Comprehensive fixtures in conftest.py
- **Real Testing**: Functional tests, not just mocks

### Code Quality

- **Ruff linting**: ZERO violations in production code
- **Line length**: 88 characters (Ruff default)
- **Import organization**: Ruff handles automatically
- **Security**: Bandit scanning with zero critical issues

---

## Development Workflow

### Using Serena MCP for Code Navigation

```python
# Activate project
mcp__serena__activate_project project="flext-plugin"

# Explore structure
mcp__serena__list_dir relative_path="src/flext_plugin"

# Get symbol overview (ALWAYS do this before reading full file)
mcp__serena__get_symbols_overview relative_path="src/flext_plugin/platform.py"

# Find specific symbols
mcp__serena__find_symbol name_path="FlextPluginPlatform" relative_path="src/flext_plugin"

# Find references (critical before API changes)
mcp__serena__find_referencing_symbols name_path="FlextPluginPlatform" relative_path="src/flext_plugin/platform.py"

# Intelligent editing (symbol-based)
mcp__serena__replace_symbol_body name_path="FlextPluginPlatform/execute_plugin" relative_path="src/flext_plugin/platform.py" body="..."
```

### Development Cycle

```bash
# 1. Explore with Serena (BEFORE reading full files)
mcp__serena__get_symbols_overview relative_path="src/flext_plugin/api.py"

# 2. Make changes using symbol-based tools
# ... edit code ...

# 3. Quick validation during development
make check              # lint + type-check only
make test-fast          # tests without coverage

# 4. Before commit (MANDATORY)
make validate           # Complete pipeline: lint + type + security + test
```

### Running Specific Tests

```bash
# By module
PYTHONPATH=src poetry run pytest tests/unit/test_api.py -v

# By test name
PYTHONPATH=src poetry run pytest tests/unit/test_config.py::TestFlextPluginConfig -v

# By marker
pytest -m unit              # Unit tests only
pytest -m integration       # Integration tests
pytest -m e2e              # End-to-end tests

# With coverage for specific module
PYTHONPATH=src poetry run pytest --cov=flext_plugin.api --cov-report=term-missing
```

---

## Plugin System Architecture

### Core Components

**FlextPluginApi** - Unified facade providing single entry point:
```python
from flext_plugin import FlextPluginApi

api = FlextPluginApi()

# Complete plugin lifecycle through single API
plugins = api.discover_plugins(["./plugins"])
plugin = api.load_plugin("my-plugin")
result = api.execute_plugin("my-plugin", {"data": "input"})
```

**FlextPluginPlatform** - Main platform with protocol-based architecture:
```python
from flext_plugin import FlextPluginPlatform

platform = FlextPluginPlatform()

# Protocol-driven implementation
# - PluginDiscovery protocol for finding plugins
# - PluginLoader protocol for loading
# - PluginExecution protocol for running
# - PluginSecurity protocol for validation
```

### Protocol Architecture

The platform uses structural typing protocols for maximum flexibility:

```python
from flext_plugin import FlextPluginProtocols

# Protocols define interfaces without inheritance
class PluginDiscovery:
    def discover_plugins(self, paths: list[str]) -> FlextResult[list[dict]]: ...

class PluginLoader:
    def load_plugin(self, path: str) -> FlextResult[dict]: ...

# Any class implementing these methods works with the platform
```

### Hot Reload System

Real-time plugin monitoring with watchdog integration:

```python
from flext_plugin import FlextPluginHotReload

hot_reload = FlextPluginHotReload()

# Monitor plugin directories
await hot_reload.start_watching(["./plugins", "/opt/flext/plugins"])

# Automatic reload on file changes
hot_reload.add_reload_callback(lambda name: print(f"Reloaded: {name}"))
```

---

## Testing Strategy

### Test Structure

```
tests/
├── unit/                    # Unit tests for individual components
│   ├── test_api.py         # FlextPluginApi tests
│   ├── test_config.py      # FlextPluginConfig tests
│   ├── test_entities.py    # FlextPluginEntities tests
│   └── ...
├── integration/            # Cross-layer integration tests
├── e2e/                    # End-to-end plugin workflows
├── test_*.py              # Various component tests
└── conftest.py            # Shared fixtures
```

### Test Fixtures

Available fixtures (20+ comprehensive fixtures):

```python
# Service fixtures (all modules have fixtures)
flext_plugin_api          # FlextPluginApi instance
flext_plugin_platform     # FlextPluginPlatform instance
flext_plugin_config       # FlextPluginConfig instance
flext_plugin_entities     # FlextPluginEntities instance

# Data fixtures
sample_plugin_config      # Sample plugin configuration
sample_plugin_data        # Sample plugin data
sample_execution_context  # Sample execution context

# Utility fixtures
temp_plugin_dir          # Temporary plugin directory
mock_plugin_file         # Mock plugin file
test_container           # FlextContainer for testing
```

### Writing Tests

```python
import pytest
from flext_plugin import FlextPluginApi

def test_plugin_discovery(flext_plugin_api: FlextPluginApi, temp_plugin_dir):
    """Test plugin discovery with real directory."""
    # Arrange
    create_test_plugin(temp_plugin_dir, "test_plugin.py")

    # Act
    result = flext_plugin_api.discover_plugins([str(temp_plugin_dir)])

    # Assert
    assert result.is_success
    assert len(result.unwrap()) == 1

@pytest.mark.integration
async def test_plugin_execution_workflow(flext_plugin_platform: FlextPluginPlatform):
    """Integration test for complete plugin execution."""
    # Test full workflow from discovery to execution
    pass
```

---

## Dependencies

### Core Dependencies

- **flext-core** - Foundation library (FlextResult, FlextContainer, FlextModels)
- **flext-observability** - Monitoring and tracing integration
- **watchdog** - File system monitoring for hot reload
- **pydantic** - Data validation and models
- **psutil** - System resource monitoring

### Dev Dependencies

- **ruff** - Linting and formatting
- **pyrefly** - Type checking
- **pytest** - Testing framework
- **bandit** - Security scanning

---

## Common Issues and Solutions

### Import Errors

```bash
# Always set PYTHONPATH when running tests or scripts
PYTHONPATH=src poetry run pytest tests/
PYTHONPATH=src poetry run python -c "from flext_plugin import FlextPluginApi"
```

### Type Checking Issues

```bash
# Run type check to see specific errors
PYTHONPATH=src poetry run pyrefly check src/flext_plugin/api.py

# Check specific error codes
PYTHONPATH=src poetry run pyrefly check . --show-error-codes
```

### Test Failures

```bash
# Run with verbose output
pytest tests/unit/test_api.py -vv --tb=short

# Run single failing test
pytest tests/unit/test_api.py::test_plugin_discovery -xvs

# Run last failed tests
pytest --lf
```

### Circular Import Errors

```bash
# Usually caused by incorrect import order in __init__.py
# Check dependency chain - modules should not import from modules that import them
grep -r "from flext_plugin.api import" src/flext_plugin/
grep -r "from flext_plugin.platform import" src/flext_plugin/api.py
```

### Missing FlextResult Methods

```python
# Old API (deprecated in some contexts)
result.data    # May not exist
result.value   # Use this instead

# Safe extraction
result.unwrap()  # Raises if failure
result.unwrap_or(default)  # With default
```

---

## Integration with FLEXT Ecosystem

This project is part of the FLEXT monorepo workspace. Key integration points:

- **Depends on**: flext-core (foundation), flext-observability (monitoring)
- **Used by**: All FLEXT projects requiring plugin functionality
- **Architecture**: Follows workspace-level patterns defined in `../CLAUDE.md`
- **Quality Gates**: Must pass workspace-level validation before commits

See `../CLAUDE.md` for workspace-level standards and `README.md` for project overview.

---

## Key Principles

1. **FlextResult[T] everywhere** - All operations that can fail return FlextResult
2. **Clean Architecture** - Strict domain/application/infrastructure separation
3. **Protocol-based design** - Structural typing for maximum flexibility
4. **Single class per module** - Following flext-core ecosystem standard
5. **Type safety first** - 100% type annotations with Pyrefly strict mode
6. **Test real functionality** - Functional testing with real plugin operations
7. **Railway-oriented programming** - Composable error handling throughout
8. **Root module imports** - Ecosystem compatibility requirement

---

**FLEXT-Plugin** - Enterprise plugin management system providing the extensibility foundation for the entire FLEXT ecosystem.