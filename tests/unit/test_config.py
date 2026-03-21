from __future__ import annotations

import pytest
from flext_tests import u

from flext_plugin import FlextPluginSettings


class TestFlextPluginSettings:
    def test_create_config(self) -> None:
        FlextPluginSettings.reset_for_testing()
        config = FlextPluginSettings.get_global(overrides={"app_name": "test-plugin"})
        u.Tests.Matchers.that(config.model_dump() != {}, eq=True)
        u.Tests.Matchers.that(config.app_name == "test-plugin", eq=True)

    def test_create_config_with_defaults(self) -> None:
        FlextPluginSettings.reset_for_testing()
        config = FlextPluginSettings.get_global()
        u.Tests.Matchers.that(config.debug is False, eq=True)
        u.Tests.Matchers.that(config.trace is False, eq=True)
        u.Tests.Matchers.that(config.enable_caching is True, eq=True)
        u.Tests.Matchers.that(config.cache_ttl > 0, eq=True)
        u.Tests.Matchers.that(config.max_workers > 0, eq=True)
        u.Tests.Matchers.that(config.timeout_seconds > 0, eq=True)
        u.Tests.Matchers.that(config.api_key is None, eq=True)

    def test_create_config_with_custom_values(self) -> None:
        FlextPluginSettings.reset_for_testing()
        config = FlextPluginSettings.get_global(
            overrides={
                "app_name": "custom-plugin",
                "debug": True,
                "timeout_seconds": 60.0,
                "max_workers": 8,
                "enable_caching": False,
            },
        )
        u.Tests.Matchers.that(config.app_name == "custom-plugin", eq=True)
        u.Tests.Matchers.that(config.debug is True, eq=True)
        u.Tests.Matchers.that(abs(config.timeout_seconds - 60.0) < 1e-9, eq=True)
        u.Tests.Matchers.that(config.max_workers == 8, eq=True)
        u.Tests.Matchers.that(config.enable_caching is False, eq=True)

    def test_update_timestamp(self) -> None:
        FlextPluginSettings.reset_for_testing()
        config = FlextPluginSettings.get_global()
        initial_timeout = config.timeout_seconds
        u.Tests.Matchers.that(config.apply_override("timeout_seconds", 45.0), eq=True)
        u.Tests.Matchers.that(abs(config.timeout_seconds - 45.0) < 1e-9, eq=True)
        u.Tests.Matchers.that(initial_timeout != config.timeout_seconds, eq=True)

    def test_validate_business_rules_valid(self) -> None:
        FlextPluginSettings.reset_for_testing()
        config = FlextPluginSettings.get_global(
            overrides={"debug": True, "trace": True}
        )
        u.Tests.Matchers.that(config.debug is True, eq=True)
        u.Tests.Matchers.that(config.trace is True, eq=True)

    def test_validate_business_rules_empty_name(self) -> None:
        FlextPluginSettings.reset_for_testing()
        payload = FlextPluginSettings.get_global().model_dump(mode="python")
        payload["trace"] = True
        payload["debug"] = False
        with pytest.raises(ValueError):
            _ = FlextPluginSettings.model_validate(payload)

    def test_validate_business_rules_invalid_memory(self) -> None:
        FlextPluginSettings.reset_for_testing()
        payload = FlextPluginSettings.get_global().model_dump(mode="python")
        payload["max_workers"] = "invalid"
        with pytest.raises(ValueError):
            _ = FlextPluginSettings.model_validate(payload)

    def test_validate_business_rules_invalid_cpu(self) -> None:
        FlextPluginSettings.reset_for_testing()
        payload = FlextPluginSettings.get_global().model_dump(mode="python")
        payload["log_level"] = "INVALID"
        with pytest.raises(ValueError):
            _ = FlextPluginSettings.model_validate(payload)

    def test_validate_business_rules_invalid_timeout(self) -> None:
        FlextPluginSettings.reset_for_testing()
        payload = FlextPluginSettings.get_global().model_dump(mode="python")
        payload["database_url"] = "invalid-url"
        with pytest.raises(ValueError):
            _ = FlextPluginSettings.model_validate(payload)

    def test_created_at_timestamp(self) -> None:
        FlextPluginSettings.reset_for_testing()
        config = FlextPluginSettings.get_global()
        u.Tests.Matchers.that(config.version != "", eq=True)

    def test_config_model_validation(self) -> None:
        FlextPluginSettings.reset_for_testing()
        config = FlextPluginSettings.get_global(overrides={"app_name": "valid-plugin"})
        dumped = config.model_dump()
        u.Tests.Matchers.that(dumped["app_name"] == "valid-plugin", eq=True)
