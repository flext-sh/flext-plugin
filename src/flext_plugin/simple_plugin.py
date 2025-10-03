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


class PluginRegistry(FlextService[None]):
    """Simple plugin registry with flext-core integration.

    Lightweight plugin registry providing basic registration, unregistration,
    and lookup capabilities with consistent flext-core error handling and logging.
    """

    @override
    def __init__(self) -> None:
        """Initialize empty plugin registry."""
        super().__init__()
        self.plugins: dict[str, Plugin] = {}
        self._logger = FlextLogger(__name__)

    def register(self, plugin: Plugin) -> FlextResult[None]:
        """Register a plugin with validation and logging."""
        try:
            if plugin.name in self.plugins:
                return FlextResult[None].fail(
                    f"Plugin '{plugin.name}' is already registered"
                )

            if not plugin.name:
                return FlextResult[None].fail("Plugin name cannot be empty")

            self.plugins[plugin.name] = plugin
            self._logger.info(
                "Plugin registered successfully", extra={"plugin_name": plugin.name}
            )
            return FlextResult[None].ok(None)

        except Exception as e:
            error_msg = f"Plugin registration failed: {e}"
            self._logger.error("Plugin registration error", extra={"error": error_msg})
            return FlextResult[None].fail(error_msg)

    def unregister(self, name: str) -> FlextResult[None]:
        """Unregister a plugin with validation and logging."""
        try:
            if not name:
                return FlextResult[None].fail("Plugin name cannot be empty")

            if name not in self.plugins:
                return FlextResult[None].fail(f"Plugin '{name}' is not registered")

            del self.plugins[name]
            self._logger.info(
                "Plugin unregistered successfully", extra={"plugin_name": name}
            )
            return FlextResult[None].ok(None)

        except Exception as e:
            error_msg = f"Plugin unregistration failed: {e}"
            self._logger.error(
                "Plugin unregistration error",
                extra={"error": error_msg, "plugin_name": name},
            )
            return FlextResult[None].fail(error_msg)

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
        """Load a plugin from module with comprehensive error handling."""
        logger = FlextLogger(__name__)

        try:
            logger.info(
                "Loading plugin from module",
                extra={"module_name": module_name, "class_name": class_name},
            )

            module = importlib.import_module(module_name)
            plugin_class = getattr(module, class_name)

            if not issubclass(plugin_class, Plugin):
                error_msg = f"Class '{class_name}' does not inherit from Plugin"
                logger.error("Invalid plugin class", extra={"error": error_msg})
                return FlextResult[Plugin].fail(error_msg)

            plugin = plugin_class()
            logger.info(
                "Plugin loaded successfully", extra={"plugin_name": plugin.name}
            )
            return FlextResult[Plugin].ok(plugin)

        except ImportError as e:
            error_msg = f"Module import failed: {e}"
            logger.error(
                "Plugin import error", extra={"error": error_msg, "module": module_name}
            )
            return FlextResult[Plugin].fail(error_msg)

        except AttributeError as e:
            error_msg = (
                f"Plugin class '{class_name}' not found in module '{module_name}': {e}"
            )
            logger.error("Plugin class not found", extra={"error": error_msg})
            return FlextResult[Plugin].fail(error_msg)

        except Exception as e:
            error_msg = f"Plugin loading failed: {e}"
            logger.error(
                "Plugin loading error",
                extra={"error": error_msg, "module": module_name, "class": class_name},
            )
            return FlextResult[Plugin].fail(error_msg)

    @staticmethod
    def create_registry() -> PluginRegistry:
        """Create a new plugin registry."""
        return PluginRegistry()


__all__ = [
    "Plugin",
    "PluginRegistry",
]
