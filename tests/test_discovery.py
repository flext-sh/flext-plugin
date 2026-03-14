"""Test suite for flext_plugin.discovery module.

Tests the FlextPluginDiscovery class with actual functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

from flext_plugin import FlextPluginDiscovery, FlextPluginModels


class TestFlextPluginDiscovery:
    """Tests for FlextPluginDiscovery class."""

    @pytest.fixture
    def temp_dir(self) -> Generator[Path]:
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    @pytest.fixture
    def discovery(self) -> FlextPluginDiscovery:
        """Create FlextPluginDiscovery instance for testing."""
        return FlextPluginDiscovery()

    def test_discovery_initialization(self, discovery: FlextPluginDiscovery) -> None:
        """Test discovery initialization."""
        assert discovery is not None
        assert hasattr(discovery, "logger")
        assert hasattr(discovery, "strategies")
        assert len(discovery.strategies) == 2

    def test_discover_plugins_empty_paths(
        self, discovery: FlextPluginDiscovery
    ) -> None:
        """Test discover_plugins with empty paths."""
        result = discovery.discover_plugins(paths=[])
        assert result.is_success
        assert result.value is not None
        assert len(result.value) == 0

    def test_discover_plugins_nonexistent_path(
        self, discovery: FlextPluginDiscovery
    ) -> None:
        """Test discover_plugins with nonexistent path."""
        result = discovery.discover_plugins(paths=["/nonexistent/path"])
        assert result.is_success
        assert result.value is not None

    def test_discover_plugins_with_temp_directory(
        self, discovery: FlextPluginDiscovery, temp_dir: Path
    ) -> None:
        """Test discover_plugins with actual temporary directory."""
        result = discovery.discover_plugins(paths=[str(temp_dir)])
        assert result.is_success
        assert result.value is not None
        assert isinstance(result.value, list)

    def test_discover_plugin_nonexistent(self, discovery: FlextPluginDiscovery) -> None:
        """Test discover_plugin with nonexistent path."""
        result = discovery.discover_plugin(plugin_path="/nonexistent/plugin")
        assert result.is_failure or (result.is_success and result.value is None)

    def test_validate_plugin_none_data(self, discovery: FlextPluginDiscovery) -> None:
        """Test validate_plugin with None data."""
        plugin_data = FlextPluginModels.Plugin.DiscoveryData(
            name="test_plugin",
            version="1.0.0",
            path=Path("test_path"),
            discovery_type="file",
            discovery_method="file_system",
        )
        result = discovery.validate_plugin(plugin_data=plugin_data)
        assert result.is_success
