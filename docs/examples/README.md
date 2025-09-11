# FLEXT Plugin Examples

Practical examples demonstrating how to create, configure, and integrate plugins with the FLEXT Plugin system.

## Example Categories

### 🚀 Getting Started

- **[Basic Plugin](basic-plugin.md)** - Simple plugin implementation
- **[Plugin Configuration](plugin-configuration.md)** - Configuration management patterns
- **[Plugin Lifecycle](plugin-lifecycle.md)** - Lifecycle management examples

### 🔌 Plugin Types

- **[Singer Tap Plugin](singer-tap.md)** - Data extraction plugin for Singer/Meltano
- **[Singer Target Plugin](singer-target.md)** - Data loading plugin
- **[Service Plugin](service-plugin.md)** - Microservice integration
- **[Utility Plugin](utility-plugin.md)** - General-purpose utility plugin

### 🛠️ Development Workflow

- **[Hot Reload Demo](hot-reload-demo.md)** - Development with live reloading
- **[Testing Plugins](testing-plugins.md)** - Comprehensive testing strategies
- **[Plugin Debugging](plugin-debugging.md)** - Debugging and troubleshooting

### 🏗️ Advanced Integration

- **[FlexCore Integration](flexcore-integration.md)** - Go service integration
- **[Multi-Plugin Orchestration](multi-plugin-orchestration.md)** - Coordinating multiple plugins
- **[Custom Plugin Types](custom-plugin-types.md)** - Creating custom plugin categories

## Quick Reference

### Basic Plugin Creation

```python
from flext_plugin import create_flext_plugin, create_flext_plugin_platform
from flext_plugin.core.types import PluginType

# Create simple plugin
plugin = create_flext_plugin(
    name="hello-world",
    version="0.9.0",
    plugin_type=PluginType.UTILITY
)

# Create platform and register plugin
platform = create_flext_plugin_platform()
await platform.register_plugin(plugin)
await platform.activate_plugin("hello-world")
```

### Singer Plugin Creation

```python
from flext_plugin.core.types import PluginType

# Create Singer tap plugin
tap_plugin = create_flext_plugin(
    name="tap-example-api",
    version="0.9.0",
    plugin_type=PluginType.TAP,
    config={
        "description": "Extract data from Example API",
        "schema_file": "tap_schema.json",
        "singer_spec": "0.7.0"
    }
)
```

### Hot Reload Development

```python
from flext_plugin.hot_reload import enable_hot_reload

# Enable hot reload for development
await enable_hot_reload(
    watch_paths=["./plugins", "./custom-plugins"],
    reload_on_change=True
)

print("Hot reload enabled - modify plugin files to see changes")
```

### Testing Setup

```python
import pytest
from flext_plugin import create_flext_plugin_platform

@pytest.fixture
async def platform():
    """Test platform fixture."""
    platform = create_flext_plugin_platform(config={"test_mode": True})
    yield platform
    await platform.shutdown()

async def test_plugin_activation(platform):
    """Test plugin activation."""
    plugin = create_flext_plugin(name="test-plugin", version="0.9.0")
    await platform.register_plugin(plugin)

    result = await platform.activate_plugin("test-plugin")
    assert result.success()
```

## Example Projects Structure

```
examples/
├── basic-plugin/            
│   ├── plugin.py             # Plugin class definition
│   ├── config.json           # Plugin configuration
│   ├── test_plugin.py        # Unit tests
│   └── README.md             # Documentation
│
├── singer-tap/               # Singer tap example
│   ├── tap_example_api.py    # Tap implementation
│   ├── schema.json           # Data schema
│   ├── meltano.yml           # Meltano configuration
│   └── README.md
│
├── service-plugin/           # Microservice plugin
│   ├── service.py            # FastAPI service
│   ├── routes.py             # API routes
│   ├── models.py             # Data models
│   ├── docker-compose.yml    # Container setup
│   └── README.md
│
├── hot-reload-demo/          # Hot reload development
│   ├── demo_plugin.py        # Demo plugin
│   ├── development.py        # Development server
│   ├── watch_config.json     # Watch configuration
│   └── README.md
│
└── integration-examples/     # Advanced integration
    ├── flexcore-bridge/      # Go service integration
    ├── multi-plugin-app/     # Multiple plugin coordination
    ├── custom-types/         # Custom plugin types
    └── README.md
```

## Running Examples

### Prerequisites

```bash
# Install FLEXT Plugin system
poetry add flext-plugin

# Or clone repository for development
git clone https://github.com/flext-sh/flext.git
cd flext/flext-plugin
make setup
```

### Running Individual Examples

```bash
# Navigate to example directory
cd docs/examples/basic-plugin

# Install example dependencies (if any)
poetry install

# Run example
python plugin.py

# Run tests
pytest test_plugin.py -v
```

### Development Mode

```bash
# Start hot reload development server
cd docs/examples/hot-reload-demo
python development.py

# In another terminal, modify demo_plugin.py to see live changes
echo "# Modified at $(date)" >> demo_plugin.py
```

## Example Templates

### Plugin Template

```python
from flext_plugin.domain.entities import FlextPlugin
from flext_plugin.core.types import PluginStatus, PluginType
from flext_core import FlextResult
from typing import Dict, object

class ExamplePlugin(FlextPlugin):
    """Template for creating custom plugins."""

    def __init__(self, **kwargs):
        super().__init__(
            name="example-plugin",
            version="0.9.0",
            config={
                "plugin_type": PluginType.UTILITY,
                "description": "Example plugin template",
                "author": "Your Name"
            },
            **kwargs
        )

    async def initialize(self) -> FlextResult[bool]:
        """Initialize plugin resources."""
        try:
            # Setup plugin resources
            await self._setup_resources()
            return FlextResult[None].ok(data=True)
        except Exception as e:
            return FlextResult[None].fail(f"Initialization failed: {e}")

    async def execute(self, data: Dict[str, object]) -> FlextResult[Dict[str, object]]:
        """Execute plugin logic."""
        try:
            # Validate plugin is active
            if self.status != PluginStatus.ACTIVE:
                return FlextResult[None].fail("Plugin not active")

            # Process data
            result = await self._process_data(data)
            return FlextResult[None].ok(result)

        except Exception as e:
            return FlextResult[None].fail(f"Execution failed: {e}")

    async def cleanup(self) -> FlextResult[bool]:
        """Cleanup plugin resources."""
        try:
            await self._cleanup_resources()
            return FlextResult[None].ok(data=True)
        except Exception as e:
            return FlextResult[None].fail(f"Cleanup failed: {e}")

    async def _setup_resources(self):
        """Setup plugin-specific resources."""
        pass

    async def _process_data(self, data: Dict[str, object]) -> Dict[str, object]:
        """Core processing logic - implement in subclass."""
        return {"processed": True, "input": data}

    async def _cleanup_resources(self):
        """Cleanup plugin-specific resources."""
        pass
```

### Test Template

```python
import pytest
from flext_plugin import create_flext_plugin_platform
from your_plugin import ExamplePlugin

class TestExamplePlugin:
    """Test suite template for plugins."""

    @pytest.fixture
    def plugin(self):
        """Create plugin instance for testing."""
        return ExamplePlugin()

    @pytest.fixture
    async def platform(self):
        """Create test platform."""
        platform = create_flext_plugin_platform(config={"test_mode": True})
        yield platform
        await platform.shutdown()

    def test_plugin_creation(self, plugin):
        """Test plugin creation."""
        assert plugin.name == "example-plugin"
        assert plugin.plugin_version == "0.9.0"
        assert plugin.is_valid()

    async def test_plugin_initialization(self, plugin):
        """Test plugin initialization."""
        result = await plugin.initialize()
        assert result.success()

    async def test_plugin_execution(self, plugin):
        """Test plugin execution."""
        # Initialize first
        await plugin.initialize()
        plugin.activate()

        # Test execution
        test_data = {"input": "test_value"}
        result = await plugin.execute(test_data)

        assert result.success()
        assert "processed" in result.data

    async def test_plugin_lifecycle(self, platform, plugin):
        """Test complete plugin lifecycle."""
        # Register plugin
        register_result = await platform.register_plugin(plugin)
        assert register_result.success()

        # Activate plugin
        activate_result = await platform.activate_plugin(plugin.name)
        assert activate_result.success()

        # Execute plugin
        execute_result = await platform.execute_plugin(
            plugin.name,
            {"test": "data"}
        )
        assert execute_result.success()

        # Deactivate plugin
        deactivate_result = await platform.deactivate_plugin(plugin.name)
        assert deactivate_result.success()
```

### Configuration Template

```json
{
  "plugin": {
    "name": "example-plugin",
    "version": "0.9.0",
    "type": "utility",
    "description": "Example plugin for demonstration",
    "author": "Your Name",
    "license": "MIT"
  },
  "configuration": {
    "debug": false,
    "timeout": 30,
    "retries": 3,
    "batch_size": 100
  },
  "dependencies": {
    "flext-core": ">=0.9.0",
    "flext-observability": ">=0.9.0"
  },
  "metadata": {
    "tags": ["example", "demo", "utility"],
    "keywords": ["plugin", "flext", "example"],
    "homepage": "https://github.com/flext-sh/flext",
    "repository": "https://github.com/flext-sh/flext/tree/main/flext-plugin"
  }
}
```

## Best Practices Demonstrated

### 1. Error Handling

All examples demonstrate proper error handling using `FlextResult` pattern:

```python
try:
    result = await operation()
    if result.success():
        return result.data
    else:
        logger.error(f"Operation failed: {result.error}")
        return None
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return FlextResult[None].fail(f"Unexpected error: {e}")
```

### 2. Resource Management

Proper resource cleanup in plugin lifecycle:

```python
async def cleanup(self) -> FlextResult[bool]:
    """Cleanup with error handling."""
    try:
        if hasattr(self, '_connection') and self._connection:
            await self._connection.close()

        if hasattr(self, '_temp_files'):
            for file_path in self._temp_files:
                os.unlink(file_path)

        return FlextResult[None].ok(data=True)
    except Exception as e:
        return FlextResult[None].fail(f"Cleanup failed: {e}")
```

### 3. Type Safety

All examples use proper type hints:

```python
from typing import Dict, List, Optional, object
from flext_core import FlextResult

async def process_data(
    self,
    data: Dict[str, object]
) -> FlextResult[Dict[str, object]]:
    """Type-safe data processing."""
    pass
```

### 4. Testing Coverage

Comprehensive test coverage for all plugin functionality:

- Unit tests for individual methods
- Integration tests for plugin lifecycle
- End-to-end tests for complete workflows
- Performance tests for critical paths

## Contributing Examples

### Adding New Examples

1. **Create Example Directory**:

   ```bash
   mkdir docs/examples/your-example
   cd docs/examples/your-example
   ```

2. **Follow Template Structure**:

   - `plugin.py` - Main plugin implementation
   - `test_plugin.py` - Comprehensive tests
   - `config.json` - Configuration example
   - `README.md` - Documentation and usage

3. **Update Index**:
   Add your example to this README.md file

4. **Test Example**:

   ```bash
   # Ensure example works
   python plugin.py
   pytest test_plugin.py -v

   # Validate against quality gates
   make lint
   make type-check
   ```

### Example Quality Standards

- **85% Test Coverage**: Comprehensive test suites
- **Type Safety**: Full type annotation coverage
- **Documentation**: Clear README with usage instructions
- **Error Handling**: Proper FlextResult pattern usage
- **Resource Management**: Clean initialization and cleanup

---

**Next Steps**: Browse individual example directories for detailed implementations and run the examples to see FLEXT Plugin system in action.
