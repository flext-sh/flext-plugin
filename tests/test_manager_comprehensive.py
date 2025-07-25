"""Comprehensive tests for flext_plugin.manager module.

Tests for plugin manager functionality covering all methods and edge cases.
"""

from __future__ import annotations

from unittest.mock import Mock, patch

import pytest

# 🚨 ARCHITECTURAL COMPLIANCE: Using módulo raiz imports
from flext_core import FlextResult

from flext_plugin.core.types import PluginType
from flext_plugin.manager import (
    PluginConfiguration,
    PluginExecutionContext,
    PluginManager,
    PluginManagerResult,
    SimplePluginRegistry,
    create_plugin_manager,
)


class TestSimplePluginRegistryComprehensive:
    """Comprehensive test SimplePluginRegistry functionality."""

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
        plugin.metadata.plugin_type = PluginType.TAP
        return plugin

    @pytest.fixture
    def mock_plugin_2(self) -> Mock:
        """Create second mock plugin for testing."""
        plugin = Mock()
        plugin.metadata = Mock()
        plugin.metadata.name = "test-plugin-2"
        plugin.metadata.plugin_type = PluginType.TARGET
        return plugin

    async def test_register_plugin_success(
        self,
        registry: SimplePluginRegistry,
        mock_plugin: Mock,
    ) -> None:
        """Test successful plugin registration."""
        result = await registry.register_plugin(mock_plugin)

        assert result.success
        assert result.data == mock_plugin
        assert registry.get_plugin("test-plugin") == mock_plugin
        assert registry.get_plugin_count() == 1

    async def test_register_multiple_plugins(
        self,
        registry: SimplePluginRegistry,
        mock_plugin: Mock,
        mock_plugin_2: Mock,
    ) -> None:
        """Test registering multiple plugins."""
        # Register first plugin
        result1 = await registry.register_plugin(mock_plugin)
        assert result1.is_success
        assert registry.get_plugin_count() == 1

        # Register second plugin
        result2 = await registry.register_plugin(mock_plugin_2)
        assert result2.is_success
        assert registry.get_plugin_count() == 2

        # Both should be retrievable
        assert registry.get_plugin("test-plugin") == mock_plugin
        assert registry.get_plugin("test-plugin-2") == mock_plugin_2

    async def test_register_plugin_without_metadata(
        self,
        registry: SimplePluginRegistry,
    ) -> None:
        """Test failed plugin registration without metadata."""
        invalid_plugin = Mock()
        invalid_plugin.metadata = None

        result = await registry.register_plugin(invalid_plugin)

        assert not result.success
        assert result.error is not None
        assert "registration failed" in result.error.lower()
        assert registry.get_plugin_count() == 0

    async def test_register_plugin_without_name(
        self,
        registry: SimplePluginRegistry,
    ) -> None:
        """Test failed plugin registration without name."""
        invalid_plugin = Mock()
        invalid_plugin.metadata = Mock()
        # Don't set name attribute to trigger AttributeError
        del invalid_plugin.metadata.name

        result = await registry.register_plugin(invalid_plugin)

        assert not result.success
        assert result.error is not None
        assert "registration failed" in result.error.lower()
        assert registry.get_plugin_count() == 0

    async def test_unregister_plugin_success(
        self,
        registry: SimplePluginRegistry,
        mock_plugin: Mock,
    ) -> None:
        """Test successful plugin unregistration."""
        # First register a plugin
        await registry.register_plugin(mock_plugin)
        assert registry.get_plugin_count() == 1

        # Then unregister it
        result = await registry.unregister_plugin("test-plugin")

        assert result.success
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
        assert result.success
        assert result.data is True

    def test_get_plugin_nonexistent(self, registry: SimplePluginRegistry) -> None:
        """Test getting non-existent plugin."""
        result = registry.get_plugin("non-existent")
        assert result is None

    def test_list_plugins_empty(self, registry: SimplePluginRegistry) -> None:
        """Test listing plugins when registry is empty."""
        plugins = registry.list_plugins()
        assert len(plugins) == 0

    def test_list_plugins_with_plugins(
        self,
        registry: SimplePluginRegistry,
        mock_plugin: Mock,
        mock_plugin_2: Mock,
    ) -> None:
        """Test listing plugins with registered plugins."""
        # Register plugins directly in the registry
        registry._plugins["test-plugin"] = mock_plugin
        registry._plugins["test-plugin-2"] = mock_plugin_2

        # Test listing all plugins
        all_plugins = registry.list_plugins()
        assert len(all_plugins) == 2

        # Should return metadata objects
        plugin_names = [p.name for p in all_plugins]
        assert "test-plugin" in plugin_names
        assert "test-plugin-2" in plugin_names

    def test_list_plugins_with_type_filter(
        self,
        registry: SimplePluginRegistry,
        mock_plugin: Mock,
        mock_plugin_2: Mock,
    ) -> None:
        """Test listing plugins with type filter."""
        # Register plugins directly in the registry
        registry._plugins["test-plugin"] = mock_plugin
        registry._plugins["test-plugin-2"] = mock_plugin_2

        # Test filtering by TAP type
        tap_plugins = registry.list_plugins(PluginType.TAP)
        assert len(tap_plugins) == 1
        assert tap_plugins[0].name == "test-plugin"

        # Test filtering by TARGET type
        target_plugins = registry.list_plugins(PluginType.TARGET)
        assert len(target_plugins) == 1
        assert target_plugins[0].name == "test-plugin-2"

        # Test filtering by non-existent type
        transform_plugins = registry.list_plugins(PluginType.TRANSFORM)
        assert len(transform_plugins) == 0

    async def test_cleanup_all_empty(self, registry: SimplePluginRegistry) -> None:
        """Test cleaning up empty registry."""
        await registry.cleanup_all()
        assert registry.get_plugin_count() == 0

    async def test_cleanup_all_with_plugins(
        self,
        registry: SimplePluginRegistry,
        mock_plugin: Mock,
        mock_plugin_2: Mock,
    ) -> None:
        """Test cleaning up registry with plugins."""
        await registry.register_plugin(mock_plugin)
        await registry.register_plugin(mock_plugin_2)
        assert registry.get_plugin_count() == 2

        await registry.cleanup_all()
        assert registry.get_plugin_count() == 0


class TestPluginConfigurationComprehensive:
    """Comprehensive test PluginConfiguration model."""

    def test_configuration_creation_full(self) -> None:
        """Test creating plugin configuration with all parameters."""
        config = PluginConfiguration(
            plugin_id="test-plugin",
            enabled=True,
            configuration={"key": "value", "nested": {"item": 123}},
            permissions=["read", "write", "execute"],
            auto_load=False,
            hot_reload=True,
            priority=50,
        )

        assert config.plugin_id == "test-plugin"
        assert config.enabled is True
        assert config.configuration == {"key": "value", "nested": {"item": 123}}
        assert config.permissions == ["read", "write", "execute"]
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

    def test_configuration_edge_values(self) -> None:
        """Test configuration with edge values."""
        config = PluginConfiguration(
            plugin_id="edge-plugin",
            enabled=False,
            configuration={"empty": {}, "zero": 0, "false": False},
            permissions=[],
            priority=1,
        )

        assert config.plugin_id == "edge-plugin"
        assert config.enabled is False
        assert config.configuration["empty"] == {}
        assert config.configuration["zero"] == 0
        assert config.configuration["false"] is False
        assert config.permissions == []
        assert config.priority == 1


class TestPluginExecutionContextComprehensive:
    """Comprehensive test PluginExecutionContext model."""

    def test_execution_context_creation_full(self) -> None:
        """Test creating execution context with all parameters."""
        context = PluginExecutionContext(
            plugin_id="test-plugin",
            execution_id="exec-123",
            input_data={"data": "test", "items": [1, 2, 3]},
            context={"env": "test", "user": "tester"},
            timeout_seconds=30,
        )

        assert context.plugin_id == "test-plugin"
        assert context.execution_id == "exec-123"
        assert context.input_data == {"data": "test", "items": [1, 2, 3]}
        assert context.context == {"env": "test", "user": "tester"}
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

    def test_execution_context_edge_values(self) -> None:
        """Test execution context with edge values."""
        context = PluginExecutionContext(
            plugin_id="",
            execution_id="",
            input_data={},
            context={},
            timeout_seconds=0,
        )

        assert context.plugin_id == ""
        assert context.execution_id == ""
        assert context.input_data == {}
        assert context.context == {}
        assert context.timeout_seconds == 0


class TestPluginManagerResultComprehensive:
    """Comprehensive test PluginManagerResult model."""

    def test_manager_result_success(self) -> None:
        """Test creating successful manager result."""
        result = PluginManagerResult(
            operation="initialize",
            success=True,
            plugins_affected=["plugin1", "plugin2"],
            execution_time_ms=150.5,
            details={"plugins_loaded": 2, "config_applied": True},
            errors=[],
        )

        assert result.operation == "initialize"
        assert result.success is True
        assert result.plugins_affected == ["plugin1", "plugin2"]
        assert result.execution_time_ms == 150.5
        assert result.details == {"plugins_loaded": 2, "config_applied": True}
        assert result.errors == []

    def test_manager_result_failure(self) -> None:
        """Test creating failed manager result."""
        result = PluginManagerResult(
            operation="load_plugins",
            success=False,
            plugins_affected=[],
            execution_time_ms=50.0,
            details={"attempted": 3, "failed": 3},
            errors=["Plugin not found", "Invalid configuration", "Permission denied"],
        )

        assert result.operation == "load_plugins"
        assert result.success is False
        assert result.plugins_affected == []
        assert result.execution_time_ms == 50.0
        assert result.details == {"attempted": 3, "failed": 3}
        assert len(result.errors) == 3
        assert "Plugin not found" in result.errors

    def test_manager_result_edge_values(self) -> None:
        """Test manager result with edge values."""
        result = PluginManagerResult(
            operation="",
            success=False,
            plugins_affected=[],
            execution_time_ms=0.0,
            details={},
            errors=[],
        )

        assert result.operation == ""
        assert result.success is False
        assert result.plugins_affected == []
        assert result.execution_time_ms == 0.0
        assert result.details == {}
        assert result.errors == []


class TestPluginManagerComprehensive:
    """Comprehensive test PluginManager functionality."""

    @pytest.fixture
    def manager(self) -> PluginManager:
        """Create plugin manager for testing."""
        return PluginManager(auto_discover=False, security_enabled=False)

    @pytest.fixture
    def manager_with_auto_discover(self) -> PluginManager:
        """Create plugin manager with auto-discovery enabled."""
        return PluginManager(auto_discover=True, security_enabled=False)

    async def test_manager_initialization_basic(self, manager: PluginManager) -> None:
        """Test basic plugin manager initialization."""
        assert not manager.is_initialized

        result = await manager.initialize()

        assert result.success
        assert manager.is_initialized
        assert isinstance(result.data, PluginManagerResult)
        assert result.data.operation == "initialize"
        assert result.data.success is True

    async def test_manager_initialization_with_auto_discover(
        self,
        manager_with_auto_discover: PluginManager,
    ) -> None:
        """Test manager initialization with auto-discovery."""
        # Mock the discovery method to avoid actual file system operations
        with patch.object(
            manager_with_auto_discover,
            "discover_and_load_plugins",
        ) as mock_discover:
            mock_discover.return_value = FlextResult.ok(
                PluginManagerResult(
                    operation="discover_and_load",
                    success=True,
                    plugins_affected=["test-plugin"],
                    execution_time_ms=100.0,
                    details={"plugins_discovered": 1},
                    errors=[],
                ),
            )

            result = await manager_with_auto_discover.initialize()

            assert result.success
            assert manager_with_auto_discover.is_initialized
            mock_discover.assert_called_once()

    async def test_manager_properties(self, manager: PluginManager) -> None:
        """Test manager properties."""
        # Before initialization
        assert not manager.is_initialized
        assert manager.plugin_count == 0

        # After initialization
        result = await manager.initialize()
        assert result.success
        assert manager.is_initialized
        assert manager.plugin_count == 0  # No plugins loaded

    async def test_discover_and_load_plugins_empty(
        self,
        manager: PluginManager,
    ) -> None:
        """Test discovering plugins when none are available."""
        # Mock discovery to return empty results
        with patch.object(manager.discovery, "discover_all", return_value={}):
            result = await manager.discover_and_load_plugins()

            assert not result.success
            assert result.error is not None
            assert "No plugins discovered" in result.error

    async def test_execute_plugin_not_found(self, manager: PluginManager) -> None:
        """Test executing non-existent plugin."""
        await manager.initialize()

        result = await manager.execute_plugin(
            "non-existent-plugin",
            {"test": "data"},
        )

        assert not result.success
        assert result.error is not None
        assert "not found" in result.error.lower()

    async def test_configure_plugin_not_found(self, manager: PluginManager) -> None:
        """Test configuring non-existent plugin."""
        await manager.initialize()

        config = PluginConfiguration(plugin_id="non-existent")
        result = await manager.configure_plugin("non-existent", config)

        assert not result.success
        assert result.error is not None
        assert "not found" in result.error.lower()

    async def test_reload_plugin_not_configured(self, manager: PluginManager) -> None:
        """Test reloading plugin that doesn't exist."""
        await manager.initialize()

        result = await manager.reload_plugin("test-plugin")

        assert not result.success
        assert result.error is not None
        assert "not discovered" in result.error.lower()

    async def test_unload_plugin_not_found(self, manager: PluginManager) -> None:
        """Test unloading non-existent plugin."""
        await manager.initialize()

        result = await manager.unload_plugin("non-existent")

        assert not result.success
        assert result.error is not None
        assert "plugin unload failed" in result.error.lower()

    async def test_integrate_with_protocols(self, manager: PluginManager) -> None:
        """Test protocol integration."""
        await manager.initialize()

        result = await manager.integrate_with_protocols()

        # Should succeed as it's currently a placeholder
        assert result.success

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

    def test_list_plugins_by_type(self, manager: PluginManager) -> None:
        """Test listing plugins by type."""
        plugins = manager.list_plugins(plugin_type=PluginType.TAP)
        assert plugins == []

    async def test_cleanup(self, manager: PluginManager) -> None:
        """Test plugin manager cleanup."""
        await manager.initialize()
        assert manager.is_initialized

        await manager.cleanup()
        assert not manager.is_initialized

    async def test_create_plugin_context(self, manager: PluginManager) -> None:
        """Test creating plugin context."""
        context = await manager._create_plugin_context("test-plugin")

        assert context.plugin_name == "test-plugin"
        assert context.services == {}
        assert context.dependencies == {}
        assert context.permissions == ["read", "execute"]
        assert context.security_level == "standard"


class TestCreatePluginManagerComprehensive:
    """Comprehensive test plugin manager factory function."""

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

    def test_create_plugin_manager_all_combinations(self) -> None:
        """Test creating plugin manager with all parameter combinations."""
        # Test all boolean combinations
        combinations = [
            (True, True),
            (True, False),
            (False, True),
            (False, False),
        ]

        for auto_discover, security_enabled in combinations:
            manager = create_plugin_manager(
                auto_discover=auto_discover,
                security_enabled=security_enabled,
            )

            assert isinstance(manager, PluginManager)
            assert manager.auto_discover is auto_discover
            assert manager.security_enabled is security_enabled
