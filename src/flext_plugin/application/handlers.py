"""FLEXT Plugin Application Handlers - CQRS command and event handlers.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextPlugin, FlextResult
from flext_core.handlers import FlextBaseHandler

from flext_plugin.application.services import FlextPluginService


class FlextPluginHandler(FlextBaseHandler):
    """Base command handler for plugin-related operations with service coordination."""

    def __init__(self, plugin_service: FlextPluginService | None = None) -> None:
      """Initialize plugin command handler with service dependency.

      Sets up the base command handler with optional plugin service injection.
      The service can be provided during initialization or injected later
      through dependency injection patterns.

      Args:
          plugin_service: FlextPluginService instance for business logic execution.
                        If None, handlers should gracefully handle missing service
                        or expect service injection through other mechanisms.

      Note:
          Handlers should validate service availability before attempting
          operations and provide appropriate error messages when services
          are unavailable.

      """
      super().__init__()
      self._plugin_service = plugin_service


class FlextPluginRegistrationHandler(FlextPluginHandler):
    """Specialized CQRS command handler for plugin registration operations."""

    def handle_register_plugin(self, plugin: FlextPlugin) -> FlextResult[bool]:
      """Handle plugin registration command.

      Args:
          plugin: Plugin to register
      Returns:
          FlextResult indicating success or failure

      """
      try:
          # Validation logic
          if not plugin.name:
              return FlextResult.fail("Plugin name is required")
          if not plugin.version:
              return FlextResult.fail("Plugin version is required")
          if self._plugin_service is None:
              return FlextResult.fail("Plugin service not available")
          # Use real plugin service to register plugin
          return self._plugin_service.load_plugin(plugin)
      except (RuntimeError, ValueError, TypeError) as e:
          return FlextResult.fail(f"Failed to register plugin: {e}")

    def handle_unregister_plugin(self, plugin_name: str) -> FlextResult[bool]:
      """Handle plugin unregistration command.

      Args:
          plugin_name: Name of plugin to unregister
      Returns:
          FlextResult indicating success or failure

      """
      try:
          if not plugin_name:
              return FlextResult.fail("Plugin name is required")
          if self._plugin_service is None:
              return FlextResult.fail("Plugin service not available")
          # Use real plugin service to unregister plugin
          return self._plugin_service.unload_plugin(plugin_name)
      except (RuntimeError, ValueError, TypeError) as e:
          return FlextResult.fail(f"Failed to unregister plugin: {e}")


class FlextPluginEventHandler(FlextBaseHandler):
    """CQRS event handler for plugin lifecycle events and domain event processing."""

    def handle_plugin_loaded(self, plugin: FlextPlugin) -> FlextResult[bool]:
      """Handle plugin loaded event.

      Args:
          plugin: Plugin that was loaded
      Returns:
          FlextResult indicating success or failure

      """
      try:
          # Log plugin loaded event
          getattr(plugin, "name", "unknown")
          getattr(plugin, "version", "unknown")
          # In a real implementation, this could:
          # - Log the event to observability system
          # - Notify other services
          # - Update plugin registry metrics
          # For now, we consider successful if plugin has required attributes
          if not hasattr(plugin, "name") or not plugin.name:
              return FlextResult.fail("Plugin loaded event: plugin missing name")
          return FlextResult.ok(data=True)
      except (RuntimeError, ValueError, TypeError) as e:
          return FlextResult.fail(f"Failed to handle plugin loaded event: {e}")

    def handle_plugin_unloaded(self, plugin_name: str) -> FlextResult[None]:
      """Handle plugin unloaded event.

      Args:
          plugin_name: Name of plugin that was unloaded
      Returns:
          FlextResult indicating success or failure

      """
      try:
          if not plugin_name or not plugin_name.strip():
              return FlextResult.fail(
                  "Plugin unloaded event: plugin name is required",
              )
          # In a real implementation, this could:
          # - Log the unload event to observability system
          # - Clean up plugin-specific resources
          # - Update plugin registry metrics
          # - Notify dependent services
          # For now, we validate plugin_name and consider it successful
          return FlextResult.ok(None)
      except (RuntimeError, ValueError, TypeError) as e:
          return FlextResult.fail(f"Failed to handle plugin unloaded event: {e}")
