"""Unit tests for FlextPluginModels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest
from flext_tests import u

from flext_plugin import FlextPluginConstants, FlextPluginModels


class TestFlextPluginModels:
    """Test cases for FlextPluginModels."""

    def test_models_initialization(self) -> None:
        """Test that models can be initialized."""
        models = FlextPluginModels()
        u.Tests.Matchers.that(models is not None, eq=True)

    def test_plugin_status_enum(self) -> None:
        """Test PluginStatus enum values and methods."""
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginStatus.UNKNOWN == "unknown", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginStatus.DISCOVERED == "discovered", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginStatus.LOADED == "loaded", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginStatus.ACTIVE == "active", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginStatus.INACTIVE == "inactive", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginStatus.LOADING == "loading", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginStatus.ERROR == "error", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginStatus.DISABLED == "disabled", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginStatus.HEALTHY == "healthy", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginStatus.UNHEALTHY == "unhealthy", eq=True
        )
        operational_statuses = (
            FlextPluginConstants.Plugin.PluginStatus.get_operational_statuses()
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginStatus.ACTIVE in operational_statuses,
            eq=True,
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginStatus.HEALTHY in operational_statuses,
            eq=True,
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginStatus.LOADED in operational_statuses,
            eq=True,
        )
        error_statuses = FlextPluginConstants.Plugin.PluginStatus.get_error_statuses()
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginStatus.ERROR in error_statuses, eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginStatus.UNHEALTHY in error_statuses,
            eq=True,
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginStatus.DISABLED in error_statuses, eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginStatus.ACTIVE.is_operational(), eq=True
        )
        u.Tests.Matchers.that(
            not FlextPluginConstants.Plugin.PluginStatus.ERROR.is_operational(), eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginStatus.ERROR.is_error_state(), eq=True
        )
        u.Tests.Matchers.that(
            not FlextPluginConstants.Plugin.PluginStatus.ACTIVE.is_error_state(),
            eq=True,
        )

    def test_plugin_type_enum(self) -> None:
        """Test PluginType enum values."""
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginType.TAP == "tap", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginType.TARGET == "target", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginType.TRANSFORM == "transform", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginType.EXTENSION == "extension", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginType.SERVICE == "service", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginType.MIDDLEWARE == "middleware", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginType.TRANSFORMER == "transformer", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginType.API == "api", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginType.DATABASE == "database", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginType.NOTIFICATION == "notification",
            eq=True,
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginType.AUTHENTICATION == "authentication",
            eq=True,
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginType.AUTHORIZATION == "authorization",
            eq=True,
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginType.UTILITY == "utility", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginType.TOOL == "tool", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginType.HANDLER == "handler", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginType.PROCESSOR == "processor", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginType.CORE == "core", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginType.ADDON == "addon", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginType.THEME == "theme", eq=True
        )
        u.Tests.Matchers.that(
            FlextPluginConstants.Plugin.PluginType.LANGUAGE == "language", eq=True
        )

    def test_plugin_model_creation(self) -> None:
        """Test Plugin model creation."""
        plugin = FlextPluginModels.Plugin.Plugin(
            name="test-plugin",
            plugin_version="1.0.0",
            plugin_type=FlextPluginConstants.Plugin.PluginType.UTILITY,
        )
        u.Tests.Matchers.that(plugin.name == "test-plugin", eq=True)
        u.Tests.Matchers.that(plugin.plugin_version == "1.0.0", eq=True)
        u.Tests.Matchers.that(
            plugin.plugin_type == FlextPluginConstants.Plugin.PluginType.UTILITY,
            eq=True,
        )
        u.Tests.Matchers.that(plugin.is_enabled is True, eq=True)

    def test_plugin_model_validation(self) -> None:
        """Test Plugin model validation rules."""
        plugin = FlextPluginModels.Plugin.Plugin(
            name="valid-plugin",
            plugin_version="1.0.0",
            plugin_type=FlextPluginConstants.Plugin.PluginType.UTILITY,
        )
        u.Tests.Matchers.that(plugin.name == "valid-plugin", eq=True)
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
        u.Tests.Matchers.that(result.success is True, eq=True)
        u.Tests.Matchers.that(result.data == {"output": "result"}, eq=True)
        u.Tests.Matchers.that(not result.error, eq=True)
        u.Tests.Matchers.that(
            result.execution_time_ms == pytest.approx(1500.0), eq=True
        )

    def test_execution_result_failure(self) -> None:
        """Test ExecutionResult failure case."""
        result = FlextPluginModels.Plugin.ExecutionResult(
            success=False,
            data={},
            error="Plugin execution failed",
            execution_time_ms=500.0,
        )
        u.Tests.Matchers.that(result.success is False, eq=True)
        u.Tests.Matchers.that(result.error == "Plugin execution failed", eq=True)

    def test_discovery_data_creation(self) -> None:
        """Test DiscoveryData creation."""
        discovery = FlextPluginModels.Plugin.DiscoveryData(
            name="test-plugin",
            version="1.0.0",
            path=Path("/path/to/plugin"),
            discovery_type="file",
            discovery_method="file_system",
        )
        u.Tests.Matchers.that(discovery.name == "test-plugin", eq=True)
        u.Tests.Matchers.that(discovery.version == "1.0.0", eq=True)
        u.Tests.Matchers.that(discovery.path == Path("/path/to/plugin"), eq=True)
        u.Tests.Matchers.that(discovery.discovery_type == "file", eq=True)
        u.Tests.Matchers.that(discovery.discovery_method == "file_system", eq=True)

    def test_plugin_metadata_creation(self) -> None:
        """Test PluginMetadata creation."""
        metadata = FlextPluginModels.Plugin.PluginMetadata(
            name="test-plugin",
            version="1.0.0",
            entry_point="test_plugin:main",
            author="Test Author",
            description="Test plugin description",
        )
        u.Tests.Matchers.that(metadata.name == "test-plugin", eq=True)
        u.Tests.Matchers.that(metadata.version == "1.0.0", eq=True)
        u.Tests.Matchers.that(metadata.author == "Test Author", eq=True)
        u.Tests.Matchers.that(
            metadata.description == "Test plugin description", eq=True
        )

    def test_validation_result_creation(self) -> None:
        """Test ValidationResult creation."""
        result = FlextPluginModels.Plugin.ValidationResult(
            is_valid=True, errors=[], warnings=[]
        )
        u.Tests.Matchers.that(result.is_valid is True, eq=True)
        u.Tests.Matchers.that(result.errors == [], eq=True)
        u.Tests.Matchers.that(result.warnings == [], eq=True)

    def test_validation_result_with_errors(self) -> None:
        """Test ValidationResult with errors."""
        result = FlextPluginModels.Plugin.ValidationResult(
            is_valid=False, errors=["Error 1", "Error 2"], warnings=["Warning 1"]
        )
        u.Tests.Matchers.that(result.is_valid is False, eq=True)
        u.Tests.Matchers.that(len(result.errors) == 2, eq=True)
        u.Tests.Matchers.that(len(result.warnings) == 1, eq=True)

    def test_config_creation(self) -> None:
        """Test Config model creation."""
        config = FlextPluginModels.Plugin.PluginConfig(
            plugin_name="test-plugin", settings={"key": "value"}
        )
        u.Tests.Matchers.that(config.plugin_name == "test-plugin", eq=True)
        u.Tests.Matchers.that(config.settings == {"key": "value"}, eq=True)

    def test_registry_creation(self) -> None:
        """Test Registry model creation."""
        registry = FlextPluginModels.Plugin.Registry(plugins={"plugin1": {}})
        u.Tests.Matchers.that("plugin1" in registry.plugins, eq=True)
        u.Tests.Matchers.that(isinstance(registry.last_updated, datetime), eq=True)
        u.Tests.Matchers.that(isinstance(registry.created_at, datetime), eq=True)
