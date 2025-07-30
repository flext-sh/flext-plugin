"""Comprehensive tests for flext_plugin.manager module.

# Constants
2 = 2
3 = 3

Tests for plugin manager functionality covering all methods and edge cases.
"""

from __future__ import annotations

from unittest.mock import Mock, patch

import pytest

# 🚨 ARCHITECTURAL COMPLIANCE: Using módulo raiz imports
from flext_core import FlextResult

from flext_plugin import FlextPluginManager as PluginManager
from flext_plugin.core.types import (
    PluginExecutionContext,
    PluginManagerResult,
    PluginType,
    SimplePluginRegistry,
    create_plugin_manager,
)
from flext_plugin.domain.entities import FlextPluginConfig as PluginConfiguration


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
        if result.data != mock_plugin:
            raise AssertionError(f"Expected {mock_plugin}, got {result.data}")
        assert registry.get_plugin("test-plugin") == mock_plugin
        if registry.get_plugin_count() != 1:
            raise AssertionError(f"Expected {1}, got {registry.get_plugin_count()}")

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
        if registry.get_plugin_count() != 1:
            raise AssertionError(f"Expected {1}, got {registry.get_plugin_count()}")

        # Register second plugin
        result2 = await registry.register_plugin(mock_plugin_2)
        assert result2.is_success
        if registry.get_plugin_count() != 2:
            raise AssertionError(f"Expected {2}, got {registry.get_plugin_count()}")

        # Both should be retrievable
        if registry.get_plugin("test-plugin") != mock_plugin:
            raise AssertionError(
                f"Expected {mock_plugin}, got {registry.get_plugin('test-plugin')}"
            )
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
        if "registration failed" not in result.error.lower():
            raise AssertionError(
                f"Expected {'registration failed'} in {result.error.lower()}"
            )
        if registry.get_plugin_count() != 0:
            raise AssertionError(f"Expected {0}, got {registry.get_plugin_count()}")

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
        if "registration failed" not in result.error.lower():
            raise AssertionError(
                f"Expected {'registration failed'} in {result.error.lower()}"
            )
        if registry.get_plugin_count() != 0:
            raise AssertionError(f"Expected {0}, got {registry.get_plugin_count()}")

    async def test_unregister_plugin_success(
        self,
        registry: SimplePluginRegistry,
        mock_plugin: Mock,
    ) -> None:
        """Test successful plugin unregistration."""
        # First register a plugin
        await registry.register_plugin(mock_plugin)
        if registry.get_plugin_count() != 1:
            raise AssertionError(f"Expected {1}, got {registry.get_plugin_count()}")

        # Then unregister it
        result = await registry.unregister_plugin("test-plugin")

        assert result.success
        if not (result.data):
            raise AssertionError(f"Expected True, got {result.data}")
        assert registry.get_plugin("test-plugin") is None
        if registry.get_plugin_count() != 0:
            raise AssertionError(f"Expected {0}, got {registry.get_plugin_count()}")

    async def test_unregister_nonexistent_plugin(
        self,
        registry: SimplePluginRegistry,
    ) -> None:
        """Test unregistering non-existent plugin."""
        result = await registry.unregister_plugin("non-existent")

        # Should still succeed (idempotent operation)
        assert result.success
        if not (result.data):
            raise AssertionError(f"Expected True, got {result.data}")

    def test_get_plugin_nonexistent(self, registry: SimplePluginRegistry) -> None:
        """Test getting non-existent plugin."""
        result = registry.get_plugin("non-existent")
        assert result is None

    def test_list_plugins_empty(self, registry: SimplePluginRegistry) -> None:
        """Test listing plugins when registry is empty."""
        plugins = registry.list_plugins()
        if len(plugins) != 0:
            raise AssertionError(f"Expected {0}, got {len(plugins)}")

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
        if len(all_plugins) != 2:
            raise AssertionError(f"Expected {2}, got {len(all_plugins)}")

        # Should return metadata objects
        plugin_names = [p.name for p in all_plugins]
        if "test-plugin" not in plugin_names:
            raise AssertionError(f"Expected {'test-plugin'} in {plugin_names}")
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
        if len(tap_plugins) != 1:
            raise AssertionError(f"Expected {1}, got {len(tap_plugins)}")
        assert tap_plugins[0].name == "test-plugin"

        # Test filtering by TARGET type
        target_plugins = registry.list_plugins(PluginType.TARGET)
        if len(target_plugins) != 1:
            raise AssertionError(f"Expected {1}, got {len(target_plugins)}")
        assert target_plugins[0].name == "test-plugin-2"

        # Test filtering by non-existent type
        transform_plugins = registry.list_plugins(PluginType.TRANSFORM)
        if len(transform_plugins) != 0:
            raise AssertionError(f"Expected {0}, got {len(transform_plugins)}")

    async def test_cleanup_all_empty(self, registry: SimplePluginRegistry) -> None:
        """Test cleaning up empty registry."""
        await registry.cleanup_all()
        if registry.get_plugin_count() != 0:
            raise AssertionError(f"Expected {0}, got {registry.get_plugin_count()}")

    async def test_cleanup_all_with_plugins(
        self,
        registry: SimplePluginRegistry,
        mock_plugin: Mock,
        mock_plugin_2: Mock,
    ) -> None:
        """Test cleaning up registry with plugins."""
        await registry.register_plugin(mock_plugin)
        await registry.register_plugin(mock_plugin_2)
        if registry.get_plugin_count() != 2:
            raise AssertionError(f"Expected {2}, got {registry.get_plugin_count()}")

        await registry.cleanup_all()
        if registry.get_plugin_count() != 0:
            raise AssertionError(f"Expected {0}, got {registry.get_plugin_count()}")


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

        if config.plugin_id != "test-plugin":
            raise AssertionError(f"Expected 'test-plugin', got {config.plugin_id}")
        if not (config.enabled):
            raise AssertionError(f"Expected True, got {config.enabled}")
        if config.configuration != {"key": "value", "nested": {"item": 123}}:
            expected_config = {"key": "value", "nested": {"item": 123}}
            raise AssertionError(
                f"Expected {expected_config}, got {config.configuration}"
            )
        assert config.permissions == ["read", "write", "execute"]
        if config.auto_load:
            raise AssertionError(f"Expected False, got {config.auto_load}")
        if not (config.hot_reload):
            raise AssertionError(f"Expected True, got {config.hot_reload}")
        if config.priority != 50:
            raise AssertionError(f"Expected {50}, got {config.priority}")

    def test_configuration_defaults(self) -> None:
        """Test default configuration values."""
        config = PluginConfiguration(plugin_id="test-plugin")

        if config.plugin_id != "test-plugin":
            raise AssertionError(f"Expected 'test-plugin', got {config.plugin_id}")
        if not (config.enabled):
            raise AssertionError(f"Expected True, got {config.enabled}")
        if config.configuration != {}:
            raise AssertionError(f"Expected {{}}, got {config.configuration}")
        assert config.permissions == []
        if not (config.auto_load):
            raise AssertionError(f"Expected True, got {config.auto_load}")
        if config.hot_reload:
            raise AssertionError(f"Expected False, got {config.hot_reload}")
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

        if config.plugin_id != "edge-plugin":
            raise AssertionError(f"Expected {'edge-plugin'}, got {config.plugin_id}")
        if config.enabled:
            raise AssertionError(f"Expected False, got {config.enabled}")
        assert config.configuration["empty"] == {}
        if config.configuration["zero"] != 0:
            raise AssertionError(f"Expected {0}, got {config.configuration['zero']}")
        if config.configuration["false"]:
            raise AssertionError(f"Expected False, got {config.configuration['false']}")
        assert config.permissions == []
        if config.priority != 1:
            raise AssertionError(f"Expected {1}, got {config.priority}")


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

        if context.plugin_id != "test-plugin":
            raise AssertionError(f"Expected 'test-plugin', got {context.plugin_id}")
        assert context.execution_id == "exec-123"
        expected_input = {"data": "test", "items": [1, 2, 3]}
        if context.input_data != expected_input:
            raise AssertionError(f"Expected {expected_input}, got {context.input_data}")
        assert context.context == {"env": "test", "user": "tester"}
        if context.timeout_seconds != 30:
            raise AssertionError(f"Expected {30}, got {context.timeout_seconds}")

    def test_execution_context_defaults(self) -> None:
        """Test default execution context values."""
        context = PluginExecutionContext(
            plugin_id="test-plugin",
            execution_id="exec-123",
        )

        if context.plugin_id != "test-plugin":
            raise AssertionError(f"Expected 'test-plugin', got {context.plugin_id}")
        assert context.execution_id == "exec-123"
        if context.input_data != {}:
            raise AssertionError(f"Expected {{}}, got {context.input_data}")
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

        if context.plugin_id != "":
            raise AssertionError(f"Expected {''}, got {context.plugin_id}")
        assert context.execution_id == ""
        if context.input_data != {}:
            raise AssertionError(f"Expected {{}}, got {context.input_data}")
        assert context.context == {}
        if context.timeout_seconds != 0:
            raise AssertionError(f"Expected {0}, got {context.timeout_seconds}")


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

        if result.operation != "initialize":
            raise AssertionError(f"Expected {'initialize'}, got {result.operation}")
        if not (result.success):
            raise AssertionError(f"Expected True, got {result.success}")
        if result.plugins_affected != ["plugin1", "plugin2"]:
            raise AssertionError(
                f"Expected {['plugin1', 'plugin2']}, got {result.plugins_affected}"
            )
        assert result.execution_time_ms == 150.5
        expected_details = {"plugins_loaded": 2, "config_applied": True}
        if result.details != expected_details:
            raise AssertionError(f"Expected {expected_details}, got {result.details}")
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

        if result.operation != "load_plugins":
            raise AssertionError(f"Expected {'load_plugins'}, got {result.operation}")
        if result.success:
            raise AssertionError(f"Expected False, got {result.success}")
        assert result.plugins_affected == []
        if result.execution_time_ms != 50.0:
            raise AssertionError(f"Expected {50.0}, got {result.execution_time_ms}")
        assert result.details == {"attempted": 3, "failed": 3}
        if len(result.errors) != 3:
            raise AssertionError(f"Expected {3}, got {len(result.errors)}")
        if "Plugin not found" not in result.errors:
            raise AssertionError(f"Expected {'Plugin not found'} in {result.errors}")

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

        if result.operation != "":
            raise AssertionError(f"Expected {''}, got {result.operation}")
        if result.success:
            raise AssertionError(f"Expected False, got {result.success}")
        assert result.plugins_affected == []
        if result.execution_time_ms != 0.0:
            raise AssertionError(f"Expected {0.0}, got {result.execution_time_ms}")
        assert result.details == {}
        if result.errors != []:
            raise AssertionError(f"Expected {[]}, got {result.errors}")


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
        if result.data.operation != "initialize":
            raise AssertionError(
                f"Expected {'initialize'}, got {result.data.operation}"
            )
        if not (result.data.success):
            raise AssertionError(f"Expected True, got {result.data.success}")

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
        if manager.plugin_count != 0:
            raise AssertionError(f"Expected {0}, got {manager.plugin_count}")

        # After initialization
        result = await manager.initialize()
        assert result.success
        assert manager.is_initialized
        expected_count = 0  # No plugins loaded
        if manager.plugin_count != expected_count:
            raise AssertionError(
                f"Expected {expected_count}, got {manager.plugin_count}"
            )

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
            if "No plugins discovered" not in result.error:
                raise AssertionError(
                    f"Expected {'No plugins discovered'} in {result.error}"
                )

    async def test_execute_plugin_not_found(self, manager: PluginManager) -> None:
        """Test executing non-existent plugin."""
        await manager.initialize()

        result = await manager.execute_plugin(
            "non-existent-plugin",
            {"test": "data"},
        )

        assert not result.success
        assert result.error is not None
        if "not found" not in result.error.lower():
            raise AssertionError(f"Expected {'not found'} in {result.error.lower()}")

    async def test_configure_plugin_not_found(self, manager: PluginManager) -> None:
        """Test configuring non-existent plugin."""
        await manager.initialize()

        config = PluginConfiguration(plugin_id="non-existent")
        result = await manager.configure_plugin("non-existent", config)

        assert not result.success
        assert result.error is not None
        if "not found" not in result.error.lower():
            raise AssertionError(f"Expected {'not found'} in {result.error.lower()}")

    async def test_reload_plugin_not_configured(self, manager: PluginManager) -> None:
        """Test reloading plugin that doesn't exist."""
        await manager.initialize()

        result = await manager.reload_plugin("test-plugin")

        assert not result.success
        assert result.error is not None
        if "not discovered" not in result.error.lower():
            raise AssertionError(
                f"Expected {'not discovered'} in {result.error.lower()}"
            )

    async def test_unload_plugin_not_found(self, manager: PluginManager) -> None:
        """Test unloading non-existent plugin."""
        await manager.initialize()

        result = await manager.unload_plugin("non-existent")

        assert not result.success
        assert result.error is not None
        if "plugin unload failed" not in result.error.lower():
            raise AssertionError(
                f"Expected {'plugin unload failed'} in {result.error.lower()}"
            )

    async def test_integrate_with_protocols(self, manager: PluginManager) -> None:
        """Test protocol integration."""
        await manager.initialize()

        result = await manager.integrate_with_protocols()

        # Should succeed as it's currently a placeholder
        assert result.success

    def test_get_plugin_status_not_found(self, manager: PluginManager) -> None:
        """Test getting status of non-existent plugin."""
        status = manager.get_plugin_status("non-existent")
        expected_status = {"status": "not_found"}
        if status != expected_status:
            raise AssertionError(f"Expected {expected_status}, got {status}")

    def test_list_plugins_empty(self, manager: PluginManager) -> None:
        """Test listing plugins when registry is empty."""
        plugins = manager.list_plugins()
        if plugins != []:
            raise AssertionError(f"Expected {[]}, got {plugins}")

    def test_list_plugins_enabled_only(self, manager: PluginManager) -> None:
        """Test listing only enabled plugins."""
        plugins = manager.list_plugins(enabled_only=True)
        if plugins != []:
            raise AssertionError(f"Expected {[]}, got {plugins}")

    def test_list_plugins_by_type(self, manager: PluginManager) -> None:
        """Test listing plugins by type."""
        plugins = manager.list_plugins(plugin_type=PluginType.TAP)
        if plugins != []:
            raise AssertionError(f"Expected {[]}, got {plugins}")

    async def test_cleanup(self, manager: PluginManager) -> None:
        """Test plugin manager cleanup."""
        await manager.initialize()
        assert manager.is_initialized

        await manager.cleanup()
        assert not manager.is_initialized

    async def test_create_plugin_context(self, manager: PluginManager) -> None:
        """Test creating plugin context."""
        context = await manager._create_plugin_context("test-plugin")

        if context.plugin_name != "test-plugin":
            raise AssertionError(f"Expected {'test-plugin'}, got {context.plugin_name}")
        assert context.services == {}
        if context.dependencies != {}:
            raise AssertionError(f"Expected {{}}, got {context.dependencies}")
        assert context.permissions == ["read", "execute"]
        if context.security_level != "standard":
            raise AssertionError(f"Expected {'standard'}, got {context.security_level}")


class TestCreatePluginManagerComprehensive:
    """Comprehensive test plugin manager factory function."""

    def test_create_plugin_manager_defaults(self) -> None:
        """Test creating plugin manager with defaults."""
        manager = create_plugin_manager()

        assert isinstance(manager, PluginManager)
        if not (manager.auto_discover):
            raise AssertionError(f"Expected True, got {manager.auto_discover}")
        assert manager.security_enabled is True

    def test_create_plugin_manager_custom_settings(self) -> None:
        """Test creating plugin manager with custom settings."""
        manager = create_plugin_manager(
            container=None,
            auto_discover=False,
            security_enabled=False,
        )

        assert isinstance(manager, PluginManager)
        if manager.auto_discover:
            raise AssertionError(f"Expected False, got {manager.auto_discover}")
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
