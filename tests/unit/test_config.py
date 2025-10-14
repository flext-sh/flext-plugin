"""Unit tests for FlextPluginConfig.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from unittest.mock import patch

import pytest

from flext_plugin.config import FlextPluginConfig


class TestFlextPluginConfig:
    """Test cases for FlextPluginConfig."""

    def test_config_initialization(self) -> None:
        """Test that config can be initialized with defaults."""
        config = FlextPluginConfig()
        assert config is not None

    def test_discovery_config(self) -> None:
        """Test discovery configuration section."""
        config = FlextPluginConfig()
        discovery = config.discovery

        assert discovery.plugin_paths is not None
        assert len(discovery.plugin_paths) > 0
        assert discovery.timeout_seconds > 0
        assert discovery.enable_validation is True
        assert discovery.enable_security_scan is True
        assert discovery.recursive_search is True
        assert len(discovery.file_extensions) > 0

    def test_discovery_config_validation(self) -> None:
        """Test discovery configuration validation."""
        config = FlextPluginConfig()
        discovery = config.discovery

        # Test valid plugin paths
        discovery.plugin_paths = ["/path1", "/path2"]
        assert discovery.plugin_paths == ["/path1", "/path2"]

        # Test empty plugin paths
        with pytest.raises(ValueError):
            discovery.plugin_paths = []

        # Test invalid timeout
        with pytest.raises(ValueError):
            discovery.timeout_seconds = 0

        with pytest.raises(ValueError):
            discovery.timeout_seconds = -1

    def test_security_config(self) -> None:
        """Test security configuration section."""
        config = FlextPluginConfig()
        security = config.security

        assert security.default_level in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
        assert isinstance(security.enable_sandboxing, bool)
        assert isinstance(security.require_signature_verification, bool)
        assert isinstance(security.allowed_imports, list)
        assert isinstance(security.blocked_imports, list)
        assert isinstance(security.network_access, bool)
        assert isinstance(security.file_system_access, bool)
        assert security.max_execution_time > 0

    def test_security_config_validation(self) -> None:
        """Test security configuration validation."""
        config = FlextPluginConfig()
        security = config.security

        # Test valid security level
        security.default_level = "HIGH"
        assert security.default_level == "HIGH"

        # Test invalid security level
        with pytest.raises(ValueError):
            security.default_level = "INVALID"

        # Test case insensitive security level
        security.default_level = "high"
        assert security.default_level == "HIGH"

    def test_performance_config(self) -> None:
        """Test performance configuration section."""
        config = FlextPluginConfig()
        performance = config.performance

        assert performance.max_memory_mb > 0
        assert 0 <= performance.max_cpu_percent <= 100
        assert performance.max_concurrent_plugins > 0
        assert isinstance(performance.enable_resource_monitoring, bool)
        assert isinstance(performance.performance_thresholds, dict)

    def test_performance_config_validation(self) -> None:
        """Test performance configuration validation."""
        config = FlextPluginConfig()
        performance = config.performance

        # Test valid memory limit
        performance.max_memory_mb = 512
        assert performance.max_memory_mb == 512

        # Test memory limit too low
        with pytest.raises(ValueError):
            performance.max_memory_mb = 32

        # Test memory limit too high
        with pytest.raises(ValueError):
            performance.max_memory_mb = 2048

        # Test valid CPU percent
        performance.max_cpu_percent = 75
        assert performance.max_cpu_percent == 75

        # Test CPU percent too high
        with pytest.raises(ValueError):
            performance.max_cpu_percent = 150

        # Test CPU percent too low
        with pytest.raises(ValueError):
            performance.max_cpu_percent = -10

    def test_hot_reload_config(self) -> None:
        """Test hot reload configuration section."""
        config = FlextPluginConfig()
        hot_reload = config.hot_reload

        assert isinstance(hot_reload.enabled, bool)
        assert hot_reload.watch_interval > 0
        assert hot_reload.debounce_ms >= 0
        assert hot_reload.max_retries > 0
        assert isinstance(hot_reload.enable_rollback, bool)
        assert isinstance(hot_reload.watch_paths, list)

    def test_hot_reload_config_validation(self) -> None:
        """Test hot reload configuration validation."""
        config = FlextPluginConfig()
        hot_reload = config.hot_reload

        # Test valid watch interval
        hot_reload.watch_interval = 5.0
        assert hot_reload.watch_interval == 5.0

        # Test invalid watch interval
        with pytest.raises(ValueError):
            hot_reload.watch_interval = 0

        with pytest.raises(ValueError):
            hot_reload.watch_interval = -1.0

        # Test valid debounce
        hot_reload.debounce_ms = 1000
        assert hot_reload.debounce_ms == 1000

        # Test invalid debounce
        with pytest.raises(ValueError):
            hot_reload.debounce_ms = -100

    def test_monitoring_config(self) -> None:
        """Test monitoring configuration section."""
        config = FlextPluginConfig()
        monitoring = config.monitoring

        assert isinstance(monitoring.enabled, bool)
        assert isinstance(monitoring.metrics_enabled, bool)
        assert isinstance(monitoring.health_checks_enabled, bool)
        assert isinstance(monitoring.performance_tracking, bool)
        assert isinstance(monitoring.error_tracking, bool)
        assert monitoring.log_level in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        assert 1 <= monitoring.retention_days <= 365

    def test_monitoring_config_validation(self) -> None:
        """Test monitoring configuration validation."""
        config = FlextPluginConfig()
        monitoring = config.monitoring

        # Test valid log level
        monitoring.log_level = "DEBUG"
        assert monitoring.log_level == "DEBUG"

        # Test case insensitive log level
        monitoring.log_level = "debug"
        assert monitoring.log_level == "DEBUG"

        # Test invalid log level
        with pytest.raises(ValueError):
            monitoring.log_level = "INVALID"

        # Test valid retention days
        monitoring.retention_days = 60
        assert monitoring.retention_days == 60

        # Test invalid retention days
        with pytest.raises(ValueError):
            monitoring.retention_days = 0

        with pytest.raises(ValueError):
            monitoring.retention_days = 400

    def test_registry_config(self) -> None:
        """Test registry configuration section."""
        config = FlextPluginConfig()
        registry = config.registry

        assert isinstance(registry.enabled, bool)
        assert registry.registry_url is None or isinstance(registry.registry_url, str)
        assert isinstance(registry.require_authentication, bool)
        assert registry.api_key is None or isinstance(registry.api_key, str)
        assert isinstance(registry.verify_signatures, bool)
        assert isinstance(registry.trusted_publishers, list)
        assert registry.sync_interval > 0

    def test_registry_config_validation(self) -> None:
        """Test registry configuration validation."""
        config = FlextPluginConfig()
        registry = config.registry

        # Test valid sync interval
        registry.sync_interval = 7200
        assert registry.sync_interval == 7200

        # Test invalid sync interval
        with pytest.raises(ValueError):
            registry.sync_interval = 0

        with pytest.raises(ValueError):
            registry.sync_interval = -100

    def test_get_plugin_paths(self) -> None:
        """Test get_plugin_paths method."""
        config = FlextPluginConfig()
        paths = config.get_plugin_paths()

        assert isinstance(paths, list)
        assert len(paths) > 0
        assert all(isinstance(path, str) for path in paths)

    def test_is_security_enabled(self) -> None:
        """Test is_security_enabled method."""
        config = FlextPluginConfig()

        # Test with security features enabled
        config.security.enable_sandboxing = True
        config.security.require_signature_verification = False
        assert config.is_security_enabled() is True

        config.security.enable_sandboxing = False
        config.security.require_signature_verification = True
        assert config.is_security_enabled() is True

        # Test with security features disabled
        config.security.enable_sandboxing = False
        config.security.require_signature_verification = False
        assert config.is_security_enabled() is False

    def test_is_monitoring_enabled(self) -> None:
        """Test is_monitoring_enabled method."""
        config = FlextPluginConfig()

        # Test with monitoring enabled
        config.monitoring.enabled = True
        config.monitoring.metrics_enabled = True
        config.monitoring.health_checks_enabled = True
        config.monitoring.performance_tracking = True
        assert config.is_monitoring_enabled() is True

        # Test with monitoring disabled
        config.monitoring.enabled = False
        assert config.is_monitoring_enabled() is False

        # Test with monitoring enabled but no features
        config.monitoring.enabled = True
        config.monitoring.metrics_enabled = False
        config.monitoring.health_checks_enabled = False
        config.monitoring.performance_tracking = False
        assert config.is_monitoring_enabled() is False

    def test_get_performance_limits(self) -> None:
        """Test get_performance_limits method."""
        config = FlextPluginConfig()
        limits = config.get_performance_limits()

        assert isinstance(limits, dict)
        assert "max_memory_mb" in limits
        assert "max_cpu_percent" in limits
        assert "max_concurrent_plugins" in limits
        assert "max_execution_time" in limits

        assert isinstance(limits["max_memory_mb"], int)
        assert isinstance(limits["max_cpu_percent"], int)
        assert isinstance(limits["max_concurrent_plugins"], int)
        assert isinstance(limits["max_execution_time"], int)

    def test_validate_configuration(self) -> None:
        """Test validate_configuration method."""
        config = FlextPluginConfig()

        # Test valid configuration
        assert config.validate_configuration() is True

        # Test with invalid configuration (this would require mocking)
        # In practice, you would test with actual invalid configurations

    def test_environment_variable_loading(self) -> None:
        """Test loading configuration from environment variables."""
        with patch.dict(
            "os.environ",
            {
                "FLEXT_PLUGIN_DISCOVERY__TIMEOUT_SECONDS": "15",
                "FLEXT_PLUGIN_SECURITY__DEFAULT_LEVEL": "HIGH",
                "FLEXT_PLUGIN_PERFORMANCE__MAX_MEMORY_MB": "1024",
                "FLEXT_PLUGIN_MONITORING__LOG_LEVEL": "DEBUG",
            },
        ):
            config = FlextPluginConfig()

            assert config.discovery.timeout_seconds == 15
            assert config.security.default_level == "HIGH"
            assert config.performance.max_memory_mb == 1024
            assert config.monitoring.log_level == "DEBUG"

    def test_config_sections_are_objects(self) -> None:
        """Test that config sections are proper objects."""
        config = FlextPluginConfig()

        # Test that sections are accessible as attributes
        assert hasattr(config, "discovery")
        assert hasattr(config, "security")
        assert hasattr(config, "performance")
        assert hasattr(config, "hot_reload")
        assert hasattr(config, "monitoring")
        assert hasattr(config, "registry")

        # Test that sections have their own attributes
        assert hasattr(config.discovery, "plugin_paths")
        assert hasattr(config.security, "default_level")
        assert hasattr(config.performance, "max_memory_mb")
        assert hasattr(config.hot_reload, "enabled")
        assert hasattr(config.monitoring, "enabled")
        assert hasattr(config.registry, "enabled")

    def test_config_immutability(self) -> None:
        """Test that config values can be modified but structure is consistent."""
        config = FlextPluginConfig()

        # Test that we can modify values
        original_timeout = config.discovery.timeout_seconds
        config.discovery.timeout_seconds = 20
        assert config.discovery.timeout_seconds == 20

        # Test that we can reset
        config.discovery.timeout_seconds = original_timeout
        assert config.discovery.timeout_seconds == original_timeout

    def test_config_defaults_consistency(self) -> None:
        """Test that default values are consistent and reasonable."""
        config = FlextPluginConfig()

        # Test discovery defaults
        assert config.discovery.timeout_seconds > 0
        assert config.discovery.enable_validation is True
        assert config.discovery.enable_security_scan is True

        # Test security defaults
        assert config.security.default_level in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
        assert config.security.enable_sandboxing is True
        assert config.security.require_signature_verification is False

        # Test performance defaults
        assert config.performance.max_memory_mb > 0
        assert 0 <= config.performance.max_cpu_percent <= 100
        assert config.performance.max_concurrent_plugins > 0

        # Test hot reload defaults
        assert config.hot_reload.watch_interval > 0
        assert config.hot_reload.debounce_ms >= 0
        assert config.hot_reload.max_retries > 0

        # Test monitoring defaults
        assert config.monitoring.log_level in {
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
        }
        assert 1 <= config.monitoring.retention_days <= 365

        # Test registry defaults
        assert config.registry.sync_interval > 0
