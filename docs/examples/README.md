# FLEXT Plugin Examples

<!-- TOC START -->

- [Example Categories](#example-categories)
  - [🚀 Getting Started](#getting-started)
  - [🔌 Plugin Types](#plugin-types)
  - [🛠️ Development Workflow](#development-workflow)
  - [🏗️ Advanced Integration](#advanced-integration)
- [Quick Reference](#quick-reference)
  - [Basic Plugin Creation](#basic-plugin-creation)
  - [Singer Plugin Creation](#singer-plugin-creation)
  - [Hot Reload Development](#hot-reload-development)
  - [Testing Setup](#testing-setup)
- [Example Projects Structure](#example-projects-structure)
- [Running Examples](#running-examples)
  - [Prerequisites](#prerequisites)
  - [Running Individual Examples](#running-individual-examples)
  - [Development Mode](#development-mode)
- [Example Templates](#example-templates)
  - [Plugin Template](#plugin-template)
  - [Test Template](#test-template)
  - [Configuration Template](#configuration-template)
- [Best Practices Demonstrated](#best-practices-demonstrated)
  - [1. Error Handling](#1-error-handling)
  - [2. Resource Management](#2-resource-management)
  - [3. Type Safety](#3-type-safety)
  - [4. Testing Coverage](#4-testing-coverage)
- [Contributing Examples](#contributing-examples)
  - [Adding New Examples](#adding-new-examples)
  - [Example Quality Standards](#example-quality-standards)

<!-- TOC END -->

Practical examples demonstrating how to create, configure, and integrate plugins with the FLEXT Plugin system.

## Example Categories

### 🚀 Getting Started

- **Basic Plugin** - Simple plugin implementation
- **Plugin Configuration** - Configuration management patterns (_Documentation coming soon_)
- **Plugin Lifecycle** - Lifecycle management examples (_Documentation coming soon_)

### 🔌 Plugin Types

- **Singer Tap Plugin** - Data extraction plugin for Singer/Meltano (_Documentation coming soon_)
- **Singer Target Plugin** - Data loading plugin (_Documentation coming soon_)
- **Service Plugin** - Microservice integration (_Documentation coming soon_)
- **Utility Plugin** - General-purpose utility plugin (_Documentation coming soon_)

### 🛠️ Development Workflow

- **Hot Reload Demo** - Development with live reloading (_Documentation coming soon_)
- **Testing Plugins** - Comprehensive testing strategies (_Documentation coming soon_)
- **Plugin Debugging** - Debugging and troubleshooting (_Documentation coming soon_)

### 🏗️ Advanced Integration

- **FlexCore Integration** - Go service integration (_Documentation coming soon_)
- **Multi-Plugin Orchestration** - Coordinating multiple plugins (_Documentation coming soon_)
- **Custom Plugin Types** - Creating custom plugin categories (_Documentation coming soon_)

## Quick Reference

### Basic Plugin Creation

```python
from flext_plugin import create_flext_plugin, create_flext_plugin_platform
from flext_plugin import PluginType

# Create simple plugin
plugin = create_flext_plugin(
    name="hello-world", version="0.9.9", plugin_type=PluginType.UTILITY
)

# Create platform and register plugin
platform = create_flext_plugin_platform()
platform.register_plugin(plugin)
platform.activate_plugin("hello-world")
```

### Singer Plugin Creation

```python
from flext_plugin import PluginType

# Create Singer tap plugin
tap_plugin = create_flext_plugin(
    name="tap-example-api",
    version="0.9.9",
    plugin_type=PluginType.TAP,
    config={
        "description": "Extract data from Example API",
        "schema_file": "tap_schema.json",
        "singer_spec": "0.9.9",
    },
)
```

### Hot Reload Development

```python
from flext_plugin import enable_hot_reload

# Enable hot reload for development
enable_hot_reload(watch_paths=["./plugins", "./custom-plugins"], reload_on_change=True)

print("Hot reload enabled - modify plugin files to see changes")
```

### Testing Setup

```python
import pytest
from flext_plugin import create_flext_plugin_platform


@pytest.fixture
def platform():
    """Test platform fixture."""
    platform = create_flext_plugin_platform(config={"test_mode": True})
    yield platform
    platform.shutdown()


def test_plugin_activation(platform):
    """Test plugin activation."""
    plugin = create_flext_plugin(name="test-plugin", version="0.9.9")
    platform.register_plugin(plugin)

    result = platform.activate_plugin("test-plugin")
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
from flext_plugin import FlextPlugin
from flext_plugin import PluginStatus, PluginType
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import h
from flext_core import FlextLogger
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import t
from flext_core import u
from typing import Dict


class ExamplePlugin(FlextPlugin):
    """Template for creating custom plugins."""

    def __init__(self, **kwargs):
        super().__init__(
            name="example-plugin",
            version="0.9.9",
            config={
                "plugin_type": PluginType.UTILITY,
                "description": "Example plugin template",
                "author": "Your Name",
            },
            **kwargs,
        )

    def initialize(self) -> r[bool]:
        """Initialize plugin resources."""
        try:
            # Setup plugin resources
            self._setup_resources()
            return r[bool].ok(data=True)
        except Exception as e:
            return r[bool].fail(f"Initialization failed: {e}")

    def execute(self, data: t.Dict) -> r[t.Dict]:
        """Execute plugin logic."""
        try:
            # Validate plugin is active
            if self.status != PluginStatus.ACTIVE:
                return r[bool].fail("Plugin not active")

            # Process data
            result = self._process_data(data)
            return r[bool].ok(result)

        except Exception as e:
            return r[bool].fail(f"Execution failed: {e}")

    def cleanup(self) -> r[bool]:
        """Cleanup plugin resources."""
        try:
            self._cleanup_resources()
            return r[bool].ok(data=True)
        except Exception as e:
            return r[bool].fail(f"Cleanup failed: {e}")

    def _setup_resources(self):
        """Setup plugin-specific resources."""
        pass

    def _process_data(self, data: t.Dict) -> t.Dict:
        """Core processing logic - implement in subclass."""
        return {"processed": True, "input": data}

    def _cleanup_resources(self):
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
    def platform(self):
        """Create test platform."""
        platform = create_flext_plugin_platform(config={"test_mode": True})
        yield platform
        platform.shutdown()

    def test_plugin_creation(self, plugin):
        """Test plugin creation."""
        assert plugin.name == "example-plugin"
        assert plugin.plugin_version == "0.9.9"
        assert plugin.is_valid()

    def test_plugin_initialization(self, plugin):
        """Test plugin initialization."""
        result = plugin.initialize()
        assert result.success()

    def test_plugin_execution(self, plugin):
        """Test plugin execution."""
        # Initialize first
        plugin.initialize()
        plugin.activate()

        # Test execution
        test_data = {"input": "test_value"}
        result = plugin.execute(test_data)

        assert result.success()
        assert "processed" in result.data

    def test_plugin_lifecycle(self, platform, plugin):
        """Test complete plugin lifecycle."""
        # Register plugin
        register_result = platform.register_plugin(plugin)
        assert register_result.success()

        # Activate plugin
        activate_result = platform.activate_plugin(plugin.name)
        assert activate_result.success()

        # Execute plugin
        execute_result = platform.execute_plugin(plugin.name, {"test": "data"})
        assert execute_result.success()

        # Deactivate plugin
        deactivate_result = platform.deactivate_plugin(plugin.name)
        assert deactivate_result.success()
```

### Configuration Template

```json
{
  "plugin": {
    "name": "example-plugin",
    "version": "0.9.9",
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
    "flext-core": ">=0.9.9",
    "flext-observability": ">=0.9.9"
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

All examples demonstrate proper error handling using `r` pattern:

```python
try:
    result = operation()
    if result.success():
        return result.data
    else:
        logger.error(f"Operation failed: {result.error}")
        return None
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return r[bool].fail(f"Unexpected error: {e}")
```

### 2. Resource Management

Proper resource cleanup in plugin lifecycle:

```python
def cleanup(self) -> r[bool]:
    """Cleanup with error handling."""
    try:
        if hasattr(self, "_connection") and self._connection:
            self._connection.close()

        if hasattr(self, "_temp_files"):
            for file_path in self._temp_files:
                os.unlink(file_path)

        return r[bool].ok(data=True)
    except Exception as e:
        return r[bool].fail(f"Cleanup failed: {e}")
```

### 3. Type Safety

All examples use proper type hints:

```python
from typing import Dict, List, Optional
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import h
from flext_core import FlextLogger
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import t
from flext_core import u


def process_data(self, data: t.Dict) -> r[t.Dict]:
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

1. **Follow Template Structure**:

   - `plugin.py` - Main plugin implementation
   - `test_plugin.py` - Comprehensive tests
   - `config.json` - Configuration example
   - `README.md` - Documentation and usage

1. **Update Index**:
   Add your example to this README.md file

1. **Test Example**:

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
- **Error Handling**: Proper r pattern usage
- **Resource Management**: Clean initialization and cleanup

______________________________________________________________________

**Next Steps**: Browse individual example directories for detailed implementations and run the examples to see FLEXT Plugin system in action.
