# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `flext-plugin`, an enterprise-grade plugin management system for the FLEXT data platform. It implements dynamic plugin loading, lifecycle management, and hot-reload capabilities using Clean Architecture and Domain-Driven Design patterns.

**Key Features:**
- Dynamic plugin discovery and loading
- Hot-reload with file watching capabilities  
- Plugin lifecycle management (activate, deactivate, enable, disable)
- Clean Architecture with strict layer separation
- Domain-driven design with plugin entities and value objects
- Type-safe implementation with Python 3.13
- Enterprise-grade quality gates and testing

## Architecture

The project follows Clean Architecture with these layers:

### Core Layer (`src/flext_plugin/core/`)
- **`types.py`**: Core plugin types, enums (`PluginStatus`, `PluginType`), and result objects
- **`discovery.py`**: Plugin discovery logic

### Domain Layer (`src/flext_plugin/domain/`)
- **`entities.py`**: Core business entities (`FlextPlugin`, `FlextPluginConfig`, `FlextPluginMetadata`, `FlextPluginRegistry`)
- **`ports.py`**: Domain interfaces/contracts

### Application Layer (`src/flext_plugin/application/`)
- **`services.py`**: Application services (`FlextPluginService`, `FlextPluginDiscoveryService`)
- **`handlers.py`**: Command/query handlers

### Infrastructure Layer (`src/flext_plugin/infrastructure/`)
- **`di_container.py`**: Dependency injection setup

### Platform Integration
- **`platform.py`**: Main platform class providing unified API access
- **`simple_api.py`**: Simplified API for common operations
- **Hot-reload system**: File watching and dynamic plugin reloading

## Development Commands

All commands use Poetry for dependency management and follow zero-tolerance quality gates.

### Essential Quality Checks
```bash
make validate          # Complete validation (lint + type + security + test) - MUST PASS
make check             # Essential checks (lint + type + test)
make lint              # Ruff linting with ALL rules enabled
make type-check        # MyPy strict mode (zero errors tolerated)
make security          # Security scans (bandit + pip-audit)
```

### Testing (85% coverage minimum)
```bash
make test              # Full test suite with coverage validation
make test-unit         # Unit tests only
make test-integration  # Integration tests only
make test-plugin       # Plugin-specific tests
make coverage          # Generate detailed coverage report
```

### Plugin Management Commands
```bash
# Plugin lifecycle
make plugin-create NAME=my-plugin TYPE=extractor    # Create new plugin
make plugin-install NAME=tap-github                 # Install plugin
make plugin-list                                    # List all plugins
make plugin-watch                                   # Watch with hot-reload
make plugin-reload                                  # Hot reload all plugins

# Plugin state management  
make plugin-enable NAME=plugin-name                 # Enable plugin
make plugin-disable NAME=plugin-name                # Disable plugin
make plugin-validate                                # Validate plugin system
```

### Development Setup
```bash
make setup             # Complete development setup  
make install           # Install dependencies
make dev-install       # Development environment setup
make pre-commit        # Setup pre-commit hooks
```

### Build & Cleanup
```bash
make build             # Build distribution packages
make clean             # Remove all artifacts
make format            # Format code with ruff
make fix               # Auto-fix all issues
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

The project maintains 85% minimum test coverage with comprehensive test categories:

```bash
# Run specific test categories
pytest -m unit              # Unit tests
pytest -m integration       # Integration tests  
pytest -m plugin            # Plugin system tests
pytest -m hot_reload        # Hot-reload functionality tests
```

**Test Structure:**
- `tests/unit/`: Isolated unit tests for each layer
- `tests/integration/`: Cross-layer integration tests
- `tests/e2e/`: End-to-end plugin lifecycle tests
- `tests/fixtures/`: Shared test data and fixtures

## Configuration

The plugin system uses environment variables for configuration:

```bash
# Plugin discovery
FLEXT_PLUGIN_DISCOVERY_PATHS=plugins:~/.flext/plugins:/opt/flext/plugins
FLEXT_PLUGIN_CACHE_DIR=.plugin_cache

# Hot reload
FLEXT_PLUGIN_HOT_RELOAD=true
FLEXT_PLUGIN_WATCH_INTERVAL=2
FLEXT_PLUGIN_RELOAD_ON_CHANGE=true
FLEXT_PLUGIN_PRESERVE_STATE=true
FLEXT_PLUGIN_ROLLBACK_ON_ERROR=true

# Performance
FLEXT_PLUGIN_MAX_WORKERS=10
```

## Common Development Patterns

### Creating a New Plugin
1. Use `make plugin-create NAME=my-plugin TYPE=extractor`
2. Implement required interfaces from `domain/ports.py`
3. Follow the plugin lifecycle: `initialize()` → `execute()` → `cleanup()`
4. Add comprehensive tests with 85%+ coverage
5. Validate with `make plugin-validate`

### Plugin Hot Reload Development
1. Start file watcher: `make plugin-watch`
2. Make changes to plugin files
3. System automatically detects and reloads plugins
4. Test with `make plugin-test-hot-reload`

### Quality Gate Workflow
1. Make code changes
2. Run `make fix` to auto-format and fix issues
3. Run `make validate` - ALL checks must pass
4. Commit only after validation succeeds

## Integration with FLEXT Ecosystem

This plugin system integrates with the larger FLEXT platform:
- **FlexCore**: Runtime container service (Go) on port 8080
- **FLEXT Service**: Data platform service (Go/Python) on port 8081  
- **Singer Integration**: Supports tap/target/transform plugins for Meltano
- **Clean Architecture**: Follows platform-wide architectural patterns

The plugin system is designed to be platform-agnostic while providing deep integration with FLEXT's data processing pipeline.

## TODO: GAPS DE ARQUITETURA IDENTIFICADOS - PRIORIDADE CRÍTICA

### 🚨 GAP 1: Plugin System Foundation Missing in flext-core
**Status**: CRÍTICO - flext-core não tem plugin foundation mas flext-plugin implementa sistema completo
**Problema**:
- flext-plugin implementa sistema completo mas flext-core não tem plugin base
- Inconsistência arquitetural: foundation missing in core library
- Plugin interfaces podem não ser compatíveis com ecosystem expectations

**TODO**:
- [ ] Migrar plugin foundation patterns para flext-core
- [ ] Criar FlextPlugin base interface em flext-core
- [ ] Refatorar flext-plugin para usar flext-core plugin foundation
- [ ] Documentar plugin architecture consistency com ecosystem

### 🚨 GAP 2: FlexCore (Go) Plugin Integration Missing
**Status**: CRÍTICO - FlexCore menciona plugin system mas sem integration
**Problema**:
- FlexCore (Go) usa plugin system mas não integra com flext-plugin
- Protocol para Go-Python plugin communication não definido
- Plugin registry não shared entre Go e Python services

**TODO**:
- [ ] Criar shared plugin registry entre Go e Python
- [ ] Implementar Go-Python plugin communication protocols
- [ ] Documentar plugin integration patterns com FlexCore
- [ ] Criar plugin testing patterns cross-language

### 🚨 GAP 3: Meltano Plugin Integration Superficial
**Status**: ALTO - Singer plugin types mencionados mas integration incomplete
**Problema**:
- PluginType define TAP, TARGET, TRANSFORM mas Meltano integration não completa
- Plugin discovery não integra com Meltano project structure
- Hot-reload não compatível com Meltano plugin lifecycle

**TODO**:
- [ ] Implementar complete Meltano plugin integration
- [ ] Integrar plugin discovery com meltano.yml configuration
- [ ] Criar Meltano-compatible plugin lifecycle management
- [ ] Documentar Singer plugin development patterns

### 🚨 GAP 4: Plugin CLI Integration Missing
**Status**: ALTO - Plugin management não integrado com flext-cli
**Problema**:
- Plugin management commands não available via flext-cli
- Plugin hot-reload não accessible via CLI
- Plugin validation não integrated com CLI workflow

**TODO**:
- [ ] Integrar plugin commands com flext-cli
- [ ] Implementar plugin management via flext CLI
- [ ] Criar plugin development workflow via CLI
- [ ] Documentar plugin CLI usage patterns