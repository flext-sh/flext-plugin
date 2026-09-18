# from flext-plugin/docs/architecture/implementation.md:417
from __future__ import annotations

# tests/unit/test_entities.py
from flext_plugin import FlextPluginModels


class TestPluginEntity:
    """Test plugin domain entity business rules."""

    def test_plugin_creation_success(self):
        """Test successful plugin creation."""
        plugin = FlextPluginModels.Plugin.create(
            name="test-plugin", plugin_version="1.0.0", settings={"type": "extension"}
        )

        assert plugin.name == "test-plugin"
        assert plugin.plugin_version == "1.0.0"
        assert plugin.status == PluginStatus.INACTIVE

    def test_plugin_validation_business_rules(self):
        """Test plugin business rule validation."""
        # Valid plugin
        plugin = FlextPluginModels.Plugin.create(
            name="valid-plugin", plugin_version="1.0.0", settings={}
        )
        result = plugin.validate_business_rules()
        assert result.success

        # Invalid plugin (empty name)
        plugin = FlextPluginModels.Plugin.create(
            name="", plugin_version="1.0.0", settings={}
        )
        result = plugin.validate_business_rules()
        assert result.failure
        assert "name cannot be empty" in result.error

    def test_plugin_activation_workflow(self):
        """Test plugin activation business workflow."""
        plugin = FlextPluginModels.Plugin.create(
            name="test-plugin", plugin_version="1.0.0", settings={"type": "extension"}
        )

        # Should fail validation initially
        result = plugin.validate_business_rules()
        assert result.failure

        # Fix configuration and activate
        plugin.settings = {"type": "extension", "author": "test"}
        result = plugin.validate_business_rules()
        assert result.success

        activation_result = plugin.activate()
        assert activation_result.success
        assert plugin.status == PluginStatus.ACTIVE```
#### **Application Service Testing**

