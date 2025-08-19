"""Comprehensive test suite for flext_plugin.simple_plugin module.

This test module provides complete coverage for the simple plugin system,
testing all classes, methods, and utility functions to achieve 100% code
coverage and validate all functionality in the simple plugin implementation.

Test Coverage:
    - Plugin class: activation, deactivation, lifecycle management
    - PluginRegistry class: registration, unregistration, listing operations
    - Utility functions: load_plugin, create_registry
    - Error handling: all exception scenarios and edge cases
    - Integration: FlextResult patterns and error management

Testing Strategy:
    - Complete method coverage for all public APIs
    - Error condition testing for all exception paths
    - Integration testing with FlextResult patterns
    - Edge case validation and boundary condition testing

Architecture Integration:
    - Tests simple plugin system compatibility with FLEXT ecosystem
    - Validates FlextResult usage patterns throughout simple plugin system
    - Ensures proper error handling and business logic validation
    - Maintains compatibility with Clean Architecture patterns
"""

from __future__ import annotations

from collections import UserDict
from unittest.mock import Mock, patch

import pytest

from flext_plugin import (
    Plugin,
    PluginRegistry,
    create_registry,
    load_plugin,
)


class TestPlugin:
    """Comprehensive test suite for Plugin base class functionality.

    Tests the lightweight plugin base class with essential lifecycle management,
    activation/deactivation capabilities, and FlextResult integration patterns.
    """

    @pytest.fixture
    def plugin(self) -> Plugin:
        """Create plugin instance for testing."""
        return Plugin("test-plugin")

    def test_plugin_initialization(self, plugin: Plugin) -> None:
        """Test plugin initialization with name and default state."""
        assert plugin.name == "test-plugin"
        assert not plugin.active
        assert isinstance(plugin, Plugin)

    def test_plugin_activate_success(self, plugin: Plugin) -> None:
        """Test successful plugin activation."""
        result = plugin.activate()

        assert result.success
        assert result.data is None
        assert plugin.active
        assert result.error is None

    def test_plugin_activate_exception_handling(self) -> None:
        """Test plugin activation exception handling."""

        # Create a plugin that will fail during activation
        class FailingPlugin(Plugin):
            def __setattr__(self, name: str, value: object) -> None:
                if name == "active" and value is True:
                    msg = "Activation failed"
                    raise RuntimeError(msg)
                super().__setattr__(name, value)

        failing_plugin = FailingPlugin("failing-plugin")
        result = failing_plugin.activate()

        assert result.is_failure
        assert "Plugin activation failed" in result.error
        assert "Activation failed" in result.error

    def test_plugin_deactivate_success(self, plugin: Plugin) -> None:
        """Test successful plugin deactivation."""
        # First activate the plugin
        plugin.active = True

        result = plugin.deactivate()

        assert result.success
        assert result.data is None
        assert not plugin.active
        assert result.error is None

    def test_plugin_deactivate_exception_handling(self) -> None:
        """Test plugin deactivation exception handling."""

        # Create a plugin that will fail during deactivation
        class FailingDeactivatePlugin(Plugin):
            def __init__(self, name: str) -> None:
                self.name = name
                # Skip the automatic self.active = False in parent __init__
                self.active = True  # Start as active

            def __setattr__(self, name: str, value: object) -> None:
                if name == "active" and value is False and hasattr(self, "active"):
                    msg = "Deactivation failed"
                    raise ValueError(msg)
                super().__setattr__(name, value)

        failing_plugin = FailingDeactivatePlugin("failing-deactivate-plugin")

        result = failing_plugin.deactivate()

        assert result.is_failure
        assert "Plugin deactivation failed" in result.error
        assert "Deactivation failed" in result.error

    def test_plugin_lifecycle_complete(self, plugin: Plugin) -> None:
        """Test complete plugin lifecycle: inactive -> active -> inactive."""
        # Initial state
        assert not plugin.active

        # Activate
        activate_result = plugin.activate()
        assert activate_result.success
        assert plugin.active

        # Deactivate
        deactivate_result = plugin.deactivate()
        assert deactivate_result.success
        assert not plugin.active

    def test_plugin_multiple_activations(self, plugin: Plugin) -> None:
        """Test multiple activations are handled correctly."""
        # First activation
        result1 = plugin.activate()
        assert result1.success
        assert plugin.active

        # Second activation (should still work)
        result2 = plugin.activate()
        assert result2.success
        assert plugin.active


class TestPluginRegistry:
    """Comprehensive test suite for PluginRegistry management functionality.

    Tests plugin registration, unregistration, retrieval, and listing operations
    with complete error handling and edge case validation.
    """

    @pytest.fixture
    def registry(self) -> PluginRegistry:
        """Create plugin registry for testing."""
        return PluginRegistry()

    @pytest.fixture
    def plugin(self) -> Plugin:
        """Create plugin for registry testing."""
        return Plugin("test-plugin")

    def test_registry_initialization(self, registry: PluginRegistry) -> None:
        """Test registry initialization with empty plugin collection."""
        assert isinstance(registry.plugins, dict)
        assert len(registry.plugins) == 0
        assert registry.list_plugins() == []

    def test_register_plugin_success(
        self,
        registry: PluginRegistry,
        plugin: Plugin,
    ) -> None:
        """Test successful plugin registration."""
        result = registry.register(plugin)

        assert result.success
        assert result.data is None
        assert result.error is None
        assert plugin.name in registry.plugins
        assert registry.plugins[plugin.name] is plugin
        assert plugin.name in registry.list_plugins()

    def test_register_plugin_exception_handling(self) -> None:
        """Test plugin registration exception handling."""

        # Create a registry that will fail during registration
        class FailingRegistry(PluginRegistry):
            def __init__(self) -> None:
                super().__init__()

                # Create a dict that will raise exception on assignment
                class FailingDict(UserDict):
                    def __setitem__(self, key: str, value: object) -> None:
                        msg = "Registration failed"
                        raise RuntimeError(msg)

                self.plugins = FailingDict()

        registry = FailingRegistry()
        plugin = Plugin("test-plugin")

        result = registry.register(plugin)

        assert result.is_failure
        assert "Plugin registration failed" in result.error
        assert "Registration failed" in result.error

    def test_unregister_plugin_success(
        self,
        registry: PluginRegistry,
        plugin: Plugin,
    ) -> None:
        """Test successful plugin unregistration."""
        # First register the plugin
        registry.register(plugin)
        assert plugin.name in registry.plugins

        # Then unregister
        result = registry.unregister(plugin.name)

        assert result.success
        assert result.data is None
        assert result.error is None
        assert plugin.name not in registry.plugins
        assert plugin.name not in registry.list_plugins()

    def test_unregister_nonexistent_plugin(self, registry: PluginRegistry) -> None:
        """Test unregistering plugin that doesn't exist."""
        result = registry.unregister("nonexistent-plugin")

        # Should succeed (graceful handling)
        assert result.success
        assert result.data is None
        assert result.error is None

    def test_unregister_plugin_exception_handling(self) -> None:
        """Test plugin unregistration exception handling."""

        # Create a registry that will fail during unregistration
        class FailingUnregisterRegistry(PluginRegistry):
            def __init__(self) -> None:
                super().__init__()

                # Create a dict that will raise exception on deletion
                class FailingDeleteDict(UserDict):
                    def __delitem__(self, key: str) -> None:
                        msg = "Unregistration failed"
                        raise ValueError(msg)

                self.plugins = FailingDeleteDict()

        registry = FailingUnregisterRegistry()
        plugin = Plugin("test-plugin")

        # Add plugin to the dict directly
        registry.plugins["test-plugin"] = plugin

        result = registry.unregister("test-plugin")

        assert result.is_failure
        assert "Plugin unregistration failed" in result.error
        assert "Unregistration failed" in result.error

    def test_get_plugin_success(self, registry: PluginRegistry, plugin: Plugin) -> None:
        """Test successful plugin retrieval."""
        registry.register(plugin)

        retrieved_plugin = registry.get(plugin.name)

        assert retrieved_plugin is plugin
        assert retrieved_plugin.name == plugin.name

    def test_get_plugin_not_found(self, registry: PluginRegistry) -> None:
        """Test retrieving plugin that doesn't exist."""
        retrieved_plugin = registry.get("nonexistent-plugin")

        assert retrieved_plugin is None

    def test_list_plugins_empty(self, registry: PluginRegistry) -> None:
        """Test listing plugins when registry is empty."""
        plugins = registry.list_plugins()

        assert isinstance(plugins, list)
        assert len(plugins) == 0

    def test_list_plugins_multiple(self, registry: PluginRegistry) -> None:
        """Test listing multiple registered plugins."""
        plugin1 = Plugin("plugin-1")
        plugin2 = Plugin("plugin-2")
        plugin3 = Plugin("plugin-3")

        registry.register(plugin1)
        registry.register(plugin2)
        registry.register(plugin3)

        plugins = registry.list_plugins()

        assert isinstance(plugins, list)
        assert len(plugins) == 3
        assert "plugin-1" in plugins
        assert "plugin-2" in plugins
        assert "plugin-3" in plugins

    def test_registry_multiple_operations(self, registry: PluginRegistry) -> None:
        """Test multiple registry operations in sequence."""
        plugin1 = Plugin("plugin-1")
        plugin2 = Plugin("plugin-2")

        # Register plugins
        result1 = registry.register(plugin1)
        result2 = registry.register(plugin2)
        assert result1.success
        assert result2.success
        assert len(registry.list_plugins()) == 2

        # Retrieve plugins
        assert registry.get("plugin-1") is plugin1
        assert registry.get("plugin-2") is plugin2

        # Unregister one plugin
        unregister_result = registry.unregister("plugin-1")
        assert unregister_result.success
        assert len(registry.list_plugins()) == 1
        assert "plugin-2" in registry.list_plugins()
        assert "plugin-1" not in registry.list_plugins()


class TestUtilityFunctions:
    """Comprehensive test suite for utility functions in simple_plugin module.

    Tests load_plugin and create_registry functions with complete error handling
    and edge case validation to achieve 100% coverage.
    """

    def test_create_registry(self) -> None:
        """Test create_registry utility function."""
        registry = create_registry()

        assert isinstance(registry, PluginRegistry)
        assert isinstance(registry.plugins, dict)
        assert len(registry.plugins) == 0

    def test_create_multiple_registries(self) -> None:
        """Test creating multiple independent registries."""
        registry1 = create_registry()
        registry2 = create_registry()

        assert registry1 is not registry2
        assert registry1.plugins is not registry2.plugins

    @patch("importlib.import_module")
    def test_load_plugin_success(self, mock_import: Mock) -> None:
        """Test successful plugin loading from module."""
        # Create mock module with mock plugin class
        mock_module = Mock()
        mock_plugin_class = Mock()
        mock_plugin_instance = Plugin("loaded-plugin")

        mock_plugin_class.return_value = mock_plugin_instance
        mock_module.Plugin = mock_plugin_class
        mock_import.return_value = mock_module

        result = load_plugin("test_module", "Plugin")

        assert result.success
        assert result.data is mock_plugin_instance
        assert result.error is None
        mock_import.assert_called_once_with("test_module")

    @patch("importlib.import_module")
    def test_load_plugin_custom_class_name(self, mock_import: Mock) -> None:
        """Test loading plugin with custom class name."""
        mock_module = Mock()
        mock_plugin_class = Mock()
        mock_plugin_instance = Plugin("custom-plugin")

        mock_plugin_class.return_value = mock_plugin_instance
        mock_module.CustomPlugin = mock_plugin_class
        mock_import.return_value = mock_module

        result = load_plugin("test_module", "CustomPlugin")

        assert result.success
        assert result.data is mock_plugin_instance
        mock_import.assert_called_once_with("test_module")

    @patch("importlib.import_module")
    def test_load_plugin_import_error(self, mock_import: Mock) -> None:
        """Test plugin loading with import error."""
        mock_import.side_effect = ImportError("Module not found")

        result = load_plugin("nonexistent_module")

        assert result.is_failure
        assert "Module import failed" in result.error
        assert "Module not found" in result.error

    @patch("importlib.import_module")
    def test_load_plugin_attribute_error(self, mock_import: Mock) -> None:
        """Test plugin loading with missing class."""
        mock_module = Mock()
        mock_module.Plugin = Mock(side_effect=AttributeError("Plugin class not found"))
        mock_import.return_value = mock_module

        # Simulate getattr raising AttributeError
        with patch(
            "builtins.getattr",
            side_effect=AttributeError("Plugin class not found"),
        ):
            result = load_plugin("test_module", "Plugin")

        assert result.is_failure
        assert "Plugin class not found" in result.error

    @patch("importlib.import_module")
    def test_load_plugin_runtime_error(self, mock_import: Mock) -> None:
        """Test plugin loading with runtime error during instantiation."""
        mock_module = Mock()
        mock_plugin_class = Mock(
            side_effect=RuntimeError("Plugin instantiation failed"),
        )
        mock_module.Plugin = mock_plugin_class
        mock_import.return_value = mock_module

        result = load_plugin("test_module", "Plugin")

        assert result.is_failure
        assert "Plugin loading failed" in result.error
        assert "Plugin instantiation failed" in result.error

    @patch("importlib.import_module")
    def test_load_plugin_value_error(self, mock_import: Mock) -> None:
        """Test plugin loading with value error during instantiation."""
        mock_module = Mock()
        mock_plugin_class = Mock(side_effect=ValueError("Invalid plugin configuration"))
        mock_module.Plugin = mock_plugin_class
        mock_import.return_value = mock_module

        result = load_plugin("test_module", "Plugin")

        assert result.is_failure
        assert "Plugin loading failed" in result.error
        assert "Invalid plugin configuration" in result.error

    @patch("importlib.import_module")
    def test_load_plugin_type_error(self, mock_import: Mock) -> None:
        """Test plugin loading with type error during instantiation."""
        mock_module = Mock()
        mock_plugin_class = Mock(side_effect=TypeError("Type error in plugin"))
        mock_module.Plugin = mock_plugin_class
        mock_import.return_value = mock_module

        result = load_plugin("test_module", "Plugin")

        assert result.is_failure
        assert "Plugin loading failed" in result.error
        assert "Type error in plugin" in result.error


class TestSimplePluginIntegration:
    """Integration tests for complete simple plugin system workflow.

    Tests end-to-end scenarios combining Plugin, PluginRegistry, and utility
    functions to validate complete system integration and workflow patterns.
    """

    def test_complete_plugin_workflow(self) -> None:
        """Test complete plugin workflow from creation to cleanup."""
        # Create registry
        registry = create_registry()

        # Create and register plugin
        plugin = Plugin("workflow-plugin")
        register_result = registry.register(plugin)
        assert register_result.success

        # Activate plugin
        activate_result = plugin.activate()
        assert activate_result.success
        assert plugin.active

        # Verify plugin in registry
        retrieved_plugin = registry.get("workflow-plugin")
        assert retrieved_plugin is plugin
        assert retrieved_plugin.active

        # List plugins
        plugins = registry.list_plugins()
        assert "workflow-plugin" in plugins

        # Deactivate plugin
        deactivate_result = plugin.deactivate()
        assert deactivate_result.success
        assert not plugin.active

        # Unregister plugin
        unregister_result = registry.unregister("workflow-plugin")
        assert unregister_result.success
        assert len(registry.list_plugins()) == 0

    def test_multiple_plugin_management(self) -> None:
        """Test managing multiple plugins simultaneously."""
        registry = create_registry()

        # Create multiple plugins
        plugins = [Plugin(f"plugin-{i}") for i in range(5)]

        # Register all plugins
        for plugin in plugins:
            result = registry.register(plugin)
            assert result.success

        # Verify all registered
        plugin_names = registry.list_plugins()
        assert len(plugin_names) == 5
        for i in range(5):
            assert f"plugin-{i}" in plugin_names

        # Activate some plugins
        for i in [0, 2, 4]:
            result = plugins[i].activate()
            assert result.success
            assert plugins[i].active

        # Verify inactive plugins remain inactive
        for i in [1, 3]:
            assert not plugins[i].active

        # Clean up
        for plugin in plugins:
            if plugin.active:
                plugin.deactivate()
            registry.unregister(plugin.name)

        assert len(registry.list_plugins()) == 0

    def test_error_resilience_workflow(self) -> None:
        """Test system resilience with various error conditions."""
        registry = create_registry()

        # Test unregistering nonexistent plugin
        result = registry.unregister("nonexistent")
        assert result.success  # Graceful handling

        # Test getting nonexistent plugin
        plugin = registry.get("nonexistent")
        assert plugin is None

        # Test multiple operations on same plugin
        test_plugin = Plugin("resilient-plugin")

        # Multiple registrations
        result1 = registry.register(test_plugin)
        result2 = registry.register(test_plugin)  # Overwrites previous
        assert result1.success
        assert result2.success

        # Multiple activations
        activate1 = test_plugin.activate()
        activate2 = test_plugin.activate()
        assert activate1.success
        assert activate2.success
        assert test_plugin.active

        # Multiple deactivations
        deactivate1 = test_plugin.deactivate()
        deactivate2 = test_plugin.deactivate()
        assert deactivate1.success
        assert deactivate2.success
        assert not test_plugin.active
