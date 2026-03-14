"""Unit tests for FlextPluginConstants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext_plugin import FlextPluginConstants


class TestFlextPluginConstants:
    """Test cases for FlextPluginConstants."""

    def test_constants_initialization(self) -> None:
        """Test that constants can be initialized."""
        constants = FlextPluginConstants()
        assert constants is not None

    def test_discovery_constants(self) -> None:
        """Test discovery-related constants."""
        assert FlextPluginConstants.Plugin.Discovery.DEFAULT_TIMEOUT_SECONDS > 0
        assert FlextPluginConstants.Plugin.Discovery.DISCOVERY_TIMEOUT_SECONDS > 0
        assert len(FlextPluginConstants.Plugin.Discovery.DEFAULT_PLUGIN_PATHS) > 0
        assert FlextPluginConstants.Plugin.Discovery.MIN_PLUGIN_NAME_LENGTH > 0
        assert FlextPluginConstants.Plugin.Discovery.MAX_PLUGIN_NAME_LENGTH > 0
        assert FlextPluginConstants.Plugin.Discovery.VALID_PLUGIN_NAME_PATTERN

    def test_types_constants(self) -> None:
        """Test plugin type constants."""
        assert len(FlextPluginConstants.Plugin.Types.SINGER_PLUGIN_TYPES) > 0
        assert len(FlextPluginConstants.Plugin.Types.ARCHITECTURE_PLUGIN_TYPES) > 0
        assert len(FlextPluginConstants.Plugin.Types.INTEGRATION_PLUGIN_TYPES) > 0
        assert len(FlextPluginConstants.Plugin.Types.UTILITY_PLUGIN_TYPES) > 0
        assert len(FlextPluginConstants.Plugin.Types.ALL_PLUGIN_TYPES) > 0

    def test_lifecycle_constants(self) -> None:
        """Test lifecycle-related constants."""
        assert len(FlextPluginConstants.Plugin.Lifecycle.PLUGIN_LIFECYCLE_STATES) > 0
        assert FlextPluginConstants.Plugin.Lifecycle.MAX_PLUGIN_WORKERS > 0
        assert FlextPluginConstants.Plugin.Lifecycle.MIN_PLUGIN_WORKERS >= 0
        assert FlextPluginConstants.Plugin.Lifecycle.DEFAULT_WORKERS > 0

    def test_hot_reload_constants(self) -> None:
        """Test hot reload constants."""
        assert FlextPluginConstants.Plugin.HotReload.DEFAULT_INTERVAL_SECONDS > 0
        assert FlextPluginConstants.Plugin.HotReload.DEBOUNCE_MS >= 0
        assert FlextPluginConstants.Plugin.HotReload.MAX_RETRIES > 0

    def test_files_constants(self) -> None:
        """Test file-related constants."""
        assert FlextPluginConstants.Plugin.Files.PYTHON_EXTENSION
        assert FlextPluginConstants.Plugin.Files.YAML_CONFIG_EXTENSION
        assert FlextPluginConstants.Plugin.Files.JSON_CONFIG_EXTENSION
        assert FlextPluginConstants.Plugin.Files.TOML_CONFIG_EXTENSION
        assert FlextPluginConstants.Plugin.Files.DEFAULT_PLUGIN_DIR
        assert FlextPluginConstants.Plugin.Files.DEFAULT_CACHE_DIR
        assert FlextPluginConstants.Plugin.Files.DEFAULT_CONFIG_DIR

    def test_plugin_messages_constants(self) -> None:
        """Test plugin message constants."""
        assert FlextPluginConstants.Plugin.PluginMessages.PLUGIN_NOT_FOUND
        assert FlextPluginConstants.Plugin.PluginMessages.PLUGIN_ALREADY_EXISTS
        assert FlextPluginConstants.Plugin.PluginMessages.PLUGIN_LOAD_FAILED
        assert FlextPluginConstants.Plugin.PluginMessages.PLUGIN_INVALID_NAME
        assert FlextPluginConstants.Plugin.PluginMessages.PLUGIN_LOADED_SUCCESS
        assert FlextPluginConstants.Plugin.PluginMessages.PLUGIN_ACTIVATED_SUCCESS

    def test_plugin_security_constants(self) -> None:
        """Test plugin security constants."""
        assert len(FlextPluginConstants.Plugin.PluginSecurity.SECURITY_LEVELS) > 0
        assert FlextPluginConstants.Plugin.PluginSecurity.DEFAULT_SECURITY_LEVEL
        assert FlextPluginConstants.Plugin.PluginSecurity.SECURITY_SCAN_TIMEOUT > 0

    def test_plugin_performance_constants(self) -> None:
        """Test plugin performance constants."""
        assert FlextPluginConstants.Plugin.PluginPerformance.PERCENTAGE_MAX == 100
        assert FlextPluginConstants.Plugin.PluginPerformance.PERCENTAGE_MIN == 0
        assert FlextPluginConstants.Plugin.PluginPerformance.EXCELLENT_SUCCESS_RATE > 0
        assert FlextPluginConstants.Plugin.PluginPerformance.GOOD_SUCCESS_RATE > 0
        assert FlextPluginConstants.Plugin.PluginPerformance.FAIR_SUCCESS_RATE > 0
        assert FlextPluginConstants.Plugin.PluginPerformance.EXCELLENT_TIME_MS > 0
        assert FlextPluginConstants.Plugin.PluginPerformance.GOOD_TIME_MS > 0
        assert FlextPluginConstants.Plugin.PluginPerformance.FAIR_TIME_MS > 0
        assert (
            FlextPluginConstants.Plugin.PluginPerformance.EXECUTION_TIME_SCALE_MS_TO_S
            == 1000
        )
        assert FlextPluginConstants.Plugin.PluginPerformance.READY_TIMEOUT_SECONDS > 0
        assert FlextPluginConstants.Plugin.PluginPerformance.READY_MAX_MEMORY_MB > 0
        assert (
            FlextPluginConstants.Plugin.PluginPerformance.MAX_CONCURRENT_LOADS_WARNING_THRESHOLD
            > 0
        )
        assert FlextPluginConstants.Plugin.PluginPerformance.MINIMUM_MEMORY_LIMIT_MB > 0
        assert (
            FlextPluginConstants.Plugin.PluginPerformance.MAXIMUM_EXECUTION_TIMEOUT_SECONDS
            > 0
        )

    def test_constants_immutability(self) -> None:
        """Test that constants are immutable."""
        assert isinstance(
            FlextPluginConstants.Plugin.Discovery.DEFAULT_TIMEOUT_SECONDS, int
        )
        assert isinstance(
            FlextPluginConstants.Plugin.Discovery.DISCOVERY_TIMEOUT_SECONDS, int
        )
        assert isinstance(
            FlextPluginConstants.Plugin.HotReload.DEFAULT_INTERVAL_SECONDS, int
        )
        assert isinstance(
            FlextPluginConstants.Plugin.PluginPerformance.PERCENTAGE_MAX, int
        )

    def test_plugin_type_consistency(self) -> None:
        """Test that plugin types are consistent across constants."""
        all_types = FlextPluginConstants.Plugin.Types.ALL_PLUGIN_TYPES
        singer_types = FlextPluginConstants.Plugin.Types.SINGER_PLUGIN_TYPES
        arch_types = FlextPluginConstants.Plugin.Types.ARCHITECTURE_PLUGIN_TYPES
        integration_types = FlextPluginConstants.Plugin.Types.INTEGRATION_PLUGIN_TYPES
        utility_types = FlextPluginConstants.Plugin.Types.UTILITY_PLUGIN_TYPES
        assert singer_types.issubset(all_types)
        assert arch_types.issubset(all_types)
        assert integration_types.issubset(all_types)
        assert utility_types.issubset(all_types)
        assert singer_types.isdisjoint(arch_types)
        assert singer_types.isdisjoint(integration_types)
        assert singer_types.isdisjoint(utility_types)
        assert arch_types.isdisjoint(integration_types)
        assert arch_types.isdisjoint(utility_types)
        assert integration_types.isdisjoint(utility_types)

    def test_security_levels_consistency(self) -> None:
        """Test that security levels are consistent."""
        security_levels = FlextPluginConstants.Plugin.PluginSecurity.SECURITY_LEVELS
        default_level = (
            FlextPluginConstants.Plugin.PluginSecurity.DEFAULT_SECURITY_LEVEL
        )
        assert default_level in security_levels
        assert len(security_levels) == 4
        assert "LOW" in security_levels
        assert "MEDIUM" in security_levels
        assert "HIGH" in security_levels
        assert "CRITICAL" in security_levels

    def test_lifecycle_states_consistency(self) -> None:
        """Test that lifecycle states are consistent."""
        states = FlextPluginConstants.Plugin.Lifecycle.PLUGIN_LIFECYCLE_STATES
        expected_states = {
            "unknown",
            "discovered",
            "loaded",
            "active",
            "inactive",
            "loading",
            "error",
            "disabled",
            "healthy",
            "unhealthy",
        }
        assert states == expected_states
        assert len(states) == 10
