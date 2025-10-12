"""FLEXT Plugin Platform - Main plugin platform facade.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextCore

from flext_plugin.config import FlextPluginConfig
from flext_plugin.entities import FlextPluginEntities
from flext_plugin.protocols import FlextPluginProtocols
from flext_plugin.types import FlextPluginTypes


class FlextPluginPlatform(FlextCore.Service[FlextCore.Result]):
    """Main plugin platform facade providing unified plugin management.

    This is the primary entry point for all plugin operations in the FLEXT ecosystem.
    It orchestrates plugin discovery, loading, execution, and lifecycle management
    through a clean, unified interface.

    Usage:
        ```python
        from flext_plugin import FlextPluginPlatform
        from flext_core import FlextCore

        # Initialize platform
        container = FlextCore.Container()
        platform = FlextPluginPlatform(container)

        # Discover and load plugins
        result = await platform.discover_plugins(["./plugins"])
        if result.success:
            plugins = result.value
            print(f"Discovered {len(plugins)} plugins")

        # Execute a plugin
        execution_result = await platform.execute_plugin("my-plugin", {"input": "data"})
        ```
    """

    def __init__(
        self,
        container: FlextCore.Container,
    ) -> None:
        """Initialize the plugin platform.

        Args:
            container: FLEXT dependency injection container

        """
        super().__init__(container=container, config=FlextPluginConfig())

        # Type annotation for proper type checking
        self.config: FlextPluginConfig

        # Initialize internal state
        self._plugins: dict[str, FlextPluginEntities.Plugin] = {}
        self._executions: dict[str, FlextPluginEntities.Execution] = {}
        self._registry = FlextPluginEntities.Registry.create(name="default")

        # Initialize protocol implementations (will be injected via container)
        self._discovery: FlextPluginProtocols.PluginDiscovery | None = None
        self._loader: FlextPluginProtocols.PluginLoader | None = None
        self._executor: FlextPluginProtocols.PluginExecution | None = None
        self._security: FlextPluginProtocols.PluginSecurity | None = None
        self._hot_reload: FlextPluginProtocols.PluginHotReload | None = None
        self._monitoring: FlextPluginProtocols.PluginMonitoring | None = None

    async def discover_plugins(
        self, paths: FlextCore.Types.StringList
    ) -> FlextCore.Result[list[FlextPluginEntities.Plugin]]:
        """Discover plugins in the specified paths.

        Args:
            paths: List of paths to search for plugins

        Returns:
            FlextCore.Result containing list of discovered plugins

        """
        try:
            if not self._discovery:
                return FlextCore.Result.fail("Plugin discovery not initialized")

            discovery_result = self._discovery.discover_plugins(paths)
            if discovery_result.is_failure:
                return FlextCore.Result.fail(
                    f"Discovery failed: {discovery_result.error}"
                )

            plugins_data = discovery_result.value
            plugins = []

            for plugin_data in plugins_data:
                plugin = FlextPluginEntities.Plugin.create(
                    name=str(plugin_data["name"]),
                    plugin_version=str(plugin_data.get("version", "1.0.0")),
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
                self._plugins[plugin.name] = plugin

            self.logger.info(f"Discovered {len(plugins)} plugins")
            return FlextCore.Result.ok(plugins)

        except Exception as e:
            self.logger.exception("Plugin discovery failed")
            return FlextCore.Result.fail(f"Discovery error: {e!s}")

    async def load_plugin(
        self, plugin_path: str
    ) -> FlextCore.Result[FlextPluginEntities.Plugin]:
        """Load a single plugin from the specified path.

        Args:
            plugin_path: Path to the plugin to load

        Returns:
            FlextCore.Result containing the loaded plugin

        """
        try:
            if not self._loader:
                return FlextCore.Result.fail("Plugin loader not initialized")

            load_result = self._loader.load_plugin(plugin_path)
            if load_result.is_failure:
                return FlextCore.Result.fail(
                    f"Plugin loading failed: {load_result.error}"
                )

            plugin_data = load_result.value
            plugin = FlextPluginEntities.Plugin.create(
                name=str(plugin_data["name"]),
                plugin_version=str(plugin_data.get("version", "1.0.0")),
                config=plugin_data,
            )

            # Validate plugin
            validation_result = plugin.validate_business_rules()
            if validation_result.is_failure:
                return FlextCore.Result.fail(
                    f"Plugin validation failed: {validation_result.error}"
                )

            self._plugins[plugin.name] = plugin
            self.logger.info(f"Loaded plugin: {plugin.name}")
            return FlextCore.Result.ok(plugin)

        except Exception as e:
            self.logger.exception(f"Failed to load plugin from {plugin_path}")
            return FlextCore.Result.fail(f"Loading error: {e!s}")

    async def execute_plugin(
        self,
        plugin_name: str,
        context: FlextCore.Types.Dict,
        execution_id: str | None = None,
    ) -> FlextCore.Result[FlextPluginEntities.Execution]:
        """Execute a plugin with the given context.

        Args:
            plugin_name: Name of the plugin to execute
            context: Execution context data
            execution_id: Optional execution ID (generated if not provided)

        Returns:
            FlextCore.Result containing the execution result

        """
        try:
            if plugin_name not in self._plugins:
                return FlextCore.Result.fail(f"Plugin '{plugin_name}' not found")

            if not self._executor:
                return FlextCore.Result.fail("Plugin executor not initialized")

            # Create execution entity
            execution = FlextPluginEntities.Execution.create(
                plugin_name=plugin_name,
                execution_config={"input_data": context, "status": "pending"},
                execution_id=execution_id,
            )

            # Start execution
            execution.mark_started()
            self._executions[execution.execution_id] = execution

            # Execute plugin
            execution_context: FlextPluginTypes.Execution.ExecutionContext = {
                "plugin_id": plugin_name,
                "execution_id": execution.execution_id,
                "input_data": context,
                "timeout_seconds": self.config.security.max_execution_time,
            }

            exec_result = self._executor.execute_plugin(plugin_name, execution_context)

            if exec_result.is_failure:
                execution.mark_completed(success=False, error_message=exec_result.error)
                return FlextCore.Result.fail(f"Execution failed: {exec_result.error}")

            # Mark execution as completed
            execution.mark_completed(success=True)
            execution.result = exec_result.value

            self.logger.info(f"Executed plugin '{plugin_name}' successfully")
            return FlextCore.Result.ok(execution)

        except Exception as e:
            self.logger.exception(f"Failed to execute plugin '{plugin_name}'")
            return FlextCore.Result.fail(f"Execution error: {e!s}")

    async def register_plugin(
        self, plugin: FlextPluginEntities.Plugin
    ) -> FlextCore.Result[bool]:
        """Register a plugin in the platform registry.

        Args:
            plugin: Plugin entity to register

        Returns:
            FlextCore.Result indicating success or failure

        """
        try:
            # Validate plugin
            validation_result = plugin.validate_business_rules()
            if validation_result.is_failure:
                return FlextCore.Result.fail(
                    f"Plugin validation failed: {validation_result.error}"
                )

            # Register in internal registry
            register_result = self._registry.register(plugin)
            if register_result.is_failure:
                return FlextCore.Result.fail(
                    f"Registration failed: {register_result.error}"
                )

            # Store in platform plugins
            self._plugins[plugin.name] = plugin

            self.logger.info(f"Registered plugin: {plugin.name}")
            return FlextCore.Result.ok(True)

        except Exception as e:
            self.logger.exception(f"Failed to register plugin '{plugin.name}'")
            return FlextCore.Result.fail(f"Registration error: {e!s}")

    async def unregister_plugin(self, plugin_name: str) -> FlextCore.Result[bool]:
        """Unregister a plugin from the platform.

        Args:
            plugin_name: Name of the plugin to unregister

        Returns:
            FlextCore.Result indicating success or failure

        """
        try:
            # Unregister from internal registry
            unregister_result = self._registry.unregister_plugin(plugin_name)
            if not unregister_result:
                return FlextCore.Result.fail(
                    f"Unregistration failed: plugin '{plugin_name}' not found in registry"
                )

            # Remove from platform plugins
            if plugin_name in self._plugins:
                del self._plugins[plugin_name]

            self.logger.info(f"Unregistered plugin: {plugin_name}")
            return FlextCore.Result.ok(True)

        except Exception as e:
            self.logger.exception(f"Failed to unregister plugin '{plugin_name}'")
            return FlextCore.Result.fail(f"Unregistration error: {e!s}")

    def get_plugin(self, plugin_name: str) -> FlextPluginEntities.Plugin | None:
        """Get a plugin by name.

        Args:
            plugin_name: Name of the plugin to retrieve

        Returns:
            Plugin entity if found, None otherwise

        """
        return self._plugins.get(plugin_name)

    def list_plugins(self) -> list[FlextPluginEntities.Plugin]:
        """List all registered plugins.

        Returns:
            List of all registered plugin entities

        """
        return list(self._plugins.values())

    def get_plugin_status(self, plugin_name: str) -> str | None:
        """Get the status of a specific plugin.

        Args:
            plugin_name: Name of the plugin

        Returns:
            Plugin status if found, None otherwise

        """
        plugin = self.get_plugin(plugin_name)
        return plugin.status if plugin else None

    def is_plugin_active(self, plugin_name: str) -> bool:
        """Check if a plugin is currently active.

        Args:
            plugin_name: Name of the plugin

        Returns:
            True if plugin is active, False otherwise

        """
        plugin = self.get_plugin(plugin_name)
        return plugin.is_active() if plugin else False

    async def start_hot_reload(
        self, paths: FlextCore.Types.StringList
    ) -> FlextCore.Result[bool]:
        """Start hot reload monitoring for the specified paths.

        Args:
            paths: List of paths to monitor for changes

        Returns:
            FlextCore.Result indicating success or failure

        """
        try:
            if not self._hot_reload:
                return FlextCore.Result.fail("Hot reload not initialized")

            start_result = self._hot_reload.start_watching(paths)
            if start_result.is_failure:
                return FlextCore.Result.fail(
                    f"Hot reload start failed: {start_result.error}"
                )

            self.logger.info(f"Started hot reload monitoring for {len(paths)} paths")
            return FlextCore.Result.ok(True)

        except Exception as e:
            self.logger.exception("Failed to start hot reload")
            return FlextCore.Result.fail(f"Hot reload error: {e!s}")

    async def stop_hot_reload(self) -> FlextCore.Result[bool]:
        """Stop hot reload monitoring.

        Returns:
            FlextCore.Result indicating success or failure

        """
        try:
            if not self._hot_reload:
                return FlextCore.Result.fail("Hot reload not initialized")

            stop_result = self._hot_reload.stop_watching()
            if stop_result.is_failure:
                return FlextCore.Result.fail(
                    f"Hot reload stop failed: {stop_result.error}"
                )

            self.logger.info("Stopped hot reload monitoring")
            return FlextCore.Result.ok(True)

        except Exception as e:
            self.logger.exception("Failed to stop hot reload")
            return FlextCore.Result.fail(f"Hot reload error: {e!s}")

    def get_platform_status(self) -> FlextCore.Types.Dict:
        """Get the current status of the plugin platform.

        Returns:
            Dictionary containing platform status information

        """
        return {
            "total_plugins": len(self._plugins),
            "active_plugins": len([p for p in self._plugins.values() if p.is_active()]),
            "total_executions": len(self._executions),
            "running_executions": len([
                e for e in self._executions.values() if e.is_running
            ]),
            "hot_reload_enabled": self._hot_reload is not None
            and self._hot_reload.is_watching()
            if self._hot_reload
            else False,
            "monitoring_enabled": self._monitoring is not None,
            "config": {
                "discovery_paths": self.config.discovery.plugin_paths,
                "security_enabled": self.config.security.enable_sandboxing,
                "monitoring_enabled": self._monitoring is not None,
            },
        }

    def get_execution(self, execution_id: str) -> FlextPluginEntities.Execution | None:
        """Get an execution by ID.

        Args:
            execution_id: ID of the execution to retrieve

        Returns:
            Execution entity if found, None otherwise

        """
        return self._executions.get(execution_id)

    def list_executions(self) -> list[FlextPluginEntities.Execution]:
        """List all executions.

        Returns:
            List of all execution entities

        """
        return list(self._executions.values())

    def get_running_executions(self) -> list[FlextPluginEntities.Execution]:
        """Get all currently running executions.

        Returns:
            List of running execution entities

        """
        return [e for e in self._executions.values() if e.is_running]

    def cleanup_executions(self) -> int:
        """Clean up completed executions to free memory.

        Returns:
            Number of executions cleaned up

        """
        completed_executions = [
            eid for eid, execution in self._executions.items() if execution.is_completed
        ]

        for eid in completed_executions:
            del self._executions[eid]

        self.logger.info(f"Cleaned up {len(completed_executions)} completed executions")
        return len(completed_executions)


__all__ = ["FlextPluginPlatform"]
