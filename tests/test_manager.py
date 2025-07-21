"""Tests for flext_plugin.manager module.

Comprehensive tests for plugin manager functionality.
"""

from __future__ import annotations

from unittest.mock import Mock, patch

import pytest
from flext_core.domain.types import ServiceResult

from flext_plugin.core.types import PluginType
from flext_plugin.manager import (
    PluginConfiguration,
    PluginExecutionContext,
    PluginManager,
    PluginManagerResult,
    SimplePluginRegistry,
    create_plugin_manager,
)


class TestSimplePluginRegistry:
    """Test SimplePluginRegistry functionality."""

    @pytest.fixture
    def registry(self) -> SimplePluginRegistry:
        """Create registry for testing."""
        return SimplePluginRegistry()

    @pytest.fixture
    def mock_plugin(self) -> Mock:
        """Create mock plugin for testing."""
        plugin = Mock()
        plugin.metadata = Mock()
        plugin.metadata.name = "test-plugin"
        return plugin

    async def test_register_plugin_success(
        self,
        registry: SimplePluginRegistry,
        mock_plugin: Mock,
    ) -> None:
        """Test successful plugin registration."""
        result = await registry.register_plugin(mock_plugin)

        assert result.is_success
        assert result.data == mock_plugin
        assert registry.get_plugin("test-plugin") == mock_plugin
        assert registry.get_plugin_count() == 1

    async def test_register_plugin_failure(
        self,
        registry: SimplePluginRegistry,
    ) -> None:
        """Test failed plugin registration."""
        # Plugin without metadata should fail
        invalid_plugin = Mock()
        invalid_plugin.metadata = None

        result = await registry.register_plugin(invalid_plugin)

        assert not result.is_success
        assert result.error is not None
        assert "registration failed" in result.error.lower()
        assert registry.get_plugin_count() == 0

    async def test_unregister_plugin(
        self,
        registry: SimplePluginRegistry,
        mock_plugin: Mock,
    ) -> None:
        """Test plugin unregistration."""
        # First register a plugin
        await registry.register_plugin(mock_plugin)
        assert registry.get_plugin_count() == 1

        # Then unregister it
        result = await registry.unregister_plugin("test-plugin")

        assert result.is_success
        assert result.data is True
        assert registry.get_plugin("test-plugin") is None
        assert registry.get_plugin_count() == 0

    async def test_unregister_nonexistent_plugin(
        self,
        registry: SimplePluginRegistry,
    ) -> None:
        """Test unregistering non-existent plugin."""
        result = await registry.unregister_plugin("non-existent")

        # Should still succeed (idempotent operation)
        assert result.is_success
        assert result.data is True

    def test_list_plugins(self, registry: SimplePluginRegistry) -> None:
        """Test listing plugins."""
        # Empty registry
        plugins = registry.list_plugins()
        assert len(plugins) == 0

    def test_list_plugins_with_type_filter(
        self,
        registry: SimplePluginRegistry,
    ) -> None:
        """Test listing plugins with type filter."""
        # Create mock plugins with different types
        tap_plugin = Mock()
        tap_plugin.metadata = Mock()
        tap_plugin.metadata.name = "tap-plugin"
        tap_plugin.metadata.plugin_type = PluginType.TAP

        target_plugin = Mock()
        target_plugin.metadata = Mock()
        target_plugin.metadata.name = "target-plugin"
        target_plugin.metadata.plugin_type = PluginType.TARGET

        # Register plugins
        registry._plugins["tap-plugin"] = tap_plugin
        registry._plugins["target-plugin"] = target_plugin

        # Test filtering
        all_plugins = registry.list_plugins()
        assert len(all_plugins) == 2

        tap_plugins = registry.list_plugins(PluginType.TAP)
        assert len(tap_plugins) == 1
        assert tap_plugins[0].name == "tap-plugin"

    async def test_cleanup_all(
        self,
        registry: SimplePluginRegistry,
        mock_plugin: Mock,
    ) -> None:
        """Test cleaning up all plugins."""
        await registry.register_plugin(mock_plugin)
        assert registry.get_plugin_count() == 1

        await registry.cleanup_all()
        assert registry.get_plugin_count() == 0


class TestPluginConfiguration:
    """Test PluginConfiguration model."""

    def test_configuration_creation(self) -> None:
        """Test creating plugin configuration."""
        config = PluginConfiguration(
            plugin_id="test-plugin",
            enabled=True,
            configuration={"key": "value"},
            permissions=["read", "write"],
            auto_load=False,
            hot_reload=True,
            priority=50,
        )

        assert config.plugin_id == "test-plugin"
        assert config.enabled is True
        assert config.configuration == {"key": "value"}
        assert config.permissions == ["read", "write"]
        assert config.auto_load is False
        assert config.hot_reload is True
        assert config.priority == 50

    def test_configuration_defaults(self) -> None:
        """Test default configuration values."""
        config = PluginConfiguration(plugin_id="test-plugin")

        assert config.plugin_id == "test-plugin"
        assert config.enabled is True
        assert config.configuration == {}
        assert config.permissions == []
        assert config.auto_load is True
        assert config.hot_reload is False
        assert config.priority == 100


class TestPluginExecutionContext:
    """Test PluginExecutionContext model."""

    def test_execution_context_creation(self) -> None:
        """Test creating execution context."""
        context = PluginExecutionContext(
            plugin_id="test-plugin",
            execution_id="exec-123",
            input_data={"test": "data"},
            context={"env": "test"},
            timeout_seconds=30,
        )

        assert context.plugin_id == "test-plugin"
        assert context.execution_id == "exec-123"
        assert context.input_data == {"test": "data"}
        assert context.context == {"env": "test"}
        assert context.timeout_seconds == 30

    def test_execution_context_defaults(self) -> None:
        """Test default execution context values."""
        context = PluginExecutionContext(
            plugin_id="test-plugin",
            execution_id="exec-123",
        )

        assert context.plugin_id == "test-plugin"
        assert context.execution_id == "exec-123"
        assert context.input_data == {}
        assert context.context == {}
        assert context.timeout_seconds is None


class TestPluginManagerResult:
    """Test PluginManagerResult model."""

    def test_manager_result_creation(self) -> None:
        """Test creating manager result."""
        result = PluginManagerResult(
            operation="initialize",
            success=True,
            plugins_affected=["plugin1", "plugin2"],
            execution_time_ms=150.5,
            details={"plugins_loaded": 2},
            errors=[],
        )

        assert result.operation == "initialize"
        assert result.success is True
        assert result.plugins_affected == ["plugin1", "plugin2"]
        assert result.execution_time_ms == 150.5
        assert result.details == {"plugins_loaded": 2}
        assert result.errors == []

    def test_manager_result_with_errors(self) -> None:
        """Test manager result with errors."""
        result = PluginManagerResult(
            operation="load_plugins",
            success=False,
            plugins_affected=[],
            execution_time_ms=50.0,
            details={},
            errors=["Plugin not found", "Invalid configuration"],
        )

        assert result.operation == "load_plugins"
        assert result.success is False
        assert result.errors == ["Plugin not found", "Invalid configuration"]


class TestPluginManager:
    """Test PluginManager functionality."""

    @pytest.fixture
    def manager(self) -> PluginManager:
        """Create plugin manager for testing."""
        return PluginManager(auto_discover=False, security_enabled=False)

    async def test_manager_initialization(self, manager: PluginManager) -> None:
        """Test plugin manager initialization."""
        assert not manager.is_initialized

        result = await manager.initialize()

        assert result.is_success
        assert manager.is_initialized
        assert isinstance(result.data, PluginManagerResult)  # type: ignore[unreachable]
        assert result.data.operation == "initialize"

    async def test_manager_initialization_with_auto_discover(self) -> None:
        """Test manager initialization with auto-discovery."""
        manager = PluginManager(auto_discover=True, security_enabled=False)

        # Mock the discovery method to avoid actual file system operations
        with patch.object(manager, "discover_and_load_plugins") as mock_discover:
            mock_discover.return_value = ServiceResult.ok(
                PluginManagerResult(
                    operation="discover_and_load",
                    success=True,
                    plugins_affected=["test-plugin"],
                    execution_time_ms=100.0,
                    details={"plugins_discovered": 1},
                    errors=[],
                ),
            )

            result = await manager.initialize()

            assert result.is_success
            assert manager.is_initialized
            mock_discover.assert_called_once()

    async def test_discover_and_load_plugins_empty(
        self,
        manager: PluginManager,
    ) -> None:
        """Test discovering plugins when none are available."""
        # Mock discovery to return empty results
        with patch.object(manager.discovery, "discover_all") as mock_discover:
            mock_discover.return_value = {}

            result = await manager.discover_and_load_plugins()

            assert not result.is_success
            assert result.error is not None
        assert result.error is not None
        assert "No plugins discovered" in result.error

    async def test_execute_plugin_not_found(self, manager: PluginManager) -> None:
        """Test executing non-existent plugin."""
        await manager.initialize()

        result = await manager.execute_plugin(
            "non-existent-plugin",
            {"test": "data"},
        )

        assert not result.is_success
        assert result.error is not None
        assert "not found" in result.error.lower()

    async def test_configure_plugin_not_found(self, manager: PluginManager) -> None:
        """Test configuring non-existent plugin."""
        await manager.initialize()

        config = PluginConfiguration(plugin_id="non-existent")
        result = await manager.configure_plugin("non-existent", config)

        assert not result.is_success
        assert result.error is not None
        assert "not found" in result.error.lower()

    async def test_reload_plugin_not_configured(self, manager: PluginManager) -> None:
        """Test reloading plugin that doesn't exist."""
        await manager.initialize()

        result = await manager.reload_plugin("test-plugin")

        assert not result.is_success
        assert result.error is not None
        assert "not discovered" in result.error.lower()

    async def test_unload_plugin_not_found(self, manager: PluginManager) -> None:
        """Test unloading non-existent plugin."""
        await manager.initialize()

        result = await manager.unload_plugin("non-existent")

        assert not result.is_success
        assert result.error is not None
        assert "plugin unload failed" in result.error.lower()

    async def test_integrate_with_protocols(self, manager: PluginManager) -> None:
        """Test protocol integration."""
        await manager.initialize()

        result = await manager.integrate_with_protocols()

        # Should succeed as it's currently a placeholder
        assert result.is_success

    def test_get_plugin_status_not_found(self, manager: PluginManager) -> None:
        """Test getting status of non-existent plugin."""
        status = manager.get_plugin_status("non-existent")
        assert status == {"status": "not_found"}

    def test_list_plugins_empty(self, manager: PluginManager) -> None:
        """Test listing plugins when registry is empty."""
        plugins = manager.list_plugins()
        assert plugins == []

    def test_list_plugins_enabled_only(self, manager: PluginManager) -> None:
        """Test listing only enabled plugins."""
        plugins = manager.list_plugins(enabled_only=True)
        assert plugins == []

    async def test_cleanup(self, manager: PluginManager) -> None:
        """Test plugin manager cleanup."""
        await manager.initialize()
        assert manager.is_initialized

        await manager.cleanup()
        assert not manager.is_initialized

    def test_plugin_count_property(self, manager: PluginManager) -> None:
        """Test plugin count property."""
        assert manager.plugin_count == 0

    async def test_create_plugin_context(self, manager: PluginManager) -> None:
        """Test creating plugin context."""
        context = await manager._create_plugin_context("test-plugin")

        assert context.plugin_name == "test-plugin"
        assert context.services == {}
        assert context.dependencies == {}
        assert context.permissions == ["read", "execute"]
        assert context.security_level == "standard"


class TestCreatePluginManager:
    """Test plugin manager factory function."""

    def test_create_plugin_manager_defaults(self) -> None:
        """Test creating plugin manager with defaults."""
        manager = create_plugin_manager()

        assert isinstance(manager, PluginManager)
        assert manager.auto_discover is True
        assert manager.security_enabled is True

    def test_create_plugin_manager_custom_settings(self) -> None:
        """Test creating plugin manager with custom settings."""
        manager = create_plugin_manager(
            container=None,
            auto_discover=False,
            security_enabled=False,
        )

        assert isinstance(manager, PluginManager)
        assert manager.auto_discover is False
        assert manager.security_enabled is False
