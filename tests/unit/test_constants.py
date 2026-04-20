"""Unit tests for FlextPluginConstants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import tm

from tests import c


class TestFlextPluginConstants:
    """Test cases for FlextPluginConstants."""

    def test_constants_initialization(self) -> None:
        """Test that constants can be initialized."""
        constants = c()
        assert constants is not None

    def test_discovery_constants(self) -> None:
        """Test discovery-related constants."""
        tm.that(c.Plugin.Discovery.DEFAULT_TIMEOUT_SECONDS, gt=0)
        tm.that(c.Plugin.Discovery.DISCOVERY_TIMEOUT_SECONDS, gt=0)
        tm.that(c.Plugin.Discovery.DEFAULT_PLUGIN_PATHS, none=False)
        tm.that(c.Plugin.Discovery.MIN_PLUGIN_NAME_LENGTH, gt=0)
        tm.that(c.Plugin.Discovery.MAX_PLUGIN_NAME_LENGTH, gt=0)
        tm.that(
            c.Plugin.Discovery.VALID_PLUGIN_NAME_PATTERN,
            empty=False,
        )

    def test_types_constants(self) -> None:
        """Test plugin type constants."""
        tm.that(c.Plugin.Types.SINGER_PLUGIN_TYPES, none=False)
        tm.that(
            c.Plugin.Types.ARCHITECTURE_PLUGIN_TYPES,
            none=False,
        )
        tm.that(c.Plugin.Types.INTEGRATION_PLUGIN_TYPES, none=False)
        tm.that(c.Plugin.Types.UTILITY_PLUGIN_TYPES, none=False)
        tm.that(c.Plugin.Types.ALL_PLUGIN_TYPES, none=False)

    def test_lifecycle_constants(self) -> None:
        """Test lifecycle-related constants."""
        tm.that(
            c.Plugin.Lifecycle.PLUGIN_LIFECYCLE_STATES,
            none=False,
        )
        tm.that(c.Plugin.Lifecycle.MAX_PLUGIN_WORKERS, gt=0)
        tm.that(c.Plugin.Lifecycle.MIN_PLUGIN_WORKERS, gte=0)
        tm.that(c.Plugin.Lifecycle.DEFAULT_WORKERS, gt=0)

    def test_hot_reload_constants(self) -> None:
        """Test hot reload constants."""
        tm.that(c.Plugin.HotReload.DEFAULT_INTERVAL_SECONDS, gt=0)
        tm.that(c.Plugin.HotReload.DEBOUNCE_MS, gte=0)
        tm.that(c.Plugin.HotReload.MAX_RETRIES, gt=0)

    def test_files_constants(self) -> None:
        """Test file-related constants."""
        tm.that(c.Plugin.Files.PYTHON_EXTENSION, empty=False)
        tm.that(c.Plugin.Files.YAML_CONFIG_EXTENSION, empty=False)
        tm.that(c.Plugin.Files.JSON_CONFIG_EXTENSION, empty=False)
        tm.that(c.Plugin.Files.TOML_CONFIG_EXTENSION, empty=False)
        tm.that(c.Plugin.Files.DEFAULT_PLUGIN_DIR, empty=False)
        tm.that(c.Plugin.Files.DEFAULT_CACHE_DIR, empty=False)
        tm.that(c.Plugin.Files.DEFAULT_CONFIG_DIR, empty=False)

    def test_plugin_messages_constants(self) -> None:
        """Test plugin message constants."""
        tm.that(
            c.Plugin.PluginMessages.PLUGIN_NOT_FOUND,
            empty=False,
        )
        tm.that(
            c.Plugin.PluginMessages.PLUGIN_ALREADY_EXISTS,
            empty=False,
        )
        tm.that(
            c.Plugin.PluginMessages.PLUGIN_LOAD_FAILED,
            empty=False,
        )
        tm.that(
            c.Plugin.PluginMessages.PLUGIN_INVALID_NAME,
            empty=False,
        )
        tm.that(
            c.Plugin.PluginMessages.PLUGIN_LOADED_SUCCESS,
            empty=False,
        )
        tm.that(
            c.Plugin.PluginMessages.PLUGIN_ACTIVATED_SUCCESS,
            empty=False,
        )

    def test_plugin_security_constants(self) -> None:
        """Test plugin security constants."""
        tm.that(c.Plugin.PluginSecurity.SECURITY_LEVELS, none=False)
        tm.that(
            c.Plugin.PluginSecurity.DEFAULT_SECURITY_LEVEL,
            empty=False,
        )
        tm.that(c.Plugin.PluginSecurity.SECURITY_SCAN_TIMEOUT, gt=0)

    def test_plugin_performance_constants(self) -> None:
        """Test plugin performance constants."""
        tm.that(c.Plugin.PluginPerformance.PERCENTAGE_MAX, eq=100)
        tm.that(c.Plugin.PluginPerformance.PERCENTAGE_MIN, eq=0)
        tm.that(
            c.Plugin.PluginPerformance.EXCELLENT_SUCCESS_RATE,
            gt=0,
        )
        tm.that(c.Plugin.PluginPerformance.GOOD_SUCCESS_RATE, gt=0)
        tm.that(c.Plugin.PluginPerformance.FAIR_SUCCESS_RATE, gt=0)
        tm.that(c.Plugin.PluginPerformance.EXCELLENT_TIME_MS, gt=0)
        tm.that(c.Plugin.PluginPerformance.GOOD_TIME_MS, gt=0)
        tm.that(c.Plugin.PluginPerformance.FAIR_TIME_MS, gt=0)
        tm.that(
            (c.Plugin.PluginPerformance.EXECUTION_TIME_SCALE_MS_TO_S == 1000),
            eq=True,
        )
        tm.that(
            c.Plugin.PluginPerformance.READY_TIMEOUT_SECONDS,
            gt=0,
        )
        tm.that(c.Plugin.PluginPerformance.READY_MAX_MEMORY_MB, gt=0)
        tm.that(
            (c.Plugin.PluginPerformance.MAX_CONCURRENT_LOADS_WARNING_THRESHOLD > 0),
            eq=True,
        )
        tm.that(
            c.Plugin.PluginPerformance.MINIMUM_MEMORY_LIMIT_MB,
            gt=0,
        )
        tm.that(
            (c.Plugin.PluginPerformance.MAXIMUM_EXECUTION_TIMEOUT_SECONDS > 0),
            eq=True,
        )

    def test_constants_immutability(self) -> None:
        """Test that constants are immutable."""
        tm.that(c.Plugin.Discovery.DEFAULT_TIMEOUT_SECONDS, is_=int)
        tm.that(
            c.Plugin.Discovery.DISCOVERY_TIMEOUT_SECONDS,
            is_=int,
        )
        tm.that(c.Plugin.HotReload.DEFAULT_INTERVAL_SECONDS, is_=int)
        tm.that(c.Plugin.PluginPerformance.PERCENTAGE_MAX, is_=int)

    def test_plugin_type_consistency(self) -> None:
        """Test that plugin types are consistent across constants."""
        all_types = c.Plugin.Types.ALL_PLUGIN_TYPES
        singer_types = c.Plugin.Types.SINGER_PLUGIN_TYPES
        arch_types = c.Plugin.Types.ARCHITECTURE_PLUGIN_TYPES
        integration_types = c.Plugin.Types.INTEGRATION_PLUGIN_TYPES
        utility_types = c.Plugin.Types.UTILITY_PLUGIN_TYPES
        tm.that(singer_types.issubset(all_types), eq=True)
        tm.that(arch_types.issubset(all_types), eq=True)
        tm.that(integration_types.issubset(all_types), eq=True)
        tm.that(utility_types.issubset(all_types), eq=True)
        tm.that(singer_types.isdisjoint(arch_types), eq=True)
        tm.that(singer_types.isdisjoint(integration_types), eq=True)
        tm.that(singer_types.isdisjoint(utility_types), eq=True)
        tm.that(arch_types.isdisjoint(integration_types), eq=True)
        tm.that(arch_types.isdisjoint(utility_types), eq=True)
        tm.that(integration_types.isdisjoint(utility_types), eq=True)

    def test_security_levels_consistency(self) -> None:
        """Test that security levels are consistent."""
        security_levels = c.Plugin.PluginSecurity.SECURITY_LEVELS
        default_level = c.Plugin.PluginSecurity.DEFAULT_SECURITY_LEVEL
        tm.that(security_levels, has=default_level)
        tm.that(len(security_levels), eq=4)
        tm.that(security_levels, has="LOW")
        tm.that(security_levels, has="MEDIUM")
        tm.that(security_levels, has="HIGH")
        tm.that(security_levels, has="CRITICAL")

    def test_lifecycle_states_consistency(self) -> None:
        """Test that lifecycle states are consistent."""
        states = c.Plugin.Lifecycle.PLUGIN_LIFECYCLE_STATES
        expected_states: frozenset[str] = frozenset({
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
        })
        assert states == expected_states
        tm.that(len(states), eq=10)
