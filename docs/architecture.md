# Architecture


<!-- TOC START -->
- [Clean Architecture Overview](#clean-architecture-overview)
- [Domain Layer](#domain-layer)
  - [Core Entities](#core-entities)
  - [Services](#services)
- [Application Layer](#application-layer)
  - [FlextPluginPlatform (Facade)](#flextpluginplatform-facade)
  - [Application Services](#application-services)
- [Infrastructure Layer](#infrastructure-layer)
  - [Adapters](#adapters)
- [Integration Patterns](#integration-patterns)
  - [FLEXT-Core Integration](#flext-core-integration)
  - [Singer Ecosystem Integration](#singer-ecosystem-integration)
- [Current Architecture Status ✅ COMPLIANT](#current-architecture-status-compliant)
  - [FLEXT Single-Class-Per-Module Compliance Achieved](#flext-single-class-per-module-compliance-achieved)
  - [Architecture Achievements](#architecture-achievements)
- [Future Architecture Enhancements](#future-architecture-enhancements)
  - [Version 0.10.0 Enhancements](#version-0100-enhancements)
  - [Version 1.0.0 Enterprise Features](#version-100-enterprise-features)
  - [Integration Points](#integration-points)
- [Related Documentation](#related-documentation)
<!-- TOC END -->

**FLEXT Plugin System Architecture**

---

## Clean Architecture Overview

flext-plugin follows Clean Architecture principles with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                    INTERFACE LAYER                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   CLI Interface │  │   API Interface │  │  Simple API     │  │
│  │                 │  │                 │  │                 │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                 APPLICATION LAYER                               │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │             FlextPluginPlatform (Facade)                    │ │
│  └─────────────────────────────────────────────────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Plugin        │  │   Discovery     │  │   Hot Reload    │  │
│  │   Services      │  │   Services      │  │   Services      │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                   DOMAIN LAYER                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │  FlextPlugin    │  │ FlextPluginModels.Config│  │PluginRegistry   │  │
│  │   (Entity)      │  │    (Entity)     │  │   (Entity)      │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                INFRASTRUCTURE LAYER                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │  File System    │  │    Watchdog     │  │   Containers    │  │
│  │   Discovery     │  │   Hot Reload    │  │      (DI)       │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Domain Layer

### Core Entities

#### FlextPlugin

```python
class FlextPlugin(FlextModels.Entity):
    """Core plugin entity with business rules"""
    name: str
    plugin_version: str
    status: PluginStatus
    config: t.Dict

    def activate(self) -> bool:
        """Business rule: Plugin must be loaded before activation"""

    def validate_business_rules(self) -> FlextResult[bool]:
        """Domain validation logic"""
```

#### FlextPluginModels.Config

```python
class FlextPluginModels.Config(FlextModels.Entity):
    """Plugin configuration with validation"""
    name: str
    version: str
    dependencies: t.StringList
    metadata: FlextPluginModels.Metadata

    class Config:
        frozen = True  # Immutable value object
```

### Services

Plugin-specific business logic that doesn't belong to a single entity.

---

## Application Layer

### FlextPluginPlatform (Facade)

Coordinates all plugin operations:

```python
class FlextPluginPlatform:
    """Main facade for plugin system"""

    def __init__(self, container: FlextContainer | None = None):
        self.container = container or FlextContainer()
        self._setup_services()

    def load_plugin(self, plugin: FlextPluginModels.Entity) -> FlextResult[bool]:
        """Coordinate plugin loading across services"""

    def discover_plugins(self, path: str) -> FlextResult[list[FlextPluginModels.Entity]]:
        """Coordinate plugin discovery"""
```

### Application Services

- **FlextPluginService**: Core plugin operations
- **FlextPluginDiscoveryService**: Plugin discovery and validation
- **Hot Reload Services**: File watching and reload logic

---

## Infrastructure Layer

### Adapters

#### File System Discovery

```python
class FileSystemPluginDiscovery:
    """Discovers plugins from file system"""

    def scan_directory(self, path: str) -> FlextResult[list[PluginInfo]]:
        """Scan directory for plugin files"""
```

#### Watchdog Integration

```python
class WatchdogHotReload:
    """File system monitoring for hot reload"""

    def watch_directory(self, path: str, callback: Callable):
        """Monitor directory for changes"""
```

---

## Integration Patterns

### FLEXT-Core Integration

#### FlextResult Pattern

All operations return `FlextResult[T]` for railway-oriented programming:

```python
def load_plugin(self, plugin: FlextPluginModels.Entity) -> FlextResult[bool]:
    try:
        # Plugin loading logic
        return FlextResult[bool].ok(True)
    except Exception as e:
        return FlextResult[bool].fail(f"Loading failed: {e}")
```

#### Dependency Injection

Uses FlextContainer for service management:

```python
def _setup_services(self) -> None:
    """Register services in DI container"""
    self.container.register(
        "plugin_service",
        FlextPluginService(container=self.container)
    )
```

### Singer Ecosystem Integration

Plugins can implement Singer tap/target patterns:

```python
class SingerTapPlugin(FlextPlugin):
    """Plugin implementing Singer tap protocol"""

    def create_tap(self) -> SingerTap:
        """Create Singer tap instance"""
```

---

## Current Architecture Status ✅ COMPLIANT

### FLEXT Single-Class-Per-Module Compliance Achieved

All modules follow the FLEXT single-class-per-module standard with nested helper classes:

- ✅ `entities.py`: Unified `FlextPluginModels` class (domain entities)
- ✅ `implementations.py`: Unified `FlextPluginImplementations` class (concrete implementations)
- ✅ `hot_reload.py`: Unified `FlextPluginHotReload` class (file monitoring)
- ✅ All 20 modules: Single main class following FLEXT ecosystem patterns

### Architecture Achievements

- ✅ **Clean Architecture**: Proper domain/application/infrastructure layer separation
- ✅ **Domain-Driven Design**: Entities with business rules and validation
- ✅ **FLEXT Compliance**: Single-class-per-module standard achieved across all modules
- ✅ **Type Safety**: Complete MyPy compliance with Python 3.13+ features
- ✅ **Railway Pattern**: FlextResult[T] throughout for composable error handling

---

## Future Architecture Enhancements

### Version 0.10.0 Enhancements

1. **Entry Points Discovery**: Python 3.13 `importlib.metadata` for pip-installable plugins
2. **CLI Integration**: Complete command-line interface with flext-cli integration
3. **Performance Optimization**: Enhanced plugin loading and execution efficiency
4. **Security Framework**: Plugin sandboxing and validation mechanisms

### Version 1.0.0 Enterprise Features

1. **Multi-Format Discovery**: Entry points + file-based + setuptools integration
2. **Advanced Security**: Process/container isolation for high-security environments
3. **Plugin Marketplace**: Registry integration for plugin distribution and discovery
4. **Enterprise Monitoring**: Comprehensive plugin metrics and health checks

### Integration Points

- **flext-cli**: Command-line plugin management
- **flext-web**: Web interface for plugin REDACTED_LDAP_BIND_PASSWORDistration
- **flext-api**: REST API for plugin operations
- **Singer Projects**: Plugin framework for data pipeline components

---

This architecture enables the plugin system to serve as reliable infrastructure for the entire FLEXT ecosystem while maintaining clean separation of concerns and integration with FLEXT-core patterns.

## Related Documentation

**Within Project**:

- Getting Started - Installation and basic usage
- API Reference - Complete API documentation
- Examples - Working code examples
- Development - Contributing guidelines

**Across Projects**:

- [flext-core Foundation](https://github.com/organization/flext/tree/main/flext-core/docs/architecture/overview.md) - Clean architecture and CQRS patterns
- [flext-core Service Patterns](https://github.com/organization/flext/tree/main/flext-core/docs/guides/service-patterns.md) - Service patterns and dependency injection
- [flext-meltano Pipelines](https://github.com/organization/flext/tree/main/flext-meltano/CLAUDE.md) - Data integration and ELT orchestration

**External Resources**:

- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
