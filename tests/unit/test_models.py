"""Behavioral unit tests for FlextPluginModels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_tests import tm

from tests import c, m, u


class TestsFlextPluginModelsUnit:
    """Behavioral contract tests for the plugin domain models."""

    # ---- Enum public contract -------------------------------------------

    @pytest.mark.parametrize(
        ("status", "expected_value"),
        [
            (c.Plugin.PluginStatus.UNKNOWN, "unknown"),
            (c.Plugin.PluginStatus.DISCOVERED, "discovered"),
            (c.Plugin.PluginStatus.LOADED, "loaded"),
            (c.Plugin.PluginStatus.ACTIVE, "active"),
            (c.Plugin.PluginStatus.INACTIVE, "inactive"),
            (c.Plugin.PluginStatus.LOADING, "loading"),
            (c.Plugin.PluginStatus.ERROR, "error"),
            (c.Plugin.PluginStatus.DISABLED, "disabled"),
            (c.Plugin.PluginStatus.HEALTHY, "healthy"),
            (c.Plugin.PluginStatus.UNHEALTHY, "unhealthy"),
        ],
    )
    def test_plugin_status_serialises_to_wire_value(
        self,
        status: c.Plugin.PluginStatus,
        expected_value: str,
    ) -> None:
        """Each status renders its documented lowercase wire string."""
        tm.that(status.value, eq=expected_value)
        tm.that(str(status), eq=expected_value)

    @pytest.mark.parametrize(
        "status",
        [
            c.Plugin.PluginStatus.ACTIVE,
            c.Plugin.PluginStatus.HEALTHY,
            c.Plugin.PluginStatus.LOADED,
        ],
    )
    def test_operational_statuses_classify_as_operational(
        self,
        status: c.Plugin.PluginStatus,
    ) -> None:
        """Operational statuses are reported operational and not error states."""
        tm.that(c.Plugin.PluginStatus.get_operational_statuses(), has=status)
        tm.that(status.is_operational(), eq=True)
        tm.that(status.is_error_state(), eq=False)

    @pytest.mark.parametrize(
        "status",
        [
            c.Plugin.PluginStatus.ERROR,
            c.Plugin.PluginStatus.UNHEALTHY,
            c.Plugin.PluginStatus.DISABLED,
        ],
    )
    def test_error_statuses_classify_as_error_state(
        self,
        status: c.Plugin.PluginStatus,
    ) -> None:
        """Error statuses report as error states and never as operational."""
        tm.that(c.Plugin.PluginStatus.get_error_statuses(), has=status)
        tm.that(status.is_error_state(), eq=True)
        tm.that(status.is_operational(), eq=False)

    @pytest.mark.parametrize(
        ("plugin_type", "expected_value"),
        [
            (c.Plugin.Type.TAP, "tap"),
            (c.Plugin.Type.TARGET, "target"),
            (c.Plugin.Type.TRANSFORM, "transform"),
            (c.Plugin.Type.EXTENSION, "extension"),
            (c.Plugin.Type.SERVICE, "service"),
            (c.Plugin.Type.MIDDLEWARE, "middleware"),
            (c.Plugin.Type.TRANSFORMER, "transformer"),
            (c.Plugin.Type.UTILITY, "utility"),
            (c.Plugin.Type.CORE, "core"),
        ],
    )
    def test_plugin_type_serialises_to_wire_value(
        self,
        plugin_type: c.Plugin.Type,
        expected_value: str,
    ) -> None:
        """Plugin type members render their documented wire strings."""
        tm.that(plugin_type.value, eq=expected_value)

    # ---- Entity construction & validation -------------------------------

    def test_entity_exposes_constructor_state_via_public_fields(self) -> None:
        """A constructed entity reflects supplied values through its public API."""
        plugin = m.Plugin.Entity(
            name="test-plugin",
            plugin_version="1.2.3",
            plugin_type=c.Plugin.Type.UTILITY,
            is_enabled=True,
        )
        tm.that(plugin.name, eq="test-plugin")
        tm.that(plugin.plugin_version, eq="1.2.3")
        assert plugin.plugin_type is c.Plugin.Type.UTILITY
        tm.that(plugin.is_enabled, eq=True)

    def test_entity_applies_documented_field_defaults(self) -> None:
        """Optional fields fall back to their documented defaults."""
        plugin = m.Plugin.Entity(name="defaults-plugin")
        tm.that(plugin.plugin_version, eq="1.0.0")
        tm.that(plugin.description, eq="")
        tm.that(plugin.author, eq="")
        assert plugin.plugin_type is c.Plugin.Type.UTILITY
        tm.that(plugin.is_enabled, eq=True)
        tm.that(dict(plugin.metadata), eq={})

    def test_entity_rejects_empty_name(self) -> None:
        """An empty name violates the name constraint and is refused."""
        with pytest.raises(ValueError, match=r".*"):
            m.Plugin.Entity(name="", plugin_version="1.0.0")

    @pytest.mark.parametrize(
        "bad_version",
        ["invalid-version", "1", "1.0.0.0", "a.b.c", "x.y"],
    )
    def test_entity_rejects_non_semantic_version(self, bad_version: str) -> None:
        """Versions outside the X.Y[.Z] numeric form are refused."""
        with pytest.raises(ValueError, match=r"semantic"):
            m.Plugin.Entity(name="test-plugin", plugin_version=bad_version)

    @pytest.mark.parametrize("good_version", ["1.0.0", "10.20.30", "2.3.4"])
    def test_entity_accepts_valid_semantic_versions(self, good_version: str) -> None:
        """Well-formed semantic versions are accepted verbatim."""
        plugin = m.Plugin.Entity(name="ok-plugin", plugin_version=good_version)
        tm.that(plugin.plugin_version, eq=good_version)

    # ---- Lifecycle behavior (r[T] contract) -----------------------------

    def test_validate_business_rules_passes_for_well_formed_entity(self) -> None:
        """A valid entity passes business-rule validation."""
        plugin = m.Plugin.Entity(name="valid", plugin_version="1.0.0")
        result = u.Plugin.Platform.Rules.validate_business_rules(plugin)
        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    # ---- create() factory -----------------------------------------------

    def test_create_factory_builds_validated_entity(self) -> None:
        """The create factory yields a fully validated entity."""
        plugin = m.Plugin.Entity.create(
            name="factory-plugin",
            plugin_version="2.0.0",
            plugin_type=c.Plugin.Type.SERVICE,
        )
        tm.that(plugin.name, eq="factory-plugin")
        tm.that(plugin.plugin_version, eq="2.0.0")
        assert plugin.plugin_type is c.Plugin.Type.SERVICE

    # NOTE: p.Plugin.DiscoveryData is intentionally NOT tested here. Its `path`
    # field annotation resolves to `Path`, which src/flext_plugin/models.py
    # imports only under `TYPE_CHECKING`, so the model is never fully defined at
    # runtime and every construction raises PydanticUserError
    # ("DiscoveryData is not fully defined; you should define Path"). The public
    # constructor contract is therefore unreachable through the model's public
    # API until that src forward-ref defect is fixed. Not stubbed, not faked.

    # ---- PluginMetadata value object ------------------------------------

    def test_plugin_metadata_exposes_public_state(self) -> None:
        """Plugin metadata reflects supplied values through public fields."""
        metadata = m.Plugin.PluginMetadata(
            name="meta-plugin",
            version="1.0.0",
            entry_point="meta_plugin:main",
            author="Test Author",
            description="Test plugin description",
            plugin_type="extension",
        )
        tm.that(metadata.name, eq="meta-plugin")
        tm.that(metadata.version, eq="1.0.0")
        tm.that(metadata.entry_point, eq="meta_plugin:main")
        tm.that(metadata.author, eq="Test Author")
        tm.that(metadata.description, eq="Test plugin description")

    def test_plugin_metadata_applies_documented_defaults(self) -> None:
        """Optional metadata fields fall back to documented defaults."""
        metadata = m.Plugin.PluginMetadata(
            name="meta-plugin",
            version="1.0.0",
            entry_point="meta_plugin:main",
        )
        tm.that(metadata.description, eq="")
        tm.that(metadata.author, eq="Unknown")
        tm.that(metadata.plugin_type, eq="extension")
        tm.that(tuple(metadata.dependencies), eq=())


__all__: list[str] = ["TestsFlextPluginModelsUnit"]
