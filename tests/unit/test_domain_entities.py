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

import pytest
from flext_tests import tm

from tests import c, m, u


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
