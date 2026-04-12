"""FLEXT Plugin API - Railway-oriented facade.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Sequence

from flext_core import FlextContainer, r
from flext_plugin import FlextPluginPlatform, m, p, t, u


class FlextPluginApi:
    """Railway-oriented plugin facade with composition."""

    __slots__ = ("logger", "platform")

    def __init__(self, container: p.Container | None = None) -> None:
        """Initialize FlextPlugin with optional container.

        Args:
        container: Dependency injection container (uses default if None)

        """
        self.logger = u.fetch_logger(__name__)
        self.platform = FlextPluginPlatform.PluginPlatformService(
            container=container or FlextContainer(),
        )

    def discover_plugins(
        self,
        paths: t.StrSequence,
    ) -> r[Sequence[m.Plugin.Plugin]]:
        """Discover plugins in the given paths."""
        result = self.platform.discover_plugins(paths)
        if result.success:
            plugins = result.value
            self.logger.info(f"Discovered {len(plugins)} plugins")
            return r[Sequence[m.Plugin.Plugin]].ok(plugins)
        return r[Sequence[m.Plugin.Plugin]].fail(
            result.error or "Discovery failed",
        )

    def execute_plugin(
        self,
        plugin_name: str,
        context: t.RecursiveContainerMapping,
        execution_id: str | None = None,
    ) -> r[t.RecursiveContainerMapping]:
        """Execute a plugin by name with the given context."""
        result = self.platform.execute_plugin(plugin_name, context, execution_id)
        if result.failure:
            return r[t.RecursiveContainerMapping].fail(
                result.error or "Execution failed"
            )
        return r[t.RecursiveContainerMapping].ok({"execution_id": str(result.value)})

    def get_plugin(self, _plugin_name: str) -> m.Plugin.Plugin | None:
        """Get a plugin by name."""
        return self.platform.get_plugin(_plugin_name)

    def get_plugin_status(self, _plugin_name: str) -> str | None:
        """Get the status of a plugin by name."""
        return self.platform.get_plugin_status(_plugin_name)

    def is_plugin_active(self, _plugin_name: str) -> bool:
        """Check if a plugin is active."""
        return self.platform.is_plugin_active(_plugin_name)

    def list_plugins(self) -> Sequence[m.Plugin.Plugin]:
        """List all registered plugins."""
        return self.platform.list_plugins()

    def load_plugin(self, _plugin_path: str) -> r[m.Plugin.Plugin]:
        """Load a plugin from the given path."""
        result = self.platform.load_plugin(_plugin_path)
        if result.failure:
            return r[m.Plugin.Plugin].fail(result.error or "Load failed")
        plugin = result.value
        self.logger.info(f"Loaded plugin: {plugin.name}")
        return r[m.Plugin.Plugin].ok(plugin)

    def register_plugin(self, _plugin: m.Plugin.Plugin) -> r[bool]:
        """Register a plugin in the platform."""
        return self.platform.register_plugin(_plugin)

    def start_hot_reload(self, paths: t.StrSequence) -> r[bool]:
        """Start hot reload monitoring for the given paths."""
        return self.platform.start_hot_reload(paths)

    def stop_hot_reload(self) -> r[bool]:
        """Stop hot reload monitoring."""
        return self.platform.stop_hot_reload()

    def unregister_plugin(self, _plugin_name: str) -> r[bool]:
        """Unregister a plugin by name."""
        return self.platform.unregister_plugin(_plugin_name)


plugin = FlextPluginApi

__all__: list[str] = ["FlextPluginApi", "plugin"]
