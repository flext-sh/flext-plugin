"""FLEXT Plugin API - Railway-oriented facade.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Sequence

from flext_core import r
from flext_core.container import FlextContainer
from flext_core.loggings import FlextLogger

from flext_plugin.models import FlextPluginModels
from flext_plugin.platform import FlextPluginPlatform
from flext_plugin.typings import t


class FlextPluginApi:
    """Railway-oriented plugin facade with composition."""

    __slots__ = ("logger", "platform")

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize FlextPlugin with optional container.

        Args:
        container: Dependency injection container (uses default if None)

        """
        self.logger = FlextLogger(__name__)
        self.platform = FlextPluginPlatform(container=container or FlextContainer())

    # Core operations with logging composition
    def discover_plugins(
        self,
        paths: list[str],
    ) -> r[list[FlextPluginModels.Plugin]]:
        """Discover plugins in the given paths."""

        def log_and_return(
            plugins: list[FlextPluginModels.Plugin],
        ) -> list[FlextPluginModels.Plugin]:
            self.logger.info(f"Discovered {len(plugins)} plugins")
            return plugins

        result = self.platform.discover_plugins(paths)
        # The platform returns list[Plugin] which is compatible with list[FlextPluginModels.Plugin]
        # Use explicit type conversion
        if result.is_success:
            return r[list[FlextPluginModels.Plugin]].ok([
                FlextPluginModels.Plugin.create(
                    name=plugin.name,
                    plugin_version=plugin.plugin_version,
                    description=plugin.description,
                    author=plugin.author,
                    plugin_type=plugin.plugin_type,
                    is_enabled=plugin.is_enabled,
                    metadata=plugin.metadata,
                    entity_id=plugin.unique_id,
                )
                for plugin in result.value
            ])
        return r[list[FlextPluginModels.Plugin]].fail(
            result.error or "Discovery failed"
        )

    def load_plugin(self, _plugin_path: str) -> r[FlextPluginModels.Plugin]:
        """Load a plugin from the given path."""
        return self.platform.load_plugin(_plugin_path).map(
            lambda plugin: (self.logger.info(f"Loaded plugin: {plugin.name}"), plugin)[
                1
            ],
        )

    def execute_plugin(
        self,
        plugin_name: str,
        context: dict[str, t.GeneralValueType],
        execution_id: str | None = None,
    ) -> r[FlextPluginPlatform.PluginExecution]:
        """Execute a plugin by name with the given context."""
        return self.platform.execute_plugin(plugin_name, context, execution_id)

    # Direct delegation with railway patterns
    def register_plugin(self, _plugin: FlextPluginModels.Plugin) -> r[bool]:
        """Register a plugin in the platform."""
        return self.platform.register_plugin(_plugin)

    def unregister_plugin(self, _plugin_name: str) -> r[bool]:
        """Unregister a plugin by name."""
        return self.platform.unregister_plugin(_plugin_name)

    # Hot reload operations
    def start_hot_reload(self, paths: list[str]) -> r[bool]:
        """Start hot reload monitoring for the given paths."""
        return self.platform.start_hot_reload(paths)

    def stop_hot_reload(self) -> r[bool]:
        """Stop hot reload monitoring."""
        return self.platform.stop_hot_reload()

    # Plugin accessors
    def get_plugin(self, _plugin_name: str) -> FlextPluginModels.Plugin | None:
        """Get a plugin by name."""
        return self.platform.get_plugin(_plugin_name)

    def list_plugins(self) -> Sequence[FlextPluginModels.Plugin]:
        """List all registered plugins."""
        return self.platform.list_plugins()

    def get_plugin_status(self, _plugin_name: str) -> str | None:
        """Get the status of a plugin by name."""
        return self.platform.get_plugin_status(_plugin_name)

    def is_plugin_active(self, _plugin_name: str) -> bool:
        """Check if a plugin is active."""
        return self.platform.is_plugin_active(_plugin_name)
