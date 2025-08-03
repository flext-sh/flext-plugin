# FLEXT Plugin API Reference

Complete API reference for the FLEXT Plugin system, covering all public interfaces, classes, and functions.

## Core APIs

### Platform API

The main entry point for plugin management operations.

```python
from flext_plugin import FlextPluginPlatform, create_flext_plugin_platform

# Create platform instance
platform = create_flext_plugin_platform(config={"debug": True})

# Platform operations
await platform.register_plugin(plugin)
await platform.activate_plugin("plugin-name")
result = await platform.execute_plugin("plugin-name", data)
```

**Key Methods:**
- `register_plugin(plugin)` - Register new plugin
- `activate_plugin(plugin_id)` - Activate registered plugin
- `deactivate_plugin(plugin_id)` - Deactivate active plugin
- `execute_plugin(plugin_id, data)` - Execute plugin with data
- `get_plugin(plugin_id)` - Retrieve plugin by ID
- `list_plugins(filter_criteria)` - List plugins with filtering

### Simple API

Factory functions for easy plugin creation and management.

```python
from flext_plugin import (
    create_flext_plugin,
    create_flext_plugin_config,
    create_flext_plugin_metadata,
    create_flext_plugin_registry
)

# Create plugin with factory function
plugin = create_flext_plugin(
    name="my-plugin",
    version="1.0.0",
    plugin_type=PluginType.SERVICE
)
```

**Factory Functions:**
- `create_flext_plugin()` - Create plugin entity
- `create_flext_plugin_config()` - Create plugin configuration
- `create_flext_plugin_metadata()` - Create plugin metadata
- `create_flext_plugin_registry()` - Create plugin registry
- `create_flext_plugin_platform()` - Create platform instance

## Core Types

### Plugin Enums

```python
from flext_plugin.core.types import PluginStatus, PluginType

# Plugin lifecycle states
class PluginStatus(Enum):
    UNKNOWN = "unknown"
    DISCOVERED = "discovered"
    LOADED = "loaded"
    ACTIVE = "active"
    INACTIVE = "inactive"
    LOADING = "loading"
    ERROR = "error"
    DISABLED = "disabled"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"

# Plugin categories
class PluginType(Enum):
    # Singer ETL types
    TAP = "tap"
    TARGET = "target"
    TRANSFORM = "transform"
    
    # Architecture types
    EXTENSION = "extension"
    SERVICE = "service"
    MIDDLEWARE = "middleware"
    TRANSFORMER = "transformer"
    
    # Integration types
    API = "api"
    DATABASE = "database"
    NOTIFICATION = "notification"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    
    # Utility types
    UTILITY = "utility"
    TOOL = "tool"
    HANDLER = "handler"
    PROCESSOR = "processor"
    
    # System types
    CORE = "core"
    ADDON = "addon"
    THEME = "theme"
    LANGUAGE = "language"
```

### Result Objects

```python
from flext_plugin.core.types import PluginExecutionResult, PluginExecutionContext

# Plugin execution result
class PluginExecutionResult:
    success: bool
    data: object
    error: str
    plugin_name: str
    execution_time: float
    
    def is_success(self) -> bool
    def is_failure(self) -> bool

# Plugin execution context
class PluginExecutionContext:
    plugin_id: str
    execution_id: str
    input_data: dict[str, object]
    context: dict[str, object]
    timeout_seconds: int | None
```

### Error Handling

```python
from flext_plugin.core.types import PluginError

class PluginError(FlextProcessingError):
    """Base exception for plugin-related errors."""
    
    def __init__(
        self,
        message: str,
        plugin_name: str = "",
        plugin_id: str = "",
        **kwargs: object
    ):
        super().__init__(message, **kwargs)
        self.plugin_name = plugin_name
        self.plugin_id = plugin_id
```

## Domain Entities

### FlextPlugin

The core plugin entity with lifecycle management.

```python
from flext_plugin.domain.entities import FlextPlugin
from flext_core import FlextEntity, FlextEntityId

class FlextPlugin(FlextEntity):
    """Plugin entity representing a plugin in the system."""
    
    # Core attributes
    name: str
    plugin_version: str
    description: str
    author: str
    status: PluginStatus
    
    def __init__(
        self,
        entity_id: FlextEntityId | None = None,
        *,
        name: str = "",
        version: str = "",
        config: dict[str, object] | None = None,
        metadata: object = None,
        **kwargs: object
    ):
        """Initialize plugin entity."""
    
    # Lifecycle methods
    def activate(self) -> bool:
        """Activate the plugin."""
    
    def deactivate(self) -> bool:
        """Deactivate the plugin."""
    
    def is_valid(self) -> bool:
        """Validate plugin entity state."""
    
    # Properties
    @property
    def plugin_name(self) -> str:
        """Get plugin name (compatibility)."""
    
    def get_version(self) -> str:
        """Get plugin version (compatibility)."""
    
    @property
    def plugin_status(self) -> PluginStatus:
        """Get plugin status (compatibility)."""
```

### FlextPluginConfig

Configuration management for plugins.

```python
from flext_plugin.domain.entities import FlextPluginConfig

class FlextPluginConfig(FlextEntity):
    """Plugin configuration entity with update tracking."""
    
    plugin_id: str
    config_data: dict[str, object]
    created_at: datetime
    updated_at: datetime
    version: str
    
    def update_config(
        self, 
        new_config: dict[str, object]
    ) -> FlextResult[bool]:
        """Update configuration with validation."""
    
    def get_config_value(
        self, 
        key: str, 
        default: object = None
    ) -> object:
        """Get configuration value by key."""
    
    def validate_config(self) -> FlextResult[bool]:
        """Validate configuration against schema."""
```

### FlextPluginMetadata

Additional plugin information and metadata.

```python
from flext_plugin.domain.entities import FlextPluginMetadata

class FlextPluginMetadata(FlextEntity):
    """Plugin metadata entity with tags and additional information."""
    
    plugin_id: str
    tags: list[str]
    homepage_url: str
    repository_url: str
    documentation_url: str
    license: str
    keywords: list[str]
    dependencies: list[str]
    
    def add_tag(self, tag: str) -> FlextResult[bool]:
        """Add tag to plugin metadata."""
    
    def remove_tag(self, tag: str) -> FlextResult[bool]:
        """Remove tag from plugin metadata."""
    
    def has_tag(self, tag: str) -> bool:
        """Check if plugin has specific tag."""
    
    def update_urls(self, urls: dict[str, str]) -> FlextResult[bool]:
        """Update plugin URLs (homepage, repository, docs)."""
```

### FlextPluginRegistry

Plugin collection management with discovery and lifecycle operations.

```python
from flext_plugin.domain.entities import FlextPluginRegistry

class FlextPluginRegistry(FlextEntity):
    """Plugin registry aggregate managing collection of plugins."""
    
    plugins: dict[str, FlextPlugin]
    discovery_paths: list[str]
    last_discovery: datetime
    
    # Registration operations
    async def register_plugin(
        self, 
        plugin: FlextPlugin
    ) -> FlextResult[FlextPlugin]:
        """Register plugin with validation and conflict resolution."""
    
    async def unregister_plugin(
        self, 
        plugin_id: str
    ) -> FlextResult[bool]:
        """Unregister plugin and cleanup resources."""
    
    # Query operations
    def get_plugin(self, plugin_id: str) -> FlextPlugin | None:
        """Get plugin by ID."""
    
    def list_plugins(
        self, 
        plugin_type: PluginType | None = None,
        status: PluginStatus | None = None
    ) -> list[FlextPlugin]:
        """List plugins with optional filtering."""
    
    def get_plugin_count(self) -> int:
        """Get total number of registered plugins."""
    
    # Discovery operations  
    async def discover_plugins(
        self, 
        paths: list[str] | None = None
    ) -> FlextResult[list[FlextPlugin]]:
        """Discover plugins in specified paths."""
    
    async def refresh_discovery(self) -> FlextResult[int]:
        """Refresh plugin discovery in all configured paths."""
    
    # Lifecycle operations
    async def activate_all_plugins(self) -> FlextResult[list[str]]:
        """Activate all registered plugins."""
    
    async def deactivate_all_plugins(self) -> FlextResult[list[str]]:
        """Deactivate all active plugins."""
    
    async def cleanup_all(self) -> None:
        """Cleanup all plugins and registry resources."""
```

## Application Services

### FlextPluginService

Core plugin management service with business logic.

```python
from flext_plugin.application.services import FlextPluginService

class FlextPluginService:
    """Core plugin management service."""
    
    def __init__(self, registry: FlextPluginRegistry):
        """Initialize service with plugin registry."""
    
    # Plugin lifecycle management
    async def create_plugin(
        self, 
        config: dict[str, object]
    ) -> FlextResult[FlextPlugin]:
        """Create new plugin with validation."""
    
    async def activate_plugin(
        self, 
        plugin_id: str
    ) -> FlextResult[bool]:
        """Activate plugin with lifecycle management."""
    
    async def deactivate_plugin(
        self, 
        plugin_id: str
    ) -> FlextResult[bool]:
        """Deactivate plugin with cleanup."""
    
    async def execute_plugin(
        self,
        plugin_id: str,
        data: dict[str, object],
        context: dict[str, object] | None = None
    ) -> FlextResult[PluginExecutionResult]:
        """Execute plugin with data and context."""
    
    # Plugin information
    async def get_plugin_info(
        self, 
        plugin_id: str
    ) -> FlextResult[dict[str, object]]:
        """Get comprehensive plugin information."""
    
    async def get_plugin_status(
        self, 
        plugin_id: str
    ) -> FlextResult[PluginStatus]:
        """Get current plugin status."""
    
    async def list_active_plugins(self) -> FlextResult[list[FlextPlugin]]:
        """List all currently active plugins."""
    
    # Configuration management
    async def update_plugin_config(
        self,
        plugin_id: str,
        config: dict[str, object]
    ) -> FlextResult[bool]:
        """Update plugin configuration."""
    
    async def validate_plugin_config(
        self,
        plugin_id: str,
        config: dict[str, object]
    ) -> FlextResult[bool]:
        """Validate plugin configuration."""
```

### FlextPluginDiscoveryService

Plugin discovery and scanning service.

```python
from flext_plugin.application.services import FlextPluginDiscoveryService

class FlextPluginDiscoveryService:
    """Plugin discovery and scanning service."""
    
    # Discovery operations
    async def discover_plugins(
        self, 
        path: str
    ) -> FlextResult[list[FlextPlugin]]:
        """Discover plugins in specified path."""
    
    async def discover_plugins_recursive(
        self,
        root_path: str,
        max_depth: int = 3
    ) -> FlextResult[list[FlextPlugin]]:
        """Recursively discover plugins in directory tree."""
    
    async def scan_for_singer_plugins(
        self, 
        path: str
    ) -> FlextResult[list[FlextPlugin]]:
        """Scan for Singer tap/target plugins."""
    
    # Validation operations
    async def validate_plugin_structure(
        self, 
        plugin_path: str
    ) -> FlextResult[bool]:
        """Validate plugin directory structure."""
    
    async def validate_plugin_metadata(
        self, 
        plugin: FlextPlugin
    ) -> FlextResult[bool]:
        """Validate plugin metadata and configuration."""
    
    # Cache operations
    async def clear_discovery_cache(self) -> FlextResult[bool]:
        """Clear plugin discovery cache."""
    
    async def refresh_plugin_cache(
        self, 
        plugin_id: str
    ) -> FlextResult[bool]:
        """Refresh cache for specific plugin."""
```

## Command/Query Handlers

### FlextPluginHandler

CQRS command handler for plugin operations.

```python
from flext_plugin.application.handlers import FlextPluginHandler

class FlextPluginHandler:
    """CQRS command handler for plugin operations."""
    
    def __init__(self, service: FlextPluginService):
        """Initialize handler with plugin service."""
    
    # Command handling
    async def handle_create_plugin_command(
        self, 
        command: dict[str, object]
    ) -> FlextResult[FlextPlugin]:
        """Handle plugin creation command."""
    
    async def handle_activate_plugin_command(
        self, 
        command: dict[str, object]
    ) -> FlextResult[bool]:
        """Handle plugin activation command."""
    
    async def handle_deactivate_plugin_command(
        self, 
        command: dict[str, object]
    ) -> FlextResult[bool]:
        """Handle plugin deactivation command."""
    
    async def handle_execute_plugin_command(
        self,
        command: dict[str, object]
    ) -> FlextResult[PluginExecutionResult]:
        """Handle plugin execution command."""
    
    # Query handling
    async def handle_get_plugin_query(
        self, 
        query: dict[str, object]
    ) -> FlextResult[FlextPlugin]:
        """Handle get plugin query."""
    
    async def handle_list_plugins_query(
        self, 
        query: dict[str, object]
    ) -> FlextResult[list[FlextPlugin]]:
        """Handle list plugins query."""
```

### FlextPluginRegistrationHandler

Specialized handler for plugin registration operations.

```python
from flext_plugin.application.handlers import FlextPluginRegistrationHandler

class FlextPluginRegistrationHandler:
    """Specialized handler for plugin registration operations."""
    
    def __init__(self, registry: FlextPluginRegistry):
        """Initialize handler with plugin registry."""
    
    async def handle_register_plugin(
        self, 
        plugin: FlextPlugin
    ) -> FlextResult[FlextPlugin]:
        """Handle plugin registration with validation."""
    
    async def handle_unregister_plugin(
        self, 
        plugin_id: str
    ) -> FlextResult[bool]:
        """Handle plugin unregistration with cleanup."""
    
    async def handle_bulk_register(
        self, 
        plugins: list[FlextPlugin]
    ) -> FlextResult[list[str]]:
        """Handle bulk plugin registration."""
    
    async def validate_registration(
        self, 
        plugin: FlextPlugin
    ) -> FlextResult[bool]:
        """Validate plugin before registration."""
```

## Domain Ports

Interface definitions for external dependencies.

```python
from flext_plugin.domain.ports import (
    FlextPluginManagerPort,
    FlextPluginLoaderPort,
    FlextPluginDiscoveryPort
)

# Plugin management interface
class FlextPluginManagerPort(Protocol):
    """Port for plugin management operations."""
    
    async def register_plugin(self, plugin: FlextPlugin) -> FlextResult[FlextPlugin]
    async def activate_plugin(self, plugin_id: str) -> FlextResult[bool]
    async def deactivate_plugin(self, plugin_id: str) -> FlextResult[bool]
    async def execute_plugin(self, plugin_id: str, data: dict) -> FlextResult

# Plugin loading interface
class FlextPluginLoaderPort(Protocol):
    """Port for plugin loading operations."""
    
    async def load_plugin(self, plugin_path: str) -> FlextResult[FlextPlugin]
    async def unload_plugin(self, plugin_id: str) -> FlextResult[bool]
    async def reload_plugin(self, plugin_id: str) -> FlextResult[bool]

# Plugin discovery interface
class FlextPluginDiscoveryPort(Protocol):
    """Port for plugin discovery operations."""
    
    async def discover_plugins(self, path: str) -> FlextResult[list[FlextPlugin]]
    async def scan_directory(self, directory: str) -> FlextResult[list[str]]
    async def validate_plugin(self, plugin_path: str) -> FlextResult[bool]
```

## Hot Reload System

### Hot Reload Functions

```python
from flext_plugin.hot_reload import (
    enable_hot_reload,
    disable_hot_reload,
    reload_plugin,
    watch_plugin_directory
)

# Enable hot reload for development
await enable_hot_reload(
    watch_paths=["./plugins"],
    reload_on_change=True,
    preserve_state=True
)

# Reload specific plugin
result = await reload_plugin("plugin-name")

# Watch directory for changes
watcher = await watch_plugin_directory(
    "./plugins",
    callback=lambda path: print(f"Changed: {path}")
)
```

### Hot Reload Configuration

```python
from flext_plugin.hot_reload import HotReloadConfig

class HotReloadConfig:
    """Configuration for hot reload system."""
    
    enabled: bool = True
    watch_paths: list[str] = []
    watch_interval: int = 2
    reload_on_change: bool = True
    preserve_state: bool = True
    rollback_on_error: bool = True
    ignore_patterns: list[str] = ["*.pyc", "__pycache__"]
```

## Usage Examples

### Basic Plugin Operations

```python
from flext_plugin import create_flext_plugin_platform, create_flext_plugin
from flext_plugin.core.types import PluginType

# Create platform and plugin
platform = create_flext_plugin_platform()
plugin = create_flext_plugin(
    name="example-plugin",
    version="1.0.0",
    plugin_type=PluginType.SERVICE
)

# Register and activate
await platform.register_plugin(plugin)
await platform.activate_plugin("example-plugin")

# Execute plugin
result = await platform.execute_plugin(
    "example-plugin",
    {"input": "data"}
)
print(f"Result: {result.data if result.is_success() else result.error}")
```

### Plugin Discovery

```python
from flext_plugin.application.services import FlextPluginDiscoveryService

# Discover plugins
discovery = FlextPluginDiscoveryService()
plugins = await discovery.discover_plugins("./plugins")

# List discovered plugins
for plugin in plugins:
    print(f"Found: {plugin.name} v{plugin.plugin_version}")
    print(f"Type: {plugin.plugin_type}")
    print(f"Status: {plugin.status}")
```

### Error Handling

```python
from flext_plugin.core.types import PluginError
from flext_core import FlextResult

try:
    result = await platform.activate_plugin("non-existent-plugin")
    if result.is_failure():
        print(f"Activation failed: {result.error}")
        
except PluginError as e:
    print(f"Plugin error: {e}")
    print(f"Plugin: {e.plugin_name}")
```

## Type Definitions

### Type Aliases

```python
from typing import Dict, List, Optional, Union, Any

# Common type aliases used throughout the API
PluginId = str
PluginName = str
PluginVersion = str
PluginConfig = Dict[str, Any]
PluginData = Dict[str, Any]
PluginMetadata = Dict[str, Any]
PluginList = List[FlextPlugin] 
ExecutionResult = FlextResult[PluginExecutionResult]
```

### Generic Types

```python
from typing import TypeVar, Generic
from flext_core import FlextResult

T = TypeVar('T')

class PluginResult(Generic[T]):
    """Generic plugin operation result."""
    
    success: bool
    data: Optional[T]
    error: Optional[str]
    plugin_id: Optional[str]
```

---

For detailed implementation examples, see the [Examples Documentation](../examples/README.md).