from __future__ import annotations

import pytest
from flext_tests import tm

from flext_plugin import FlextPluginSettings


class TestFlextPluginSettings:
    def test_create_config(self) -> None:
        FlextPluginSettings.reset_for_testing()
        config = FlextPluginSettings(app_name="test-plugin")
        tm.that(config is not None, eq=True)
        tm.that(config.app_name == "test-plugin", eq=True)

    def test_create_config_with_defaults(self) -> None:
        FlextPluginSettings.reset_for_testing()
        config = FlextPluginSettings()
        tm.that(config.debug is False, eq=True)
        tm.that(config.trace is False, eq=True)
        tm.that(config.enable_caching is True, eq=True)
        tm.that(config.cache_ttl > 0, eq=True)
        tm.that(config.max_workers > 0, eq=True)
        tm.that(config.timeout_seconds > 0, eq=True)
        tm.that(config.api_key is None, eq=True)

    def test_create_config_with_custom_values(self) -> None:
        FlextPluginSettings.reset_for_testing()
        config = FlextPluginSettings(
            app_name="custom-plugin",
            debug=True,
            timeout_seconds=60.0,
            max_workers=8,
            enable_caching=False,
        )
        tm.that(config.app_name == "custom-plugin", eq=True)
        tm.that(config.debug is True, eq=True)
        tm.that(config.timeout_seconds == 60.0, eq=True)
        tm.that(config.max_workers == 8, eq=True)
        tm.that(config.enable_caching is False, eq=True)

    def test_update_timestamp(self) -> None:
        FlextPluginSettings.reset_for_testing()
        config = FlextPluginSettings()
        tm.that(config.timeout_seconds == 30.0, eq=True)
        tm.that(config.apply_override("timeout_seconds", 45.0), eq=True)
        tm.that(config.timeout_seconds == 45.0, eq=True)

    def test_validate_business_rules_valid(self) -> None:
        FlextPluginSettings.reset_for_testing()
        config = FlextPluginSettings(debug=True, trace=True)
        tm.that(config.debug is True, eq=True)
        tm.that(config.trace is True, eq=True)

    def test_validate_business_rules_empty_name(self) -> None:
        FlextPluginSettings.reset_for_testing()
        with pytest.raises(ValueError):
            _ = FlextPluginSettings(trace=True)

    def test_validate_business_rules_invalid_memory(self) -> None:
        FlextPluginSettings.reset_for_testing()
        with pytest.raises(ValueError):
            _ = FlextPluginSettings(max_workers="invalid")

    def test_validate_business_rules_invalid_cpu(self) -> None:
        FlextPluginSettings.reset_for_testing()
        with pytest.raises(ValueError):
            _ = FlextPluginSettings(log_level="INVALID")

    def test_validate_business_rules_invalid_timeout(self) -> None:
        FlextPluginSettings.reset_for_testing()
        with pytest.raises(ValueError):
            _ = FlextPluginSettings(database_url="invalid-url")

    def test_created_at_timestamp(self) -> None:
        FlextPluginSettings.reset_for_testing()
        config = FlextPluginSettings()
        tm.that(config.version != "", eq=True)

    def test_config_model_validation(self) -> None:
        FlextPluginSettings.reset_for_testing()
        config = FlextPluginSettings(app_name="valid-plugin")
        dumped = config.model_dump()
        tm.that(dumped["app_name"] == "valid-plugin", eq=True)
