"""FLEXT Simple Plugin System - Lightweight plugin base classes and utilities.

This module provides simplified plugin base classes and utilities for
rapid plugin development and prototyping. The simple plugin system
offers a lightweight alternative to the full domain entity system
while maintaining compatibility and integration capabilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import importlib
from typing import override

from flext_core import (
    FlextLogger,
    FlextResult,
    FlextService,
    FlextTypes,
)


class Plugin(FlextService[None]):
    """Lightweight plugin base class with essential lifecycle management.

    Simplified plugin implementation providing basic lifecycle management,
    activation/deactivation capabilities, and integration with FLEXT patterns.
    This class serves as a lightweight alternative to full domain entities
    while maintaining compatibility with the broader plugin ecosystem.

    Extends FlextService and integrates flext-core components:
    - FlextService for consistent service behavior
    - FlextLogger for structured logging
    - FlextResult for type-safe error handling

    The Plugin class provides essential functionality for plugin development
    without the complexity of full domain modeling, making it suitable for
    rapid prototyping, simple implementations, and educational purposes.

    Key Features:
      - Basic lifecycle management (activate/deactivate)
      - FlextResult integration for consistent error handling
      - FlextLogger for structured plugin operation logging
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
      ...     result: FlextResult[object] = plugin.execute(my_data)

    """

    @override
    def __init__(self, name: str) -> None:
        """Initialize plugin with a name."""
        super().__init__()
        self.name = name
        self.active = False
        self._logger = FlextLogger(f"{__name__}.{name}")

    def activate(self) -> FlextResult[None]:
        """Activate plugin with logging and validation."""
        try:
            if self.active:
                return FlextResult[None].fail("Plugin is already active")

            self.active = True
            self._logger.info("Plugin activated successfully")
            return FlextResult[None].ok(None)

        except Exception as e:
            error_msg = f"Plugin activation failed: {e}"
            self._logger.error("Plugin activation error", extra={"error": error_msg})
            return FlextResult[None].fail(error_msg)

    def deactivate(self) -> FlextResult[None]:
        """Deactivate plugin with logging and validation."""
        try:
            if not self.active:
                return FlextResult[None].fail("Plugin is not active")

            self.active = False
            self._logger.info("Plugin deactivated successfully")
            return FlextResult[None].ok(None)

        except Exception as e:
            error_msg = f"Plugin deactivation failed: {e}"
            self._logger.error("Plugin deactivation error", extra={"error": error_msg})
            return FlextResult[None].fail(error_msg)


class PluginRegistry:
    """Simple plugin registry."""

    @override
    def __init__(self: object) -> None:
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

    def list_plugins(self: object) -> FlextTypes.StringList:
        """List all registered plugins."""
        return list(self.plugins.keys())

    @staticmethod
    def load_plugin(
        module_name: str, class_name: str = "Plugin"
    ) -> FlextResult[Plugin]:
        """Load a plugin from module."""
        try:
            module = importlib.import_module(module_name)
            plugin_class = getattr(module, class_name)
            plugin = plugin_class()
            return FlextResult[Plugin].ok(plugin)
        except ImportError as e:
            return FlextResult[Plugin].fail(f"Module import failed: {e}")
        except AttributeError as e:
            return FlextResult[Plugin].fail(f"Plugin class not found: {e}")
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[Plugin].fail(f"Plugin loading failed: {e}")
        except Exception as e:
            return FlextResult[Plugin].fail(f"Plugin loading failed: {e}")

    @staticmethod
    def create_registry() -> PluginRegistry:
        """Create a new plugin registry."""
        return PluginRegistry()


__all__ = [
    "Plugin",
    "PluginRegistry",
]
