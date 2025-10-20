"""FLEXT Plugin API - Railway-oriented facade.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Sequence

from flext_core import FlextContainer, FlextLogger, FlextResult

from flext_plugin.models import FlextPluginModels
from flext_plugin.platform import FlextPluginPlatform, PluginExecution


class FlextPluginApi:
    """Railway-oriented plugin facade with advanced composition."""

    __slots__ = ("logger", "platform")

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize FlextPlugin with optional container.

        Args:
            container: Dependency injection container (uses default if None)

        """
        self.logger = FlextLogger(__name__)
        self.platform = FlextPluginPlatform(container or FlextContainer())

    # Core operations with logging composition
    def discover_plugins(
        self, paths: list[str]
    ) -> FlextResult[Sequence[FlextPluginModels.Plugin]]:
        return self.platform.discover_plugins(paths).map(
            lambda plugins: (
                self.logger.info(f"Discovered {len(plugins)} plugins"),
                plugins,
            )[1],
        )

    def load_plugin(self, plugin_path: str) -> FlextResult[FlextPluginModels.Plugin]:
        return self.platform.load_plugin(plugin_path).map(
            lambda plugin: (self.logger.info(f"Loaded plugin: {plugin.name}"), plugin)[
                1
            ],
        )

    def execute_plugin(
        self,
        plugin_name: str,
        context: dict[str, object],
        execution_id: str | None = None,
    ) -> FlextResult[PluginExecution]:
        return self.platform.execute_plugin(plugin_name, context, execution_id)

    # Direct delegation with railway patterns
    def register_plugin(self, plugin: FlextPluginModels.Plugin) -> FlextResult[bool]:
        return self.platform.register_plugin(plugin)

    def unregister_plugin(self, plugin_name: str) -> FlextResult[bool]:
        return self.platform.unregister_plugin(plugin_name)

    # Hot reload operations
    def start_hot_reload(self, paths: list[str]) -> FlextResult[bool]:
        return self.platform.start_hot_reload(paths)

    def stop_hot_reload(self) -> FlextResult[bool]:
        return self.platform.stop_hot_reload()

    # Plugin accessors
    def get_plugin(self, plugin_name: str) -> FlextPluginModels.Plugin | None:
        return self.platform.get_plugin(plugin_name)

    def list_plugins(self) -> Sequence[FlextPluginModels.Plugin]:
        return self.platform.list_plugins()

    def get_plugin_status(self, plugin_name: str) -> str | None:
        return self.platform.get_plugin_status(plugin_name)

    def is_plugin_active(self, plugin_name: str) -> bool:
        return self.platform.is_plugin_active(plugin_name)
