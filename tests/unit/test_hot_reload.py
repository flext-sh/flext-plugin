"""Test suite for flext_plugin.hot_reload module.

Tests the actual FlextPluginHotReload class that exists in the codebase.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_plugin import FlextPluginHotReload


class TestsFlextPluginHotReload:
    """Tests for FlextPluginHotReload class."""

    @pytest.fixture
    def hot_reload(self) -> FlextPluginHotReload:
        """Create hot reload instance for testing."""
        return FlextPluginHotReload()

    def test_initialization(self, hot_reload: FlextPluginHotReload) -> None:
        """Test hot reload initialization."""
        assert hot_reload is not None

    def test_class_exists(self) -> None:
        """Test that FlextPluginHotReload class exists and is callable."""
        assert FlextPluginHotReload is not None
        assert callable(FlextPluginHotReload)
