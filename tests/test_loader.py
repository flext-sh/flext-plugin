"""Test suite for flext_plugin.loader module.

Tests the actual FlextPluginLoader class that exists in the codebase.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_plugin import FlextPluginLoader


class TestFlextPluginLoader:
    """Tests for FlextPluginLoader class."""

    @pytest.fixture
    def loader(self) -> FlextPluginLoader:
        """Create loader instance for testing."""
        return FlextPluginLoader()

    def test_initialization(self, loader: FlextPluginLoader) -> None:
        """Test loader initialization."""
        assert loader is not None
        assert hasattr(loader, "logger")

    def test_class_exists(self) -> None:
        """Test that FlextPluginLoader class exists and is callable."""
        assert FlextPluginLoader is not None
        assert callable(FlextPluginLoader)
