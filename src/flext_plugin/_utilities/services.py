"""FLEXT Plugin Services - Plugin system application services.

Copyright (c) 2025 FLEXT TeaFlextPluginModels. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    Callable,
    MutableMapping,
    MutableSequence,
    Sequence,
)
from typing import override

from flext_core import FlextContainer
from flext_plugin import (
    FlextPluginAdapters,
    FlextPluginPlatform,
    c,
    m,
    p,
    r,
    t,
    u,
    x,
)


class FlextPluginService(x):
    """Main plugin service orchestrating plugin operations using SOLID principles.

    This service provides high-level operations for plugin management,
    coordinating between different protocol implementations to deliver
    complete plugin functionality using composition over inheritance.

    Follows SOLID principles:
    - Single Responsibility: Only handles plugin orchestration
    - Open/Closed: Extensible through protocol implementations
    - Liskov Substitution: No forced inheritance from unrelated base classes
    - Interface Segregation: Uses specific protocols for different concerns
    - Dependency Inversion: Depends on abstractions, not concretions

    Usage:
        ```python
        from flext_plugin import FlextPluginService

        # Initialize service with dependency injection
        service = FlextPluginService()

        # Discover plugins
        result = await service.discover_and_register_plugins(["./plugins"])
        if result.success:
            # Process the registered plugins
        ```
    """

    _discovery: p.Plugin.PluginDiscovery
    _loader: p.Plugin.PluginLoader
    _executor: p.Plugin.PluginExecution
    _security: p.Plugin.PluginSecurity
    _registry: p.Plugin.PluginRegistry
    _monitoring: p.Plugin.PluginMonitoring

    def __init__(
        self,
        discovery: p.Plugin.PluginDiscovery | None = None,
        loader: p.Plugin.PluginLoader | None = None,
        executor: p.Plugin.PluginExecution | None = None,
        registry: p.Plugin.PluginRegistry | None = None,
        monitoring: p.Plugin.PluginMonitoring | None = None,
    ) -> None:
        """Initialize the plugin service with protocol implementations and dependency injection.

        Args:
            discovery: Plugin discovery implementation
            loader: Plugin loader implementation
            executor: Plugin execution implementation
            registry: Plugin registry implementation
            monitoring: Plugin monitoring implementation

        """
        super().__init__(
            settings_type=None,
            settings_overrides=None,
            initial_context=None,
        )
        self._discovery = discovery or FlextPluginAdapters.FileSystemDiscoveryAdapter()
        self._loader = loader or FlextPluginAdapters.DynamicLoaderAdapter()
        self._executor = executor or FlextPluginAdapters.PluginExecutorAdapter()
        self._security = FlextPluginAdapters.PluginSecurityAdapter()
        self._registry = registry or FlextPluginAdapters.MemoryRegistryAdapter()
        self._monitoring = monitoring or FlextPluginAdapters.PluginMonitoringAdapter()
        self._plugins: MutableMapping[str, m.Plugin.Entity] = {}
        self._executions: MutableMapping[str, FlextPluginPlatform.PluginExecution] = {}

    @property
    @override
    def container(self) -> p.Container:
        """Get the container for this service instance."""
        return FlextContainer.shared()

    @staticmethod
    def _to_general_mapping(
        value: t.JsonPayload | m.BaseModel | None,
    ) -> t.JsonMapping:
        if value is None:
            return t.CONTAINER_MAPPING_ADAPTER.validate_python({})
        normalized_value = u.normalize_to_metadata(value)
        return t.CONTAINER_MAPPING_ADAPTER.validate_python(
            normalized_value,
        )

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

    def disable_plugin(self, plugin_name: str) -> p.Result[bool]:
        """Disable a plugin by name.

        Args:
            plugin_name: Name of the plugin to disable

        Returns:
            r indicating success or failure

        """
        plugin = self.fetch_plugin(plugin_name)
        if plugin is None:
            return r[bool].fail(f"Plugin '{plugin_name}' not found")
        plugin.is_enabled = False
        return r[bool].ok(True)

    def discover_and_register_plugins(
        self,
        paths: t.StrSequence,
    ) -> p.Result[Sequence[m.Plugin.Entity]]:
        """Discover plugins and register them in the service.

        Args:
        paths: List of paths to search for plugins

        Returns:
        r containing list of registered plugins

        """
        try:
            if not self._discovery:
                return r[Sequence[m.Plugin.Entity]].fail(
                    "Plugin discovery not available",
                )
            discovery_result = self._discovery.discover_plugins(paths)
            if discovery_result.failure:
                return r[Sequence[m.Plugin.Entity]].fail(
                    f"Discovery failed: {discovery_result.error}",
                )
            registered_plugins: MutableSequence[m.Plugin.Entity] = []
            for plugin_data in discovery_result.value:
                name = plugin_data.name
                version = plugin_data.version
                metadata = self._to_general_mapping(plugin_data.metadata)
                if not name:
                    continue
                plugin_type_value = c.Plugin.Type(
                    str(metadata.get("plugin_type", c.Plugin.Type.UTILITY.value))
                )
                plugin = m.Plugin.Entity.create(
                    name=name,
                    plugin_version=version,
                    description=str(metadata.get("description", "")),
                    author=str(metadata.get("author", "")),
                    plugin_type=plugin_type_value,
                    metadata=metadata,
                )
                finalize_result = self._finalize_plugin_registration(plugin)
                if finalize_result.failure:
                    self.logger.warning(
                        f"Plugin {plugin.name} registration flow failed: "
                        f"{finalize_result.error if finalize_result.error is not None else ''}",
                    )
                    continue
                registered_plugins.append(finalize_result.value)
            self.logger.info(f"Registered {len(registered_plugins)} plugins")
            return r[Sequence[m.Plugin.Entity]].ok(registered_plugins)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Plugin discovery and registration failed")
            return r[Sequence[m.Plugin.Entity]].fail(
                f"Service error: {e!s}",
            )

    def discover_plugins(
        self,
        paths: t.StrSequence,
    ) -> p.Result[Sequence[m.Plugin.Entity]]:
        """Discover plugins from the specified paths.

        Alias for discover_and_register_plugins.

        Args:
            paths: List of paths to search for plugins

        Returns:
            r containing list of discovered plugins

        """
        return self.discover_and_register_plugins(paths)

    def enable_plugin(self, plugin_name: str) -> p.Result[bool]:
        """Enable a plugin by name.

        Args:
            plugin_name: Name of the plugin to enable

        Returns:
            r indicating success or failure

        """
        plugin = self.fetch_plugin(plugin_name)
        if plugin is None:
            return r[bool].fail(f"Plugin '{plugin_name}' not found")
        plugin.is_enabled = True
        return r[bool].ok(True)

    def execute_plugin(
        self,
        plugin_name: str,
        context: t.JsonMapping,
        execution_id: str | None = None,
    ) -> p.Result[FlextPluginPlatform.PluginExecution]:
        """Execute a plugin with the given context.

        Args:
        plugin_name: Name of the plugin to execute
        context: Execution context data
        execution_id: Optional execution ID (generated if not provided)

        Returns:
        r containing the execution result

        """
        try:
            if plugin_name not in self._plugins:
                return r[FlextPluginPlatform.PluginExecution].fail(
                    f"Plugin '{plugin_name}' not found",
                )
            if not self._executor:
                return r[FlextPluginPlatform.PluginExecution].fail(
                    "Plugin executor not available",
                )
            plugin = self._plugins[plugin_name]
            execution_config = t.CONTAINER_VALUE_MAPPING_ADAPTER.validate_python(
                {
                    "input_data": context,
                    "status": "pending",
                },
            )
            execution = FlextPluginPlatform.PluginExecution.create(
                plugin_name=plugin_name,
                execution_config=execution_config,
                execution_id=execution_id,
            )
            execution.mark_started()
            self._executions[execution.execution_id] = execution
            exec_result = self._executor.execute_plugin(plugin_name, context)
            if exec_result.failure:
                execution.mark_completed(success=False, error_message=exec_result.error)
                return r[FlextPluginPlatform.PluginExecution].fail(
                    f"Execution failed: {exec_result.error}",
                )
            execution.mark_completed(success=True)
            if u.dict_like(exec_result.value):
                execution.result = self._to_general_mapping(exec_result.value)
            plugin.record_execution(0.0, success=True)
            self.logger.info("Executed plugin '%s' successfully", plugin_name)
            return r[FlextPluginPlatform.PluginExecution].ok(execution)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to execute plugin '%s'", plugin_name)
            return r[FlextPluginPlatform.PluginExecution].fail(
                f"Execution error: {e!s}",
            )

    def fetch_execution(
        self,
        execution_id: str,
    ) -> FlextPluginPlatform.PluginExecution | None:
        """Fetch an execution by ID.

        Args:
        execution_id: ID of the execution to retrieve

        Returns:
        Execution entity if found, None otherwise

        """
        return self._executions.get(execution_id)

    def fetch_plugin(self, plugin_name: str) -> m.Plugin.Entity | None:
        """Fetch a plugin by name.

        Args:
        plugin_name: Name of the plugin to retrieve

        Returns:
        Plugin entity if found, None otherwise

        """
        return self._plugins.get(plugin_name)

    def fetch_plugin_config(
        self,
        plugin_name: str,
    ) -> p.Result[m.Plugin.PluginConfig]:
        """Get configuration for a plugin.

        Args:
            plugin_name: Name of the plugin

        Returns:
            r containing plugin configuration

        """
        plugin = self.fetch_plugin(plugin_name)
        if plugin is None:
            return r[m.Plugin.PluginConfig].fail(
                f"Plugin '{plugin_name}' not found",
            )
        config_data = plugin.metadata.get("settings", {})
        config = self._to_general_mapping(config_data)
        settings = m.Plugin.PluginConfig(
            plugin_name=plugin.name,
            config=config,
        )
        return r[m.Plugin.PluginConfig].ok(settings)

    async def fetch_plugin_health(
        self,
        plugin_name: str,
    ) -> p.Result[t.JsonMapping]:
        """Get health status for a specific plugin.

        Args:
        plugin_name: Name of the plugin

        Returns:
        r containing plugin health information

        """
        return self._get_plugin_monitoring_data(
            plugin_name=plugin_name,
            operation=self._monitoring.fetch_plugin_health,
            operation_name="health",
            operation_failure_prefix="Health check failed",
            response_label="Health",
            operation_error_prefix="Health check error",
        )

    async def fetch_plugin_metrics(
        self,
        plugin_name: str,
    ) -> p.Result[t.JsonMapping]:
        """Get metrics for a specific plugin.

        Args:
        plugin_name: Name of the plugin

        Returns:
        r containing plugin metrics

        """
        return self._get_plugin_monitoring_data(
            plugin_name=plugin_name,
            operation=self._monitoring.fetch_plugin_metrics,
            operation_name="metrics",
            operation_failure_prefix="Metrics retrieval failed",
            response_label="Metrics",
            operation_error_prefix="Metrics error",
        )

    def _get_plugin_monitoring_data(
        self,
        plugin_name: str,
        operation: Callable[[str], p.Result[t.JsonMapping]],
        operation_name: str,
        operation_failure_prefix: str,
        response_label: str,
        operation_error_prefix: str,
    ) -> p.Result[t.JsonMapping]:
        try:
            if not self._monitoring:
                return r[t.JsonMapping].fail(
                    "Plugin monitoring not available",
                )
            if plugin_name not in self._plugins:
                return r[t.JsonMapping].fail(
                    f"Plugin '{plugin_name}' not found",
                )

            monitoring_result = operation(plugin_name)
            if monitoring_result.failure:
                return r[t.JsonMapping].fail(
                    f"{operation_failure_prefix}: {monitoring_result.error}",
                )
            if not u.dict_like(monitoring_result.value):
                return r[t.JsonMapping].fail(
                    f"{response_label} response is not a mapping",
                )
            return r[t.JsonMapping].ok(
                self._to_general_mapping(monitoring_result.value)
            )
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception(
                "Failed to get %s for plugin '%s'",
                operation_name,
                plugin_name,
            )
            return r[t.JsonMapping].fail(
                f"{operation_error_prefix}: {e!s}",
            )

    def fetch_plugin_status(self, plugin_name: str) -> str | None:
        """Fetch the status of a specific plugin.

        Args:
        plugin_name: Name of the plugin

        Returns:
        Plugin status if found, None otherwise

        """
        plugin = self.fetch_plugin(plugin_name)
        if plugin is None:
            return None
        if plugin.is_enabled:
            return str(c.Plugin.PluginStatus.ACTIVE)
        return str(c.Plugin.PluginStatus.INACTIVE)

    def list_running_executions(
        self,
    ) -> t.SequenceOf[FlextPluginPlatform.PluginExecution]:
        """List all currently running executions.

        Returns:
        List of running execution entities

        """
        return [e for e in self._executions.values() if e.is_running]

    def fetch_service_status(self) -> t.JsonMapping:
        """Fetch the current status of the plugin service.

        Returns:
        Dictionary containing service status information

        """
        return {
            "total_plugins": len(self._plugins),
            "active_plugins": len([p for p in self._plugins.values() if p.is_enabled]),
            "total_executions": len(self._executions),
            "running_executions": len([
                e for e in self._executions.values() if e.is_running
            ]),
            "monitoring_enabled": True,
            "discovery_available": True,
            "loader_available": True,
            "executor_available": True,
            "security_available": True,
            "registry_available": True,
        }

    def install_plugin(self, plugin_path: str) -> p.Result[m.Plugin.Entity]:
        """Install a plugin from the specified path.

        This loads and registers the plugin.

        Args:
            plugin_path: Path to the plugin to install

        Returns:
            r containing the installed plugin

        """
        result = self.load_plugin(plugin_path)
        if result.success:
            plugin = result.value
            self._plugins[plugin.name] = plugin
            return r[m.Plugin.Entity].ok(plugin)
        return r[m.Plugin.Entity].fail(
            result.error or "Plugin installation failed",
        )

    def plugin_loaded(self, plugin_name: str) -> bool:
        """Check if a plugin is currently loaded.

        Args:
        plugin_name: Name of the plugin

        Returns:
        True if plugin is loaded, False otherwise

        """
        return plugin_name in self._plugins

    def list_executions(self) -> t.SequenceOf[FlextPluginPlatform.PluginExecution]:
        """List all executions.

        Returns:
        List of all execution entities

        """
        return list(self._executions.values())

    def list_plugins(self) -> t.SequenceOf[m.Plugin.Entity]:
        """List all loaded plugins.

        Returns:
        List of all loaded plugin entities

        """
        return list(self._plugins.values())

    def load_plugin(self, plugin_path: str) -> p.Result[m.Plugin.Entity]:
        """Load a single plugin from the specified path.

        Args:
        plugin_path: Path to the plugin to load

        Returns:
        r containing the loaded plugin

        """
        try:
            if not self._loader:
                return r[m.Plugin.Entity].fail(
                    "Plugin loader not available",
                )
            load_result = self._loader.load_plugin(plugin_path)
            if load_result.failure:
                return r[m.Plugin.Entity].fail(
                    f"Plugin loading failed: {load_result.error}",
                )
            value = load_result.value
            if u.dict_like(value):
                data = value
                metadata_value = data.get("metadata")
                metadata = self._to_general_mapping(metadata_value)
                plugin = m.Plugin.Entity.create(
                    name=str(data.get("name", "")),
                    plugin_version=str(data.get("version", "1.0.0")),
                    description=str(data.get("description", "")),
                    author=str(data.get("author", "")),
                    plugin_type=c.Plugin.Type.UTILITY,
                    metadata=metadata,
                )
            else:
                plugin_name = str(getattr(value, "name", ""))
                if not plugin_name:
                    return r[m.Plugin.Entity].fail(
                        "Loader did not return valid load data",
                    )
                plugin_version = str(getattr(value, "version", "1.0.0"))
                module = getattr(value, "module", None)
                module_doc = str(getattr(module, "__doc__", "") or "")
                module_name = str(getattr(module, "__name__", ""))
                module_path = str(getattr(value, "path", ""))
                plugin = m.Plugin.Entity.create(
                    name=plugin_name,
                    plugin_version=plugin_version,
                    description=module_doc,
                    author="",
                    plugin_type=c.Plugin.Type.UTILITY,
                    metadata={"module": module_name, "path": module_path},
                )
            register_result = self._finalize_plugin_registration(plugin)
            if register_result.failure:
                return register_result
            self.logger.info(f"Loaded plugin: {plugin.name}")
            return register_result
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to load plugin from %s", plugin_path)
            return r[m.Plugin.Entity].fail_op("Loading", e)

    def _finalize_plugin_registration(
        self,
        plugin: m.Plugin.Entity,
    ) -> p.Result[m.Plugin.Entity]:
        validation_result = plugin.validate_business_rules()
        if validation_result.failure:
            return r[m.Plugin.Entity].fail(
                f"Plugin validation failed: {validation_result.error}",
            )
        if self._security:
            security_result = self._security.validate_plugin_security(plugin)
            if security_result.failure:
                return r[m.Plugin.Entity].fail(
                    f"Security validation failed: {security_result.error}",
                )
        if self._registry:
            register_result = self._registry.register_plugin(plugin)
            if register_result.failure:
                return r[m.Plugin.Entity].fail(
                    f"Registration failed: {register_result.error}",
                )
        self._plugins[plugin.name] = plugin
        if self._monitoring:
            monitoring_result = self._monitoring.start_monitoring(plugin.name)
            if monitoring_result.failure:
                self.logger.warning(
                    f"Monitoring startup failed for plugin {plugin.name}: "
                    f"{monitoring_result.error if monitoring_result.error is not None else ''}",
                )
        return r[m.Plugin.Entity].ok(plugin)

    def uninstall_plugin(self, plugin_name: str) -> p.Result[bool]:
        """Uninstall a plugin by name.

        Args:
            plugin_name: Name of the plugin to uninstall

        Returns:
            r indicating success or failure

        """
        if plugin_name not in self._plugins:
            return r[bool].fail(f"Plugin '{plugin_name}' not found")
        del self._plugins[plugin_name]
        return r[bool].ok(True)

    async def unload_plugin(self, plugin_name: str) -> p.Result[bool]:
        """Unload a plugin from the service.

        Args:
        plugin_name: Name of the plugin to unload

        Returns:
        r indicating success or failure

        """
        try:
            if plugin_name not in self._plugins:
                return r[bool].fail(f"Plugin '{plugin_name}' not found")
            if self._monitoring:
                monitoring_result = self._monitoring.stop_monitoring(plugin_name)
                if monitoring_result.failure:
                    self.logger.warning(
                        f"Failed to stop monitoring for {plugin_name}: "
                        f"{monitoring_result.error if monitoring_result.error is not None else ''}",
                    )
            if self._registry:
                unregister_result = self._registry.unregister_plugin(plugin_name)
                if unregister_result.failure:
                    return r[bool].fail(
                        f"Unregistration failed: {unregister_result.error}",
                    )
            if self._loader:
                unload_result = self._loader.unload_plugin(plugin_name)
                if unload_result.failure:
                    return r[bool].fail_op("Unloading", unload_result.error)
            del self._plugins[plugin_name]
            self.logger.info("Unloaded plugin: %s", plugin_name)
            return r[bool].ok(True)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to unload plugin '%s'", plugin_name)
            return r[bool].fail_op("Unloading", e)

    def update_plugin_config(
        self,
        plugin_name: str,
        settings: t.JsonMapping,
    ) -> p.Result[bool]:
        """Update configuration for a plugin.

        Args:
            plugin_name: Name of the plugin
            settings: New configuration

        Returns:
            r indicating success or failure

        """
        plugin = self.fetch_plugin(plugin_name)
        if plugin is None:
            return r[bool].fail(f"Plugin '{plugin_name}' not found")
        existing_config = plugin.metadata.get("settings")
        merged_config = t.CONTAINER_VALUE_MAPPING_ADAPTER.validate_python(
            {
                **self._to_general_mapping(existing_config),
                **settings,
            },
        )
        plugin.metadata = dict(
            t.CONTAINER_VALUE_MAPPING_ADAPTER.validate_python(
                {
                    **self._to_general_mapping(plugin.metadata),
                    "settings": merged_config,
                },
            ),
        )
        return r[bool].ok(True)


__all__: list[str] = ["FlextPluginService"]
