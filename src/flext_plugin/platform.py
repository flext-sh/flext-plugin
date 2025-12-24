"""FLEXT Plugin Platform - composition-based platform.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import uuid

from flext_core import (
    FlextResult,
    FlextService,
    FlextUtilities,
)

from flext_plugin.models import m
from flext_plugin.protocols import p
from flext_plugin.settings import FlextPluginSettings
from flext_plugin.typings import t

# =========================================================================
# PLUGIN DOMAIN CLASSES - SOLID Plugin Architecture
# =========================================================================


class PluginStatus:
    """Plugin status enumeration."""

    LOADED = "loaded"
    UNLOADED = "unloaded"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"


class PluginExecution:
    """Plugin execution entity with lifecycle management."""

    def __init__(
        self,
        plugin_name: str,
        execution_config: dict[str, object],
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
        self.result: dict[str, object] | None = None
        self.started_at: str | None = None
        self.completed_at: str | None = None

    @classmethod
    def create(
        cls,
        plugin_name: str,
        execution_config: dict[str, object],
        execution_id: str | None = None,
    ) -> PluginExecution:
        """Create new plugin execution."""
        return cls(plugin_name, execution_config, execution_id)

    def mark_started(self) -> None:
        """Mark execution as started."""
        self.is_running = True
        self.started_at = FlextUtilities.Generators.generate_iso_timestamp()

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
        self.completed_at = FlextUtilities.Generators.generate_iso_timestamp()


class PluginRegistry:
    """Plugin registry for managing plugin lifecycle."""

    def __init__(self, name: str = "default") -> None:
        """Initialize plugin registry."""
        self.name = name
        self._plugins: dict[str, object] = {}

    @classmethod
    def create(cls, name: str) -> PluginRegistry:
        """Create new plugin registry."""
        return cls(name)

    def register(self, plugin: m.Plugin) -> FlextResult[bool]:
        """Register plugin."""
        try:
            self._plugins[plugin.name] = plugin
            return FlextResult.ok(True)
        except Exception as e:
            return FlextResult.fail(f"Registration failed: {e}")

    def unregister_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Unregister plugin."""
        try:
            self._plugins.pop(plugin_name, None)
            return FlextResult.ok(True)
        except Exception as e:
            return FlextResult.fail(f"Unregistration failed: {e}")


class Plugin(m.Plugin):
    """Plugin entity extending the base model."""

    def is_active(self) -> bool:
        """Check if plugin is active."""
        return self.is_enabled

    @property
    def status(self) -> str:
        """Get plugin status."""
        if not self.is_enabled:
            return PluginStatus.INACTIVE
        return PluginStatus.ACTIVE


class FlextPluginPlatform(FlextService[None]):
    """railway-oriented plugin platform with functional composition."""

    def __init__(self, container: object | None = None) -> None:
        """Initialize plugin platform."""
        super().__init__(config=FlextPluginSettings())
        # Set container if provided
        if container is not None:
            self._container = container

        # Plugin storage
        self.plugins: dict[str, Plugin] = {}
        self.executions: dict[str, PluginExecution] = {}
        self.registry = PluginRegistry.create(name="platform")

        # Injected protocols
        self.discovery: p.Plugin.PluginDiscovery | None = None
        self.loader: p.Plugin.PluginLoader | None = None
        self.executor: p.Plugin.PluginExecution | None = None

    def execute(self, **_kwargs: object) -> FlextResult[None]:
        """Execute main platform initialization (FlextService protocol)."""
        # Platform is always ready - no specific initialization needed
        return FlextResult[None].ok(None)

    # Core plugin operations with advanced composition
    def discover_plugins(self, paths: list[str]) -> FlextResult[list[Plugin]]:
        """Discover plugins with railway composition."""

        def discover_and_validate(_: None) -> FlextResult[list[dict[str, object]]]:
            # Handle None discovery protocol
            if not self.discovery:
                return FlextResult.fail("Discovery protocol not configured")

            result = self.discovery.discover_plugins(paths)
            if result.is_success:
                # Convert DiscoveryData objects to dicts
                plugin_dicts: list[dict[str, object]] = [
                    {
                        "name": discovery_data.name,
                        "version": discovery_data.version,
                        "path": str(discovery_data.path),
                        "discovery_type": discovery_data.discovery_type,
                        "discovery_method": discovery_data.discovery_method,
                        "metadata": discovery_data.metadata,
                    }
                    for discovery_data in result.value
                ]
                return FlextResult.ok(plugin_dicts)
            return FlextResult[list[dict[str, object]]].fail(
                result.error or "Discovery failed",
            )

        def create_plugins_from_data(
            data: list[dict[str, object]],
        ) -> FlextResult[list[Plugin]]:
            return self._validate_and_create_plugins(data)

        return (
            self._check_protocol(self.discovery, "Discovery")
            .flat_map(discover_and_validate)
            .flat_map(create_plugins_from_data)
            .map(self._register_all)
        )

    def load_plugin(self, plugin_path: str) -> FlextResult[Plugin]:
        """Load single plugin with composition."""

        def load_and_validate(_: None) -> FlextResult[dict[str, object]]:
            # Handle None loader protocol
            if not self.loader:
                return FlextResult.fail("Loader protocol not configured")

            result = self.loader.load_plugin(plugin_path)
            if result.is_success:
                load_data = result.value
                plugin_dict: dict[str, object] = {
                    "name": load_data.name,
                    "version": load_data.version,
                    "path": str(load_data.path),
                    "load_type": load_data.load_type,
                    "loaded_at": load_data.loaded_at,
                    "entry_file": str(load_data.entry_file)
                    if load_data.entry_file
                    else None,
                }
                return FlextResult.ok(plugin_dict)
            return FlextResult[dict[str, object]].fail(result.error or "Load failed")

        def create_plugin_from_load_data(
            data: dict[str, object],
        ) -> FlextResult[Plugin]:
            return self._validate_and_create_plugin(data)

        return (
            self._check_protocol(self.loader, "Loader")
            .flat_map(load_and_validate)
            .flat_map(create_plugin_from_load_data)
            .map(self._register_single)
        )

    def execute_plugin(
        self,
        plugin_name: str,
        context: dict[str, object],
        execution_id: str | None = None,
    ) -> FlextResult[PluginExecution]:
        """Execute plugin with async composition."""

        def get_plugin_result(plugin_name_param: str) -> FlextResult[Plugin]:
            return self._get_plugin(plugin_name_param)

        def create_execution_from_plugin(
            plugin: Plugin,
        ) -> FlextResult[PluginExecution]:
            return self._create_execution(plugin, context, execution_id)

        def prepare_execution_result(
            execution: PluginExecution,
        ) -> FlextResult[PluginExecution]:
            return self._prepare_execution(execution)

        def execute_with_executor_result(
            execution: PluginExecution,
        ) -> FlextResult[PluginExecution]:
            return self._execute_with_executor(execution)

        return (
            get_plugin_result(plugin_name)
            .flat_map(create_execution_from_plugin)
            .flat_map(prepare_execution_result)
            .flat_map(execute_with_executor_result)
        )

    # Plugin management with functional patterns
    def register_plugin(self, plugin: m.Plugin) -> FlextResult[bool]:
        """Register plugin with validation chain."""

        def validate_plugin_result(_: None) -> FlextResult[bool]:
            return self.registry.register(plugin)

        def add_to_plugins_result(*, registry_result: bool) -> bool:
            # Use registry_result for validation
            if not registry_result:
                error_msg = "Plugin registration failed"
                raise ValueError(error_msg)
            if isinstance(plugin, Plugin):
                return self._add_to_plugins(plugin)
            return self._add_to_plugins(Plugin.create(
                name=plugin.name,
                plugin_version=plugin.plugin_version,
            ))

        return (
            plugin.validate_business_rules()
            .flat_map(validate_plugin_result)
            .map(add_to_plugins_result)
        )

    def unregister_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Unregister with cleanup chain."""

        def unregister_from_registry(*, registry_result: bool) -> bool:
            # Use registry_result for validation
            if not registry_result:
                error_msg = "Plugin unregistration failed"
                raise ValueError(error_msg)
            return self._remove_from_plugins(plugin_name)

        return self.registry.unregister_plugin(plugin_name).map(
            unregister_from_registry,
        )

    # Accessors using walrus and comprehension patterns
    def get_plugin(self, name: str) -> Plugin | None:
        """Get plugin by name."""
        return self.plugins.get(name)

    def list_plugins(self) -> list[Plugin]:
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
    def get_execution(self, eid: str) -> PluginExecution | None:
        """Get execution by ID."""
        return self.executions.get(eid)

    def list_executions(self) -> list[PluginExecution]:
        """List all executions."""
        return list(self.executions.values())

    def get_running_executions(self) -> list[PluginExecution]:
        """Get all running executions."""
        return [
            execution for execution in self.executions.values() if execution.is_running
        ]

    def cleanup_executions(self) -> int:
        """Clean completed executions."""
        completed_ids = [
            eid for eid, execution in self.executions.items() if execution.is_completed
        ]
        for eid in completed_ids:
            del self.executions[eid]
        return len(completed_ids)

    # Hot reload placeholders
    def start_hot_reload(self, paths: list[str]) -> FlextResult[bool]:
        """Start hot reload for given paths."""
        _ = paths
        return FlextResult.ok(True)

    def stop_hot_reload(self) -> FlextResult[bool]:
        """Stop hot reload."""
        return FlextResult.ok(True)

    # Status with dict comprehension
    @property
    def get_platform_status(self) -> dict[str, object]:
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
    def _check_protocol(self, protocol: object, name: str) -> FlextResult[None]:
        """Protocol validation helper."""
        return (
            FlextResult.ok(None)
            if protocol
            else FlextResult.fail(f"{name} not configured")
        )

    def _validate_and_create_plugins(
        self,
        plugin_data: list[dict[str, object]],
    ) -> FlextResult[list[Plugin]]:
        """Create validated plugins from data."""
        plugins: list[Plugin] = []
        for data in plugin_data:
            plugin = Plugin.create(
                name=str(data["name"]),
                plugin_version=str(data.get("version", "1.0.0")),
            )
            validation_result = plugin.validate_business_rules()
            if validation_result.is_success:
                plugins.append(plugin)
        return FlextResult.ok(plugins)

    def _validate_and_create_plugin(
        self,
        plugin_data: dict[str, object],
    ) -> FlextResult[Plugin]:
        """Create single validated plugin."""
        plugin = Plugin.create(
            name=str(plugin_data["name"]),
            plugin_version=str(plugin_data.get("version", "1.0.0")),
        )
        validation_result = plugin.validate_business_rules()
        if validation_result.is_success:
            return FlextResult.ok(plugin)
        return FlextResult.fail(validation_result.error or "Plugin validation failed")

    def _register_all(self, plugins: list[Plugin]) -> list[Plugin]:
        """Register multiple plugins."""
        for plugin in plugins:
            self.plugins[plugin.name] = plugin
            self.registry.register(plugin)
        return plugins

    def _register_single(self, plugin: Plugin) -> Plugin:
        """Register single plugin."""
        self.plugins[plugin.name] = plugin
        self.registry.register(plugin)
        return plugin

    def _get_plugin(self, name: str) -> FlextResult[Plugin]:
        """Get plugin with error handling."""
        if plugin := self.plugins.get(name):
            return FlextResult.ok(plugin)
        return FlextResult.fail(f"Plugin '{name}' not found")

    def _create_execution(
        self,
        plugin: Plugin,
        context: dict[str, object],
        execution_id: str | None,
    ) -> FlextResult[PluginExecution]:
        """Create execution entity."""
        execution = PluginExecution.create(
            plugin_name=plugin.name,
            execution_config={"input_data": context},
            execution_id=execution_id,
        )
        return FlextResult.ok(execution)

    def _prepare_execution(
        self,
        execution: PluginExecution,
    ) -> FlextResult[PluginExecution]:
        """Prepare execution for running."""
        execution.mark_started()
        self.executions[execution.execution_id] = execution
        return FlextResult.ok(execution)

    def _execute_with_executor(
        self,
        execution: PluginExecution,
    ) -> FlextResult[PluginExecution]:
        """Execute with injected executor."""
        if not self.executor:
            execution.mark_completed(
                success=False,
                error_message="Executor not configured",
            )
            return FlextResult.fail("Executor not configured")

        exec_context: t.Execution.ExecutionContext = {
            "plugin_id": execution.plugin_name,
            "execution_id": execution.execution_id,
            "input_data": execution.input_data,
            "timeout_seconds": getattr(self.config, "security", {}).get(
                "max_execution_time",
                30,
            ),
        }

        result = self.executor.execute_plugin(execution.plugin_name, exec_context)
        execution.mark_completed(
            success=result.is_success,
            error_message=result.error if result.is_failure else None,
        )
        if result.is_success:
            execution.result = result.value

        return result.map(lambda _: execution)

    def _add_to_plugins(self, plugin: Plugin) -> bool:
        """Add plugin to internal registry."""
        self.plugins[plugin.name] = plugin
        return True

    def _remove_from_plugins(self, plugin_name: str) -> bool:
        """Remove plugin from internal registry."""
        self.plugins.pop(plugin_name, None)
        return True


__all__ = ["FlextPluginPlatform"]
