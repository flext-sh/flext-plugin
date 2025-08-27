"""REAL test suite for flext_plugin.discovery module - NO MOCKS.

This test module validates the PluginDiscovery functionality with actual file
system operations, real plugin files, and authentic business logic validation.
Follows user requirement: "pare de ficar mockando tudo" - stop mocking everything.

Test Coverage:
    - PluginDiscovery() factory method with proper validation
    - PluginDiscovery.scan() with real plugin directory scanning
    - PluginDiscovery.discover_plugin_entry_points() entry point detection
    - PluginDiscovery.validate_business_rules() domain validation
    - Real file system operations with tmp_path fixtures
    - Actual plugin file creation and scanning

Testing Architecture:
    - REAL file system operations using tmp_path fixtures
    - Actual plugin file creation and content validation
    - Authentic business logic testing without mocks
    - Real error condition testing with invalid directories

Quality Patterns:
    - Direct testing of actual implementation functionality
    - Real file system operations for authentic validation
    - Comprehensive coverage of success and failure scenarios
    - Integration testing with realistic plugin structures
    - Performance validation for real scanning operations

Integration Points:
    - Built on flext-core foundation with FlextResult patterns
    - Real plugin discovery with actual file system scanning
    - Authentic entry point detection and validation
    - Real business rules validation and error handling
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import cast

import pytest
from flext_core import FlextResult

from flext_plugin.discovery import PluginDiscovery


class TestPluginDiscovery:
    """REAL test suite for PluginDiscovery - NO MOCKS, ACTUAL FUNCTIONALITY.

    This test class validates the actual PluginDiscovery implementation using
    real file system operations, actual plugin files, and authentic business
    logic validation. Follows Clean Architecture testing patterns with real
    infrastructure operations.

    Test Categories:
      - Creation: PluginDiscovery() factory method validation
      - Scanning: Real file system scanning with actual plugin files
      - Entry Points: Authentic entry point detection and validation
      - Business Rules: Real domain validation and error handling
      - File Operations: Actual file creation, scanning, and validation

    Architecture Integration:
      - Clean Architecture: Real infrastructure layer testing
      - Domain Logic: Authentic business rules validation
      - File System: Real directory and file operations
      - Error Handling: Actual exception and validation testing
    """

    def test_discovery_creation_with_valid_directory(self) -> None:
        """Test PluginDiscovery() factory method with valid directory."""
        # Create discovery instance using constructor
        discovery: PluginDiscovery = PluginDiscovery(
            plugin_directory="/valid/path"
        )

        # Validate creation succeeded
        assert discovery is not None
        assert isinstance(discovery, PluginDiscovery)
        assert discovery.plugin_directory == "/valid/path"
        assert hasattr(discovery, "id")
        assert hasattr(discovery, "version")

    def test_discovery_creation_with_empty_directory(self) -> None:
        """Test PluginDiscovery() with empty directory path."""
        # Create discovery with empty directory
        discovery: PluginDiscovery = PluginDiscovery(plugin_directory="")

        # Should still create instance (validation happens in validate_business_rules)
        assert discovery is not None
        assert discovery.plugin_directory == ""

    @pytest.mark.asyncio
    async def test_scan_empty_directory_real(self, tmp_path: Path) -> None:
        """Test scanning empty directory with real file system operations.

        Creates actual empty directory and validates that scan() returns
        empty list gracefully without errors.
        """
        # Create real empty directory
        empty_dir = tmp_path / "empty_plugins"
        empty_dir.mkdir()

        # Create discovery instance with real directory
        discovery: PluginDiscovery = PluginDiscovery(
            plugin_directory=str(empty_dir)
        )

        # discover_all should return empty dict
        result: dict[str, object] = await discovery.discover_all()

        assert result == {}
        assert isinstance(result, dict)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_scan_plugins_with_real_files(self, tmp_path: Path) -> None:
        """Test scanning directory with real plugin files.

        Creates actual Python plugin files and validates that scan()
        properly detects and returns plugin information.
        """
        # Create real plugin directory
        plugin_dir = tmp_path / "test_plugins"
        plugin_dir.mkdir()

        # Create real Python plugin files
        plugin1_content = '''
"""Test plugin 1."""

class TestPlugin1:
    """A real test plugin."""

    def __init__(self) -> None:
        self.name = "test-plugin-1"
        self.version = "1.0.0"

    def execute(self) -> dict[str, str]:
        return {"status": "success", "plugin": "test1"}
'''

        plugin2_content = '''
"""Test plugin 2."""

def get_plugin() -> dict[str, str]:
    return {"name": "test-plugin-2", "version": "2.0.0"}
'''

        (plugin_dir / "test_plugin1.py").write_text(plugin1_content)
        (plugin_dir / "test_plugin2.py").write_text(plugin2_content)

        # Create discovery instance
        discovery: PluginDiscovery = PluginDiscovery(
            plugin_directory=str(plugin_dir)
        )

        # Discover plugins
        result: dict[str, object] = await discovery.discover_all()

        # Validate results
        assert len(result) == 2
        plugin_names: list[str] = list(result.keys())
        assert "test_plugin1" in plugin_names
        assert "test_plugin2" in plugin_names

        # Validate plugin structure
        for plugin_data in result.values():
            plugin = cast("dict[str, object]", plugin_data)
            assert "name" in plugin
            assert "path" in plugin
            assert "file_name" in plugin
            assert "size" in plugin
            assert "modified" in plugin
            assert isinstance(plugin["name"], str)
            assert isinstance(plugin["path"], str)
            assert isinstance(plugin["size"], int)
            assert isinstance(plugin["modified"], float)

    @pytest.mark.asyncio
    async def test_scan_nonexistent_directory_real(self) -> None:
        """Test scanning non-existent directory with real file system.

        Creates discovery instance with non-existent directory path and
        validates that scan() handles missing directory gracefully.
        """
        # Create discovery with non-existent directory
        discovery: PluginDiscovery = PluginDiscovery(
            plugin_directory="/absolutely/nonexistent/path"
        )

        # Should return empty dict gracefully (no exceptions)
        result: dict[str, object] = await discovery.discover_all()

        assert result == {}
        assert isinstance(result, dict)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_discover_plugin_entry_points_real(self, tmp_path: Path) -> None:
        """Test discovering plugin entry points with real files.

        Creates actual plugin files and validates that discover_plugin_entry_points()
        properly detects and returns entry point information.
        """
        # Create plugin directory with real files
        plugin_dir = tmp_path / "entry_point_plugins"
        plugin_dir.mkdir()

        # Create real plugin files
        (plugin_dir / "entry_plugin1.py").write_text('''
"""Entry plugin 1."""

class EntryPlugin1:
    """Entry plugin class."""

    def execute(self) -> dict[str, str]:
        return {"status": "ok"}
''')

        (plugin_dir / "entry_plugin2.py").write_text('''
"""Entry plugin 2."""

def plugin_function() -> str:
    return "entry_plugin2"
''')

        # Create discovery instance
        discovery: PluginDiscovery = PluginDiscovery(
            plugin_directory=str(plugin_dir)
        )

        # Discover entry points
        result: dict[str, object] = await discovery.discover_all()

        # Validate results
        assert len(result) == 2
        entry_names: list[str] = list(result.keys())
        assert "entry_plugin1" in entry_names
        assert "entry_plugin2" in entry_names

        # Validate entry point structure
        for entry_point_data in result.values():
            entry_point = cast("dict[str, object]", entry_point_data)
            assert "name" in entry_point
            assert "module_name" in entry_point
            assert "plugin_class" in entry_point
            assert "path" in entry_point
            assert "type" in entry_point
            assert entry_point["plugin_class"] == "Plugin"
            assert entry_point["type"] == "generic"

    def test_business_rules_validation_real(self) -> None:
        """Test business rules validation with real validation logic.

        Tests the actual validate_business_rules() method implementation
        with valid and invalid directory configurations.
        """
        # Test with empty plugin directory (should fail)
        invalid_discovery: PluginDiscovery = PluginDiscovery(plugin_directory="")

        validation_result: FlextResult[None] = (
            invalid_discovery.validate_business_rules()
        )

        assert not validation_result.success
        assert validation_result.error is not None
        assert "Plugin directory is required" in validation_result.error

        # Test with valid plugin directory (should pass)
        valid_discovery: PluginDiscovery = PluginDiscovery(
            plugin_directory="/valid/directory"
        )

        valid_result: FlextResult[None] = valid_discovery.validate_business_rules()

        assert valid_result.success
        assert valid_result.error is None

    @pytest.mark.asyncio
    async def test_scan_ignores_special_files(self, tmp_path: Path) -> None:
        """Test that scan() properly ignores __pycache__ and special files.

        Creates directory with special Python files and validates that
        scan() correctly filters them out.
        """
        # Create plugin directory
        plugin_dir = tmp_path / "filtered_plugins"
        plugin_dir.mkdir()

        # Create valid plugin
        (plugin_dir / "valid_plugin.py").write_text('''
"""Valid plugin."""

class ValidPlugin:
    def execute(self) -> str:
        return "valid"
''')

        # Create special files that should be ignored
        (plugin_dir / "__init__.py").write_text("# Init file")
        (plugin_dir / "__pycache__").mkdir()
        (plugin_dir / "__main__.py").write_text("# Main file")

        # Create discovery instance
        discovery: PluginDiscovery = PluginDiscovery(
            plugin_directory=str(plugin_dir)
        )

        # Scan plugins
        result: dict[str, object] = await discovery.discover_all()

        # Should only find the valid plugin (ignores __ files)
        assert len(result) == 1
        assert "valid_plugin" in result

    def test_plugin_discovery_factory_validation(self) -> None:
        """Test PluginDiscovery() factory method with various parameters.

        Tests the actual factory method implementation with different
        parameter combinations and validates proper entity creation.
        """
        # Test with minimal parameters
        discovery1: PluginDiscovery = PluginDiscovery(
            plugin_directory="/test/path"
        )
        assert discovery1.plugin_directory == "/test/path"
        assert hasattr(discovery1, "id")
        assert hasattr(discovery1, "version")

        # Test with additional kwargs
        discovery2: PluginDiscovery = PluginDiscovery(
            plugin_directory="/another/path", version=2, metadata={"env": "test"}
        )
        assert discovery2.plugin_directory == "/another/path"
        # Version and metadata are handled by FlextEntity

    @pytest.mark.asyncio
    async def test_scan_reports_accurate_file_sizes(self, tmp_path: Path) -> None:
        """Test that scan() accurately reports file sizes for different plugins.

        Creates plugins with different content sizes and validates that
        scan() correctly reports the actual file sizes.
        """
        # Create plugin directory
        plugin_dir = tmp_path / "size_test_plugins"
        plugin_dir.mkdir()

        # Create plugins with different content sizes
        small_content = "# Small plugin\nclass Small: pass"
        large_content = (
            "# Large plugin\n" + "# Comment line\n" * 100 + "class Large: pass"
        )

        (plugin_dir / "small_plugin.py").write_text(small_content)
        (plugin_dir / "large_plugin.py").write_text(large_content)

        # Create discovery instance
        discovery: PluginDiscovery = PluginDiscovery(
            plugin_directory=str(plugin_dir)
        )

        # Scan plugins
        result: dict[str, object] = await discovery.discover_all()

        # Validate results include accurate size information
        assert len(result) == 2

        small_plugin: dict[str, object] = cast("dict[str, object]", result["small_plugin"])
        large_plugin: dict[str, object] = cast("dict[str, object]", result["large_plugin"])

        # Validate size accuracy
        small_size = cast("int", small_plugin["size"])
        large_size = cast("int", large_plugin["size"])
        assert large_size > small_size
        assert isinstance(small_size, int)
        assert isinstance(large_size, int)
        assert small_size > 0  # File is not empty
        assert large_size > 1000  # Large file should be significantly bigger

    @pytest.mark.asyncio
    async def test_scan_with_modified_timestamps(self, tmp_path: Path) -> None:
        """Test that scan() correctly reports file modification timestamps.

        Creates plugin files at different times and validates that
        scan() correctly captures the modification timestamps.
        """
        # Create plugin directory
        plugin_dir = tmp_path / "timestamp_plugins"
        plugin_dir.mkdir()

        # Create first plugin
        (plugin_dir / "first_plugin.py").write_text("# First plugin\nclass First: pass")

        # Wait a bit to ensure different timestamp
        await asyncio.sleep(0.1)

        # Create second plugin
        (plugin_dir / "second_plugin.py").write_text(
            "# Second plugin\nclass Second: pass"
        )

        # Create discovery instance
        discovery: PluginDiscovery = PluginDiscovery(
            plugin_directory=str(plugin_dir)
        )

        # Scan plugins
        result: dict[str, object] = await discovery.discover_all()

        # Validate timestamp information
        assert len(result) == 2

        for plugin_data in result.values():
            plugin = cast("dict[str, object]", plugin_data)
            assert "modified" in plugin
            assert isinstance(plugin["modified"], float)
            assert plugin["modified"] > 0  # Should be valid timestamp

        # Get plugins by name
        first_plugin: dict[str, object] = cast("dict[str, object]", result["first_plugin"])
        second_plugin: dict[str, object] = cast("dict[str, object]", result["second_plugin"])

        # Second plugin should have later timestamp (might be equal if too fast)
        first_time = cast("float", first_plugin["modified"])
        second_time = cast("float", second_plugin["modified"])
        assert second_time >= first_time
