"""FLEXT Plugin Application Handlers - CQRS command and event handlers.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import override

from flext_core import FlextResult

from flext_plugin.entities import FlextPluginEntity
from flext_plugin.ports import FlextPluginLoaderPort


class FlextPluginHandler:
    """Base handler for plugin operations."""

    @override
    def __init__(self, plugin_service: FlextPluginLoaderPort | None = None) -> None:
        """Initialize handler with optional plugin service."""
        self._plugin_service = plugin_service


class FlextPluginRegistrationHandler(FlextPluginHandler):
    """Specialized CQRS command handler for plugin registration operations."""

    def handle_register_plugin(self, plugin: FlextPluginEntity) -> FlextResult[bool]:
        """Handle plugin registration command.

        Args:
            plugin: Plugin to register
        Returns:
            FlextResult indicating success or failure

        """
        try:
            # Validation logic
            if not plugin.name:
                return FlextResult[bool].fail("Plugin name is required")
            if not plugin.plugin_version:
                return FlextResult[bool].fail("Plugin version is required")
            if self._plugin_service is None:
                return FlextResult[bool].fail("Plugin service not available")
            # Use real plugin service to register plugin
            return self._plugin_service.load_plugin(plugin)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[bool].fail(f"Failed to register plugin: {e}")

    def handle_unregister_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Handle plugin unregistration command.

        Args:
            plugin_name: Name of plugin to unregister
        Returns:
            FlextResult indicating success or failure

        """
        try:
            if not plugin_name:
                return FlextResult[bool].fail("Plugin name is required")
            if self._plugin_service is None:
                return FlextResult[bool].fail("Plugin service not available")
            # Use real plugin service to unregister plugin
            return self._plugin_service.unload_plugin(plugin_name)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[bool].fail(f"Failed to unregister plugin: {e}")


class FlextPluginEventHandler:
    """CQRS event handler for plugin lifecycle events and domain event processing."""

    def handle_plugin_loaded(self, plugin: FlextPluginEntity) -> FlextResult[bool]:
        """Handle plugin loaded event.

        Args:
            plugin: Plugin that was loaded
        Returns:
            FlextResult indicating success or failure

        """
        try:
            # Log plugin loaded event
            getattr(plugin, "name", "unknown")
            getattr(plugin, "plugin_version", "unknown")
            # In a real implementation, this could:
            # - Log the event to observability system
            # - Notify other services
            # - Update plugin registry metrics
            # For now, we consider successful if plugin has required attributes
            if not hasattr(plugin, "name") or not plugin.name:
                return FlextResult[bool].fail(
                    "Plugin loaded event: plugin missing name",
                )
            return FlextResult[bool].ok(data=True)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[bool].fail(f"Failed to handle plugin loaded event: {e}")

    def handle_plugin_unloaded(self, plugin_name: str) -> FlextResult[None]:
        """Handle plugin unloaded event.

        Args:
            plugin_name: Name of plugin that was unloaded
        Returns:
            FlextResult indicating success or failure

        """
        try:
            if not plugin_name or not plugin_name.strip():
                return FlextResult[None].fail(
                    "Plugin unloaded event: plugin name is required",
                )
            # In a real implementation, this could:
            # - Log the unload event to observability system
            # - Clean up plugin-specific resources
            # - Update plugin registry metrics
            # - Notify dependent services
            # For now, we validate plugin_name and consider it successful
            return FlextResult[None].ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[None].fail(
                f"Failed to handle plugin unloaded event: {e}",
            )


__all__ = [
    "FlextPluginEventHandler",
    "FlextPluginHandler",
    "FlextPluginRegistrationHandler",
]
