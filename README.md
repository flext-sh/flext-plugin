# FLEXT-Plugin

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**FLEXT-Plugin** is the extensible engine powering the [FLEXT data integration ecosystem](https://github.com/flext/flext). It provides comprehensive lifecycle management for plugins, enabling dynamic component discovery, secure validation, and hot-reload capabilities across all FLEXT projects.

**Reviewed**: 2026-02-17 | **Version**: 0.10.0-dev

Part of the [FLEXT](https://github.com/flext/flext) ecosystem.

## 🚀 Key Features

- **Plugin Discovery**: Dual support for file-based plugins (`.py` files in directories) and entry-point based plugins (installed packages via `importlib.metadata`).
- **Lifecycle Management**: Fine-grained control with `load`, `unload`, `enable`, and `disable` operations.
- **Hot Reload**: Live monitoring of plugin directories with automatic reloading on file changes (via `watchdog`).
- **Security & Validation**: Sandboxed execution and rigorous validation of plugin metadata and structure.
- **FLEXT Integration**: Built on foundational `flext-core` patterns (`FlextResult`, `FlextContainer`) for seamless interoperability.
- **Clean Architecture**: Separation of concerns with distinct layers for domain logic, service orchestration, and infrastructure adapters.

## 📦 Installation

To install `flext-plugin`:

```bash
pip install flext-plugin
```

Or with Poetry:

```bash
poetry add flext-plugin
```

## 🛠️ Usage

### Plugin Discovery

Scan directories for available plugins.

```python
from flext_plugin import FlextPluginPlatform, FlextContainer

# 1. Initialize Platform
container = FlextContainer()
platform = FlextPluginPlatform(container)

# 2. Discover Plugins
discovery_result = platform.discover_plugins("./plugins_directory")

if discovery_result.is_success:
    plugins = discovery_result.unwrap()
    print(f"Discovered {len(plugins)} plugins:")
    for plugin in plugins:
        print(f" - {plugin.name} v{plugin.version}: {plugin.description}")
```

### Loading and Managing Plugins

Load, enable, and disable plugins dynamically.

```python
# 1. Load a Plugin
load_result = platform.load_plugin("my-custom-transform")

if load_result.is_success:
    plugin_instance = load_result.unwrap()
    
    # 2. Enable Plugin
    platform.enable_plugin(plugin_instance.name)
    print(f"Plugin {plugin_instance.name} is active.")

    # 3. Disable Plugin
    platform.disable_plugin(plugin_instance.name)
```

### Hot Reload

Enable automatic reloading for development workflows.

```python
# 1. Enable Watcher
platform.enable_hot_reload("./plugins_directory")
print("Watching for plugin changes...")

# Making changes to Python files in the directory will trigger 
# automatic reloading of associated plugins.
```

## 🏗️ Architecture

FLEXT-Plugin is designed as the core extensibility framework:

- **Facade Layer**: `FlextPluginPlatform` provides a simple, unified API for all operations.
- **Service Layer**: Orchestrates discovery, loading, and state management logic.
- **Infrastructure Layer**: Handles file system monitoring and dynamic import mechanics.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/development.md) for details on creating new plugins, enhancing the discovery engine, and submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
