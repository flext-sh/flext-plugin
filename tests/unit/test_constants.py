"""Unit tests for FlextPluginConstants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import tm

from tests import c


class TestsFlextPluginConstantsUnit:
    """Test cases for FlextPluginConstants."""

    def test_constants_initialization(self) -> None:
        """Test that constants can be initialized."""
        constants = c()
        assert constants is not None

    def test_types_constants(self) -> None:
        """Test plugin type constants."""
        tm.that(c.Plugin.SINGER_PLUGIN_TYPES, none=False)
        tm.that(
            c.Plugin.ARCHITECTURE_PLUGIN_TYPES,
            none=False,
        )
        tm.that(c.Plugin.INTEGRATION_PLUGIN_TYPES, none=False)
        tm.that(c.Plugin.UTILITY_PLUGIN_TYPES, none=False)
        tm.that(c.Plugin.ALL_PLUGIN_TYPES, none=False)

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

    def test_plugin_type_consistency(self) -> None:
        """Test that plugin types are consistent across constants."""
        all_types = c.Plugin.ALL_PLUGIN_TYPES
        singer_types = c.Plugin.SINGER_PLUGIN_TYPES
        arch_types = c.Plugin.ARCHITECTURE_PLUGIN_TYPES
        integration_types = c.Plugin.INTEGRATION_PLUGIN_TYPES
        utility_types = c.Plugin.UTILITY_PLUGIN_TYPES
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
