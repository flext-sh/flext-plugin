# Architecture

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
│  │  FlextPlugin    │  │ FlextPluginConfig│  │PluginRegistry   │  │
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
    config: Dict[str, object]

    def activate(self) -> bool:
        """Business rule: Plugin must be loaded before activation"""

    def validate_business_rules(self) -> FlextResult[bool]:
        """Domain validation logic"""
```

#### FlextPluginConfig

```python
class FlextPluginConfig(FlextModels.Entity):
    """Plugin configuration with validation"""
    name: str
    version: str
    dependencies: List[str]
    metadata: FlextPluginMetadata

    class Config:
        frozen = True  # Immutable value object
```

### Domain Services

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

    def load_plugin(self, plugin: FlextPluginEntity) -> FlextResult[bool]:
        """Coordinate plugin loading across services"""

    def discover_plugins(self, path: str) -> FlextResult[list[FlextPluginEntity]]:
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
def load_plugin(self, plugin: FlextPluginEntity) -> FlextResult[bool]:
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

## Current Architecture Issues

### Multi-Class Module Problem

Several modules violate the FLEXT single-class-per-module standard:

- `entities.py`: 8 classes (needs consolidation)
- `implementations.py`: 10+ classes (needs consolidation)
- `hot_reload.py`: 10+ classes (needs consolidation)

### Resolution Strategy

Each module will be refactored to have one main class with nested helper classes:

```python
class FlextPluginEntities:
    """Unified plugin entities with nested helpers"""

    class Plugin(FlextModels.Entity):
        """Main plugin entity"""

    class Config(FlextModels.Entity):
        """Plugin configuration entity"""

    class _ValidationHelper:
        """Nested validation helper"""
```

---

## Future Architecture

### Planned Enhancements

1. **Entry Points Discovery**: Standard Python plugin discovery mechanism
2. **Process Isolation**: Subprocess-based plugin execution for security
3. **Container Integration**: Docker/Podman support for high-security environments
4. **Configuration Management**: TOML, YAML, JSON support with schema validation

### Integration Points

- **flext-cli**: Command-line plugin management
- **flext-web**: Web interface for plugin REDACTED_LDAP_BIND_PASSWORDistration
- **flext-api**: REST API for plugin operations
- **Singer Projects**: Plugin framework for data pipeline components

---

This architecture enables the plugin system to serve as reliable infrastructure for the entire FLEXT ecosystem while maintaining clean separation of concerns and integration with FLEXT-core patterns.
