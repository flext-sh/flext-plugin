"""Unit tests for FlextPluginModels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests import c, m


class TestsFlextPluginModelsUnit:
    """Test cases for FlextPluginModels."""

    def test_models_initialization(self) -> None:
        """Test that models can be initialized."""
        models = m()
        assert models is not None

    def test_plugin_status_enum(self) -> None:
        """Test PluginStatus enum values and methods."""
        assert c.Plugin.PluginStatus.UNKNOWN.value == "unknown"
        assert c.Plugin.PluginStatus.DISCOVERED.value == "discovered"
        assert c.Plugin.PluginStatus.LOADED.value == "loaded"
        assert c.Plugin.PluginStatus.ACTIVE.value == "active"
        assert c.Plugin.PluginStatus.INACTIVE.value == "inactive"
        assert c.Plugin.PluginStatus.LOADING.value == "loading"
        assert c.Plugin.PluginStatus.ERROR.value == "error"
        assert c.Plugin.PluginStatus.DISABLED.value == "disabled"
        assert c.Plugin.PluginStatus.HEALTHY.value == "healthy"
        assert c.Plugin.PluginStatus.UNHEALTHY.value == "unhealthy"
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
        assert c.Plugin.Type.TAP.value == "tap"
        assert c.Plugin.Type.TARGET.value == "target"
        assert c.Plugin.Type.TRANSFORM.value == "transform"
        assert c.Plugin.Type.EXTENSION.value == "extension"
        assert c.Plugin.Type.SERVICE.value == "service"
        assert c.Plugin.Type.MIDDLEWARE.value == "middleware"
        assert c.Plugin.Type.TRANSFORMER.value == "transformer"
        assert c.Plugin.Type.API.value == "api"
        assert c.Plugin.Type.DATABASE.value == "database"
        assert c.Plugin.Type.NOTIFICATION.value == "notification"
        assert c.Plugin.Type.AUTHENTICATION.value == "authentication"
        assert c.Plugin.Type.AUTHORIZATION.value == "authorization"
        assert c.Plugin.Type.UTILITY.value == "utility"
        assert c.Plugin.Type.TOOL.value == "tool"
        assert c.Plugin.Type.HANDLER.value == "handler"
        assert c.Plugin.Type.PROCESSOR.value == "processor"
        assert c.Plugin.Type.CORE.value == "core"
        assert c.Plugin.Type.ADDON.value == "addon"
        assert c.Plugin.Type.THEME.value == "theme"
        assert c.Plugin.Type.LANGUAGE.value == "language"

    def test_plugin_model_creation(self) -> None:
        """Test Plugin model creation."""
        plugin = m.Plugin.Entity(
            name="test-plugin",
            plugin_version="1.0.0",
            description="",
            author="",
            plugin_type=c.Plugin.Type.UTILITY,
            is_enabled=True,
        )
        assert plugin.name == "test-plugin"
        assert plugin.plugin_version == "1.0.0"
        assert plugin.plugin_type == c.Plugin.Type.UTILITY
        assert plugin.is_enabled is True

    def test_plugin_model_validation(self) -> None:
        """Test Plugin model validation rules."""
        plugin = m.Plugin.Entity(
            name="valid-plugin",
            plugin_version="1.0.0",
            description="",
            author="",
            plugin_type=c.Plugin.Type.UTILITY,
            is_enabled=True,
        )
        assert plugin.name == "valid-plugin"
        with pytest.raises(ValueError):
            m.Plugin.Entity(
                name="",
                plugin_version="1.0.0",
                description="",
                author="",
                plugin_type=c.Plugin.Type.UTILITY,
                is_enabled=True,
            )
        with pytest.raises(ValueError):
            m.Plugin.Entity(
                name="test-plugin",
                plugin_version="invalid-version",
                description="",
                author="",
                plugin_type=c.Plugin.Type.UTILITY,
                is_enabled=True,
            )

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
