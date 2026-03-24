"""Test suite for flext_plugin platform module.

Tests the Plugin and PluginRegistry classes from platform.py.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_plugin import FlextPluginModels, FlextPluginPlatform


class TestPluginModel:
    """Tests for Plugin model class."""

    def test_plugin_create(self) -> None:
        """Test plugin creation with factory method."""
        plugin = FlextPluginModels.Plugin.Plugin.create(
            name="test-plugin",
            plugin_version="1.0.0",
        )
        assert plugin.name == "test-plugin"
        assert plugin.plugin_version == "1.0.0"
        assert plugin.is_enabled

    def test_plugin_enable(self) -> None:
        """Test plugin enable method."""
        plugin = FlextPluginModels.Plugin.Plugin.create(
            name="test-plugin",
            plugin_version="1.0.0",
            is_enabled=False,
        )
        assert not plugin.is_enabled
        result = plugin.enable()
        assert result.is_success
        assert plugin.is_enabled

    def test_plugin_enable_already_enabled(self) -> None:
        """Test enabling already enabled plugin."""
        plugin = FlextPluginModels.Plugin.Plugin.create(
            name="test-plugin",
            plugin_version="1.0.0",
            is_enabled=True,
        )
        result = plugin.enable()
        assert result.is_failure
        assert result.error is not None
        assert "already enabled" in result.error

    def test_plugin_disable(self) -> None:
        """Test plugin disable method."""
        plugin = FlextPluginModels.Plugin.Plugin.create(
            name="test-plugin",
            plugin_version="1.0.0",
            is_enabled=True,
        )
        assert plugin.is_enabled
        result = plugin.disable()
        assert result.is_success
        assert not plugin.is_enabled

    def test_plugin_disable_already_disabled(self) -> None:
        """Test disabling already disabled plugin."""
        plugin = FlextPluginModels.Plugin.Plugin.create(
            name="test-plugin",
            plugin_version="1.0.0",
            is_enabled=False,
        )
        result = plugin.disable()
        assert result.is_failure
        assert result.error is not None
        assert "already disabled" in result.error


class TestPluginPlatform:
    """Tests for FlextPluginPlatform.Plugin class from platform.py."""

    def test_plugin_is_active_when_enabled(self) -> None:
        """Test is_active returns True when plugin is enabled."""
        plugin = FlextPluginPlatform.Plugin(
            name="test-plugin",
            plugin_version="1.0.0",
            is_enabled=True,
        )
        assert plugin.is_active()

    def test_plugin_is_active_when_disabled(self) -> None:
        """Test is_active returns False when plugin is disabled."""
        plugin = FlextPluginPlatform.Plugin(
            name="test-plugin",
            plugin_version="1.0.0",
            is_enabled=False,
        )
        assert not plugin.is_active()

    def test_plugin_status_active(self) -> None:
        """Test status property when active."""
        plugin = FlextPluginPlatform.Plugin(
            name="test-plugin",
            plugin_version="1.0.0",
            is_enabled=True,
        )
        assert plugin.status == "active"

    def test_plugin_status_inactive(self) -> None:
        """Test status property when inactive."""
        plugin = FlextPluginPlatform.Plugin(
            name="test-plugin",
            plugin_version="1.0.0",
            is_enabled=False,
        )
        assert plugin.status == "inactive"


class TestPluginRegistry:
    """Tests for FlextPluginPlatform.PluginRegistry class."""

    @pytest.fixture(autouse=True)
    def reset_registry(self) -> None:
        """Reset class-level storage before each test."""
        FlextPluginPlatform.PluginRegistry._class_plugin_storage = {}
        FlextPluginPlatform.PluginRegistry._class_registered_keys = set()

    @pytest.fixture
    def registry(self) -> FlextPluginPlatform.PluginRegistry:
        """Create registry instance for testing."""
        return FlextPluginPlatform.PluginRegistry.create()

    @pytest.fixture
    def plugin(self) -> FlextPluginPlatform.Plugin:
        """Create plugin for registry testing."""
        return FlextPluginPlatform.Plugin(name="test-plugin", plugin_version="1.0.0")

    def test_registry_initialization(
        self,
        registry: FlextPluginPlatform.PluginRegistry,
    ) -> None:
        """Test registry initialization."""
        plugins_result = registry.list_plugins()
        assert plugins_result.is_success
        assert not plugins_result.value

    def test_register_plugin_success(
        self,
        registry: FlextPluginPlatform.PluginRegistry,
        plugin: FlextPluginPlatform.Plugin,
    ) -> None:
        """Test successful plugin registration."""
        result = registry.register(plugin.name, plugin)
        assert result.is_success
        assert result.value
        get_result = registry.get(plugin.name)
        assert get_result.is_success
        assert get_result.value.name == plugin.name

    def test_unregister_plugin_success(
        self,
        registry: FlextPluginPlatform.PluginRegistry,
        plugin: FlextPluginPlatform.Plugin,
    ) -> None:
        """Test successful plugin unregistration."""
        registry.register(plugin.name, plugin)
        plugins_result = registry.list_plugins()
        assert plugin.name in plugins_result.value
        result = registry.unregister(plugin.name)
        assert result.is_success
        assert result.value
        plugins_result = registry.list_plugins()
        assert plugin.name not in plugins_result.value

    def test_unregister_nonexistent_plugin(
        self,
        registry: FlextPluginPlatform.PluginRegistry,
    ) -> None:
        """Test unregistering plugin that doesn't exist."""
        result = registry.unregister("nonexistent-plugin")
        assert result.is_failure

    def test_register_multiple_plugins(
        self,
        registry: FlextPluginPlatform.PluginRegistry,
    ) -> None:
        """Test registering multiple plugins."""
        plugins = [
            FlextPluginPlatform.Plugin(name=f"plugin-{i}", plugin_version="1.0.0")
            for i in range(3)
        ]
        for plugin in plugins:
            result = registry.register(plugin.name, plugin)
            assert result.is_success
        plugins_result = registry.list_plugins()
        assert len(plugins_result.value) == 3
        for plugin in plugins:
            assert plugin.name in plugins_result.value
