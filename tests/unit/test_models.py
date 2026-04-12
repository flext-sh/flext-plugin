"""Unit tests for FlextPluginModels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import math
from datetime import datetime
from pathlib import Path

import pytest

from tests import c, m


class TestFlextPluginModels:
    """Test cases for FlextPluginModels."""

    def test_models_initialization(self) -> None:
        """Test that models can be initialized."""
        models = m()
        assert models is not None

    def test_plugin_status_enum(self) -> None:
        """Test PluginStatus enum values and methods."""
        assert c.Plugin.PluginStatus.UNKNOWN == "unknown"
        assert c.Plugin.PluginStatus.DISCOVERED == "discovered"
        assert c.Plugin.PluginStatus.LOADED == "loaded"
        assert c.Plugin.PluginStatus.ACTIVE == "active"
        assert c.Plugin.PluginStatus.INACTIVE == "inactive"
        assert c.Plugin.PluginStatus.LOADING == "loading"
        assert c.Plugin.PluginStatus.ERROR == "error"
        assert c.Plugin.PluginStatus.DISABLED == "disabled"
        assert c.Plugin.PluginStatus.HEALTHY == "healthy"
        assert c.Plugin.PluginStatus.UNHEALTHY == "unhealthy"
        operational_statuses = c.Plugin.PluginStatus.get_operational_statuses()
        assert c.Plugin.PluginStatus.ACTIVE in operational_statuses
        assert c.Plugin.PluginStatus.HEALTHY in operational_statuses
        assert c.Plugin.PluginStatus.LOADED in operational_statuses
        error_statuses = c.Plugin.PluginStatus.get_error_statuses()
        assert c.Plugin.PluginStatus.ERROR in error_statuses
        assert c.Plugin.PluginStatus.UNHEALTHY in error_statuses
        assert c.Plugin.PluginStatus.DISABLED in error_statuses
        assert c.Plugin.PluginStatus.ACTIVE.is_operational() is True
        assert c.Plugin.PluginStatus.ERROR.is_operational() is False
        assert c.Plugin.PluginStatus.ERROR.is_error_state() is True
        assert c.Plugin.PluginStatus.ACTIVE.is_error_state() is False

    def test_plugin_type_enum(self) -> None:
        """Test PluginType enum values."""
        assert c.Plugin.PluginType.TAP == "tap"
        assert c.Plugin.PluginType.TARGET == "target"
        assert c.Plugin.PluginType.TRANSFORM == "transform"
        assert c.Plugin.PluginType.EXTENSION == "extension"
        assert c.Plugin.PluginType.SERVICE == "service"
        assert c.Plugin.PluginType.MIDDLEWARE == "middleware"
        assert c.Plugin.PluginType.TRANSFORMER == "transformer"
        assert c.Plugin.PluginType.API == "api"
        assert c.Plugin.PluginType.DATABASE == "database"
        assert c.Plugin.PluginType.NOTIFICATION == "notification"
        assert c.Plugin.PluginType.AUTHENTICATION == "authentication"
        assert c.Plugin.PluginType.AUTHORIZATION == "authorization"
        assert c.Plugin.PluginType.UTILITY == "utility"
        assert c.Plugin.PluginType.TOOL == "tool"
        assert c.Plugin.PluginType.HANDLER == "handler"
        assert c.Plugin.PluginType.PROCESSOR == "processor"
        assert c.Plugin.PluginType.CORE == "core"
        assert c.Plugin.PluginType.ADDON == "addon"
        assert c.Plugin.PluginType.THEME == "theme"
        assert c.Plugin.PluginType.LANGUAGE == "language"

    def test_plugin_model_creation(self) -> None:
        """Test Plugin model creation."""
        plugin = m.Plugin.Plugin(
            name="test-plugin",
            plugin_version="1.0.0",
            description="",
            author="",
            plugin_type=c.Plugin.PluginType.UTILITY,
            is_enabled=True,
        )
        assert plugin.name == "test-plugin"
        assert plugin.plugin_version == "1.0.0"
        assert plugin.plugin_type == c.Plugin.PluginType.UTILITY
        assert plugin.is_enabled is True

    def test_plugin_model_validation(self) -> None:
        """Test Plugin model validation rules."""
        plugin = m.Plugin.Plugin(
            name="valid-plugin",
            plugin_version="1.0.0",
            description="",
            author="",
            plugin_type=c.Plugin.PluginType.UTILITY,
            is_enabled=True,
        )
        assert plugin.name == "valid-plugin"
        with pytest.raises(ValueError):
            m.Plugin.Plugin(
                name="",
                plugin_version="1.0.0",
                description="",
                author="",
                plugin_type=c.Plugin.PluginType.UTILITY,
                is_enabled=True,
            )
        with pytest.raises(ValueError):
            m.Plugin.Plugin(
                name="test-plugin",
                plugin_version="invalid-version",
                description="",
                author="",
                plugin_type=c.Plugin.PluginType.UTILITY,
                is_enabled=True,
            )

    def test_execution_result_creation(self) -> None:
        """Test ExecutionResult creation."""
        result = m.Plugin.ExecutionResult(
            success=True,
            data={"output": "result"},
            error="",
            execution_time_ms=1500.0,
        )
        assert result.success is True
        assert result.data == {"output": "result"}
        assert not result.error
        assert math.isclose(result.execution_time_ms, 1500.0)

    def test_execution_result_failure(self) -> None:
        """Test ExecutionResult failure case."""
        result = m.Plugin.ExecutionResult(
            success=False,
            data={},
            error="Plugin execution failed",
            execution_time_ms=500.0,
        )
        assert result.success is False
        assert result.error == "Plugin execution failed"

    def test_discovery_data_creation(self) -> None:
        """Test DiscoveryData creation."""
        discovery = m.Plugin.DiscoveryData(
            name="test-plugin",
            version="1.0.0",
            path=Path("/path/to/plugin"),
            discovery_type=c.Plugin.DiscoveryTypeLiteral.FILE,
            discovery_method=c.Plugin.DiscoveryMethodLiteral.FILE_SYSTEM,
        )
        assert discovery.name == "test-plugin"
        assert discovery.version == "1.0.0"
        assert discovery.path == Path("/path/to/plugin")
        assert discovery.discovery_type == "file"
        assert discovery.discovery_method == "file_system"

    def test_plugin_metadata_creation(self) -> None:
        """Test PluginMetadata creation."""
        metadata = m.Plugin.PluginMetadata(
            name="test-plugin",
            version="1.0.0",
            entry_point="test_plugin:main",
            author="Test Author",
            description="Test plugin description",
            plugin_type="extension",
        )
        assert metadata.name == "test-plugin"
        assert metadata.version == "1.0.0"
        assert metadata.author == "Test Author"
        assert metadata.description == "Test plugin description"

    def test_validation_result_creation(self) -> None:
        """Test ValidationResult creation."""
        result = m.Plugin.ValidationResult(
            valid=True,
            errors=[],
            warnings=[],
        )
        assert result.valid is True
        assert result.errors == []
        assert result.warnings == []

    def test_validation_result_with_errors(self) -> None:
        """Test ValidationResult with errors."""
        result = m.Plugin.ValidationResult(
            valid=False,
            errors=["Error 1", "Error 2"],
            warnings=["Warning 1"],
        )
        assert result.valid is False
        assert len(result.errors) == 2
        assert len(result.warnings) == 1

    def test_config_creation(self) -> None:
        """Test Config model creation."""
        settings = m.Plugin.PluginConfig(
            plugin_name="test-plugin",
            config={"key": "value"},
        )
        assert settings.plugin_name == "test-plugin"
        assert settings.config == {"key": "value"}

    def test_registry_creation(self) -> None:
        """Test Registry model creation."""
        registry = m.Plugin.Registry(plugins={"plugin1": {}})
        assert "plugin1" in registry.plugins
        assert isinstance(registry.last_updated, datetime)
        assert isinstance(registry.created_at, datetime)
