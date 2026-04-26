"""FLEXT Plugin API - Railway-oriented facade.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    Sequence,
)

from flext_core import FlextContainer
from flext_plugin import FlextPluginPlatform, m, p, r, t, u


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
    ) -> p.Result[Sequence[m.Plugin.Entity]]:
        """Discover plugins in the given paths."""
        result = self.platform.discover_plugins(paths)
        if result.success:
            plugins = result.value
            self.logger.info(f"Discovered {len(plugins)} plugins")
            return r[Sequence[m.Plugin.Entity]].ok(plugins)
        return r[Sequence[m.Plugin.Entity]].fail(
            result.error or "Discovery failed",
        )

    def execute_plugin(
        self,
        plugin_name: str,
        context: t.JsonMapping,
        execution_id: str | None = None,
    ) -> p.Result[t.JsonMapping]:
        """Execute a plugin by name with the given context."""
        result = self.platform.execute_plugin(plugin_name, context, execution_id)
        if result.failure:
            return r[t.JsonMapping].fail(result.error or "Execution failed")
        return r[t.JsonMapping].ok({"execution_id": str(result.value)})

    def fetch_plugin(self, plugin_name: str) -> m.Plugin.Entity | None:
        """Fetch a plugin by name."""
        return self.platform.fetch_plugin(plugin_name)

    def fetch_plugin_status(self, plugin_name: str) -> str | None:
        """Fetch the status of a plugin by name."""
        return self.platform.fetch_plugin_status(plugin_name)

    def resolve_plugin_active(self, plugin_name: str) -> bool:
        """Resolve whether a plugin is active."""
        return self.platform.resolve_plugin_active(plugin_name)

    def list_plugins(self) -> Sequence[m.Plugin.Entity]:
        """List all registered plugins."""
        return self.platform.list_plugins()

    def load_plugin(self, plugin_path: str) -> p.Result[m.Plugin.Entity]:
        """Load a plugin from the given path."""
        result = self.platform.load_plugin(plugin_path)
        if result.failure:
            return r[m.Plugin.Entity].fail(result.error or "Load failed")
        plugin = result.value
        self.logger.info(f"Loaded plugin: {plugin.name}")
        return r[m.Plugin.Entity].ok(plugin)

    def register_plugin(self, plugin: m.Plugin.Entity) -> p.Result[bool]:
        """Register a plugin in the platform."""
        return self.platform.register_plugin(plugin)

    def start_hot_reload(self, paths: t.StrSequence) -> p.Result[bool]:
        """Start hot reload monitoring for the given paths."""
        return self.platform.start_hot_reload(paths)

    def stop_hot_reload(self) -> p.Result[bool]:
        """Stop hot reload monitoring."""
        return self.platform.stop_hot_reload()

    def unregister_plugin(self, plugin_name: str) -> p.Result[bool]:
        """Unregister a plugin by name."""
        return self.platform.unregister_plugin(plugin_name)


plugin = FlextPluginApi

__all__: list[str] = ["FlextPluginApi", "plugin"]
