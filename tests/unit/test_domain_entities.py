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

from tests.constants import c
from tests.models import m


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

        assert plugin.unique_id == "test-id"
        assert plugin.name == "test-plugin"
        assert plugin.plugin_version == "1.0.0"
        assert plugin.description == "Test plugin"
        assert plugin.author == "Test Author"

    def test_create_defaults_plugin_to_enabled_with_empty_metadata(self) -> None:
        """A freshly created plugin is enabled and carries no metrics yet."""
        plugin = self._make_plugin()

        assert plugin.is_enabled is True
        assert dict(plugin.metadata) == {}

    def test_create_applies_declared_field_defaults(self) -> None:
        """Optional fields fall back to their declared defaults."""
        plugin = m.Plugin.Entity.create(name="minimal-plugin", entity_id="min-id")

        assert plugin.plugin_version == "1.0.0"
        assert plugin.description == ""
        assert plugin.author == ""
        assert plugin.plugin_type == c.Plugin.Type.UTILITY

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

        result = plugin.disable()

        assert result.success
        assert result.unwrap() is True
        assert plugin.is_enabled is False

    def test_disable_is_rejected_when_already_disabled(self) -> None:
        """A second disable() fails with an explanatory error, state unchanged."""
        plugin = self._make_plugin()
        plugin.disable()

        result = plugin.disable()

        assert result.failure
        assert result.error is not None
        assert "already disabled" in result.error
        assert plugin.is_enabled is False

    def test_enable_restores_a_disabled_plugin(self) -> None:
        """enable() re-activates a disabled plugin."""
        plugin = self._make_plugin()
        plugin.disable()

        result = plugin.enable()

        assert result.success
        assert plugin.is_enabled is True

    def test_enable_is_rejected_when_already_enabled(self) -> None:
        """enable() on an already-enabled plugin fails idempotently."""
        plugin = self._make_plugin()

        result = plugin.enable()

        assert result.failure
        assert result.error is not None
        assert "already enabled" in result.error
        assert plugin.is_enabled is True

    def test_enable_disable_round_trip_returns_to_enabled(self) -> None:
        """Disable then enable is a no-net-change round trip on public state."""
        plugin = self._make_plugin()

        assert plugin.disable().success
        assert plugin.enable().success
        assert plugin.is_enabled is True

    # ------------------------------------------------------------------ #
    # Execution metric accumulation (public metadata state)
    # ------------------------------------------------------------------ #

    def test_record_execution_accumulates_counts_and_time(self) -> None:
        """Successive successful executions accumulate count, time, successes."""
        plugin = self._make_plugin()

        plugin.record_execution(150.5, success=True)

        assert plugin.metadata["execution_count"] == 1
        assert plugin.metadata["success_count"] == 1
        assert plugin.metadata["failure_count"] == 0
        first_total = plugin.metadata["total_execution_time"]
        assert isinstance(first_total, float)
        assert math.isclose(first_total, 150.5)

        plugin.record_execution(200.0, success=True)

        assert plugin.metadata["execution_count"] == 2
        assert plugin.metadata["success_count"] == 2
        second_total = plugin.metadata["total_execution_time"]
        assert isinstance(second_total, float)
        assert math.isclose(second_total, 350.5)

    def test_record_execution_tracks_failures_separately(self) -> None:
        """A failed execution increments the failure count, not the success count."""
        plugin = self._make_plugin()
        plugin.record_execution(150.5, success=True)

        plugin.record_execution(50.0, success=False)

        assert plugin.metadata["execution_count"] == 2
        assert plugin.metadata["success_count"] == 1
        assert plugin.metadata["failure_count"] == 1
        total = plugin.metadata["total_execution_time"]
        assert isinstance(total, float)
        assert math.isclose(total, 200.5)

    def test_record_error_accumulates_count_and_keeps_last_message(self) -> None:
        """record_error() counts errors and surfaces the most recent message."""
        plugin = self._make_plugin()

        plugin.record_error("Test error message")

        assert plugin.metadata["error_count"] == 1
        assert plugin.metadata["last_error"] == "Test error message"

        plugin.record_error("Second error")

        assert plugin.metadata["error_count"] == 2
        assert plugin.metadata["last_error"] == "Second error"

    # ------------------------------------------------------------------ #
    # Business-rule validation
    # ------------------------------------------------------------------ #

    def test_validate_business_rules_accepts_a_well_formed_plugin(self) -> None:
        """A validly-constructed plugin passes its business-rule check."""
        plugin = self._make_plugin(name="valid-plugin", description="Valid plugin")

        result = plugin.validate_business_rules()

        assert result.success
        assert result.unwrap() is True

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

        assert metadata.name == "test-plugin"
        assert metadata.version == "1.0.0"
        assert metadata.entry_point == "test.entry:main"
        assert metadata.plugin_type == c.Plugin.Type.TAP.value
        assert metadata.description == "Test extractor plugin"
        assert "requests" in metadata.dependencies
        assert "pydantic" in metadata.dependencies

    def test_metadata_value_object_applies_declared_defaults(self) -> None:
        """Omitted optional PluginMetadata fields take their declared defaults."""
        metadata = m.Plugin.PluginMetadata(
            name="minimal-plugin",
            version="1.0.0",
            entry_point="minimal.entry:main",
        )

        assert metadata.description == ""
        assert metadata.author == "Unknown"
        assert metadata.plugin_type == "extension"
        assert metadata.dependencies == ()
        assert dict(metadata.metadata) == {}

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

        assert metadata.author == "Test Author"
        assert metadata.plugin_type == "extension"
        assert len(metadata.dependencies) == 2
        assert metadata.metadata["key"] == "value"


__all__: list[str] = ["TestsFlextPluginDomainEntities"]
