"""FLEXT Plugin API - Railway-oriented facade.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextContainer, FlextLogger, FlextResult

from flext_plugin.platform import FlextPluginPlatform
from flext_plugin.plugin import Plugin, PluginStatus
from flext_plugin.plugin_execution import PluginExecution


class FlextPluginApi:
    """Railway-oriented plugin facade with advanced composition."""

    __slots__ = ("logger", "platform")

    def __init__(self, container: FlextContainer | None = None) -> None:
        self.logger = FlextLogger(__name__)
        self.platform = FlextPluginPlatform(container or FlextContainer())

    # Core operations with logging composition
    async def discover_plugins(self, paths: list[str]) -> FlextResult[list[Plugin]]:
        return (await self.platform.discover_plugins(paths)).map(
            lambda plugins: (self._log(f"Discovered {len(plugins)} plugins"), plugins)[
                1
            ]
        )

    async def load_plugin(self, plugin_path: str) -> FlextResult[Plugin]:
        return (await self.platform.load_plugin(plugin_path)).map(
            lambda plugin: (self._log(f"Loaded plugin: {plugin.name}"), plugin)[1]
        )

    async def execute_plugin(
        self,
        plugin_name: str,
        context: dict[str, object],
        execution_id: str | None = None,
    ) -> FlextResult[PluginExecution]:
        return await self.platform.execute_plugin(plugin_name, context, execution_id)

    # Direct delegation with railway patterns
    def register_plugin(self, plugin: Plugin) -> FlextResult[bool]:
        return self.platform.register_plugin(plugin)

    def unregister_plugin(self, plugin_name: str) -> FlextResult[bool]:
        return self.platform.unregister_plugin(plugin_name)

    # Hot reload operations
    async def start_hot_reload(self, paths: list[str]) -> FlextResult[bool]:
        return await self.platform.start_hot_reload(paths)

    async def stop_hot_reload(self) -> FlextResult[bool]:
        return await self.platform.stop_hot_reload()

    # Plugin accessors
    def get_plugin(self, plugin_name: str) -> Plugin | None:
        return self.platform.get_plugin(plugin_name)

    def list_plugins(self) -> list[Plugin]:
        return self.platform.list_plugins()

    def get_plugin_status(self, plugin_name: str) -> PluginStatus | None:
        return self.platform.get_plugin_status(plugin_name)

    def is_plugin_active(self, plugin_name: str) -> bool:
        return self.platform.is_plugin_active(plugin_name)

    @property
    def get_platform_status(self) -> dict[str, object]:
        return self.platform.get_platform_status

    # Private logging helper
    def _log(self, message: str) -> None:
        self.logger.info(message)


__all__ = ["FlextPluginApi"]
