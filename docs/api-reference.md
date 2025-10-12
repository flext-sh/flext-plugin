# API Reference

**FLEXT Plugin System API Reference**

---

## Core Classes

### FlextPluginPlatform

Main facade for all plugin operations.

```python
class FlextPluginPlatform:
    """Unified plugin management platform"""

    def __init__(self, container: FlextCore.Container | None = None) -> None:
        """Initialize platform with dependency injection container"""

    # Plugin Lifecycle
    def load_plugin(self, plugin: FlextPluginEntities.Entity) -> FlextCore.Result[bool]:
        """Load a plugin into the system"""

    def unload_plugin(self, plugin_name: str) -> FlextCore.Result[bool]:
        """Unload a plugin from the system"""

    def enable_plugin(self, plugin_name: str) -> FlextCore.Result[bool]:
        """Enable an already loaded plugin"""

    def disable_plugin(self, plugin_name: str) -> FlextCore.Result[bool]:
        """Disable an active plugin"""

    # Plugin Management
    def install_plugin(self, plugin_path: str) -> FlextCore.Result[FlextPluginEntities.Entity]:
        """Install a plugin from file system path"""

    def uninstall_plugin(self, plugin_name: str) -> FlextCore.Result[bool]:
        """Uninstall a plugin completely"""

    def is_plugin_loaded(self, plugin_name: str) -> FlextCore.Result[bool]:
        """Check if plugin is currently loaded"""

    # Discovery
    def scan_directory(self, directory_path: str) -> FlextCore.Result[list[FlextPluginEntities.Entity]]:
        """Scan directory for plugins"""

    def validate_plugin(self, plugin: FlextPluginEntities.Entity) -> FlextCore.Result[bool]:
        """Validate plugin integrity and requirements"""

    # Configuration
    def get_plugin_config(self, plugin_name: str) -> FlextCore.Result[FlextPluginEntities.Config]:
        """Get plugin configuration"""

    def update_plugin_config(self, plugin_name: str, config: FlextPluginEntities.Config) -> FlextCore.Result[bool]:
        """Update plugin configuration"""
```

### FlextPlugin (Entity)

Core plugin domain entity.

```python
class FlextPlugin(FlextCore.Models.Entity):
    """Plugin entity with business rules"""

    # Properties
    name: str                           # Plugin identifier
    plugin_version: str                 # Plugin version
    status: PluginStatus               # Current lifecycle status
    config: FlextCore.Types.Dict             # Plugin configuration
    metadata: FlextPluginEntities.Metadata      # Plugin metadata

    # Business Methods
    def activate(self) -> bool:
        """Activate plugin (business rule: must be loaded first)"""

    def deactivate(self) -> bool:
        """Deactivate plugin"""

    def validate_business_rules(self) -> FlextCore.Result[bool]:
        """Validate plugin business rules"""
```

### FlextPluginEntities.Config (Entity)

Plugin configuration entity.

```python
class FlextPluginEntities.Config(FlextCore.Models.Entity):
    """Plugin configuration with validation"""

    name: str                          # Plugin name
    version: str                       # Plugin version
    description: str                   # Plugin description
    author: str                        # Plugin author
    dependencies: FlextCore.Types.StringList            # Plugin dependencies
    metadata: FlextPluginEntities.Metadata      # Additional metadata

    def validate_business_rules(self) -> FlextCore.Result[bool]:
        """Validate configuration business rules"""
```

---

## Enumerations

### PluginStatus

```python
class PluginStatus(str, Enum):
    """Plugin lifecycle status"""
    INACTIVE = "INACTIVE"              # Plugin created but not loaded
    LOADED = "LOADED"                  # Plugin loaded but not active
    ACTIVE = "ACTIVE"                  # Plugin active and running
    ERROR = "ERROR"                    # Plugin in error state
```

### PluginType

```python
class PluginType(str, Enum):
    """Plugin type classification"""
    UTILITY = "UTILITY"                # General utility plugin
    SERVICE = "SERVICE"                # Service plugin
    MIDDLEWARE = "MIDDLEWARE"          # Middleware plugin
    TAP = "TAP"                       # Singer tap plugin
    TARGET = "TARGET"                 # Singer target plugin
    TRANSFORM = "TRANSFORM"           # DBT transform plugin
```

---

## Factory Functions

### create_flext_plugin

```python
def create_flext_plugin(
    name: str,
    version: str,
    config: FlextCore.Types.Dict | None = None,
    plugin_type: PluginType = PluginType.UTILITY,
    **kwargs
) -> FlextPluginEntities.Entity:
    """Create a new plugin entity"""
```

### create_flext_plugin_platform

```python
def create_flext_plugin_platform(
    config: FlextCore.Types.Dict | None = None
) -> FlextPluginPlatform:
    """Create configured plugin platform"""
```

---

## Discovery Services

### FlextPluginDiscoveryService

```python
class FlextPluginDiscoveryService:
    """Plugin discovery and validation service"""

    def scan_directory(self, path: str) -> FlextCore.Result[list[FlextPluginEntities.Entity]]:
        """Scan directory for plugins"""

    def validate_plugin_integrity(self, plugin: FlextPluginEntities.Entity) -> FlextCore.Result[bool]:
        """Validate plugin integrity"""
```

---

## Hot Reload

### Hot Reload Configuration

```python
# Environment variables for hot reload
FLEXT_PLUGIN_HOT_RELOAD=true          # Enable hot reload
FLEXT_PLUGIN_WATCH_INTERVAL=2         # Watch interval in seconds
```

---

## Error Handling

All API methods return `FlextCore.Result[T]` for consistent error handling:

```python
result = platform.load_plugin(plugin)
if result.success:
    # Plugin loaded successfully
    plugin_data = result.data
else:
    # Handle error
    error_message = result.error
    print(f"Failed to load plugin: {error_message}")
```

### Exception Types

```python
class FlextPluginError(Exception):
    """Base plugin system error"""

class FlextPluginConfigurationError(FlextPluginError):
    """Plugin configuration error"""

class FlextPluginLoadingError(FlextPluginError):
    """Plugin loading error"""

class FlextPluginExecutionError(FlextPluginError):
    """Plugin execution error"""
```

---

## Integration Patterns

### FLEXT-Core Integration

```python
# Use FlextCore.Result for all operations
from flext_core import FlextCore

def plugin_operation() -> FlextCore.Result[bool]:
    try:
        # Plugin operation
        return FlextCore.Result[bool].ok(True)
    except Exception as e:
        return FlextCore.Result[bool].fail(str(e))

# Use dependency injection
from flext_core import FlextCore

container = FlextCore.Container()
platform = FlextPluginPlatform(container)
```

### Singer Integration

```python
# Singer tap plugin example
from flext_plugin import FlextPlugin, PluginType

class MyTapPlugin(FlextPlugin):
    def __init__(self, **kwargs):
        super().__init__(
            name="tap-my-source",
            version="0.9.9",
            config={"plugin_type": PluginType.TAP},
            **kwargs
        )
```

---

## Usage Examples

### Basic Plugin Management

```python
from flext_plugin import FlextPluginPlatform, create_flext_plugin

# Create platform
platform = FlextPluginPlatform()

# Create and load plugin
plugin = create_flext_plugin("my-plugin", "0.9.9")
result = platform.load_plugin(plugin)

if result.success:
    # Enable plugin
    enable_result = platform.enable_plugin("my-plugin")
    if enable_result.success:
        print("Plugin ready for use")
```

### Plugin Discovery

```python
# Discover plugins in directory
discovery_result = platform.scan_directory("./plugins")
if discovery_result.success:
    for plugin in discovery_result.data:
        print(f"Found: {plugin.name} v{plugin.plugin_version}")

        # Validate each plugin
        validation = platform.validate_plugin(plugin)
        if validation.success:
            print(f"  ✓ Valid plugin")
        else:
            print(f"  ✗ Invalid: {validation.error}")
```

---

For complete examples and usage patterns, see the [examples/](examples/) directory.
