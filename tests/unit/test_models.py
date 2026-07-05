"""Behavioral unit tests for FlextPluginModels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from tests.constants import c
from tests.models import m


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
        assert status.value == expected_value
        assert str(status) == expected_value

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
        assert status in c.Plugin.PluginStatus.get_operational_statuses()
        assert status.is_operational() is True
        assert status.is_error_state() is False

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
        assert status in c.Plugin.PluginStatus.get_error_statuses()
        assert status.is_error_state() is True
        assert status.is_operational() is False

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
        assert plugin_type.value == expected_value

    # ---- Entity construction & validation -------------------------------

    def test_entity_exposes_constructor_state_via_public_fields(self) -> None:
        """A constructed entity reflects supplied values through its public API."""
        plugin = m.Plugin.Entity(
            name="test-plugin",
            plugin_version="1.2.3",
            plugin_type=c.Plugin.Type.UTILITY,
            is_enabled=True,
        )
        assert plugin.name == "test-plugin"
        assert plugin.plugin_version == "1.2.3"
        assert plugin.plugin_type is c.Plugin.Type.UTILITY
        assert plugin.is_enabled is True

    def test_entity_applies_documented_field_defaults(self) -> None:
        """Optional fields fall back to their documented defaults."""
        plugin = m.Plugin.Entity(name="defaults-plugin")
        assert plugin.plugin_version == "1.0.0"
        assert plugin.description == ""
        assert plugin.author == ""
        assert plugin.plugin_type is c.Plugin.Type.UTILITY
        assert plugin.is_enabled is True
        assert dict(plugin.metadata) == {}

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
        assert plugin.plugin_version == good_version

    # ---- Lifecycle behavior (r[T] contract) -----------------------------

    def test_disable_transitions_enabled_plugin_and_reports_success(self) -> None:
        """Disabling an enabled plugin succeeds and flips public state."""
        plugin = m.Plugin.Entity(name="lifecycle", is_enabled=True)
        result = plugin.disable()
        assert result.success
        assert result.unwrap() is True
        assert plugin.is_enabled is False

    def test_disable_is_rejected_when_already_disabled(self) -> None:
        """Disabling an already-disabled plugin is a failure, state unchanged."""
        plugin = m.Plugin.Entity(name="lifecycle", is_enabled=False)
        result = plugin.disable()
        assert result.failure
        assert "already disabled" in (result.error or "")
        assert plugin.is_enabled is False

    def test_enable_transitions_disabled_plugin_and_reports_success(self) -> None:
        """Enabling a disabled plugin succeeds and flips public state."""
        plugin = m.Plugin.Entity(name="lifecycle", is_enabled=False)
        result = plugin.enable()
        assert result.success
        assert result.unwrap() is True
        assert plugin.is_enabled is True

    def test_enable_is_rejected_when_already_enabled(self) -> None:
        """Enabling an already-enabled plugin is a failure, state unchanged."""
        plugin = m.Plugin.Entity(name="lifecycle", is_enabled=True)
        result = plugin.enable()
        assert result.failure
        assert "already enabled" in (result.error or "")
        assert plugin.is_enabled is True

    def test_disable_then_enable_round_trips_to_enabled(self) -> None:
        """A disable/enable cycle returns the plugin to enabled state."""
        plugin = m.Plugin.Entity(name="cycle", is_enabled=True)
        assert plugin.disable().success
        assert plugin.enable().success
        assert plugin.is_enabled is True

    # ---- Metrics recording (observable via metadata) --------------------

    def test_record_error_accumulates_error_metadata(self) -> None:
        """Recording errors increments the count and stores the last message."""
        plugin = m.Plugin.Entity(name="err-plugin")
        plugin.record_error("boom")
        plugin.record_error("kaboom")
        assert plugin.metadata["error_count"] == 2
        assert plugin.metadata["last_error"] == "kaboom"

    def test_record_execution_accumulates_success_and_timing(self) -> None:
        """Successful executions increment counts and total execution time."""
        plugin = m.Plugin.Entity(name="exec-plugin")
        plugin.record_execution(1.5, success=True)
        plugin.record_execution(2.5, success=True)
        assert plugin.metadata["execution_count"] == 2
        assert plugin.metadata["success_count"] == 2
        assert plugin.metadata["failure_count"] == 0
        assert plugin.metadata["total_execution_time"] == pytest.approx(4.0)

    def test_record_execution_tracks_failures_separately(self) -> None:
        """Failed executions increment the failure counter only."""
        plugin = m.Plugin.Entity(name="exec-plugin")
        plugin.record_execution(0.5, success=False)
        assert plugin.metadata["execution_count"] == 1
        assert plugin.metadata["failure_count"] == 1
        assert plugin.metadata["success_count"] == 0

    # ---- Business-rule validation (r[T] contract) -----------------------

    def test_validate_business_rules_passes_for_well_formed_entity(self) -> None:
        """A valid entity passes business-rule validation."""
        plugin = m.Plugin.Entity(name="valid", plugin_version="1.0.0")
        result = plugin.validate_business_rules()
        assert result.success
        assert result.unwrap() is True

    # ---- create() factory -----------------------------------------------

    def test_create_factory_builds_validated_entity(self) -> None:
        """The create factory yields a fully validated entity."""
        plugin = m.Plugin.Entity.create(
            name="factory-plugin",
            plugin_version="2.0.0",
            plugin_type=c.Plugin.Type.SERVICE,
        )
        assert plugin.name == "factory-plugin"
        assert plugin.plugin_version == "2.0.0"
        assert plugin.plugin_type is c.Plugin.Type.SERVICE

    # NOTE: m.Plugin.DiscoveryData is intentionally NOT tested here. Its `path`
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
        assert metadata.name == "meta-plugin"
        assert metadata.version == "1.0.0"
        assert metadata.entry_point == "meta_plugin:main"
        assert metadata.author == "Test Author"
        assert metadata.description == "Test plugin description"

    def test_plugin_metadata_applies_documented_defaults(self) -> None:
        """Optional metadata fields fall back to documented defaults."""
        metadata = m.Plugin.PluginMetadata(
            name="meta-plugin",
            version="1.0.0",
            entry_point="meta_plugin:main",
        )
        assert metadata.description == ""
        assert metadata.author == "Unknown"
        assert metadata.plugin_type == "extension"
        assert tuple(metadata.dependencies) == ()


__all__: list[str] = ["TestsFlextPluginModelsUnit"]
