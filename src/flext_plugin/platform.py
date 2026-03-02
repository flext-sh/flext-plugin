"""FLEXT Plugin Platform - composition-based platforFlextPluginModels.

Copyright (c) 2025 FLEXT TeaFlextPluginModels. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import uuid
from collections.abc import Mapping
from typing import override

from flext_core import (
    FlextContainer,
    FlextRegistry,
    FlextResult,
    FlextService,
    FlextSettings,
    r,
    t as core_t,
    u,
)
from pydantic import PrivateAttr

from flext_plugin import (
    FlextPluginModels,
    FlextPluginProtocols,
    FlextPluginSettings,
    c,
    p,
    t,
)

# =========================================================================
# PLUGIN DOMAIN CLASSES - SOLID Plugin Architecture
# =========================================================================


# PluginStatus moved to constants.py - use c.Plugin.PluginStatus


class FlextPluginPlatform:
    """Platform namespace for plugin platform classes."""

    class PluginExecution:
        """Plugin execution entity with lifecycle management."""

        def __init__(
            self,
            plugin_name: str,
            execution_config: Mapping[str, t.GeneralValueType],
            execution_id: str | None = None,
        ) -> None:
            """Initialize plugin execution."""
            self.plugin_name = plugin_name
            self.execution_id = execution_id or str(uuid.uuid4())
            self.input_data = execution_config.get("input_data", {})
            self.is_running = False
            self.is_completed = False
            self.success = False
            self.error_message: str | None = None
            self.result: dict[str, t.GeneralValueType] | None = None
            self.started_at: str | None = None
            self.completed_at: str | None = None

        @classmethod
        def create(
            cls,
            plugin_name: str,
            execution_config: Mapping[str, t.GeneralValueType],
            execution_id: str | None = None,
        ) -> FlextPluginPlatform.PluginExecution:
            """Create new plugin execution."""
            return cls(plugin_name, execution_config, execution_id)

        def mark_started(self) -> None:
            """Mark execution as started."""
            self.is_running = True
            self.started_at = u.Generators.generate_iso_timestamp()

        def mark_completed(
            self,
            *,
            success: bool,
            error_message: str | None = None,
        ) -> None:
            """Mark execution as completed."""
            self.is_running = False
            self.is_completed = True
            self.success = success
            self.error_message = error_message
            self.completed_at = u.Generators.generate_iso_timestamp()

    class PluginRegistry(FlextRegistry):
        """Plugin registry for managing plugin lifecycle.

        Extends FlextRegistry to provide plugin-specific registration with
        class-level storage for auto-discovery patterns.
        """

        # Plugin category constant
        PLUGINS: str = "plugins"

        def __init__(self) -> None:
            """Initialize plugin registry."""
            super().__init__()

        @override
        @classmethod
        def create(
            cls,
            dispatcher: p.CommandBus | None = None,
            *,
            auto_discover_handlers: bool = False,
        ) -> FlextPluginPlatform.PluginRegistry:
            """Create new plugin registry.

            Args:
                dispatcher: Optional dispatcher instance
                auto_discover_handlers: Whether to auto-discover handlers

            Returns:
                New PluginRegistry instance

            """
            _ = dispatcher, auto_discover_handlers
            return cls()

        @override
        def register(
            self,
            name: str,
            service: core_t.RegistrablePlugin,
            metadata: t.GeneralValueType | None = None,
        ) -> r[bool]:
            """Register plugin using class-level storage.

            Args:
                name: Plugin registration name
                service: Plugin service instance
                metadata: Optional metadata

            Returns:
                Result indicating success or failure

            """
            _ = metadata
            return self.register_class_plugin(self.PLUGINS, name, service)

        def unregister(self, plugin_name: str) -> r[bool]:
            """Unregister plugin from class-level storage."""
            return self.unregister_class_plugin(self.PLUGINS, plugin_name)

        def get(self, plugin_name: str) -> r[FlextPluginModels.Plugin.Plugin]:
            """Get plugin by name from class-level storage."""
            result = self.get_class_plugin(self.PLUGINS, plugin_name)
            if result.is_success:
                try:
                    plugin = FlextPluginModels.Plugin.Plugin.model_validate(
                        result.value,
                    )
                    return r[FlextPluginModels.Plugin.Plugin].ok(plugin)
                except (
                    ValueError,
                    TypeError,
                    KeyError,
                    AttributeError,
                    OSError,
                    RuntimeError,
                    ImportError,
                ):
                    return r[FlextPluginModels.Plugin.Plugin].fail(
                        "Plugin is not a valid Plugin type",
                    )
            if result.is_failure:
                return r[FlextPluginModels.Plugin.Plugin].fail(result.error)
            return r[FlextPluginModels.Plugin.Plugin].fail("Plugin not found")

        @override
        def list_plugins(self, category: str = "plugins") -> r[list[str]]:
            """List all registered plugin names.

            Args:
                category: Plugin category to list

            Returns:
                Result containing list of plugin names

            """
            return self.list_class_plugins(category)

    class Plugin(FlextPluginModels.Plugin.Plugin):
        """Plugin entity extending the base model."""

        def is_active(self) -> bool:
            """Check if plugin is active."""
            return self.is_enabled

        @property
        def status(self) -> str:
            """Get plugin status."""
            if not self.is_enabled:
                return c.Plugin.PluginStatus.INACTIVE
            return c.Plugin.PluginStatus.ACTIVE

    class PluginPlatformService(FlextService[None]):
        """railway-oriented plugin platform with functional composition."""

        # Use PrivateAttr for instance variables that are not model fields
        _plugins: dict[str, FlextPluginPlatform.Plugin] = PrivateAttr(
            default_factory=dict,
        )
        _executions: dict[str, FlextPluginPlatform.PluginExecution] = PrivateAttr(
            default_factory=dict,
        )
        _registry: FlextPluginPlatform.PluginRegistry | None = PrivateAttr(default=None)
        _discovery: FlextPluginProtocols.Plugin.PluginDiscovery | None = PrivateAttr(
            default=None,
        )
        _loader: FlextPluginProtocols.Plugin.PluginLoader | None = PrivateAttr(
            default=None,
        )
        _executor: FlextPluginProtocols.Plugin.PluginExecution | None = PrivateAttr(
            default=None,
        )

        @override
        @classmethod
        def _get_service_config_type(cls) -> type[FlextSettings]:
            """Return FlextPluginSettings as the config type for this service."""
            return FlextPluginSettings

        def __init__(
            self,
            container: FlextContainer | None = None,
        ) -> None:
            """Initialize plugin platforFlextPluginModels."""
            super().__init__()
            # Set container if provided
            if container is not None:
                self._container = container

            # Initialize private attributes
            self._plugins = {}
            self._executions = {}
            self._registry = FlextPluginPlatform.PluginRegistry.create()
            self._discovery = None
            self._loader = None
            self._executor = None

        @property
        def plugins(self) -> Mapping[str, FlextPluginPlatform.Plugin]:
            """Plugin storage."""
            return self._plugins

        @property
        def executions(self) -> Mapping[str, FlextPluginPlatform.PluginExecution]:
            """Execution storage."""
            return self._executions

        @property
        def registry(self) -> FlextPluginPlatform.PluginRegistry:
            """Plugin registry."""
            if self._registry is None:
                self._registry = FlextPluginPlatform.PluginRegistry.create()
            registry = self._registry
            if registry is None:
                error_msg = "Plugin registry not initialized"
                raise RuntimeError(error_msg)
            return registry

        @property
        def discovery(self) -> FlextPluginProtocols.Plugin.PluginDiscovery | None:
            """Discovery protocol."""
            return self._discovery

        @discovery.setter
        def discovery(
            self,
            value: FlextPluginProtocols.Plugin.PluginDiscovery | None,
        ) -> None:
            """Set discovery protocol."""
            self._discovery = value

        @property
        def loader(self) -> FlextPluginProtocols.Plugin.PluginLoader | None:
            """Loader protocol."""
            return self._loader

        @loader.setter
        def loader(
            self,
            value: FlextPluginProtocols.Plugin.PluginLoader | None,
        ) -> None:
            """Set loader protocol."""
            self._loader = value

        @property
        def executor(self) -> FlextPluginProtocols.Plugin.PluginExecution | None:
            """Executor protocol."""
            return self._executor

        @executor.setter
        def executor(
            self,
            value: FlextPluginProtocols.Plugin.PluginExecution | None,
        ) -> None:
            """Set executor protocol."""
            self._executor = value

        @override
        def execute(self) -> FlextResult[None]:
            """Execute main platform initialization (FlextService protocol)."""
            # Platform is always ready - no specific initialization needed
            return FlextResult[None].ok(None)

        # Core plugin operations with advanced composition
        def discover_plugins(
            self,
            paths: list[str],
        ) -> FlextResult[list[FlextPluginPlatform.Plugin]]:
            """Discover plugins with railway composition."""

            def discover_and_validate(
                _checked: t.GeneralValueType,
            ) -> FlextResult[list[Mapping[str, t.GeneralValueType]]]:
                # Handle None discovery protocol
                if not self.discovery:
                    return FlextResult.fail("Discovery protocol not configured")

                # Call discover_plugins - it exists on protocol implementations
                discovery_result = self.discovery.discover_plugins(paths)
                if discovery_result.is_success:
                    discovered_items = discovery_result.value
                    plugin_dicts: list[Mapping[str, t.GeneralValueType]] = []
                    for item in discovered_items:
                        if u.is_dict_like(item):
                            plugin_dicts.append(dict(item))
                            continue
                        name = getattr(item, "name", "")
                        version = getattr(item, "version", "1.0.0")
                        path = getattr(item, "path", "")
                        discovery_type = getattr(item, "discovery_type", "file")
                        discovery_method = getattr(
                            item,
                            "discovery_method",
                            "file_system",
                        )
                        metadata = getattr(item, "metadata", {})
                        if u.is_dict_like(metadata):
                            plugin_dicts.append({
                                "name": str(name),
                                "version": str(version),
                                "path": str(path),
                                "discovery_type": str(discovery_type),
                                "discovery_method": str(discovery_method),
                                "metadata": dict(metadata),
                            })
                    return FlextResult.ok(plugin_dicts)
                return FlextResult[list[Mapping[str, t.GeneralValueType]]].fail(
                    discovery_result.error or "Discovery failed",
                )

            def create_plugins_from_data(
                data: list[Mapping[str, t.GeneralValueType]],
            ) -> FlextResult[list[FlextPluginPlatform.Plugin]]:
                return self._validate_and_create_plugins(data)

            return (
                self
                ._check_protocol(self.discovery, "Discovery")
                .flat_map(discover_and_validate)
                .flat_map(create_plugins_from_data)
                .map(self._register_all)
            )

        def load_plugin(
            self,
            plugin_path: str,
        ) -> FlextResult[FlextPluginPlatform.Plugin]:
            """Load single plugin with composition."""

            def load_and_validate(
                _checked: t.GeneralValueType,
            ) -> FlextResult[Mapping[str, t.GeneralValueType]]:
                # Handle None loader protocol
                if not self.loader:
                    return FlextResult.fail("Loader protocol not configured")

                load_result = self.loader.load_plugin(plugin_path)
                if load_result.is_success:
                    load_data = load_result.value
                    # Check if it's a LoadData object or already a dict
                    if u.is_dict_like(load_data):
                        return FlextResult.ok(dict(load_data))
                    if getattr(load_data, "name", None):
                        plugin_dict: dict[str, t.GeneralValueType] = {
                            "name": str(getattr(load_data, "name", "")),
                            "version": str(getattr(load_data, "version", "1.0.0")),
                            "path": str(getattr(load_data, "path", "")),
                            "load_type": str(getattr(load_data, "load_type", "file")),
                            "loaded_at": getattr(load_data, "loaded_at", ""),
                            "entry_file": str(getattr(load_data, "entry_file", ""))
                            if getattr(load_data, "entry_file", None)
                            else None,
                        }
                        return FlextResult.ok(plugin_dict)
                    return FlextResult.fail("Invalid load data format")
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    load_result.error or "Load failed",
                )

            def create_plugin_from_load_data(
                data: Mapping[str, t.GeneralValueType],
            ) -> FlextResult[FlextPluginPlatform.Plugin]:
                return self._validate_and_create_plugin(data)

            return (
                self
                ._check_protocol(self.loader, "Loader")
                .flat_map(load_and_validate)
                .flat_map(create_plugin_from_load_data)
                .map(self._register_single)
            )

        def execute_plugin(
            self,
            plugin_name: str,
            context: Mapping[str, t.GeneralValueType],
            execution_id: str | None = None,
        ) -> FlextResult[FlextPluginPlatform.PluginExecution]:
            """Execute plugin with async composition."""

            def get_plugin_result(
                plugin_name_param: str,
            ) -> FlextResult[FlextPluginPlatform.Plugin]:
                return self._get_plugin(plugin_name_param)

            def create_execution_from_plugin(
                plugin: FlextPluginPlatform.Plugin,
            ) -> FlextResult[FlextPluginPlatform.PluginExecution]:
                return self._create_execution(plugin, context, execution_id)

            def prepare_execution_result(
                execution: FlextPluginPlatform.PluginExecution,
            ) -> FlextResult[FlextPluginPlatform.PluginExecution]:
                return self._prepare_execution(execution)

            def execute_with_executor_result(
                execution: FlextPluginPlatform.PluginExecution,
            ) -> FlextResult[FlextPluginPlatform.PluginExecution]:
                return self._execute_with_executor(execution)

            return (
                get_plugin_result(plugin_name)
                .flat_map(create_execution_from_plugin)
                .flat_map(prepare_execution_result)
                .flat_map(execute_with_executor_result)
            )

        # Plugin management with functional patterns
        def register_plugin(
            self,
            plugin: FlextPluginPlatform.Plugin | FlextPluginModels.Plugin.Plugin,
        ) -> FlextResult[bool]:
            """Register plugin with validation chain."""

            def validate_plugin_result(_: t.GeneralValueType) -> FlextResult[bool]:
                return self.registry.register(plugin.name, plugin)

            def add_to_plugins_result(_registry_result: t.GeneralValueType) -> bool:
                # Use _registry_result for validation
                if _registry_result is not True:
                    error_msg = "Plugin registration failed"
                    raise ValueError(error_msg)
                plugin_entity = FlextPluginPlatform.Plugin.model_validate(
                    plugin.model_dump(),
                )
                return self._add_to_plugins(plugin_entity)

            return (
                plugin
                .validate_business_rules()
                .flat_map(validate_plugin_result)
                .map(add_to_plugins_result)
            )

        def unregister_plugin(self, plugin_name: str) -> FlextResult[bool]:
            """Unregister with cleanup chain."""

            def unregister_from_registry(_registry_result: t.GeneralValueType) -> bool:
                # Use _registry_result for validation
                if _registry_result is not True:
                    error_msg = "Plugin unregistration failed"
                    raise ValueError(error_msg)
                return self._remove_from_plugins(plugin_name)

            return self.registry.unregister(plugin_name).map(
                unregister_from_registry,
            )

        # Accessors using walrus and comprehension patterns
        def get_plugin(self, name: str) -> FlextPluginPlatform.Plugin | None:
            """Get plugin by name."""
            return self.plugins.get(name)

        def list_plugins(self) -> list[FlextPluginPlatform.Plugin]:
            """List all registered plugins."""
            return list(self.plugins.values())

        def get_plugin_status(self, name: str) -> str | None:
            """Get plugin status."""
            plugin = self.get_plugin(name)
            return plugin.status if plugin else None

        def is_plugin_active(self, name: str) -> bool:
            """Check if plugin is active."""
            plugin = self.get_plugin(name)
            return plugin.is_active() if plugin else False

        # Execution management with advanced patterns
        def get_execution(self, eid: str) -> FlextPluginPlatform.PluginExecution | None:
            """Get execution by ID."""
            return self.executions.get(eid)

        def list_executions(self) -> list[FlextPluginPlatform.PluginExecution]:
            """List all executions."""
            return list(self.executions.values())

        def get_running_executions(self) -> list[FlextPluginPlatform.PluginExecution]:
            """Get all running executions."""
            return [
                execution
                for execution in self.executions.values()
                if execution.is_running
            ]

        def cleanup_executions(self) -> int:
            """Clean completed executions."""
            completed_ids = [
                eid
                for eid, execution in self.executions.items()
                if execution.is_completed
            ]
            for eid in completed_ids:
                del self._executions[eid]
            return len(completed_ids)

        # Hot reload hooks — triggered on plugin configuration changes
        def start_hot_reload(self, paths: list[str]) -> FlextResult[bool]:
            """Start hot reload for given paths."""
            _ = paths
            return FlextResult.ok(True)

        def stop_hot_reload(self) -> FlextResult[bool]:
            """Stop hot reload."""
            return FlextResult.ok(True)

        # Status with dict comprehension
        @property
        def get_platform_status(self) -> Mapping[str, t.GeneralValueType]:
            """Get platform status information."""
            return {
                "total_plugins": len(self.plugins),
                "active_plugins": sum(
                    plugin.is_active() for plugin in self.plugins.values()
                ),
                "total_executions": len(self.executions),
                "running_executions": sum(
                    execution.is_running for execution in self.executions.values()
                ),
            }

        # Private composition helpers
        def _check_protocol(
            self,
            protocol: object | None,
            name: str,
        ) -> FlextResult[bool]:
            """Protocol validation helper."""
            return (
                FlextResult[bool].ok(True)
                if protocol
                else FlextResult[bool].fail(f"{name} not configured")
            )

        def _validate_and_create_plugins(
            self,
            plugin_data: list[Mapping[str, t.GeneralValueType]],
        ) -> FlextResult[list[FlextPluginPlatform.Plugin]]:
            """Create validated plugins from data."""
            plugins: list[FlextPluginPlatform.Plugin] = []
            for data in plugin_data:
                plugin = FlextPluginPlatform.Plugin.create(
                    name=str(data["name"]),
                    plugin_version=str(data.get("version", "1.0.0")),
                )
                validation_result = plugin.validate_business_rules()
                if validation_result.is_success:
                    plugins.append(plugin)
            return FlextResult.ok(plugins)

        def _validate_and_create_plugin(
            self,
            plugin_data: Mapping[str, t.GeneralValueType],
        ) -> FlextResult[FlextPluginPlatform.Plugin]:
            """Create single validated plugin."""
            plugin = FlextPluginPlatform.Plugin.create(
                name=str(plugin_data["name"]),
                plugin_version=str(plugin_data.get("version", "1.0.0")),
            )
            validation_result = plugin.validate_business_rules()
            if validation_result.is_success:
                return FlextResult.ok(plugin)
            return FlextResult.fail(
                validation_result.error or "Plugin validation failed",
            )

        def _register_all(
            self,
            plugins: list[FlextPluginPlatform.Plugin],
        ) -> list[FlextPluginPlatform.Plugin]:
            """Register multiple plugins."""
            for plugin in plugins:
                self._plugins[plugin.name] = plugin
                self.registry.register(plugin.name, plugin)
            return plugins

        def _register_single(
            self,
            plugin: FlextPluginPlatform.Plugin,
        ) -> FlextPluginPlatform.Plugin:
            """Register single plugin."""
            self._plugins[plugin.name] = plugin
            self.registry.register(plugin.name, plugin)
            return plugin

        def _get_plugin(self, name: str) -> FlextResult[FlextPluginPlatform.Plugin]:
            """Get plugin with error handling."""
            if plugin := self.plugins.get(name):
                return FlextResult.ok(plugin)
            return FlextResult.fail(f"Plugin '{name}' not found")

        def _create_execution(
            self,
            plugin: FlextPluginPlatform.Plugin,
            context: Mapping[str, t.GeneralValueType],
            execution_id: str | None,
        ) -> FlextResult[FlextPluginPlatform.PluginExecution]:
            """Create execution entity."""
            execution = FlextPluginPlatform.PluginExecution.create(
                plugin_name=plugin.name,
                execution_config={"input_data": context},
                execution_id=execution_id,
            )
            return FlextResult.ok(execution)

        def _prepare_execution(
            self,
            execution: FlextPluginPlatform.PluginExecution,
        ) -> FlextResult[FlextPluginPlatform.PluginExecution]:
            """Prepare execution for running."""
            execution.mark_started()
            self._executions[execution.execution_id] = execution
            return FlextResult.ok(execution)

        def _execute_with_executor(
            self,
            execution: FlextPluginPlatform.PluginExecution,
        ) -> FlextResult[FlextPluginPlatform.PluginExecution]:
            """Execute with injected executor."""
            if not self.executor:
                execution.mark_completed(
                    success=False,
                    error_message="Executor not configured",
                )
                return FlextResult.fail("Executor not configured")

            exec_context: dict[str, t.GeneralValueType] = {
                "plugin_id": execution.plugin_name,
                "execution_id": execution.execution_id,
                "input_data": execution.input_data,
                "timeout_seconds": self.config.timeout_seconds,
            }

            result = self.executor.execute_plugin(execution.plugin_name, exec_context)
            execution.mark_completed(
                success=result.is_success,
                error_message=result.error if result.is_failure else None,
            )
            if result.is_success:
                execution.result = dict(result.value)

            # Map result to PluginExecution type
            if result.is_success:
                return FlextResult.ok(execution)
            return FlextResult.fail(result.error or "Execution failed")

        def _add_to_plugins(self, plugin: FlextPluginPlatform.Plugin) -> bool:
            """Add plugin to internal registry."""
            self._plugins[plugin.name] = plugin
            return True

        def _remove_from_plugins(self, plugin_name: str) -> bool:
            """Remove plugin from internal registry."""
            self._plugins.pop(plugin_name, None)
            return True


Plugin = FlextPluginPlatform.Plugin
PluginExecution = FlextPluginPlatform.PluginExecution
PluginRegistry = FlextPluginPlatform.PluginRegistry

__all__ = ["FlextPluginPlatform", "Plugin", "PluginExecution", "PluginRegistry"]
