"""REAL test suite for flext_plugin.core.discovery module.

This test module provides comprehensive validation of plugin discovery functionality
using REAL method calls and actual file system operations without ANY mocks.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import ClassVar

import pytest

from flext_core import FlextTypes
from flext_plugin import PluginDiscovery, PluginType


class TestPluginDiscoveryReal:
    """REAL test suite for PluginDiscovery with actual file system operations.

    This test class validates plugin discovery functionality using REAL method
    calls and file operations, providing integration-focused testing that validates
    actual system behavior without any mocks.
    """

    @pytest.fixture
    def temp_dir(self) -> Generator[Path]:
        """Create REAL temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    def test_discovery_initialization_with_defaults(self) -> None:
        """Test plugin discovery initialization with default values."""
        discovery = PluginDiscovery()

        assert discovery is not None
        assert discovery.plugin_directory == "/usr/local/plugins"
        assert isinstance(discovery.plugin_directories, list)
        assert len(discovery.plugin_directories) == 0
        # Internal fields are excluded from serialization but accessible
        assert hasattr(discovery, "discovered_plugins")
        assert hasattr(discovery, "blacklisted_plugins")

    def test_discovery_initialization_with_custom_directory(
        self,
        temp_dir: Path,
    ) -> None:
        """Test plugin discovery initialization with custom directory."""
        custom_dir = str(temp_dir / "custom_plugins")
        discovery = PluginDiscovery(plugin_directory=custom_dir)

        assert discovery.plugin_directory == custom_dir
        assert isinstance(discovery.plugin_directories, list)
        assert len(discovery.plugin_directories) == 0

    def test_discovery_initialization_with_additional_directories(
        self,
        temp_dir: Path,
    ) -> None:
        """Test plugin discovery initialization with additional directories."""
        main_dir = str(temp_dir / "main_plugins")
        additional_dirs = [
            str(temp_dir / "extra1"),
            str(temp_dir / "extra2"),
        ]

        discovery = PluginDiscovery(
            plugin_directory=main_dir,
            plugin_directories=additional_dirs,
        )

        assert discovery.plugin_directory == main_dir
        assert discovery.plugin_directories == additional_dirs

    def test_validate_business_rules_success(self, temp_dir: Path) -> None:
        """Test business rules validation with valid directory."""
        plugin_dir = str(temp_dir / "plugins")
        discovery = PluginDiscovery(plugin_directory=plugin_dir)

        result = discovery.validate_business_rules()

        assert result.success
        assert result.data is None
        assert result.error is None

    def test_validate_business_rules_empty_directory_fails(self) -> None:
        """Test business rules validation with empty directory fails."""
        discovery = PluginDiscovery(plugin_directory="")

        result = discovery.validate_business_rules()

        assert not result.success
        assert result.error is not None
        assert "Plugin directory is required" in result.error

    def test_add_plugin_directory(self, temp_dir: Path) -> None:
        """Test adding a new plugin directory."""
        discovery = PluginDiscovery()
        new_dir = temp_dir / "new_plugins"

        # Initially empty
        assert len(discovery.plugin_directories) == 0

        # Add directory
        discovery.add_plugin_directory(new_dir)

        # Should be added
        assert len(discovery.plugin_directories) == 1
        assert str(new_dir) in discovery.plugin_directories

    def test_add_duplicate_plugin_directory_ignored(self, temp_dir: Path) -> None:
        """Test adding duplicate plugin directory is ignored."""
        discovery = PluginDiscovery()
        plugin_dir = temp_dir / "plugins"

        # Add same directory twice
        discovery.add_plugin_directory(plugin_dir)
        discovery.add_plugin_directory(plugin_dir)

        # Should only appear once
        assert len(discovery.plugin_directories) == 1
        assert str(plugin_dir) in discovery.plugin_directories

    def test_add_multiple_plugin_directories(self, temp_dir: Path) -> None:
        """Test adding multiple different plugin directories."""
        discovery = PluginDiscovery()

        dir1 = temp_dir / "plugins1"
        dir2 = temp_dir / "plugins2"
        dir3 = temp_dir / "plugins3"

        discovery.add_plugin_directory(dir1)
        discovery.add_plugin_directory(dir2)
        discovery.add_plugin_directory(dir3)

        assert len(discovery.plugin_directories) == 3
        assert str(dir1) in discovery.plugin_directories
        assert str(dir2) in discovery.plugin_directories
        assert str(dir3) in discovery.plugin_directories

    def test_blacklist_plugin_functionality(self) -> None:
        """Test plugin blacklisting functionality."""
        discovery = PluginDiscovery()

        # Initially not blacklisted
        assert not discovery.is_blacklisted("test-plugin")

        # Blacklist plugin
        discovery.blacklist_plugin("test-plugin")

        # Should be blacklisted
        assert discovery.is_blacklisted("test-plugin")

        # Other plugins should not be blacklisted
        assert not discovery.is_blacklisted("other-plugin")

    def test_blacklist_multiple_plugins(self) -> None:
        """Test blacklisting multiple plugins."""
        discovery = PluginDiscovery()

        plugins_to_blacklist = ["plugin1", "plugin2", "plugin3"]

        # Blacklist all plugins
        for plugin_id in plugins_to_blacklist:
            discovery.blacklist_plugin(plugin_id)

        # All should be blacklisted
        for plugin_id in plugins_to_blacklist:
            assert discovery.is_blacklisted(plugin_id)

        # Non-blacklisted plugin should not be blacklisted
        assert not discovery.is_blacklisted("clean-plugin")

    def test_get_discovered_plugin_not_found(self) -> None:
        """Test getting non-existent discovered plugin."""
        discovery = PluginDiscovery()

        result = discovery.get_discovered_plugin("non-existent")

        assert result is None

    def test_register_plugin_class_valid(self) -> None:
        """Test registering a valid plugin class."""
        discovery = PluginDiscovery()

        # Create REAL plugin class with required methods
        class ValidPlugin:
            METADATA: ClassVar[FlextTypes.Core.Headers] = {
                "name": "valid-plugin",
                "version": "1.0.0",
            }

            def initialize(self) -> None:
                pass

            def cleanup(self) -> None:
                pass

            def health_check(self) -> bool:
                return True

            def execute(self) -> FlextTypes.Core.Dict:
                return {"status": "success"}

        # Register plugin
        discovery.register_plugin(ValidPlugin)

        # Should be discovered
        plugin = discovery.get_discovered_plugin("valid-plugin")
        assert plugin is not None
        assert isinstance(plugin, ValidPlugin)

    def test_register_plugin_class_without_metadata(self) -> None:
        """Test registering plugin class without metadata."""
        discovery = PluginDiscovery()

        # Create REAL plugin class without metadata
        class PluginWithoutMetadata:
            def initialize(self) -> None:
                pass

            def cleanup(self) -> None:
                pass

            def health_check(self) -> bool:
                return True

            def execute(self) -> FlextTypes.Core.Dict:
                return {"status": "success"}

        # Register plugin (should use class name)
        discovery.register_plugin(PluginWithoutMetadata)

        # Should be discovered with class name
        plugin = discovery.get_discovered_plugin("PluginWithoutMetadata")
        assert plugin is not None
        assert isinstance(plugin, PluginWithoutMetadata)

    def test_register_plugin_class_invalid(self) -> None:
        """Test registering invalid plugin class."""
        discovery = PluginDiscovery()

        # Create REAL plugin class missing required methods
        class InvalidPlugin:
            def some_method(self) -> None:
                pass

        # Register plugin (should be ignored due to validation failure)
        discovery.register_plugin(InvalidPlugin)

        # Should not be discovered
        plugin = discovery.get_discovered_plugin("InvalidPlugin")
        assert plugin is None

    @pytest.mark.asyncio
    async def test_discover_plugins_empty_directories(self, temp_dir: Path) -> None:
        """Test discovering plugins from empty directories."""
        plugin_dir = temp_dir / "empty_plugins"
        plugin_dir.mkdir()

        discovery = PluginDiscovery(plugin_directory=str(plugin_dir))
        discovery.add_plugin_directory(plugin_dir)

        result = await discovery.discover_all()

        # Should return empty dict for empty directories
        assert isinstance(result, dict)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_discover_plugins_with_real_files(self, temp_dir: Path) -> None:
        """Test discovering plugins with REAL plugin files and manifests."""
        plugin_dir = temp_dir / "real_plugins"
        plugin_dir.mkdir()

        # Create REAL plugin file
        plugin_file = plugin_dir / "test_plugin.py"
        plugin_file.write_text('''
"""REAL test plugin."""

class TestPlugin:
    def initialize(self):
        pass

    def cleanup(self):
        pass

    def health_check(self):
        return True

    def execute(self):
        return {"message": "REAL plugin execution"}
''')

        # Create REAL manifest file
        manifest_file = plugin_dir / "test_plugin.json"
        manifest_data = {
            "name": "test-plugin",
            "version": "1.0.0",
            "description": "REAL test plugin",
            "type": PluginType.TAP.value,
            "author": "Test Suite",
        }
        manifest_file.write_text(json.dumps(manifest_data, indent=2))

        discovery = PluginDiscovery(plugin_directory=str(plugin_dir))
        discovery.add_plugin_directory(plugin_dir)

        result = await discovery.discover_all()

        # Should discover the plugin
        assert isinstance(result, dict)
        assert len(result) > 0
        assert "test-plugin" in result

        plugin_info = result["test-plugin"]
        assert isinstance(plugin_info, dict)
        assert plugin_info["name"] == "test-plugin"
        assert plugin_info["version"] == "1.0.0"

    @pytest.mark.asyncio
    async def test_discover_multiple_plugins_different_directories(
        self, temp_dir: Path
    ) -> None:
        """Test discovering multiple plugins from different directories."""
        # Create multiple plugin directories
        dir1 = temp_dir / "plugins1"
        dir2 = temp_dir / "plugins2"
        dir1.mkdir()
        dir2.mkdir()

        # Create plugin in first directory
        plugin1_file = dir1 / "plugin1.py"
        plugin1_file.write_text("# Plugin 1 content")
        manifest1_file = dir1 / "plugin1.json"
        manifest1_file.write_text(
            json.dumps(
                {
                    "name": "plugin-1",
                    "version": "1.0.0",
                    "type": PluginType.TAP.value,
                },
            ),
        )

        # Create plugin in second directory
        plugin2_file = dir2 / "plugin2.py"
        plugin2_file.write_text("# Plugin 2 content")
        manifest2_file = dir2 / "plugin2.json"
        manifest2_file.write_text(
            json.dumps(
                {
                    "name": "plugin-2",
                    "version": "2.0.0",
                    "type": PluginType.TARGET.value,
                },
            ),
        )

        discovery = PluginDiscovery()
        discovery.add_plugin_directory(dir1)
        discovery.add_plugin_directory(dir2)

        result = await discovery.discover_all()

        # Should discover both plugins
        assert len(result) == 2
        assert "plugin-1" in result
        assert "plugin-2" in result

    @pytest.mark.asyncio
    async def test_discover_plugins_by_type(self, temp_dir: Path) -> None:
        """Test discovering plugins by type with REAL plugins."""
        plugin_dir = temp_dir / "typed_plugins"
        plugin_dir.mkdir()

        # Create TAP plugin
        tap_file = plugin_dir / "tap_plugin.py"
        tap_file.write_text("# TAP plugin content")
        tap_manifest = plugin_dir / "tap_plugin.json"
        tap_manifest.write_text(
            json.dumps(
                {
                    "name": "tap-plugin",
                    "type": PluginType.TAP.value,
                    "version": "1.0.0",
                },
            ),
        )

        # Create TARGET plugin
        target_file = plugin_dir / "target_plugin.py"
        target_file.write_text("# TARGET plugin content")
        target_manifest = plugin_dir / "target_plugin.json"
        target_manifest.write_text(
            json.dumps(
                {
                    "name": "target-plugin",
                    "type": PluginType.TARGET.value,
                    "version": "1.0.0",
                },
            ),
        )

        discovery = PluginDiscovery()
        discovery.add_plugin_directory(plugin_dir)

        # Discover TAP plugins only
        tap_plugins = await discovery.discover_by_type(PluginType.TAP)

        assert len(tap_plugins) == 1
        assert "tap-plugin" in tap_plugins
        assert "target-plugin" not in tap_plugins

        # Discover TARGET plugins only
        target_plugins = await discovery.discover_by_type(PluginType.TARGET)

        assert len(target_plugins) == 1
        assert "target-plugin" in target_plugins
        assert "tap-plugin" not in target_plugins

    @pytest.mark.asyncio
    async def test_discovery_ignores_system_files(self, temp_dir: Path) -> None:
        """Test that discovery ignores __init__.py and similar files."""
        plugin_dir = temp_dir / "dunder_test"
        plugin_dir.mkdir()

        # Create __init__.py file (should be ignored)
        init_file = plugin_dir / "__init__.py"
        init_file.write_text("# Init file")

        # Create __pycache__ directory (should be ignored)
        pycache_dir = plugin_dir / "__pycache__"
        pycache_dir.mkdir()
        cache_file = pycache_dir / "test.pyc"
        cache_file.write_text("# Cache file")

        # Create valid plugin
        plugin_file = plugin_dir / "valid_plugin.py"
        plugin_file.write_text("# Valid plugin")
        manifest_file = plugin_dir / "valid_plugin.json"
        manifest_file.write_text(
            json.dumps(
                {
                    "name": "valid-plugin",
                    "version": "1.0.0",
                },
            ),
        )

        discovery = PluginDiscovery()
        discovery.add_plugin_directory(plugin_dir)

        result = await discovery.discover_all()

        # Should only discover the valid plugin
        assert len(result) == 1
        assert "valid-plugin" in result

    @pytest.mark.asyncio
    async def test_discovery_handles_invalid_manifests(self, temp_dir: Path) -> None:
        """Test discovery handles invalid manifest files gracefully."""
        plugin_dir = temp_dir / "invalid_manifest_test"
        plugin_dir.mkdir()

        # Create plugin with invalid JSON manifest
        plugin_file = plugin_dir / "broken_plugin.py"
        plugin_file.write_text("# Plugin with broken manifest")

        invalid_manifest = plugin_dir / "broken_plugin.json"
        invalid_manifest.write_text("{ invalid json content }")

        # Create valid plugin for comparison
        valid_file = plugin_dir / "valid_plugin.py"
        valid_file.write_text("# Valid plugin")
        valid_manifest = plugin_dir / "valid_plugin.json"
        valid_manifest.write_text(
            json.dumps(
                {
                    "name": "valid-plugin",
                    "version": "1.0.0",
                },
            ),
        )

        discovery = PluginDiscovery()
        discovery.add_plugin_directory(plugin_dir)

        result = await discovery.discover_all()

        # Should discover valid plugin and ignore invalid one
        assert len(result) == 1
        assert "valid-plugin" in result
        assert "broken-plugin" not in result

    @pytest.mark.asyncio
    async def test_discovery_with_nonexistent_directory(self, temp_dir: Path) -> None:
        """Test discovery with nonexistent directory."""
        nonexistent_dir = temp_dir / "does_not_exist"

        discovery = PluginDiscovery()
        discovery.add_plugin_directory(nonexistent_dir)

        # Should not raise exception
        result = await discovery.discover_all()

        assert isinstance(result, dict)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_full_discovery_workflow_with_real_files(
        self,
        temp_dir: Path,
    ) -> None:
        """Test complete discovery workflow with REAL files and operations."""
        # Setup multiple plugin directories
        main_dir = temp_dir / "main_plugins"
        extra_dir = temp_dir / "extra_plugins"
        main_dir.mkdir()
        extra_dir.mkdir()

        # Create plugins in main directory
        main_plugin_file = main_dir / "main_plugin.py"
        main_plugin_file.write_text("""

class MainPlugin:
    def initialize(self): pass
    def cleanup(self): pass
    def health_check(self): return True
    def execute(self): return {"source": "main"}
""")
        main_manifest = main_dir / "main_plugin.json"
        main_manifest.write_text(
            json.dumps(
                {
                    "name": "main-plugin",
                    "type": PluginType.TAP.value,
                    "version": "1.0.0",
                },
            ),
        )

        # Create plugins in extra directory
        extra_plugin_file = extra_dir / "extra_plugin.py"
        extra_plugin_file.write_text("""

class ExtraPlugin:
    def initialize(self): pass
    def cleanup(self): pass
    def health_check(self): return True
    def execute(self): return {"source": "extra"}
""")
        extra_manifest = extra_dir / "extra_plugin.json"
        extra_manifest.write_text(
            json.dumps(
                {
                    "name": "extra-plugin",
                    "type": PluginType.TARGET.value,
                    "version": "2.0.0",
                },
            ),
        )

        # Initialize discovery
        discovery = PluginDiscovery(plugin_directory=str(main_dir))
        discovery.add_plugin_directory(main_dir)  # Add main directory to scanning list
        discovery.add_plugin_directory(extra_dir)

        # Register manual plugin
        class ManualPlugin:
            METADATA: ClassVar[FlextTypes.Core.Headers] = {
                "name": "manual-plugin",
                "version": "3.0.0",
            }

            def initialize(self) -> None:
                pass

            def cleanup(self) -> None:
                pass

            def health_check(self) -> bool:
                return True

            def execute(self) -> FlextTypes.Core.Headers:
                return {"source": "manual"}

        discovery.register_plugin(ManualPlugin)

        # Blacklist one plugin
        discovery.blacklist_plugin("extra-plugin")

        # Discover all
        all_plugins = await discovery.discover_all()

        # Verify results
        assert len(all_plugins) >= 2  # File-based + manual
        assert "main-plugin" in all_plugins
        assert "extra-plugin" in all_plugins  # Discovery finds it
        assert discovery.is_blacklisted("extra-plugin")  # But it's blacklisted

        # Test type-specific discovery
        tap_plugins = await discovery.discover_by_type(PluginType.TAP)
        target_plugins = await discovery.discover_by_type(PluginType.TARGET)

        assert "main-plugin" in tap_plugins
        assert "extra-plugin" in target_plugins

        # Test individual plugin retrieval
        manual_plugin = discovery.get_discovered_plugin("manual-plugin")
        assert manual_plugin is not None
        assert isinstance(manual_plugin, ManualPlugin)
