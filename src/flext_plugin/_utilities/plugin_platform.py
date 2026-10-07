"""FLEXT Plugin Platform - composition-based platforFlextPluginModels.

Copyright (c) 2025 FLEXT TeaFlextPluginModels. All rights reserved.
SPDX-License-Identifier: MIT

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import uuid
from collections.abc import MutableMapping, MutableSequence, Sequence
from typing import override

from flext_cli import u

from flext_plugin import FlextPluginSettings, c, e, m, p, r, s, t


class _PluginLifecycleOperations:
    """Plugin discovery, registration, and execution lifecycle operations."""

    def discover_plugins(
        self,
        paths: t.StrSequence,
    ) -> p.Result[Sequence[_Platform.Plugin]]:
        """Discover plugins with railway composition.

        Returns:
            The resulting ``p.Result[Sequence[_Platform.Plugin]]``.

        """

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

        checked: p.Result[bool] = self._require_protocol(
            self.discovery,
            "Discovery",
        )

        discovered: p.Result[Sequence[m.Plugin.DiscoveryData]] = checked.flat_map(
            discover_and_validate,
        )

        plugins: p.Result[Sequence[_Platform.Plugin]] = discovered.flat_map(
            self._validate_and_create_plugins,
        )

        return plugins.map(self._register_all)

    def execute_plugin(
        self,
        plugin_name: str,
        context: t.JsonMapping,
        execution_id: str | None = None,
    ) -> p.Result[_Platform.PluginExecution]:
        """Execute plugin with async composition.

        Returns:
            The resulting ``p.Result[_Platform.PluginExecution]``.

        """
        plugin_r: p.Result[_Platform.Plugin] = self._get_plugin(
            plugin_name,
        )

        exec_r: p.Result[_Platform.PluginExecution] = plugin_r.flat_map(
            lambda plugin: self._create_execution(plugin, context, execution_id),
        )

        prepared_r: p.Result[_Platform.PluginExecution] = exec_r.flat_map(
            self._prepare_execution,
        )

        return prepared_r.flat_map(self._execute_with_executor)

    def fetch_plugin(self, name: str) -> _Platform.Plugin | None:
        """Fetch a plugin by name.

        Returns:
            The resulting ``FlextPluginPlatform.Plugin | None``.

        """
        plugin: _Platform.Plugin | None = self.plugins.get(name)

        return plugin

    def fetch_plugin_status(self, name: str) -> str | None:
        """Fetch a plugin status label.

        Returns:
            The resulting ``str | None``.

        """
        plugin = self.fetch_plugin(name)

        return plugin.status if plugin else None

    def resolve_plugin_active(self, name: str) -> bool:
        """Resolve whether a plugin is active.

        Returns:
            The resulting ``bool``.

        """
        plugin = self.fetch_plugin(name)

        return plugin.active() if plugin else False

    def load_plugin(self, plugin_path: str) -> p.Result[_Platform.Plugin]:
        """Load single plugin with composition.

        Returns:
            The resulting ``p.Result[_Platform.Plugin]``.

        """

        def load_and_validate(_checked: t.JsonValue) -> p.Result[t.JsonMapping]:

            if not self.loader:
                return r[t.JsonMapping].fail("Loader protocol not configured")

            return self.loader.load_plugin(plugin_path)

        checked_l: p.Result[bool] = self._require_protocol(self.loader, "Loader")

        loaded: p.Result[t.JsonMapping] = checked_l.flat_map(load_and_validate)

        plugin_r2: p.Result[_Platform.Plugin] = loaded.flat_map(
            self._validate_and_create_plugin,
        )

        return plugin_r2.map(self._register_single)

    def register_plugin(
        self,
        plugin: _Platform.Plugin | m.Plugin.Entity,
    ) -> p.Result[bool]:
        """Register plugin with validation chain.

        Returns:
            The resulting ``p.Result[bool]``.

        """

        def validate_plugin_result(_: t.JsonValue) -> p.Result[bool]:

            return self.registry.register(plugin.name, plugin)

        def add_to_plugins_result(_registry_result: t.JsonValue) -> bool:

            if _registry_result is not True:
                error_msg = "Plugin registration failed"

                raise ValueError(error_msg)

            plugin_entity = _Platform.Plugin.model_validate(
                plugin.model_dump(mode="json"),
            )

            return self._add_to_plugins(plugin_entity)

            validated_biz: p.Result[bool] = (
                FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Rules.validate_business_rules(
                    plugin,
                )
            )
            registered: p.Result[bool] = validated_biz.flat_map(validate_plugin_result)
            return registered.map(add_to_plugins_result)

    def unregister_plugin(self, plugin_name: str) -> p.Result[bool]:
        """Unregister with cleanup chain.

        Returns:
            The resulting ``p.Result[bool]``.

        """

        def unregister_from_registry(_registry_result: t.JsonValue) -> bool:

            if _registry_result is not True:
                error_msg = "Plugin unregistration failed"

                raise ValueError(error_msg)

            return self._remove_from_plugins(plugin_name)

        return self.registry.unregister(plugin_name).map(unregister_from_registry)


class FlextPluginUtilitiesPluginPlatform:
    """Canonical namespace owner."""

    PluginLifecycleOperations = _PluginLifecycleOperations

    class FlextPluginPlatform:
        """Platform namespace for plugin platform classes."""

        class Rules:
            """Plugin lifecycle + business-rule behavior (U17: moved off the model)."""

            @staticmethod
            def validate_business_rules(plugin: m.Plugin.Entity) -> p.Result[bool]:
                """Validate plugin business rules.

                Returns:
                    The resulting ``p.Result[bool]``.
                """
                min_version_parts = 2
                max_version_parts = 3
                if not plugin.name or not plugin.name.strip():
                    return r[bool].fail("Plugin name cannot be empty")
                version_parts = plugin.plugin_version.split(".")
                if (
                    len(version_parts) < min_version_parts
                    or len(version_parts) > max_version_parts
                ):
                    return r[bool].fail(
                        f"Invalid semantic version: {plugin.plugin_version}",
                    )
                if not all(part.isdigit() for part in version_parts if part):
                    return r[bool].fail(
                        f"Version parts must be numeric: {plugin.plugin_version}",
                    )
                # Plugin type validity is enforced by Pydantic via
                # c.Plugin.Type StrEnum.
                return r[bool].ok(value=True)

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
            ) -> _Platform.PluginExecution:
                """Create new plugin execution.

                Returns:
                    The resulting ``FlextPluginPlatform.PluginExecution``.
                """
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
            ) -> _Platform.PluginRegistry:
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
                """Get plugin by name from class-level storage.

                Returns:
                    The resulting ``p.Result[m.Plugin.Entity]``.
                """
                result = self.fetch_plugin(
                    self.PLUGINS,
                    data,
                    scope=c.RegistrationScope.CLASS,
                )
                if result.success:
                    try:
                        plugin = m.Plugin.Entity.model_validate(result.value)
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
                    scope: Registration scope to list plugins from

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
                """Unregister plugin from class-level storage.

                Returns:
                    The resulting ``p.Result[bool]``.
                """
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
                """Delegate plugin lookup to the canonical registry.

                Returns:
                    The resulting ``p.Result[t.JsonPayload | None]``.
                """
                return r[t.JsonPayload | None].from_result(
                    self._registry.fetch_plugin(category, name, scope=scope),
                )

        class Plugin(m.Plugin.Entity):
            """Plugin entity extending the base model."""

            @property
            def status(self) -> str:
                """The plugin status."""
                if not self.is_enabled:
                    return str(c.Plugin.PluginStatus.INACTIVE)
                return str(c.Plugin.PluginStatus.ACTIVE)

            def active(self) -> bool:
                """Check if plugin is active.

                Returns:
                    The resulting ``bool``.
                """
                return self.status == str(c.Plugin.PluginStatus.ACTIVE)

        class PluginPlatformService(
            _PluginLifecycleOperations,
            s[m.Plugin.Registry],
        ):
            """railway-oriented plugin platform with functional composition."""

            _plugins: MutableMapping[
                str,
                FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin,
            ] = u.PrivateAttr(
                default_factory=dict,
            )
            _executions: MutableMapping[
                str,
                _Platform.PluginExecution,
            ] = u.PrivateAttr(default_factory=dict)
            _registry: _Platform.PluginRegistry | None = u.PrivateAttr(
                default_factory=lambda: None,
            )
            _discovery: p.Plugin.Discovery | None = u.PrivateAttr(
                default_factory=lambda: None,
            )
            _loader: p.Plugin.Loader | None = u.PrivateAttr(
                default_factory=lambda: None,
            )
            _executor: p.Plugin.Execution | None = u.PrivateAttr(
                default_factory=lambda: None,
            )

            @staticmethod
            def _to_general_mapping(
                value: t.JsonPayload | m.BaseModel | None,
            ) -> t.JsonMapping:
                """Convert mapping-like values to a typed dict.

                Returns:
                    The resulting ``t.JsonMapping``.
                """
                if value is None:
                    return t.json_mapping_adapter().validate_python({})
                normalized_value = u.normalize_to_metadata(value)
                return t.json_mapping_adapter().validate_python(normalized_value)

            def __init__(self, container: p.Container | None = None) -> None:
                """Initialize plugin platforFlextPluginModels."""
                super().__init__()
                if container is not None:
                    self._container = container
                self._plugins = {}
                self._executions = {}
                self._registry = _Platform.PluginRegistry()
                self._discovery = None
                self._loader = None
                self._executor = None

            def inject_execution(
                self,
                eid: str,
                execution: _Platform.PluginExecution,
            ) -> None:
                """Track the given execution under the supplied id."""
                self._executions[eid] = execution

            def reset_registry(self) -> None:
                """Reset the registry to lazy-initialize on next access."""
                self._registry = None

            @property
            def discovery(self) -> p.Plugin.Discovery | None:
                """Discovery protocol."""
                return self._discovery

            @discovery.setter
            def discovery(self, value: p.Plugin.Discovery | None) -> None:
                """Inject discovery protocol (test hook)."""
                self._discovery = value

            @property
            def executions(
                self,
            ) -> t.MappingKV[
                str,
                _Platform.PluginExecution,
            ]:
                """Execution storage."""
                return self._executions

            @property
            def executor(self) -> p.Plugin.Execution | None:
                """Executor protocol."""
                return self._executor

            @executor.setter
            def executor(self, value: p.Plugin.Execution | None) -> None:
                """Inject executor protocol (test hook)."""
                self._executor = value

            @property
            def platform_status(self) -> t.JsonMapping:
                """The platform status information."""
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
            def loader(self) -> p.Plugin.Loader | None:
                """Loader protocol."""
                return self._loader

            @loader.setter
            def loader(self, value: p.Plugin.Loader | None) -> None:
                """Inject loader protocol (test hook)."""
                self._loader = value

            @property
            def plugins(
                self,
            ) -> t.MappingKV[
                str,
                FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin,
            ]:
                """Plugin storage."""
                return self._plugins

            @property
            def registry(
                self,
            ) -> _Platform.PluginRegistry:
                """Plugin registry."""
                if self._registry is None:
                    self._registry = _Platform.PluginRegistry()
                return self._registry

            @classmethod
            def _get_service_config_type(cls) -> type[FlextPluginSettings]:
                """Return FlextPluginSettings as the settings type for this service."""
                return FlextPluginSettings

            def cleanup_executions(self) -> int:
                """Clean completed executions.

                Returns:
                    The resulting ``int``.
                """
                completed_ids = [
                    eid
                    for eid, execution in self.executions.items()
                    if execution.is_completed
                ]
                for eid in completed_ids:
                    del self._executions[eid]
                return len(completed_ids)

            @override
            def execute(self) -> p.Result[m.Plugin.Registry]:
                """Execute main platform initialization (s protocol).

                Returns:
                    The resulting ``p.Result[m.Plugin.Registry]``.
                """
                plugin_entries: dict[str, t.JsonMapping] = {
                    name: self._to_general_mapping(plugin)
                    for name, plugin in self.plugins.items()
                }
                registry = m.Plugin.Registry(
                    version=c.Plugin.DEFAULT_PLUGIN_VERSION,
                    plugins={
                        name: dict(entry) for name, entry in plugin_entries.items()
                    },
                )
                return r[m.Plugin.Registry].ok(registry)

            def fetch_execution(
                self,
                eid: str,
            ) -> _Platform.PluginExecution | None:
                """Fetch an execution by ID.

                Returns:
                    The resulting ``FlextPluginPlatform.PluginExecution | None``.
                """
                execution: _Platform.PluginExecution | None = self.executions.get(
                    eid,
                )
                return execution

            def list_running_executions(
                self,
            ) -> t.SequenceOf[_Platform.PluginExecution]:
                """List all running executions.

                Returns:
                    The resulting ``t.SequenceOf[FlextPluginPlatform.PluginExecution]``.
                """
                return [
                    execution
                    for execution in self.executions.values()
                    if execution.is_running
                ]

            def list_executions(
                self,
            ) -> t.SequenceOf[_Platform.PluginExecution]:
                """List all executions.

                Returns:
                    The resulting ``t.SequenceOf[FlextPluginPlatform.PluginExecution]``.
                """
                return list(self.executions.values())

            def list_plugins(
                self,
            ) -> t.SequenceOf[_Platform.Plugin]:
                """List all registered plugins.

                Returns:
                    The resulting ``t.SequenceOf[FlextPluginPlatform.Plugin]``.
                """
                return list(self.plugins.values())

            @staticmethod
            def start_hot_reload(paths: t.StrSequence) -> p.Result[bool]:
                """Start hot reload for given paths.

                Returns:
                    The resulting ``p.Result[bool]``.
                """
                _ = paths
                return r[bool].ok(value=True)

            @staticmethod
            def stop_hot_reload() -> p.Result[bool]:
                """Stop hot reload.

                Returns:
                    The resulting ``p.Result[bool]``.
                """
                return r[bool].ok(value=True)

            def _add_to_plugins(
                self,
                plugin: _Platform.Plugin,
            ) -> bool:
                """Add plugin to internal registry.

                Returns:
                    The resulting ``bool``.
                """
                self._plugins[plugin.name] = plugin
                return True

            @staticmethod
            def _require_protocol(
                protocol: p.Plugin.Discovery
                | p.Plugin.Loader
                | p.Plugin.Execution
                | None,
                name: str,
            ) -> p.Result[bool]:
                """Protocol validation helper.

                Returns:
                    The resulting ``p.Result[bool]``.
                """
                return (
                    r[bool].ok(value=True)
                    if protocol
                    else r[bool].fail(f"{name} not configured")
                )

            @staticmethod
            def _create_execution(
                plugin: _Platform.Plugin,
                context: t.JsonMapping,
                execution_id: str | None,
            ) -> p.Result[_Platform.PluginExecution]:
                """Create execution entity.

                Returns:
                    The resulting ``p.Result[_Platform.PluginExecution]``.
                """
                execution = _Platform.PluginExecution(
                    plugin_name=plugin.name,
                    execution_config=t.json_mapping_adapter().validate_python({
                        "input_data": context,
                    }),
                    execution_id=execution_id,
                )
                if execution_id is not None:
                    execution.execution_id = execution_id
                return r[_Platform.PluginExecution].ok(execution)

            def _execute_with_executor(
                self,
                execution: _Platform.PluginExecution,
            ) -> p.Result[_Platform.PluginExecution]:
                """Execute with injected executor.

                Returns:
                    The resulting ``p.Result[_Platform.PluginExecution]``.
                """
                if not self.executor:
                    execution.mark_completed(
                        success=False,
                        error_message="Executor not configured",
                    )
                    return r[_Platform.PluginExecution].fail(
                        "Executor not configured",
                    )
                exec_context: t.JsonMapping = {
                    "plugin_id": execution.plugin_name,
                    "execution_id": execution.execution_id,
                    "input_data": dict(execution.input_data),
                }
                result = self.executor.execute_plugin(
                    execution.plugin_name,
                    exec_context,
                )
                execution.mark_completed(
                    success=result.success,
                    error_message=result.error if result.failure else None,
                )
                if result.success:
                    execution.result = self._to_general_mapping(result.value)
                if result.success:
                    return r[_Platform.PluginExecution].ok(execution)
                return r[_Platform.PluginExecution].fail(
                    result.error or "Execution failed",
                )

            def _get_plugin(
                self,
                name: str,
            ) -> p.Result[
                FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin
            ]:
                """Get plugin with error handling.

                Returns:
                    The resulting ``p.Result[_Platform.Plugin]``.
                """
                if plugin := self.plugins.get(name):
                    return r[_Platform.Plugin].ok(plugin)
                return e.fail_not_found(
                    "Plugin",
                    name,
                    result_type=r[_Platform.Plugin],
                )

            def _prepare_execution(
                self,
                execution: _Platform.PluginExecution,
            ) -> p.Result[_Platform.PluginExecution]:
                """Prepare execution for running.

                Returns:
                    The resulting ``p.Result[_Platform.PluginExecution]``.
                """
                execution.mark_started()
                self._executions[execution.execution_id] = execution
                return r[_Platform.PluginExecution].ok(execution)

            def _register_all(
                self,
                plugins: t.SequenceOf[_Platform.Plugin],
            ) -> t.SequenceOf[_Platform.Plugin]:
                """Register multiple plugins.

                Returns:
                    The resulting ``t.SequenceOf[FlextPluginPlatform.Plugin]``.
                """
                for plugin in plugins:
                    self._plugins[plugin.name] = plugin
                    self.registry.register(plugin.name, plugin)
                return plugins

            def _register_single(
                self,
                plugin: _Platform.Plugin,
            ) -> _Platform.Plugin:
                """Register single plugin.

                Returns:
                    The resulting ``FlextPluginPlatform.Plugin``.
                """
                self._plugins[plugin.name] = plugin
                self.registry.register(plugin.name, plugin)
                return plugin

            def _remove_from_plugins(self, plugin_name: str) -> bool:
                """Remove plugin from internal registry.

                Returns:
                    The resulting ``bool``.
                """
                self._plugins.pop(plugin_name, None)
                return True

            @staticmethod
            def _validate_and_create_plugin(
                plugin_data: t.JsonMapping,
            ) -> p.Result[_Platform.Plugin]:
                """Create single validated plugin.

                Returns:
                    The resulting ``p.Result[_Platform.Plugin]``.
                """
                plugin = _Platform.Plugin(
                    name=str(plugin_data["name"]),
                    plugin_version=str(
                        plugin_data.get("version", c.Plugin.DEFAULT_PLUGIN_VERSION),
                    ),
                )
                validation_result = _Platform.Rules.validate_business_rules(
                    plugin,
                )
                if validation_result.success:
                    return r[_Platform.Plugin].ok(plugin)
                return r[_Platform.Plugin].fail(
                    validation_result.error or "Plugin validation failed",
                )

            @staticmethod
            def _validate_and_create_plugins(
                plugin_data: t.SequenceOf[m.Plugin.DiscoveryData],
            ) -> p.Result[Sequence[_Platform.Plugin]]:
                """Create validated plugins from data.

                Returns:
                    The resulting ``p.Result[Sequence[_Platform.Plugin]]``.
                """
                plugins: MutableSequence[_Platform.Plugin] = []
                for data in plugin_data:
                    plugin = _Platform.Plugin(
                        name=data.name,
                        plugin_version=data.version,
                    )
                    validation_result = _Platform.Rules.validate_business_rules(
                        plugin,
                    )
                    if validation_result.success:
                        plugins.append(plugin)
                return r[Sequence[_Platform.Plugin]].ok(plugins)


_Platform = FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform

__all__: list[str] = ["FlextPluginUtilitiesPluginPlatform"]
