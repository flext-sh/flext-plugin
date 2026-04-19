# Quick Start Guide

<!-- TOC START -->
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Option 1: Install from PyPI (Recommended)](#option-1-install-from-pypi-recommended)
  - [Option 2: Development Installation](#option-2-development-installation)
- [Your First Plugin (5 minutes)](#your-first-plugin-5-minutes)
  - [Step 1: Create a Simple Plugin](#step-1-create-a-simple-plugin)
  - [Step 2: Use the Plugin Platform](#step-2-use-the-plugin-platform)
  - [Step 3: Create a Custom Plugin Class](#step-3-create-a-custom-plugin-class)
- [Plugin Discovery](#plugin-discovery)
- [Testing Your Plugin](#testing-your-plugin)
- [Development with Hot Reload](#development-with-hot-reload)
- [Quality Gates](#quality-gates)
- [Next Steps](#next-steps)
  - [Immediate Next Steps](#immediate-next-steps)
  - [Plugin Types to Explore](#plugin-types-to-explore)
  - [Advanced Topics](#advanced-topics)
- [Troubleshooting](#troubleshooting)
  - [Common Issues](#common-issues)
  - [Getting Help](#getting-help)
<!-- TOC END -->

**⚠️ DEVELOPMENT BLOCKED**: This guide describes the TARGET functionality after Phase 0 compliance. Current implementation is non-compliant with FLEXT standards and modern Python practices.

## Prerequisites

**IMMEDIATE REQUIREMENTS (Phase 0):**

- **FLEXT Compliance**: Single class per module architecture
- **Modern Python Libraries**: setuptools entry points, importlib-metadata, packaging
- **Production Security**: Process isolation (NO RestrictedPython)

**Standard Prerequisites:**

- **Python 3.13+** with pip or Poetry
- **Git** (for development setup)
- Understanding of modern Python plugin architecture

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
# Install FLEXT Plugin
pip install flext-plugin

# Or with Poetry
poetry add flext-plugin
```

### Option 2: Development Installation

```bash
# Clone the FLEXT repository
git clone https://github.com/flext-sh/flext.git
cd flext/flext-plugin

# Setup development environment
make setup

# Verify installation
python -c "import flext_plugin; print(f'FLEXT Plugin v{flext_plugin.__version__}')"
```

## Your First Plugin (5 minutes)

### Step 1: Create a Simple Plugin

Create a file called `hello_plugin.py`:

```python
from flext_plugin import create_flext_plugin
from flext_plugin import PluginType

# Create a simple utility plugin
hello_plugin = create_flext_plugin(
    name="hello-world",
    version="0.9.9",
    plugin_type=PluginType.UTILITY,
    settings={"description": "My first FLEXT plugin", "author": "Your Name"},
)

print(f"Created plugin: {hello_plugin.name} v{hello_plugin.plugin_version}")
print(f"Status: {hello_plugin.status}")
print(f"Valid: {hello_plugin.is_valid()}")
```

Run it:

```bash
python hello_plugin.py
```

Expected output:

```
Created plugin: hello-world v1.0.0
Status: PluginStatus.INACTIVE
Valid: True
```

### Step 2: Use the Plugin Platform

Create `platform_example.py`:

```python
from flext_plugin import create_flext_plugin_platform, create_flext_plugin
from flext_plugin import PluginType


def main():
    # Create plugin platform
    platform = create_flext_plugin_platform(settings={"debug": True})

    # Create plugin
    plugin = create_flext_plugin(
        name="hello-world", version="0.9.9", plugin_type=PluginType.UTILITY
    )

    try:
        # Register plugin
        print("Registering plugin...")
        result = platform.register_plugin(plugin)
        if result.success():
            print("✅ Plugin registered successfully")
        else:
            print(f"❌ Registration failed: {result.error}")
            return

        # Activate plugin
        print("Activating plugin...")
        result = platform.activate_plugin("hello-world")
        if result.success():
            print("✅ Plugin activated successfully")
        else:
            print(f"❌ Activation failed: {result.error}")
            return

        # List active plugins
        active_plugins = platform.list_active_plugins()
        print(f"Active plugins: {[p.name for p in active_plugins.data]}")

    finally:
        # Cleanup
        platform.shutdown()


# Run the example
run(main())
```

Run it:

```bash
python platform_example.py
```

Expected output:

```
Registering plugin...
✅ Plugin registered successfully
Activating plugin...
✅ Plugin activated successfully
Active plugins: ['hello-world']
```

### Step 3: Create a Custom Plugin Class

Create `custom_plugin.py`:

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
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r, p
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u
from typing import Dict

class GreetingPlugin(FlextPlugin):
    """Custom plugin that generates personalized greetings."""

    def __init__(self, **kwargs):
        super().__init__(
            name="greeting-generator",
            version="0.9.9",
            settings={
                "plugin_type": PluginType.UTILITY,
                "description": "Generates personalized greetings",
                "author": "Your Name"
            },
            **kwargs
        )

    def initialize(self) -> p.Result[bool]:
        """Initialize plugin resources."""
        print(f"Initializing {self.name}...")
        # Setup any resources here
        return r[bool].ok(data=True)

    def execute(self, data: m.Dict) -> p.Result[m.Dict]:
        """Generate greeting based on input data."""
        try:
            # Validate plugin is active
            if self.status != PluginStatus.ACTIVE:
                return r[bool].fail("Plugin not active")

            # Extract name from input
            name = data.get("name", "World")
            language = data.get("language", "english")

            # Generate greeting based on language
            greetings = {
                "english": f"Hello, {name}!",
                "spanish": f"¡Hola, {name}!",
                "french": f"Bonjour, {name}!",
                "german": f"Hallo, {name}!",
                "portuguese": f"Olá, {name}!"
            }

            greeting = greetings.get(language.lower(), f"Hello, {name}!")

            result = {
                "greeting": greeting,
                "name": name,
                "language": language,
                "plugin": self.name,
                "version": self.plugin_version
            }

            return r[bool].ok(result)

        except Exception as e:
            return r[bool].fail(f"Execution failed: {e}")

    def cleanup(self) -> p.Result[bool]:
        """Cleanup plugin resources."""
        print(f"Cleaning up {self.name}...")
        return r[bool].ok(data=True)

# Usage example
def demo_custom_plugin():
from flext_plugin import create_flext_plugin_platform

    # Create platform and plugin
    platform = create_flext_plugin_platform()
    plugin = GreetingPlugin()

    try:
        # Register and activate
        platform.register_plugin(plugin)
        platform.activate_plugin(plugin.name)

        # Test different greetings
        test_cases = [
            {"name": "Alice", "language": "english"},
            {"name": "Carlos", "language": "spanish"},
            {"name": "Marie", "language": "french"},
            {"name": "Hans", "language": "german"},
            {"name": "João", "language": "portuguese"},
        ]

        print("\n--- Testing Greeting Plugin ---")
        for test_data in test_cases:
            result = platform.execute_plugin(plugin.name, test_data)
            if result.success():
                data = result.value
                print(f"✅ {data['greeting']} (Language: {data['language']})")
            else:
                print(f"❌ Failed: {result.error}")

    finally:
        platform.shutdown()

if __name__ == "__main__":
    run(demo_custom_plugin())
```

Run it:

```bash
python custom_plugin.py
```

Expected output:

```
Initializing greeting-generator...

--- Testing Greeting Plugin ---
✅ Hello, Alice! (Language: english)
✅ ¡Hola, Carlos! (Language: spanish)
✅ Bonjour, Marie! (Language: french)
✅ Hallo, Hans! (Language: german)
✅ Olá, João! (Language: portuguese)
Cleaning up greeting-generator...
```

## Plugin Discovery

FLEXT Plugin can automatically discover plugins in directories:

```python
from flext_plugin import FlextPluginDiscoveryService


def discover_plugins():
    """Discover plugins in current directory."""
    discovery = FlextPluginDiscoveryService()

    # Discover plugins (this will scan for Python files with plugin classes)
    result = discovery.discover_plugins("./")

    if result.success():
        plugins = result.value
        print(f"Found {len(plugins)} plugins:")
        for plugin in plugins:
            print(f"  - {plugin.name} v{plugin.plugin_version} ({plugin.status})")
    else:
        print(f"Discovery failed: {result.error}")


# Run discovery
run(discover_plugins())
```

## Testing Your Plugin

Create `test_greeting_plugin.py`:

```python
import pytest
from custom_plugin import GreetingPlugin
from flext_plugin import create_flext_plugin_platform


class TestGreetingPlugin:
    """Test suite for GreetingPlugin."""

    @pytest.fixture
    def plugin(self):
        """Create plugin instance."""
        return GreetingPlugin()

    @pytest.fixture
    def platform(self):
        """Create test platform."""
        platform = create_flext_plugin_platform(settings={"test_mode": True})
        yield platform
        platform.shutdown()

    def test_plugin_creation(self, plugin):
        """Test plugin creation."""
        assert plugin.name == "greeting-generator"
        assert plugin.plugin_version == "0.9.9"
        assert plugin.is_valid()

    def test_plugin_initialization(self, plugin):
        """Test plugin initialization."""
        result = plugin.initialize()
        assert result.success()

    def test_greeting_generation(self, plugin):
        """Test greeting generation."""
        plugin.initialize()
        plugin.activate()

        # Test English greeting
        result = plugin.execute({"name": "Test", "language": "english"})
        assert result.success()
        assert result.value["greeting"] == "Hello, Test!"

        # Test Spanish greeting
        result = plugin.execute({"name": "Test", "language": "spanish"})
        assert result.success()
        assert result.value["greeting"] == "¡Hola, Test!"

    def test_platform_integration(self, platform, plugin):
        """Test plugin integration with platform."""
        # Register plugin
        register_result = platform.register_plugin(plugin)
        assert register_result.success()

        # Activate plugin
        activate_result = platform.activate_plugin(plugin.name)
        assert activate_result.success()

        # Execute through platform
        execute_result = platform.execute_plugin(
            plugin.name, {"name": "Platform", "language": "english"}
        )
        assert execute_result.success()
        assert "Hello, Platform!" in str(execute_result.value)


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

Run tests:

```bash
# Install pytest if not already installed
pip install pytest

# Run tests
python test_greeting_plugin.py
```

## Development with Hot Reload

For development, you can enable hot reload to automatically reload plugins when files change:

```python
from flext_plugin import enable_hot_reload
from flext_plugin import create_flext_plugin_platform


def development_server():
    """Development server with hot reload."""

    # Enable hot reload
    enable_hot_reload(
        watch_paths=["./"],  # Watch current directory
        reload_on_change=True,
    )

    # Create platform
    platform = create_flext_plugin_platform(
        settings={"hot_reload": True, "debug": True}
    )

    print("🔥 Hot reload enabled!")
    print("Modify plugin files to see live updates...")
    print("Press Ctrl+C to stop")

    try:
        # Keep server running
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down development server...")
        platform.shutdown()


# Run development server
run(development_server())
```

## Quality Gates

FLEXT Plugin includes comprehensive quality gates. Set them up for your project:

```bash
# Install development dependencies
poetry add --group dev ruff mypy pytest pytest-cov bandit

# Run quality checks
ruff check .          # Linting
mypy .
pytest               # Testing
bandit -r .          # Security scanning
```

## Next Steps

Now that you have a basic understanding of FLEXT Plugin, explore these topics:

### Immediate Next Steps

1. **Plugin Development Guide** - Learn advanced plugin patterns (_Documentation coming soon_)
1. **Testing Guide** - Comprehensive testing strategies (_Documentation coming soon_)
1. **Examples** - More detailed examples

### Plugin Types to Explore

1. **Singer Integration** - Create data extraction/loading plugins (_Documentation coming soon_)
1. **Service Plugins** - Build microservice integrations (_Documentation coming soon_)
1. **Custom Plugin Types** - Define your own plugin categories (_Documentation coming soon_)

### Advanced Topics

1. **Architecture Guide** - Understand the system design
1. **Performance Optimization** - Scale your plugins (_Documentation coming soon_)
1. **FLEXT Ecosystem Integration** - Integrate with other FLEXT services (_Documentation coming soon_)

## Troubleshooting

### Common Issues

**Import Error: "No module named 'flext_plugin'"**

```bash
# Verify installation
pip list | grep flext-plugin

# Reinstall if necessary
pip install --force-reinstall flext-plugin
```

**Plugin Not Activating**

```python
# Check plugin status and validation
print(f"Plugin valid: {plugin.is_valid()}")
print(f"Plugin status: {plugin.status}")

# Ensure plugin is initialized before activation
plugin.initialize()
plugin.activate()
```

**Hot Reload Not Working**

```bash
# Ensure watchdog is installed
pip install watchdog

# Check file permissions in watch directory
ls -la ./
```

### Getting Help

- **Documentation**: Browse the complete documentation
- **Examples**: Check practical examples
- **Issues**: [Report bugs](https://github.com/flext-sh/flext/issues)
- **Discussions**: [Ask questions](https://github.com/flext-sh/flext/discussions)

______________________________________________________________________

🎉 **Congratulations!** You've successfully created your first FLEXT Plugin. Continue with the Plugin Development Guide to learn advanced patterns and best practices.
