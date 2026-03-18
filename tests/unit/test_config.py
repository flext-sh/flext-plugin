"""Unit tests for FlextPluginSettings.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import tm

from flext_plugin import FlextPluginSettings


class TestFlextPluginSettings:
    """Test cases for FlextPluginSettings."""

    def test_create_config(self) -> None:
        """Test that config can be created with the create method."""
        config = FlextPluginSettings.create(plugin_name="test-plugin")
        tm.that(config is not None, eq=True)
        tm.that(config.plugin_name == "test-plugin", eq=True)

    def test_create_config_with_defaults(self) -> None:
        """Test that config has sensible defaults."""
        config = FlextPluginSettings.create(plugin_name="test-plugin")
        tm.that(config.enabled is True, eq=True)
        tm.that(config.priority == 100, eq=True)
        tm.that(config.max_memory_mb == 512, eq=True)
        tm.that(config.max_cpu_percent == 50, eq=True)
        tm.that(config.timeout_seconds == 30, eq=True)
        tm.that(config.dependencies == [], eq=True)
        tm.that(config.settings == {}, eq=True)
        tm.that(config.config_data == {}, eq=True)

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
        tm.that(config.plugin_name == "custom-plugin", eq=True)
        tm.that(config.enabled is False, eq=True)
        tm.that(config.priority == 50, eq=True)
        tm.that(config.max_memory_mb == 1024, eq=True)
        tm.that(config.max_cpu_percent == 75, eq=True)
        tm.that(config.timeout_seconds == 60, eq=True)
        tm.that(config.dependencies == ["dep1", "dep2"], eq=True)
        tm.that(config.settings == {"key": "value"}, eq=True)
        tm.that(config.config_data == {"data_key": "data_value"}, eq=True)

    def test_update_timestamp(self) -> None:
        """Test update_timestamp method."""
        config = FlextPluginSettings.create(plugin_name="test-plugin")
        tm.that(config.updated_at is None, eq=True)
        config.update_timestamp()
        tm.that(config.updated_at is not None, eq=True)

    def test_validate_business_rules_valid(self) -> None:
        """Test validate_business_rules with valid config."""
        config = FlextPluginSettings.create(plugin_name="test-plugin")
        result = config.validate_business_rules()
        tm.that(result.is_success, eq=True)

    def test_validate_business_rules_empty_name(self) -> None:
        """Test validate_business_rules rejects empty name."""
        config = FlextPluginSettings.create(plugin_name="test")
        config.plugin_name = ""
        result = config.validate_business_rules()
        tm.that(result.is_failure, eq=True)
        tm.that("Plugin name is required" in str(result.error), eq=True)

    def test_validate_business_rules_invalid_memory(self) -> None:
        """Test validate_business_rules rejects invalid memory."""
        config = FlextPluginSettings.create(plugin_name="test-plugin")
        config.max_memory_mb = 0
        result = config.validate_business_rules()
        tm.that(result.is_failure, eq=True)
        tm.that("Maximum memory must be positive" in str(result.error), eq=True)

    def test_validate_business_rules_invalid_cpu(self) -> None:
        """Test validate_business_rules rejects invalid CPU percent."""
        config = FlextPluginSettings.create(plugin_name="test-plugin")
        config.max_cpu_percent = 150
        result = config.validate_business_rules()
        tm.that(result.is_failure, eq=True)
        tm.that(
            "CPU percentage must be between 0 and 100" in str(result.error), eq=True
        )

    def test_validate_business_rules_invalid_timeout(self) -> None:
        """Test validate_business_rules rejects invalid timeout."""
        config = FlextPluginSettings.create(plugin_name="test-plugin")
        config.timeout_seconds = 0
        result = config.validate_business_rules()
        tm.that(result.is_failure, eq=True)
        tm.that("Timeout must be positive" in str(result.error), eq=True)

    def test_created_at_timestamp(self) -> None:
        """Test that created_at is set automatically."""
        config = FlextPluginSettings.create(plugin_name="test-plugin")
        tm.that(config.created_at is not None, eq=True)

    def test_config_model_validation(self) -> None:
        """Test that Pydantic validates the model."""
        config = FlextPluginSettings.create(plugin_name="valid-plugin")
        tm.that(config.plugin_name == "valid-plugin", eq=True)
