# Quick Start Guide

Get up and running with FLEXT Plugin in just a few minutes. This guide will walk you through installation, creating your first plugin, and basic usage patterns.

## Prerequisites

- **Python 3.13+** with pip or Poetry
- **Git** (for development setup)
- Basic understanding of Python async/await patterns

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
from flext_plugin.core.types import PluginType

# Create a simple utility plugin
hello_plugin = create_flext_plugin(
    name="hello-world",
    version="1.0.0",
    plugin_type=PluginType.UTILITY,
    config={
        "description": "My first FLEXT plugin",
        "author": "Your Name"
    }
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
import asyncio
from flext_plugin import create_flext_plugin_platform, create_flext_plugin
from flext_plugin.core.types import PluginType

async def main():
    # Create plugin platform
    platform = create_flext_plugin_platform(config={
        "debug": True
    })

    # Create plugin
    plugin = create_flext_plugin(
        name="hello-world",
        version="1.0.0",
        plugin_type=PluginType.UTILITY
    )

    try:
        # Register plugin
        print("Registering plugin...")
        result = await platform.register_plugin(plugin)
        if result.success():
            print("✅ Plugin registered successfully")
        else:
            print(f"❌ Registration failed: {result.error}")
            return

        # Activate plugin
        print("Activating plugin...")
        result = await platform.activate_plugin("hello-world")
        if result.success():
            print("✅ Plugin activated successfully")
        else:
            print(f"❌ Activation failed: {result.error}")
            return

        # List active plugins
        active_plugins = await platform.list_active_plugins()
        print(f"Active plugins: {[p.name for p in active_plugins.data]}")

    finally:
        # Cleanup
        await platform.shutdown()

# Run the example
asyncio.run(main())
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
import asyncio
from flext_plugin.domain.entities import FlextPlugin
from flext_plugin.core.types import PluginStatus, PluginType
from flext_core import FlextResult
from typing import Dict, Any

class GreetingPlugin(FlextPlugin):
    """Custom plugin that generates personalized greetings."""

    def __init__(self, **kwargs):
        super().__init__(
            name="greeting-generator",
            version="1.0.0",
            config={
                "plugin_type": PluginType.UTILITY,
                "description": "Generates personalized greetings",
                "author": "Your Name"
            },
            **kwargs
        )

    async def initialize(self) -> FlextResult[bool]:
        """Initialize plugin resources."""
        print(f"Initializing {self.name}...")
        # Setup any resources here
        return FlextResult[None].ok(True)

    async def execute(self, data: Dict[str, Any]) -> FlextResult[Dict[str, Any]]:
        """Generate greeting based on input data."""
        try:
            # Validate plugin is active
            if self.status != PluginStatus.ACTIVE:
                return FlextResult[None].fail("Plugin not active")

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

            return FlextResult[None].ok(result)

        except Exception as e:
            return FlextResult[None].fail(f"Execution failed: {e}")

    async def cleanup(self) -> FlextResult[bool]:
        """Cleanup plugin resources."""
        print(f"Cleaning up {self.name}...")
        return FlextResult[None].ok(True)

# Usage example
async def demo_custom_plugin():
from flext_plugin import create_flext_plugin_platform

    # Create platform and plugin
    platform = create_flext_plugin_platform()
    plugin = GreetingPlugin()

    try:
        # Register and activate
        await platform.register_plugin(plugin)
        await platform.activate_plugin(plugin.name)

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
            result = await platform.execute_plugin(plugin.name, test_data)
            if result.success():
                data = result.data
                print(f"✅ {data['greeting']} (Language: {data['language']})")
            else:
                print(f"❌ Failed: {result.error}")

    finally:
        await platform.shutdown()

if __name__ == "__main__":
    asyncio.run(demo_custom_plugin())
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
import asyncio
from flext_plugin.application.services import FlextPluginDiscoveryService

async def discover_plugins():
    """Discover plugins in current directory."""
    discovery = FlextPluginDiscoveryService()

    # Discover plugins (this will scan for Python files with plugin classes)
    result = await discovery.discover_plugins("./")

    if result.success():
        plugins = result.data
        print(f"Found {len(plugins)} plugins:")
        for plugin in plugins:
            print(f"  - {plugin.name} v{plugin.plugin_version} ({plugin.status})")
    else:
        print(f"Discovery failed: {result.error}")

# Run discovery
asyncio.run(discover_plugins())
```

## Testing Your Plugin

Create `test_greeting_plugin.py`:

```python
import pytest
import asyncio
from custom_plugin import GreetingPlugin
from flext_plugin import create_flext_plugin_platform

class TestGreetingPlugin:
    """Test suite for GreetingPlugin."""

    @pytest.fixture
    def plugin(self):
        """Create plugin instance."""
        return GreetingPlugin()

    @pytest.fixture
    async def platform(self):
        """Create test platform."""
        platform = create_flext_plugin_platform(config={"test_mode": True})
        yield platform
        await platform.shutdown()

    def test_plugin_creation(self, plugin):
        """Test plugin creation."""
        assert plugin.name == "greeting-generator"
        assert plugin.plugin_version == "1.0.0"
        assert plugin.is_valid()

    async def test_plugin_initialization(self, plugin):
        """Test plugin initialization."""
        result = await plugin.initialize()
        assert result.success()

    async def test_greeting_generation(self, plugin):
        """Test greeting generation."""
        await plugin.initialize()
        plugin.activate()

        # Test English greeting
        result = await plugin.execute({"name": "Test", "language": "english"})
        assert result.success()
        assert result.data["greeting"] == "Hello, Test!"

        # Test Spanish greeting
        result = await plugin.execute({"name": "Test", "language": "spanish"})
        assert result.success()
        assert result.data["greeting"] == "¡Hola, Test!"

    async def test_platform_integration(self, platform, plugin):
        """Test plugin integration with platform."""
        # Register plugin
        register_result = await platform.register_plugin(plugin)
        assert register_result.success()

        # Activate plugin
        activate_result = await platform.activate_plugin(plugin.name)
        assert activate_result.success()

        # Execute through platform
        execute_result = await platform.execute_plugin(
            plugin.name,
            {"name": "Platform", "language": "english"}
        )
        assert execute_result.success()
        assert "Hello, Platform!" in str(execute_result.data)

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
import asyncio
from flext_plugin.hot_reload import enable_hot_reload
from flext_plugin import create_flext_plugin_platform

async def development_server():
    """Development server with hot reload."""

    # Enable hot reload
    await enable_hot_reload(
        watch_paths=["./"],  # Watch current directory
        reload_on_change=True
    )

    # Create platform
    platform = create_flext_plugin_platform(config={
        "hot_reload": True,
        "debug": True
    })

    print("🔥 Hot reload enabled!")
    print("Modify plugin files to see live updates...")
    print("Press Ctrl+C to stop")

    try:
        # Keep server running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down development server...")
        await platform.shutdown()

# Run development server
asyncio.run(development_server())
```

## Quality Gates

FLEXT Plugin includes comprehensive quality gates. Set them up for your project:

```bash
# Install development dependencies
poetry add --group dev ruff mypy pytest pytest-cov bandit

# Create basic pyproject.toml configuration
cat > pyproject.toml << EOF
extend = "../.ruff-shared.toml"
lint.isort.known-first-party = ["flext_plugin"]

[tool.mypy]
python_version = "3.13"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=. --cov-report=term-missing"
EOF

# Run quality checks
ruff check .          # Linting
mypy .               # Type checking
pytest               # Testing
bandit -r .          # Security scanning
```

## Next Steps

Now that you have a basic understanding of FLEXT Plugin, explore these topics:

### Immediate Next Steps

1. **[Plugin Development Guide](plugin-development.md)** - Learn advanced plugin patterns
2. **[Testing Guide](testing.md)** - Comprehensive testing strategies
3. **[Examples](../examples/README.md)** - More detailed examples

### Plugin Types to Explore

1. **[Singer Integration](singer-integration.md)** - Create data extraction/loading plugins
2. **[Service Plugins](service-plugins.md)** - Build microservice integrations
3. **[Custom Plugin Types](custom-plugin-types.md)** - Define your own plugin categories

### Advanced Topics

1. **[Architecture Guide](../architecture/README.md)** - Understand the system design
2. **[Performance Optimization](performance-optimization.md)** - Scale your plugins
3. **[FLEXT Ecosystem Integration](ecosystem-integration.md)** - Integrate with other FLEXT services

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
await plugin.initialize()
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

- **Documentation**: Browse the [complete documentation](../README.md)
- **Examples**: Check [practical examples](../examples/README.md)
- **Issues**: [Report bugs](https://github.com/flext-sh/flext/issues)
- **Discussions**: [Ask questions](https://github.com/flext-sh/flext/discussions)

---

🎉 **Congratulations!** You've successfully created your first FLEXT Plugin. Continue with the [Plugin Development Guide](plugin-development.md) to learn advanced patterns and best practices.
