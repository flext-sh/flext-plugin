# Python Module Organization & Semantic Patterns

<!-- TOC START -->
- [🏗️ **Module Architecture Overview**](#module-architecture-overview)
  - [**Core Design Principles**](#core-design-principles)
- [📁 **Module Structure & Responsibilities**](#module-structure-responsibilities)
  - [**Foundation Layer** (`src/flext_plugin/`)](#foundation-layer-srcflextplugin)
  - [**Core Layer** (`src/flext_plugin/core/`)](#core-layer-srcflextplugincore)
  - [**Domain Layer** (`src/flext_plugin/domain/`)](#domain-layer-srcflextplugindomain)
  - [**Application Layer** (`src/flext_plugin/application/`)](#application-layer-srcflextpluginapplication)
  - [**Configuration Layer** (`src/flext_plugin/settings/`)](#configuration-layer-srcflextpluginconfig)
- [🎯 **Semantic Naming Conventions**](#semantic-naming-conventions)
  - [**Public API Naming (FlextPlugin prefix)**](#public-api-naming-flextplugin-prefix)
  - [**Module-Level Naming**](#module-level-naming)
  - [**Plugin Type Naming**](#plugin-type-naming)
- [📦 **Import Patterns & Best Practices**](#import-patterns-best-practices)
  - [**Recommended Import Styles**](#recommended-import-styles)
  - [**Anti-Patterns (Forbidden)**](#anti-patterns-forbidden)
- [🏛️ **Architectural Patterns**](#architectural-patterns)
  - [**Clean Architecture Layer Separation**](#clean-architecture-layer-separation)
  - [**Plugin Lifecycle Architecture**](#plugin-lifecycle-architecture)
  - [**Hot-Reload Architecture**](#hot-reload-architecture)
- [🔄 **Plugin-Oriented Programming Patterns**](#plugin-oriented-programming-patterns)
  - [**Plugin Factory Patterns**](#plugin-factory-patterns)
  - [**Plugin Lifecycle Management**](#plugin-lifecycle-management)
  - [**Plugin Discovery Patterns**](#plugin-discovery-patterns)
- [🎯 **Domain-Driven Design Patterns**](#domain-driven-design-patterns)
  - [**Plugin Entity Patterns**](#plugin-entity-patterns)
  - [**Plugin Aggregate Patterns**](#plugin-aggregate-patterns)
  - [**Plugin Value Object Patterns**](#plugin-value-object-patterns)
- [🚀 **Performance & Optimization Patterns**](#performance-optimization-patterns)
  - [**Lazy Plugin Loading**](#lazy-plugin-loading)
  - [**Plugin Caching Patterns**](#plugin-caching-patterns)
- [📏 **Code Quality Standards**](#code-quality-standards)
  - [**Type Annotation Requirements**](#type-annotation-requirements)
  - [**Error Handling Standards**](#error-handling-standards)
  - [**Plugin Documentation Standards**](#plugin-documentation-standards)
- [📋 **Checklist for Plugin Module Creation**](#checklist-for-plugin-module-creation)
  - [**Plugin Module Creation Checklist**](#plugin-module-creation-checklist)
  - [**Plugin Quality Gate Checklist**](#plugin-quality-gate-checklist)
  - [**Plugin-Specific Validation**](#plugin-specific-validation)
- [🌐 **FLEXT Ecosystem Integration Guidelines**](#flext-ecosystem-integration-guidelines)
  - [**Cross-Project Plugin Standards**](#cross-project-plugin-standards)
  - [**Plugin Configuration Integration**](#plugin-configuration-integration)
  - [**Plugin Registry Integration**](#plugin-registry-integration)
<!-- TOC END -->

**FLEXT Plugin Module Architecture & Best Practices for Plugin System Development**

______________________________________________________________________

## 🏗️ **Module Architecture Overview**

FLEXT Plugin implements a **Clean Architecture layered module system** specifically designed for dynamic plugin management within the FLEXT ecosystem. This structure follows the established patterns from flext-core while adding plugin-specific architectural layers for lifecycle management, discovery, and hot-reload capabilities.

### **Core Design Principles**

1. **Plugin-First Architecture**: Every module designed for dynamic plugin loading
1. **Lifecycle Management**: Clear separation of plugin states and transitions
1. **Hot-Reload Capability**: File watching and dynamic reloading support
1. **Type-Safe Plugin System**: Comprehensive type hints for plugin interfaces
1. **Ecosystem Integration**: Seamless integration with 32 FLEXT projects

______________________________________________________________________

## 📁 **Module Structure & Responsibilities**

### **Foundation Layer** (`src/flext_plugin/`)

```python
# Plugin system foundation
src/flext_plugin/
├── __init__.py              # 🎯 Plugin system public API gateway
├── platform.py              # 🎯 Main plugin platform orchestration
├── simple_api.py            # 🎯 Simplified factory functions
├── simple_plugin.py         # 🎯 Basic plugin interface
├── hot_reload.py            # 🎯 Hot-reload system integration
├── loader.py                # 🎯 Dynamic plugin loading
├── discovery.py             # 🎯 High-level plugin discovery
└── py.typed                 # 🎯 Type checking marker
```

**Responsibility**: Establish the plugin system's public interface and high-level orchestration.

**Import Pattern**:

```python
# Primary entry point for plugin system
from flext_plugin import FlextPluginPlatform, create_flext_plugin
from flext_plugin import create_flext_plugin_platform
```

### **Core Layer** (`src/flext_plugin/core/`)

```python
# Plugin system core patterns
├── core/
│   ├── __init__.py          # 🚀 Core plugin types export
│   ├── types.py             # 🚀 Plugin types, enums, results
│   └── discovery.py         # 🚀 Core discovery algorithms
```

**Responsibility**: Define fundamental plugin types, status enums, and core discovery logic.

**Usage Pattern**:

```python
from flext_plugin import PluginStatus, PluginType, PluginError
from flext_plugin import PluginDiscovery

# Plugin type definitions
plugin_type = PluginType.TAP  # Singer data extraction
status = PluginStatus.ACTIVE  # Plugin lifecycle state
```

### **Domain Layer** (`src/flext_plugin/domain/`)

```python
# Plugin domain modeling (DDD)
├── domain/
│   ├── __init__.py          # 🏛️ Domain exports
│   ├── entities.py          # 🏛️ Plugin entities (FlextPlugin, FlextPluginModels.Registry)
│   ├── ports.py             # 🏛️ Domain interfaces and contracts
│   └── value_objects.py     # 🏛️ Plugin metadata and configuration
```

**Responsibility**: Rich domain modeling following Domain-Driven Design principles.

**Entity Pattern**:

```python
from flext_plugin import FlextPlugin, FlextPluginModels.Registry
from flext_plugin import FlextPlugins.Manager

class CustomPlugin(FlextPlugin):
    """Rich plugin entity with business logic"""

    def activate(self) -> r[bool]:
        """Business operation with domain validation"""
        if self.status == PluginStatus.ACTIVE:
            return r[bool].fail("Plugin already active")

        # Business logic and domain events
        self.status = PluginStatus.ACTIVE
        self.add_domain_event("PluginActivated", {"plugin_id": self.id})
        return r[bool].ok(data=True)
```

### **Application Layer** (`src/flext_plugin/application/`)

```python
# Plugin application services and handlers
├── application/
│   ├── __init__.py          # 📤 Application layer exports
│   ├── services.py          # 📤 Plugin management services
│   └── handlers.py          # 📤 CQRS command/query handlers
```

**Responsibility**: Orchestrate plugin business logic and coordinate between layers.

**Service Pattern**:

```python
from flext_plugin import (
    FlextPluginService,
    FlextPluginDiscoveryService,
)
from flext_plugin import FlextPluginHandler


class PluginWorkflow:
    def __init__(self, service: FlextPluginService):
        self.service = service

    def deploy_plugin(self, plugin_config: dict) -> r[FlextPlugin]:
        """Complete plugin deployment workflow"""
        return (
            self.service
            .validate_plugin_config(plugin_config)
            .flat_map(lambda settings: self.service.create_plugin(settings))
            .flat_map(lambda plugin: self.service.register_plugin(plugin))
            .flat_map(lambda plugin: self.service.activate_plugin(plugin.id))
        )
```

### **Configuration Layer** (`src/flext_plugin/settings/`)

```python
# Plugin configuration management
├── settings/
│   ├── __init__.py          # ⚙️ Configuration exports
│   ├── settings.py          # ⚙️ Plugin-specific settings
│   ├── validation.py        # ⚙️ Configuration validation
│   └── environment.py       # ⚙️ Environment-specific settings
```

**Responsibility**: Handle plugin system configuration, validation, and environment management.

**Configuration Pattern**:

```python
from flext_plugin import PluginSystemSettings
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import FlextLogger
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u


class PluginSystemSettings(FlextSettings):
    """Plugin system configuration with environment support"""

    discovery_paths: t.StringList = ["./plugins", "~/.flext/plugins"]
    hot_reload_enabled: bool = True
    watch_interval: int = 2
    max_workers: int = 10
    cache_dir: str = ".plugin_cache"

    class Config:
        env_prefix = "FLEXT_PLUGIN_"
        env_file = ".env"


# Environment variables:
# FLEXT_PLUGIN_DISCOVERY_PATHS=/opt/plugins:/usr/local/plugins
# FLEXT_PLUGIN_HOT_RELOAD_ENABLED=true
# FLEXT_PLUGIN_WATCH_INTERVAL=1
```

______________________________________________________________________

## 🎯 **Semantic Naming Conventions**

### **Public API Naming (FlextPlugin prefix)**

All plugin-related exports use consistent prefixing to avoid namespace conflicts:

```python
# Core plugin patterns
FlextPlugin  # Main plugin entity
FlextPluginModels.Config  # Plugin configuration entity
FlextPluginModels.Metadata  # Plugin metadata value t.NormalizedValue
FlextPluginModels.Registry  # Plugin collection aggregate
FlextPluginPlatform  # Main platform orchestrator

# Plugin management patterns
FlextPluginService  # Core plugin management service
FlextPluginDiscoveryService  # Plugin discovery and scanning
FlextPluginHandler  # CQRS command/query handler
FlextPlugins.Manager  # Plugin management interface

# Plugin lifecycle patterns
FlextPluginLoader  # Dynamic plugin loading
FlextPluginWatcher  # File system watching
FlextPluginReloader  # Hot-reload management
```

**Rationale**: Clear namespace separation prevents conflicts across FLEXT's 32 projects.

### **Module-Level Naming**

```python
# Core functionality modules
types.py  # Plugin types, enums, and result objects
entities.py  # Domain entities (FlextPlugin, FlextPluginModels.Registry)
ports.py  # Domain interfaces and contracts
services.py  # Application services and business logic
handlers.py  # CQRS command and query handlers

# Platform integration modules
platform.py  # Main platform orchestration
simple_api.py  # Factory functions and utilities
hot_reload.py  # Hot-reload system integration
discovery.py  # High-level plugin discovery
loader.py  # Dynamic plugin loading mechanisms
```

**Pattern**: One primary concern per module with cohesive functionality.

### **Plugin Type Naming**

```python
# Singer ETL plugin types (Meltano integration)
PluginType.TAP  # Data extraction from sources
PluginType.TARGET  # Data loading to destinations
PluginType.TRANSFORM  # DBT-based transformations

# Architecture plugin types
PluginType.SERVICE  # Microservice components
PluginType.MIDDLEWARE  # Request/response processing
PluginType.EXTENSION  # Platform extensions

# Integration plugin types
PluginType.API  # REST/GraphQL endpoints
PluginType.DATABASE  # Database connectivity
PluginType.AUTHENTICATION  # Auth providers and strategies

# Utility plugin types
PluginType.UTILITY  # General-purpose utilities
PluginType.TOOL  # Development and REDACTED_LDAP_BIND_PASSWORD tools
PluginType.PROCESSOR  # Data processing components
```

______________________________________________________________________

## 📦 **Import Patterns & Best Practices**

### **Recommended Import Styles**

#### **1. Primary Pattern (Recommended for Ecosystem)**

```python
# Import from main package - gets everything needed
from flext_plugin import (
    FlextPluginPlatform,
    create_flext_plugin,
    create_flext_plugin_platform,
)
from flext_plugin import PluginStatus, PluginType


# Use patterns directly
def deploy_plugin():
    platform = create_flext_plugin_platform()
    plugin = create_flext_plugin(
        name="data-processor", version="0.9.9", plugin_type=PluginType.PROCESSOR
    )
    return platform.register_plugin(plugin)
```

#### **2. Specific Module Pattern (For Advanced Usage)**

```python
# Import from specific modules for clarity
from flext_plugin import FlextPlugin, FlextPluginModels.Registry
from flext_plugin import FlextPluginService
from flext_plugin import PluginStatus, PluginType

# More explicit but verbose
service = FlextPluginService(registry)
plugin = FlextPlugin(name="custom", version="0.9.9")
```

#### **3. Factory Function Pattern**

```python
# Use factory functions for common operations
from flext_plugin import (
    create_flext_plugin,
    create_flext_plugin_config,
    create_flext_plugin_metadata,
    create_flext_plugin_registry,
)

# Simplified plugin creation
plugin = create_flext_plugin(
    name="api-gateway",
    version="2.1.0",
    plugin_type=PluginType.API,
    settings={
        "description": "API Gateway plugin",
        "author": "FLEXT Team",
        "endpoints": ["/api/v1/*", "/api/v2/*"],
    },
)
```

### **Anti-Patterns (Forbidden)**

```python
# ❌ Don't import everything
from flext_plugin import *

# ❌ Don't import internal modules
from flext_plugin import _PrivateClass

# ❌ Don't use deep imports for public APIs
from flext_plugin import FlextPlugin, _private_method

# ❌ Don't alias core plugin types
from flext_plugin import FlextPlugin as Plugin  # Confusing across ecosystem

# ❌ Don't bypass the main API
from flext_plugin import _InternalPlatformManager
```

______________________________________________________________________

## 🏛️ **Architectural Patterns**

### **Clean Architecture Layer Separation**

```python
# Plugin-specific Clean Architecture layers
┌─────────────────────────────────────────┐
│         Platform Integration            │  # platform.py, simple_api.py
│    (External Plugin Interfaces)         │  # hot_reload.py, loader.py
├─────────────────────────────────────────┤
│         Application Layer               │  # services.py, handlers.py
│  (Plugin Management, CQRS Handlers)     │  # workflow orchestration
├─────────────────────────────────────────┤
│          Domain Layer                   │  # entities.py, ports.py
│   (Plugin Business Logic, DDD)          │  # value_objects.py
├─────────────────────────────────────────┤
│           Core Layer                    │
│    (Plugin Types, Base Patterns)        │  # error handling
├─────────────────────────────────────────┤
│        Foundation Layer                 │  # flext-core integration
│   (r, FlextContainer)         │  # base patterns
└─────────────────────────────────────────┘
```

### **Plugin Lifecycle Architecture**

```python
# Plugin state transitions with architectural boundaries
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  DISCOVERED  │───▶│    LOADED    │───▶│    ACTIVE    │
│  (Discovery) │    │   (Loader)   │    │  (Platform)  │
└──────────────┘    └──────────────┘    └──────────────┘
        │                    │                    │
        │                    ▼                    ▼
        │            ┌──────────────┐    ┌──────────────┐
        │            │    ERROR     │    │   INACTIVE   │
        │            │  (Handler)   │    │  (Platform)  │
        │            └──────────────┘    └──────────────┘
        │                    │                    │
        ▼                    │                    │
┌──────────────┐            │                    │
│   DISABLED   │◀───────────┴────────────────────┘
│  (Manager)   │
└──────────────┘
```

### **Hot-Reload Architecture**

```python
# Hot-reload system with file watching and state preservation
┌─────────────────────────────────────────────────────────┐
│                File System Watcher                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   plugins/  │  │ ~/.flext/   │  │ /opt/flext/ │    │
│  │   directory │  │   plugins   │  │   plugins   │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────┘
            │                    │                    │
            ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────┐
│                 Change Detection                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Created   │  │  Modified   │  │   Deleted   │    │
│  │    Files    │  │    Files    │  │    Files    │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────┘
            │                    │                    │
            ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────┐
│                 Plugin Reloader                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ State Save  │  │   Reload    │  │State Restore│    │
│  │ & Cleanup   │  │   Plugin    │  │ & Activate  │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────┘
```

______________________________________________________________________

## 🔄 **Plugin-Oriented Programming Patterns**

### **Plugin Factory Patterns**

```python
from flext_plugin import create_flext_plugin
from flext_plugin import PluginType
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import FlextLogger
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u


# Factory pattern for plugin creation
def create_singer_tap_plugin(
    name: str, version: str, tap_config: t.Dict
) -> r[FlextPlugin]:
    """Create Singer tap plugin with validation."""
    try:
        plugin = create_flext_plugin(
            name=f"tap-{name}",
            version=version,
            plugin_type=PluginType.TAP,
            settings={
                **tap_config,
                "singer_spec": "0.9.9",
                "description": f"Singer tap for {name} data extraction",
            },
        )
        return r[bool].ok(plugin)
    except Exception as e:
        return r[bool].fail(f"Failed to create tap plugin: {e}")


# Usage with railway-oriented chaining
def deploy_tap_plugin(settings: dict) -> r[FlextPlugin]:
    return (
        validate_tap_config(settings)
        .flat_map(
            lambda cfg: create_singer_tap_plugin(cfg["name"], cfg["version"], cfg)
        )
        .flat_map(lambda plugin: register_plugin(plugin))
        .flat_map(lambda plugin: activate_plugin(plugin.id))
    )
```

### **Plugin Lifecycle Management**

```python
from flext_plugin import FlextPlugin
from flext_plugin import PluginStatus
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import FlextLogger
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u


class PluginLifecycleManager:
    """Manages plugin lifecycle with state transitions."""

    def initialize_plugin(self, plugin: FlextPlugin) -> r[bool]:
        """Initialize plugin with resource allocation."""
        if plugin.status != PluginStatus.LOADED:
            return r[bool].fail("Plugin must be loaded before initialization")

        try:
            # Allocate resources
            self._allocate_plugin_resources(plugin)

            # Run initialization logic
            init_result = plugin.initialize()
            if init_result.is_failure:
                self._cleanup_plugin_resources(plugin)
                return init_result

            # Update status
            plugin.status = PluginStatus.INACTIVE
            self._emit_plugin_event("PluginInitialized", plugin)

            return r[bool].ok(data=True)

        except Exception as e:
            self._cleanup_plugin_resources(plugin)
            return r[bool].fail(f"Plugin initialization failed: {e}")

    def activate_plugin(self, plugin: FlextPlugin) -> r[bool]:
        """Activate plugin with dependency checking."""
        if plugin.status not in [PluginStatus.INACTIVE, PluginStatus.LOADED]:
            return r[bool].fail("Plugin not ready for activation")

        # Check dependencies
        dependency_check = self._validate_plugin_dependencies(plugin)
        if dependency_check.is_failure:
            return dependency_check

        # Activate plugin
        activation_result = plugin.activate()
        if activation_result.success:
            plugin.status = PluginStatus.ACTIVE
            self._emit_plugin_event("PluginActivated", plugin)

        return activation_result

    def hot_reload_plugin(self, plugin_id: str) -> r[FlextPlugin]:
        """Hot reload plugin with state preservation."""
        try:
            # Get current plugin
            current_plugin = self._get_plugin(plugin_id)
            if current_plugin.is_failure:
                return current_plugin

            plugin = current_plugin.data

            # Save current state
            state_backup = self._backup_plugin_state(plugin)

            # Deactivate and unload
            self.deactivate_plugin(plugin)
            self._unload_plugin(plugin)

            # Reload plugin
            reload_result = self._reload_plugin_from_file(plugin_id)
            if reload_result.is_failure:
                # Restore from backup
                self._restore_plugin_state(plugin, state_backup.data)
                return reload_result

            new_plugin = reload_result.data

            # Restore state and reactivate
            self._restore_plugin_state(new_plugin, state_backup.data)
            self.activate_plugin(new_plugin)

            return r[bool].ok(new_plugin)

        except Exception as e:
            return r[bool].fail(f"Hot reload failed: {e}")
```

### **Plugin Discovery Patterns**

```python
from flext_plugin import FlextPluginDiscoveryService
from flext_plugin import PluginDiscovery
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import FlextLogger
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u


class AdvancedPluginDiscovery:
    """Advanced plugin discovery with filtering and validation."""

    def __init__(self, discovery_service: FlextPluginDiscoveryService):
        self.discovery_service = discovery_service
        self.core_discovery = PluginDiscovery()

    def discover_plugins_by_type(
        self, plugin_type: PluginType, paths: t.StringList
    ) -> r[List[FlextPlugin]]:
        """Discover plugins filtered by type."""
        try:
            all_plugins = []

            for path in paths:
                result = self.discovery_service.discover_plugins(path)
                if result.success:
                    # Filter by type
                    typed_plugins = [
                        p
                        for p in result.data
                        if hasattr(p, "plugin_type") and p.plugin_type == plugin_type
                    ]
                    all_plugins.extend(typed_plugins)

            return r[bool].ok(all_plugins)

        except Exception as e:
            return r[bool].fail(f"Plugin discovery failed: {e}")

    def discover_singer_plugins(
        self, meltano_path: str
    ) -> r[Mapping[str, List[FlextPlugin]]]:
        """Discover Singer plugins from Meltano project structure."""
        try:
            meltano_yml_path = Path(meltano_path) / "meltano.yml"
            if not meltano_yml_path.exists():
                return r[bool].fail("meltano.yml not found")

            # Parse meltano.yml
            meltano_config = self._parse_meltano_config(meltano_yml_path)

            # Discover by Singer plugin type
            singer_plugins = {
                "taps": self.discover_plugins_by_type(PluginType.TAP, [meltano_path]),
                "targets": self.discover_plugins_by_type(
                    PluginType.TARGET, [meltano_path]
                ),
                "transforms": self.discover_plugins_by_type(
                    PluginType.TRANSFORM, [meltano_path]
                ),
            }

            # Validate against meltano.yml
            validated_plugins = {}
            for category, plugins_result in singer_plugins.items():
                if plugins_result.success:
                    validated = self._validate_against_meltano_config(
                        plugins_result.data, meltano_config.get(category, [])
                    )
                    validated_plugins[category] = (
                        validated.data if validated.success else []
                    )

            return r[bool].ok(validated_plugins)

        except Exception as e:
            return r[bool].fail(f"Singer plugin discovery failed: {e}")
```

______________________________________________________________________

## 🎯 **Domain-Driven Design Patterns**

### **Plugin Entity Patterns**

```python
from flext_plugin import FlextPlugin
from flext_plugin import PluginStatus, PluginType
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import FlextLogger
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u
from typing import List, Dict
from datetime import datetime


class FlextPlugin(FlextModels.Entity):
    """
    Rich plugin entity with comprehensive business logic.

    Represents a plugin in the FLEXT ecosystem with full lifecycle management,
    dependency tracking, and event sourcing capabilities.
    """

    # Core plugin attributes
    name: str
    plugin_version: str
    plugin_type: PluginType
    status: PluginStatus = PluginStatus.DISCOVERED

    # Metadata and configuration
    description: str = ""
    author: str = ""
    homepage_url: str = ""
    repository_url: str = ""
    license: str = "MIT"
    tags: t.StringList = field(default_factory=list)

    # Dependencies and compatibility
    dependencies: t.StringList = field(default_factory=list)
    flext_core_version: str = ">=0.9.9"
    python_version: str = ">=3.13"

    # Runtime state
    last_activated: Optional[datetime] = None
    last_executed: Optional[datetime] = None
    execution_count: int = 0
    error_count: int = 0

    # Business logic methods
    def can_activate(self) -> r[bool]:
        """Check if plugin can be activated with business rules."""
        if self.status == PluginStatus.ACTIVE:
            return r[bool].fail("Plugin already active")

        if self.status not in [PluginStatus.LOADED, PluginStatus.INACTIVE]:
            return r[bool].fail(f"Cannot activate plugin in {self.status} state")

        # Check dependencies
        if not self._validate_dependencies():
            return r[bool].fail("Plugin dependencies not satisfied")

        return r[bool].ok(data=True)

    def activate(self) -> r[bool]:
        """Activate plugin with business validation and event generation."""
        validation = self.can_activate()
        if validation.is_failure:
            return validation

        # Perform activation
        self.status = PluginStatus.ACTIVE
        self.last_activated = datetime.utcnow()

        # Generate domain event
        self.add_domain_event({
            "type": "PluginActivated",
            "plugin_id": str(self.id),
            "plugin_name": self.name,
            "timestamp": self.last_activated.isoformat(),
            "plugin_type": self.plugin_type.value,
        })

        return r[bool].ok(data=True)

    def record_execution(self, success: bool, execution_time: float) -> None:
        """Record plugin execution with metrics."""
        self.execution_count += 1
        self.last_executed = datetime.utcnow()

        if not success:
            self.error_count += 1

        # Generate execution event
        self.add_domain_event({
            "type": "PluginExecuted",
            "plugin_id": str(self.id),
            "success": success,
            "execution_time": execution_time,
            "timestamp": self.last_executed.isoformat(),
        })

    def get_health_status(self) -> t.Dict:
        """Get plugin health metrics."""
        if self.execution_count == 0:
            success_rate = 0.0
        else:
            success_rate = (
                self.execution_count - self.error_count
            ) / self.execution_count

        return {
            "status": self.status.value,
            "execution_count": self.execution_count,
            "error_count": self.error_count,
            "success_rate": success_rate,
            "last_executed": self.last_executed.isoformat()
            if self.last_executed
            else None,
            "health": "healthy"
            if success_rate > 0.9
            else "degraded"
            if success_rate > 0.5
            else "unhealthy",
        }

    def _validate_dependencies(self) -> bool:
        """Validate plugin dependencies are satisfied."""
        # Implementation for dependency validation
        return True
```

### **Plugin Aggregate Patterns**

```python
from flext_plugin import FlextPluginModels.Registry
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import FlextLogger
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u
from typing import Dict, List, Optional

class FlextPluginModels.Registry(FlextModels.AggregateRoot):
    """
    Plugin registry aggregate managing plugin collections.

    Serves as the consistency boundary for plugin operations,
    ensuring business rules and maintaining registry integrity.
    """

    plugins: Dict[str, FlextPlugin] = field(default_factory=dict)
    discovery_paths: t.StringList = field(default_factory=list)
    last_discovery: Optional[datetime] = None
    registry_version: str = "0.9.9"

    # Registry-level business rules
    MAX_PLUGINS_PER_TYPE = 100
    RESERVED_PLUGIN_NAMES = ["system", "core", "REDACTED_LDAP_BIND_PASSWORD", "flext"]

    def register_plugin(self, plugin: FlextPlugin) -> r[FlextPlugin]:
        """Register plugin with business rule validation."""
        try:
            # Validate plugin name
            if plugin.name in self.RESERVED_PLUGIN_NAMES:
                return r[bool].fail(f"Plugin name '{plugin.name}' is reserved")

            # Check for duplicates
            if plugin.name in self.plugins:
                existing = self.plugins[plugin.name]
                if existing.plugin_version == plugin.plugin_version:
                    return r[bool].fail(f"Plugin {plugin.name} v{plugin.plugin_version} already registered")

            # Validate plugin type limits
            type_count = len([p for p in self.plugins.values() if p.plugin_type == plugin.plugin_type])
            if type_count >= self.MAX_PLUGINS_PER_TYPE:
                return r[bool].fail(f"Maximum plugins of type {plugin.plugin_type} exceeded")

            # Register plugin
            self.plugins[plugin.name] = plugin
            plugin.status = PluginStatus.LOADED

            # Generate registry event
            self.add_domain_event({
                "type": "PluginRegistered",
                "registry_id": str(self.id),
                "plugin_id": str(plugin.id),
                "plugin_name": plugin.name,
                "plugin_type": plugin.plugin_type.value,
                "timestamp": datetime.utcnow().isoformat()
            })

            return r[bool].ok(plugin)

        except Exception as e:
            return r[bool].fail(f"Plugin registration failed: {e}")

    def get_plugins_by_type(self, plugin_type: PluginType) -> List[FlextPlugin]:
        """Get all plugins of specified type."""
        return [p for p in self.plugins.values() if p.plugin_type == plugin_type]

    def get_active_plugins(self) -> List[FlextPlugin]:
        """Get all currently active plugins."""
        return [p for p in self.plugins.values() if p.status == PluginStatus.ACTIVE]

    def get_registry_health(self) -> t.Dict:
        """Get overall registry health metrics."""
        total_plugins = len(self.plugins)
        active_plugins = len(self.get_active_plugins())

        # Calculate health by plugin type
        type_distribution = {}
        for plugin_type in PluginType:
            count = len(self.get_plugins_by_type(plugin_type))
            type_distribution[plugin_type.value] = count

        # Calculate overall health score
        unhealthy_plugins = len([
            p for p in self.plugins.values()
            if p.get_health_status()["health"] == "unhealthy"
        ])

        health_score = (total_plugins - unhealthy_plugins) / total_plugins if total_plugins > 0 else 1.0

        return {
            "total_plugins": total_plugins,
            "active_plugins": active_plugins,
            "type_distribution": type_distribution,
            "health_score": health_score,
            "last_discovery": self.last_discovery.isoformat() if self.last_discovery else None,
            "registry_version": self.registry_version
        }
```

### **Plugin Value Object Patterns**

```python
from flext_plugin import FlextPluginModels.Metadata, FlextPluginModels.Config
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import FlextLogger
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u
from typing import List, Dict, Optional


class FlextPluginModels.Metadata(FlextModels.Value):
    """
    Immutable plugin metadata value t.NormalizedValue.

    Contains descriptive information about the plugin that doesn't
    change frequently and doesn't affect plugin identity.
    """

    description: str
    author: str
    license: str = "MIT"
    homepage_url: Optional[str] = None
    repository_url: Optional[str] = None
    documentation_url: Optional[str] = None
    tags: t.StringList = field(default_factory=list)
    keywords: t.StringList = field(default_factory=list)

    def __post_init__(self):
        """Validate metadata on creation."""
        if not self.description.strip():
            raise ValueError("Plugin description cannot be empty")

        if not self.author.strip():
            raise ValueError("Plugin author cannot be empty")

        # Validate URLs if provided
        for url_field in ["homepage_url", "repository_url", "documentation_url"]:
            url = getattr(self, url_field)
            if url and not self._is_valid_url(url):
                raise ValueError(f"Invalid {url_field}: {url}")

    def has_tag(self, tag: str) -> bool:
        """Check if metadata contains specific tag."""
        return tag.lower() in [t.lower() for t in self.tags]

    def has_keyword(self, keyword: str) -> bool:
        """Check if metadata contains specific keyword."""
        return keyword.lower() in [k.lower() for k in self.keywords]

    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format."""
        return url.startswith(("http://", "https://"))

class FlextPluginModels.Config(FlextModels.Value):
    """
    Immutable plugin configuration value t.NormalizedValue.

    Contains plugin-specific configuration that affects plugin
    behavior but doesn't change plugin identity.
    """

    config_data: t.Dict
    schema_version: str = "0.9.9"
    environment: str = "production"

    def __post_init__(self):
        """Validate configuration on creation."""
        if not isinstance(self.config_data, dict):
            raise ValueError("Config data must be a dictionary")

        # Validate required configuration keys
        required_keys = self._get_required_keys()
        missing_keys = [key for key in required_keys if key not in self.config_data]
        if missing_keys:
            raise ValueError(f"Missing required configuration keys: {missing_keys}")

    def get_value(self, key: str, default = None):
        """Get configuration value with default fallback."""
        return self.config_data.get(key, default)

    def has_key(self, key: str) -> bool:
        """Check if configuration contains specific key."""
        return key in self.config_data

    def with_override(self, overrides: t.Dict) -> 'FlextPluginModels.Config':
        """Create new settings with overridden values."""
        new_config_data = {**self.config_data, **overrides}
        return FlextPluginModels.Config(
            config_data=new_config_data,
            schema_version=self.schema_version,
            environment=self.environment
        )

    def _get_required_keys(self) -> t.StringList:
        """Get required configuration keys based on environment."""
        base_required = ["name", "version"]

        if self.environment == "production":
            return base_required + ["log_level", "metrics_enabled"]
        else:
            return base_required
```

______________________________________________________________________

## 🚀 **Performance & Optimization Patterns**

### **Lazy Plugin Loading**

```python
from functools import cached_property
from typing import Optional, Dict


class LazyPluginLoader:
    """Lazy loading pattern for plugin resources."""

    def __init__(self, plugin_config: t.Dict):
        self.plugin_config = plugin_config
        self._loaded_modules: t.Dict = {}

    @cached_property
    def plugin_module(self) -> r[t.NormalizedValue]:
        """Lazy load plugin module."""
        try:
            module_path = self.plugin_config.get("module_path")
            if not module_path:
                return r[bool].fail("Module path not specified")

            # Dynamic import with caching
            if module_path not in self._loaded_modules:
                module = __import__(module_path, fromlist=[""])
                self._loaded_modules[module_path] = module

            return r[bool].ok(self._loaded_modules[module_path])

        except ImportError as e:
            return r[bool].fail(f"Failed to import plugin module: {e}")

    @cached_property
    def plugin_class(self) -> r[type]:
        """Lazy load plugin class."""
        return self.plugin_module.flat_map(
            lambda module: self._extract_plugin_class(module)
        )

    def create_instance(self, *args, **kwargs) -> r[FlextPlugin]:
        """Create plugin instance with lazy loading."""
        return self.plugin_class.flat_map(
            lambda cls: self._instantiate_plugin(cls, *args, **kwargs)
        )

    def _extract_plugin_class(self, module) -> r[type]:
        """Extract plugin class from module."""
        class_name = self.plugin_config.get("class_name", "Plugin")

        if not hasattr(module, class_name):
            return r[bool].fail(f"Plugin class '{class_name}' not found in module")

        plugin_class = getattr(module, class_name)

        # Validate plugin class
        if not issubclass(plugin_class, FlextPlugin):
            return r[bool].fail(f"Class '{class_name}' is not a FlextPlugin subclass")

        return r[bool].ok(plugin_class)

    def _instantiate_plugin(
        self, plugin_class: type, *args, **kwargs
    ) -> r[FlextPlugin]:
        """Instantiate plugin with error handling."""
        try:
            instance = plugin_class(*args, **kwargs)
            return r[bool].ok(instance)
        except Exception as e:
            return r[bool].fail(f"Failed to instantiate plugin: {e}")
```

### **Plugin Caching Patterns**

```python
from functools import wraps
from typing import Callable, Optional

import hashlib
import json


class PluginCache:
    """Plugin-aware caching system."""

    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.max_size = max_size
        self.ttl = ttl
        self._cache: Dict[str, t.Dict] = {}

    def cache_plugin_result(
        self,
        cache_key_func: Callable[..., str],
        invalidate_on_plugin_change: bool = True,
    ):
        """Decorator for caching plugin operation results."""

        def decorator(func: Callable[..., r[t.NormalizedValue]]):
            @wraps(func)
            def wrapper(*args, **kwargs) -> r[t.NormalizedValue]:
                # Generate cache key
                cache_key = cache_key_func(*args, **kwargs)

                # Check cache first
                cached_result = self._get_cached_result(cache_key)
                if cached_result is not None:
                    return r[bool].ok(cached_result)

                # Execute function
                result = func(*args, **kwargs)

                # Cache successful results
                if result.success:
                    self._cache_result(
                        cache_key,
                        result.data,
                        {"invalidate_on_plugin_change": invalidate_on_plugin_change},
                    )

                return result

            return wrapper

        return decorator

    def invalidate_plugin_cache(self, plugin_id: str) -> None:
        """Invalidate cache entries related to specific plugin."""
        keys_to_remove = []

        for cache_key, cache_entry in self._cache.items():
            metadata = cache_entry.get("metadata", {})
            if metadata.get("invalidate_on_plugin_change") and plugin_id in cache_key:
                keys_to_remove.append(cache_key)

        for key in keys_to_remove:
            del self._cache[key]

    def _get_cached_result(self, cache_key: str) -> Optional[t.NormalizedValue]:
        """Get cached result if still valid."""
        if cache_key not in self._cache:
            return None

        cache_entry = self._cache[cache_key]

        # Check TTL
        import time

        if time.time() - cache_entry["timestamp"] > self.ttl:
            del self._cache[cache_key]
            return None

        return cache_entry["data"]

    def _cache_result(self, cache_key: str, data, metadata: t.Dict) -> None:
        """Cache result with metadata."""
        import time

        # Implement LRU eviction if needed
        if len(self._cache) >= self.max_size:
            oldest_key = min(
                self._cache.keys(), key=lambda k: self._cache[k]["timestamp"]
            )
            del self._cache[oldest_key]

        self._cache[cache_key] = {
            "data": data,
            "timestamp": time.time(),
            "metadata": metadata,
        }


# Usage example
plugin_cache = PluginCache()


@plugin_cache.cache_plugin_result(
    cache_key_func=lambda plugin_id, settings: (
        f"plugin_execution:{plugin_id}:{hash(json.dumps(settings, sort_keys=True))}"
    ),
    invalidate_on_plugin_change=True,
)
def execute_plugin_cached(plugin_id: str, settings: t.Dict) -> r[t.NormalizedValue]:
    """Execute plugin with caching."""
    # Actual plugin execution logic
    pass
```

______________________________________________________________________

## 📏 **Code Quality Standards**

### **Type Annotation Requirements**

```python
# ✅ Complete type annotations for plugin interfaces
from typing import Dict, List, Optional, Callable, Awaitable, Protocol

from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import FlextLogger
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u


class PluginInterface(Protocol):
    """Protocol defining plugin interface with complete type safety."""

    def initialize(self) -> r[bool]:
        """Initialize plugin resources."""
        ...

    def execute(self, data: t.Dict) -> r[t.Dict]:
        """Execute plugin with typed input/output."""
        ...

    def cleanup(self) -> r[bool]:
        """Cleanup plugin resources."""
        ...


# ✅ Generic plugin handler with type safety
T = TypeVar("T")
U = TypeVar("U")


def process_plugin_data(
    plugin: PluginInterface,
    data: t.Dict,
    transformer: Callable[[t.Dict], T],
    validator: Callable[[T], r[U]],
) -> r[U]:
    """Process plugin data with complete type safety."""
    execution_result = plugin.execute(data)

    if execution_result.is_failure:
        return r[bool].fail(execution_result.error)

    try:
        transformed_data = transformer(execution_result.data)
        return validator(transformed_data)
    except Exception as e:
        return r[bool].fail(f"Data processing failed: {e}")


# ❌ Avoid untyped plugin interfaces
def execute_plugin(plugin, data):  # Missing types
    return plugin.execute(data)
```

### **Error Handling Standards**

```python
# ✅ Plugin-specific error handling with r
from flext_plugin import PluginError


def safe_plugin_operation(plugin: FlextPlugin) -> r[bool]:
    """Plugin operation with comprehensive error handling."""
    try:
        # Validate plugin state
        if not plugin.is_valid():
            return r[bool].fail("Plugin is not in valid state")

        # Check plugin dependencies
        dependency_check = validate_plugin_dependencies(plugin)
        if dependency_check.is_failure:
            return dependency_check

        # Execute plugin operation
        result = plugin.execute({})

        if result.is_failure:
            # Log plugin-specific error
            logger.error(
                "Plugin execution failed",
                plugin_name=plugin.name,
                plugin_version=plugin.plugin_version,
                error=result.error,
            )
            return result

        return r[bool].ok(data=True)

    except PluginError as e:
        # Handle plugin-specific errors
        return r[bool].fail(f"Plugin error: {e}")
    except Exception as e:
        # Handle unexpected errors
        logger.exception(
            "Unexpected error in plugin operation", plugin_name=plugin.name
        )
        return r[bool].fail(f"Unexpected error: {e}")


# ✅ Plugin error hierarchy
class PluginError(e.ProcessingError):
    """Base plugin error."""

    pass


class PluginConfigurationError(PluginError):
    """Plugin configuration error."""

    pass


class PluginDependencyError(PluginError):
    """Plugin dependency error."""

    pass


class PluginExecutionError(PluginError):
    """Plugin execution error."""

    pass


# ❌ Avoid raising exceptions in plugin business logic
def bad_plugin_operation(plugin: FlextPlugin) -> None:
    if not plugin.is_valid():
        raise ValueError("Invalid plugin")  # Breaks railway pattern
```

### **Plugin Documentation Standards**

````python
class DataProcessorPlugin(FlextPlugin):
    """
    Data processing plugin with comprehensive business logic.

    This plugin implements advanced data processing capabilities for the FLEXT
    platform, supporting multiple data formats and transformation pipelines.
    It follows Clean Architecture principles and integrates seamlessly with
    the Singer ecosystem for ETL operations.

    Business Capabilities:
        - Multi-format data processing (JSON, CSV, XML, Parquet)
        - Real-time and batch processing modes
        - Custom transformation pipeline support
        - Data validation and quality checks
        - Integration with FLEXT observability

    Architecture Integration:
        - Built on flext-core foundation patterns
        - Uses r for railway-oriented programming
        - Implements domain events for audit trails
        - Supports hot-reload for development workflows

    Configuration:
        The plugin accepts configuration through FlextPluginModels.Config with
        the following structure:

        ```json
        {
            "batch_size": 1000,
            "timeout_seconds": 300,
            "formats": ["json", "csv"],
            "transformations": {
                "normalize_names": true,
                "validate_emails": true,
                "deduplicate": false
            }
        }
        ```

    Example:
        >>> settings = FlextPluginModels.Config({
        ...     "batch_size": 500,
        ...     "formats": ["json"],
        ... })
        >>> plugin = DataProcessorPlugin(settings=settings)
        >>> plugin.initialize()
        >>> result = plugin.execute({"data": [...]})
        >>> if result.success:
        ...     print(f"Processed {len(result.data)} records")

    Singer Integration:
        When used as a Singer transform, the plugin automatically adapts
        to Singer message format and provides schema evolution capabilities:

        >>> # As Singer transform in Meltano
        >>> meltano run tap-source transform-data-processor target-destination

    Performance:
        - Processes up to 10,000 records/second in batch mode
        - Memory usage scales linearly with batch size
        - Supports horizontal scaling through plugin instances

    See Also:
        - FlextPlugin: Base plugin class documentation
        - FlextPluginModels.Config: Configuration pattern documentation
        - Singer Integration Guide: docs/guides/singer-integration.md
    """

    def __init__(
        self,
        settings: Optional[FlextPluginModels.Config] = None,
        metadata: Optional[FlextPluginModels.Metadata] = None,
        **kwargs,
    ) -> None:
        """
        Initialize data processor plugin with configuration.

        Args:
            settings: Plugin-specific configuration with processing parameters.
                   Must include batch_size and timeout_seconds. Optional
                   formats list defaults to ["json", "csv"].
            metadata: Plugin metadata with description, author, and tags.
                     Used for plugin discovery and catalog management.
            **kwargs: Additional arguments passed to FlextPlugin base class.
                     Supports all base plugin initialization parameters.

        Raises:
            PluginConfigurationError: When required configuration is missing
                                    or invalid. Common issues include negative
                                    batch_size or unsupported data formats.

        Example:
            >>> settings = FlextPluginModels.Config({
            ...     "batch_size": 1000,
            ...     "timeout_seconds": 60,
            ...     "formats": ["json", "parquet"],
            ... })
            >>> plugin = DataProcessorPlugin(settings=settings)
        """
        super().__init__(
            name="data-processor",
            version="2.1.0",
            settings=settings,
            metadata=metadata,
            **kwargs,
        )

    def execute(self, data: t.Dict) -> r[t.Dict]:
        """
        Execute data processing pipeline on input data.

        Processes input data through configurable transformation pipeline,
        applying format-specific parsers, validation rules, and business
        logic transformations. Supports both real-time and batch processing
        modes based on configuration.

        Processing Pipeline:
            1. Input validation and format detection
            2. Data parsing and normalization
            3. Business rule application
            4. Quality validation and error handling
            5. Output formatting and metadata generation

        Args:
            data: Input data dictionary with the following structure:
                 - "payload": Main data content (required)
                 - "format": Data format hint ("json", "csv", etc.)
                 - "batch_mode": Boolean for batch vs real-time processing
                 - "metadata": Additional processing metadata (optional)

        Returns:
            r[t.Dict]: Processing results containing:
                - "processed_data": Transformed data in requested format
                - "statistics": Processing metrics (records, errors, timing)
                - "metadata": Output metadata with schema information
                - "quality_report": Data quality assessment results

            On failure, contains detailed error information including:
                - Error type and description
                - Failed processing step
                - Input data characteristics
                - Suggested remediation actions

        Raises:
            PluginExecutionError: Never raised directly. All errors are
                                 wrapped in r for railway-oriented
                                 programming compatibility.

        Performance:
            - Batch mode: 10,000+ records/second
            - Real-time mode: <100ms latency per request
            - Memory usage: O(batch_size) linear scaling
            - CPU usage: Optimized for multi-core processing

        Example:
            >>> input_data = {
            ...     "payload": [
            ...         {"name": "John Doe", "email": "john@example.com"},
            ...         {"name": "Jane Smith", "email": "jane@example.com"},
            ...     ],
            ...     "format": "json",
            ...     "batch_mode": True,
            ... }
            >>> result = plugin.execute(input_data)
            >>> if result.success:
            ...     stats = result.data["statistics"]
            ...     print(f"Processed {stats['records_processed']} records")
            ...     print(f"Processing time: {stats['processing_time']}s")
        """
        # Implementation follows...
````

______________________________________________________________________

## 📋 **Checklist for Plugin Module Creation**

### **Plugin Module Creation Checklist**

- [ ] **Naming**: Uses `flext_plugin.*` namespace following conventions
- [ ] **Location**: Placed in appropriate Clean Architecture layer
- [ ] **Imports**: Only imports from same or lower layers, uses flext-core patterns
- [ ] **Types**: Complete type annotations with PluginType and PluginStatus
- [ ] **Error Handling**: Uses r for all plugin operations
- [ ] **Lifecycle**: Implements initialize(), execute(), cleanup() pattern
- [ ] **Documentation**: Comprehensive docstrings with plugin-specific examples
- [ ] **Tests**: 85% coverage minimum with plugin lifecycle testing
- [ ] **Exports**: Added to appropriate `__init__.py` if public API
- [ ] **Hot Reload**: Compatible with hot-reload system requirements
- [ ] **Singer Support**: Integration patterns for Singer ecosystem if applicable

### **Plugin Quality Gate Checklist**

- [ ] **Linting**: `make lint` passes (Ruff with ALL rules enabled)
- [ ] **Type Check**: `make type-check` passes (strict MyPy, 95%+ coverage)
- [ ] **Tests**: `make test` passes (85% coverage minimum for plugins)
- [ ] **Security**: `make security` passes (Bandit + pip-audit)
- [ ] **Plugin Validation**: `make plugin-validate` passes
- [ ] **Hot Reload**: Plugin supports hot-reload without state loss
- [ ] **Integration**: Works with FlexCore and FLEXT Service integration
- [ ] **Documentation**: Plugin-specific documentation added to docs/
- [ ] **Examples**: Working plugin examples in examples/ directory

### **Plugin-Specific Validation**

- [ ] **Plugin Interface**: Implements required plugin interface methods
- [ ] **Status Management**: Proper PluginStatus transitions and validation
- [ ] **Configuration**: Uses FlextPluginModels.Config pattern with validation
- [ ] **Metadata**: Complete FlextPluginModels.Metadata with discovery information
- [ ] **Dependencies**: Properly declared plugin dependencies
- [ ] **Events**: Domain events for plugin lifecycle and execution
- [ ] **Registry**: Compatible with FlextPluginModels.Registry management
- [ ] **Discovery**: Discoverable through plugin discovery system
- [ ] **Platform**: Integrates with FlextPluginPlatform orchestration

______________________________________________________________________

## 🌐 **FLEXT Ecosystem Integration Guidelines**

### **Cross-Project Plugin Standards**

```python
# ✅ Standard plugin creation across ecosystem projects
from flext_plugin import create_flext_plugin
from flext_plugin import PluginType
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import FlextLogger
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u


# Oracle WMS plugin (flext-oracle-wms project)
def create_oracle_wms_plugin(settings: t.Dict) -> r[FlextPlugin]:
    """Create Oracle WMS plugin following ecosystem standards."""
    return r[bool].ok(
        create_flext_plugin(
            name="oracle-wms-connector",
            version="0.9.9",
            plugin_type=PluginType.DATABASE,
            settings={
                **settings,
                "description": "Oracle WMS database connector plugin",
                "dependencies": ["flext-core>=0.9.9", "flext-db-oracle>=0.9.9"],
            },
        )
    )


# Singer tap plugin (flext-tap-oracle project)
def create_oracle_tap_plugin(tap_config: t.Dict) -> r[FlextPlugin]:
    """Create Oracle Singer tap plugin."""
    return r[bool].ok(
        create_flext_plugin(
            name=f"tap-oracle-{tap_config.get('schema', 'default')}",
            version="0.9.9",
            plugin_type=PluginType.TAP,
            settings={
                **tap_config,
                "singer_spec": "0.9.9",
                "description": f"Oracle tap for {tap_config.get('schema')} schema",
            },
        )
    )


# ❌ Don't create custom plugin systems per project
class OracleCustomPlugin:  # Creates ecosystem fragmentation
    pass
```

### **Plugin Configuration Integration**

```python
# ✅ Extend plugin configuration patterns consistently
from flext_plugin import PluginSystemSettings
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import FlextLogger
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u


class OraclePluginSettings(FlextSettings):
    """Oracle plugin configuration extending FLEXT patterns."""

    connection_string: str
    schema: str = "HR"
    pool_size: int = 10
    timeout: int = 30

    class Config:
        env_prefix = "ORACLE_PLUGIN_"


class ProjectPluginConfig(PluginSystemSettings):
    """Project plugin configuration composing ecosystem settings."""

    oracle: OraclePluginSettings = field(default_factory=OraclePluginSettings)
    ldap: LdapPluginSettings = field(default_factory=LdapPluginSettings)

    # Inherit base plugin settings
    # discovery_paths, hot_reload_enabled, etc.
```

### **Plugin Registry Integration**

```python
# ✅ Use centralized plugin registry across ecosystem
from flext_plugin import FlextPluginModels.Registry
from flext_plugin import create_flext_plugin_platform

class EcosystemPluginManager:
    """Centralized plugin management for FLEXT ecosystem."""

    def __init__(self):
        self.platform = create_flext_plugin_platform()
        self.registry = self.platform.registry

    def register_ecosystem_plugins(self) -> r[t.StringList]:
        """Register plugins from all ecosystem projects."""
        plugin_sources = [
            "./flext-tap-oracle/plugins",
            "./flext-target-oracle/plugins",
            "./flext-db-oracle/plugins",
            "./flext-ldap/plugins",
            "./flext-api/plugins"
        ]

        registered_plugins = []

        for source_path in plugin_sources:
            discovery_result = self.platform.discover_plugins(source_path)
            if discovery_result.success:
                for plugin in discovery_result.data:
                    register_result = self.registry.register_plugin(plugin)
                    if register_result.success:
                        registered_plugins.append(plugin.name)

        return r[bool].ok(registered_plugins)
```

______________________________________________________________________

**Last Updated**: August 3, 2025
**Target Audience**: FLEXT Plugin developers and ecosystem contributors
**Scope**: Python module organization for plugin system development
**Version**: 0.9.9 RC → 0.9.9 development guidelines for plugin architecture
