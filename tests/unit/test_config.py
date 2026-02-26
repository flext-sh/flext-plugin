"""Unit tests for FlextPluginSettings.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from flext_plugin.settings import FlextPluginSettings


class TestFlextPluginSettings:
    """Test cases for FlextPluginSettings."""

    def test_create_config(self) -> None:
        """Test that config can be created with the create method."""
        config = FlextPluginSettings.create(plugin_name="test-plugin")
        assert config is not None
        assert config.plugin_name == "test-plugin"

    def test_create_config_with_defaults(self) -> None:
        """Test that config has sensible defaults."""
        config = FlextPluginSettings.create(plugin_name="test-plugin")

        assert config.enabled is True
        assert config.priority == 100
        assert config.max_memory_mb == 512
        assert config.max_cpu_percent == 50
        assert config.timeout_seconds == 30
        assert config.dependencies == []
        assert config.settings == {}
        assert config.config_data == {}

    def test_create_config_with_custom_values(self) -> None:
        """Test config creation with custom values."""
        options = FlextPluginSettings.CreateOptions(
            enabled=False,
            priority=50,
            max_memory_mb=1024,
            max_cpu_percent=75,
            timeout_seconds=60,
            dependencies=["dep1", "dep2"],
            settings={"key": "value"},
        )
        config = FlextPluginSettings.create(
            plugin_name="custom-plugin",
            config_data={"data_key": "data_value"},
            options=options,
        )

        assert config.plugin_name == "custom-plugin"
        assert config.enabled is False
        assert config.priority == 50
        assert config.max_memory_mb == 1024
        assert config.max_cpu_percent == 75
        assert config.timeout_seconds == 60
        assert config.dependencies == ["dep1", "dep2"]
        assert config.settings == {"key": "value"}
        assert config.config_data == {"data_key": "data_value"}

    def test_update_timestamp(self) -> None:
        """Test update_timestamp method."""
        config = FlextPluginSettings.create(plugin_name="test-plugin")
        assert config.updated_at is None

        config.update_timestamp()
        assert config.updated_at is not None

    def test_validate_business_rules_valid(self) -> None:
        """Test validate_business_rules with valid config."""
        config = FlextPluginSettings.create(plugin_name="test-plugin")
        result = config.validate_business_rules()
        assert result.is_success

    def test_validate_business_rules_empty_name(self) -> None:
        """Test validate_business_rules rejects empty name."""
        config = FlextPluginSettings.create(plugin_name="test")
        config.plugin_name = ""
        result = config.validate_business_rules()
        assert result.is_failure
        assert "Plugin name is required" in str(result.error)

    def test_validate_business_rules_invalid_memory(self) -> None:
        """Test validate_business_rules rejects invalid memory."""
        config = FlextPluginSettings.create(plugin_name="test-plugin")
        config.max_memory_mb = 0
        result = config.validate_business_rules()
        assert result.is_failure
        assert "Maximum memory must be positive" in str(result.error)

    def test_validate_business_rules_invalid_cpu(self) -> None:
        """Test validate_business_rules rejects invalid CPU percent."""
        config = FlextPluginSettings.create(plugin_name="test-plugin")
        config.max_cpu_percent = 150
        result = config.validate_business_rules()
        assert result.is_failure
        assert "CPU percentage must be between 0 and 100" in str(result.error)

    def test_validate_business_rules_invalid_timeout(self) -> None:
        """Test validate_business_rules rejects invalid timeout."""
        config = FlextPluginSettings.create(plugin_name="test-plugin")
        config.timeout_seconds = 0
        result = config.validate_business_rules()
        assert result.is_failure
        assert "Timeout must be positive" in str(result.error)

    def test_created_at_timestamp(self) -> None:
        """Test that created_at is set automatically."""
        config = FlextPluginSettings.create(plugin_name="test-plugin")
        assert config.created_at is not None

    def test_config_model_validation(self) -> None:
        """Test that Pydantic validates the model."""
        # Valid config should work
        config = FlextPluginSettings.create(plugin_name="valid-plugin")
        assert config.plugin_name == "valid-plugin"
