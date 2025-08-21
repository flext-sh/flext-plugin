"""REAL test suite for flext_plugin.manager module.

This test module provides comprehensive validation of plugin management functionality
using REAL manager components without ANY mocks.

Testing Strategy - REAL FUNCTIONALITY ONLY:
    - SimplePluginRegistry: REAL plugin registry with registration and discovery
    - PluginExecutionContext: REAL execution environment and context management
    - Factory Functions: REAL plugin manager creation and configuration
    - FlextResult Patterns: REAL railway-oriented programming validation

Quality Standards:
    - 100% code coverage through REAL functionality testing
    - NO MOCKS - only real manager components and actual plugin entities
    - Enterprise-grade error handling validation
    - Complete integration testing with real FlextPluginEntity objects
"""

from __future__ import annotations

import pytest

from flext_plugin import (
    PluginExecutionContext,
    PluginManagerResult,
    PluginType,
    SimplePluginRegistry,
    create_plugin_manager,
)
from flext_plugin.domain.entities import FlextPluginEntity


class TestSimplePluginRegistryReal:
    """REAL test suite for SimplePluginRegistry functionality."""

    @pytest.fixture
    def registry(self) -> SimplePluginRegistry:
        """Create registry for testing."""
        return SimplePluginRegistry()

    @pytest.fixture
    def real_plugin(self) -> FlextPluginEntity:
        """Create REAL plugin entity for testing."""
        return FlextPluginEntity.create(
            name="real-registry-plugin",
            plugin_version="1.0.0",
            description="Real plugin for registry testing",
            plugin_type=PluginType.UTILITY,
        )

    @pytest.mark.asyncio
    async def test_register_plugin_success_real(
        self,
        registry: SimplePluginRegistry,
        real_plugin: FlextPluginEntity,
    ) -> None:
        """Test successful REAL plugin registration."""
        result = await registry.register_plugin(real_plugin)

        assert result.success
        assert result.data == real_plugin
        assert registry.get_plugin("real-registry-plugin") == real_plugin
        assert registry.get_plugin_count() == 1

    @pytest.mark.asyncio
    async def test_register_plugin_with_duplicate_name(
        self,
        registry: SimplePluginRegistry,
        real_plugin: FlextPluginEntity,
    ) -> None:
        """Test registering plugin with duplicate name."""
        # Register first plugin
        result1 = await registry.register_plugin(real_plugin)
        assert result1.success

        # Create another plugin with same name
        duplicate_plugin = FlextPluginEntity.create(
            name="real-registry-plugin",  # Same name
            plugin_version="2.0.0",  # Different version
            description="Duplicate plugin",
        )

        # Register duplicate (should replace first)
        result2 = await registry.register_plugin(duplicate_plugin)
        assert result2.success

        # Should still have only 1 plugin (replaced)
        assert registry.get_plugin_count() == 1
        registered_plugin = registry.get_plugin("real-registry-plugin")
        assert registered_plugin is not None
        assert registered_plugin.plugin_version == "2.0.0"

    @pytest.mark.asyncio
    async def test_unregister_plugin_real(
        self,
        registry: SimplePluginRegistry,
        real_plugin: FlextPluginEntity,
    ) -> None:
        """Test REAL plugin unregistration."""
        # First register a plugin
        await registry.register_plugin(real_plugin)
        assert registry.get_plugin_count() == 1

        # Then unregister it
        result = await registry.unregister_plugin("real-registry-plugin")

        assert result.success
        assert result.data is True
        assert registry.get_plugin("real-registry-plugin") is None
        assert registry.get_plugin_count() == 0

    @pytest.mark.asyncio
    async def test_unregister_nonexistent_plugin_real(
        self,
        registry: SimplePluginRegistry,
    ) -> None:
        """Test unregistering REAL non-existent plugin."""
        # Verify registry is empty
        assert registry.get_plugin_count() == 0

        result = await registry.unregister_plugin("non-existent-plugin")

        # Should still succeed (idempotent operation)
        assert result.success
        assert result.data is True
        assert registry.get_plugin_count() == 0

    def test_list_plugins_real(self, registry: SimplePluginRegistry) -> None:
        """Test listing REAL plugins."""
        # Empty registry
        plugins = registry.list_plugins()
        assert len(plugins) == 0
        assert isinstance(plugins, list)

    @pytest.mark.asyncio
    async def test_list_plugins_with_type_filter_real(
        self,
        registry: SimplePluginRegistry,
    ) -> None:
        """Test listing REAL plugins with type filter."""
        # Create real plugin entities with different types
        tap_plugin = FlextPluginEntity.create(
            name="tap-plugin",
            plugin_version="1.0.0",
            description="Real tap plugin for testing",
            plugin_type=PluginType.TAP,
        )

        target_plugin = FlextPluginEntity.create(
            name="target-plugin",
            plugin_version="1.0.0",
            description="Real target plugin for testing",
            plugin_type=PluginType.TARGET,
        )

        # Register plugins properly
        await registry.register_plugin(tap_plugin)
        await registry.register_plugin(target_plugin)

        # Test listing all plugins
        all_plugins = registry.list_plugins()
        assert len(all_plugins) == 2

        # Test filtering by type
        tap_plugins = registry.list_plugins(PluginType.TAP)
        assert len(tap_plugins) == 1

        # Verify the plugin is the right one (type-safe access)
        found_tap_plugin = tap_plugins[0]
        assert hasattr(found_tap_plugin, "name")
        if hasattr(found_tap_plugin, "name"):
            assert found_tap_plugin.name == "tap-plugin"

    @pytest.mark.asyncio
    async def test_cleanup_all_real(
        self,
        registry: SimplePluginRegistry,
        real_plugin: FlextPluginEntity,
    ) -> None:
        """Test cleaning up all REAL plugins."""
        await registry.register_plugin(real_plugin)
        assert registry.get_plugin_count() == 1

        await registry.cleanup_all()
        assert registry.get_plugin_count() == 0

    @pytest.mark.asyncio
    async def test_registry_multiple_operations_real(
        self,
        registry: SimplePluginRegistry,
    ) -> None:
        """Test REAL registry with multiple operations."""
        # Create multiple plugins
        plugins = []
        for i in range(3):
            plugin = FlextPluginEntity.create(
                name=f"multi-plugin-{i}",
                plugin_version="1.0.0",
                description=f"Multi plugin {i} for testing",
                plugin_type=PluginType.UTILITY,
            )
            plugins.append(plugin)
            await registry.register_plugin(plugin)

        # Verify all registered
        assert registry.get_plugin_count() == 3

        # Test getting individual plugins
        for i in range(3):
            plugin = registry.get_plugin(f"multi-plugin-{i}")
            assert plugin is not None
            assert plugin.name == f"multi-plugin-{i}"

        # Test unregistering one
        result = await registry.unregister_plugin("multi-plugin-1")
        assert result.success
        assert registry.get_plugin_count() == 2

        # Verify specific plugin was removed
        assert registry.get_plugin("multi-plugin-1") is None
        assert registry.get_plugin("multi-plugin-0") is not None
        assert registry.get_plugin("multi-plugin-2") is not None


class TestPluginExecutionContextReal:
    """REAL test suite for PluginExecutionContext functionality."""

    def test_execution_context_creation_real(self) -> None:
        """Test creating REAL plugin execution context."""
        context = PluginExecutionContext(
            plugin_id="real-execution-plugin",
            execution_id="exec-12345",
            input_data={"source": "database", "table": "users"},
            context={"environment": "test", "debug": True},
            timeout_seconds=60,
        )

        assert context.plugin_id == "real-execution-plugin"
        assert context.execution_id == "exec-12345"
        assert context.input_data["source"] == "database"
        assert context.input_data["table"] == "users"
        assert context.context["environment"] == "test"
        assert context.context["debug"] is True
        assert context.timeout_seconds == 60

    def test_execution_context_defaults_real(self) -> None:
        """Test REAL execution context with default values."""
        context = PluginExecutionContext(
            plugin_id="minimal-context-plugin",
            execution_id="minimal-exec",
        )

        assert context.plugin_id == "minimal-context-plugin"
        assert context.execution_id == "minimal-exec"
        assert context.input_data == {}
        assert context.context == {}
        assert context.timeout_seconds is None

    def test_execution_context_with_complex_data_real(self) -> None:
        """Test REAL execution context with complex data structures."""
        complex_input: dict[str, object] = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "tables": ["users", "orders"],
            },
            "api": {"endpoints": ["/data", "/export"], "auth": {"type": "bearer"}},
        }
        complex_context: dict[str, object] = {
            "execution_mode": "batch",
            "batch_size": 1000,
            "retry_policy": {"max_retries": 3, "backoff": "exponential"},
        }

        context = PluginExecutionContext(
            plugin_id="complex-data-plugin",
            execution_id="complex-exec-789",
            input_data=complex_input,
            context=complex_context,
            timeout_seconds=300,
        )

        assert context.plugin_id == "complex-data-plugin"
        assert context.execution_id == "complex-exec-789"
        # Type-safe access to nested data
        database_data = context.input_data.get("database", {})
        assert isinstance(database_data, dict)
        assert database_data.get("host") == "localhost"

        tables_data = database_data.get("tables", [])
        assert isinstance(tables_data, list)
        assert len(tables_data) == 2

        assert context.context.get("execution_mode") == "batch"
        assert context.context.get("batch_size") == 1000
        assert context.timeout_seconds == 300


class TestPluginManagerResultReal:
    """REAL test suite for PluginManagerResult functionality."""

    def test_manager_result_creation_real(self) -> None:
        """Test creating REAL manager result."""
        result = PluginManagerResult(
            operation="bulk_load",
            success=True,
        )
        result.plugins_affected = [
            "extractor-plugin",
            "loader-plugin",
            "transformer-plugin",
        ]
        result.execution_time_ms = 250.75
        result.details = {
            "plugins_loaded": 3,
            "load_method": "dynamic",
            "total_size_mb": 12.5,
        }
        result.errors = []

        assert result.operation == "bulk_load"
        assert result.success is True
        assert result.plugins_affected == [
            "extractor-plugin",
            "loader-plugin",
            "transformer-plugin",
        ]
        assert result.execution_time_ms == 250.75
        assert result.details["plugins_loaded"] == 3
        assert result.details["load_method"] == "dynamic"
        assert result.errors == []

    def test_manager_result_with_errors_real(self) -> None:
        """Test REAL manager result with errors."""
        result = PluginManagerResult(
            operation="validate_plugins",
            success=False,
        )
        result.plugins_affected = ["corrupted-plugin"]
        result.execution_time_ms = 85.25
        result.details = {
            "validation_failures": 2,
            "corrupted_files": ["config.yaml", "manifest.json"],
        }
        result.errors = [
            "Configuration validation failed: missing required field 'name'",
            "Manifest parsing error: invalid JSON structure",
        ]

        assert result.operation == "validate_plugins"
        assert result.success is False
        assert result.plugins_affected == ["corrupted-plugin"]
        assert result.execution_time_ms == 85.25
        assert result.details["validation_failures"] == 2
        assert len(result.errors) == 2
        assert "Configuration validation failed" in result.errors[0]

    def test_manager_result_create_detailed_real(self) -> None:
        """Test creating REAL detailed manager result from config."""
        config: dict[str, object] = {
            "success": True,
            "plugins_affected": ["test-plugin-1", "test-plugin-2"],
            "execution_time_ms": 125.5,
            "details": {"batch_processed": True, "total_plugins": 2},
            "errors": [],
        }

        result = PluginManagerResult.create_detailed("batch_process", config)

        assert result.operation == "batch_process"
        assert result.success is True
        assert result.plugins_affected == ["test-plugin-1", "test-plugin-2"]
        assert result.execution_time_ms == 125.5
        assert result.details["batch_processed"] is True
        assert result.errors == []


class TestCreatePluginManagerFactoryReal:
    """REAL test suite for create_plugin_manager factory function."""

    def test_create_plugin_manager_default_real(self) -> None:
        """Test creating REAL plugin manager with default settings."""
        manager = create_plugin_manager()

        assert manager is not None
        assert isinstance(manager, SimplePluginRegistry)
        assert manager.get_plugin_count() == 0

    def test_create_plugin_manager_with_options_real(self) -> None:
        """Test creating REAL plugin manager with specific options."""
        manager = create_plugin_manager(
            _auto_discover=True,
            _security_enabled=False,
        )

        assert manager is not None
        assert isinstance(manager, SimplePluginRegistry)
        assert manager.get_plugin_count() == 0

    @pytest.mark.asyncio
    async def test_factory_created_manager_functionality_real(self) -> None:
        """Test REAL functionality of factory-created manager."""
        manager = create_plugin_manager()

        # Create real plugin to test with
        plugin = FlextPluginEntity.create(
            name="factory-test-plugin",
            plugin_version="1.0.0",
            description="Plugin created for factory testing",
            plugin_type=PluginType.PROCESSOR,
        )

        # Test registration
        result = await manager.register_plugin(plugin)
        assert result.success
        assert manager.get_plugin_count() == 1

        # Test retrieval
        retrieved_plugin = manager.get_plugin("factory-test-plugin")
        assert retrieved_plugin is not None
        assert retrieved_plugin.name == "factory-test-plugin"

        # Test cleanup
        await manager.cleanup_all()
        assert manager.get_plugin_count() == 0
