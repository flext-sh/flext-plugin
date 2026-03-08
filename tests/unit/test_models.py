"""Unit tests for FlextPluginModels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest

from flext_plugin import FlextPluginConstants, FlextPluginModels


class TestFlextPluginModels:
    """Test cases for FlextPluginModels."""

    def test_models_initialization(self) -> None:
        """Test that models can be initialized."""
        models = FlextPluginModels()
        assert models is not None

    def test_plugin_status_enum(self) -> None:
        """Test PluginStatus enum values and methods."""
        assert FlextPluginConstants.Plugin.PluginStatus.UNKNOWN == "unknown"
        assert FlextPluginConstants.Plugin.PluginStatus.DISCOVERED == "discovered"
        assert FlextPluginConstants.Plugin.PluginStatus.LOADED == "loaded"
        assert FlextPluginConstants.Plugin.PluginStatus.ACTIVE == "active"
        assert FlextPluginConstants.Plugin.PluginStatus.INACTIVE == "inactive"
        assert FlextPluginConstants.Plugin.PluginStatus.LOADING == "loading"
        assert FlextPluginConstants.Plugin.PluginStatus.ERROR == "error"
        assert FlextPluginConstants.Plugin.PluginStatus.DISABLED == "disabled"
        assert FlextPluginConstants.Plugin.PluginStatus.HEALTHY == "healthy"
        assert FlextPluginConstants.Plugin.PluginStatus.UNHEALTHY == "unhealthy"
        operational_statuses = (
            FlextPluginConstants.Plugin.PluginStatus.get_operational_statuses()
        )
        assert FlextPluginConstants.Plugin.PluginStatus.ACTIVE in operational_statuses
        assert FlextPluginConstants.Plugin.PluginStatus.HEALTHY in operational_statuses
        assert FlextPluginConstants.Plugin.PluginStatus.LOADED in operational_statuses
        error_statuses = FlextPluginConstants.Plugin.PluginStatus.get_error_statuses()
        assert FlextPluginConstants.Plugin.PluginStatus.ERROR in error_statuses
        assert FlextPluginConstants.Plugin.PluginStatus.UNHEALTHY in error_statuses
        assert FlextPluginConstants.Plugin.PluginStatus.DISABLED in error_statuses
        assert FlextPluginConstants.Plugin.PluginStatus.ACTIVE.is_operational()
        assert not FlextPluginConstants.Plugin.PluginStatus.ERROR.is_operational()
        assert FlextPluginConstants.Plugin.PluginStatus.ERROR.is_error_state()
        assert not FlextPluginConstants.Plugin.PluginStatus.ACTIVE.is_error_state()

    def test_plugin_type_enum(self) -> None:
        """Test PluginType enum values."""
        assert FlextPluginConstants.Plugin.PluginType.TAP == "tap"
        assert FlextPluginConstants.Plugin.PluginType.TARGET == "target"
        assert FlextPluginConstants.Plugin.PluginType.TRANSFORM == "transform"
        assert FlextPluginConstants.Plugin.PluginType.EXTENSION == "extension"
        assert FlextPluginConstants.Plugin.PluginType.SERVICE == "service"
        assert FlextPluginConstants.Plugin.PluginType.MIDDLEWARE == "middleware"
        assert FlextPluginConstants.Plugin.PluginType.TRANSFORMER == "transformer"
        assert FlextPluginConstants.Plugin.PluginType.API == "api"
        assert FlextPluginConstants.Plugin.PluginType.DATABASE == "database"
        assert FlextPluginConstants.Plugin.PluginType.NOTIFICATION == "notification"
        assert FlextPluginConstants.Plugin.PluginType.AUTHENTICATION == "authentication"
        assert FlextPluginConstants.Plugin.PluginType.AUTHORIZATION == "authorization"
        assert FlextPluginConstants.Plugin.PluginType.UTILITY == "utility"
        assert FlextPluginConstants.Plugin.PluginType.TOOL == "tool"
        assert FlextPluginConstants.Plugin.PluginType.HANDLER == "handler"
        assert FlextPluginConstants.Plugin.PluginType.PROCESSOR == "processor"
        assert FlextPluginConstants.Plugin.PluginType.CORE == "core"
        assert FlextPluginConstants.Plugin.PluginType.ADDON == "addon"
        assert FlextPluginConstants.Plugin.PluginType.THEME == "theme"
        assert FlextPluginConstants.Plugin.PluginType.LANGUAGE == "language"

    def test_plugin_model_creation(self) -> None:
        """Test Plugin model creation."""
        plugin = FlextPluginModels.Plugin.Plugin(
            name="test-plugin",
            plugin_version="1.0.0",
            plugin_type=FlextPluginConstants.Plugin.PluginType.UTILITY,
        )
        assert plugin.name == "test-plugin"
        assert plugin.plugin_version == "1.0.0"
        assert plugin.plugin_type == FlextPluginConstants.Plugin.PluginType.UTILITY
        assert plugin.is_enabled is True

    def test_plugin_model_validation(self) -> None:
        """Test Plugin model validation rules."""
        plugin = FlextPluginModels.Plugin.Plugin(
            name="valid-plugin",
            plugin_version="1.0.0",
            plugin_type=FlextPluginConstants.Plugin.PluginType.UTILITY,
        )
        assert plugin.name == "valid-plugin"
        with pytest.raises(ValueError):
            FlextPluginModels.Plugin.Plugin(
                name="",
                plugin_version="1.0.0",
                plugin_type=FlextPluginConstants.Plugin.PluginType.UTILITY,
            )
        with pytest.raises(ValueError):
            FlextPluginModels.Plugin.Plugin(
                name="test-plugin",
                plugin_version="invalid-version",
                plugin_type=FlextPluginConstants.Plugin.PluginType.UTILITY,
            )

    def test_execution_result_creation(self) -> None:
        """Test ExecutionResult creation."""
        result = FlextPluginModels.Plugin.ExecutionResult(
            success=True, data={"output": "result"}, error="", execution_time_ms=1500.0
        )
        assert result.success is True
        assert result.data == {"output": "result"}
        assert not result.error
        assert result.execution_time_ms == pytest.approx(1500.0)

    def test_execution_result_failure(self) -> None:
        """Test ExecutionResult failure case."""
        result = FlextPluginModels.Plugin.ExecutionResult(
            success=False,
            data={},
            error="Plugin execution failed",
            execution_time_ms=500.0,
        )
        assert result.success is False
        assert result.error == "Plugin execution failed"

    def test_discovery_data_creation(self) -> None:
        """Test DiscoveryData creation."""
        discovery = FlextPluginModels.Plugin.DiscoveryData(
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
        metadata = FlextPluginModels.Plugin.PluginMetadata(
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
        result = FlextPluginModels.Plugin.ValidationResult(
            is_valid=True, errors=[], warnings=[]
        )
        assert result.is_valid is True
        assert result.errors == []
        assert result.warnings == []

    def test_validation_result_with_errors(self) -> None:
        """Test ValidationResult with errors."""
        result = FlextPluginModels.Plugin.ValidationResult(
            is_valid=False, errors=["Error 1", "Error 2"], warnings=["Warning 1"]
        )
        assert result.is_valid is False
        assert len(result.errors) == 2
        assert len(result.warnings) == 1

    def test_config_creation(self) -> None:
        """Test Config model creation."""
        config = FlextPluginModels.Plugin.PluginConfig(
            plugin_name="test-plugin", settings={"key": "value"}
        )
        assert config.plugin_name == "test-plugin"
        assert config.settings == {"key": "value"}

    def test_registry_creation(self) -> None:
        """Test Registry model creation."""
        registry = FlextPluginModels.Plugin.Registry(plugins={"plugin1": {}})
        assert "plugin1" in registry.plugins
        assert isinstance(registry.last_updated, datetime)
        assert isinstance(registry.created_at, datetime)
