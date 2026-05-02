"""FLEXT Plugin Platform - composition-based platforFlextPluginModels.

Copyright (c) 2025 FLEXT TeaFlextPluginModels. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import uuid
from collections.abc import (
    MutableMapping,
    MutableSequence,
    Sequence,
)
from typing import override

from flext_core import FlextSettings, e
from flext_plugin import (
    FlextPluginSettings,
    c,
    m,
    p,
    r,
    s,
    t,
    u,
)


class FlextPluginPlatform:
    """Platform namespace for plugin platform classes."""

    class PluginExecution:
        """Plugin execution entity with lifecycle management."""

        def __init__(
            self,
            plugin_name: str,
            execution_config: t.JsonMapping,
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
            self.result: t.JsonMapping | None = None
            self.started_at: str | None = None
            self.completed_at: str | None = None

        @classmethod
        def create(
            cls,
            plugin_name: str,
            execution_config: t.JsonMapping,
            execution_id: str | None = None,
        ) -> FlextPluginPlatform.PluginExecution:
            """Create new plugin execution."""
            return cls(plugin_name, execution_config, execution_id)

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
            self.completed_at = u.generate_iso_timestamp()

        def mark_started(self) -> None:
            """Mark execution as started."""
            self.is_running = True
            self.started_at = u.generate_iso_timestamp()

    class PluginRegistry:
        """Plugin registry for managing plugin lifecycle via `p.Registry`."""

        PLUGINS: str = "plugins"
        _registry: p.Registry

        def __init__(self, dispatcher: p.Dispatcher | None = None) -> None:
            """Initialize plugin registry."""
            self._registry = u.build_registry(dispatcher=dispatcher)

        @classmethod
        def create(
            cls,
            dispatcher: p.Dispatcher | None = None,
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
            _ = auto_discover_handlers
            return cls(dispatcher=dispatcher)

        def get(self, data: str) -> p.Result[m.Plugin.Entity]:
            """Get plugin by name from class-level storage."""
            result = self.fetch_plugin(
                self.PLUGINS,
                data,
                scope=c.RegistrationScope.CLASS,
            )
            if result.success:
                try:
                    plugin = m.Plugin.Entity.model_validate(
                        result.value,
                    )
                    return r[m.Plugin.Entity].ok(plugin)
                except c.EXC_BROAD_IO_TYPE:
                    return r[m.Plugin.Entity].fail(
                        "Plugin is not a valid Plugin type",
                    )
            if result.failure:
                return r[m.Plugin.Entity].fail(result.error)
            return e.fail_not_found("Plugin", "", result_type=r[m.Plugin.Entity])

        def list_plugins(
            self,
            category: str = "plugins",
            *,
            scope: c.RegistrationScope = c.RegistrationScope.CLASS,
        ) -> p.Result[t.StrSequence]:
            """List all registered plugin names.

            Args:
                category: Plugin category to list

            Returns:
                Result containing list of plugin names

            """
            return r[t.StrSequence].from_result(
                self._registry.list_plugins(category, scope=scope),
            )

        def register(
            self,
            name: str,
            service: t.RegistrablePlugin,
            metadata: m.ConfigMap | m.Metadata | None = None,
        ) -> p.Result[bool]:
            """Register plugin using class-level storage.

            Args:
                name: Plugin registration name
                service: Plugin service instance
                metadata: Optional metadata

            Returns:
                Result indicating success or failure

            """
            _ = metadata
            return r[bool].from_result(
                self._registry.register_plugin(
                    self.PLUGINS,
                    name,
                    service,
                    scope=c.RegistrationScope.CLASS,
                ),
            )

        def unregister(self, plugin_name: str) -> p.Result[bool]:
            """Unregister plugin from class-level storage."""
            return r[bool].from_result(
                self._registry.unregister_plugin(
                    self.PLUGINS,
                    plugin_name,
                    scope=c.RegistrationScope.CLASS,
                ),
            )

        def fetch_plugin(
            self,
            category: str,
            name: str,
            *,
            scope: c.RegistrationScope = c.RegistrationScope.INSTANCE,
        ) -> p.Result[t.JsonPayload | None]:
            """Delegate plugin lookup to the canonical registry."""
            return r[t.JsonPayload | None].from_result(
                self._registry.fetch_plugin(category, name, scope=scope),
            )

    class Plugin(m.Plugin.Entity):
        """Plugin entity extending the base model."""

        @property
        def status(self) -> str:
            """Get plugin status."""
            if not self.is_enabled:
                return str(c.Plugin.PluginStatus.INACTIVE)
            return str(c.Plugin.PluginStatus.ACTIVE)

        def active(self) -> bool:
            """Check if plugin is active."""
            return self.status == str(c.Plugin.PluginStatus.ACTIVE)

    class PluginPlatformService(s):
        """railway-oriented plugin platform with functional composition."""

        _plugins: MutableMapping[str, FlextPluginPlatform.Plugin] = u.PrivateAttr(
            default_factory=lambda: dict[str, FlextPluginPlatform.Plugin](),
        )
        _executions: MutableMapping[str, FlextPluginPlatform.PluginExecution] = (
            u.PrivateAttr(
                default_factory=lambda: dict[
                    str,
                    FlextPluginPlatform.PluginExecution,
                ](),
            )
        )
        _registry: FlextPluginPlatform.PluginRegistry | None = u.PrivateAttr(
            default_factory=lambda: None
        )
        _discovery: p.Plugin.PluginDiscovery | None = u.PrivateAttr(
            default_factory=lambda: None,
        )
        _loader: p.Plugin.PluginLoader | None = u.PrivateAttr(
            default_factory=lambda: None,
        )
        _executor: p.Plugin.PluginExecution | None = u.PrivateAttr(
            default_factory=lambda: None,
        )

        @staticmethod
        def _to_general_mapping(
            value: t.JsonPayload | m.BaseModel | None,
        ) -> t.JsonMapping:
            """Convert mapping-like values to a typed dict."""
            if value is None:
                return t.CONTAINER_VALUE_MAPPING_ADAPTER.validate_python({})
            normalized_value = u.normalize_to_metadata(value)
            return t.CONTAINER_VALUE_MAPPING_ADAPTER.validate_python(
                normalized_value,
            )

        def __init__(self, container: p.Container | None = None) -> None:
            """Initialize plugin platforFlextPluginModels."""
            super().__init__()
            if container is not None:
                self._container = container
            self._plugins = dict[str, FlextPluginPlatform.Plugin]()
            self._executions = dict[str, FlextPluginPlatform.PluginExecution]()
            self._registry = FlextPluginPlatform.PluginRegistry.create()
            self._discovery = None
            self._loader = None
            self._executor = None

        @property
        def discovery(self) -> p.Plugin.PluginDiscovery | None:
            """Discovery protocol."""
            return self._discovery

        @property
        def executions(self) -> t.MappingKV[str, FlextPluginPlatform.PluginExecution]:
            """Execution storage."""
            return self._executions

        @property
        def executor(self) -> p.Plugin.PluginExecution | None:
            """Executor protocol."""
            return self._executor

        @property
        def platform_status(self) -> t.JsonMapping:
            """Return platform status information."""
            return {
                "total_plugins": len(self.plugins),
                "active_plugins": sum(
                    plugin.active() for plugin in self.plugins.values()
                ),
                "total_executions": len(self.executions),
                "running_executions": sum(
                    execution.is_running for execution in self.executions.values()
                ),
            }

        @property
        def loader(self) -> p.Plugin.PluginLoader | None:
            """Loader protocol."""
            return self._loader

        @property
        def plugins(self) -> t.MappingKV[str, FlextPluginPlatform.Plugin]:
            """Plugin storage."""
            return self._plugins

        @property
        def registry(self) -> FlextPluginPlatform.PluginRegistry:
            """Plugin registry."""
            if self._registry is None:
                self._registry = FlextPluginPlatform.PluginRegistry.create()
            return self._registry

        @classmethod
        def _get_service_config_type(cls) -> type[FlextSettings]:
            """Return FlextPluginSettings as the settings type for this service."""
            return FlextPluginSettings

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

        def discover_plugins(
            self,
            paths: t.StrSequence,
        ) -> p.Result[Sequence[FlextPluginPlatform.Plugin]]:
            """Discover plugins with railway composition."""

            def discover_and_validate(
                _checked: t.JsonValue,
            ) -> p.Result[Sequence[m.Plugin.DiscoveryData]]:
                if not self.discovery:
                    return r[Sequence[m.Plugin.DiscoveryData]].fail(
                        "Discovery protocol not configured",
                    )
                discovery_result = self.discovery.discover_plugins(paths)
                if discovery_result.success:
                    return r[Sequence[m.Plugin.DiscoveryData]].ok(
                        discovery_result.value,
                    )
                return r[Sequence[m.Plugin.DiscoveryData]].fail(
                    discovery_result.error or "Discovery failed",
                )

            def create_plugins_from_data(
                data: t.SequenceOf[m.Plugin.DiscoveryData],
            ) -> p.Result[Sequence[FlextPluginPlatform.Plugin]]:
                return self._validate_and_create_plugins(data)

            checked: p.Result[bool] = self._require_protocol(
                self.discovery, "Discovery"
            )
            discovered: p.Result[Sequence[m.Plugin.DiscoveryData]] = checked.flat_map(
                discover_and_validate
            )
            plugins: p.Result[Sequence[FlextPluginPlatform.Plugin]] = (
                discovered.flat_map(create_plugins_from_data)
            )
            return plugins.map(self._register_all)

        @override
        def execute(self) -> p.Result[None]:
            """Execute main platform initialization (s protocol)."""
            return r[None].ok(None)

        def execute_plugin(
            self,
            plugin_name: str,
            context: t.JsonMapping,
            execution_id: str | None = None,
        ) -> p.Result[FlextPluginPlatform.PluginExecution]:
            """Execute plugin with async composition."""

            def get_plugin_result(
                plugin_name_param: str,
            ) -> p.Result[FlextPluginPlatform.Plugin]:
                return self._get_plugin(plugin_name_param)

            def create_execution_from_plugin(
                plugin: FlextPluginPlatform.Plugin,
            ) -> p.Result[FlextPluginPlatform.PluginExecution]:
                return self._create_execution(plugin, context, execution_id)

            def prepare_execution_result(
                execution: FlextPluginPlatform.PluginExecution,
            ) -> p.Result[FlextPluginPlatform.PluginExecution]:
                return self._prepare_execution(execution)

            def execute_with_executor_result(
                execution: FlextPluginPlatform.PluginExecution,
            ) -> p.Result[FlextPluginPlatform.PluginExecution]:
                return self._execute_with_executor(execution)

            plugin_r: p.Result[FlextPluginPlatform.Plugin] = get_plugin_result(
                plugin_name
            )
            exec_r: p.Result[FlextPluginPlatform.PluginExecution] = plugin_r.flat_map(
                create_execution_from_plugin
            )
            prepared_r: p.Result[FlextPluginPlatform.PluginExecution] = exec_r.flat_map(
                prepare_execution_result
            )
            return prepared_r.flat_map(execute_with_executor_result)

        def fetch_execution(
            self,
            eid: str,
        ) -> FlextPluginPlatform.PluginExecution | None:
            """Fetch an execution by ID."""
            return self.executions.get(eid)

        def fetch_plugin(self, name: str) -> FlextPluginPlatform.Plugin | None:
            """Fetch a plugin by name."""
            return self.plugins.get(name)

        def fetch_plugin_status(self, name: str) -> str | None:
            """Fetch a plugin status label."""
            plugin = self.fetch_plugin(name)
            return plugin.status if plugin else None

        def list_running_executions(
            self,
        ) -> t.SequenceOf[FlextPluginPlatform.PluginExecution]:
            """List all running executions."""
            return [
                execution
                for execution in self.executions.values()
                if execution.is_running
            ]

        def resolve_plugin_active(self, name: str) -> bool:
            """Resolve whether a plugin is active."""
            plugin = self.fetch_plugin(name)
            return plugin.active() if plugin else False

        def list_executions(self) -> t.SequenceOf[FlextPluginPlatform.PluginExecution]:
            """List all executions."""
            return list(self.executions.values())

        def list_plugins(self) -> t.SequenceOf[FlextPluginPlatform.Plugin]:
            """List all registered plugins."""
            return list(self.plugins.values())

        def load_plugin(self, plugin_path: str) -> p.Result[FlextPluginPlatform.Plugin]:
            """Load single plugin with composition."""

            def load_and_validate(
                _checked: t.JsonValue,
            ) -> p.Result[t.JsonMapping]:
                if not self.loader:
                    return r[t.JsonMapping].fail(
                        "Loader protocol not configured",
                    )
                load_result = self.loader.load_plugin(plugin_path)
                if load_result.success:
                    load_data = load_result.value
                    if u.dict_like(load_data):
                        return r[t.JsonMapping].ok(self._to_general_mapping(load_data))
                    if getattr(load_data, "name", None):
                        plugin_dict = {
                            "name": str(getattr(load_data, "name", "")),
                            "version": str(getattr(load_data, "version", "1.0.0")),
                            "path": str(getattr(load_data, "path", "")),
                            "load_type": str(getattr(load_data, "load_type", "file")),
                            "loaded_at": getattr(load_data, "loaded_at", ""),
                            "entry_file": str(getattr(load_data, "entry_file", ""))
                            if getattr(load_data, "entry_file", None)
                            else None,
                        }
                        return r[t.JsonMapping].ok(plugin_dict)
                    return r[t.JsonMapping].fail(
                        "Invalid load data format",
                    )
                return r[t.JsonMapping].fail(
                    load_result.error or "Load failed",
                )

            def create_plugin_from_load_data(
                data: t.JsonMapping,
            ) -> p.Result[FlextPluginPlatform.Plugin]:
                return self._validate_and_create_plugin(data)

            checked_l: p.Result[bool] = self._require_protocol(self.loader, "Loader")
            loaded: p.Result[t.JsonMapping] = checked_l.flat_map(load_and_validate)
            plugin_r2: p.Result[FlextPluginPlatform.Plugin] = loaded.flat_map(
                create_plugin_from_load_data
            )
            return plugin_r2.map(self._register_single)

        def register_plugin(
            self,
            plugin: FlextPluginPlatform.Plugin | m.Plugin.Entity,
        ) -> p.Result[bool]:
            """Register plugin with validation chain."""

            def validate_plugin_result(_: t.JsonValue) -> p.Result[bool]:
                return self.registry.register(plugin.name, plugin)

            def add_to_plugins_result(_registry_result: t.JsonValue) -> bool:
                if _registry_result is not True:
                    error_msg = "Plugin registration failed"
                    raise ValueError(error_msg)
                plugin_entity = FlextPluginPlatform.Plugin.model_validate(
                    plugin.model_dump(mode="json"),
                )
                return self._add_to_plugins(plugin_entity)

            validated_biz: p.Result[bool] = plugin.validate_business_rules()
            registered: p.Result[bool] = validated_biz.flat_map(validate_plugin_result)
            return registered.map(add_to_plugins_result)

        def start_hot_reload(self, paths: t.StrSequence) -> p.Result[bool]:
            """Start hot reload for given paths."""
            _ = paths
            return r[bool].ok(True)

        def stop_hot_reload(self) -> p.Result[bool]:
            """Stop hot reload."""
            return r[bool].ok(True)

        def unregister_plugin(self, plugin_name: str) -> p.Result[bool]:
            """Unregister with cleanup chain."""

            def unregister_from_registry(
                _registry_result: t.JsonValue,
            ) -> bool:
                if _registry_result is not True:
                    error_msg = "Plugin unregistration failed"
                    raise ValueError(error_msg)
                return self._remove_from_plugins(plugin_name)

            return self.registry.unregister(plugin_name).map(unregister_from_registry)

        def _add_to_plugins(self, plugin: FlextPluginPlatform.Plugin) -> bool:
            """Add plugin to internal registry."""
            self._plugins[plugin.name] = plugin
            return True

        def _require_protocol(
            self,
            protocol: p.Plugin.PluginDiscovery
            | p.Plugin.PluginLoader
            | p.Plugin.PluginExecution
            | None,
            name: str,
        ) -> p.Result[bool]:
            """Protocol validation helper."""
            return (
                r[bool].ok(True) if protocol else r[bool].fail(f"{name} not configured")
            )

        def _create_execution(
            self,
            plugin: FlextPluginPlatform.Plugin,
            context: t.JsonMapping,
            execution_id: str | None,
        ) -> p.Result[FlextPluginPlatform.PluginExecution]:
            """Create execution entity."""
            execution = FlextPluginPlatform.PluginExecution.create(
                plugin_name=plugin.name,
                execution_config=t.CONTAINER_VALUE_MAPPING_ADAPTER.validate_python(
                    {"input_data": context},
                ),
                execution_id=execution_id,
            )
            return r[FlextPluginPlatform.PluginExecution].ok(execution)

        def _execute_with_executor(
            self,
            execution: FlextPluginPlatform.PluginExecution,
        ) -> p.Result[FlextPluginPlatform.PluginExecution]:
            """Execute with injected executor."""
            if not self.executor:
                execution.mark_completed(
                    success=False,
                    error_message="Executor not configured",
                )
                return r[FlextPluginPlatform.PluginExecution].fail(
                    "Executor not configured",
                )
            exec_context = {
                "plugin_id": execution.plugin_name,
                "execution_id": execution.execution_id,
                "input_data": execution.input_data,
                "timeout_seconds": self.settings.timeout_seconds,
            }
            result = self.executor.execute_plugin(execution.plugin_name, exec_context)
            execution.mark_completed(
                success=result.success,
                error_message=result.error if result.failure else None,
            )
            if result.success:
                execution.result = self._to_general_mapping(result.value)
            if result.success:
                return r[FlextPluginPlatform.PluginExecution].ok(execution)
            return r[FlextPluginPlatform.PluginExecution].fail(
                result.error or "Execution failed",
            )

        def _get_plugin(self, name: str) -> p.Result[FlextPluginPlatform.Plugin]:
            """Get plugin with error handling."""
            if plugin := self.plugins.get(name):
                return r[FlextPluginPlatform.Plugin].ok(plugin)
            return e.fail_not_found("Plugin", name, result_type=r[FlextPluginPlatform.Plugin])

        def _prepare_execution(
            self,
            execution: FlextPluginPlatform.PluginExecution,
        ) -> p.Result[FlextPluginPlatform.PluginExecution]:
            """Prepare execution for running."""
            execution.mark_started()
            self._executions[execution.execution_id] = execution
            return r[FlextPluginPlatform.PluginExecution].ok(execution)

        def _register_all(
            self,
            plugins: t.SequenceOf[FlextPluginPlatform.Plugin],
        ) -> t.SequenceOf[FlextPluginPlatform.Plugin]:
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

        def _remove_from_plugins(self, plugin_name: str) -> bool:
            """Remove plugin from internal registry."""
            self._plugins.pop(plugin_name, None)
            return True

        def _validate_and_create_plugin(
            self,
            plugin_data: t.JsonMapping,
        ) -> p.Result[FlextPluginPlatform.Plugin]:
            """Create single validated plugin."""
            plugin = FlextPluginPlatform.Plugin.create(
                name=str(plugin_data["name"]),
                plugin_version=str(plugin_data.get("version", "1.0.0")),
            )
            validation_result = plugin.validate_business_rules()
            if validation_result.success:
                return r[FlextPluginPlatform.Plugin].ok(plugin)
            return r[FlextPluginPlatform.Plugin].fail(
                validation_result.error or "Plugin validation failed",
            )

        def _validate_and_create_plugins(
            self,
            plugin_data: t.SequenceOf[m.Plugin.DiscoveryData],
        ) -> p.Result[Sequence[FlextPluginPlatform.Plugin]]:
            """Create validated plugins from data."""
            plugins: MutableSequence[FlextPluginPlatform.Plugin] = []
            for data in plugin_data:
                plugin = FlextPluginPlatform.Plugin.create(
                    name=data.name,
                    plugin_version=data.version,
                )
                validation_result = plugin.validate_business_rules()
                if validation_result.success:
                    plugins.append(plugin)
            return r[Sequence[FlextPluginPlatform.Plugin]].ok(plugins)


__all__: list[str] = ["FlextPluginPlatform"]
