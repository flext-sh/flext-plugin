# Getting Started with FLEXT Plugin

**Version**: 0.9.9 RC
**Last Updated**: 2025-09-17

---

## Prerequisites

- **Python 3.13+** with Poetry
- **FLEXT Workspace** - flext-plugin is part of the FLEXT ecosystem
- Basic understanding of Clean Architecture and domain-driven design

---

## Installation

### Development Installation (Recommended)

```bash
# Clone FLEXT workspace
git clone https://github.com/flext-sh/flext.git
cd flext/flext-plugin

# Setup development environment
make setup

# Verify installation
python -c "import flext_plugin; print(f'Version: {flext_plugin.__version__}')"
```

### Dependencies

flext-plugin integrates with these FLEXT ecosystem components:

```bash
# Core dependencies (automatically installed)
flext-core>=0.9.9        # Foundation patterns and FlextResult
flext-observability>=0.9.9  # Monitoring and observability
```

---

## First Plugin

### Create a Basic Plugin

```python
from flext_plugin import FlextPluginPlatform, create_flext_plugin
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import FlextHandlers
from flext_core import FlextLogger
from flext_core import FlextMixins
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import FlextProtocols
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import FlextTypes
from flext_core import FlextUtilities

# Create plugin platform
platform = FlextPluginPlatform()

# Create a simple plugin
plugin = create_flext_plugin(
    name="hello-world",
    version="0.9.9",
    config={
        "description": "A basic plugin example",
        "author": "FLEXT Developer"
    }
)

# Load and activate plugin
load_result = platform.load_plugin(plugin)
if load_result.success:
    print(f"Plugin {plugin.name} loaded successfully")

    activate_result = platform.enable_plugin("hello-world")
    if activate_result.success:
        print("Plugin activated")
```

### Plugin Discovery

```python
from flext_plugin import FlextPluginPlatform

platform = FlextPluginPlatform()

# Discover plugins in directory
discovery_result = platform.scan_directory("./plugins")
if discovery_result.success:
    plugins = discovery_result.data
    print(f"Found {len(plugins)} plugins")
    for plugin in plugins:
        print(f"- {plugin.name} v{plugin.plugin_version}")
```

---

## Configuration

### Environment Variables

```bash
# Plugin discovery paths
export FLEXT_PLUGIN_DISCOVERY_PATHS="plugins:~/.flext/plugins:/opt/flext/plugins"

# Hot reload settings
export FLEXT_PLUGIN_HOT_RELOAD=true
export FLEXT_PLUGIN_WATCH_INTERVAL=2
```

### Plugin Directory Structure

```
plugins/
├── my_plugin/
│   ├── __init__.py
│   ├── plugin.py      # Plugin implementation
│   └── config.json    # Plugin configuration
└── another_plugin/
    ├── __init__.py
    └── plugin.py
```

---

## Development Commands

```bash
# Setup and validation
make setup                 # Complete development setup
make validate              # Full validation pipeline
make check                 # Quick lint and type check

# Testing
make test                  # Run all tests
make coverage-html         # Generate coverage report

# Plugin development
make plugin-validate       # Validate plugin system
make plugin-watch          # Enable hot reload for development
```

---

## Next Steps

- **[Architecture](architecture.md)** - Understand the plugin system design
- **[API Reference](api-reference.md)** - Complete API documentation
- **[Examples](examples/)** - Working code examples
- **[Development](development.md)** - Contributing guidelines

---

For advanced usage and integration patterns, see the complete documentation in the [docs/](.) directory.
