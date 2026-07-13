"""Behavioral test suite for flext_plugin domain entities.

Exercises the OBSERVABLE PUBLIC CONTRACT of FlextPluginModels.Plugin entities:
factory construction, enable/disable lifecycle (r[bool] outcomes and
idempotence), execution/error metric accumulation via public state, business
rule validation, and immutable value-object construction. No private attribute
access, no internal-collaborator spying, no line-coverage pokes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import math

import pytest
from flext_tests import tm

from flext_plugin import u
from tests import c, m


class TestsFlextPluginDomainEntities:
    """Behavioral contract tests for FlextPlugin domain entities.

    Asserts return values, r[bool] success/failure outcomes and error
    messages, public model state (fields, metadata), invariants, idempotence,
    and error paths through the public API only.
    """

    @staticmethod
    def _make_plugin(
        *,
        name: str = "test-plugin",
        plugin_version: str = "1.0.0",
        entity_id: str = "test-id",
        description: str = "Test plugin",
        author: str = "Test Author",
    ) -> m.Plugin.Entity:
        """Construct a Plugin entity through the public factory."""
        return m.Plugin.Entity.create(
            name=name,
            plugin_version=plugin_version,
            entity_id=entity_id,
            description=description,
            author=author,
        )

    # ------------------------------------------------------------------ #
    # Factory construction contract
    # ------------------------------------------------------------------ #

    def test_create_maps_entity_id_to_unique_id_and_sets_fields(self) -> None:
        """create() exposes the supplied identity and descriptive fields."""
        plugin = self._make_plugin()

        tm.that(plugin.unique_id, eq="test-id")
        tm.that(plugin.name, eq="test-plugin")
        tm.that(plugin.plugin_version, eq="1.0.0")
        tm.that(plugin.description, eq="Test plugin")
        tm.that(plugin.author, eq="Test Author")

    def test_create_defaults_plugin_to_enabled_with_empty_metadata(self) -> None:
        """A freshly created plugin is enabled and carries no metrics yet."""
        plugin = self._make_plugin()

        tm.that(plugin.is_enabled, eq=True)
        tm.that(dict(plugin.metadata), eq={})

    def test_create_applies_declared_field_defaults(self) -> None:
        """Optional fields fall back to their declared defaults."""
        plugin = m.Plugin.Entity.create(name="minimal-plugin", entity_id="min-id")

        tm.that(plugin.plugin_version, eq="1.0.0")
        tm.that(plugin.description, eq="")
        tm.that(plugin.author, eq="")
        tm.that(plugin.plugin_type, eq=c.Plugin.Type.UTILITY)

    @pytest.mark.parametrize(
        "bad_name",
        ["ab", "-bad", "1bad", ""],
    )
    def test_create_rejects_names_violating_contract(self, bad_name: str) -> None:
        """Names shorter than the minimum or breaking the pattern are refused."""
        with pytest.raises(ValueError, match=r".+"):
            m.Plugin.Entity.create(name=bad_name, entity_id="id")

    @pytest.mark.parametrize(
        "bad_version",
        ["1", "1.2.3.4", "x.y.z", "abc"],
    )
    def test_create_rejects_non_semantic_versions(self, bad_version: str) -> None:
        """Versions outside the X.Y.Z shape are rejected at construction."""
        with pytest.raises(ValueError, match=r"semantic|version|pattern|string"):
            m.Plugin.Entity.create(
                name="valid-plugin",
                plugin_version=bad_version,
                entity_id="id",
            )

    # ------------------------------------------------------------------ #
    # Enable / disable lifecycle
    # ------------------------------------------------------------------ #

    def test_disable_transitions_enabled_plugin_to_disabled(self) -> None:
        """disable() succeeds once and flips the public enabled state."""
        plugin = self._make_plugin()

        result = u.Plugin.Platform.Rules.disable(plugin)

        tm.ok(result)
        tm.that(result.unwrap().is_enabled, eq=False)

    def test_disable_is_rejected_when_already_disabled(self) -> None:
        """A second disable() fails with an explanatory error, state unchanged."""
        plugin = self._make_plugin()
        disabled = u.Plugin.Platform.Rules.disable(plugin).unwrap()

        result = u.Plugin.Platform.Rules.disable(disabled)

        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(result.error, has="already disabled")
        tm.that(disabled.is_enabled, eq=False)

    def test_enable_restores_a_disabled_plugin(self) -> None:
        """enable() re-activates a disabled plugin."""
        plugin = self._make_plugin()
        disabled = u.Plugin.Platform.Rules.disable(plugin).unwrap()

        result = u.Plugin.Platform.Rules.enable(disabled)

        tm.ok(result)
        tm.that(result.unwrap().is_enabled, eq=True)

    def test_enable_is_rejected_when_already_enabled(self) -> None:
        """enable() on an already-enabled plugin fails idempotently."""
        plugin = self._make_plugin()

        result = u.Plugin.Platform.Rules.enable(plugin)

        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(result.error, has="already enabled")
        tm.that(plugin.is_enabled, eq=True)

    def test_enable_disable_round_trip_returns_to_enabled(self) -> None:
        """Disable then enable is a no-net-change round trip on public state."""
        plugin = self._make_plugin()

        disabled = u.Plugin.Platform.Rules.disable(plugin).unwrap()
        enabled = u.Plugin.Platform.Rules.enable(disabled).unwrap()
        tm.that(enabled.is_enabled, eq=True)

    # ------------------------------------------------------------------ #
    # Execution metric accumulation (public metadata state)
    # ------------------------------------------------------------------ #

    def test_record_execution_accumulates_counts_and_time(self) -> None:
        """Successive successful executions accumulate count, time, successes."""
        plugin = self._make_plugin()

        recorded = u.Plugin.Platform.Rules.record_execution(
            plugin,
            150.5,
            success=True,
        )

        tm.that(recorded.metadata["execution_count"], eq=1)
        tm.that(recorded.metadata["success_count"], eq=1)
        tm.that(recorded.metadata["failure_count"], eq=0)
        first_total = recorded.metadata["total_execution_time"]
        tm.that(first_total, is_=float)
        assert math.isclose(first_total, 150.5)

        recorded = u.Plugin.Platform.Rules.record_execution(
            recorded,
            200.0,
            success=True,
        )

        tm.that(recorded.metadata["execution_count"], eq=2)
        tm.that(recorded.metadata["success_count"], eq=2)
        second_total = recorded.metadata["total_execution_time"]
        tm.that(second_total, is_=float)
        assert math.isclose(second_total, 350.5)

    def test_record_execution_tracks_failures_separately(self) -> None:
        """A failed execution increments the failure count, not the success count."""
        plugin = self._make_plugin()
        recorded = u.Plugin.Platform.Rules.record_execution(
            plugin,
            150.5,
            success=True,
        )

        recorded = u.Plugin.Platform.Rules.record_execution(
            recorded,
            50.0,
            success=False,
        )

        tm.that(recorded.metadata["execution_count"], eq=2)
        tm.that(recorded.metadata["success_count"], eq=1)
        tm.that(recorded.metadata["failure_count"], eq=1)
        total = recorded.metadata["total_execution_time"]
        tm.that(total, is_=float)
        assert math.isclose(total, 200.5)

    def test_record_error_accumulates_count_and_keeps_last_message(self) -> None:
        """record_error() counts errors and surfaces the most recent message."""
        plugin = self._make_plugin()

        recorded = u.Plugin.Platform.Rules.record_error(plugin, "Test error message")

        tm.that(recorded.metadata["error_count"], eq=1)
        tm.that(recorded.metadata["last_error"], eq="Test error message")

        recorded = u.Plugin.Platform.Rules.record_error(recorded, "Second error")

        tm.that(recorded.metadata["error_count"], eq=2)
        tm.that(recorded.metadata["last_error"], eq="Second error")

    # ------------------------------------------------------------------ #
    # Business-rule validation
    # ------------------------------------------------------------------ #

    def test_validate_business_rules_accepts_a_well_formed_plugin(self) -> None:
        """A validly-constructed plugin passes its business-rule check."""
        plugin = self._make_plugin(name="valid-plugin", description="Valid plugin")

        result = u.Plugin.Platform.Rules.validate_business_rules(plugin)

        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    # ------------------------------------------------------------------ #
    # PluginMetadata value object
    # ------------------------------------------------------------------ #

    def test_metadata_value_object_preserves_all_supplied_fields(self) -> None:
        """PluginMetadata round-trips the fields it is constructed with."""
        metadata = m.Plugin.PluginMetadata(
            name="test-plugin",
            version="1.0.0",
            entry_point="test.entry:main",
            plugin_type=c.Plugin.Type.TAP.value,
            description="Test extractor plugin",
            author="test-author",
            dependencies=["requests", "pydantic"],
        )

        tm.that(metadata.name, eq="test-plugin")
        tm.that(metadata.version, eq="1.0.0")
        tm.that(metadata.entry_point, eq="test.entry:main")
        tm.that(metadata.plugin_type, eq=c.Plugin.Type.TAP.value)
        tm.that(metadata.description, eq="Test extractor plugin")
        tm.that(metadata.dependencies, has="requests")
        tm.that(metadata.dependencies, has="pydantic")

    def test_metadata_value_object_applies_declared_defaults(self) -> None:
        """Omitted optional PluginMetadata fields take their declared defaults."""
        metadata = m.Plugin.PluginMetadata(
            name="minimal-plugin",
            version="1.0.0",
            entry_point="minimal.entry:main",
        )

        tm.that(metadata.description, eq="")
        tm.that(metadata.author, eq="Unknown")
        tm.that(metadata.plugin_type, eq="extension")
        tm.that(metadata.dependencies, eq=())
        tm.that(dict(metadata.metadata), eq={})

    def test_metadata_value_object_carries_all_optional_fields(self) -> None:
        """PluginMetadata retains explicitly supplied optional fields."""
        metadata = m.Plugin.PluginMetadata(
            name="full-plugin",
            version="2.0.0",
            entry_point="full.entry:main",
            description="A full plugin",
            author="Test Author",
            plugin_type="extension",
            dependencies=["dep1", "dep2"],
            metadata={"key": "value"},
        )

        tm.that(metadata.author, eq="Test Author")
        tm.that(metadata.plugin_type, eq="extension")
        tm.that(len(metadata.dependencies), eq=2)
        tm.that(metadata.metadata["key"], eq="value")


__all__: list[str] = ["TestsFlextPluginDomainEntities"]
