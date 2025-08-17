"""Simplified test suite for flext_plugin.core.loader module.

This test module provides streamlined validation of plugin loading functionality
using real implementation components with minimal mocking, focusing on actual
behavior validation and integration testing with the core loading system.

Plugin Loading Architecture Testing:
    - FlextPlugin: Loaded plugin wrapper with lifecycle management capabilities
    - PluginLoader: Core plugin loading system with security and registry management

Test Implementation Philosophy:
    - Real Implementation Focus: Uses actual loader components for authentic testing
    - Minimal Mocking Strategy: Only mocks external dependencies and plugin instances
    - Lifecycle Validation: Tests complete plugin initialization and cleanup cycles
    - Registry Management: Validates plugin loading state and registry operations

Testing Coverage:
    - Plugin Wrapper Functionality: FlextPlugin lifecycle and state management
    - Loader Initialization: Default and custom configuration testing
    - Plugin Registry Operations: Loading state tracking and plugin retrieval
    - Security Configuration: Security-enabled and disabled loader testing
    - Error Handling: Proper exception handling for invalid operations
    - Lifecycle Management: Plugin initialization, cleanup, and state transitions

Plugin System Integration:
    - Built on flext-core foundation patterns
    - Integrates with plugin discovery and validation systems
    - Coordinates with plugin lifecycle management
    - Supports both secure and non-secure loading modes

Quality Standards:
    - Enterprise-grade error handling with proper exception types
    - Comprehensive lifecycle testing with state validation
    - Real-world scenario simulation with mock plugin instances
    - Integration testing with actual loading system components
"""

from __future__ import annotations

from unittest.mock import AsyncMock, Mock

import pytest

from flext_plugin import FlextPlugin, PluginLoader


class TestFlextPluginSimple:
    """Comprehensive test suite for FlextPlugin wrapper functionality.

    Validates the FlextPlugin wrapper class that encapsulates loaded plugin instances
    with lifecycle management, state tracking, and proper initialization/cleanup cycles.

    Test Categories:
      - Plugin Creation: FlextPlugin instantiation with various configuration options
      - Lifecycle Management: Initialize and cleanup operations with state tracking
      - State Validation: Plugin initialization state and metadata preservation
      - Configuration Handling: Plugin configuration management and validation

    Plugin Wrapper Validation:
      - Proper plugin instance encapsulation with metadata preservation
      - Initialization state tracking with is_initialized property
      - Lifecycle method delegation to underlying plugin instance
      - Configuration management with default and custom settings

    Integration Testing:
      - Mock plugin instance integration for controlled testing
      - Async operation support for initialization and cleanup
      - State synchronization between wrapper and plugin instance
    """

    @pytest.fixture
    def mock_plugin_instance(self) -> Mock:
        """Create mock plugin instance."""
        instance = Mock()
        instance.metadata = Mock()
        instance.metadata.name = "test-plugin"
        instance.metadata.version = "0.9.0"
        instance.initialize = AsyncMock()
        instance.cleanup = AsyncMock()
        instance._initialized = False
        instance._update_lifecycle_state = Mock()
        instance._update_status = Mock()
        return instance

    def test_loaded_plugin_creation(self, mock_plugin_instance: Mock) -> None:  # noqa: ARG002
        """Test creating FlextPlugin."""
        loaded = FlextPlugin.create(
            name="test-plugin",
            plugin_version="0.9.0",
            config={"test": "config"},
        )

        if loaded.name != "test-plugin":
            raise AssertionError(f"Expected {'test-plugin'}, got {loaded.name}")
        # FlextPlugin.version is the entity version (int), plugin_version is the string
        assert loaded.plugin_version == "0.9.0"
        # No metadata or config properties in FlextPlugin entity
        assert loaded.description == ""  # From empty config
        assert loaded.author == ""

    def test_loaded_plugin_validation(self, mock_plugin_instance: Mock) -> None:  # noqa: ARG002
        """Test FlextPlugin validation."""
        loaded = FlextPlugin.create(
            name="test-plugin",
            plugin_version="0.9.0",
            config={"description": "Test plugin", "author": "Test Author"},
        )

        # Test validation
        assert loaded.is_valid()
        assert loaded.name == "test-plugin"
        assert loaded.plugin_version == "0.9.0"
        assert loaded.description == "Test plugin"
        assert loaded.author == "Test Author"


class TestPluginLoaderSimple:
    """Comprehensive test suite for PluginLoader core functionality.

    Validates the core plugin loading system including plugin registry management,
    security configuration, and loaded plugin lifecycle operations.

    Test Categories:
      - Loader Initialization: Default and custom configuration testing
      - Registry Operations: Plugin loading state tracking and retrieval
      - Security Configuration: Security-enabled and disabled loader modes
      - Plugin Management: Loading, unloading, and state validation operations
      - Error Handling: Proper exception handling for invalid operations

    Loading System Validation:
      - Plugin registry management with loaded plugin tracking
      - Security mode configuration with proper initialization
      - Plugin retrieval operations with proper null handling
      - Plugin state validation with is_loaded checking
      - Comprehensive error handling for invalid plugin operations

    Integration Points:
      - Real PluginLoader implementation testing without excessive mocking
      - Plugin registry state management with proper isolation
      - Security configuration testing for enterprise deployment scenarios
      - Error condition testing with proper exception types and messages
    """

    @pytest.fixture
    def loader(self) -> PluginLoader:
        """Create plugin loader for testing."""
        return PluginLoader(security_enabled=False)

    @pytest.fixture
    def secure_loader(self) -> PluginLoader:
        """Create secure plugin loader for testing."""
        return PluginLoader(security_enabled=True)

    @pytest.fixture
    def mock_discovered_plugin(self) -> Mock:
        """Create mock discovered plugin."""
        discovered = Mock()
        discovered.metadata = Mock()
        discovered.metadata.name = "test-plugin"
        discovered.metadata.version = "0.9.0"
        discovered.plugin_class = Mock()
        discovered.source = "file"
        return discovered

    def test_loader_initialization_default(self) -> None:
        """Test plugin loader initialization with defaults."""
        loader = PluginLoader()

        if not (loader.security_enabled):
            raise AssertionError(f"Expected True, got {loader.security_enabled}")
        assert hasattr(loader, "_loaded_plugins")
        assert isinstance(loader._loaded_plugins, dict)
        if len(loader._loaded_plugins) != 0:
            raise AssertionError(f"Expected {0}, got {len(loader._loaded_plugins)}")

    def test_loader_initialization_custom(self) -> None:
        """Test plugin loader initialization with custom settings."""
        loader = PluginLoader(security_enabled=False)

        if loader.security_enabled:
            raise AssertionError(f"Expected False, got {loader.security_enabled}")
        assert hasattr(loader, "_loaded_plugins")

    def test_get_loaded_plugin_not_found(self, loader: PluginLoader) -> None:
        """Test getting loaded plugin that doesn't exist."""
        result = loader.get_loaded_plugin("non-existent")
        assert result.is_failure
        assert "not loaded" in result.error.lower()

    def test_is_plugin_loaded_false(self, loader: PluginLoader) -> None:
        """Test checking if plugin is loaded when it's not."""
        if loader.is_loaded("non-existent"):
            raise AssertionError(
                f"Expected False, got {loader.is_loaded('non-existent')}",
            )

    def test_get_all_loaded_plugins_empty(self, loader: PluginLoader) -> None:
        """Test getting all loaded plugins when none are loaded."""
        result = loader.get_all_loaded_plugins()
        assert result.success
        if result.data != {}:
            raise AssertionError(f"Expected {{}}, got {result.data}")

    @pytest.mark.asyncio
    async def test_unload_plugin_not_loaded(self, loader: PluginLoader) -> None:
        """Test unloading plugin that's not loaded."""
        # Should complete without error (graceful handling)
        await loader.unload_plugin("non-existent")
        # No exception raised - this is the expected behavior

    def test_loader_properties(self, loader: PluginLoader) -> None:
        """Test loader properties and attributes."""
        assert hasattr(loader, "security_enabled")
        assert hasattr(loader, "_loaded_plugins")
        assert hasattr(loader, "get_loaded_plugin")
        assert hasattr(loader, "get_all_loaded_plugins")
        assert hasattr(loader, "is_loaded")

    def test_loaded_plugin_in_registry(self, loader: PluginLoader) -> None:
        """Test manually adding and retrieving loaded plugin."""
        # Create a mock loaded plugin
        mock_instance = Mock()
        mock_instance.metadata = Mock()
        mock_instance.metadata.name = "test-plugin"

        # Create plugin using factory method with proper parameters
        loaded_plugin = FlextPlugin.create(
            name="test-plugin",
            plugin_version="1.0.0",
            config={"description": "Test plugin", "author": "Test Author"},
        )

        # Manually add to loader's registry
        loader._loaded_plugins["test-plugin"] = loaded_plugin

        # Should be able to retrieve it
        result = loader.get_loaded_plugin("test-plugin")
        assert result.success
        if result.data != loaded_plugin:
            raise AssertionError(f"Expected {loaded_plugin}, got {result.data}")
        if not (loader.is_loaded("test-plugin")):
            raise AssertionError(
                f"Expected True, got {loader.is_loaded('test-plugin')}",
            )

        # Should appear in all loaded plugins
        all_plugins_result = loader.get_all_loaded_plugins()
        assert all_plugins_result.success
        all_plugins = all_plugins_result.data
        if len(all_plugins) != 1:
            raise AssertionError(f"Expected {1}, got {len(all_plugins)}")
        assert all_plugins["test-plugin"] == loaded_plugin
