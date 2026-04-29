"""Comprehensive test suite for flext_plugin.domain.entities module.

This test module provides comprehensive validation of domain entity behavior,
business rules, and integration patterns following enterprise testing standards.
Tests cover entity lifecycle, validation rules, business logic enforcement,
and integration scenarios across all domain entities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import math

from tests import c, m


class TestsFlextPluginDomainEntities:
    """Test suite for FlextPlugin domain entity.

    Tests Plugin entity including creation, validation, business rules,
    enable/disable lifecycle, and execution/error tracking.
    """

    def test_plugin_instance_creation(self) -> None:
        """Test creating FlextPlugin entity with factory method."""
        plugin = m.Plugin.Entity.create(
            name="test-plugin",
            plugin_version="1.0.0",
            entity_id="test-id",
            description="Test plugin",
            author="Test Author",
        )
        assert plugin.unique_id == "test-id"
        assert plugin.name == "test-plugin"
        assert plugin.plugin_version == "1.0.0"
        assert plugin.description == "Test plugin"
        assert plugin.author == "Test Author"
        assert plugin.is_enabled is True

    def test_plugin_enable_disable(self) -> None:
        """Test plugin enable and disable methods."""
        plugin = m.Plugin.Entity.create(
            name="test-plugin",
            plugin_version="1.0.0",
            entity_id="test-id",
            description="Test plugin",
            author="Test Author",
        )
        assert plugin.is_enabled is True
        result = plugin.disable()
        assert result.success
        is_enabled_after_disable = bool(plugin.is_enabled)
        assert not is_enabled_after_disable
        result = plugin.enable()
        assert result.success
        result = plugin.enable()
        assert result.failure

    def test_plugin_execution_recording(self) -> None:
        """Test recording plugin execution metrics in metadata."""
        plugin = m.Plugin.Entity.create(
            name="test-plugin",
            plugin_version="1.0.0",
            entity_id="test-id",
            description="Test plugin",
            author="Test Author",
        )
        plugin.record_execution(150.5, success=True)
        assert plugin.metadata["execution_count"] == 1
        exec_time_1 = plugin.metadata["total_execution_time"]
        assert isinstance(exec_time_1, float) and math.isclose(exec_time_1, 150.5)
        assert plugin.metadata["success_count"] == 1
        assert plugin.metadata["failure_count"] == 0
        plugin.record_execution(200.0, success=True)
        assert plugin.metadata["execution_count"] == 2
        exec_time_2 = plugin.metadata["total_execution_time"]
        assert isinstance(exec_time_2, float) and math.isclose(exec_time_2, 350.5)
        assert plugin.metadata["success_count"] == 2
        plugin.record_execution(50.0, success=False)
        assert plugin.metadata["execution_count"] == 3
        assert plugin.metadata["failure_count"] == 1

    def test_plugin_error_recording(self) -> None:
        """Test recording plugin errors in metadata."""
        plugin = m.Plugin.Entity.create(
            name="test-plugin",
            plugin_version="1.0.0",
            entity_id="test-id",
            description="Test plugin",
            author="Test Author",
        )
        plugin.record_error("Test error message")
        assert plugin.metadata["error_count"] == 1
        assert plugin.metadata["last_error"] == "Test error message"
        plugin.record_error("Second error")
        assert plugin.metadata["error_count"] == 2
        assert plugin.metadata["last_error"] == "Second error"

    def test_plugin_business_rules_validation(self) -> None:
        """Test plugin business rules validation."""
        plugin = m.Plugin.Entity.create(
            name="valid-plugin",
            plugin_version="1.0.0",
            entity_id="test-id",
            description="Valid plugin",
            author="Test Author",
        )
        result = plugin.validate_business_rules()
        assert result.success

    """Test FlextPluginModels.Config entity functionality."""

    def test_configuration_creation(self) -> None:
        """Test creating FlextPluginModels.Config."""
        settings = m.Plugin.PluginConfig(
            plugin_name="test-plugin",
            config={"enabled": True, "key": "value"},
        )
        assert settings.plugin_name == "test-plugin"
        assert settings.config["enabled"] is True
        assert settings.config["key"] == "value"

    def test_metadata_creation(self) -> None:
        """Test creating m.Plugin.PluginMetadata."""
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

    def test_metadata_defaults(self) -> None:
        """Test PluginMetadata default values."""
        metadata = m.Plugin.PluginMetadata(
            name="minimal-plugin",
            version="1.0.0",
            entry_point="minimal.entry:main",
            description="",
            author="Unknown",
            plugin_type="extension",
        )
        assert metadata.name == "minimal-plugin"
        assert metadata.version == "1.0.0"
        assert metadata.description == ""
        assert metadata.dependencies == ()
        assert dict(metadata.metadata) == {}

    def test_metadata_with_all_fields(self) -> None:
        """Test PluginMetadata with all fields."""
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
        assert metadata.name == "full-plugin"
        assert metadata.version == "2.0.0"
        assert metadata.author == "Test Author"
        assert metadata.plugin_type == "extension"
        assert len(metadata.dependencies) == 2
        assert metadata.metadata["key"] == "value"
