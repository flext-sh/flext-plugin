"""Unit tests for FlextPluginModels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest
from flext_tests import tm

from flext_plugin import FlextPluginConstants, FlextPluginModels


class TestFlextPluginModels:
    """Test cases for FlextPluginModels."""

    def test_models_initialization(self) -> None:
        """Test that models can be initialized."""
        models = FlextPluginModels()
        tm.that(models, none=False)

    def test_plugin_status_enum(self) -> None:
        """Test PluginStatus enum values and methods."""
        tm.that(FlextPluginConstants.Plugin.PluginStatus.UNKNOWN, eq="unknown")
        tm.that(FlextPluginConstants.Plugin.PluginStatus.DISCOVERED, eq="discovered")
        tm.that(FlextPluginConstants.Plugin.PluginStatus.LOADED, eq="loaded")
        tm.that(FlextPluginConstants.Plugin.PluginStatus.ACTIVE, eq="active")
        tm.that(FlextPluginConstants.Plugin.PluginStatus.INACTIVE, eq="inactive")
        tm.that(FlextPluginConstants.Plugin.PluginStatus.LOADING, eq="loading")
        tm.that(FlextPluginConstants.Plugin.PluginStatus.ERROR, eq="error")
        tm.that(FlextPluginConstants.Plugin.PluginStatus.DISABLED, eq="disabled")
        tm.that(FlextPluginConstants.Plugin.PluginStatus.HEALTHY, eq="healthy")
        tm.that(FlextPluginConstants.Plugin.PluginStatus.UNHEALTHY, eq="unhealthy")
        operational_statuses = (
            FlextPluginConstants.Plugin.PluginStatus.get_operational_statuses()
        )
        tm.that(
            operational_statuses, has=FlextPluginConstants.Plugin.PluginStatus.ACTIVE
        )
        tm.that(
            operational_statuses, has=FlextPluginConstants.Plugin.PluginStatus.HEALTHY
        )
        tm.that(
            operational_statuses, has=FlextPluginConstants.Plugin.PluginStatus.LOADED
        )
        error_statuses = FlextPluginConstants.Plugin.PluginStatus.get_error_statuses()
        tm.that(error_statuses, has=FlextPluginConstants.Plugin.PluginStatus.ERROR)
        tm.that(error_statuses, has=FlextPluginConstants.Plugin.PluginStatus.UNHEALTHY)
        tm.that(error_statuses, has=FlextPluginConstants.Plugin.PluginStatus.DISABLED)
        tm.that(
            FlextPluginConstants.Plugin.PluginStatus.ACTIVE.is_operational(), eq=True
        )
        tm.that(
            FlextPluginConstants.Plugin.PluginStatus.ERROR.is_operational(), eq=False
        )
        tm.that(
            FlextPluginConstants.Plugin.PluginStatus.ERROR.is_error_state(), eq=True
        )
        tm.that(
            FlextPluginConstants.Plugin.PluginStatus.ACTIVE.is_error_state(), eq=False
        )

    def test_plugin_type_enum(self) -> None:
        """Test PluginType enum values."""
        tm.that(FlextPluginConstants.Plugin.PluginType.TAP, eq="tap")
        tm.that(FlextPluginConstants.Plugin.PluginType.TARGET, eq="target")
        tm.that(FlextPluginConstants.Plugin.PluginType.TRANSFORM, eq="transform")
        tm.that(FlextPluginConstants.Plugin.PluginType.EXTENSION, eq="extension")
        tm.that(FlextPluginConstants.Plugin.PluginType.SERVICE, eq="service")
        tm.that(FlextPluginConstants.Plugin.PluginType.MIDDLEWARE, eq="middleware")
        tm.that(FlextPluginConstants.Plugin.PluginType.TRANSFORMER, eq="transformer")
        tm.that(FlextPluginConstants.Plugin.PluginType.API, eq="api")
        tm.that(FlextPluginConstants.Plugin.PluginType.DATABASE, eq="database")
        tm.that(FlextPluginConstants.Plugin.PluginType.NOTIFICATION, eq="notification")
        tm.that(
            FlextPluginConstants.Plugin.PluginType.AUTHENTICATION, eq="authentication"
        )
        tm.that(
            FlextPluginConstants.Plugin.PluginType.AUTHORIZATION, eq="authorization"
        )
        tm.that(FlextPluginConstants.Plugin.PluginType.UTILITY, eq="utility")
        tm.that(FlextPluginConstants.Plugin.PluginType.TOOL, eq="tool")
        tm.that(FlextPluginConstants.Plugin.PluginType.HANDLER, eq="handler")
        tm.that(FlextPluginConstants.Plugin.PluginType.PROCESSOR, eq="processor")
        tm.that(FlextPluginConstants.Plugin.PluginType.CORE, eq="core")
        tm.that(FlextPluginConstants.Plugin.PluginType.ADDON, eq="addon")
        tm.that(FlextPluginConstants.Plugin.PluginType.THEME, eq="theme")
        tm.that(FlextPluginConstants.Plugin.PluginType.LANGUAGE, eq="language")

    def test_plugin_model_creation(self) -> None:
        """Test Plugin model creation."""
        plugin = FlextPluginModels.Plugin.Plugin(
            name="test-plugin",
            plugin_version="1.0.0",
            plugin_type=FlextPluginConstants.Plugin.PluginType.UTILITY,
        )
        tm.that(plugin.name, eq="test-plugin")
        tm.that(plugin.plugin_version, eq="1.0.0")
        tm.that(plugin.plugin_type, eq=FlextPluginConstants.Plugin.PluginType.UTILITY)
        tm.that(plugin.is_enabled is True, eq=True)

    def test_plugin_model_validation(self) -> None:
        """Test Plugin model validation rules."""
        plugin = FlextPluginModels.Plugin.Plugin(
            name="valid-plugin",
            plugin_version="1.0.0",
            plugin_type=FlextPluginConstants.Plugin.PluginType.UTILITY,
        )
        tm.that(plugin.name, eq="valid-plugin")
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
        tm.that(result.success is True, eq=True)
        tm.that(result.data, eq={"output": "result"})
        tm.that(result.error, eq=False)
        tm.that(result.execution_time_ms, eq=pytest.approx(1500.0))

    def test_execution_result_failure(self) -> None:
        """Test ExecutionResult failure case."""
        result = FlextPluginModels.Plugin.ExecutionResult(
            success=False,
            data={},
            error="Plugin execution failed",
            execution_time_ms=500.0,
        )
        tm.that(result.success is False, eq=True)
        tm.that(result.error, eq="Plugin execution failed")

    def test_discovery_data_creation(self) -> None:
        """Test DiscoveryData creation."""
        discovery = FlextPluginModels.Plugin.DiscoveryData(
            name="test-plugin",
            version="1.0.0",
            path=Path("/path/to/plugin"),
            discovery_type="file",
            discovery_method="file_system",
        )
        tm.that(discovery.name, eq="test-plugin")
        tm.that(discovery.version, eq="1.0.0")
        tm.that(discovery.path, eq=Path("/path/to/plugin"))
        tm.that(discovery.discovery_type, eq="file")
        tm.that(discovery.discovery_method, eq="file_system")

    def test_plugin_metadata_creation(self) -> None:
        """Test PluginMetadata creation."""
        metadata = FlextPluginModels.Plugin.PluginMetadata(
            name="test-plugin",
            version="1.0.0",
            entry_point="test_plugin:main",
            author="Test Author",
            description="Test plugin description",
        )
        tm.that(metadata.name, eq="test-plugin")
        tm.that(metadata.version, eq="1.0.0")
        tm.that(metadata.author, eq="Test Author")
        tm.that(metadata.description, eq="Test plugin description")

    def test_validation_result_creation(self) -> None:
        """Test ValidationResult creation."""
        result = FlextPluginModels.Plugin.ValidationResult(
            is_valid=True, errors=[], warnings=[]
        )
        tm.that(result.is_valid is True, eq=True)
        tm.that(result.errors, eq=[])
        tm.that(result.warnings, eq=[])

    def test_validation_result_with_errors(self) -> None:
        """Test ValidationResult with errors."""
        result = FlextPluginModels.Plugin.ValidationResult(
            is_valid=False, errors=["Error 1", "Error 2"], warnings=["Warning 1"]
        )
        tm.that(result.is_valid is False, eq=True)
        tm.that(len(result.errors), eq=2)
        tm.that(len(result.warnings), eq=1)

    def test_config_creation(self) -> None:
        """Test Config model creation."""
        config = FlextPluginModels.Plugin.PluginConfig(
            plugin_name="test-plugin", settings={"key": "value"}
        )
        tm.that(config.plugin_name, eq="test-plugin")
        tm.that(config.settings, eq={"key": "value"})

    def test_registry_creation(self) -> None:
        """Test Registry model creation."""
        registry = FlextPluginModels.Plugin.Registry(plugins={"plugin1": {}})
        tm.that(registry.plugins, has="plugin1")
        tm.that(registry.last_updated, is_=datetime)
        tm.that(registry.created_at, is_=datetime)
