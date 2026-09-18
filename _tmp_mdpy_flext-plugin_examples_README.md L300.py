# from flext-plugin/examples/README.md:300
from __future__ import annotations

import pytest
from flext_plugin import create_flext_plugin_platform
from your_plugin import ExamplePlugin


class TestExamplePlugin:
    """Test suite template for plugins."""

    @pytest.fixture
    def plugin(self):
        """Create plugin instance for testing."""
        return ExamplePlugin()

    @pytest.fixture
    def platform(self):
        """Create test platform."""
        platform = create_flext_plugin_platform(settings={"test_mode": True})
        yield platform
        platform.shutdown()

    def test_plugin_creation(self, plugin):
        """Test plugin creation."""
        assert plugin.name == "example-plugin"
        assert plugin.plugin_version == "0.12.0-dev"
        assert plugin.is_valid()

    def test_plugin_initialization(self, plugin):
        """Test plugin initialization."""
        result = plugin.initialize()
        assert result.success

    def test_plugin_execution(self, plugin):
        """Test plugin execution."""
        # Initialize first
        plugin.initialize()
        plugin.activate()

        # Test execution
        test_data = {"input": "test_value"}
        result = plugin.execute(test_data)

        assert result.success
        assert "processed" in result.value

    def test_plugin_lifecycle(self, platform, plugin):
        """Test complete plugin lifecycle."""
        # Register plugin
        register_result = platform.register_plugin(plugin)
        assert register_result.success

        # Activate plugin
        activate_result = platform.activate_plugin(plugin.name)
        assert activate_result.success

        # Execute plugin
        execute_result = platform.execute_plugin(plugin.name, {"test": "data"})
        assert execute_result.success

        # Deactivate plugin
        deactivate_result = platform.deactivate_plugin(plugin.name)
        assert deactivate_result.success
