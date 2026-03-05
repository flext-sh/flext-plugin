"""FLEXT Plugin Services - Plugin system application services.

Copyright (c) 2025 FLEXT TeaFlextPluginModels. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from typing import override

from flext_core import FlextContainer, r, t, u, x

from flext_plugin import (
    FlextPluginAdapters,
    FlextPluginModels,
    FlextPluginPlatform,
    FlextPluginProtocols,
    FlextPluginTypes,
    c,
)


class FlextPluginService(FlextPluginModels.ArbitraryTypesModel, x):
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
        if result.is_success:
            # Process the registered plugins
        ```
    """

    # Use protocol types (interfaces) for attributes - follows Dependency Inversion
    _discovery: FlextPluginProtocols.Plugin.PluginDiscovery
    _loader: FlextPluginProtocols.Plugin.PluginLoader
    _executor: FlextPluginProtocols.Plugin.PluginExecution
    _security: FlextPluginProtocols.Plugin.PluginSecurity
    _registry: FlextPluginProtocols.Plugin.PluginRegistry
    _monitoring: FlextPluginProtocols.Plugin.PluginMonitoring

    def __init__(
        self,
        container: FlextContainer | None = None,
        discovery: FlextPluginProtocols.Plugin.PluginDiscovery | None = None,
        loader: FlextPluginProtocols.Plugin.PluginLoader | None = None,
        executor: FlextPluginProtocols.Plugin.PluginExecution | None = None,
        security: FlextPluginProtocols.Plugin.PluginSecurity | None = None,
        registry: FlextPluginProtocols.Plugin.PluginRegistry | None = None,
        monitoring: FlextPluginProtocols.Plugin.PluginMonitoring | None = None,
    ) -> None:
        """Initialize the plugin service with protocol implementations and dependency injection.

        Args:
            container: Dependency injection container (uses x for DI)
            discovery: Plugin discovery implementation
            loader: Plugin loader implementation
            executor: Plugin execution implementation
            security: Plugin security implementation
            registry: Plugin registry implementation
            monitoring: Plugin monitoring implementation

        """
        # Set container before initializing mixins if provided
        if container is not None:
            # Set the container for this service instance
            self._container = container

        # Initialize mixins for dependency injection
        x.__init__(self)

        # Store protocol implementations with defaults - no cast needed
        # Concrete adapters implement the protocols
        self._discovery = discovery or FlextPluginAdapters.FileSystemDiscoveryAdapter()
        self._loader = loader or FlextPluginAdapters.DynamicLoaderAdapter()
        self._executor = executor or FlextPluginAdapters.PluginExecutorAdapter()
        self._security = security or FlextPluginAdapters.PluginSecurityAdapter()
        self._registry = registry or FlextPluginAdapters.MemoryRegistryAdapter()
        self._monitoring = monitoring or FlextPluginAdapters.PluginMonitoringAdapter()

        # Internal state
        self._plugins: dict[str, FlextPluginModels.Plugin.Plugin] = {}
        self._executions: dict[str, FlextPluginPlatform.PluginExecution] = {}

    @property
    @override
    def container(self) -> FlextContainer:
        """Get the container for this service instance."""
        return FlextContainer.get_global()

    @staticmethod
    def _to_general_mapping(
        value: t.ContainerValue,
    ) -> dict[str, t.ContainerValue]:
        if not isinstance(value, Mapping):
            return {}
        return {key: item for key, item in value.items() if isinstance(key, str)}

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

    def disable_plugin(self, plugin_name: str) -> r[bool]:
        """Disable a plugin by name.

        Args:
            plugin_name: Name of the plugin to disable

        Returns:
            r indicating success or failure

        """
        plugin = self.get_plugin(plugin_name)
        if plugin is None:
            return r.fail(f"Plugin '{plugin_name}' not found")

        # Plugin model has is_enabled field
        plugin.is_enabled = False
        return r.ok(True)

    def discover_and_register_plugins(
        self,
        paths: list[str],
    ) -> r[list[FlextPluginModels.Plugin.Plugin]]:
        """Discover plugins and register them in the service.

        Args:
        paths: List of paths to search for plugins

        Returns:
        r containing list of registered plugins

        """
        try:
            if not self._discovery:
                return r.fail("Plugin discovery not available")

            # Discover plugins
            discovery_result = self._discovery.discover_plugins(paths)
            if discovery_result.is_failure:
                return r.fail(f"Discovery failed: {discovery_result.error}")

            # Type narrowing - discovery returns list of DiscoveryData or dicts
            if not u.is_list_like(discovery_result.value):
                return r.fail("Discovery did not return a list")
            registered_plugins: list[FlextPluginModels.Plugin.Plugin] = []

            for plugin_data in discovery_result.value:
                # Support both DiscoveryData model and dict (adapter may return either)
                if u.is_dict_like(plugin_data):
                    name = str(plugin_data.get("name", ""))
                    version = str(plugin_data.get("version", "1.0.0"))
                    metadata_value = plugin_data.get("metadata")
                    metadata = self._to_general_mapping(metadata_value)
                else:
                    name = str(getattr(plugin_data, "name", ""))
                    version = str(getattr(plugin_data, "version", "1.0.0"))
                    metadata_value = getattr(plugin_data, "metadata", {})
                    metadata = self._to_general_mapping(metadata_value)
                if not name:
                    continue
                # Create plugin entity
                # Note: discovery_type is how plugin was found (file/entry_point)
                # plugin_type should come from metadata or default to "utility"
                plugin_type_str = str(metadata.get("plugin_type", "utility"))
                plugin = FlextPluginModels.Plugin.Plugin.create(
                    name=name,
                    plugin_version=version,
                    description=str(metadata.get("description", "")),
                    author=str(metadata.get("author", "")),
                    plugin_type=plugin_type_str,
                    metadata=metadata,
                )

                # Validate plugin
                validation_result = plugin.validate_business_rules()
                if validation_result.is_failure:
                    self.logger.warning(
                        f"Plugin {plugin.name} validation failed: {validation_result.error}",
                    )
                    continue

                # Security validation
                if self._security:
                    plugin_payload = self._to_general_mapping(
                        plugin.model_dump(mode="python"),
                    )
                    security_result = self._security.validate_plugin_security(
                        plugin_payload,
                    )
                    if security_result.is_failure:
                        self.logger.warning(
                            "Plugin %s security validation failed: %s",
                            plugin.name,
                            security_result.error,
                        )
                        continue

                # Register plugin
                if self._registry:
                    plugin_payload = self._to_general_mapping(
                        plugin.model_dump(mode="python"),
                    )
                    register_result = self._registry.register_plugin(plugin_payload)
                    if register_result.is_failure:
                        self.logger.warning(
                            "Plugin %s registration failed: %s",
                            plugin.name,
                            register_result.error,
                        )
                        continue

                # Store in service
                self._plugins[plugin.name] = plugin
                registered_plugins.append(plugin)

                # Start monitoring if available
                if self._monitoring:
                    monitoring_result = self._monitoring.start_monitoring(plugin.name)
                    if monitoring_result.is_failure:
                        self.logger.warning(
                            "Plugin %s monitoring startup failed: %s",
                            plugin.name,
                            monitoring_result.error,
                        )

            self.logger.info(f"Registered {len(registered_plugins)} plugins")
            return r.ok(registered_plugins)

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
            return r.fail(f"Service error: {e!s}")

    def discover_plugins(
        self,
        paths: list[str],
    ) -> r[list[FlextPluginModels.Plugin.Plugin]]:
        """Discover plugins from the specified paths.

        Alias for discover_and_register_plugins.

        Args:
            paths: List of paths to search for plugins

        Returns:
            r containing list of discovered plugins

        """
        return self.discover_and_register_plugins(paths)

    def enable_plugin(self, plugin_name: str) -> r[bool]:
        """Enable a plugin by name.

        Args:
            plugin_name: Name of the plugin to enable

        Returns:
            r indicating success or failure

        """
        plugin = self.get_plugin(plugin_name)
        if plugin is None:
            return r.fail(f"Plugin '{plugin_name}' not found")

        # Plugin model has is_enabled field
        plugin.is_enabled = True
        return r.ok(True)

    def execute_plugin(
        self,
        plugin_name: str,
        context: FlextPluginTypes.Execution.ExecutionContext,
        execution_id: str | None = None,
    ) -> r[FlextPluginPlatform.PluginExecution]:
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
                return r.fail(f"Plugin '{plugin_name}' not found")

            if not self._executor:
                return r.fail("Plugin executor not available")

            plugin = self._plugins[plugin_name]

            # Create execution entity
            execution = FlextPluginPlatform.PluginExecution.create(
                plugin_name=plugin_name,
                execution_config={"input_data": context, "status": "pending"},
                execution_id=execution_id,
            )

            # Start execution
            execution.mark_started()
            self._executions[execution.execution_id] = execution

            exec_result = self._executor.execute_plugin(plugin_name, context)

            if exec_result.is_failure:
                execution.mark_completed(success=False, error_message=exec_result.error)
                return r.fail(f"Execution failed: {exec_result.error}")

            # Mark execution as completed
            execution.mark_completed(success=True)
            # Type narrowing - executor returns dict result
            if u.is_dict_like(exec_result.value):
                execution.result = dict(exec_result.value)

            # Record execution metrics
            plugin.record_execution(0.0, success=True)

            self.logger.info("Executed plugin '%s' successfully", plugin_name)
            return r.ok(execution)

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
            return r.fail(f"Execution error: {e!s}")

    def get_execution(
        self, execution_id: str
    ) -> FlextPluginPlatform.PluginExecution | None:
        """Get an execution by ID.

        Args:
        execution_id: ID of the execution to retrieve

        Returns:
        Execution entity if found, None otherwise

        """
        return self._executions.get(execution_id)

    def get_plugin(self, plugin_name: str) -> FlextPluginModels.Plugin.Plugin | None:
        """Get a plugin by name.

        Args:
        plugin_name: Name of the plugin to retrieve

        Returns:
        Plugin entity if found, None otherwise

        """
        return self._plugins.get(plugin_name)

    def get_plugin_config(
        self,
        plugin_name: str,
    ) -> r[FlextPluginModels.Plugin.PluginConfig]:
        """Get configuration for a plugin.

        Args:
            plugin_name: Name of the plugin

        Returns:
            r containing plugin configuration

        """
        plugin = self.get_plugin(plugin_name)
        if plugin is None:
            return r.fail(f"Plugin '{plugin_name}' not found")

        # Plugin stores config in metadata
        config_data = plugin.metadata.get("config", {})
        # Type narrowing - config should be a dict
        settings = self._to_general_mapping(config_data)
        config = FlextPluginModels.Plugin.PluginConfig(
            plugin_name=plugin.name,
            settings=settings,
        )
        return r.ok(config)

    async def get_plugin_health(
        self,
        plugin_name: str,
    ) -> r[Mapping[str, t.ContainerValue]]:
        """Get health status for a specific plugin.

        Args:
        plugin_name: Name of the plugin

        Returns:
        r containing plugin health information

        """
        try:
            if not self._monitoring:
                return r.fail("Plugin monitoring not available")

            if plugin_name not in self._plugins:
                return r.fail(f"Plugin '{plugin_name}' not found")

            health_result = self._monitoring.get_plugin_health(plugin_name)
            if health_result.is_failure:
                return r.fail(f"Health check failed: {health_result.error}")
            if not u.is_dict_like(health_result.value):
                return r.fail("Health response is not a mapping")
            return r.ok(dict(health_result.value))

        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to get health for plugin '%s'", plugin_name)
            return r.fail(f"Health check error: {e!s}")

    async def get_plugin_metrics(
        self,
        plugin_name: str,
    ) -> r[Mapping[str, t.ContainerValue]]:
        """Get metrics for a specific plugin.

        Args:
        plugin_name: Name of the plugin

        Returns:
        r containing plugin metrics

        """
        try:
            if not self._monitoring:
                return r.fail("Plugin monitoring not available")

            if plugin_name not in self._plugins:
                return r.fail(f"Plugin '{plugin_name}' not found")

            metrics_result = self._monitoring.get_plugin_metrics(plugin_name)
            if metrics_result.is_failure:
                return r.fail(
                    f"Metrics retrieval failed: {metrics_result.error}",
                )
            if not u.is_dict_like(metrics_result.value):
                return r.fail("Metrics response is not a mapping")
            return r.ok(dict(metrics_result.value))

        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to get metrics for plugin '%s'", plugin_name)
            return r.fail(f"Metrics error: {e!s}")

    def get_plugin_status(self, plugin_name: str) -> str | None:
        """Get the status of a specific plugin.

        Args:
        plugin_name: Name of the plugin

        Returns:
        Plugin status if found, None otherwise

        """
        plugin = self.get_plugin(plugin_name)
        if plugin is None:
            return None
        if plugin.is_enabled:
            return c.Plugin.PluginStatus.ACTIVE
        return c.Plugin.PluginStatus.INACTIVE

    def get_running_executions(self) -> list[FlextPluginPlatform.PluginExecution]:
        """Get all currently running executions.

        Returns:
        List of running execution entities

        """
        return [e for e in self._executions.values() if e.is_running]

    def get_service_status(self) -> Mapping[str, t.ContainerValue]:
        """Get the current status of the plugin service.

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

    def install_plugin(self, plugin_path: str) -> r[FlextPluginModels.Plugin.Plugin]:
        """Install a plugin from the specified path.

        This loads and registers the plugin.

        Args:
            plugin_path: Path to the plugin to install

        Returns:
            r containing the installed plugin

        """
        result = self.load_plugin(plugin_path)
        if result.is_success:
            plugin = result.value
            self._plugins[plugin.name] = plugin
            return r.ok(plugin)
        return r.fail(result.error or "Plugin installation failed")

    def is_plugin_loaded(self, plugin_name: str) -> bool:
        """Check if a plugin is currently loaded.

        Args:
        plugin_name: Name of the plugin

        Returns:
        True if plugin is loaded, False otherwise

        """
        return plugin_name in self._plugins

    def list_executions(self) -> list[FlextPluginPlatform.PluginExecution]:
        """List all executions.

        Returns:
        List of all execution entities

        """
        return list(self._executions.values())

    def list_plugins(self) -> list[FlextPluginModels.Plugin.Plugin]:
        """List all loaded plugins.

        Returns:
        List of all loaded plugin entities

        """
        return list(self._plugins.values())

    def load_plugin(self, plugin_path: str) -> r[FlextPluginModels.Plugin.Plugin]:
        """Load a single plugin from the specified path.

        Args:
        plugin_path: Path to the plugin to load

        Returns:
        r containing the loaded plugin

        """
        try:
            if not self._loader:
                return r.fail("Plugin loader not available")

            # Load plugin
            load_result = self._loader.load_plugin(plugin_path)
            if load_result.is_failure:
                return r.fail(f"Plugin loading failed: {load_result.error}")

            # Loader may return LoadData (FlextPluginLoader) or dict (adapter)
            value = load_result.value
            if u.is_dict_like(value):
                data = value
                metadata_value = data.get("metadata")
                metadata = self._to_general_mapping(metadata_value)
                plugin = FlextPluginModels.Plugin.Plugin.create(
                    name=str(data.get("name", "")),
                    plugin_version=str(data.get("version", "1.0.0")),
                    description=str(data.get("description", "")),
                    author=str(data.get("author", "")),
                    plugin_type=c.Plugin.PluginType.UTILITY,
                    metadata=metadata,
                )
            else:
                plugin_name = str(getattr(value, "name", ""))
                if not plugin_name:
                    return r.fail("Loader did not return valid load data")
                plugin_version = str(getattr(value, "version", "1.0.0"))
                module = getattr(value, "module", None)
                module_doc = str(getattr(module, "__doc__", "") or "")
                module_name = str(getattr(module, "__name__", ""))
                module_path = str(getattr(value, "path", ""))
                plugin = FlextPluginModels.Plugin.Plugin.create(
                    name=plugin_name,
                    plugin_version=plugin_version,
                    description=module_doc,
                    author="",
                    plugin_type=c.Plugin.PluginType.UTILITY,
                    metadata={
                        "module": module_name,
                        "path": module_path,
                    },
                )

            # Validate plugin
            validation_result = plugin.validate_business_rules()
            if validation_result.is_failure:
                return r.fail(
                    f"Plugin validation failed: {validation_result.error}",
                )

            # Security validation
            if self._security:
                plugin_payload = self._to_general_mapping(
                    plugin.model_dump(mode="python"),
                )
                security_result = self._security.validate_plugin_security(
                    plugin_payload,
                )
                if security_result.is_failure:
                    return r.fail(
                        f"Security validation failed: {security_result.error}",
                    )

            # Register plugin
            if self._registry:
                plugin_payload = self._to_general_mapping(
                    plugin.model_dump(mode="python"),
                )
                register_result = self._registry.register_plugin(plugin_payload)
                if register_result.is_failure:
                    return r.fail(f"Registration failed: {register_result.error}")

            # Store in service
            self._plugins[plugin.name] = plugin

            # Start monitoring
            if self._monitoring:
                monitoring_result = self._monitoring.start_monitoring(plugin.name)
                if monitoring_result.is_failure:
                    self.logger.warning(
                        "Monitoring startup failed for plugin %s: %s",
                        plugin.name,
                        monitoring_result.error,
                    )

            self.logger.info(f"Loaded plugin: {plugin.name}")
            return r.ok(plugin)

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
            return r.fail(f"Loading error: {e!s}")

    def uninstall_plugin(self, plugin_name: str) -> r[bool]:
        """Uninstall a plugin by name.

        Args:
            plugin_name: Name of the plugin to uninstall

        Returns:
            r indicating success or failure

        """
        if plugin_name not in self._plugins:
            return r.fail(f"Plugin '{plugin_name}' not found")

        del self._plugins[plugin_name]
        return r.ok(True)

    async def unload_plugin(self, plugin_name: str) -> r[bool]:
        """Unload a plugin from the service.

        Args:
        plugin_name: Name of the plugin to unload

        Returns:
        r indicating success or failure

        """
        try:
            if plugin_name not in self._plugins:
                return r.fail(f"Plugin '{plugin_name}' not found")

            # Stop monitoring
            if self._monitoring:
                monitoring_result = self._monitoring.stop_monitoring(plugin_name)
                if monitoring_result.is_failure:
                    self.logger.warning(
                        "Failed to stop monitoring for %s: %s",
                        plugin_name,
                        monitoring_result.error,
                    )

            # Unregister from registry
            if self._registry:
                unregister_result = self._registry.unregister_plugin(plugin_name)
                if unregister_result.is_failure:
                    return r.fail(
                        f"Unregistration failed: {unregister_result.error}",
                    )

            # Unload from loader
            if self._loader:
                unload_result = self._loader.unload_plugin(plugin_name)
                if unload_result.is_failure:
                    return r.fail(f"Unloading failed: {unload_result.error}")

            # Remove from service
            del self._plugins[plugin_name]

            self.logger.info("Unloaded plugin: %s", plugin_name)
            return r.ok(True)

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
            return r.fail(f"Unloading error: {e!s}")

    def update_plugin_config(
        self,
        plugin_name: str,
        config: Mapping[str, t.ContainerValue],
    ) -> r[bool]:
        """Update configuration for a plugin.

        Args:
            plugin_name: Name of the plugin
            config: New configuration

        Returns:
            r indicating success or failure

        """
        plugin = self.get_plugin(plugin_name)
        if plugin is None:
            return r.fail(f"Plugin '{plugin_name}' not found")

        # Assuming Plugin model has config field
        existing_config = plugin.metadata.get("config")
        merged_config = self._to_general_mapping(existing_config)
        merged_config.update(config)
        plugin.metadata["config"] = merged_config
        return r.ok(True)


__all__ = ["FlextPluginService"]
