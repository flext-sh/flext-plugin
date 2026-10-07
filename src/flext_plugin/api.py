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

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence

from flext_core import FlextContainer
from flext_plugin import e, p, r, s, t, u
from flext_plugin._utilities.plugin_platform import FlextPluginUtilitiesPluginPlatform

_Platform = FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform


def _build_default_platform() -> _Platform.PluginPlatformService:
    """Construct the default platform service bound to a fresh container.

    Returns:
        The resulting ``FlextPluginPlatform.PluginPlatformService``.
    """
    return FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.PluginPlatformService(
        container=FlextContainer(),
    )


class FlextPluginApi(s):
    """Railway-oriented plugin facade with composition (MRO via FlextService).

    Per AGENTS.md §2.5 service facade pattern: state via u.PrivateAttr,
    no constructor, public surface returns `r[T]` uniformly.
    """

    _logger: p.Logger = u.PrivateAttr(
        default_factory=lambda: u.fetch_logger("flext_plugin.api"),
    )
    _platform: _Platform.PluginPlatformService = u.PrivateAttr(
        default_factory=_build_default_platform,
    )

    @property
    def platform(
        self,
    ) -> _Platform.PluginPlatformService:
        """The plugin platform service."""
        return self._platform

    @platform.setter
    def platform(
        self,
        value: _Platform.PluginPlatformService,
    ) -> None:
        """Inject the plugin platform service (test hook)."""
        self._platform = value

    def discover_plugins(
        self,
        paths: t.StrSequence,
    ) -> p.Result[
        Sequence[FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin]
    ]:
        """Discover plugins in the given paths; logs the count discovered.

        Returns:
            The resulting ``p.Result[Sequence[FlextPluginPlatform.Plugin]]``.
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

        Returns:
            The resulting ``p.Result[t.JsonMapping]``.
        """
        return self._platform.execute_plugin(plugin_name, context, execution_id).map(
            lambda execution: {"execution_id": execution.execution_id},
        )

    def fetch_plugin(
        self,
        plugin_name: str,
    ) -> p.Result[FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin]:
        """Fetch a plugin by name; fails when missing (ENFORCE-056).

        Returns:
            The resulting ``p.Result[FlextPluginPlatform.Plugin]``.
        """
        plugin = self._platform.fetch_plugin(plugin_name)
        if plugin is None:
            return e.fail_not_found(
                "plugin",
                plugin_name,
                result_type=r[
                    FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin
                ],
            )
        return r[FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin].ok(
            plugin,
        )

    def fetch_plugin_status(self, plugin_name: str) -> p.Result[str]:
        """Fetch the status of a plugin by name; fails when missing.

        Returns:
            The resulting ``p.Result[str]``.
        """
        status = self._platform.fetch_plugin_status(plugin_name)
        if status is None:
            return e.fail_not_found("plugin", plugin_name, result_type=r[str])
        return r[str].ok(status)

    def resolve_plugin_active(self, plugin_name: str) -> p.Result[bool]:
        """Resolve whether a plugin is active.

        Returns:
            The resulting ``p.Result[bool]``.
        """
        return r[bool].ok(self._platform.resolve_plugin_active(plugin_name))

    def list_plugins(
        self,
    ) -> p.Result[
        Sequence[FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin]
    ]:
        """List all registered plugins.

        Returns:
            The resulting ``p.Result[Sequence[FlextPluginPlatform.Plugin]]``.
        """
        return r[
            Sequence[FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin]
        ].ok(self._platform.list_plugins())

    def load_plugin(
        self,
        plugin_path: str,
    ) -> p.Result[FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin]:
        """Load a plugin from the given path; logs the loaded plugin's name.

        Returns:
            The resulting ``p.Result[FlextPluginPlatform.Plugin]``.
        """
        result = self._platform.load_plugin(plugin_path)
        if result.success:
            self._logger.info("Loaded plugin: %s", result.value.name)
        return result

    def register_plugin(
        self,
        plugin: FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin,
    ) -> p.Result[bool]:
        """Register a plugin in the platform.

        Returns:
            The resulting ``p.Result[bool]``.
        """
        return self._platform.register_plugin(plugin)

    def start_hot_reload(self, paths: t.StrSequence) -> p.Result[bool]:
        """Start hot reload monitoring for the given paths.

        Returns:
            The resulting ``p.Result[bool]``.
        """
        return self._platform.start_hot_reload(paths)

    def stop_hot_reload(self) -> p.Result[bool]:
        """Stop hot reload monitoring.

        Returns:
            The resulting ``p.Result[bool]``.
        """
        return self._platform.stop_hot_reload()

    def unregister_plugin(self, plugin_name: str) -> p.Result[bool]:
        """Unregister a plugin by name.

        Returns:
            The resulting ``p.Result[bool]``.
        """
        return self._platform.unregister_plugin(plugin_name)


plugin: FlextPluginApi = FlextPluginApi.fetch_global()
"""Process-wide plugin facade singleton."""

__all__: list[str] = ["FlextPluginApi", "plugin"]
