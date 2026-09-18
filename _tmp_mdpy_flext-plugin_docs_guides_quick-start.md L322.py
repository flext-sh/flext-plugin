# from flext-plugin/docs/guides/quick-start.md:322
from __future__ import annotations

import pytest
from custom_plugin import GreetingPlugin
from flext_plugin import create_flext_plugin_platform


class TestGreetingPlugin:
    """Test suite for GreetingPlugin."""

    @pytest.fixture
    def plugin(self):
        """Create plugin instance."""
        return GreetingPlugin()

    @pytest.fixture
    def platform(self):
        """Create test platform."""
        platform = create_flext_plugin_platform(settings={"test_mode": True})
        yield platform
        platform.shutdown()

    def test_plugin_creation(self, plugin):
        """Test plugin creation."""
        assert plugin.name == "greeting-generator"
        assert plugin.plugin_version == "0.9.9"
        assert plugin.is_valid()

    def test_plugin_initialization(self, plugin):
        """Test plugin initialization."""
        result = plugin.initialize()
        assert result.success

    def test_greeting_generation(self, plugin):
        """Test greeting generation."""
        plugin.initialize()
        plugin.activate()

        # Test English greeting
        result = plugin.execute({"name": "Test", "language": "english"})
        assert result.success
        assert result.value["greeting"] == "Hello, Test!"

        # Test Spanish greeting
        result = plugin.execute({"name": "Test", "language": "spanish"})
        assert result.success
        assert result.value["greeting"] == "¡Hola, Test!"

    def test_platform_integration(self, platform, plugin):
        """Test plugin integration with platform."""
        # Register plugin
        register_result = platform.register_plugin(plugin)
        assert register_result.success

        # Activate plugin
        activate_result = platform.activate_plugin(plugin.name)
        assert activate_result.success

        # Execute through platform
        execute_result = platform.execute_plugin(
            plugin.name, {"name": "Platform", "language": "english"}
        )
        assert execute_result.success
        assert "Hello, Platform!" in str(execute_result.value)


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])```
Run tests:

