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

from flext_tests import tm
from tests import m, u


@pytest.mark.usefixtures("reset_registry")
class TestsFlextPluginPlugin:
    """Behavioral tests for the Plugin entity and PluginRegistry contract."""

    @staticmethod
    def _make_plugin(
        *, name: str = "test-plugin", is_enabled: bool = True
    ) -> u.Plugin.Platform.Plugin:
        """Build a Plugin platform entity for registry-facing tests."""
        return u.Plugin.Platform.Plugin(
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
        tm.that(plugin.name, eq="test-plugin")
        tm.that(plugin.plugin_version, eq="1.0.0")

    def test_create_defaults_to_enabled(self) -> None:
        """A freshly created plugin defaults to the enabled state."""
        plugin = m.Plugin.Entity.create(name="test-plugin", plugin_version="1.0.0")
        tm.that(plugin.is_enabled, eq=True)

    def test_create_honors_explicit_disabled_state(self) -> None:
        """create() respects an explicit is_enabled=False argument."""
        plugin = m.Plugin.Entity.create(
            name="test-plugin", plugin_version="1.0.0", is_enabled=False
        )
        tm.that(plugin.is_enabled, eq=False)

    @pytest.mark.parametrize("bad_version", ["1", "1.2.3.4", "1.x", "abc"])
    def test_create_rejects_non_semantic_version(self, bad_version: str) -> None:
        """create() raises when the version is not semantic X.Y[.Z]."""
        with pytest.raises(ValueError, match="semantic"):
            m.Plugin.Entity.create(name="test-plugin", plugin_version=bad_version)

    # ----- Plugin entity: enable/disable lifecycle ------------------------

    def test_validate_business_rules_accepts_valid_plugin(self) -> None:
        """A well-formed plugin passes business-rule validation."""
        plugin = m.Plugin.Entity.create(name="test-plugin", plugin_version="1.0.0")
        result = u.Plugin.Platform.Rules.validate_business_rules(plugin)
        tm.ok(result)

    @pytest.mark.parametrize(
        ("is_enabled", "expected_status", "expected_active"),
        [(True, "active", True), (False, "inactive", False)],
    )
    def test_status_and_active_reflect_enabled_state(
        self, *, is_enabled: bool, expected_status: str, expected_active: bool
    ) -> None:
        """Status and active() derive directly from the enabled state."""
        plugin = self._make_plugin(is_enabled=is_enabled)
        tm.that(plugin.status, eq=expected_status)
        assert plugin.active() is expected_active

    # ----- Registry fixtures ----------------------------------------------

    @pytest.fixture
    def reset_registry(self) -> None:
        """Reset class-level registry storage before each test."""
        registry = u.Plugin.Platform.PluginRegistry.create()
        plugins_result = registry.list_plugins()
        if plugins_result.success:
            for plugin_name in plugins_result.value:
                _ = registry.unregister(plugin_name)

    @pytest.fixture
    def registry(self) -> u.Plugin.Platform.PluginRegistry:
        """Create a registry instance for testing."""
        return u.Plugin.Platform.PluginRegistry.create()

    @pytest.fixture
    def plugin(self) -> u.Plugin.Platform.Plugin:
        """Create a plugin for registry testing."""
        return self._make_plugin()

    # ----- Registry: lifecycle contract -----------------------------------

    def test_new_registry_lists_no_plugins(
        self, registry: u.Plugin.Platform.PluginRegistry
    ) -> None:
        """A cleared registry reports an empty plugin listing."""
        plugins_result = registry.list_plugins()
        tm.ok(plugins_result)
        assert not plugins_result.value

    def test_register_then_get_returns_same_plugin(
        self,
        registry: u.Plugin.Platform.PluginRegistry,
        plugin: u.Plugin.Platform.Plugin,
    ) -> None:
        """A registered plugin is retrievable by name via get()."""
        register_result = registry.register(plugin.name, plugin)
        tm.ok(register_result)
        tm.that(register_result.value, eq=True)

        get_result = registry.get(plugin.name)
        tm.ok(get_result)
        tm.that(get_result.value.name, eq=plugin.name)

    def test_registered_plugin_appears_in_listing(
        self,
        registry: u.Plugin.Platform.PluginRegistry,
        plugin: u.Plugin.Platform.Plugin,
    ) -> None:
        """A registered plugin's name is present in list_plugins()."""
        registry.register(plugin.name, plugin)
        plugins_result = registry.list_plugins()
        tm.ok(plugins_result)
        tm.that(plugins_result.value, has=plugin.name)

    def test_get_unknown_plugin_fails(
        self, registry: u.Plugin.Platform.PluginRegistry
    ) -> None:
        """get() for an unregistered name returns a failure result."""
        result = registry.get("nonexistent-plugin")
        tm.fail(result)

    def test_unregister_removes_plugin_from_listing(
        self,
        registry: u.Plugin.Platform.PluginRegistry,
        plugin: u.Plugin.Platform.Plugin,
    ) -> None:
        """unregister() drops a registered plugin from the listing."""
        registry.register(plugin.name, plugin)
        tm.that(registry.list_plugins().value, has=plugin.name)

        result = registry.unregister(plugin.name)
        tm.ok(result)
        tm.that(result.value, eq=True)
        tm.that(registry.list_plugins().value, lacks=plugin.name)

    def test_unregister_unknown_plugin_fails(
        self, registry: u.Plugin.Platform.PluginRegistry
    ) -> None:
        """unregister() for a name never registered returns a failure."""
        result = registry.unregister("nonexistent-plugin")
        tm.fail(result)

    def test_register_multiple_plugins_all_listed(
        self, registry: u.Plugin.Platform.PluginRegistry
    ) -> None:
        """Every registered plugin is reflected in the listing."""
        plugins = [self._make_plugin(name=f"plugin-{i}") for i in range(3)]
        for candidate in plugins:
            tm.ok(registry.register(candidate.name, candidate))

        plugins_result = registry.list_plugins()
        tm.ok(plugins_result)
        listed = plugins_result.value
        tm.that(len(listed), eq=3)
        for candidate in plugins:
            tm.that(listed, has=candidate.name)


__all__: list[str] = ["TestsFlextPluginPlugin"]
