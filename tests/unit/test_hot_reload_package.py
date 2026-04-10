"""Test suite for flext_plugin.hot_reload package.

Tests the actual FlextPluginHotReload class that exists in the codebase.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_plugin import FlextPluginHotReload


class TestHotReloadPackage:
    """Tests for FlextPluginHotReload package functionality."""

    def test_hot_reload_class_exists(self) -> None:
        """Test that FlextPluginHotReload class exists and is callable."""
        assert FlextPluginHotReload is not None
        assert callable(FlextPluginHotReload)

    def test_hot_reload_instantiation(self) -> None:
        """Test that FlextPluginHotReload can be instantiated."""
        instance = FlextPluginHotReload()
        assert instance is not None
