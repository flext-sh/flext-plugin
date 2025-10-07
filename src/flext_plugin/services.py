"""FLEXT Plugin Services - Plugin system application services.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Any

from flext_core import FlextLogger, FlextResult, FlextService

from flext_plugin.entities import FlextPluginEntities
from flext_plugin.protocols import FlextPluginProtocols
from flext_plugin.types import FlextPluginTypes


class FlextPluginService(FlextService[FlextResult]):
    """Main plugin service orchestrating plugin operations.

    This service provides high-level operations for plugin management,
    coordinating between different protocol implementations to deliver
    comprehensive plugin functionality.

    Usage:
        ```python
        from flext_plugin import FlextPluginService
        from flext_core import FlextContainer

        # Initialize service
        container = FlextContainer()
        service = FlextPluginService(container)

        # Discover plugins
        result = await service.discover_and_register_plugins(["./plugins"])
        if result.success:
            print(f"Registered {len(result.value)} plugins")
        ```
    """

    def __init__(
        self,
        discovery: FlextPluginProtocols.PluginDiscovery | None = None,
        loader: FlextPluginProtocols.PluginLoader | None = None,
        executor: FlextPluginProtocols.PluginExecution | None = None,
        security: FlextPluginProtocols.PluginSecurity | None = None,
        registry: FlextPluginProtocols.PluginRegistry | None = None,
        monitoring: FlextPluginProtocols.PluginMonitoring | None = None,
    ) -> None:
        """Initialize the plugin service with protocol implementations.

        Args:
            discovery: Plugin discovery implementation
            loader: Plugin loader implementation
            executor: Plugin execution implementation
            security: Plugin security implementation
            registry: Plugin registry implementation
            monitoring: Plugin monitoring implementation

        """
        super().__init__()
        self.logger = FlextLogger(__name__)

        # Store protocol implementations
        self._discovery = discovery
        self._loader = loader
        self._executor = executor
        self._security = security
        self._registry = registry
        self._monitoring = monitoring

        # Internal state
        self._plugins: dict[str, FlextPluginEntities.Plugin] = {}
        self._executions: dict[str, FlextPluginEntities.Execution] = {}

    def discover_and_register_plugins(
        self, paths: list[str]
    ) -> FlextResult[list[FlextPluginEntities.Plugin]]:
        """Discover plugins and register them in the service.

        Args:
            paths: List of paths to search for plugins

        Returns:
            FlextResult containing list of registered plugins

        """
        try:
            if not self._discovery:
                return FlextResult.fail("Plugin discovery not available")

            # Discover plugins
            discovery_result = self._discovery.discover_plugins(paths)
            if discovery_result.is_failure:
                return FlextResult.fail(f"Discovery failed: {discovery_result.error}")

            plugins_data = discovery_result.value
            registered_plugins = []

            for plugin_data in plugins_data:
                # Create plugin entity
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

                # Security validation
                if self._security:
                    security_result = await self._security.validate_plugin(plugin)
                    if security_result.is_failure:
                        self.logger.warning(
                            f"Plugin {plugin.name} security validation failed: {security_result.error}"
                        )
                        continue

                # Register plugin
                if self._registry:
                    register_result = await self._registry.register_plugin(plugin)
                    if register_result.is_failure:
                        self.logger.warning(
                            f"Plugin {plugin.name} registration failed: {register_result.error}"
                        )
                        continue

                # Store in service
                self._plugins[plugin.name] = plugin
                registered_plugins.append(plugin)

                # Start monitoring if available
                if self._monitoring:
                    await self._monitoring.start_monitoring(plugin.name)

            self.logger.info(f"Registered {len(registered_plugins)} plugins")
            return FlextResult.ok(registered_plugins)

        except Exception as e:
            self.logger.exception("Plugin discovery and registration failed")
            return FlextResult.fail(f"Service error: {e!s}")

    def load_plugin(self, plugin_path: str) -> FlextResult[FlextPluginEntities.Plugin]:
        """Load a single plugin from the specified path.

        Args:
            plugin_path: Path to the plugin to load

        Returns:
            FlextResult containing the loaded plugin

        """
        try:
            if not self._loader:
                return FlextResult.fail("Plugin loader not available")

            # Load plugin
            load_result = self._loader.load_plugin(plugin_path)
            if load_result.is_failure:
                return FlextResult.fail(f"Plugin loading failed: {load_result.error}")

            plugin_data = load_result.value
            plugin = FlextPluginEntities.Plugin.create(
                name=str(plugin_data["name"]),
                plugin_version=str(plugin_data.get("version", "1.0.0")),
                config=plugin_data,
            )

            # Validate plugin
            validation_result = plugin.validate_business_rules()
            if validation_result.is_failure:
                return FlextResult.fail(
                    f"Plugin validation failed: {validation_result.error}"
                )

            # Security validation
            if self._security:
                security_result = await self._security.validate_plugin(plugin)
                if security_result.is_failure:
                    return FlextResult.fail(
                        f"Security validation failed: {security_result.error}"
                    )

            # Register plugin
            if self._registry:
                register_result = await self._registry.register_plugin(plugin)
                if register_result.is_failure:
                    return FlextResult.fail(
                        f"Registration failed: {register_result.error}"
                    )

            # Store in service
            self._plugins[plugin.name] = plugin

            # Start monitoring
            if self._monitoring:
                await self._monitoring.start_monitoring(plugin.name)

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
            execution_id: Optional execution ID (generated if not provided)

        Returns:
            FlextResult containing the execution result

        """
        try:
            if plugin_name not in self._plugins:
                return FlextResult.fail(f"Plugin '{plugin_name}' not found")

            if not self._executor:
                return FlextResult.fail("Plugin executor not available")

            plugin = self._plugins[plugin_name]

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
            execution_context = FlextPluginTypes.Execution.ExecutionContext(
                plugin_id=plugin_name,
                execution_id=execution.execution_id,
                input_data=context,
            )

            exec_result = await self._executor.execute_plugin(
                plugin_name, execution_context
            )

            if exec_result.is_failure:
                execution.mark_completed(success=False, error_message=exec_result.error)
                return FlextResult.fail(f"Execution failed: {exec_result.error}")

            # Mark execution as completed
            execution.mark_completed(success=True)
            execution.result = exec_result.value

            # Record execution metrics
            plugin.record_execution(
                execution_time_ms=execution.execution_time * 1000, success=True
            )

            self.logger.info(f"Executed plugin '{plugin_name}' successfully")
            return FlextResult.ok(execution)

        except Exception as e:
            self.logger.exception(f"Failed to execute plugin '{plugin_name}'")
            return FlextResult.fail(f"Execution error: {e!s}")

    async def unload_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Unload a plugin from the service.

        Args:
            plugin_name: Name of the plugin to unload

        Returns:
            FlextResult indicating success or failure

        """
        try:
            if plugin_name not in self._plugins:
                return FlextResult.fail(f"Plugin '{plugin_name}' not found")

            # Stop monitoring
            if self._monitoring:
                await self._monitoring.stop_monitoring(plugin_name)

            # Unregister from registry
            if self._registry:
                unregister_result = await self._registry.unregister_plugin(plugin_name)
                if unregister_result.is_failure:
                    return FlextResult.fail(
                        f"Unregistration failed: {unregister_result.error}"
                    )

            # Unload from loader
            if self._loader:
                unload_result = await self._loader.unload_plugin(plugin_name)
                if unload_result.is_failure:
                    return FlextResult.fail(f"Unloading failed: {unload_result.error}")

            # Remove from service
            del self._plugins[plugin_name]

            self.logger.info(f"Unloaded plugin: {plugin_name}")
            return FlextResult.ok(True)

        except Exception as e:
            self.logger.exception(f"Failed to unload plugin '{plugin_name}'")
            return FlextResult.fail(f"Unloading error: {e!s}")

    def get_plugin(self, plugin_name: str) -> FlextPluginEntities.Plugin | None:
        """Get a plugin by name.

        Args:
            plugin_name: Name of the plugin to retrieve

        Returns:
            Plugin entity if found, None otherwise

        """
        return self._plugins.get(plugin_name)

    def list_plugins(self) -> list[FlextPluginEntities.Plugin]:
        """List all loaded plugins.

        Returns:
            List of all loaded plugin entities

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

    def is_plugin_loaded(self, plugin_name: str) -> bool:
        """Check if a plugin is currently loaded.

        Args:
            plugin_name: Name of the plugin

        Returns:
            True if plugin is loaded, False otherwise

        """
        return plugin_name in self._plugins

    async def get_plugin_metrics(
        self, plugin_name: str
    ) -> FlextResult[FlextPluginTypes.Performance.Metrics]:
        """Get metrics for a specific plugin.

        Args:
            plugin_name: Name of the plugin

        Returns:
            FlextResult containing plugin metrics

        """
        try:
            if not self._monitoring:
                return FlextResult.fail("Plugin monitoring not available")

            if plugin_name not in self._plugins:
                return FlextResult.fail(f"Plugin '{plugin_name}' not found")

            metrics_result = await self._monitoring.get_plugin_metrics(plugin_name)
            if metrics_result.is_failure:
                return FlextResult.fail(
                    f"Metrics retrieval failed: {metrics_result.error}"
                )

            return FlextResult.ok(metrics_result.value)

        except Exception as e:
            self.logger.exception(f"Failed to get metrics for plugin '{plugin_name}'")
            return FlextResult.fail(f"Metrics error: {e!s}")

    async def get_plugin_health(self, plugin_name: str) -> FlextResult[dict[str, Any]]:
        """Get health status for a specific plugin.

        Args:
            plugin_name: Name of the plugin

        Returns:
            FlextResult containing plugin health information

        """
        try:
            if not self._monitoring:
                return FlextResult.fail("Plugin monitoring not available")

            if plugin_name not in self._plugins:
                return FlextResult.fail(f"Plugin '{plugin_name}' not found")

            health_result = await self._monitoring.get_plugin_health(plugin_name)
            if health_result.is_failure:
                return FlextResult.fail(f"Health check failed: {health_result.error}")

            return FlextResult.ok(health_result.value)

        except Exception as e:
            self.logger.exception(f"Failed to get health for plugin '{plugin_name}'")
            return FlextResult.fail(f"Health check error: {e!s}")

    def get_service_status(self) -> dict[str, Any]:
        """Get the current status of the plugin service.

        Returns:
            Dictionary containing service status information

        """
        return {
            "total_plugins": len(self._plugins),
            "active_plugins": len([p for p in self._plugins.values() if p.is_active()]),
            "total_executions": len(self._executions),
            "running_executions": len([
                e for e in self._executions.values() if e.is_running
            ]),
            "monitoring_enabled": self._monitoring is not None,
            "discovery_available": self._discovery is not None,
            "loader_available": self._loader is not None,
            "executor_available": self._executor is not None,
            "security_available": self._security is not None,
            "registry_available": self._registry is not None,
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


__all__ = ["FlextPluginService"]
