"""REAL test suite for flext_plugin.simple_plugin module.

This test module provides complete coverage for the simple plugin system
using REAL plugin classes and functionality without ANY mocks.

Testing Strategy - REAL FUNCTIONALITY ONLY:
    - Plugin class: REAL activation, deactivation, lifecycle management
    - PluginRegistry class: REAL registration, unregistration, listing operations
    - Utility functions: REAL load_plugin and create_registry with actual modules
    - Error handling: REAL exception scenarios with genuine edge cases
    - Integration: REAL FlextResult patterns and error management

Real Component Testing:
    - Plugin: REAL lifecycle with actual state management
    - PluginRegistry: REAL plugin storage and retrieval operations
    - load_plugin(): REAL dynamic module loading with actual Python files
    - create_registry(): REAL registry instantiation

Real Integration Testing:
    - REAL plugin class hierarchies and inheritance
    - Actual FlextResult success and failure patterns
    - REAL error handling with genuine exceptions
    - Complete edge case validation with real scenarios

Quality Standards:
    - 100% code coverage through REAL functionality testing
    - NO MOCKS - only real plugin classes and actual business logic
    - Enterprise-grade error handling validation
    - Complete integration testing with real plugin scenarios
"""

from __future__ import annotations

import sys
import tempfile
from collections import UserDict
from pathlib import Path
from typing import override

import pytest

from flext_plugin.simple_plugin import (
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
            @override
            def __setattr__(self, name: str, value: object) -> None:
                if name == "active" and value is True:
                    msg = "Activation failed"
                    raise RuntimeError(msg)
                super().__setattr__(name, value)

        failing_plugin = FailingPlugin("failing-plugin")
        result = failing_plugin.activate()

        assert result.is_failure
        assert result.error is not None
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

            @override
            def __setattr__(self, name: str, value: object) -> None:
                if name == "active" and value is False and hasattr(self, "active"):
                    msg = "Deactivation failed"
                    raise ValueError(msg)
                super().__setattr__(name, value)

        failing_plugin = FailingDeactivatePlugin("failing-deactivate-plugin")

        result = failing_plugin.deactivate()

        assert result.is_failure
        assert result.error is not None
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
                class FailingDict(UserDict[str, Plugin]):
                    @override
                    def __setitem__(self, key: str, value: Plugin) -> None:
                        msg = "Registration failed"
                        raise RuntimeError(msg)

                self.plugins = FailingDict()

        registry = FailingRegistry()
        plugin = Plugin("test-plugin")

        result = registry.register(plugin)

        assert result.is_failure
        assert result.error is not None
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
                class FailingDeleteDict(UserDict[str, Plugin]):
                    @override
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
        assert result.error is not None
        assert "Plugin unregistration failed" in result.error
        assert "Unregistration failed" in result.error

    def test_get_plugin_success(self, registry: PluginRegistry, plugin: Plugin) -> None:
        """Test successful plugin retrieval."""
        registry.register(plugin)

        retrieved_plugin = registry.get(plugin.name)

        assert retrieved_plugin is plugin
        assert retrieved_plugin is not None  # For pyright
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

    def test_load_plugin_success_with_real_module(self) -> None:
        """Test successful plugin loading from REAL module with actual file system."""
        # Create REAL temporary module file
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            module_file = temp_path / "test_real_plugin.py"

            # Write REAL plugin module content
            module_file.write_text('''
"""REAL test plugin module."""

from flext_plugin.simple_plugin import Plugin

class Plugin(Plugin):
    """REAL plugin implementation."""

    def __init__(self):
        super().__init__("real-loaded-plugin")
        self.loaded = True

    def execute(self):
        return f"REAL execution from {self.name}"
''')

            # Add temp directory to Python path temporarily

            sys.path.insert(0, str(temp_path))

            try:
                result = load_plugin("test_real_plugin", "Plugin")

                assert result.success
                assert result.data is not None
                assert isinstance(result.data, Plugin)
                assert result.data.name == "real-loaded-plugin"
                assert result.error is None
                assert hasattr(result.data, "loaded")
                assert result.data.loaded is True
            finally:
                # Clean up path
                sys.path.remove(str(temp_path))
                # Remove module from cache
                if "test_real_plugin" in sys.modules:
                    del sys.modules["test_real_plugin"]

    def test_load_plugin_custom_class_name_with_real_module(self) -> None:
        """Test loading plugin with custom class name from REAL module."""
        # Create REAL temporary module file with custom class name
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            module_file = temp_path / "test_custom_plugin.py"

            # Write REAL plugin module content with custom class name
            module_file.write_text('''
"""REAL test plugin module with custom class name."""

from flext_plugin.simple_plugin import Plugin

class CustomPlugin(Plugin):
    """REAL plugin implementation with custom name."""

    def __init__(self):
        super().__init__("custom-named-plugin")
        self.custom_attribute = "custom_value"

    def custom_method(self):
        return f"Custom method from {self.name}"
''')

            # Add temp directory to Python path temporarily

            sys.path.insert(0, str(temp_path))

            try:
                result = load_plugin("test_custom_plugin", "CustomPlugin")

                assert result.success
                assert result.data is not None
                assert isinstance(result.data, Plugin)
                assert result.data.name == "custom-named-plugin"
                assert result.error is None
                assert hasattr(result.data, "custom_attribute")
                assert result.data.custom_attribute == "custom_value"
            finally:
                # Clean up path
                sys.path.remove(str(temp_path))
                # Remove module from cache
                if "test_custom_plugin" in sys.modules:
                    del sys.modules["test_custom_plugin"]

    def test_load_plugin_import_error_with_real_nonexistent_module(self) -> None:
        """Test plugin loading with import error from REAL nonexistent module."""
        result = load_plugin("totally_nonexistent_module_that_does_not_exist")

        assert result.is_failure
        assert result.error is not None
        assert "Module import failed" in result.error
        assert "No module named" in result.error

    def test_load_plugin_attribute_error_with_real_missing_class(self) -> None:
        """Test plugin loading with missing class from REAL module."""
        # Create REAL temporary module file without Plugin class
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            module_file = temp_path / "test_no_plugin_class.py"

            # Write REAL module content without Plugin class
            module_file.write_text('''
"""REAL test module without Plugin class."""

def some_function():
    return "This module has no Plugin class"

class SomeOtherClass:
    pass
''')

            # Add temp directory to Python path temporarily

            sys.path.insert(0, str(temp_path))

            try:
                result = load_plugin("test_no_plugin_class", "Plugin")

                assert result.is_failure
                assert result.error is not None
                assert "Plugin class not found" in result.error
            finally:
                # Clean up path
                sys.path.remove(str(temp_path))
                # Remove module from cache
                if "test_no_plugin_class" in sys.modules:
                    del sys.modules["test_no_plugin_class"]

    def test_load_plugin_runtime_error_with_real_failing_plugin(self) -> None:
        """Test plugin loading with runtime error during instantiation from REAL plugin."""
        # Create REAL temporary module file with failing plugin class
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            module_file = temp_path / "test_failing_plugin.py"

            # Write REAL plugin module content that fails during instantiation
            module_file.write_text('''
"""REAL test plugin module with failing initialization."""

from flext_plugin.simple_plugin import Plugin

class Plugin(Plugin):
    """REAL plugin implementation that fails during instantiation."""

    def __init__(self):
        raise RuntimeError("Plugin instantiation failed")
''')

            # Add temp directory to Python path temporarily

            sys.path.insert(0, str(temp_path))

            try:
                result = load_plugin("test_failing_plugin", "Plugin")

                assert result.is_failure
                assert result.error is not None
                assert "Plugin loading failed" in result.error
                assert "Plugin instantiation failed" in result.error
            finally:
                # Clean up path
                sys.path.remove(str(temp_path))
                # Remove module from cache
                if "test_failing_plugin" in sys.modules:
                    del sys.modules["test_failing_plugin"]

    def test_load_plugin_value_error_with_real_invalid_plugin(self) -> None:
        """Test plugin loading with value error during instantiation from REAL plugin."""
        # Create REAL temporary module file with invalid plugin class
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            module_file = temp_path / "test_invalid_plugin.py"

            # Write REAL plugin module content with validation error
            module_file.write_text('''
"""REAL test plugin module with invalid configuration."""

from flext_plugin.simple_plugin import Plugin

class Plugin(Plugin):
    """REAL plugin implementation with invalid configuration."""

    def __init__(self):
        raise ValueError("Invalid plugin configuration")
''')

            # Add temp directory to Python path temporarily

            sys.path.insert(0, str(temp_path))

            try:
                result = load_plugin("test_invalid_plugin", "Plugin")

                assert result.is_failure
                assert result.error is not None
                assert "Plugin loading failed" in result.error
                assert "Invalid plugin configuration" in result.error
            finally:
                # Clean up path
                sys.path.remove(str(temp_path))
                # Remove module from cache
                if "test_invalid_plugin" in sys.modules:
                    del sys.modules["test_invalid_plugin"]

    def test_load_plugin_type_error_with_real_type_error_plugin(self) -> None:
        """Test plugin loading with type error during instantiation from REAL plugin."""
        # Create REAL temporary module file with type error plugin class
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            module_file = temp_path / "test_type_error_plugin.py"

            # Write REAL plugin module content with type error
            module_file.write_text('''
"""REAL test plugin module with type error."""

from flext_plugin.simple_plugin import Plugin

class Plugin(Plugin):
    """REAL plugin implementation with type error."""

    def __init__(self):
        raise TypeError("Type error in plugin")
''')

            # Add temp directory to Python path temporarily

            sys.path.insert(0, str(temp_path))

            try:
                result = load_plugin("test_type_error_plugin", "Plugin")

                assert result.is_failure
                assert result.error is not None
                assert "Plugin loading failed" in result.error
                assert "Type error in plugin" in result.error
            finally:
                # Clean up path
                sys.path.remove(str(temp_path))
                # Remove module from cache
                if "test_type_error_plugin" in sys.modules:
                    del sys.modules["test_type_error_plugin"]


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
        assert retrieved_plugin is not None  # For pyright
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
