"""Behavioral test suite for the flext_plugin platform module.

Exercises the public contract of the Plugin entity and PluginRegistry:
factory creation, enable/disable lifecycle (r[T] outcomes), status/active
projection, business-rule validation, and registry register/get/list/
unregister semantics. Asserts observable behavior only — never internals.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_plugin import u
from tests.models import m

FlextPluginPlatform = u.Plugin.Platform


@pytest.mark.usefixtures("reset_registry")
class TestsFlextPluginPlugin:
    """Behavioral tests for the Plugin entity and PluginRegistry contract."""

    @staticmethod
    def _make_plugin(
        *,
        name: str = "test-plugin",
        is_enabled: bool = True,
    ) -> FlextPluginPlatform.Plugin:
        """Build a Plugin platform entity for registry-facing tests."""
        return FlextPluginPlatform.Plugin(
            name=name,
            plugin_version="1.0.0",
            description="",
            author="",
            plugin_type="utility",
            is_enabled=is_enabled,
        )

    # ----- Plugin entity: creation contract -------------------------------

    def test_create_returns_entity_with_supplied_fields(self) -> None:
        """create() yields an entity exposing the given name and version."""
        plugin = m.Plugin.Entity.create(name="test-plugin", plugin_version="1.0.0")
        assert plugin.name == "test-plugin"
        assert plugin.plugin_version == "1.0.0"

    def test_create_defaults_to_enabled(self) -> None:
        """A freshly created plugin defaults to the enabled state."""
        plugin = m.Plugin.Entity.create(name="test-plugin", plugin_version="1.0.0")
        assert plugin.is_enabled is True

    def test_create_honors_explicit_disabled_state(self) -> None:
        """create() respects an explicit is_enabled=False argument."""
        plugin = m.Plugin.Entity.create(
            name="test-plugin",
            plugin_version="1.0.0",
            is_enabled=False,
        )
        assert plugin.is_enabled is False

    @pytest.mark.parametrize("bad_version", ["1", "1.2.3.4", "1.x", "abc"])
    def test_create_rejects_non_semantic_version(self, bad_version: str) -> None:
        """create() raises when the version is not semantic X.Y[.Z]."""
        with pytest.raises(ValueError, match="semantic"):
            m.Plugin.Entity.create(name="test-plugin", plugin_version=bad_version)

    # ----- Plugin entity: enable/disable lifecycle ------------------------

    def test_enable_disabled_plugin_succeeds_and_flips_state(self) -> None:
        """enable() on a disabled plugin succeeds and turns it enabled."""
        plugin = m.Plugin.Entity.create(
            name="test-plugin",
            plugin_version="1.0.0",
            is_enabled=False,
        )
        result = u.Plugin.Platform.Rules.enable(plugin)
        assert result.success
        assert plugin.is_enabled is True

    def test_enable_already_enabled_fails_without_state_change(self) -> None:
        """enable() on an enabled plugin fails and leaves it enabled."""
        plugin = m.Plugin.Entity.create(
            name="test-plugin",
            plugin_version="1.0.0",
            is_enabled=True,
        )
        result = u.Plugin.Platform.Rules.enable(plugin)
        assert result.failure
        assert result.error is not None
        assert "already enabled" in result.error
        assert plugin.is_enabled is True

    def test_disable_enabled_plugin_succeeds_and_flips_state(self) -> None:
        """disable() on an enabled plugin succeeds and turns it disabled."""
        plugin = m.Plugin.Entity.create(
            name="test-plugin",
            plugin_version="1.0.0",
            is_enabled=True,
        )
        result = u.Plugin.Platform.Rules.disable(plugin)
        assert result.success
        assert plugin.is_enabled is False

    def test_disable_already_disabled_fails_without_state_change(self) -> None:
        """disable() on a disabled plugin fails and leaves it disabled."""
        plugin = m.Plugin.Entity.create(
            name="test-plugin",
            plugin_version="1.0.0",
            is_enabled=False,
        )
        result = u.Plugin.Platform.Rules.disable(plugin)
        assert result.failure
        assert result.error is not None
        assert "already disabled" in result.error
        assert plugin.is_enabled is False

    def test_disable_then_enable_round_trips_to_enabled(self) -> None:
        """A disable followed by enable returns the plugin to enabled."""
        plugin = m.Plugin.Entity.create(
            name="test-plugin",
            plugin_version="1.0.0",
            is_enabled=True,
        )
        assert u.Plugin.Platform.Rules.disable(plugin).success
        assert u.Plugin.Platform.Rules.enable(plugin).success
        assert plugin.is_enabled is True

    # ----- Plugin entity: business rules & metadata -----------------------

    def test_validate_business_rules_accepts_valid_plugin(self) -> None:
        """A well-formed plugin passes business-rule validation."""
        plugin = m.Plugin.Entity.create(name="test-plugin", plugin_version="1.0.0")
        result = u.Plugin.Platform.Rules.validate_business_rules(plugin)
        assert result.success

    def test_record_error_is_observable_in_public_metadata(self) -> None:
        """record_error() surfaces count and message via the metadata field."""
        plugin = m.Plugin.Entity.create(name="test-plugin", plugin_version="1.0.0")
        u.Plugin.Platform.Rules.record_error(plugin, "boom")
        assert plugin.metadata["error_count"] == 1
        assert plugin.metadata["last_error"] == "boom"

    def test_record_error_accumulates_count(self) -> None:
        """Repeated record_error() calls increment the observable error count."""
        plugin = m.Plugin.Entity.create(name="test-plugin", plugin_version="1.0.0")
        u.Plugin.Platform.Rules.record_error(plugin, "first")
        u.Plugin.Platform.Rules.record_error(plugin, "second")
        assert plugin.metadata["error_count"] == 2
        assert plugin.metadata["last_error"] == "second"

    # ----- Plugin platform entity: status / active projection -------------

    @pytest.mark.parametrize(
        ("is_enabled", "expected_status", "expected_active"),
        [
            (True, "active", True),
            (False, "inactive", False),
        ],
    )
    def test_status_and_active_reflect_enabled_state(
        self,
        *,
        is_enabled: bool,
        expected_status: str,
        expected_active: bool,
    ) -> None:
        """Status and active() derive directly from the enabled state."""
        plugin = self._make_plugin(is_enabled=is_enabled)
        assert plugin.status == expected_status
        assert plugin.active() is expected_active

    # ----- Registry fixtures ----------------------------------------------

    @pytest.fixture
    def reset_registry(self) -> None:
        """Reset class-level registry storage before each test."""
        registry = FlextPluginPlatform.PluginRegistry.create()
        plugins_result = registry.list_plugins()
        if plugins_result.success:
            for plugin_name in plugins_result.value:
                _ = registry.unregister(plugin_name)

    @pytest.fixture
    def registry(self) -> FlextPluginPlatform.PluginRegistry:
        """Create a registry instance for testing."""
        return FlextPluginPlatform.PluginRegistry.create()

    @pytest.fixture
    def plugin(self) -> FlextPluginPlatform.Plugin:
        """Create a plugin for registry testing."""
        return self._make_plugin()

    # ----- Registry: lifecycle contract -----------------------------------

    def test_new_registry_lists_no_plugins(
        self,
        registry: FlextPluginPlatform.PluginRegistry,
    ) -> None:
        """A cleared registry reports an empty plugin listing."""
        plugins_result = registry.list_plugins()
        assert plugins_result.success
        assert not plugins_result.value

    def test_register_then_get_returns_same_plugin(
        self,
        registry: FlextPluginPlatform.PluginRegistry,
        plugin: FlextPluginPlatform.Plugin,
    ) -> None:
        """A registered plugin is retrievable by name via get()."""
        register_result = registry.register(plugin.name, plugin)
        assert register_result.success
        assert register_result.value is True

        get_result = registry.get(plugin.name)
        assert get_result.success
        assert get_result.value.name == plugin.name

    def test_registered_plugin_appears_in_listing(
        self,
        registry: FlextPluginPlatform.PluginRegistry,
        plugin: FlextPluginPlatform.Plugin,
    ) -> None:
        """A registered plugin's name is present in list_plugins()."""
        registry.register(plugin.name, plugin)
        plugins_result = registry.list_plugins()
        assert plugins_result.success
        assert plugin.name in plugins_result.value

    def test_get_unknown_plugin_fails(
        self,
        registry: FlextPluginPlatform.PluginRegistry,
    ) -> None:
        """get() for an unregistered name returns a failure result."""
        result = registry.get("nonexistent-plugin")
        assert result.failure

    def test_unregister_removes_plugin_from_listing(
        self,
        registry: FlextPluginPlatform.PluginRegistry,
        plugin: FlextPluginPlatform.Plugin,
    ) -> None:
        """unregister() drops a registered plugin from the listing."""
        registry.register(plugin.name, plugin)
        assert plugin.name in registry.list_plugins().value

        result = registry.unregister(plugin.name)
        assert result.success
        assert result.value is True
        assert plugin.name not in registry.list_plugins().value

    def test_unregister_unknown_plugin_fails(
        self,
        registry: FlextPluginPlatform.PluginRegistry,
    ) -> None:
        """unregister() for a name never registered returns a failure."""
        result = registry.unregister("nonexistent-plugin")
        assert result.failure

    def test_register_multiple_plugins_all_listed(
        self,
        registry: FlextPluginPlatform.PluginRegistry,
    ) -> None:
        """Every registered plugin is reflected in the listing."""
        plugins = [self._make_plugin(name=f"plugin-{i}") for i in range(3)]
        for candidate in plugins:
            assert registry.register(candidate.name, candidate).success

        plugins_result = registry.list_plugins()
        assert plugins_result.success
        listed = plugins_result.value
        assert len(listed) == 3
        for candidate in plugins:
            assert candidate.name in listed


__all__: list[str] = ["TestsFlextPluginPlugin"]
