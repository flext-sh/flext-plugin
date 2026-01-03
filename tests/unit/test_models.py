"""Unit tests for FlextPluginModels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime

import pytest

from flext_plugin.constants import FlextPluginConstants
from flext_plugin.models import FlextPluginModels

# Alias for convenience
PluginType = FlextPluginConstants.Plugin.PluginType
PluginStatus = FlextPluginConstants.Plugin.PluginStatus


class TestFlextPluginModels:
    """Test cases for FlextPluginModels."""

    def test_models_initialization(self) -> None:
        """Test that models can be initialized."""
        models = FlextPluginModels()
        assert models is not None

    def test_plugin_status_enum(self) -> None:
        """Test PluginStatus enum values and methods."""
        # Test enum values
        assert PluginStatus.UNKNOWN == "unknown"
        assert PluginStatus.DISCOVERED == "discovered"
        assert PluginStatus.LOADED == "loaded"
        assert PluginStatus.ACTIVE == "active"
        assert PluginStatus.INACTIVE == "inactive"
        assert PluginStatus.LOADING == "loading"
        assert PluginStatus.ERROR == "error"
        assert PluginStatus.DISABLED == "disabled"
        assert PluginStatus.HEALTHY == "healthy"
        assert PluginStatus.UNHEALTHY == "unhealthy"

        # Test class methods
        operational_statuses = PluginStatus.get_operational_statuses()
        assert PluginStatus.ACTIVE in operational_statuses
        assert PluginStatus.HEALTHY in operational_statuses
        assert PluginStatus.LOADED in operational_statuses

        error_statuses = PluginStatus.get_error_statuses()
        assert PluginStatus.ERROR in error_statuses
        assert PluginStatus.UNHEALTHY in error_statuses
        assert PluginStatus.DISABLED in error_statuses

        # Test instance methods
        assert PluginStatus.ACTIVE.is_operational()
        assert not PluginStatus.ERROR.is_operational()
        assert PluginStatus.ERROR.is_error_state()
        assert not PluginStatus.ACTIVE.is_error_state()

    def test_plugin_type_enum(self) -> None:
        """Test PluginType enum values."""
        # Test ETL types
        assert PluginType.TAP == "tap"
        assert PluginType.TARGET == "target"
        assert PluginType.TRANSFORM == "transform"

        # Test architecture types
        assert PluginType.EXTENSION == "extension"
        assert PluginType.SERVICE == "service"
        assert PluginType.MIDDLEWARE == "middleware"
        assert PluginType.TRANSFORMER == "transformer"

        # Test integration types
        assert PluginType.API == "api"
        assert PluginType.DATABASE == "database"
        assert PluginType.NOTIFICATION == "notification"
        assert PluginType.AUTHENTICATION == "authentication"
        assert PluginType.AUTHORIZATION == "authorization"

        # Test utility types
        assert PluginType.UTILITY == "utility"
        assert PluginType.TOOL == "tool"
        assert PluginType.HANDLER == "handler"
        assert PluginType.PROCESSOR == "processor"

        # Test additional types
        assert PluginType.CORE == "core"
        assert PluginType.ADDON == "addon"
        assert PluginType.THEME == "theme"
        assert PluginType.LANGUAGE == "language"

    def test_plugin_model_creation(self) -> None:
        """Test Plugin model creation."""
        plugin = FlextPluginModels.Plugin(
            name="test-plugin",
            plugin_version="1.0.0",
            plugin_type=PluginType.UTILITY,
        )

        assert plugin.name == "test-plugin"
        assert plugin.plugin_version == "1.0.0"
        assert plugin.plugin_type == PluginType.UTILITY
        assert plugin.is_enabled is True

    def test_plugin_model_validation(self) -> None:
        """Test Plugin model validation rules."""
        # Test valid plugin
        plugin = FlextPluginModels.Plugin(
            name="valid-plugin",
            plugin_version="1.0.0",
            plugin_type=PluginType.UTILITY,
        )
        assert plugin.name == "valid-plugin"

        # Test invalid plugin name
        with pytest.raises(ValueError):
            FlextPluginModels.Plugin(
                name="",  # Empty name should fail
                plugin_version="1.0.0",
                plugin_type=PluginType.UTILITY,
            )

        # Test invalid version format
        with pytest.raises(ValueError):
            FlextPluginModels.Plugin(
                name="test-plugin",
                plugin_version="invalid-version",  # Invalid format
                plugin_type=PluginType.UTILITY,
            )

    def test_execution_result_creation(self) -> None:
        """Test ExecutionResult creation."""
        result = FlextPluginModels.ExecutionResult(
            success=True,
            data={"output": "result"},
            error="",
            execution_time_ms=1500.0,
        )

        assert result.is_success is True
        assert result.data == {"output": "result"}
        assert not result.error
        assert result.execution_time_ms == 1500.0

    def test_execution_result_failure(self) -> None:
        """Test ExecutionResult failure case."""
        result = FlextPluginModels.ExecutionResult(
            success=False,
            data={},
            error="Plugin execution failed",
            execution_time_ms=500.0,
        )

        assert result.is_success is False
        assert result.error == "Plugin execution failed"

    def test_discovery_data_creation(self) -> None:
        """Test DiscoveryData creation."""
        from pathlib import Path

        discovery = FlextPluginModels.DiscoveryData(
            name="test-plugin",
            version="1.0.0",
            path=Path("/path/to/plugin"),
            discovery_type="file",
            discovery_method="file_system",
        )

        assert discovery.name == "test-plugin"
        assert discovery.version == "1.0.0"
        assert discovery.path == Path("/path/to/plugin")
        assert discovery.discovery_type == "file"
        assert discovery.discovery_method == "file_system"

    def test_plugin_metadata_creation(self) -> None:
        """Test PluginMetadata creation."""
        metadata = FlextPluginModels.PluginMetadata(
            name="test-plugin",
            version="1.0.0",
            entry_point="test_plugin:main",
            author="Test Author",
            description="Test plugin description",
        )

        assert metadata.name == "test-plugin"
        assert metadata.version == "1.0.0"
        assert metadata.author == "Test Author"
        assert metadata.description == "Test plugin description"

    def test_validation_result_creation(self) -> None:
        """Test ValidationResult creation."""
        result = FlextPluginModels.ValidationResult(
            is_valid=True,
            errors=[],
            warnings=[],
        )

        assert result.is_valid is True
        assert result.errors == []
        assert result.warnings == []

    def test_validation_result_with_errors(self) -> None:
        """Test ValidationResult with errors."""
        result = FlextPluginModels.ValidationResult(
            is_valid=False,
            errors=["Error 1", "Error 2"],
            warnings=["Warning 1"],
        )

        assert result.is_valid is False
        assert len(result.errors) == 2
        assert len(result.warnings) == 1

    def test_config_creation(self) -> None:
        """Test Config model creation."""
        config = FlextPluginModels.Config(
            plugin_name="test-plugin",
            settings={"key": "value"},
        )

        assert config.plugin_name == "test-plugin"
        assert config.settings == {"key": "value"}

    def test_registry_creation(self) -> None:
        """Test Registry model creation."""
        registry = FlextPluginModels.Registry(
            plugins={"plugin1": {}},
        )

        assert "plugin1" in registry.plugins
        assert isinstance(registry.last_updated, datetime)
        assert isinstance(registry.created_at, datetime)

