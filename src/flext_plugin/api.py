"""FLEXT Plugin API - Unified plugin system API.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Any

from flext_core import FlextContainer, FlextLogger, FlextResult

from flext_plugin.adapters import FlextPluginAdapters
from flext_plugin.config import FlextPluginConfig
from flext_plugin.discovery import FlextPluginDiscovery
from flext_plugin.entities import FlextPluginEntities
from flext_plugin.handlers import FlextPluginHandlers
from flext_plugin.hot_reload import FlextPluginHotReload
from flext_plugin.loader import FlextPluginLoader
from flext_plugin.platform import FlextPluginPlatform
from flext_plugin.services import FlextPluginService


class FlextPluginApi:
    """Unified API for the FLEXT Plugin System.

    This class provides a single entry point for all plugin operations,
    orchestrating the various components of the plugin system to deliver
    a comprehensive and easy-to-use interface.

    Usage:
        ```python
        from flext_plugin import FlextPluginApi
        from flext_core import FlextContainer

        # Initialize API
        container = FlextContainer()
        api = FlextPluginApi(container)

        # Discover and load plugins
        result = api.discover_plugins(["./plugins"])
        if result.success:
            plugins = result.value
            print(f"Discovered {len(plugins)} plugins")

        # Execute a plugin
        execution_result = api.execute_plugin("my-plugin", {"input": "data"})
        ```
    """

    def __init__(
        self,
        container: FlextContainer | None = None,
        config: FlextPluginConfig | None = None,
    ) -> None:
        """Initialize the plugin API.

        Args:
            container: FLEXT dependency injection container
            config: Optional plugin configuration

        """
        self.logger = FlextLogger(__name__)
        self.container = container or FlextContainer()
        self.config = config or FlextPluginConfig()

        # Initialize core components
        self._adapters = FlextPluginAdapters()
        self._discovery = FlextPluginDiscovery()
        self._loader = FlextPluginLoader()
        self._handlers = FlextPluginHandlers()
        self._hot_reload = FlextPluginHotReload()
        self._platform = FlextPluginPlatform(self.container, self.config)
        self._service = FlextPluginService()

        # Register default handlers
        self._handlers.register_default_handlers()

    def discover_plugins(
        self, paths: list[str]
    ) -> FlextResult[list[FlextPluginEntities.Plugin]]:
        """Discover plugins in the specified paths.

        Args:
            paths: List of paths to search for plugins

        Returns:
            FlextResult containing list of discovered plugins

        """
        try:
            # Use discovery service
            discovery_result = self._discovery.discover_plugins(paths)
            if discovery_result.is_failure:
                return FlextResult.fail(f"Discovery failed: {discovery_result.error}")

            plugins_data = discovery_result.value
            plugins = []

            for plugin_data in plugins_data:
                # Create plugin entity
                plugin = FlextPluginEntities.Plugin.create(
                    name=plugin_data["name"],
                    plugin_version=plugin_data.get("version", "1.0.0"),
                    config=plugin_data,
                )

                # Validate plugin
                validation_result = plugin.validate_business_rules()
                if validation_result.is_failure:
                    self.logger.warning(
                        f"Plugin {plugin.name} validation failed: {validation_result.error}"
                    )
                    continue

                plugins.append(plugin)

                # Trigger discovery event
                self._handlers.trigger_event(
                    "plugin_discovered",
                    {
                        "plugin_name": plugin.name,
                        "plugin_version": plugin.plugin_version,
                        "plugin_type": plugin.plugin_type,
                    },
                )

            self.logger.info(f"Discovered {len(plugins)} plugins")
            return FlextResult.ok(plugins)

        except Exception as e:
            self.logger.exception("Plugin discovery failed")
            return FlextResult.fail(f"Discovery error: {e!s}")

    def load_plugin(self, plugin_path: str) -> FlextResult[FlextPluginEntities.Plugin]:
        """Load a single plugin from the specified path.

        Args:
            plugin_path: Path to the plugin to load

        Returns:
            FlextResult containing the loaded plugin

        """
        try:
            # Use loader service
            load_result = self._loader.load_plugin(plugin_path)
            if load_result.is_failure:
                return FlextResult.fail(f"Plugin loading failed: {load_result.error}")

            plugin_data = load_result.value
            plugin = FlextPluginEntities.Plugin.create(
                name=plugin_data["name"],
                plugin_version=plugin_data.get("version", "1.0.0"),
                config=plugin_data,
            )

            # Validate plugin
            validation_result = plugin.validate_business_rules()
            if validation_result.is_failure:
                return FlextResult.fail(
                    f"Plugin validation failed: {validation_result.error}"
                )

            # Trigger load event
            self._handlers.trigger_event(
                "plugin_loaded",
                {
                    "plugin_name": plugin.name,
                    "plugin_version": plugin.plugin_version,
                    "plugin_path": plugin_path,
                },
            )

            self.logger.info(f"Loaded plugin: {plugin.name}")
            return FlextResult.ok(plugin)

        except Exception as e:
            self.logger.exception(f"Failed to load plugin from {plugin_path}")
            return FlextResult.fail(f"Loading error: {e!s}")

    def execute_plugin(
        self,
        plugin_name: str,
        context: dict[str, Any],
        execution_id: str | None = None,
    ) -> FlextResult[FlextPluginEntities.Execution]:
        """Execute a plugin with the given context.

        Args:
            plugin_name: Name of the plugin to execute
            context: Execution context data
            execution_id: Optional execution ID

        Returns:
            FlextResult containing the execution result

        """
        try:
            # Use platform for execution
            execution_result = self._platform.execute_plugin(
                plugin_name, context, execution_id
            )

            if execution_result.is_success:
                execution = execution_result.value
                # Trigger execution event
                self._handlers.trigger_event(
                    "plugin_executed",
                    {
                        "plugin_name": plugin_name,
                        "execution_id": execution.execution_id,
                        "success": execution.success,
                        "execution_time": execution.execution_time,
                    },
                )

            return execution_result

        except Exception as e:
            self.logger.exception(f"Failed to execute plugin '{plugin_name}'")
            return FlextResult.fail(f"Execution error: {e!s}")

    def register_plugin(self, plugin: FlextPluginEntities.Plugin) -> FlextResult[bool]:
        """Register a plugin in the platform.

        Args:
            plugin: Plugin entity to register

        Returns:
            FlextResult indicating success or failure

        """
        try:
            # Use platform for registration
            register_result = self._platform.register_plugin(plugin)
            if register_result.is_success:
                # Trigger registration event
                self._handlers.trigger_event(
                    "plugin_registered",
                    {
                        "plugin_name": plugin.name,
                        "plugin_version": plugin.plugin_version,
                    },
                )

            return register_result

        except Exception as e:
            self.logger.exception(f"Failed to register plugin '{plugin.name}'")
            return FlextResult.fail(f"Registration error: {e!s}")

    def unregister_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Unregister a plugin from the platform.

        Args:
            plugin_name: Name of the plugin to unregister

        Returns:
            FlextResult indicating success or failure

        """
        try:
            # Use platform for unregistration
            unregister_result = self._platform.unregister_plugin(plugin_name)
            if unregister_result.is_success:
                # Trigger unregistration event
                self._handlers.trigger_event(
                    "plugin_unregistered",
                    {
                        "plugin_name": plugin_name,
                    },
                )

            return unregister_result

        except Exception as e:
            self.logger.exception(f"Failed to unregister plugin '{plugin_name}'")
            return FlextResult.fail(f"Unregistration error: {e!s}")

    def start_hot_reload(self, paths: list[str]) -> FlextResult[bool]:
        """Start hot reload monitoring for the specified paths.

        Args:
            paths: List of paths to monitor for changes

        Returns:
            FlextResult indicating success or failure

        """
        try:
            # Use hot reload service
            start_result = self._hot_reload.start_watching(paths)
            if start_result.is_success:
                # Add reload callback
                self._hot_reload.add_reload_callback(self._handle_plugin_reload)

            return start_result

        except Exception as e:
            self.logger.exception("Failed to start hot reload")
            return FlextResult.fail(f"Hot reload error: {e!s}")

    def stop_hot_reload(self) -> FlextResult[bool]:
        """Stop hot reload monitoring.

        Returns:
            FlextResult indicating success or failure

        """
        try:
            return self._hot_reload.stop_watching()

        except Exception as e:
            self.logger.exception("Failed to stop hot reload")
            return FlextResult.fail(f"Hot reload error: {e!s}")

    def get_plugin(self, plugin_name: str) -> FlextPluginEntities.Plugin | None:
        """Get a plugin by name.

        Args:
            plugin_name: Name of the plugin to retrieve

        Returns:
            Plugin entity if found, None otherwise

        """
        return self._platform.get_plugin(plugin_name)

    def list_plugins(self) -> list[FlextPluginEntities.Plugin]:
        """List all registered plugins.

        Returns:
            List of all registered plugin entities

        """
        return self._platform.list_plugins()

    def get_plugin_status(self, plugin_name: str) -> str | None:
        """Get the status of a specific plugin.

        Args:
            plugin_name: Name of the plugin

        Returns:
            Plugin status if found, None otherwise

        """
        return self._platform.get_plugin_status(plugin_name)

    def is_plugin_active(self, plugin_name: str) -> bool:
        """Check if a plugin is currently active.

        Args:
            plugin_name: Name of the plugin

        Returns:
            True if plugin is active, False otherwise

        """
        return self._platform.is_plugin_active(plugin_name)

    def get_platform_status(self) -> dict[str, Any]:
        """Get the current status of the plugin platform.

        Returns:
            Dictionary containing platform status information

        """
        return self._platform.get_platform_status()

    def get_api_status(self) -> dict[str, Any]:
        """Get the current status of the plugin API.

        Returns:
            Dictionary containing API status information

        """
        platform_status = self.get_platform_status()
        handler_status = self._handlers.get_handler_status()
        hot_reload_status = self._hot_reload.get_hot_reload_status()

        return {
            "platform": platform_status,
            "handlers": handler_status,
            "hot_reload": hot_reload_status,
            "config": {
                "discovery_paths": self.config.get_plugin_paths(),
                "security_enabled": self.config.is_security_enabled(),
                "monitoring_enabled": self.config.is_monitoring_enabled(),
            },
        }

    def _handle_plugin_reload(self, plugin_name: str) -> None:
        """Handle plugin reload event.

        Args:
            plugin_name: Name of the plugin being reloaded

        """
        try:
            # Trigger reload event
            self._handlers.trigger_event(
                "plugin_reloaded",
                {
                    "plugin_name": plugin_name,
                    "timestamp": self._get_current_timestamp(),
                },
            )

            self.logger.info(f"Handled plugin reload: {plugin_name}")

        except Exception:
            self.logger.exception(f"Failed to handle plugin reload: {plugin_name}")

    def _get_current_timestamp(self) -> str:
        """Get current timestamp as ISO string.

        Returns:
            Current timestamp as ISO string

        """
        from datetime import UTC, datetime

        return datetime.now(UTC).isoformat()

    # Convenience methods for common operations

    def discover_and_register_plugins(
        self, paths: list[str]
    ) -> FlextResult[list[FlextPluginEntities.Plugin]]:
        """Discover plugins and register them in the platform.

        Args:
            paths: List of paths to search for plugins

        Returns:
            FlextResult containing list of registered plugins

        """
        try:
            # Discover plugins
            discover_result = self.discover_plugins(paths)
            if discover_result.is_failure:
                return discover_result

            plugins = discover_result.value
            registered_plugins = []

            # Register each plugin
            for plugin in plugins:
                register_result = self.register_plugin(plugin)
                if register_result.is_success:
                    registered_plugins.append(plugin)
                else:
                    self.logger.warning(
                        f"Failed to register plugin {plugin.name}: {register_result.error}"
                    )

            self.logger.info(
                f"Registered {len(registered_plugins)} out of {len(plugins)} discovered plugins"
            )
            return FlextResult.ok(registered_plugins)

        except Exception as e:
            self.logger.exception("Failed to discover and register plugins")
            return FlextResult.fail(f"Discover and register error: {e!s}")

    def execute_plugin_sync(
        self,
        plugin_name: str,
        context: dict[str, Any],
        timeout: float | None = None,
    ) -> FlextResult[Any]:
        """Execute a plugin synchronously and return the result.

        Args:
            plugin_name: Name of the plugin to execute
            context: Execution context data
            timeout: Optional timeout in seconds

        Returns:
            FlextResult containing the execution result data

        """
        try:
            # Execute plugin
            execution_result = self.execute_plugin(plugin_name, context)
            if execution_result.is_failure:
                return execution_result

            execution = execution_result.value
            if not execution.success:
                return FlextResult.fail(f"Plugin execution failed: {execution.error}")

            return FlextResult.ok(execution.result)

        except Exception as e:
            self.logger.exception(
                f"Failed to execute plugin synchronously: {plugin_name}"
            )
            return FlextResult.fail(f"Sync execution error: {e!s}")

    def get_plugin_info(self, plugin_name: str) -> dict[str, Any] | None:
        """Get detailed information about a plugin.

        Args:
            plugin_name: Name of the plugin

        Returns:
            Plugin information dictionary if found, None otherwise

        """
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            return None

        return {
            "name": plugin.name,
            "version": plugin.plugin_version,
            "description": plugin.description,
            "author": plugin.author,
            "status": plugin.status,
            "plugin_type": plugin.plugin_type,
            "created_at": plugin.created_at,
            "is_active": plugin.is_active(),
            "is_healthy": plugin.is_healthy,
            "execution_count": plugin.execution_count,
            "average_execution_time_ms": plugin.average_execution_time_ms,
            "error_count": plugin.error_count,
        }

    def get_execution_history(self, limit: int = 100) -> list[dict[str, Any]]:
        """Get execution history from the platform.

        Args:
            limit: Maximum number of executions to return

        Returns:
            List of execution history records

        """
        executions = self._platform.list_executions()
        if limit > 0:
            executions = executions[-limit:]

        return [
            {
                "execution_id": exec.execution_id,
                "plugin_name": exec.plugin_name,
                "status": exec.status,
                "success": exec.success,
                "execution_time": exec.execution_time,
                "start_time": exec.start_time,
                "end_time": exec.end_time,
                "error": exec.error,
            }
            for exec in executions
        ]

    def get_reload_history(self, limit: int = 100) -> list[dict[str, Any]]:
        """Get hot reload history.

        Args:
            limit: Maximum number of reload records to return

        Returns:
            List of reload history records

        """
        return self._hot_reload.get_reload_history(limit)

    def get_event_history(
        self, event_type: str | None = None, limit: int = 100
    ) -> list[dict[str, Any]]:
        """Get event history from handlers.

        Args:
            event_type: Optional event type to filter by
            limit: Maximum number of events to return

        Returns:
            List of event history records

        """
        return self._handlers.get_event_history(event_type, limit)


__all__ = ["FlextPluginApi"]
