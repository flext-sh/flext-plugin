# FLEXT Plugin Application Module

**Application services and CQRS handlers orchestrating plugin business logic.**

This module implements the application layer of the Clean Architecture, providing services that coordinate domain entities, handle use cases, and implement CQRS (Command Query Responsibility Segregation) patterns for scalable plugin management.

## Module Contents

### Application Services

#### `FlextPluginService`

Core plugin management service coordinating business operations.

```python
from flext_plugin.application.services import FlextPluginService
from flext_plugin.domain.entities import FlextPluginRegistry

registry = FlextPluginRegistry()
service = FlextPluginService(registry)

# Plugin lifecycle operations
result = await service.create_plugin({
    "name": "data-processor",
    "version": "1.0.0",
    "description": "Data processing plugin"
})

if result.success():
    plugin = result.data
    activation = await service.activate_plugin(plugin.name)
```

**Key Operations:**

- **Plugin Creation**: Validate and create plugin entities
- **Lifecycle Management**: Activate, deactivate, and manage plugin states
- **Execution Coordination**: Orchestrate plugin execution with context
- **Configuration Management**: Handle plugin configuration updates
- **Health Monitoring**: Track and report plugin health status

#### `FlextPluginDiscoveryService`

Plugin discovery and scanning service.

```python
from flext_plugin.application.services import FlextPluginDiscoveryService

discovery = FlextPluginDiscoveryService()

# Discover plugins in directories
result = await discovery.discover_plugins("./plugins")
if result.success():
    plugins = result.data
    print(f"Found {len(plugins)} plugins")

# Recursive discovery with depth control
deep_result = await discovery.discover_plugins_recursive(
    "./workspace",
    max_depth=3
)

# Singer-specific discovery
singer_result = await discovery.scan_for_singer_plugins("./meltano-project")
```

**Discovery Features:**

- **Directory Scanning**: Recursive plugin discovery with depth control
- **Singer Integration**: Specialized Singer tap/target discovery
- **Metadata Validation**: Plugin structure and metadata validation
- **Caching**: Discovery result caching for performance
- **Filtering**: Type-based and criteria-based plugin filtering

### CQRS Handlers

#### `FlextPluginHandler`

Command and query handler for plugin operations.

```python
from flext_plugin.application.handlers import FlextPluginHandler

handler = FlextPluginHandler(plugin_service)

# Command handling
create_command = {
    "operation": "create_plugin",
    "name": "api-gateway",
    "version": "2.0.0",
    "config": {"port": 8080}
}

result = await handler.handle_create_plugin_command(create_command)

# Query handling
list_query = {
    "operation": "list_plugins",
    "filter": {"status": "active"}
}

plugins = await handler.handle_list_plugins_query(list_query)
```

**Command Operations:**

- `create_plugin`: Create new plugin with validation
- `activate_plugin`: Activate plugin with dependency checking
- `deactivate_plugin`: Deactivate plugin with cleanup
- `execute_plugin`: Execute plugin with context and data
- `update_plugin_config`: Update plugin configuration

**Query Operations:**

- `get_plugin`: Retrieve plugin by identifier
- `list_plugins`: List plugins with filtering and pagination
- `get_plugin_status`: Get current plugin status and health
- `list_active_plugins`: Get all currently active plugins

#### `FlextPluginRegistrationHandler`

Specialized handler for plugin registration operations.

```python
from flext_plugin.application.handlers import FlextPluginRegistrationHandler

registration_handler = FlextPluginRegistrationHandler(registry)

# Individual registration
result = await registration_handler.handle_register_plugin(plugin)

# Bulk registration
plugins = [plugin1, plugin2, plugin3]
bulk_result = await registration_handler.handle_bulk_register(plugins)

# Registration validation
validation = await registration_handler.validate_registration(plugin)
```

**Registration Features:**

- **Individual Registration**: Single plugin registration with validation
- **Bulk Registration**: Multiple plugin registration with rollback
- **Validation**: Pre-registration validation and conflict detection
- **Dependency Resolution**: Plugin dependency validation and ordering

## Service Layer Patterns

### Application Service Pattern

Application services coordinate domain operations without containing business logic:

```python
class FlextPluginService:
    def __init__(self, registry: FlextPluginRegistry):
        self.registry = registry

    async def create_plugin(self, config: dict) -> FlextResult[FlextPlugin]:
        """Create plugin by coordinating domain operations."""
        # Validate input (application concern)
        validation = await self._validate_plugin_config(config)
        if validation.is_failure():
            return validation

        # Create domain entity (domain operation)
        plugin = FlextPlugin(**config)

        # Register with registry (domain operation)
        return await self.registry.register_plugin(plugin)

    async def activate_plugin(self, plugin_id: str) -> FlextResult[bool]:
        """Activate plugin with dependency coordination."""
        # Get plugin (domain query)
        plugin = self.registry.get_plugin(plugin_id)
        if not plugin:
            return FlextResult[None].fail(f"Plugin {plugin_id} not found")

        # Check dependencies (application coordination)
        dep_check = await self._validate_dependencies(plugin)
        if dep_check.is_failure():
            return dep_check

        # Activate plugin (domain operation)
        return plugin.activate()
```

### Transaction and Coordination

```python
class PluginDeploymentWorkflow:
    """Complex workflow coordinating multiple operations."""

    async def deploy_plugin_package(
        self,
        package_path: str
    ) -> FlextResult[FlextPlugin]:
        """Deploy plugin package with full workflow."""
        try:
            # Discovery phase
            discovery_result = await self.discovery_service.discover_plugins(
                package_path
            )
            if discovery_result.is_failure():
                return discovery_result

            plugin = discovery_result.data[0]  # Assume single plugin

            # Validation phase
            validation_result = await self._validate_plugin_package(plugin)
            if validation_result.is_failure():
                return validation_result

            # Registration phase
            registration_result = await self.registry.register_plugin(plugin)
            if registration_result.is_failure():
                return registration_result

            # Configuration phase
            config_result = await self._apply_plugin_configuration(plugin)
            if config_result.is_failure():
                # Rollback registration
                await self.registry.unregister_plugin(plugin.name)
                return config_result

            # Activation phase
            return plugin.activate()

        except Exception as e:
            return FlextResult[None].fail(f"Deployment failed: {e}")
```

## CQRS Implementation

### Command Pattern

Commands represent actions that change system state:

```python
class CreatePluginCommand:
    """Command to create a new plugin."""
    def __init__(
        self,
        name: str,
        version: str,
        plugin_type: PluginType,
        config: dict[str, Any]
    ):
        self.name = name
        self.version = version
        self.plugin_type = plugin_type
        self.config = config
        self.timestamp = datetime.utcnow()

class ActivatePluginCommand:
    """Command to activate a plugin."""
    def __init__(self, plugin_id: str, force: bool = False):
        self.plugin_id = plugin_id
        self.force = force
        self.timestamp = datetime.utcnow()
```

### Query Pattern

Queries represent read operations that don't change state:

```python
class GetPluginQuery:
    """Query to retrieve a specific plugin."""
    def __init__(self, plugin_id: str):
        self.plugin_id = plugin_id

class ListPluginsQuery:
    """Query to list plugins with filtering."""
    def __init__(
        self,
        plugin_type: Optional[PluginType] = None,
        status: Optional[PluginStatus] = None,
        limit: int = 100,
        offset: int = 0
    ):
        self.plugin_type = plugin_type
        self.status = status
        self.limit = limit
        self.offset = offset
```

### Handler Implementation

```python
class FlextPluginCommandHandler:
    """Handles plugin-related commands."""

    async def handle(self, command: CreatePluginCommand) -> FlextResult[FlextPlugin]:
        """Handle plugin creation command."""
        try:
            # Validate command
            if not command.name:
                return FlextResult[None].fail("Plugin name is required")

            # Create plugin entity
            plugin = FlextPlugin(
                name=command.name,
                version=command.version,
                config=command.config
            )

            # Register plugin
            result = await self.registry.register_plugin(plugin)

            # Publish domain events
            if result.success():
                await self._publish_events(plugin.get_domain_events())

            return result

        except Exception as e:
            return FlextResult[None].fail(f"Command handling failed: {e}")

class FlextPluginQueryHandler:
    """Handles plugin-related queries."""

    async def handle(self, query: ListPluginsQuery) -> FlextResult[list[FlextPlugin]]:
        """Handle list plugins query."""
        try:
            plugins = self.registry.list_plugins(
                plugin_type=query.plugin_type,
                status=query.status
            )

            # Apply pagination
            start = query.offset
            end = start + query.limit
            paginated = plugins[start:end]

            return FlextResult[None].ok(paginated)

        except Exception as e:
            return FlextResult[None].fail(f"Query handling failed: {e}")
```

## Error Handling and Validation

### Input Validation

```python
class PluginConfigValidator:
    """Validates plugin configuration data."""

    REQUIRED_FIELDS = ["name", "version"]
    MAX_NAME_LENGTH = 100

    def validate(self, config: dict) -> FlextResult[dict]:
        """Validate plugin configuration."""
        errors = []

        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in config:
                errors.append(f"Missing required field: {field}")

        # Validate name length
        name = config.get("name", "")
        if len(name) > self.MAX_NAME_LENGTH:
            errors.append(f"Name too long (max {self.MAX_NAME_LENGTH} characters)")

        # Validate version format
        version = config.get("version", "")
        if not self._is_valid_semver(version):
            errors.append("Version must follow semantic versioning format")

        if errors:
            return FlextResult[None].fail(f"Validation failed: {'; '.join(errors)}")

        return FlextResult[None].ok(config)

    def _is_valid_semver(self, version: str) -> bool:
        """Check if version follows semantic versioning."""
        import re
        pattern = r'^\d+\.\d+\.\d+(?:-[a-zA-Z0-9-]+)?(?:\+[a-zA-Z0-9-]+)?$'
        return bool(re.match(pattern, version))
```

### Exception Handling

```python
from flext_plugin.core.types import PluginError

class PluginServiceError(PluginError):
    """Application service specific errors."""
    pass

class PluginValidationError(PluginServiceError):
    """Plugin validation errors."""
    pass

class PluginDependencyError(PluginServiceError):
    """Plugin dependency resolution errors."""
    pass

# Usage in services
async def create_plugin(self, config: dict) -> FlextResult[FlextPlugin]:
    """Create plugin with comprehensive error handling."""
    try:
        # Validate configuration
        validation = self.validator.validate(config)
        if validation.is_failure():
            raise PluginValidationError(validation.error)

        # Check dependencies
        deps = await self._resolve_dependencies(config)
        if deps.is_failure():
            raise PluginDependencyError(deps.error)

        # Create plugin
        plugin = FlextPlugin(**config)
        return FlextResult[None].ok(plugin)

    except PluginServiceError as e:
        return FlextResult[None].fail(str(e))
    except Exception as e:
        return FlextResult[None].fail(f"Unexpected error: {e}")
```

## Testing Patterns

### Service Testing

```python
import pytest
from unittest.mock import Mock, AsyncMock
from flext_plugin.application.services import FlextPluginService

class TestFlextPluginService:
    @pytest.fixture
    def mock_registry(self):
        """Mock plugin registry for testing."""
        registry = Mock()
        registry.register_plugin = AsyncMock()
        registry.get_plugin = Mock()
        return registry

    @pytest.fixture
    def service(self, mock_registry):
        """Create service with mocked dependencies."""
        return FlextPluginService(mock_registry)

    async def test_create_plugin_success(self, service, mock_registry):
        """Test successful plugin creation."""
        config = {
            "name": "test-plugin",
            "version": "1.0.0",
            "description": "Test plugin"
        }

        mock_registry.register_plugin.return_value = FlextResult[None].ok(
            FlextPlugin(**config)
        )

        result = await service.create_plugin(config)

        assert result.success()
        assert result.data.name == "test-plugin"
        mock_registry.register_plugin.assert_called_once()

    async def test_create_plugin_validation_failure(self, service):
        """Test plugin creation with invalid configuration."""
        config = {"name": ""}  # Invalid: empty name

        result = await service.create_plugin(config)

        assert result.is_failure()
        assert "validation" in result.error.lower()
```

### Handler Testing

```python
class TestFlextPluginHandler:
    @pytest.fixture
    def mock_service(self):
        """Mock plugin service for testing."""
        service = Mock()
        service.create_plugin = AsyncMock()
        service.activate_plugin = AsyncMock()
        return service

    @pytest.fixture
    def handler(self, mock_service):
        """Create handler with mocked service."""
        return FlextPluginHandler(mock_service)

    async def test_handle_create_command(self, handler, mock_service):
        """Test create plugin command handling."""
        command = {
            "name": "test-plugin",
            "version": "1.0.0",
            "config": {}
        }

        mock_service.create_plugin.return_value = FlextResult[None].ok(
            FlextPlugin(name="test-plugin", version="1.0.0")
        )

        result = await handler.handle_create_plugin_command(command)

        assert result.success()
        mock_service.create_plugin.assert_called_once()
```

## Performance Considerations

### Caching Strategies

```python
from functools import lru_cache
from typing import Optional

class CachedPluginService(FlextPluginService):
    """Plugin service with caching for read operations."""

    @lru_cache(maxsize=128)
    def get_plugin_cached(self, plugin_id: str) -> Optional[FlextPlugin]:
        """Get plugin with LRU caching."""
        return self.registry.get_plugin(plugin_id)

    def invalidate_cache(self, plugin_id: str) -> None:
        """Invalidate cache for specific plugin."""
        # Clear specific entry from cache
        self.get_plugin_cached.cache_clear()
```

### Batch Operations

```python
async def bulk_plugin_operations(
    self,
    operations: list[dict]
) -> FlextResult[list[FlextPlugin]]:
    """Process multiple plugin operations efficiently."""
    results = []
    failed_operations = []

    # Group operations by type for efficiency
    creates = [op for op in operations if op["type"] == "create"]
    activations = [op for op in operations if op["type"] == "activate"]

    # Process creates in parallel
    create_tasks = [
        self.create_plugin(op["config"])
        for op in creates
    ]
    create_results = await asyncio.gather(*create_tasks, return_exceptions=True)

    # Process results and handle failures
    for result in create_results:
        if isinstance(result, Exception):
            failed_operations.append(str(result))
        elif result.success():
            results.append(result.data)

    if failed_operations:
        return FlextResult[None].fail(f"Bulk operation failures: {failed_operations}")

    return FlextResult[None].ok(results)
```

## Architecture Integration

### Clean Architecture Positioning

```
Platform Layer → Application Layer (THIS MODULE) → Domain Layer → Core Layer
```

### Integration with Other Layers

```python
# Application services coordinate domain entities
from flext_plugin.domain.entities import FlextPlugin, FlextPluginRegistry
from flext_plugin.core.types import PluginStatus, PluginType

# Platform layer uses application services
from flext_plugin.application.services import FlextPluginService
from flext_plugin.application.handlers import FlextPluginHandler

class PluginPlatformIntegration:
    """Integration between platform and application layers."""

    def __init__(self):
        self.registry = FlextPluginRegistry()
        self.service = FlextPluginService(self.registry)
        self.handler = FlextPluginHandler(self.service)

    async def handle_platform_request(self, request: dict) -> FlextResult:
        """Handle platform requests through application layer."""
        operation = request.get("operation")

        if operation == "create_plugin":
            return await self.handler.handle_create_plugin_command(request)
        elif operation == "list_plugins":
            return await self.handler.handle_list_plugins_query(request)
        else:
            return FlextResult[None].fail(f"Unknown operation: {operation}")
```

---

**Next Steps**: Explore the [Domain Entities](../domain/README.md) that these services orchestrate, or review the [Platform Integration](../README.md) that uses these application services.
