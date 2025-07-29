"""Simple tests for flext_plugin.core.discovery module.

Tests for plugin discovery functionality using only real methods.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from flext_plugin.core.discovery import PluginDiscovery
from flext_plugin.core.types import PluginType


class TestPluginDiscoverySimple:
    """Test PluginDiscovery functionality with real methods only."""

    @pytest.fixture
    def discovery(self) -> PluginDiscovery:
        """Create plugin discovery instance for testing."""
        return PluginDiscovery()

    def test_discovery_initialization(self, discovery: PluginDiscovery) -> None:
        """Test plugin discovery initialization."""
        assert discovery is not None
        assert hasattr(discovery, "plugin_directories")
        assert isinstance(discovery.plugin_directories, list)

    def test_add_plugin_directory(self, discovery: PluginDiscovery) -> None:
        """Test adding plugin directory."""
        test_dir = Path("/test/plugins")
        initial_count = len(discovery.plugin_directories)

        discovery.add_plugin_directory(test_dir)

        if len(discovery.plugin_directories) != initial_count + 1:

            raise AssertionError(f"Expected
            {initial_count + 1}, got {len(discovery.plugin_directories)}")
        if test_dir not in discovery.plugin_directories:
            raise AssertionError(f"Expected {test_dir} in {discovery.plugin_directories}")

    def test_add_duplicate_plugin_directory(self, discovery: PluginDiscovery) -> None:
        """Test adding duplicate plugin directory."""
        test_dir = Path("/test/plugins")

        discovery.add_plugin_directory(test_dir)
        initial_count = len(discovery.plugin_directories)

        # Add same directory again
        discovery.add_plugin_directory(test_dir)

        # Should not increase count
        if len(discovery.plugin_directories) != initial_count:
            raise AssertionError(f"Expected {initial_count}, got {len(discovery.plugin_directories)}")

    def test_blacklist_plugin(self, discovery: PluginDiscovery) -> None:
        """Test blacklisting a plugin."""
        plugin_id = "test-plugin"

        # Initially not blacklisted
        assert not discovery.is_blacklisted(plugin_id)

        # Blacklist the plugin
        discovery.blacklist_plugin(plugin_id)

        # Now should be blacklisted
        assert discovery.is_blacklisted(plugin_id)

    async def test_discover_all_empty(self, discovery: PluginDiscovery) -> None:
        """Test discovering plugins when no plugins exist."""
        # Clear plugin directories to avoid actual discovery
        discovery.plugin_directories = []

        with patch("importlib.metadata.entry_points", return_value=[]):
            result = await discovery.discover_all()

            # Should return empty dict when no plugins found
            if result != {}:
                raise AssertionError(f"Expected {{}}, got {result}")

    async def test_discover_by_type(self, discovery: PluginDiscovery) -> None:
        """Test discovering plugins by type."""
        plugin_type = PluginType.TAP

        # Mock the discover_all method to return empty results
        with patch.object(discovery, "discover_all", return_value={}):
            result = await discovery.discover_by_type(plugin_type)
            if result != {}:
                raise AssertionError(f"Expected {{}}, got {result}")

    def test_get_discovered_plugin_not_found(self, discovery: PluginDiscovery) -> None:
        """Test getting discovered plugin that doesn't exist."""
        result = discovery.get_discovered_plugin("nonexistent")
        assert result is None

    def test_validate_plugin_class_valid(self, discovery: PluginDiscovery) -> None:
        """Test validating valid plugin class."""
        # Create mock plugin class
        mock_plugin_class = Mock()
        mock_plugin_class.__name__ = "TestPlugin"
        mock_plugin_class.METADATA = Mock()

        # Mock issubclass to return True and add required methods
        with patch("flext_plugin.core.discovery.issubclass", return_value=True):
            # Mock required methods
            for method in ["initialize", "cleanup", "health_check", "execute"]:
                setattr(mock_plugin_class, method, Mock())

            result = discovery._validate_plugin_class(mock_plugin_class)
            if not (result):
                raise AssertionError(f"Expected True, got {result}")

    def test_validate_plugin_class_invalid_not_subclass(
        self,
        discovery: PluginDiscovery,
    ) -> None:
        """Test validating invalid plugin class - not a Plugin subclass."""
        mock_class = Mock()
        mock_class.__name__ = "NotAPlugin"

        with patch("flext_plugin.core.discovery.issubclass", return_value=False):
            result = discovery._validate_plugin_class(mock_class)
            if result:
                raise AssertionError(f"Expected False, got {result}")

    def test_validate_plugin_class_missing_metadata(
        self,
        discovery: PluginDiscovery,
    ) -> None:
        """Test validating plugin class missing metadata."""
        mock_plugin_class = Mock()
        mock_plugin_class.__name__ = "TestPlugin"

        # Mock hasattr to return False for METADATA
        with (
            patch("flext_plugin.core.discovery.issubclass", return_value=True),
            patch("builtins.hasattr") as mock_hasattr,
        ):
            # Return False for METADATA check, True for method checks
            def hasattr_side_effect(_obj: object, attr: str) -> bool:
                if attr == "METADATA":
                    return False
                return attr in {"initialize", "cleanup", "health_check", "execute"}

            mock_hasattr.side_effect = hasattr_side_effect

            result = discovery._validate_plugin_class(mock_plugin_class)
            if result:
                raise AssertionError(f"Expected False, got {result}")

    def test_register_plugin_manually(self, discovery: PluginDiscovery) -> None:
        """Test manually registering a plugin."""
        # Create mock plugin class
        mock_plugin_class = Mock()
        mock_plugin_class.__name__ = "TestPlugin"
        mock_plugin_class.METADATA = Mock()
        mock_plugin_class.METADATA.name = "test-plugin"

        # Mock validation to pass
        with patch.object(discovery, "_validate_plugin_class", return_value=True):
            # Should not raise an error
            discovery.register_plugin(mock_plugin_class)

            # Plugin should be discoverable
            result = discovery.get_discovered_plugin("test-plugin")
            assert result is not None
            if result.metadata.name != "test-plugin":
                raise AssertionError(f"Expected {"test-plugin"}, got {result.metadata.name}")

    async def test_discover_entry_points_empty(
        self,
        discovery: PluginDiscovery,
    ) -> None:
        """Test discovering entry points when none exist."""
        with patch("importlib.metadata.entry_points", return_value=[]):
            # Should not raise an error
            await discovery._discover_entry_points()

            # Should complete without errors
            assert True

    async def test_discover_file_system_no_directories(
        self,
        discovery: PluginDiscovery,
    ) -> None:
        """Test file system discovery with no directories."""
        # Clear plugin directories
        discovery.plugin_directories = []

        # Should not raise an error
        await discovery._discover_file_system()

        # Should complete without errors
        assert True

    async def test_discover_file_system_nonexistent_dir(
        self,
        discovery: PluginDiscovery,
    ) -> None:
        """Test file system discovery with non-existent directory."""
        test_dir = Path("/nonexistent/plugins")
        discovery.plugin_directories = [test_dir]

        # Should not raise an error even with non-existent directory
        await discovery._discover_file_system()

        # Should complete without errors
        assert True
