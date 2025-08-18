# FLEXT Plugin Domain Module

**Rich business entities and domain logic for plugin management following Domain-Driven Design principles.**

This module implements the domain layer of the Clean Architecture, containing entities that encapsulate business rules, maintain consistency boundaries, and provide the core abstractions for plugin management operations.

## Module Contents

### Core Entities

#### `FlextPlugin`

Primary plugin entity with comprehensive business logic.

```python
from flext_plugin.domain.entities import FlextPlugin
ddddddd
plugin = FlextPlugin(
    name="data-processor",
    version="1.0.0",
    config={
        "description": "Advanced data processing plugin",
        "author": "FLEXT Team"
    }
)

# Business operations
result = plugin.activate()
if result.success():
    print(f"Plugin {plugin.name} is now active")
```

**Key Features:**

- **Lifecycle Management**: Full plugin lifecycle with state transitions
- **Business Rules**: Domain rule enforcement and validation
- **Domain Events**: Event generation for plugin operations
- **Type Safety**: Complete type annotations with Pydantic integration

**Business Rules:**

- Plugin names must be unique within a registry
- Version strings follow semantic versioning
- Status transitions follow defined lifecycle rules
- Configuration changes require validation

#### `FlextPluginConfig`

Plugin configuration entity with validation and change tracking.

```python
from flext_plugin.domain.entities import FlextPluginConfig

config = FlextPluginConfig(
    plugin_id="data-processor",
    config_data={
        "batch_size": 1000,
        "timeout": 30,
        "enabled_features": ["validation", "caching"]
    }
)

# Configuration management
result = config.update_config({"batch_size": 2000})
value = config.get_config_value("timeout", default=60)
```

**Features:**

- **Change Tracking**: Automatic timestamp updates
- **Validation**: Configuration schema validation
- **Version Management**: Configuration versioning
- **Audit Trail**: Change history maintenance

#### `FlextPluginMetadata`

Plugin descriptive information and external references.

```python
from flext_plugin.domain.entities import FlextPluginMetadata

metadata = FlextPluginMetadata(
    plugin_id="data-processor",
    tags=["data", "processing", "enterprise"],
    homepage_url="https://github.com/flext-sh/flext",
    license="MIT",
    keywords=["etl", "data", "plugin"]
)

# Metadata operations
if metadata.has_tag("enterprise"):
    print("Enterprise plugin detected")

metadata_updated = metadata.add_tag("production-ready")
```

**Attributes:**

- **Tags**: Categorization and discovery tags
- **URLs**: Homepage, repository, documentation links
- **License**: Software license information
- **Keywords**: Search and discovery keywords

#### `FlextPluginRegistry`

Aggregate root managing plugin collections with consistency rules.

```python
from flext_plugin.domain.entities import FlextPluginRegistry

registry = FlextPluginRegistry(
    discovery_paths=["./plugins", "~/.flext/plugins"]
)

# Registry operations
result = await registry.register_plugin(plugin)
active_plugins = registry.get_active_plugins()
plugin_count = registry.get_plugin_count()

# Health monitoring
health = registry.get_registry_health()
print(f"Registry health score: {health['health_score']}")
```

**Key Responsibilities:**

- **Plugin Registration**: Centralized plugin management
- **Consistency Boundaries**: Domain rule enforcement
- **Discovery Coordination**: Plugin scanning and validation
- **Health Monitoring**: Registry-wide health metrics

### Domain Ports

#### Plugin Management Interfaces

Abstract interfaces defining plugin system contracts.

```python
from flext_plugin.domain.ports import (
    FlextPluginManagerPort,
    FlextPluginLoaderPort,
    FlextPluginDiscoveryPort
)

# Interface implementations provide concrete behavior
class MyPluginManager(FlextPluginManagerPort):
    async def register_plugin(self, plugin: FlextPlugin) -> FlextResult[FlextPlugin]:
        # Implementation
        pass
```

**Available Ports:**

- **FlextPluginManagerPort**: Plugin lifecycle management interface
- **FlextPluginLoaderPort**: Plugin loading and unloading interface
- **FlextPluginDiscoveryPort**: Plugin discovery and scanning interface

## Domain-Driven Design Patterns

### Entity Patterns

#### Rich Domain Model

Entities contain business logic, not just data:

```python
class FlextPlugin(FlextEntity):
    def activate(self) -> FlextResult[bool]:
        """Business operation with domain validation."""
        if self.status == PluginStatus.ACTIVE:
            return FlextResult.fail("Plugin already active")

        # Business logic and domain event generation
        self.status = PluginStatus.ACTIVE
        self.add_domain_event({
            "type": "PluginActivated",
            "plugin_id": str(self.id),
            "timestamp": datetime.utcnow().isoformat()
        })
        return FlextResult.ok(True)
```

#### Identity and Equality

Entities have unique identity and proper equality semantics:

```python
plugin1 = FlextPlugin(name="test", version="1.0.0")
plugin2 = FlextPlugin(name="test", version="1.0.0")

# Entity identity is based on ID, not values
assert plugin1.id != plugin2.id
assert plugin1 != plugin2  # Different entities
```

### Aggregate Patterns

#### Consistency Boundaries

Aggregates maintain consistency within their boundaries:

```python
class FlextPluginRegistry(FlextEntity):
    async def register_plugin(self, plugin: FlextPlugin) -> FlextResult[FlextPlugin]:
        """Enforce business rules across the aggregate."""
        # Validate uniqueness
        if plugin.name in self.plugins:
            return FlextResult.fail(f"Plugin {plugin.name} already registered")

        # Enforce limits
        if len(self.plugins) >= self.MAX_PLUGINS:
            return FlextResult.fail("Maximum plugin limit reached")

        # Register and generate events
        self.plugins[plugin.name] = plugin
        self.add_domain_event({
            "type": "PluginRegistered",
            "plugin_name": plugin.name
        })
        return FlextResult.ok(plugin)
```

### Value Object Patterns

Configuration and metadata as immutable value objects:

```python
from flext_plugin.domain.value_objects import FlextPluginConfig

# Immutable configuration
config = FlextPluginConfig(
    config_data={"timeout": 30},
    environment="production"
)

# Changes create new instances
updated_config = config.with_override({"timeout": 60})
assert config.get_value("timeout") == 30  # Original unchanged
assert updated_config.get_value("timeout") == 60  # New instance
```

## Business Rules and Validation

### Plugin Lifecycle Rules

```python
def validate_status_transition(current: PluginStatus, target: PluginStatus) -> bool:
    """Validate plugin status transitions according to business rules."""
    valid_transitions = {
        PluginStatus.DISCOVERED: [PluginStatus.LOADED, PluginStatus.ERROR],
        PluginStatus.LOADED: [PluginStatus.ACTIVE, PluginStatus.INACTIVE],
        PluginStatus.ACTIVE: [PluginStatus.INACTIVE, PluginStatus.ERROR],
        PluginStatus.INACTIVE: [PluginStatus.ACTIVE, PluginStatus.DISABLED]
    }
    return target in valid_transitions.get(current, [])
```

### Plugin Registry Rules

```python
class PluginRegistryRules:
    """Business rules for plugin registry operations."""

    MAX_PLUGINS_PER_TYPE = 100
    RESERVED_NAMES = ["system", "core", "REDACTED_LDAP_BIND_PASSWORD"]

    @staticmethod
    def validate_plugin_name(name: str) -> FlextResult[bool]:
        """Validate plugin name against business rules."""
        if not name or not name.strip():
            return FlextResult.fail("Plugin name cannot be empty")

        if name.lower() in PluginRegistryRules.RESERVED_NAMES:
            return FlextResult.fail(f"Plugin name '{name}' is reserved")

        return FlextResult.ok(True)
```

## Event Sourcing Integration

### Domain Events

Entities generate domain events for important business operations:

```python
# Plugin activation generates domain event
result = plugin.activate()
if result.success():
    events = plugin.get_domain_events()
    for event in events:
        await event_bus.publish(event)
```

**Common Events:**

- `PluginRegistered`: Plugin added to registry
- `PluginActivated`: Plugin became active
- `PluginDeactivated`: Plugin became inactive
- `PluginConfigChanged`: Plugin configuration updated
- `PluginError`: Plugin encountered error

### Event Handlers

```python
from flext_core.events import DomainEventHandler

class PluginActivatedHandler(DomainEventHandler):
    async def handle(self, event: dict) -> None:
        """Handle plugin activation events."""
        plugin_id = event["plugin_id"]

        # Update monitoring systems
        await metrics_service.record_plugin_activation(plugin_id)

        # Send notifications
        await notification_service.notify_plugin_activated(plugin_id)
```

## Testing Patterns

### Entity Testing

```python
import pytest
from flext_plugin.domain.entities import FlextPlugin

class TestFlextPlugin:
    def test_plugin_activation_success(self):
        """Test successful plugin activation."""
        plugin = FlextPlugin(name="test", version="1.0.0")

        result = plugin.activate()

        assert result.success()
        assert plugin.status == PluginStatus.ACTIVE
        assert len(plugin.get_domain_events()) == 1

    def test_plugin_activation_already_active(self):
        """Test activation of already active plugin."""
        plugin = FlextPlugin(name="test", version="1.0.0")
        plugin.status = PluginStatus.ACTIVE

        result = plugin.activate()

        assert result.is_failure()
        assert "already active" in result.error.lower()
```

### Aggregate Testing

```python
class TestFlextPluginRegistry:
    async def test_plugin_registration_success(self):
        """Test successful plugin registration."""
        registry = FlextPluginRegistry()
        plugin = FlextPlugin(name="test", version="1.0.0")

        result = await registry.register_plugin(plugin)

        assert result.success()
        assert plugin.name in registry.plugins
        assert registry.get_plugin_count() == 1

    async def test_duplicate_plugin_registration(self):
        """Test duplicate plugin registration fails."""
        registry = FlextPluginRegistry()
        plugin1 = FlextPlugin(name="test", version="1.0.0")
        plugin2 = FlextPlugin(name="test", version="2.0.0")

        await registry.register_plugin(plugin1)
        result = await registry.register_plugin(plugin2)

        assert result.is_failure()
        assert "already registered" in result.error.lower()
```

## Architecture Integration

### Clean Architecture Layers

```
Platform Layer → Application Layer → Domain Layer (THIS MODULE) → Core Layer
```

### Dependencies

**Inbound Dependencies (users of this module):**

- Application services layer
- Infrastructure adapters
- Platform integration layer

**Outbound Dependencies (dependencies of this module):**

- flext-core foundation patterns
- Core types and enumerations
- Base entity and value object patterns

### Integration Patterns

```python
# Application layer uses domain entities
from flext_plugin.domain.entities import FlextPlugin, FlextPluginRegistry
from flext_plugin.application.services import FlextPluginService

class PluginManagementWorkflow:
    def __init__(self, registry: FlextPluginRegistry):
        self.registry = registry

    async def deploy_plugin(self, plugin_config: dict) -> FlextResult[FlextPlugin]:
        """Complete plugin deployment workflow."""
        plugin = FlextPlugin(**plugin_config)

        # Domain operations
        registration_result = await self.registry.register_plugin(plugin)
        if registration_result.is_failure():
            return registration_result

        activation_result = plugin.activate()
        return activation_result.map(lambda _: plugin)
```

---

**Next Steps**: Explore the [Application Services](../application/README.md) that orchestrate these domain entities, or review the [Core Types](../core/README.md) that provide the foundation for these domain models.
