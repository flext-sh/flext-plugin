"""FLEXT Plugin Platform - Advanced composition-based platform.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from dataclasses import field
from typing import ClassVar

from flext_core import FlextResult, FlextService

from flext_plugin.config import FlextPluginConfig
from flext_plugin.plugin import Plugin, PluginStatus
from flext_plugin.plugin_execution import PluginExecution
from flext_plugin.plugin_registry import PluginRegistry
from flext_plugin.protocols import FlextPluginProtocols
from flext_plugin.types import FlextPluginTypes


class FlextPluginPlatform(FlextService[None]):
    """Advanced railway-oriented plugin platform with functional composition."""

    plugins: dict[str, Plugin] = field(default_factory=dict)
    executions: dict[str, PluginExecution] = field(default_factory=dict)
    registry: PluginRegistry = field(
        default_factory=lambda: PluginRegistry.create(name="platform")
    )

    # Injected protocols
    discovery: ClassVar[FlextPluginProtocols.PluginDiscovery | None] = None
    loader: ClassVar[FlextPluginProtocols.PluginLoader | None] = None
    executor: ClassVar[FlextPluginProtocols.PluginExecution | None] = None

    def __init__(self, container: object | None = None) -> None:
        super().__init__(container=container, config=FlextPluginConfig())

    # Core plugin operations with advanced composition
    async def discover_plugins(self, paths: list[str]) -> FlextResult[list[Plugin]]:
        """Discover plugins with railway composition."""
        return (
            await self._check_protocol(self.discovery, "Discovery")
            .flat_map(lambda _: self.discovery.discover_plugins(paths))  # type: ignore
            .flat_map(self._validate_and_create_plugins)
            .map(self._register_all)
        )

    async def load_plugin(self, plugin_path: str) -> FlextResult[Plugin]:
        """Load single plugin with composition."""
        return (
            await self._check_protocol(self.loader, "Loader")
            .flat_map(lambda _: self.loader.load_plugin(plugin_path))  # type: ignore
            .flat_map(self._validate_and_create_plugin)
            .map(self._register_single)
        )

    async def execute_plugin(
        self,
        plugin_name: str,
        context: dict[str, object],
        execution_id: str | None = None,
    ) -> FlextResult[PluginExecution]:
        """Execute plugin with advanced async composition."""
        return (
            self._get_plugin(plugin_name)
            .flat_map(
                lambda plugin: self._create_execution(plugin, context, execution_id)
            )
            .flat_map(self._prepare_execution)
            .flat_map(self._execute_with_executor)
        )

    # Plugin management with functional patterns
    def register_plugin(self, plugin: Plugin) -> FlextResult[bool]:
        """Register plugin with validation chain."""
        return (
            plugin.validate_business_rules()
            .flat_map(lambda _: self.registry.register(plugin))
            .map(lambda _: self._add_to_plugins(plugin))
        )

    def unregister_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Unregister with cleanup chain."""
        return self.registry.unregister_plugin(plugin_name).map(
            lambda _: self._remove_from_plugins(plugin_name)
        )

    # Accessors using walrus and comprehension patterns
    def get_plugin(self, name: str) -> Plugin | None:
        return self.plugins.get(name)

    def list_plugins(self) -> list[Plugin]:
        return list(self.plugins.values())

    def get_plugin_status(self, name: str) -> PluginStatus | None:
        return (p := self.get_plugin(name)) and p.status

    def is_plugin_active(self, name: str) -> bool:
        return (p := self.get_plugin(name)) and p.is_active()

    # Execution management with advanced patterns
    def get_execution(self, eid: str) -> PluginExecution | None:
        return self.executions.get(eid)

    def list_executions(self) -> list[PluginExecution]:
        return list(self.executions.values())

    def get_running_executions(self) -> list[PluginExecution]:
        return [e for e in self.executions.values() if e.is_running]

    def cleanup_executions(self) -> int:
        """Clean completed executions."""
        completed = [eid for eid, e in self.executions.items() if e.is_completed]
        for eid in completed:
            del self.executions[eid]
        return len(completed)

    # Hot reload placeholders
    async def start_hot_reload(self, paths: list[str]) -> FlextResult[bool]:
        _ = paths
        return FlextResult.ok(True)

    async def stop_hot_reload(self) -> FlextResult[bool]:
        return FlextResult.ok(True)

    # Status with dict comprehension
    @property
    def get_platform_status(self) -> dict[str, object]:
        return {
            "total_plugins": len(self.plugins),
            "active_plugins": sum(p.is_active() for p in self.plugins.values()),
            "total_executions": len(self.executions),
            "running_executions": sum(e.is_running for e in self.executions.values()),
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
        self, plugin_data: list[dict[str, object]]
    ) -> FlextResult[list[Plugin]]:
        """Create validated plugins from data."""
        plugins = [
            Plugin.create(
                name=str(data["name"]),
                plugin_version=str(data.get("version", "1.0.0")),
                config=data,
            )
            for data in plugin_data
            if Plugin.create(
                name=str(data["name"]),
                plugin_version=str(data.get("version", "1.0.0")),
                config=data,
            )
            .validate_business_rules()
            .is_success
        ]
        return FlextResult.ok(plugins)

    def _validate_and_create_plugin(
        self, plugin_data: dict[str, object]
    ) -> FlextResult[Plugin]:
        """Create single validated plugin."""
        plugin = Plugin.create(
            name=str(plugin_data["name"]),
            plugin_version=str(plugin_data.get("version", "1.0.0")),
            config=plugin_data,
        )
        return plugin.validate_business_rules().map(lambda _: plugin)

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
        self, plugin: Plugin, context: dict[str, object], execution_id: str | None
    ) -> FlextResult[PluginExecution]:
        """Create execution entity."""
        execution = PluginExecution.create(
            plugin_name=plugin.name,
            execution_config={"input_data": context},
            execution_id=execution_id,
        )
        return FlextResult.ok(execution)

    def _prepare_execution(
        self, execution: PluginExecution
    ) -> FlextResult[PluginExecution]:
        """Prepare execution for running."""
        execution.mark_started()
        self.executions[execution.execution_id] = execution
        return FlextResult.ok(execution)

    async def _execute_with_executor(
        self, execution: PluginExecution
    ) -> FlextResult[PluginExecution]:
        """Execute with injected executor."""
        if not self.executor:
            execution.mark_completed(
                success=False, error_message="Executor not configured"
            )
            return FlextResult.fail("Executor not configured")

        exec_context: FlextPluginTypes.Execution.ExecutionContext = {
            "plugin_id": execution.plugin_name,
            "execution_id": execution.execution_id,
            "input_data": execution.input_data,
            "timeout_seconds": getattr(self.config, "security", {}).get(
                "max_execution_time", 30
            ),
        }

        result = await self.executor.execute_plugin(execution.plugin_name, exec_context)
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
