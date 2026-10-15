"""FLEXT Plugin API - Railway-oriented MRO façade.

`FlextPluginApi` extends `s` (FlextService) so it inherits per-class
`fetch_global()` / `reset_for_testing()` / `with_settings()` from the
canonical service kernel. State (`logger`, `platform`) lives in
`u.PrivateAttr` — no `__init__`, no `__slots__`. All public methods return
`r[T]` (ENFORCE-056 — Uniform `r[T]` Return).

Returns expose the most-specific concrete type produced by the platform
(`FlextPluginPlatform.Plugin`, which extends `m.Plugin.Entity` per
ENFORCE-074 chain inheritance), so callers get covariant access without
losing typing precision.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Sequence

from flext_core import FlextContainer

from flext_plugin import e, p, r, s, t, u
from flext_plugin._utilities import FlextPluginPlatform


class FlextPluginApi(s):
    """Railway-oriented plugin facade with composition (MRO via FlextService).

    Per AGENTS.md §2.5 service facade pattern: state via u.PrivateAttr,
    no constructor, public surface returns `r[T]` uniformly.

    """

    _logger: p.Logger = u.PrivateAttr(
        default_factory=lambda: u.fetch_logger("flext_plugin.api"),
    )
    _platform: FlextPluginPlatform.PluginPlatformService = u.PrivateAttr(
        default_factory=lambda: FlextPluginPlatform.PluginPlatformService(
            container=FlextContainer(),
        ),
    )

    @property
    def platform(
        self,
    ) -> FlextPluginPlatform.PluginPlatformService:
        """The plugin platform service backing this facade."""
        return self._platform

    @platform.setter
    def platform(
        self,
        value: (FlextPluginPlatform.PluginPlatformService),
    ) -> None:
        """Inject the plugin platform service (test hook).

        Args:
            value: Platform service to back this facade.

        """
        self._platform = value

    def discover_plugins(
        self,
        paths: t.StrSequence,
    ) -> p.Result[Sequence[FlextPluginPlatform.Plugin]]:
        """Discover plugins in the given paths; logs the count discovered.

        Args:
            paths: Filesystem paths to scan for plugin modules.

        Returns:
            Ok with the discovered plugins, or Fail with the discovery error.

        """
        result = self._platform.discover_plugins(paths)
        if result.success:
            self._logger.info("Discovered %s plugins", len(result.value))
        return result

    def execute_plugin(
        self,
        plugin_name: str,
        context: t.JsonMapping,
        execution_id: str | None = None,
    ) -> p.Result[t.JsonMapping]:
        """Execute a plugin by name with the given context.

        Args:
            plugin_name: Name of the registered plugin to run.
            context: Input payload passed to the plugin entry point.
            execution_id: Optional identifier to track this execution.

        Returns:
            Ok with the execution id, or Fail with the execution error.

        """
        return self._platform.execute_plugin(plugin_name, context, execution_id).map(
            lambda execution: {"execution_id": execution.execution_id},
        )

    def fetch_plugin(
        self,
        plugin_name: str,
    ) -> p.Result[FlextPluginPlatform.Plugin]:
        """Fetch a plugin by name; fails when missing (ENFORCE-056).

        Args:
            plugin_name: Name of the plugin to fetch.

        Returns:
            Ok with the plugin, or Fail when no plugin is registered
            under the given name.

        """
        plugin = self._platform.fetch_plugin(plugin_name)
        if plugin is None:
            return e.fail_not_found(
                "plugin",
                plugin_name,
                result_type=r[FlextPluginPlatform.Plugin],
            )
        return r[FlextPluginPlatform.Plugin].ok(
            plugin,
        )

    def fetch_plugin_status(self, plugin_name: str) -> p.Result[str]:
        """Fetch the status of a plugin by name; fails when missing.

        Args:
            plugin_name: Name of the plugin whose status to fetch.

        Returns:
            Ok with the status string, or Fail when the plugin has no
            recorded status.

        """
        status = self._platform.fetch_plugin_status(plugin_name)
        if status is None:
            return e.fail_not_found("plugin", plugin_name, result_type=r[str])
        return r[str].ok(status)

    def resolve_plugin_active(self, plugin_name: str) -> p.Result[bool]:
        """Resolve whether a plugin is active.

        Args:
            plugin_name: Name of the plugin to inspect.

        Returns:
            Ok with ``True`` when the plugin is active, ``False`` otherwise.

        """
        return r[bool].ok(self._platform.resolve_plugin_active(plugin_name))

    def list_plugins(
        self,
    ) -> p.Result[Sequence[FlextPluginPlatform.Plugin]]:
        """List all registered plugins.

        Returns:
            Ok with the registered plugins in registration order.

        """
        return r[Sequence[FlextPluginPlatform.Plugin]].ok(self._platform.list_plugins())

    def load_plugin(
        self,
        plugin_path: str,
    ) -> p.Result[FlextPluginPlatform.Plugin]:
        """Load a plugin from the given path; logs the loaded plugin's name.

        Args:
            plugin_path: Filesystem path of the plugin module to load.

        Returns:
            Ok with the loaded plugin, or Fail with the load error.

        """
        result = self._platform.load_plugin(plugin_path)
        if result.success:
            self._logger.info("Loaded plugin: %s", result.value.name)
        return result

    def register_plugin(
        self,
        plugin: FlextPluginPlatform.Plugin,
    ) -> p.Result[bool]:
        """Register a plugin in the platform.

        Args:
            plugin: Plugin entity to register.

        Returns:
            Ok with ``True`` when registration succeeds, or Fail with the
            registration error.

        """
        return self._platform.register_plugin(plugin)

    def start_hot_reload(self, paths: t.StrSequence) -> p.Result[bool]:
        """Start hot reload monitoring for the given paths.

        Args:
            paths: Filesystem paths to watch for plugin changes.

        Returns:
            Ok with ``True`` when monitoring starts, or Fail when the
            watcher cannot be started.

        """
        return self._platform.start_hot_reload(paths)

    def stop_hot_reload(self) -> p.Result[bool]:
        """Stop hot reload monitoring.

        Returns:
            Ok with ``True`` when monitoring stops, or Fail when the
            watcher cannot be stopped.

        """
        return self._platform.stop_hot_reload()

    def unregister_plugin(self, plugin_name: str) -> p.Result[bool]:
        """Unregister a plugin by name.

        Args:
            plugin_name: Name of the plugin to remove from the registry.

        Returns:
            Ok with ``True`` when the plugin is removed, or Fail when the
            plugin is not registered.

        """
        return self._platform.unregister_plugin(plugin_name)


plugin: FlextPluginApi = FlextPluginApi.fetch_global()
"""Process-wide plugin facade singleton."""

__all__: list[str] = ["FlextPluginApi", "plugin"]
