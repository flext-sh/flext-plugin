"""FLEXT Simple Plugin System - Lightweight plugin base classes and utilities.

This module provides simplified plugin base classes and utilities for
rapid plugin development and prototyping. The simple plugin system
offers a lightweight alternative to the full domain entity system
while maintaining compatibility and integration capabilities.

The simple plugin system is designed for scenarios where full domain
modeling complexity is not required but integration with the broader
FLEXT plugin management system is still desired.

Key Components:
    - Plugin: Lightweight base class for simple plugin implementations
    - SimplePluginManager: Basic plugin management and lifecycle
    - Integration utilities for FLEXT ecosystem compatibility

Use Cases:
    - Rapid prototyping and development
    - Simple plugin implementations without complex domain logic
    - Educational and demonstration purposes
    - Integration with legacy plugin systems

Example:
    >>> from flext_plugin.simple_plugin import Plugin
    >>>
    >>> class MyPlugin(Plugin):
    ...     def execute(self):
    ...         return f"Plugin {self.name} executing"
    >>>
    >>> plugin = MyPlugin("my-plugin")
    >>> result = plugin.activate()
    >>> if result.success():
    ...     print("Plugin activated successfully")

Integration:
    - Compatible with FLEXT plugin management system
    - Uses flext-core FlextResult patterns for consistency
    - Provides upgrade path to full domain entities
    - Supports comprehensive testing and validation

"""

from __future__ import annotations

import importlib

from flext_core import FlextResult


class Plugin:
    """Lightweight plugin base class with essential lifecycle management.

    Simplified plugin implementation providing basic lifecycle management,
    activation/deactivation capabilities, and integration with FLEXT patterns.
    This class serves as a lightweight alternative to full domain entities
    while maintaining compatibility with the broader plugin ecosystem.

    The Plugin class provides essential functionality for plugin development
    without the complexity of full domain modeling, making it suitable for
    rapid prototyping, simple implementations, and educational purposes.

    Key Features:
      - Basic lifecycle management (activate/deactivate)
      - FlextResult integration for consistent error handling
      - Extensible design for custom plugin implementations
      - Compatibility with FLEXT plugin management system
      - Minimal resource footprint and complexity

    Lifecycle States:
      - Inactive: Plugin created but not activated
      - Active: Plugin activated and ready for execution

    Usage Pattern:
      Extend this class to create custom plugin implementations,
      overriding methods as needed for specific functionality.

    Example:
      >>> class DataProcessorPlugin(Plugin):
      ...     def execute(self, data):
      ...         if not self.active:
      ...             return FlextResult[None].fail("Plugin not active")
      ...         # Process data
      ...         return FlextResult[None].ok(processed_data)
      >>>
      >>> plugin = DataProcessorPlugin("data-processor")
      >>> activation = plugin.activate()
      >>> if activation.success():
      ...     result = plugin.execute(my_data)

    """

    def __init__(self, name: str) -> None:
        """Initialize plugin with a name."""
        self.name = name
        self.active = False

    def activate(self) -> FlextResult[None]:
        """Activate plugin."""
        try:
            self.active = True
            return FlextResult[None].ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[None].fail(f"Plugin activation failed: {e}")

    def deactivate(self) -> FlextResult[None]:
        """Deactivate plugin."""
        try:
            self.active = False
            return FlextResult[None].ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[None].fail(f"Plugin deactivation failed: {e}")


class PluginRegistry:
    """Simple plugin registry."""

    def __init__(self) -> None:
        """Initialize empty plugin registry."""
        self.plugins: dict[str, Plugin] = {}

    def register(self, plugin: Plugin) -> FlextResult[None]:
        """Register a plugin."""
        try:
            self.plugins[plugin.name] = plugin
            return FlextResult[None].ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[None].fail(f"Plugin registration failed: {e}")

    def unregister(self, name: str) -> FlextResult[None]:
        """Unregister a plugin."""
        try:
            if name in self.plugins:
                del self.plugins[name]
            return FlextResult[None].ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[None].fail(f"Plugin unregistration failed: {e}")

    def get(self, name: str) -> Plugin | None:
        """Get a plugin by name."""
        return self.plugins.get(name)

    def list_plugins(self) -> list[str]:
        """List all registered plugins."""
        return list(self.plugins.keys())


def load_plugin(module_name: str, class_name: str = "Plugin") -> FlextResult[Plugin]:
    """Load a plugin from module."""
    try:
        module = importlib.import_module(module_name)
        plugin_class = getattr(module, class_name)
        plugin = plugin_class()
        return FlextResult[Plugin].ok(plugin)
    except Exception as e:
        return FlextResult[Plugin].fail(f"Plugin loading failed: {e}")


def create_registry() -> PluginRegistry:
    """Create a new plugin registry."""
    return PluginRegistry()
