"""Simplified test suite for flext_plugin.core.discovery module.

This test module provides streamlined validation of plugin discovery functionality
using real method calls without extensive mocking, focusing on actual behavior
validation and integration testing with the core discovery system.

Test Philosophy:
    - Minimal mocking to validate real system behavior
    - Focus on public API contract validation
    - Integration testing with actual discovery methods
    - Error condition testing with realistic scenarios

Test Coverage:
    - Plugin discovery initialization and configuration
    - Directory management with duplicate handling
    - Plugin blacklisting and filtering mechanisms
    - Entry point and file system discovery patterns
    - Plugin validation with various error conditions
    - Manual plugin registration and retrieval

Testing Approach:
    - Real method calls where possible to validate actual behavior
    - Strategic mocking only for external dependencies
    - Comprehensive error condition validation
    - Performance validation for discovery operations

Integration Focus:
    - Built on flext-core foundation patterns
    - Validates actual plugin discovery workflows
    - Tests real plugin lifecycle integration
    - Ensures compatibility with FLEXT plugin ecosystem
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from flext_plugin import PluginDiscovery, PluginType


class TestPluginDiscoverySimple:
    """Simplified test suite for PluginDiscovery with minimal mocking approach.

    This test class validates plugin discovery functionality using real method
    calls wherever possible, providing integration-focused testing that validates
    actual system behavior rather than mocked interactions.

    Testing Strategy:
      - Real Method Calls: Uses actual discovery methods for authentic validation
      - Minimal Mocking: Only mocks external dependencies like file system
      - Integration Focus: Tests complete workflows from discovery to retrieval
      - Error Resilience: Validates graceful handling of various error conditions

    Test Categories:
      - Core Functionality: Initialization, directory management, discovery
      - Blacklist Management: Plugin filtering and blacklist state validation
      - Validation Logic: Plugin class validation with various scenarios
      - Discovery Methods: Entry point and file system discovery testing
      - Error Handling: Non-existent directories, invalid plugins, missing metadata

    Architecture Validation:
      - Clean Architecture: Tests domain logic without infrastructure mocking
      - Real Integration: Validates actual plugin discovery workflows
      - Performance: Tests discovery operations with realistic scenarios
      - Compatibility: Ensures integration with broader FLEXT ecosystem
    """

    @pytest.fixture
    def discovery(self) -> PluginDiscovery:
        """Create clean PluginDiscovery instance for integration testing.

        Provides a fresh discovery instance for each test with real initialization,
        allowing validation of actual system behavior without pre-configured state.

        Returns:
            PluginDiscovery: Real instance with clean state for testing

        """
        return PluginDiscovery(entity_id="test-simple-discovery-001")

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
            expected_count = initial_count + 1
            actual_count = len(discovery.plugin_directories)
            raise AssertionError(f"Expected {expected_count}, got {actual_count}")
        if test_dir not in discovery.plugin_directories:
            raise AssertionError(
                f"Expected {test_dir} in {discovery.plugin_directories}",
            )

    def test_add_duplicate_plugin_directory(self, discovery: PluginDiscovery) -> None:
        """Validate duplicate plugin directory handling and deduplication logic.

        Tests the discovery system's ability to handle duplicate directory additions
        gracefully, ensuring no duplicate entries are created in the directory list.

        Test Scenario:
            - Add plugin directory to discovery system
            - Record current directory count
            - Add same directory again (duplicate)
            - Verify count remains unchanged

        Validates:
            - Duplicate directories don't increase directory count
            - Directory deduplication works correctly
            - System maintains clean directory list
        """
        test_dir = Path("/test/plugins")

        discovery.add_plugin_directory(test_dir)
        initial_count = len(discovery.plugin_directories)

        # Add same directory again
        discovery.add_plugin_directory(test_dir)

        # Should not increase count
        if len(discovery.plugin_directories) != initial_count:
            raise AssertionError(
                f"Expected {initial_count}, got {len(discovery.plugin_directories)}",
            )

    def test_blacklist_plugin(self, discovery: PluginDiscovery) -> None:
        """Test blacklisting a plugin."""
        plugin_id = "test-plugin"

        # Initially not blacklisted
        assert not discovery.is_blacklisted(plugin_id)

        # Blacklist the plugin
        discovery.blacklist_plugin(plugin_id)

        # Now should be blacklisted
        assert discovery.is_blacklisted(plugin_id)

    @pytest.mark.asyncio
    async def test_discover_all_empty(self, discovery: PluginDiscovery) -> None:
        """Validate plugin discovery behavior with no available plugins.

        Tests the discovery system's handling of scenarios where no plugins
        are available through either entry points or file system discovery.

        Mock Strategy:
            - Clear plugin directories to prevent file system discovery
            - Mock entry_points to return empty list
            - Use real discovery methods for authentic validation

        Test Scenario:
            - No plugin directories configured
            - No entry points available
            - Run complete discovery process

        Validates:
            - Empty discovery returns empty dictionary
            - No errors raised during empty discovery
            - System handles absence of plugins gracefully
        """
        # Clear plugin directories to avoid actual discovery
        discovery.plugin_directories = []

        with patch("importlib.metadata.entry_points", return_value=[]):
            result = await discovery.discover_all()

            # Should return empty dict when no plugins found
            if result != {}:
                raise AssertionError(f"Expected {{}}, got {result}")

    @pytest.mark.asyncio
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
        """Validate plugin class validation when metadata is missing.

        Tests the plugin validation system's ability to reject plugin classes
        that don't provide required metadata, ensuring strict compliance.

        Mock Configuration:
            - Creates plugin class without METADATA attribute
            - Mocks issubclass to pass inheritance check
            - Mocks hasattr to fail metadata check

        Test Scenario:
            - Valid plugin inheritance but missing METADATA
            - Validation should fail due to missing metadata
            - System rejects incomplete plugin implementations

        Validates:
            - Missing metadata causes validation failure
            - Returns False for incomplete plugin classes
            - Strict metadata requirements are enforced
        """
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
        mock_plugin_class.METADATA = {"name": "test-plugin"}

        # Mock validation to pass
        with patch.object(discovery, "_validate_plugin_class", return_value=True):
            # Should not raise an error
            discovery.register_plugin(mock_plugin_class)

            # Plugin should be discoverable
            result = discovery.get_discovered_plugin("test-plugin")
            assert result is not None
            if result.metadata.name != "test-plugin":
                raise AssertionError(
                    f"Expected {'test-plugin'}, got {result.metadata.name}",
                )

    @pytest.mark.asyncio
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

    @pytest.mark.asyncio
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

    @pytest.mark.asyncio
    async def test_discover_file_system_nonexistent_dir(
        self,
        discovery: PluginDiscovery,
    ) -> None:
        """Validate file system discovery resilience with invalid directories.

        Tests the discovery system's ability to handle non-existent directories
        gracefully without raising exceptions or causing system failures.

        Test Scenario:
            - Configure discovery with non-existent directory path
            - Attempt file system discovery operation
            - Verify system handles missing directory gracefully

        Validates:
            - Non-existent directories don't cause discovery failure
            - System continues operation despite missing paths
            - No exceptions raised for invalid directory paths
        """
        test_dir = Path("/nonexistent/plugins")
        discovery.plugin_directories = [str(test_dir)]

        # Should not raise an error even with non-existent directory
        await discovery._discover_file_system()

        # Should complete without errors
        assert True
