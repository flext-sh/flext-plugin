"""Comprehensive test suite for flext_plugin.domain.entities module.

This test module provides comprehensive validation of domain entity behavior,
business rules, and integration patterns following enterprise testing standards.
Tests cover entity lifecycle, validation rules, business logic enforcement,
and integration scenarios across all domain entities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_plugin import FlextPluginConstants, FlextPluginModels
from tests import t


class TestFlextPlugin:
    """Test suite for FlextPlugin domain entity.

    Tests Plugin entity including creation, validation, business rules,
    enable/disable lifecycle, and execution/error tracking.
    """

    def test_plugin_instance_creation(self) -> None:
        """Test creating FlextPlugin entity with factory method."""
        plugin = FlextPluginModels.Plugin.Plugin.create(
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
        plugin = FlextPluginModels.Plugin.Plugin.create(
            name="test-plugin",
            plugin_version="1.0.0",
            entity_id="test-id",
            description="Test plugin",
            author="Test Author",
        )
        assert plugin.is_enabled is True
        result = plugin.disable()
        assert result.is_success
        assert not plugin.is_enabled
        result = plugin.enable()
        assert result.is_success
        assert plugin.is_enabled is True
        result = plugin.enable()
        assert result.is_failure

    def test_plugin_execution_recording(self) -> None:
        """Test recording plugin execution metrics in metadata."""
        plugin = FlextPluginModels.Plugin.Plugin.create(
            name="test-plugin",
            plugin_version="1.0.0",
            entity_id="test-id",
            description="Test plugin",
            author="Test Author",
        )
        plugin.record_execution(150.5, success=True)
        assert plugin.metadata["execution_count"] == 1
        assert plugin.metadata["total_execution_time"] == pytest.approx(150.5)
        assert plugin.metadata["success_count"] == 1
        assert plugin.metadata["failure_count"] == 0
        plugin.record_execution(200.0, success=True)
        assert plugin.metadata["execution_count"] == 2
        assert plugin.metadata["total_execution_time"] == pytest.approx(350.5)
        assert plugin.metadata["success_count"] == 2
        plugin.record_execution(50.0, success=False)
        assert plugin.metadata["execution_count"] == 3
        assert plugin.metadata["failure_count"] == 1

    def test_plugin_error_recording(self) -> None:
        """Test recording plugin errors in metadata."""
        plugin = FlextPluginModels.Plugin.Plugin.create(
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
        plugin = FlextPluginModels.Plugin.Plugin.create(
            name="valid-plugin",
            plugin_version="1.0.0",
            entity_id="test-id",
            description="Valid plugin",
            author="Test Author",
        )
        result = plugin.validate_business_rules()
        assert result.is_success


class TestFlextPluginSettings:
    """Test FlextPluginModels.Config entity functionality."""

    def test_configuration_creation(self) -> None:
        """Test creating FlextPluginModels.Config."""
        config = FlextPluginModels.Plugin.PluginConfig(
            plugin_name="test-plugin", settings={"enabled": True, "key": "value"}
        )
        assert config.plugin_name == "test-plugin"
        assert config.settings["enabled"] is True
        assert config.settings["key"] == "value"

    def test_configuration_defaults(self) -> None:
        """Test FlextPluginModels.Config default values."""
        config = FlextPluginModels.Plugin.PluginConfig(plugin_name="test-plugin")
        assert config.plugin_name == "test-plugin"
        assert config.settings == {}

    def test_configuration_with_complex_settings(self) -> None:
        """Test configuration with complex settings."""
        settings: dict[str, t.NormalizedValue] = {
            "max_memory_mb": 800,
            "max_cpu_percent": 75,
            "timeout_seconds": 300,
            "nested": {"deep": "value"},
        }
        config = FlextPluginModels.Plugin.PluginConfig(
            plugin_name="test-plugin", settings=settings
        )
        assert config.settings["max_memory_mb"] == 800
        assert config.settings["max_cpu_percent"] == 75
        assert config.settings["timeout_seconds"] == 300


class TestFlextPluginExecution:
    """Test FlextPluginModels.Plugin.ExecutionResult entity functionality."""

    def test_execution_result_success(self) -> None:
        """Test creating successful ExecutionResult."""
        result = FlextPluginModels.Plugin.ExecutionResult(
            success=True, data={"output": "test data"}, execution_time_ms=150.5
        )
        assert result.success is True
        assert result.data == {"output": "test data"}
        assert result.error == ""
        assert result.execution_time_ms == pytest.approx(150.5)

    def test_execution_result_failure(self) -> None:
        """Test creating failed ExecutionResult."""
        result = FlextPluginModels.Plugin.ExecutionResult(
            success=False, error="Plugin execution failed", execution_time_ms=50.0
        )
        assert result.success is False
        assert result.error == "Plugin execution failed"
        assert result.data == {}
        assert result.execution_time_ms == pytest.approx(50.0)

    def test_execution_result_defaults(self) -> None:
        """Test ExecutionResult default values."""
        result = FlextPluginModels.Plugin.ExecutionResult(success=True)
        assert result.success is True
        assert result.data == {}
        assert result.error == ""
        assert result.execution_time_ms == pytest.approx(0.0)

    def test_execution_result_with_complex_data(self) -> None:
        """Test ExecutionResult with complex output data."""
        complex_data: dict[str, t.NormalizedValue] = {
            "records": [1, 2, 3],
            "metadata": {"count": 3, "type": "test"},
        }
        result = FlextPluginModels.Plugin.ExecutionResult(
            success=True, data=complex_data, execution_time_ms=100.0
        )
        assert result.success is True
        assert result.data == complex_data
        assert result.execution_time_ms == pytest.approx(100.0)


class TestFlextPluginRegistryEntity:
    """Test FlextPluginModels.Plugin.Registry domain entity functionality."""

    def test_registry_creation(self) -> None:
        """Test creating FlextPluginModels.Plugin.Registry entity."""
        registry = FlextPluginModels.Plugin.Registry()
        assert registry.plugins == {}
        assert registry.last_updated is not None
        assert registry.created_at is not None

    def test_registry_with_plugins(self) -> None:
        """Test registry with plugins."""
        plugins: dict[str, t.NormalizedValue] = {
            "plugin1": {"name": "test-plugin-1"},
            "plugin2": {"name": "test-plugin-2"},
        }
        registry = FlextPluginModels.Plugin.Registry(plugins=plugins)
        assert len(registry.plugins) == 2
        assert "plugin1" in registry.plugins
        assert "plugin2" in registry.plugins

    def test_registry_timestamps(self) -> None:
        """Test registry timestamps."""
        registry = FlextPluginModels.Plugin.Registry()
        assert registry.last_updated is not None
        assert registry.created_at is not None


class TestFlextPluginMetadata:
    """Test FlextPluginModels.Plugin.PluginMetadata functionality."""

    def test_metadata_creation(self) -> None:
        """Test creating FlextPluginModels.Plugin.PluginMetadata."""
        metadata = FlextPluginModels.Plugin.PluginMetadata(
            name="test-plugin",
            version="1.0.0",
            entry_point="test.entry:main",
            plugin_type=FlextPluginConstants.Plugin.PluginType.TAP.value,
            description="Test extractor plugin",
            dependencies=["requests", "pydantic"],
        )
        assert metadata.name == "test-plugin"
        assert metadata.version == "1.0.0"
        assert metadata.entry_point == "test.entry:main"
        assert metadata.plugin_type == FlextPluginConstants.Plugin.PluginType.TAP.value
        assert metadata.description == "Test extractor plugin"
        assert "requests" in metadata.dependencies
        assert "pydantic" in metadata.dependencies

    def test_metadata_defaults(self) -> None:
        """Test PluginMetadata default values."""
        metadata = FlextPluginModels.Plugin.PluginMetadata(
            name="minimal-plugin", version="1.0.0", entry_point="minimal.entry:main"
        )
        assert metadata.name == "minimal-plugin"
        assert metadata.version == "1.0.0"
        assert metadata.description == ""
        assert metadata.dependencies == []
        assert metadata.metadata == {}

    def test_metadata_with_all_fields(self) -> None:
        """Test PluginMetadata with all fields."""
        metadata = FlextPluginModels.Plugin.PluginMetadata(
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
