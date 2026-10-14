"""Platform protocol namespace for flext-plugin.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Sequence

    from flext_plugin import m, p, t
    from flext_plugin._protocols import FlextPluginProtocolsPlugin
    from flext_plugin._utilities import FlextPluginPlatform


class FlextPluginProtocolsPlatform:
    """Platform protocol namespace for flext-plugin."""

    @runtime_checkable
    class PlatformService(Protocol):
        """Protocol for the public plugin platform facade surface."""

        @property
        def discovery(self) -> FlextPluginProtocolsPlugin.Discovery | None:
            """The configured discovery protocol implementation."""
            ...

        @discovery.setter
        def discovery(
            self,
            value: FlextPluginProtocolsPlugin.Discovery | None,
        ) -> None: ...

        @property
        def loader(self) -> FlextPluginProtocolsPlugin.Loader | None:
            """The configured loader protocol implementation."""
            ...

        @loader.setter
        def loader(self, value: FlextPluginProtocolsPlugin.Loader | None) -> None: ...

        @property
        def executor(self) -> FlextPluginProtocolsPlugin.Execution | None:
            """The configured executor protocol implementation."""
            ...

        @executor.setter
        def executor(
            self,
            value: FlextPluginProtocolsPlugin.Execution | None,
        ) -> None: ...

        def discover_plugins(
            self,
            paths: t.StrSequence,
        ) -> p.Result[Sequence[FlextPluginPlatform.Plugin]]:
            """Discover plugins from the provided paths.

            Args:
                paths: Filesystem paths to scan for plugin modules.

            Returns:
                Ok with the discovered plugins, or Fail with the
                discovery error.

            """
            ...

        def execute_plugin(
            self,
            plugin_name: str,
            context: t.JsonMapping,
            execution_id: str | None = None,
        ) -> p.Result[FlextPluginPlatform.PluginExecution]:
            """Execute a plugin with the provided context.

            Args:
                plugin_name: Name of the registered plugin to run.
                context: Input payload passed to the plugin entry point.
                execution_id: Optional identifier to track this execution.

            Returns:
                Ok with the recorded execution, or Fail with the
                execution error.

            """
            ...

        def fetch_plugin(
            self,
            name: str,
        ) -> FlextPluginPlatform.Plugin | None:
            """Fetch a plugin by name.

            Args:
                name: Name of the plugin to fetch.

            Returns:
                The registered plugin, or ``None`` when no plugin is
                registered under the name.

            """
            ...

        def fetch_plugin_status(self, name: str) -> str | None:
            """Fetch the status of a plugin by name.

            Args:
                name: Name of the plugin whose status to fetch.

            Returns:
                The status string, or ``None`` when the plugin has no
                recorded status.

            """
            ...

        def resolve_plugin_active(self, name: str) -> bool:
            """Resolve whether the named plugin is active.

            Args:
                name: Name of the plugin to inspect.

            Returns:
                ``True`` when the plugin is active, ``False`` otherwise.

            """
            ...

        def list_plugins(
            self,
        ) -> Sequence[FlextPluginPlatform.Plugin]:
            """List registered plugins.

            Returns:
                The registered plugins in registration order.

            """
            ...

        def load_plugin(
            self,
            plugin_path: str,
        ) -> p.Result[FlextPluginPlatform.Plugin]:
            """Load a plugin from disk.

            Args:
                plugin_path: Filesystem path of the plugin module.

            Returns:
                Ok with the loaded plugin, or Fail with the load error.

            """
            ...

        def register_plugin(
            self,
            plugin: (FlextPluginPlatform.Plugin | m.Plugin.Entity),
        ) -> p.Result[bool]:
            """Register a plugin instance.

            Args:
                plugin: Plugin entity to register.

            Returns:
                Ok with ``True`` when registration succeeds, or Fail with
                the registration error.

            """
            ...

        def start_hot_reload(self, paths: t.StrSequence) -> p.Result[bool]:
            """Start plugin hot reload monitoring.

            Args:
                paths: Filesystem paths to watch for plugin changes.

            Returns:
                Ok with ``True`` when monitoring starts, or Fail when the
                watcher cannot be started.

            """
            ...

        def stop_hot_reload(self) -> p.Result[bool]:
            """Stop plugin hot reload monitoring.

            Returns:
                Ok with ``True`` when monitoring stops, or Fail when the
                watcher cannot be stopped.

            """
            ...

        def unregister_plugin(self, plugin_name: str) -> p.Result[bool]:
            """Unregister a plugin by name.

            Args:
                plugin_name: Name of the plugin to remove.

            Returns:
                Ok with ``True`` when the plugin is removed, or Fail when
                the plugin is not registered.

            """
            ...


__all__: list[str] = ["FlextPluginProtocolsPlatform"]
