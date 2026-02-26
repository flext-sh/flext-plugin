"""Test suite for flext_plugin.loader module.

Tests the actual FlextPluginLoader class that exists in the codebase.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_plugin import FlextPluginLoader
from flext_plugin.adapters import FlextPluginAdapters


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


class TestDynamicLoaderAdapter:
    """Tests for DynamicLoaderAdapter class."""

    @pytest.fixture
    def plugin_file(self, tmp_path: Path) -> Path:
        plugin_path = tmp_path / "sample_plugin.py"
        _ = plugin_path.write_text(
            "__version__ = '1.0.0'\ndef run():\n    return 'ok'\n",
        )
        return plugin_path

    def test_tracks_loaded_plugin_state(self, plugin_file: Path) -> None:
        adapter = FlextPluginAdapters.DynamicLoaderAdapter()

        load_result = adapter.load_plugin(str(plugin_file))

        assert load_result.is_success
        assert adapter.is_plugin_loaded("sample_plugin") is True
        assert "sample_plugin" in adapter.get_loaded_plugins()

    def test_unload_plugin_returns_failure_when_missing(self) -> None:
        adapter = FlextPluginAdapters.DynamicLoaderAdapter()

        unload_result = adapter.unload_plugin("missing")

        assert unload_result.is_failure
        assert "Plugin not loaded: missing" in str(unload_result.error)

    def test_unload_plugin_removes_loaded_plugin(self, plugin_file: Path) -> None:
        adapter = FlextPluginAdapters.DynamicLoaderAdapter()
        _ = adapter.load_plugin(str(plugin_file))

        unload_result = adapter.unload_plugin("sample_plugin")

        assert unload_result.is_success
        assert unload_result.value is True
        assert adapter.is_plugin_loaded("sample_plugin") is False
