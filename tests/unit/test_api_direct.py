"""Behavioral tests for the plugin public API facade.

Exercises every public method of ``FlextPluginApi`` through observable
``r[T]`` outcomes and real platform state, without relying on implementation
internals.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""
# mypy: warn-unused-ignores=False

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from flext_plugin.api import FlextPluginApi
from flext_plugin.utilities import FlextPluginDiscovery, FlextPluginPlatform
from tests import tm, u

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.usefixtures("reset_api")
class TestsFlextPluginApi:
    """Behavioral tests for the plugin API facade."""

    @staticmethod
    @pytest.fixture
    def reset_api() -> None:
        """Reset the API singleton state before each test (direct entry point)."""
        api_ref = FlextPluginApi.fetch_global()
        api_ref.reset_for_testing()
        del api_ref

    @staticmethod
    def _make_plugin(
        *,
        name: str = "demo-plugin",
        is_enabled: bool = True,
    ) -> FlextPluginPlatform.Plugin:
        """Build a platform plugin entity.

        Returns:
            The resulting ``FlextPluginPlatform.Plugin``.
        """
        return FlextPluginPlatform.Plugin(
            name=name,
            plugin_version="1.0.0",
            is_enabled=is_enabled,
        )

    @staticmethod
    @pytest.fixture
    def api() -> FlextPluginApi:
        """Provide a fresh API instance with reset state.

        Returns:
            The resulting ``FlextPluginApi``.
        """
        instance = FlextPluginApi()
        instance.platform = FlextPluginPlatform.PluginPlatformService()
        return instance

    @staticmethod
    def test_discover_plugins_logs_count_and_returns_plugins(
        api: FlextPluginApi,
        tmp_path: Path,
    ) -> None:
        """discover_plugins() logs the count and returns discovered plugins."""
        (tmp_path / "found.py").write_text(
            '"""Real plugin module."""\n',
            encoding="utf-8",
        )
        api.platform.discovery = FlextPluginDiscovery()

        result = api.discover_plugins([str(tmp_path)])

        tm.that(result.success, eq=True)
        assert any(plugin.name == "found" for plugin in result.unwrap())

    @staticmethod
    def test_discover_plugins_failure_returned(
        api: FlextPluginApi,
        tmp_path: Path,
    ) -> None:
        """discover_plugins() propagates failures from the platform."""
        api.platform.discovery = u.Plugin.Tests.FailingDiscovery()

        result = api.discover_plugins([str(tmp_path / "nonexistent")])

        tm.that(result.failure, eq=True)

    def test_execute_plugin_returns_execution_id(self, api: FlextPluginApi) -> None:
        """execute_plugin() returns a mapping containing the execution_id."""
        plugin = self._make_plugin()
        api.register_plugin(plugin)
        api.platform.executor = u.Plugin.Tests.EchoExecutor()

        result = api.execute_plugin("demo-plugin", {"x": 1}, execution_id="e1")

        tm.that(result.success, eq=True)
        tm.that(result.unwrap()["execution_id"], eq="e1")

    def test_execute_plugin_failure_returned(self, api: FlextPluginApi) -> None:
        """execute_plugin() propagates execution failures."""
        plugin = self._make_plugin()
        api.register_plugin(plugin)
        api.platform.executor = u.Plugin.Tests.FailingExecutor()

        result = api.execute_plugin("demo-plugin", {})

        tm.that(result.failure, eq=True)

    def test_fetch_plugin_existing(self, api: FlextPluginApi) -> None:
        """fetch_plugin() returns the plugin when present."""
        plugin = self._make_plugin()
        api.register_plugin(plugin)

        result = api.fetch_plugin("demo-plugin")

        tm.that(result.success, eq=True)
        tm.that(result.unwrap().name, eq="demo-plugin")

    @staticmethod
    def test_fetch_plugin_missing_fails(api: FlextPluginApi) -> None:
        """fetch_plugin() fails when the plugin is absent."""
        result = api.fetch_plugin("missing")

        tm.that(result.failure, eq=True)

    def test_fetch_plugin_status_existing(self, api: FlextPluginApi) -> None:
        """fetch_plugin_status() returns the status label when present."""
        plugin = self._make_plugin()
        api.register_plugin(plugin)

        result = api.fetch_plugin_status("demo-plugin")

        tm.that(result.success, eq=True)
        tm.that(result.unwrap(), eq="active")

    @staticmethod
    def test_fetch_plugin_status_missing_fails(api: FlextPluginApi) -> None:
        """fetch_plugin_status() fails when the plugin is absent."""
        result = api.fetch_plugin_status("missing")

        tm.that(result.failure, eq=True)

    def test_resolve_plugin_active(self, api: FlextPluginApi) -> None:
        """resolve_plugin_active() reflects the plugin enabled state."""
        plugin = self._make_plugin()
        api.register_plugin(plugin)

        result = api.resolve_plugin_active("demo-plugin")

        tm.that(result.success, eq=True)
        tm.that(result.unwrap(), eq=True)

    def test_list_plugins(self, api: FlextPluginApi) -> None:
        """list_plugins() returns all registered plugins."""
        api.register_plugin(self._make_plugin(name="alpha"))
        api.register_plugin(self._make_plugin(name="beta"))

        result = api.list_plugins()

        tm.that(result.success, eq=True)
        tm.that(
            {plugin.name for plugin in result.unwrap()},
            eq=frozenset({"alpha", "beta"}),
        )

    @staticmethod
    def test_load_plugin_logs_and_returns(
        api: FlextPluginApi,
        tmp_path: Path,
    ) -> None:
        """load_plugin() logs the loaded name and returns the plugin."""
        plugin_file = tmp_path / "loaded.py"
        plugin_file.write_text('"""Real loadable plugin."""\n', encoding="utf-8")
        api.platform.loader = u.Plugin.Tests.FilePluginLoader()

        result = api.load_plugin(str(plugin_file))

        tm.that(result.success, eq=True)
        tm.that(result.unwrap().name, eq="loaded")

    def test_register_plugin(self, api: FlextPluginApi) -> None:
        """register_plugin() registers the plugin in the platform."""
        plugin = self._make_plugin()

        result = api.register_plugin(plugin)

        tm.that(result.success, eq=True)
        tm.that(api.platform.fetch_plugin("demo-plugin"), none=False)

    @staticmethod
    def test_start_hot_reload(api: FlextPluginApi, tmp_path: Path) -> None:
        """start_hot_reload() succeeds."""
        result = api.start_hot_reload([str(tmp_path)])

        tm.that(result.success, eq=True)

    @staticmethod
    def test_stop_hot_reload(api: FlextPluginApi) -> None:
        """stop_hot_reload() succeeds."""
        result = api.stop_hot_reload()

        tm.that(result.success, eq=True)

    def test_unregister_plugin(self, api: FlextPluginApi) -> None:
        """unregister_plugin() removes the plugin."""
        plugin = self._make_plugin()
        api.register_plugin(plugin)

        result = api.unregister_plugin("demo-plugin")

        tm.that(result.success, eq=True)
        tm.that(api.fetch_plugin("demo-plugin").failure, eq=True)

    @staticmethod
    def test_default_platform_is_created_lazily() -> None:
        """A fresh API instance builds a default platform automatically."""
        api = FlextPluginApi()

        tm.that(api.platform, none=False)
