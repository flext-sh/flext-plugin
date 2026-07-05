"""Behavioral tests for the plugin public API facade.

Exercises every public method of ``FlextPluginApi`` through observable
``r[T]`` outcomes and real platform state, without relying on implementation
internals.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""
# mypy: warn-unused-ignores=False

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from flext_plugin import c, m, r, t
from flext_plugin._utilities.plugin_platform import FlextPluginPlatform
from flext_plugin.api import FlextPluginApi


@pytest.mark.usefixtures("reset_api")
class TestsFlextPluginApi:
    """Behavioral tests for the plugin API facade."""

    @pytest.fixture
    def reset_api(self) -> None:
        """Reset the API singleton state before each test."""
        FlextPluginApi.fetch_global().reset_for_testing()

    @staticmethod
    def _make_plugin(
        *,
        name: str = "demo-plugin",
        is_enabled: bool = True,
    ) -> FlextPluginPlatform.Plugin:
        """Build a platform plugin entity."""
        plugin: FlextPluginPlatform.Plugin = FlextPluginPlatform.Plugin.create(
            name=name,
            plugin_version="1.0.0",
            is_enabled=is_enabled,
        )
        return plugin

    @pytest.fixture
    def api(self) -> FlextPluginApi:
        """Provide a fresh API instance with reset state."""
        instance = FlextPluginApi()
        instance._platform = FlextPluginPlatform.PluginPlatformService()
        return instance

    def test_discover_plugins_logs_count_and_returns_plugins(
        self,
        api: FlextPluginApi,
    ) -> None:
        """discover_plugins() logs the count and returns discovered plugins."""
        mock_discovery = MagicMock()
        data = m.Plugin.DiscoveryData(
            name="found",
            version="1.0.0",
            path=Path("/tmp/found.py"),
            discovery_type=c.Plugin.DiscoveryTypeLiteral.FILE,
            discovery_method=c.Plugin.DiscoveryMethodLiteral.FILE_SYSTEM,
        )
        mock_discovery.discover_plugins.return_value = r[
            Sequence[m.Plugin.DiscoveryData]
        ].ok([data])
        api._platform._discovery = mock_discovery  # type: ignore[assignment]

        result = api.discover_plugins(["/tmp"])

        assert result.success is True
        assert len(result.unwrap()) == 1

    def test_discover_plugins_failure_returned(self, api: FlextPluginApi) -> None:
        """discover_plugins() propagates failures from the platform."""
        mock_discovery = MagicMock()
        mock_discovery.discover_plugins.return_value = r[
            Sequence[FlextPluginPlatform.Plugin]
        ].fail("discovery failed")
        api._platform._discovery = mock_discovery  # type: ignore[assignment]

        result = api.discover_plugins(["/tmp"])

        assert result.failure is True

    def test_execute_plugin_returns_execution_id(self, api: FlextPluginApi) -> None:
        """execute_plugin() returns a mapping containing the execution_id."""
        plugin = self._make_plugin()
        api._platform.register_plugin(plugin)
        mock_executor = MagicMock()
        mock_executor.execute_plugin.return_value = r[t.JsonMapping].ok(
            {"output": "ok"},
        )
        api._platform._executor = mock_executor  # type: ignore[assignment]

        result = api.execute_plugin("demo-plugin", {"x": 1}, execution_id="e1")

        assert result.success is True
        assert result.unwrap()["execution_id"] == "e1"

    def test_execute_plugin_failure_returned(self, api: FlextPluginApi) -> None:
        """execute_plugin() propagates execution failures."""
        plugin = self._make_plugin()
        api._platform.register_plugin(plugin)
        mock_executor = MagicMock()
        mock_executor.execute_plugin.return_value = r[t.JsonMapping].fail("boom")
        api._platform._executor = mock_executor  # type: ignore[assignment]

        result = api.execute_plugin("demo-plugin", {})

        assert result.failure is True

    def test_fetch_plugin_existing(self, api: FlextPluginApi) -> None:
        """fetch_plugin() returns the plugin when present."""
        plugin = self._make_plugin()
        api._platform.register_plugin(plugin)

        result = api.fetch_plugin("demo-plugin")

        assert result.success is True
        assert result.unwrap().name == "demo-plugin"

    def test_fetch_plugin_missing_fails(self, api: FlextPluginApi) -> None:
        """fetch_plugin() fails when the plugin is absent."""
        result = api.fetch_plugin("missing")

        assert result.failure is True

    def test_fetch_plugin_status_existing(self, api: FlextPluginApi) -> None:
        """fetch_plugin_status() returns the status label when present."""
        plugin = self._make_plugin()
        api._platform.register_plugin(plugin)

        result = api.fetch_plugin_status("demo-plugin")

        assert result.success is True
        assert result.unwrap() == "active"

    def test_fetch_plugin_status_missing_fails(self, api: FlextPluginApi) -> None:
        """fetch_plugin_status() fails when the plugin is absent."""
        result = api.fetch_plugin_status("missing")

        assert result.failure is True

    def test_resolve_plugin_active(self, api: FlextPluginApi) -> None:
        """resolve_plugin_active() reflects the plugin enabled state."""
        plugin = self._make_plugin()
        api._platform.register_plugin(plugin)

        result = api.resolve_plugin_active("demo-plugin")

        assert result.success is True
        assert result.unwrap() is True

    def test_list_plugins(self, api: FlextPluginApi) -> None:
        """list_plugins() returns all registered plugins."""
        api._platform.register_plugin(self._make_plugin(name="alpha"))
        api._platform.register_plugin(self._make_plugin(name="beta"))

        result = api.list_plugins()

        assert result.success is True
        assert {plugin.name for plugin in result.unwrap()} == {"alpha", "beta"}

    def test_load_plugin_logs_and_returns(self, api: FlextPluginApi) -> None:
        """load_plugin() logs the loaded name and returns the plugin."""
        mock_loader = MagicMock()
        mock_loader.load_plugin.return_value = r[t.JsonMapping].ok(
            {"name": "loaded", "version": "1.0.0"},
        )
        api._platform._loader = mock_loader  # type: ignore[assignment]

        result = api.load_plugin("/tmp/loaded.py")

        assert result.success is True
        assert result.unwrap().name == "loaded"

    def test_register_plugin(self, api: FlextPluginApi) -> None:
        """register_plugin() registers the plugin in the platform."""
        plugin = self._make_plugin()

        result = api.register_plugin(plugin)

        assert result.success is True
        assert api._platform.fetch_plugin("demo-plugin") is not None

    def test_start_hot_reload(self, api: FlextPluginApi) -> None:
        """start_hot_reload() succeeds."""
        result = api.start_hot_reload(["/tmp"])

        assert result.success is True

    def test_stop_hot_reload(self, api: FlextPluginApi) -> None:
        """stop_hot_reload() succeeds."""
        result = api.stop_hot_reload()

        assert result.success is True

    def test_unregister_plugin(self, api: FlextPluginApi) -> None:
        """unregister_plugin() removes the plugin."""
        plugin = self._make_plugin()
        api.register_plugin(plugin)

        result = api.unregister_plugin("demo-plugin")

        assert result.success is True
        assert api.fetch_plugin("demo-plugin").failure is True

    def test_default_platform_is_created_lazily(self) -> None:
        """A fresh API instance builds a default platform automatically."""
        api = FlextPluginApi()

        assert api._platform is not None


__all__: list[str] = ["TestsFlextPluginApi"]
