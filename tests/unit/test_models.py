"""Unit tests for FlextPluginModels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import math
from datetime import datetime
from pathlib import Path

import pytest
from flext_tests import tm

from tests import c, m


class TestFlextPluginModels:
    """Test cases for FlextPluginModels."""

    def test_models_initialization(self) -> None:
        """Test that models can be initialized."""
        models = m()
        assert models is not None

    def test_plugin_status_enum(self) -> None:
        """Test PluginStatus enum values and methods."""
        tm.that(c.Plugin.PluginStatus.UNKNOWN, eq="unknown")
        tm.that(c.Plugin.PluginStatus.DISCOVERED, eq="discovered")
        tm.that(c.Plugin.PluginStatus.LOADED, eq="loaded")
        tm.that(c.Plugin.PluginStatus.ACTIVE, eq="active")
        tm.that(c.Plugin.PluginStatus.INACTIVE, eq="inactive")
        tm.that(c.Plugin.PluginStatus.LOADING, eq="loading")
        tm.that(c.Plugin.PluginStatus.ERROR, eq="error")
        tm.that(c.Plugin.PluginStatus.DISABLED, eq="disabled")
        tm.that(c.Plugin.PluginStatus.HEALTHY, eq="healthy")
        tm.that(c.Plugin.PluginStatus.UNHEALTHY, eq="unhealthy")
        operational_statuses = c.Plugin.PluginStatus.get_operational_statuses()
        tm.that(
            operational_statuses,
            has=c.Plugin.PluginStatus.ACTIVE,
        )
        tm.that(
            operational_statuses,
            has=c.Plugin.PluginStatus.HEALTHY,
        )
        tm.that(
            operational_statuses,
            has=c.Plugin.PluginStatus.LOADED,
        )
        error_statuses = c.Plugin.PluginStatus.get_error_statuses()
        tm.that(error_statuses, has=c.Plugin.PluginStatus.ERROR)
        tm.that(error_statuses, has=c.Plugin.PluginStatus.UNHEALTHY)
        tm.that(error_statuses, has=c.Plugin.PluginStatus.DISABLED)
        tm.that(
            c.Plugin.PluginStatus.ACTIVE.is_operational(),
            eq=True,
        )
        tm.that(
            not c.Plugin.PluginStatus.ERROR.is_operational(),
            eq=True,
        )
        tm.that(
            c.Plugin.PluginStatus.ERROR.is_error_state(),
            eq=True,
        )
        tm.that(
            not c.Plugin.PluginStatus.ACTIVE.is_error_state(),
            eq=True,
        )

    def test_plugin_type_enum(self) -> None:
        """Test PluginType enum values."""
        tm.that(c.Plugin.PluginType.TAP, eq="tap")
        tm.that(c.Plugin.PluginType.TARGET, eq="target")
        tm.that(c.Plugin.PluginType.TRANSFORM, eq="transform")
        tm.that(c.Plugin.PluginType.EXTENSION, eq="extension")
        tm.that(c.Plugin.PluginType.SERVICE, eq="service")
        tm.that(c.Plugin.PluginType.MIDDLEWARE, eq="middleware")
        tm.that(c.Plugin.PluginType.TRANSFORMER, eq="transformer")
        tm.that(c.Plugin.PluginType.API, eq="api")
        tm.that(c.Plugin.PluginType.DATABASE, eq="database")
        tm.that(c.Plugin.PluginType.NOTIFICATION, eq="notification")
        tm.that(
            c.Plugin.PluginType.AUTHENTICATION,
            eq="authentication",
        )
        tm.that(
            c.Plugin.PluginType.AUTHORIZATION,
            eq="authorization",
        )
        tm.that(c.Plugin.PluginType.UTILITY, eq="utility")
        tm.that(c.Plugin.PluginType.TOOL, eq="tool")
        tm.that(c.Plugin.PluginType.HANDLER, eq="handler")
        tm.that(c.Plugin.PluginType.PROCESSOR, eq="processor")
        tm.that(c.Plugin.PluginType.CORE, eq="core")
        tm.that(c.Plugin.PluginType.ADDON, eq="addon")
        tm.that(c.Plugin.PluginType.THEME, eq="theme")
        tm.that(c.Plugin.PluginType.LANGUAGE, eq="language")

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
        tm.that(plugin.name, eq="test-plugin")
        tm.that(plugin.plugin_version, eq="1.0.0")
        tm.that(plugin.plugin_type, eq=c.Plugin.PluginType.UTILITY)
        tm.that(plugin.is_enabled is True, eq=True)

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
        tm.that(plugin.name, eq="valid-plugin")
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
        tm.that(result.success is True, eq=True)
        tm.that(result.data, eq={"output": "result"})
        tm.that(not result.error, eq=True)
        assert math.isclose(result.execution_time_ms, 1500.0)

    def test_execution_result_failure(self) -> None:
        """Test ExecutionResult failure case."""
        result = m.Plugin.ExecutionResult(
            success=False,
            data={},
            error="Plugin execution failed",
            execution_time_ms=500.0,
        )
        tm.that(result.success is False, eq=True)
        tm.that(result.error, eq="Plugin execution failed")

    def test_discovery_data_creation(self) -> None:
        """Test DiscoveryData creation."""
        discovery = m.Plugin.DiscoveryData(
            name="test-plugin",
            version="1.0.0",
            path=Path("/path/to/plugin"),
            discovery_type=c.Plugin.DiscoveryTypeLiteral.FILE,
            discovery_method=c.Plugin.DiscoveryMethodLiteral.FILE_SYSTEM,
        )
        tm.that(discovery.name, eq="test-plugin")
        tm.that(discovery.version, eq="1.0.0")
        tm.that(discovery.path, eq=Path("/path/to/plugin"))
        tm.that(discovery.discovery_type, eq="file")
        tm.that(discovery.discovery_method, eq="file_system")

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
        tm.that(metadata.name, eq="test-plugin")
        tm.that(metadata.version, eq="1.0.0")
        tm.that(metadata.author, eq="Test Author")
        tm.that(metadata.description, eq="Test plugin description")

    def test_validation_result_creation(self) -> None:
        """Test ValidationResult creation."""
        result = m.Plugin.ValidationResult(
            is_valid=True,
            errors=[],
            warnings=[],
        )
        tm.that(result.is_valid is True, eq=True)
        tm.that(result.errors, eq=[])
        tm.that(result.warnings, eq=[])

    def test_validation_result_with_errors(self) -> None:
        """Test ValidationResult with errors."""
        result = m.Plugin.ValidationResult(
            is_valid=False,
            errors=["Error 1", "Error 2"],
            warnings=["Warning 1"],
        )
        tm.that(result.is_valid is False, eq=True)
        tm.that(len(result.errors), eq=2)
        tm.that(len(result.warnings), eq=1)

    def test_config_creation(self) -> None:
        """Test Config model creation."""
        config = m.Plugin.PluginConfig(
            plugin_name="test-plugin",
            settings={"key": "value"},
        )
        tm.that(config.plugin_name, eq="test-plugin")
        tm.that(config.settings, eq={"key": "value"})

    def test_registry_creation(self) -> None:
        """Test Registry model creation."""
        registry = m.Plugin.Registry(plugins={"plugin1": {}})
        tm.that(registry.plugins, has="plugin1")
        tm.that(registry.last_updated, is_=datetime)
        tm.that(registry.created_at, is_=datetime)
