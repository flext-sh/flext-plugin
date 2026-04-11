from __future__ import annotations

import pytest
from flext_tests import tm

from flext_plugin import FlextPluginSettings


class TestFlextPluginSettings:
    def test_create_config(self) -> None:
        FlextPluginSettings.reset_for_testing()
        config = FlextPluginSettings.fetch_global(overrides={"app_name": "test-plugin"})
        tm.that(config.model_dump(), ne={})
        tm.that(config.app_name, eq="test-plugin")

    def test_create_config_with_defaults(self) -> None:
        FlextPluginSettings.reset_for_testing()
        config = FlextPluginSettings.fetch_global()
        tm.that(config.debug is False, eq=True)
        tm.that(config.trace is False, eq=True)
        tm.that(config.enable_caching is True, eq=True)
        tm.that(config.cache_ttl, gt=0)
        tm.that(config.max_workers, gt=0)
        tm.that(config.timeout_seconds, gt=0)
        tm.that(config.api_key, none=True)

    def test_create_config_with_custom_values(self) -> None:
        FlextPluginSettings.reset_for_testing()
        config = FlextPluginSettings.fetch_global(
            overrides={
                "app_name": "custom-plugin",
                "debug": True,
                "timeout_seconds": 60.0,
                "max_workers": 8,
                "enable_caching": False,
            }
        )
        tm.that(config.app_name, eq="custom-plugin")
        tm.that(config.debug is True, eq=True)
        tm.that(abs(config.timeout_seconds - 60.0), lt=1e-9)
        tm.that(config.max_workers, eq=8)
        tm.that(config.enable_caching is False, eq=True)

    def test_update_timestamp(self) -> None:
        FlextPluginSettings.reset_for_testing()
        config = FlextPluginSettings.fetch_global()
        initial_timeout = config.timeout_seconds
        tm.that(config.apply_override("timeout_seconds", 45.0), eq=True)
        tm.that(abs(config.timeout_seconds - 45.0), lt=1e-9)
        tm.that(initial_timeout, ne=config.timeout_seconds)

    def test_validate_business_rules_valid(self) -> None:
        FlextPluginSettings.reset_for_testing()
        config = FlextPluginSettings.fetch_global(
            overrides={"debug": True, "trace": True}
        )
        tm.that(config.debug is True, eq=True)
        tm.that(config.trace is True, eq=True)

    def test_validate_business_rules_empty_name(self) -> None:
        FlextPluginSettings.reset_for_testing()
        payload = FlextPluginSettings.fetch_global().model_dump(mode="python")
        payload["trace"] = True
        payload["debug"] = False
        with pytest.raises(ValueError):
            _ = FlextPluginSettings.model_validate(payload)

    def test_validate_business_rules_invalid_memory(self) -> None:
        FlextPluginSettings.reset_for_testing()
        payload = FlextPluginSettings.fetch_global().model_dump(mode="python")
        payload["max_workers"] = "invalid"
        with pytest.raises(ValueError):
            _ = FlextPluginSettings.model_validate(payload)

    def test_validate_business_rules_invalid_cpu(self) -> None:
        FlextPluginSettings.reset_for_testing()
        payload = FlextPluginSettings.fetch_global().model_dump(mode="python")
        payload["log_level"] = "INVALID"
        with pytest.raises(ValueError):
            _ = FlextPluginSettings.model_validate(payload)

    def test_validate_business_rules_invalid_timeout(self) -> None:
        FlextPluginSettings.reset_for_testing()
        payload = FlextPluginSettings.fetch_global().model_dump(mode="python")
        payload["database_url"] = "invalid-url"
        with pytest.raises(ValueError):
            _ = FlextPluginSettings.model_validate(payload)

    def test_created_at_timestamp(self) -> None:
        FlextPluginSettings.reset_for_testing()
        config = FlextPluginSettings.fetch_global()
        tm.that(config.version, ne="")

    def test_config_model_validation(self) -> None:
        FlextPluginSettings.reset_for_testing()
        config = FlextPluginSettings.fetch_global(
            overrides={"app_name": "valid-plugin"}
        )
        dumped = config.model_dump()
        tm.that(dumped["app_name"], eq="valid-plugin")
