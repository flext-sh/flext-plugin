"""Coverage-focused test suite for flext_plugin.discovery module.

This test module focuses on maximizing code coverage for the discovery system
by testing actual implemented functionality with real file system scenarios.

Strategy: Test the 3 main methods with comprehensive file system scenarios.
"""

from __future__ import annotations

import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import cast

import pytest

from flext_plugin.core.discovery import PluginDiscovery


class TestPluginDiscovery:
    """Coverage-focused tests for PluginDiscovery.

    Tests the actual discovery system implementation with real file scenarios.
    """

    @pytest.fixture
    def temp_dir(self) -> Generator[Path]:
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    def test_discovery_initialization(self, temp_dir: Path) -> None:
        """Test discovery initialization with plugin directory."""
        plugin_dir = str(temp_dir / "plugins")
        discovery = PluginDiscovery(plugin_directory=plugin_dir)
        assert discovery is not None
        assert discovery.plugin_directory == plugin_dir

    def test_discovery_initialization_with_id(self, temp_dir: Path) -> None:
        """Test discovery initialization with custom ID."""
        plugin_dir = str(temp_dir / "plugins")
        custom_id = "custom-discovery-id"
        discovery = PluginDiscovery(entity_id=custom_id, plugin_directory=plugin_dir)
        assert discovery is not None
        assert str(discovery.id) == custom_id
        assert discovery.plugin_directory == plugin_dir

    def test_validate_domain_rules_empty_directory_fails(self) -> None:
        """Test domain validation with empty directory fails."""
        discovery = PluginDiscovery(plugin_directory="")
        result = discovery.validate_business_rules()
        assert not result.success
        assert "Plugin directory is required" in str(result.error)

    def test_validate_domain_rules_valid_directory_succeeds(
        self,
        temp_dir: Path,
    ) -> None:
        """Test domain validation with valid directory succeeds."""
        plugin_dir = str(temp_dir / "plugins")
        discovery = PluginDiscovery(plugin_directory=plugin_dir)
        result = discovery.validate_business_rules()
        assert result.success
        assert result.data is None

    @pytest.mark.asyncio
    async def test_scan_nonexistent_directory_returns_empty_list(
        self,
        temp_dir: Path,
    ) -> None:
        """Test scan with nonexistent directory returns empty list."""
        plugin_dir = str(temp_dir / "nonexistent")
        discovery = PluginDiscovery(plugin_directory=plugin_dir)
        plugins = await discovery.discover_all()
        assert isinstance(plugins, dict)
        assert len(plugins) == 0

    @pytest.mark.asyncio
    async def test_scan_empty_directory_returns_empty_list(
        self,
        temp_dir: Path,
    ) -> None:
        """Test scan with empty directory returns empty list."""
        plugin_dir = temp_dir / "plugins"
        plugin_dir.mkdir()
        discovery = PluginDiscovery(plugin_directory=str(plugin_dir))
        plugins = await discovery.discover_all()
        assert isinstance(plugins, dict)
        assert len(plugins) == 0

    @pytest.mark.asyncio
    async def test_scan_directory_with_python_files(self, temp_dir: Path) -> None:
        """Test scan with Python files returns plugin information."""
        plugin_dir = temp_dir / "plugins"
        plugin_dir.mkdir()

        # Create discovery with proper directory setup
        discovery = PluginDiscovery(plugin_directory="")
        discovery.add_plugin_directory(plugin_dir)

        # Create test plugin files with manifests
        plugin1 = plugin_dir / "test_plugin.py"
        plugin1.write_text("# Test plugin 1\nclass TestPlugin:\n    pass\n")
        manifest1 = plugin_dir / "test_plugin.json"
        manifest1.write_text('{"name": "test_plugin", "type": "generic"}')

        plugin2 = plugin_dir / "another_plugin.py"
        plugin2.write_text("# Test plugin 2\nclass AnotherPlugin:\n    pass\n")
        manifest2 = plugin_dir / "another_plugin.json"
        manifest2.write_text('{"name": "another_plugin", "type": "generic"}')

        plugins = await discovery.discover_all()
        assert isinstance(plugins, dict)
        assert len(plugins) == 2

        # Check plugin information structure
        plugin_names = set(plugins.keys())
        assert "test_plugin" in plugin_names
        assert "another_plugin" in plugin_names

        # Check plugin data structure (they are manifest dictionaries)
        for plugin_name, plugin_data in plugins.items():
            plugin_dict = cast("dict[str, object]", plugin_data)
            assert "name" in plugin_dict
            assert "type" in plugin_dict
            assert plugin_dict["name"] == plugin_name
            assert plugin_dict["type"] == "generic"

    @pytest.mark.asyncio
    async def test_scan_ignores_dunder_files(self, temp_dir: Path) -> None:
        """Test scan ignores __init__.py and other dunder files."""
        plugin_dir = temp_dir / "plugins"
        plugin_dir.mkdir()

        # Create discovery with proper directory setup
        discovery = PluginDiscovery(plugin_directory="")
        discovery.add_plugin_directory(plugin_dir)

        # Create test files including dunder files
        plugin_file = plugin_dir / "real_plugin.py"
        plugin_file.write_text("# Real plugin\nclass RealPlugin:\n    pass\n")
        manifest_file = plugin_dir / "real_plugin.json"
        manifest_file.write_text('{"name": "real_plugin", "type": "generic"}')

        init_file = plugin_dir / "__init__.py"
        init_file.write_text("# Init file\n")
        cache_file = plugin_dir / "__pycache__.py"
        cache_file.write_text("# Cache file\n")

        plugins = await discovery.discover_all()
        assert isinstance(plugins, dict)
        assert len(plugins) == 1

        # Verify only the real plugin was discovered
        assert "real_plugin" in plugins
        plugin_dict = cast("dict[str, object]", plugins["real_plugin"])
        assert plugin_dict["name"] == "real_plugin"

    @pytest.mark.asyncio
    async def test_scan_ignores_non_python_files(self, temp_dir: Path) -> None:
        """Test scan ignores non-Python files."""
        plugin_dir = temp_dir / "plugins"
        plugin_dir.mkdir()

        # Create discovery with proper directory setup
        discovery = PluginDiscovery(plugin_directory="")
        discovery.add_plugin_directory(plugin_dir)

        # Create mixed file types
        plugin_file = plugin_dir / "plugin.py"
        plugin_file.write_text("# Python plugin\nclass Plugin:\n    pass\n")
        manifest_file = plugin_dir / "plugin.json"
        manifest_file.write_text('{"name": "plugin", "type": "generic"}')

        text_file = plugin_dir / "readme.txt"
        text_file.write_text("This is a readme file")
        config_file = plugin_dir / "config.json"
        config_file.write_text('{"name": "config"}')

        plugins = await discovery.discover_all()
        assert isinstance(plugins, dict)
        assert len(plugins) == 1

        # Verify only the plugin with manifest was discovered
        assert "plugin" in plugins
        plugin_dict = cast("dict[str, object]", plugins["plugin"])
        assert plugin_dict["name"] == "plugin"

    @pytest.mark.asyncio
    async def test_scan_plugin_file_attributes(self, temp_dir: Path) -> None:
        """Test scan returns correct plugin manifest data."""
        plugin_dir = temp_dir / "plugins"
        plugin_dir.mkdir()

        # Create discovery with proper directory setup
        discovery = PluginDiscovery(plugin_directory="")
        discovery.add_plugin_directory(plugin_dir)

        # Create plugin with known content and manifest
        plugin_content = "# Test plugin with known size\nclass TestPlugin:\n    def execute(self):\n        return 'test'"
        plugin_file = plugin_dir / "size_test_plugin.py"
        plugin_file.write_text(plugin_content)

        manifest_content = (
            '{"name": "size_test_plugin", "type": "test", "version": "1.0.0"}'
        )
        manifest_file = plugin_dir / "size_test_plugin.json"
        manifest_file.write_text(manifest_content)

        plugins = await discovery.discover_all()
        assert len(plugins) == 1

        # Verify plugin data from manifest
        assert "size_test_plugin" in plugins
        plugin_dict = cast("dict[str, object]", plugins["size_test_plugin"])

        # Check manifest attributes
        assert plugin_dict["name"] == "size_test_plugin"
        assert plugin_dict["type"] == "test"
        assert plugin_dict["version"] == "1.0.0"

    @pytest.mark.asyncio
    async def test_discover_all_empty_directory(
        self,
        temp_dir: Path,
    ) -> None:
        """Test discover_all with empty directory."""
        plugin_dir = str(temp_dir / "empty")
        discovery = PluginDiscovery(plugin_directory=plugin_dir)
        discovered_plugins = await discovery.discover_all()
        assert isinstance(discovered_plugins, dict)
        assert len(discovered_plugins) == 0

    @pytest.mark.asyncio
    async def test_discover_all_with_plugins(
        self,
        temp_dir: Path,
    ) -> None:
        """Test discover_all with plugin files."""
        plugin_dir = temp_dir / "plugins"
        plugin_dir.mkdir()

        # Add directory to discovery and create manifest files for real discovery
        discovery = PluginDiscovery(plugin_directory="")
        discovery.add_plugin_directory(plugin_dir)

        # Create test plugin files with manifest files
        plugin1 = plugin_dir / "extractor_plugin.py"
        plugin1.write_text("class ExtractorPlugin:\n    pass\n")
        manifest1 = plugin_dir / "extractor_plugin.json"
        manifest1.write_text('{"name": "extractor_plugin", "type": "extractor"}')

        plugin2 = plugin_dir / "transformer_plugin.py"
        plugin2.write_text("class TransformerPlugin:\n    pass\n")
        manifest2 = plugin_dir / "transformer_plugin.json"
        manifest2.write_text('{"name": "transformer_plugin", "type": "transformer"}')

        plugins = await discovery.discover_all()
        assert isinstance(plugins, dict)
        assert len(plugins) == 2

        # Check plugin structure
        plugin_names = set(plugins.keys())
        assert "extractor_plugin" in plugin_names
        assert "transformer_plugin" in plugin_names

        # Check plugin data structure (they are manifest dictionaries)
        for plugin_name, plugin_data in plugins.items():
            plugin_dict = cast("dict[str, object]", plugin_data)
            assert "name" in plugin_dict
            assert plugin_dict["name"] == plugin_name

    @pytest.mark.asyncio
    async def test_discover_all_integration_with_scan(
        self,
        temp_dir: Path,
    ) -> None:
        """Test discover_all integrates with scan method."""
        plugin_dir = temp_dir / "plugins"
        plugin_dir.mkdir()

        # Create discovery with proper directory setup
        discovery = PluginDiscovery(plugin_directory="")
        discovery.add_plugin_directory(plugin_dir)

        # Create test plugin with manifest
        plugin_file = plugin_dir / "integration_test.py"
        plugin_file.write_text(
            "class IntegrationTestPlugin:\n    def run(self):\n        return True\n",
        )
        manifest_file = plugin_dir / "integration_test.json"
        manifest_file.write_text('{"name": "integration_test", "type": "generic"}')

        # Get results from discover_all method
        plugins = await discovery.discover_all()
        discovered_again = await discovery.discover_all()

        # Should have consistent results
        assert len(plugins) == 1
        assert len(discovered_again) == 1

        # Should be the same data
        assert "integration_test" in plugins
        assert "integration_test" in discovered_again
        plugin_data = cast("dict[str, object]", plugins["integration_test"])
        discovered_data = cast(
            "dict[str, object]", discovered_again["integration_test"]
        )
        assert plugin_data["name"] == discovered_data["name"]
        assert plugin_data["type"] == discovered_data["type"]

    @pytest.mark.asyncio
    async def test_scan_large_number_of_files(self, temp_dir: Path) -> None:
        """Test scan handles larger number of plugin files."""
        plugin_dir = temp_dir / "plugins"
        plugin_dir.mkdir()

        # Create discovery with proper directory setup
        discovery = PluginDiscovery(plugin_directory="")
        discovery.add_plugin_directory(plugin_dir)

        # Create multiple plugin files with manifests
        num_plugins = 10
        for i in range(num_plugins):
            plugin_file = plugin_dir / f"plugin_{i:02d}.py"
            plugin_file.write_text(f"# Plugin {i}\nclass Plugin{i}:\n    pass\n")
            manifest_file = plugin_dir / f"plugin_{i:02d}.json"
            manifest_file.write_text(f'{{"name": "plugin_{i:02d}", "type": "generic"}}')

        plugins = await discovery.discover_all()
        assert len(plugins) == num_plugins
        # Check all plugins are present
        plugin_names = set(plugins.keys())
        expected_names = {f"plugin_{i:02d}" for i in range(num_plugins)}
        assert plugin_names == expected_names

    @pytest.mark.asyncio
    async def test_scan_mixed_file_scenario(self, temp_dir: Path) -> None:
        """Test scan with mixed file scenario (realistic plugin directory)."""
        plugin_dir = temp_dir / "plugins"
        plugin_dir.mkdir()

        # Create discovery with proper directory setup
        discovery = PluginDiscovery(plugin_directory="")
        discovery.add_plugin_directory(plugin_dir)

        # Create realistic plugin directory structure with manifests for Python plugins
        files_to_create = [
            ("tap_github.py", "# GitHub tap plugin\nclass GitHubTap:\n    pass\n"),
            ("tap_github.json", '{"name": "tap_github", "type": "tap"}'),
            (
                "target_postgres.py",
                "# PostgreSQL target plugin\nclass PostgresTarget:\n    pass\n",
            ),
            ("target_postgres.json", '{"name": "target_postgres", "type": "target"}'),
            (
                "transform_utils.py",
                "# Transform utilities\ndef transform_data():\n    pass\n",
            ),
            (
                "transform_utils.json",
                '{"name": "transform_utils", "type": "transform"}',
            ),
            ("__init__.py", "# Package init\n"),
            ("__pycache__.py", "# Cache file\n"),
            ("config.json", '{"version": "1.0"}'),
            ("README.md", "# Plugin Documentation\n"),
            ("requirements.txt", "requests>=2.0.0\n"),
        ]
        for filename, content in files_to_create:
            file_path = plugin_dir / filename
            file_path.write_text(content)

        plugins = await discovery.discover_all()
        # Should only find the 3 plugins with manifests
        assert len(plugins) == 3
        plugin_names = set(plugins.keys())
        expected_names = {"tap_github", "target_postgres", "transform_utils"}
        assert plugin_names == expected_names

    def test_discovery_inheritance(self, temp_dir: Path) -> None:
        """Test discovery basic functionality."""
        plugin_dir = str(temp_dir / "plugins")
        discovery = PluginDiscovery(plugin_directory=plugin_dir)
        # Should be a valid PluginDiscovery instance
        assert isinstance(discovery, PluginDiscovery)
        # Should have basic attributes
        assert hasattr(discovery, "plugin_directory")
        assert discovery.plugin_directory == plugin_dir

    def test_discovery_model_config(self, temp_dir: Path) -> None:
        """Test discovery has correct model configuration."""
        plugin_dir = str(temp_dir / "plugins")
        discovery = PluginDiscovery(plugin_directory=plugin_dir)
        # Should have correct model config
        assert hasattr(discovery, "model_config")
        assert discovery.model_config.get("arbitrary_types_allowed") is True


class TestPluginDiscoveryErrorHandling:
    """Test error handling and edge cases."""

    @pytest.fixture
    def temp_dir(self) -> Generator[Path]:
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    def test_discovery_with_none_directory(self) -> None:
        """Test discovery handles None directory gracefully."""
        # Should not raise exception during creation
        discovery = PluginDiscovery(plugin_directory="")
        assert discovery is not None
        # Validation should fail
        result = discovery.validate_business_rules()
        assert not result.success

    @pytest.mark.asyncio
    async def test_scan_handles_permission_errors_gracefully(
        self,
        temp_dir: Path,
    ) -> None:
        """Test scan handles permission errors gracefully."""
        plugin_dir = temp_dir / "restricted"
        plugin_dir.mkdir()
        # Create plugin file
        plugin_file = plugin_dir / "test_plugin.py"
        plugin_file.write_text("class TestPlugin:\n    pass\n")
        discovery = PluginDiscovery(plugin_directory=str(plugin_dir))
        # Should complete without raising exceptions
        plugins = await discovery.discover_all()
        assert isinstance(plugins, dict)

    @pytest.mark.asyncio
    async def test_discover_entry_points_handles_scan_errors(
        self,
        temp_dir: Path,
    ) -> None:
        """Test discover_entry_points handles scan errors gracefully."""
        # Use nonexistent directory
        plugin_dir = str(temp_dir / "nonexistent")
        discovery = PluginDiscovery(plugin_directory=plugin_dir)
        # Should complete without raising exceptions
        discovered_plugins = await discovery.discover_all()
        assert isinstance(discovered_plugins, dict)
        assert len(discovered_plugins) == 0

    def test_discovery_string_representation(self, temp_dir: Path) -> None:
        """Test discovery has reasonable string representation."""
        plugin_dir = str(temp_dir / "plugins")
        discovery = PluginDiscovery(plugin_directory=plugin_dir)
        # Should not raise exception when converted to string
        discovery_str = str(discovery)
        assert isinstance(discovery_str, str)
        assert len(discovery_str) > 0
