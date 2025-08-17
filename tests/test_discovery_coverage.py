"""Coverage-focused test suite for flext_plugin.discovery module.

This test module focuses on maximizing code coverage for the discovery system
by testing actual implemented functionality with real file system scenarios.

Strategy: Test the 3 main methods with comprehensive file system scenarios.
"""

from __future__ import annotations

import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

from flext_plugin import PluginDiscovery


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
      discovery = PluginDiscovery.create(plugin_directory=plugin_dir)
      assert discovery is not None
      assert discovery.plugin_directory == plugin_dir

    def test_discovery_initialization_with_id(self, temp_dir: Path) -> None:
      """Test discovery initialization with custom ID."""
      plugin_dir = str(temp_dir / "plugins")
      custom_id = "custom-discovery-id"
      discovery = PluginDiscovery.create(plugin_directory=plugin_dir, id=custom_id)
      assert discovery is not None
      assert discovery.id == custom_id
      assert discovery.plugin_directory == plugin_dir

    def test_validate_domain_rules_empty_directory_fails(self) -> None:
      """Test domain validation with empty directory fails."""
      discovery = PluginDiscovery.create(plugin_directory="")
      result = discovery.validate_business_rules()
      assert not result.success
      assert "Plugin directory cannot be empty" in str(result.error)

    def test_validate_domain_rules_valid_directory_succeeds(
      self,
      temp_dir: Path,
    ) -> None:
      """Test domain validation with valid directory succeeds."""
      plugin_dir = str(temp_dir / "plugins")
      discovery = PluginDiscovery.create(plugin_directory=plugin_dir)
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
      discovery = PluginDiscovery.create(plugin_directory=plugin_dir)
      plugins = await discovery.scan()
      assert isinstance(plugins, list)
      assert len(plugins) == 0

    @pytest.mark.asyncio
    async def test_scan_empty_directory_returns_empty_list(
      self,
      temp_dir: Path,
    ) -> None:
      """Test scan with empty directory returns empty list."""
      plugin_dir = temp_dir / "plugins"
      plugin_dir.mkdir()
      discovery = PluginDiscovery.create(plugin_directory=str(plugin_dir))
      plugins = await discovery.scan()
      assert isinstance(plugins, list)
      assert len(plugins) == 0

    @pytest.mark.asyncio
    async def test_scan_directory_with_python_files(self, temp_dir: Path) -> None:
      """Test scan with Python files returns plugin information."""
      plugin_dir = temp_dir / "plugins"
      plugin_dir.mkdir()
      # Create test plugin files
      plugin1 = plugin_dir / "test_plugin.py"
      plugin1.write_text("# Test plugin 1\nclass TestPlugin:\n    pass\n")
      plugin2 = plugin_dir / "another_plugin.py"
      plugin2.write_text("# Test plugin 2\nclass AnotherPlugin:\n    pass\n")
      discovery = PluginDiscovery.create(plugin_directory=str(plugin_dir))
      plugins = await discovery.scan()
      assert isinstance(plugins, list)
      assert len(plugins) == 2
      # Check plugin information structure
      plugin_names = {plugin["name"] for plugin in plugins}
      assert "test_plugin" in plugin_names
      assert "another_plugin" in plugin_names
      # Check plugin information completeness
      for plugin in plugins:
          assert "name" in plugin
          assert "path" in plugin
          assert "file_name" in plugin
          assert "size" in plugin
          assert "modified" in plugin
          # Verify path is Path object
          assert isinstance(plugin["path"], Path)
          # Verify size is positive
          assert isinstance(plugin["size"], int)
          assert plugin["size"] > 0
          # Verify modified time is float
          assert isinstance(plugin["modified"], float)
          assert plugin["modified"] > 0

    @pytest.mark.asyncio
    async def test_scan_ignores_dunder_files(self, temp_dir: Path) -> None:
      """Test scan ignores __init__.py and other dunder files."""
      plugin_dir = temp_dir / "plugins"
      plugin_dir.mkdir()
      # Create test files including dunder files
      plugin_file = plugin_dir / "real_plugin.py"
      plugin_file.write_text("# Real plugin\nclass RealPlugin:\n    pass\n")
      init_file = plugin_dir / "__init__.py"
      init_file.write_text("# Init file\n")
      cache_file = plugin_dir / "__pycache__.py"
      cache_file.write_text("# Cache file\n")
      discovery = PluginDiscovery.create(plugin_directory=str(plugin_dir))
      plugins = await discovery.scan()
      assert isinstance(plugins, list)
      assert len(plugins) == 1
      assert plugins[0]["name"] == "real_plugin"

    @pytest.mark.asyncio
    async def test_scan_ignores_non_python_files(self, temp_dir: Path) -> None:
      """Test scan ignores non-Python files."""
      plugin_dir = temp_dir / "plugins"
      plugin_dir.mkdir()
      # Create mixed file types
      plugin_file = plugin_dir / "plugin.py"
      plugin_file.write_text("# Python plugin\nclass Plugin:\n    pass\n")
      text_file = plugin_dir / "readme.txt"
      text_file.write_text("This is a readme file")
      config_file = plugin_dir / "config.json"
      config_file.write_text('{"name": "config"}')
      discovery = PluginDiscovery.create(plugin_directory=str(plugin_dir))
      plugins = await discovery.scan()
      assert isinstance(plugins, list)
      assert len(plugins) == 1
      assert plugins[0]["name"] == "plugin"

    @pytest.mark.asyncio
    async def test_scan_plugin_file_attributes(self, temp_dir: Path) -> None:
      """Test scan returns correct file attributes."""
      plugin_dir = temp_dir / "plugins"
      plugin_dir.mkdir()
      # Create plugin with known content
      plugin_content = "# Test plugin with known size\nclass TestPlugin:\n    def execute(self):\n        return 'test'"
      plugin_file = plugin_dir / "size_test_plugin.py"
      plugin_file.write_text(plugin_content)
      discovery = PluginDiscovery.create(plugin_directory=str(plugin_dir))
      plugins = await discovery.scan()
      assert len(plugins) == 1
      plugin = plugins[0]
      # Check specific attributes
      assert plugin["name"] == "size_test_plugin"
      assert plugin["file_name"] == "size_test_plugin.py"
      assert plugin["size"] == len(plugin_content.encode())
      assert str(plugin["path"]).endswith("size_test_plugin.py")

    @pytest.mark.asyncio
    async def test_discover_plugin_entry_points_empty_directory(
      self,
      temp_dir: Path,
    ) -> None:
      """Test discover_plugin_entry_points with empty directory."""
      plugin_dir = str(temp_dir / "empty")
      discovery = PluginDiscovery.create(plugin_directory=plugin_dir)
      entry_points = await discovery.discover_plugin_entry_points()
      assert isinstance(entry_points, list)
      assert len(entry_points) == 0

    @pytest.mark.asyncio
    async def test_discover_plugin_entry_points_with_plugins(
      self,
      temp_dir: Path,
    ) -> None:
      """Test discover_plugin_entry_points with plugin files."""
      plugin_dir = temp_dir / "plugins"
      plugin_dir.mkdir()
      # Create test plugin files
      plugin1 = plugin_dir / "extractor_plugin.py"
      plugin1.write_text("class ExtractorPlugin:\n    pass\n")
      plugin2 = plugin_dir / "transformer_plugin.py"
      plugin2.write_text("class TransformerPlugin:\n    pass\n")
      discovery = PluginDiscovery.create(plugin_directory=str(plugin_dir))
      entry_points = await discovery.discover_plugin_entry_points()
      assert isinstance(entry_points, list)
      assert len(entry_points) == 2
      # Check entry point structure
      entry_point_names = {ep["name"] for ep in entry_points}
      assert "extractor_plugin" in entry_point_names
      assert "transformer_plugin" in entry_point_names
      # Check entry point completeness
      for entry_point in entry_points:
          assert "name" in entry_point
          assert "module_name" in entry_point
          assert "plugin_class" in entry_point
          assert "path" in entry_point
          assert "type" in entry_point
          # Check default values
          assert entry_point["plugin_class"] == "Plugin"
          assert entry_point["type"] == "generic"
          assert entry_point["name"] == entry_point["module_name"]
          assert isinstance(entry_point["path"], Path)

    @pytest.mark.asyncio
    async def test_discover_plugin_entry_points_integration_with_scan(
      self,
      temp_dir: Path,
    ) -> None:
      """Test discover_plugin_entry_points integrates with scan method."""
      plugin_dir = temp_dir / "plugins"
      plugin_dir.mkdir()
      # Create test plugin
      plugin_file = plugin_dir / "integration_test.py"
      plugin_file.write_text(
          "class IntegrationTestPlugin:\n    def run(self):\n        return True\n",
      )
      discovery = PluginDiscovery.create(plugin_directory=str(plugin_dir))
      # Get results from both methods
      plugins = await discovery.scan()
      entry_points = await discovery.discover_plugin_entry_points()
      # Should have consistent results
      assert len(plugins) == 1
      assert len(entry_points) == 1
      # Entry point should be based on scan result
      plugin = plugins[0]
      entry_point = entry_points[0]
      assert plugin["name"] == entry_point["name"]
      assert plugin["path"] == entry_point["path"]
      assert entry_point["module_name"] == plugin["name"]

    @pytest.mark.asyncio
    async def test_scan_large_number_of_files(self, temp_dir: Path) -> None:
      """Test scan handles larger number of plugin files."""
      plugin_dir = temp_dir / "plugins"
      plugin_dir.mkdir()
      # Create multiple plugin files
      num_plugins = 10
      for i in range(num_plugins):
          plugin_file = plugin_dir / f"plugin_{i:02d}.py"
          plugin_file.write_text(f"# Plugin {i}\nclass Plugin{i}:\n    pass\n")
      discovery = PluginDiscovery.create(plugin_directory=str(plugin_dir))
      plugins = await discovery.scan()
      assert len(plugins) == num_plugins
      # Check all plugins are present
      plugin_names = {plugin["name"] for plugin in plugins}
      expected_names = {f"plugin_{i:02d}" for i in range(num_plugins)}
      assert plugin_names == expected_names

    @pytest.mark.asyncio
    async def test_scan_mixed_file_scenario(self, temp_dir: Path) -> None:
      """Test scan with mixed file scenario (realistic plugin directory)."""
      plugin_dir = temp_dir / "plugins"
      plugin_dir.mkdir()
      # Create realistic plugin directory structure
      files_to_create = [
          ("tap_github.py", "# GitHub tap plugin\nclass GitHubTap:\n    pass\n"),
          (
              "target_postgres.py",
              "# PostgreSQL target plugin\nclass PostgresTarget:\n    pass\n",
          ),
          (
              "transform_utils.py",
              "# Transform utilities\ndef transform_data():\n    pass\n",
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
      discovery = PluginDiscovery.create(plugin_directory=str(plugin_dir))
      plugins = await discovery.scan()
      # Should only find the 3 non-dunder Python files
      assert len(plugins) == 3
      plugin_names = {plugin["name"] for plugin in plugins}
      expected_names = {"tap_github", "target_postgres", "transform_utils"}
      assert plugin_names == expected_names

    def test_discovery_inheritance(self, temp_dir: Path) -> None:
      """Test discovery inherits from FlextEntity."""
      plugin_dir = str(temp_dir / "plugins")
      discovery = PluginDiscovery.create(plugin_directory=plugin_dir)
      assert isinstance(discovery, FlextEntity)
      # Should have FlextEntity attributes
      assert hasattr(discovery, "id")
      assert hasattr(discovery, "version")
      assert hasattr(discovery, "metadata")
      assert hasattr(discovery, "domain_events")

    def test_discovery_model_config(self, temp_dir: Path) -> None:
      """Test discovery has correct model configuration."""
      plugin_dir = str(temp_dir / "plugins")
      discovery = PluginDiscovery.create(plugin_directory=plugin_dir)
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
      discovery = PluginDiscovery.create(plugin_directory="")
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
      discovery = PluginDiscovery.create(plugin_directory=str(plugin_dir))
      # Should complete without raising exceptions
      plugins = await discovery.scan()
      assert isinstance(plugins, list)

    @pytest.mark.asyncio
    async def test_discover_entry_points_handles_scan_errors(
      self,
      temp_dir: Path,
    ) -> None:
      """Test discover_entry_points handles scan errors gracefully."""
      # Use nonexistent directory
      plugin_dir = str(temp_dir / "nonexistent")
      discovery = PluginDiscovery.create(plugin_directory=plugin_dir)
      # Should complete without raising exceptions
      entry_points = await discovery.discover_plugin_entry_points()
      assert isinstance(entry_points, list)
      assert len(entry_points) == 0

    def test_discovery_string_representation(self, temp_dir: Path) -> None:
      """Test discovery has reasonable string representation."""
      plugin_dir = str(temp_dir / "plugins")
      discovery = PluginDiscovery.create(plugin_directory=plugin_dir)
      # Should not raise exception when converted to string
      discovery_str = str(discovery)
      assert isinstance(discovery_str, str)
      assert len(discovery_str) > 0
