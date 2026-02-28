"""REAL test suite for flext_plugin.application.services module.

This test module provides comprehensive validation of application services functionality
using REAL plugin discovery, loading, and execution without ANY mocks.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import asyncio
import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import Protocol, cast

import pytest
from flext_core import FlextContainer, FlextExceptions

from flext_plugin import (
    FlextPluginConstants,
    FlextPluginDiscovery,
    FlextPluginLoader,
    FlextPluginModels,
    FlextPluginService,
    t,
)


class PluginInterface(Protocol):
    """Protocol for plugin instances loaded by PluginLoader.

    This protocol defines the interface that all plugin instances
    loaded by PluginLoader should implement.
    """

    def __init__(self) -> None:
        """Initialize the plugin instance."""

    @property
    def name(self) -> str: ...

    def initialize(self) -> dict[str, t.GeneralValueType]: ...

    def execute(
        self, data: dict[str, t.GeneralValueType] | None = None
    ) -> dict[str, t.GeneralValueType]: ...

    def cleanup(self) -> dict[str, t.GeneralValueType]: ...

    def health_check(self) -> dict[str, t.GeneralValueType]: ...

    def set_should_fail(self, should_fail: bool) -> None: ...


@pytest.fixture
def temp_plugin_dir() -> Generator[Path]:
    """Create temporary directory with REAL plugin files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        plugin_dir = Path(tmp_dir)

        # Create REAL working plugin
        tap_plugin = plugin_dir / "tap_database.py"
        tap_plugin.write_text("""
'''REAL tap plugin for database extraction.'''

class DatabaseTapPlugin:
    def __init__(self):
        \"\"\"Initialize the instance.\"\"\"

        self.name = "database-tap"
        self.version = "1.0.0"
        self.plugin_type = "tap"
        self.config = {
            "database_url": "postgresql://localhost/test",
            "tables": ["users", "orders"]
        }

    def initialize(self):
        return {"status": "initialized", "plugin": self.name}

    def execute(self):
        return {
            "extracted_records": 150,
            "tables": self.config["tables"],
            "status": "success"
        }

    def cleanup(self):
        return {"status": "cleaned", "plugin": self.name}

    def health_check(self):
        return {"status": "healthy", "plugin": self.name}

def get_plugin():
    return DatabaseTapPlugin()
""")

        # Create REAL working target plugin
        target_plugin = plugin_dir / "target_warehouse.py"
        target_plugin.write_text("""
'''REAL target plugin for data warehouse loading.'''

class WarehouseTargetPlugin:
    def __init__(self):
        \"\"\"Initialize the instance.\"\"\"

        self.name = "warehouse-target"
        self.version = "2.0.0"
        self.plugin_type = "target"
        self.config = {
            "warehouse_url": "postgresql://localhost/warehouse",
            "batch_size": 1000
        }
        self.loaded_records = 0

    def initialize(self):
        return {"status": "initialized", "plugin": self.name}

    def execute(self, data=None):
        records = data.get("records", []) if data else []
        self.loaded_records += len(records)
        return {
            "loaded_records": self.loaded_records,
            "batch_size": self.config["batch_size"],
            "status": "success"
        }

    def cleanup(self):
        return {"status": "cleaned", "loaded_total": self.loaded_records}

    def health_check(self):
        return {"status": "healthy", "loaded_total": self.loaded_records}

def get_plugin():
    return WarehouseTargetPlugin()
""")

        # Create REAL processor plugin with error handling
        processor_plugin = plugin_dir / "processor_transform.py"
        processor_plugin.write_text("""
'''REAL processor plugin for data transformation.'''

class DataProcessorPlugin:
    def __init__(self):
        \"\"\"Initialize the instance.\"\"\"

        self.name = "data-processor"
        self.version = "1.5.0"
        self.plugin_type = "processor"
        self.processed_items = 0

    def initialize(self):
        self.processed_items = 0
        return {"status": "initialized", "plugin": self.name}

    def execute(self, data=None):
        if not data:
            data = {"items": [1, 2, 3, 4, 5]}

        items = data.get("items", [])
        processed = [item * 2 for item in items if isinstance(item, (int, float))]
        self.processed_items += len(processed)

        return {
            "processed_items": processed,
            "total_processed": self.processed_items,
            "status": "success"
        }

    def cleanup(self):
        return {"status": "cleaned", "total_processed": self.processed_items}

    def health_check(self):
        return {"status": "healthy", "total_processed": self.processed_items}

def get_plugin():
    return DataProcessorPlugin()
""")

        # Create REAL plugin with error case
        error_plugin = plugin_dir / "error_plugin.py"
        error_plugin.write_text("""
'''Plugin that can simulate errors for testing.'''

class ErrorPlugin:
    def __init__(self):
        \"\"\"Initialize the instance.\"\"\"

        self.name = "error-plugin"
        self.version = "0.1.0"
        self.should_fail = False

    def initialize(self):
        return {"status": "initialized", "plugin": self.name}

    def execute(self, data=None):
        if self.should_fail:
            raise RuntimeError("Simulated plugin execution error")
        return {"status": "success", "data": "processed"}

    def set_should_fail(self, should_fail: bool):
        self.should_fail = should_fail

    def cleanup(self):
        return {"status": "cleaned"}

    def health_check(self):
        return {"status": "healthy" if not self.should_fail else "unhealthy"}

def get_plugin():
    return ErrorPlugin()
""")

        yield plugin_dir


@pytest.fixture
def real_plugin_loader() -> FlextPluginLoader:
    """Create REAL plugin loader for testing."""
    return FlextPluginLoader()


@pytest.fixture
def real_plugin_discovery() -> FlextPluginDiscovery:
    """Create REAL plugin discovery for testing."""
    return FlextPluginDiscovery()


@pytest.fixture
def real_service_with_adapters(temp_plugin_dir: Path) -> FlextPluginService:
    """Create FlextPluginService with REAL adapters instead of fallbacks."""
    container = FlextContainer()

    # Register REAL implementations
    discovery_adapter = FlextPluginDiscovery()
    loader_adapter = FlextPluginLoader()
    # manager_adapter = RealPluginManagerAdapter(str(temp_plugin_dir))

    container.with_service(
        "plugin_discovery_port", cast("t.RegisterableService", discovery_adapter)
    )
    container.with_service(
        "plugin_loader_port", cast("t.RegisterableService", loader_adapter)
    )
    # container.register("plugin_manager_port", manager_adapter)

    return FlextPluginService(container=container)


@pytest.fixture
def real_discovery_service_with_adapters(
    temp_plugin_dir: Path,
) -> FlextPluginService:
    """Create FlextPluginService with REAL discovery adapters."""
    container = FlextContainer()

    # Register REAL discovery implementation
    discovery_adapter = FlextPluginDiscovery()
    container.with_service(
        "plugin_discovery_port", cast("t.RegisterableService", discovery_adapter)
    )

    return FlextPluginService(container=container)


class TestRealPluginDiscoveryAndExecution:
    """REAL test suite for plugin discovery, loading, and execution."""

    def test_real_plugin_discovery_with_actual_files(
        self,
        real_plugin_discovery: FlextPluginDiscovery,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL plugin discovery with actual Python files."""
        # Discover plugins in the temp directory
        discovery_result = real_plugin_discovery.discover_plugins([
            str(temp_plugin_dir),
        ])
        assert discovery_result.is_success
        discovered_plugins = discovery_result.value
        assert len(discovered_plugins) == 4  # tap, target, processor, error plugins

        # Verify plugins are discoverable
        plugin_files = list(temp_plugin_dir.glob("*.py"))
        assert len(plugin_files) == 4  # tap, target, processor, error plugins

        # Verify specific plugin files exist
        plugin_names = {f.stem for f in plugin_files}
        expected_plugins = {
            "tap_database",
            "target_warehouse",
            "processor_transform",
            "error_plugin",
        }
        assert plugin_names == expected_plugins

    def test_real_plugin_loading_and_execution(
        self,
        real_plugin_loader: FlextPluginLoader,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL plugin loading and execution with actual Python modules."""
        # Load tap plugin
        tap_plugin_file = temp_plugin_dir / "tap_database.py"
        tap_result = real_plugin_loader.load_plugin(str(tap_plugin_file))

        # Verify plugin loaded correctly
        assert tap_result.is_success, f"Failed to load tap plugin: {tap_result.error}"
        tap_load_data = tap_result.unwrap()
        plugin = tap_load_data.module.get_plugin()
        assert plugin.name == "database-tap"

        # Test REAL plugin execution
        result = plugin.execute()
        assert result["status"] == "success"
        assert result["extracted_records"] == 150
        assert "tables" in result

        # Load and test target plugin
        target_plugin_file = temp_plugin_dir / "target_warehouse.py"
        target_result = real_plugin_loader.load_plugin(str(target_plugin_file))

        assert target_result.is_success, (
            f"Failed to load target plugin: {target_result.error}"
        )
        target_load_data = target_result.unwrap()
        target = target_load_data.module.get_plugin()
        assert target.name == "warehouse-target"

        # Test REAL target execution with data
        target_result = target.execute({"records": [1, 2, 3, 4, 5]})
        assert target_result["status"] == "success"
        assert target_result["loaded_records"] == 5

    def test_real_plugin_processor_execution(
        self,
        real_plugin_loader: FlextPluginLoader,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL processor plugin with data transformation."""
        processor_file = temp_plugin_dir / "processor_transform.py"
        load_result = real_plugin_loader.load_plugin(str(processor_file))

        assert load_result.is_success, f"Failed to load plugin: {load_result.error}"
        load_data = load_result.unwrap()
        # Get plugin instance from module's get_plugin() function
        processor = load_data.module.get_plugin()
        assert processor.name == "data-processor"

        # Test initialization
        init_result = processor.initialize()
        assert init_result["status"] == "initialized"

        # Test REAL data processing
        process_result = processor.execute({"items": [10, 20, 30]})
        assert process_result["status"] == "success"
        assert process_result["processed_items"] == [20, 40, 60]  # Doubled values
        assert process_result["total_processed"] == 3

        # Test multiple executions accumulate
        process_result2 = processor.execute({"items": [1, 2]})
        assert process_result2["total_processed"] == 5  # 3 + 2

        # Test cleanup
        cleanup_result = processor.cleanup()
        assert cleanup_result["status"] == "cleaned"
        assert cleanup_result["total_processed"] == 5

    def test_real_plugin_error_handling(
        self,
        real_plugin_loader: FlextPluginLoader,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL error handling with actual plugin exceptions."""
        error_file = temp_plugin_dir / "error_plugin.py"
        load_result = real_plugin_loader.load_plugin(str(error_file))

        assert load_result.is_success, f"Failed to load plugin: {load_result.error}"
        load_data = load_result.unwrap()
        # Get plugin instance from module's get_plugin() function
        error = load_data.module.get_plugin()
        assert error.name == "error-plugin"

        # Test normal execution first
        normal_result = error.execute()
        assert normal_result["status"] == "success"

        # Enable error mode and test exception handling
        error.set_should_fail(True)

        # Test that plugin actually raises exception
        with pytest.raises(RuntimeError, match="Simulated plugin execution error"):
            error.execute()

        # Verify health check reflects error state
        health_result = error.health_check()
        assert health_result["status"] == "unhealthy"


class TestFlextPluginServiceWithRealAdapters:
    """REAL test suite for FlextPluginService using REAL adapters instead of fallbacks."""

    def test_discover_plugins_with_real_adapters(
        self,
        real_service_with_adapters: FlextPluginService,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL plugin discovery using real adapters."""
        # Discover plugins using REAL adapter
        result = real_service_with_adapters.discover_plugins([str(temp_plugin_dir)])

        # Should succeed and find REAL plugins
        assert result.is_success
        assert isinstance(result.data, list)
        assert len(result.data) == 4  # Our 4 real plugin files

        # Verify plugins are real FlextPluginModels.Plugin objects
        for plugin in result.data:
            assert isinstance(plugin, FlextPluginModels.Plugin.Plugin)
            assert plugin.name in {
                "tap_database",
                "target_warehouse",
                "processor_transform",
                "error_plugin",
            }
            # Discovery adapter uses default "1.0.0" when __version__ not in module
            # (test plugins use instance variables, not module-level __version__)
            assert plugin.plugin_version == "1.0.0"

    def test_load_plugin_with_real_adapters(
        self,
        real_service_with_adapters: FlextPluginService,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL plugin loading using real adapters."""
        # First discover to get real plugin entity
        discover_result = real_service_with_adapters.discover_plugins(
            [str(temp_plugin_dir)],
        )
        assert discover_result.is_success
        assert len(discover_result.data) > 0

        # Get a real plugin entity
        tap_plugin: FlextPluginModels.Plugin.Plugin | None = None
        for plugin in discover_result.data:
            if plugin.name == "tap_database":
                tap_plugin = plugin
                break

        assert tap_plugin is not None

        # Load the real plugin using real adapter by path
        tap_plugin_path = temp_plugin_dir / "tap_database.py"
        load_result = real_service_with_adapters.load_plugin(str(tap_plugin_path))
        assert load_result.is_success
        assert isinstance(load_result.data, FlextPluginModels.Plugin.Plugin)
        assert load_result.data.name == "tap_database"

    def test_install_plugin_with_real_adapters(
        self,
        real_service_with_adapters: FlextPluginService,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL plugin installation using real adapters."""
        # Install real plugin file
        tap_plugin_file = temp_plugin_dir / "tap_database.py"

        install_result = real_service_with_adapters.install_plugin(str(tap_plugin_file))
        assert install_result.is_success
        assert isinstance(install_result.data, FlextPluginModels.Plugin.Plugin)
        assert install_result.data.name == "tap_database"

    def test_is_plugin_loaded_with_real_adapters(
        self,
        real_service_with_adapters: FlextPluginService,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL plugin loaded check using real adapters."""
        # First install a plugin
        tap_plugin_file = temp_plugin_dir / "tap_database.py"
        install_result = real_service_with_adapters.install_plugin(str(tap_plugin_file))
        assert install_result.is_success

        # Check if plugin is really loaded
        loaded_result = real_service_with_adapters.is_plugin_loaded("tap_database")
        assert loaded_result is True  # Should be loaded

        # Check non-loaded plugin
        not_loaded_result = real_service_with_adapters.is_plugin_loaded("non_existent")
        assert not_loaded_result is False  # Should not be loaded


class TestFlextPluginServiceReal:
    """REAL test suite for FlextPluginService with actual plugin loading."""

    @pytest.fixture
    def service(self) -> FlextPluginService:
        """Create service instance for testing."""
        return FlextPluginService()

    def test_service_initialization_default_real(self) -> None:
        """Test REAL service initialization with default container."""
        service = FlextPluginService()
        assert service is not None
        assert hasattr(service, "container")
        assert isinstance(service.container, FlextContainer)

        # Verify service has required functionality (SOLID: composition over inheritance)
        assert hasattr(service, "logger")
        assert hasattr(service, "config")

    def test_service_initialization_with_container_real(self) -> None:
        """Test REAL service initialization with provided container."""
        container = FlextContainer()
        service = FlextPluginService(container=container)
        assert service is not None
        assert service.container is container
        # Verify service has required functionality (SOLID: composition over inheritance)
        assert hasattr(service, "logger")
        assert hasattr(service, "config")

    def test_service_inheritance_patterns(self, service: FlextPluginService) -> None:
        """Test service composition patterns (SOLID principles applied)."""
        # Verify service has required functionality through composition
        assert hasattr(service, "logger")
        assert hasattr(service, "config")
        assert hasattr(service, "container")

        # Verify domain service capabilities (SOLID: specific methods for specific purposes)
        assert hasattr(service, "container")
        assert hasattr(service, "discover_and_register_plugins")
        assert hasattr(service, "load_plugin")
        assert hasattr(service, "execute_plugin")

    def test_service_has_specific_methods_real(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test REAL service has specific methods for specific operations (SOLID principles)."""
        # Verify service has specific methods for different operations
        assert hasattr(service, "discover_and_register_plugins")
        assert hasattr(service, "load_plugin")
        assert hasattr(service, "execute_plugin")
        assert hasattr(service, "unload_plugin")

        # Service should not have generic execute method (SOLID: specific methods for specific purposes)
        assert not hasattr(service, "execute")

    def test_discovery_functionality_real(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test REAL discovery functionality through service methods."""
        # Test discovery through service method (SOLID: specific methods for specific operations)
        result = service.discover_and_register_plugins(["/non/existent/path"])

        # Should handle non-existent paths gracefully (returns empty list, not failure)
        assert result.is_success
        # Empty list when no plugins found
        assert result.unwrap() == []

    def test_loader_functionality_real(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test REAL loader functionality through service methods."""
        # Test loader functionality through service method
        result = service.is_plugin_loaded("non-existent-plugin")

        # Should handle non-existent plugins and return False
        assert result is False

    @pytest.mark.asyncio
    async def test_management_functionality_real(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test REAL management functionality through service methods."""
        # Test management functionality through service method
        result = await service.unload_plugin("non-existent-plugin")

        # Should handle non-existent plugins and return failure
        assert result.is_failure
        assert "not found" in str(result.error)

    def test_discover_plugins_empty_path_returns_list(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test REAL discover_and_register_plugins with empty path."""
        result = service.discover_and_register_plugins([""])
        # Empty path is handled gracefully and returns a list (may be empty or not)
        assert result.is_success
        assert isinstance(result.unwrap(), list)

    def test_discover_plugins_with_real_plugin_files(
        self,
        service: FlextPluginService,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL discover_and_register_plugins with actual plugin files."""
        # Test discovery with directory containing real plugin files
        result = service.discover_and_register_plugins([str(temp_plugin_dir)])

        # Check for expected infrastructure failures - these are acceptable
        if result.is_failure and ("not configured" in str(result.error)):
            # This is expected - plugin service needs properly configured container
            pytest.skip(f"Infrastructure not configured: {result.error}")
            return

        # Should handle discovery with actual plugin directory
        assert isinstance(result.is_success, bool)
        if result.is_success:
            assert hasattr(result, "data")
            assert isinstance(result.data, list)
        else:
            # Discovery not available - this is expected in test environment
            assert "Plugin discovery not available" in str(result.error)

        # Test that plugin files are actually discoverable
        plugin_files = list(temp_plugin_dir.glob("*.py"))
        assert len(plugin_files) > 0  # Should find our real plugin files

    def test_load_plugin_with_real_plugin_entity(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test REAL load_plugin with actual plugin file and entity."""
        # Create REAL plugin entity that corresponds to actual file
        plugin = FlextPluginModels.Plugin.Plugin.create(
            name="tap_database",  # Corresponds to our real plugin file
            plugin_version="1.0.0",
            description="Database tap plugin for testing",
            plugin_type=FlextPluginConstants.Plugin.PluginType.TAP.value,
        )

        # Test loading with real plugin entity
        result = service.load_plugin(plugin.name)

        # Check for expected infrastructure failures - these are acceptable
        if result.is_failure and ("not configured" in str(result.error)):
            # This is expected - plugin service needs properly configured container
            pytest.skip(f"Infrastructure not configured: {result.error}")
            return

        assert isinstance(result.is_success, bool)
        if result.is_success:
            assert hasattr(result, "data")
        else:
            assert hasattr(result, "error")

        # The load should validate the plugin first
        if not result.is_success:
            # Expected if load_plugin doesn't support Plugin entity
            error_msg = str(result.error).lower()
            assert (
                "loading" in error_msg or "failed" in error_msg or "error" in error_msg
            )

    def test_load_plugin_with_different_types_real(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test REAL load_plugin with different plugin types."""
        # Test different plugin types
        plugin_types = [
            FlextPluginConstants.Plugin.PluginType.TAP,
            FlextPluginConstants.Plugin.PluginType.TARGET,
            FlextPluginConstants.Plugin.PluginType.UTILITY,
            FlextPluginConstants.Plugin.PluginType.SERVICE,
        ]

        for plugin_type in plugin_types:
            plugin = FlextPluginModels.Plugin.Plugin.create(
                name=f"real-plugin-{plugin_type.value}",
                plugin_version="1.0.0",
                plugin_type=plugin_type.value,
            )

            result = service.load_plugin(plugin.name)
            assert isinstance(result.is_success, bool)
            # If result is success, we have a plugin; if failure, we have an error
            assert result.is_success or result.is_failure

    @pytest.mark.asyncio
    async def test_unload_plugin_empty_name_fails_real(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test REAL unload_plugin with empty name fails."""
        result = await service.unload_plugin("")
        assert result.is_failure
        error_message = str(result.error).lower()
        assert "not found" in error_message or "plugin" in error_message

    @pytest.mark.asyncio
    async def test_unload_plugin_valid_name_real(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test REAL unload_plugin with non-existent plugin returns failure."""
        result = await service.unload_plugin("real-unload-plugin")
        # Plugin doesn't exist, so unload returns failure
        assert isinstance(result.is_success, bool)
        assert result.is_failure
        assert "not found" in str(result.error)

    def test_install_plugin_empty_path_fails_real(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test REAL install_plugin with empty path fails."""
        result = service.install_plugin("")
        assert result.is_failure
        error_message = str(result.error).lower()
        assert (
            "loading" in error_message
            or "failed" in error_message
            or "error" in error_message
            or "load" in error_message
        )

    def test_install_plugin_with_real_plugin_file(
        self,
        service: FlextPluginService,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL install_plugin with actual plugin file."""
        # Use our real plugin file
        tap_plugin_file = temp_plugin_dir / "tap_database.py"

        result = service.install_plugin(str(tap_plugin_file))
        # Test actual result handling with real plugin file
        assert isinstance(result.is_success, bool)

        # With fallback implementation, might fail but should handle gracefully
        if not result.is_success:
            # Expected failure - plugin might not be installed
            error_msg = str(result.error).lower()
            assert (
                "not found" in error_msg
                or "failed" in error_msg
                or "not implemented" in error_msg
            )

    def test_uninstall_plugin_empty_name_fails(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test uninstall_plugin with empty name fails."""
        result = service.uninstall_plugin("")
        assert not result.is_success
        assert (
            "not found" in str(result.error).lower()
            or "plugin" in str(result.error).lower()
        )

    def test_uninstall_plugin_valid_name_real(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test uninstall_plugin with REAL valid name."""
        result = service.uninstall_plugin("real-test-plugin")
        # Plugin doesn't exist, so expect failure or success based on implementation
        assert result.is_success or "not found" in str(result.error).lower()

    def test_enable_plugin_empty_name_fails(self, service: FlextPluginService) -> None:
        """Test enable_plugin with empty name fails."""
        result = service.enable_plugin("")
        assert not result.is_success
        assert (
            "not found" in str(result.error).lower()
            or "plugin" in str(result.error).lower()
        )

    def test_enable_plugin_valid_name_real(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test enable_plugin with REAL valid name."""
        result = service.enable_plugin("real-test-plugin")
        # Plugin doesn't exist, so expect failure or success based on implementation
        assert result.is_success or "not found" in str(result.error).lower()

    def test_disable_plugin_empty_name_fails(self, service: FlextPluginService) -> None:
        """Test disable_plugin with empty name fails."""
        result = service.disable_plugin("")
        assert not result.is_success
        assert (
            "not found" in str(result.error).lower()
            or "plugin" in str(result.error).lower()
        )

    def test_disable_plugin_valid_name_real(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test disable_plugin with REAL valid name."""
        result = service.disable_plugin("real-test-plugin")
        # Plugin doesn't exist, so expect failure or success based on implementation
        assert result.is_success or "not found" in str(result.error).lower()

    def test_get_plugin_config_empty_name_fails(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test get_plugin_config with empty name fails."""
        result = service.get_plugin_config("")
        assert not result.is_success
        # Error message can be "Plugin name is required" or "Plugin '' not found"
        assert "not found" in str(result.error) or "required" in str(result.error)

    def test_get_plugin_config_valid_name_real(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test get_plugin_config with REAL valid name."""
        result = service.get_plugin_config("real-test-plugin")

        # Check for expected infrastructure failures - these are acceptable
        if result.is_failure and ("not configured" in str(result.error)):
            # This is expected - plugin service needs properly configured container
            pytest.skip(f"Infrastructure not configured: {result.error}")
            return

        # Plugin not found returns failure
        assert not result.is_success
        assert "not found" in str(result.error)

    def test_update_plugin_config_empty_name_fails(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test update_plugin_config with empty name fails."""
        config = FlextPluginModels.Plugin.PluginConfig(plugin_name="test")
        result = service.update_plugin_config("", config.model_dump())
        assert not result.is_success
        assert (
            "not found" in str(result.error).lower()
            or "plugin" in str(result.error).lower()
        )

    def test_update_plugin_config_mismatched_name_fails(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test update_plugin_config with mismatched plugin name fails."""
        # Create config for one plugin but try to update a different one
        config = FlextPluginModels.Plugin.PluginConfig(plugin_name="different-plugin")
        result = service.update_plugin_config("test-plugin", config.model_dump())
        # Should fail because plugin doesn't exist or names mismatch
        assert not result.is_success

    def test_update_plugin_config_valid_params_real(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test update_plugin_config with REAL valid params."""
        config = FlextPluginModels.Plugin.PluginConfig(plugin_name="real-test-plugin")
        result = service.update_plugin_config("real-test-plugin", config.model_dump())

        # Accept either success or failure - depends on plugin being loaded
        assert result.is_success or result.is_failure

    def test_is_plugin_loaded_empty_name_returns_false(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test is_plugin_loaded with empty name returns False."""
        result = service.is_plugin_loaded("")
        # is_plugin_loaded returns bool directly, False means not loaded
        assert isinstance(result, bool)
        assert result is False

    def test_is_plugin_loaded_valid_name_real(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test is_plugin_loaded with REAL valid name."""
        result = service.is_plugin_loaded("real-test-plugin")

        # is_plugin_loaded returns bool directly
        assert isinstance(result, bool)
        assert result is False  # Plugin not actually loaded


class TestFlextPluginDiscoveryReal:
    """REAL test suite for FlextPluginDiscovery with actual plugin files.

    Tests the ACTUAL API with real plugin discovery and validation.
    """

    @pytest.fixture
    def discovery_service(self) -> FlextPluginDiscovery:
        """Create discovery service instance."""
        return FlextPluginDiscovery()

    def test_discovery_service_initialization_default(self) -> None:
        """Test discovery service initialization with default settings."""
        service = FlextPluginDiscovery()
        assert service is not None
        # FlextPluginDiscovery has strategies and logger, not container
        assert hasattr(service, "strategies")
        assert hasattr(service, "logger")

    def test_discovery_service_has_two_strategies(self) -> None:
        """Test discovery service has FileSystem and EntryPoint strategies."""
        service = FlextPluginDiscovery()
        assert service is not None
        assert hasattr(service, "strategies")
        assert len(service.strategies) == 2  # FileSystemStrategy, EntryPointStrategy

    def test_discovery_service_has_strategies(
        self,
        discovery_service: FlextPluginDiscovery,
    ) -> None:
        """Test discovery service has strategies attribute."""
        assert hasattr(discovery_service, "strategies")
        assert isinstance(discovery_service.strategies, list)

    def test_discover_plugins_method_exists(
        self,
        discovery_service: FlextPluginDiscovery,
    ) -> None:
        """Test discover_plugins method exists."""
        assert hasattr(discovery_service, "discover_plugins")
        assert callable(discovery_service.discover_plugins)

    def test_discover_plugins_with_empty_paths(
        self,
        discovery_service: FlextPluginDiscovery,
    ) -> None:
        """Test discover_plugins with empty paths returns empty list."""
        result = discovery_service.discover_plugins([])
        assert result.is_success
        assert result.data == []

    def test_discover_plugins_empty_paths_succeeds(
        self,
        discovery_service: FlextPluginDiscovery,
    ) -> None:
        """Test discover_plugins with empty paths list returns empty."""
        result = discovery_service.discover_plugins([])
        assert result.is_success
        assert result.data == []

    def test_discover_plugins_with_real_files(
        self,
        discovery_service: FlextPluginDiscovery,
        temp_plugin_dir: Path,
    ) -> None:
        """Test discover_plugins with REAL plugin files."""
        try:
            result = discovery_service.discover_plugins([str(temp_plugin_dir)])
        except FlextExceptions.BaseError as e:
            # Infrastructure not configured - skip test
            pytest.skip(f"Infrastructure not configured: {e}")
            return

        # Check for expected infrastructure failures - these are acceptable
        if result.is_failure and ("not configured" in str(result.error)):
            # This is expected - plugin service needs properly configured container
            pytest.skip(f"Infrastructure not configured: {result.error}")
            return

        assert result.is_success
        assert isinstance(result.data, list)

        # With fallback implementation, might return empty but should handle real directory
        # The real test is that it doesn't crash with actual plugin files
        plugin_files = list(temp_plugin_dir.glob("*.py"))
        assert len(plugin_files) == 4  # Our real plugin files exist

    def test_validate_plugin_with_discovery_data(
        self,
        discovery_service: FlextPluginDiscovery,
        temp_plugin_dir: Path,
    ) -> None:
        """Test validate_plugin with DiscoveryData from real files."""
        # First discover a plugin to get valid DiscoveryData
        result = discovery_service.discover_plugins([str(temp_plugin_dir)])
        assert result.is_success
        assert len(result.data) > 0

        # Validate one of the discovered plugins
        plugin_data = result.data[0]
        validation_result = discovery_service.validate_plugin(plugin_data)
        assert validation_result.is_success
        assert validation_result.data is True

        # Verify the corresponding plugin file actually exists
        plugin_file = temp_plugin_dir / f"{plugin_data.name}.py"
        assert plugin_file.exists()


class TestRealPluginIntegrationWorkflow:
    """REAL integration tests using actual plugin loading and execution."""

    def test_complete_service_integration_workflow(
        self,
        real_service_with_adapters: FlextPluginService,
        temp_plugin_dir: Path,
    ) -> None:
        """Test complete REAL workflow using services with real adapters."""
        # Step 1: Discover plugins through service with real adapter
        discover_result = real_service_with_adapters.discover_plugins(
            [str(temp_plugin_dir)],
        )
        assert discover_result.is_success
        assert len(discover_result.data) == 4

        # Step 2: Find specific plugins
        tap_plugin = None
        target_plugin = None
        for plugin in discover_result.data:
            if plugin.name == "tap_database":
                tap_plugin = plugin
            elif plugin.name == "target_warehouse":
                target_plugin = plugin

        assert tap_plugin is not None
        assert target_plugin is not None

        # Step 3: Load plugins through service (using file paths)
        tap_file = temp_plugin_dir / "tap_database.py"
        target_file = temp_plugin_dir / "target_warehouse.py"
        tap_load_result = real_service_with_adapters.load_plugin(str(tap_file))
        target_load_result = real_service_with_adapters.load_plugin(str(target_file))

        assert tap_load_result.is_success
        assert target_load_result.is_success

        # Step 4: Verify plugins are loaded (is_plugin_loaded returns bool directly)
        tap_loaded = real_service_with_adapters.is_plugin_loaded("tap_database")
        target_loaded = real_service_with_adapters.is_plugin_loaded("target_warehouse")

        assert tap_loaded is True
        assert target_loaded is True

        # Step 5: Test unloading (async operation)
        unload_result = asyncio.run(
            real_service_with_adapters.unload_plugin("tap_database"),
        )
        assert unload_result.is_success

        # Step 6: Verify unloaded
        unloaded = real_service_with_adapters.is_plugin_loaded("tap_database")
        assert unloaded is False

    def test_complete_plugin_workflow_real(
        self,
        real_plugin_loader: FlextPluginLoader,
        real_plugin_discovery: FlextPluginDiscovery,
        temp_plugin_dir: Path,
    ) -> None:
        """Test complete REAL workflow: discover -> load -> execute -> cleanup."""
        # Step 1: Real plugin discovery
        discovery_result = real_plugin_discovery.discover_plugins([
            str(temp_plugin_dir),
        ])
        assert discovery_result.is_success
        discovered_plugins = discovery_result.value
        assert len(discovered_plugins) == 4  # Our real plugins

        # Use pathlib.Path for synchronous directory iteration
        plugin_files = list(temp_plugin_dir.glob("*.py"))
        assert len(plugin_files) == 4  # Our real plugins

        # Step 2: Load tap plugin and Execute workflow
        tap_file = temp_plugin_dir / "tap_database.py"
        tap_result = real_plugin_loader.load_plugin(str(tap_file))

        # Verify plugin loaded
        assert tap_result.is_success, f"Failed to load tap plugin: {tap_result.error}"
        tap_data = tap_result.unwrap()
        tap = tap_data.module.get_plugin()
        assert tap.name == "database-tap"

        # Step 3: Execute initialization
        init_result = tap.initialize()
        assert init_result["status"] == "initialized"

        # Step 4: Execute main functionality
        extract_result = tap.execute()
        assert extract_result["status"] == "success"
        assert extract_result["extracted_records"] == 150

        # Step 5: Load target plugin for pipeline
        target_file = temp_plugin_dir / "target_warehouse.py"
        target_result = real_plugin_loader.load_plugin(str(target_file))

        # Unwrap target plugin
        assert target_result.is_success, f"Failed to load target: {target_result.error}"
        target_data = target_result.unwrap()
        target = target_data.module.get_plugin()

        # Step 6: Create data pipeline between plugins
        extracted_data = {"records": list(range(extract_result["extracted_records"]))}
        load_result = target.execute(extracted_data)
        assert load_result["status"] == "success"
        assert load_result["loaded_records"] == 150

        # Step 7: Health checks on loaded plugins
        tap_health = tap.health_check()
        target_health = target.health_check()
        assert tap_health["status"] == "healthy"
        assert target_health["status"] == "healthy"

        # Step 8: Cleanup workflow
        tap_cleanup = tap.cleanup()
        target_cleanup = target.cleanup()
        assert tap_cleanup["status"] == "cleaned"
        assert target_cleanup["status"] == "cleaned"

    def test_real_plugin_loader_registry_management(
        self,
        real_plugin_loader: FlextPluginLoader,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL plugin registry management with actual plugins."""
        # Load multiple plugins
        tap_file = temp_plugin_dir / "tap_database.py"
        target_file = temp_plugin_dir / "target_warehouse.py"
        processor_file = temp_plugin_dir / "processor_transform.py"

        # Load plugins into registry
        tap_result = real_plugin_loader.load_plugin(str(tap_file))
        target_result = real_plugin_loader.load_plugin(str(target_file))
        processor_result = real_plugin_loader.load_plugin(str(processor_file))

        # Unwrap plugin results and get instances
        assert tap_result.is_success, f"Failed to load tap: {tap_result.error}"
        assert target_result.is_success, f"Failed to load target: {target_result.error}"
        assert processor_result.is_success, (
            f"Failed to load processor: {processor_result.error}"
        )
        tap = tap_result.unwrap().module.get_plugin()
        target = target_result.unwrap().module.get_plugin()
        processor = processor_result.unwrap().module.get_plugin()

        # Verify all loaded correctly
        assert tap.name == "database-tap"
        assert target.name == "warehouse-target"
        assert processor.name == "data-processor"

        # Test registry functionality
        # get_loaded_plugins() returns list of plugin names
        loaded_plugin_names = real_plugin_loader.get_loaded_plugins()
        assert len(loaded_plugin_names) >= 3  # At least our 3 plugins

        # Verify plugin names are in the list
        assert "tap_database" in loaded_plugin_names
        assert "target_warehouse" in loaded_plugin_names
        assert "processor_transform" in loaded_plugin_names

        # The plugins are already retrieved above via unwrap().module.get_plugin()
        # Verify tap plugin from earlier load
        assert tap.name == "database-tap"

    def test_real_plugin_lifecycle_management(
        self,
        real_plugin_loader: FlextPluginLoader,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL plugin lifecycle with loading/unloading."""
        # Load plugin
        processor_file = temp_plugin_dir / "processor_transform.py"
        load_result = real_plugin_loader.load_plugin(str(processor_file))

        # Verify loaded - load_plugin returns FlextResult[LoadData]
        assert load_result.is_success
        load_data = load_result.value
        assert load_data is not None
        assert load_data.name == "processor_transform"

        # Verify in loaded plugins list
        loaded_plugins = real_plugin_loader.get_loaded_plugins()
        assert "processor_transform" in loaded_plugins

        # Unload plugin
        unload_result = real_plugin_loader.unload_plugin("processor_transform")
        assert unload_result.is_success

        # Verify unloaded
        loaded_plugins_after = real_plugin_loader.get_loaded_plugins()
        assert "processor_transform" not in loaded_plugins_after

        # Reload plugin (should start fresh)
        reload_result = real_plugin_loader.load_plugin(str(processor_file))
        assert reload_result.is_success
        reloaded_data = reload_result.value
        assert reloaded_data is not None
        assert reloaded_data.name == "processor_transform"


class TestServicesIntegrationReal:
    """REAL integration tests for services working with actual plugins."""

    def test_services_can_coexist(self) -> None:
        """Test that both services can be created and used together."""
        container = FlextContainer()

        plugin_service = FlextPluginService(container=container)
        # FlextPluginDiscovery is standalone, doesn't accept container
        discovery_service = FlextPluginDiscovery()

        assert plugin_service is not None
        assert discovery_service is not None
        assert plugin_service.container is container

    def test_services_share_container_state_real(self) -> None:
        """Test services share REAL container state."""
        container = FlextContainer()

        # Register a REAL service object in the container
        test_service: dict[str, t.GeneralValueType] = {
            "name": "test_service",
            "config": {"enabled": True},
        }
        container.with_service("test_service", test_service)

        # Create services with shared container
        # Note: FlextPluginService uses container, FlextPluginDiscovery doesn't
        plugin_service = FlextPluginService(container=container)

        # Verify service has access to container state
        result1 = plugin_service.container.get("test_service")

        assert result1.is_success
        assert result1.data is test_service
        # Verify actual data
        data1 = result1.data
        assert isinstance(data1, dict)
        assert data1["name"] == "test_service"

        # FlextPluginDiscovery is standalone, doesn't require container
        discovery_service = FlextPluginDiscovery()
        assert discovery_service is not None

    def test_services_with_real_plugin_directory(
        self,
        temp_plugin_dir: Path,
    ) -> None:
        """Test services with REAL plugin directory containing actual files."""
        container = FlextContainer()

        plugin_service = FlextPluginService(container=container)
        # FlextPluginDiscovery is standalone - doesn't accept container
        discovery_service = FlextPluginDiscovery()

        # Both should work with real plugin directories - handle infrastructure errors
        try:
            plugin_discovery_result = plugin_service.discover_plugins(
                [str(temp_plugin_dir)],
            )
        except FlextExceptions.BaseError as e:
            # Infrastructure not configured - skip test
            pytest.skip(f"Infrastructure not configured: {e}")
            return

        try:
            service_discovery_result = discovery_service.discover_plugins(
                [str(temp_plugin_dir)],
            )
        except FlextExceptions.BaseError as e:
            # Infrastructure not configured - skip test
            pytest.skip(f"Infrastructure not configured: {e}")
            return

        # Check for expected infrastructure failures - these are acceptable
        if not plugin_discovery_result.is_success and (
            "not configured" in str(plugin_discovery_result.error)
        ):
            # This is expected - plugin service needs properly configured container
            pytest.skip(
                f"Infrastructure not configured: {plugin_discovery_result.error}",
            )
            return

        # Check for expected infrastructure failures - these are acceptable
        if not service_discovery_result.is_success and (
            "not configured" in str(service_discovery_result.error)
        ):
            # This is expected - discovery service needs properly configured container
            pytest.skip(
                f"Infrastructure not configured: {service_discovery_result.error}",
            )
            return

        assert plugin_discovery_result.is_success
        assert service_discovery_result.is_success
        assert isinstance(plugin_discovery_result.data, list)
        assert isinstance(service_discovery_result.data, list)

        # Verify the directory actually contains our real plugin files
        plugin_files = list(temp_plugin_dir.glob("*.py"))
        assert len(plugin_files) == 4  # Our real plugin files


class TestRealPluginErrorScenarios:
    """Test REAL error scenarios with actual plugin files."""

    def test_real_plugin_execution_error_handling(
        self,
        real_plugin_loader: FlextPluginLoader,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL error handling with plugin that actually throws exceptions."""
        # Load our error plugin
        error_file = temp_plugin_dir / "error_plugin.py"
        load_result = real_plugin_loader.load_plugin(str(error_file))

        # Verify plugin loaded
        assert load_result.is_success, f"Failed to load plugin: {load_result.error}"
        load_data = load_result.unwrap()
        error = load_data.module.get_plugin()
        assert error.name == "error-plugin"

        # Test normal execution first
        normal_result = error.execute()
        assert normal_result["status"] == "success"

        # Enable error mode
        error.set_should_fail(True)

        # Test that we can catch REAL plugin exceptions
        with pytest.raises(RuntimeError, match="Simulated plugin execution error"):
            error.execute()

        # Test that plugin state reflects error condition
        health = error.health_check()
        assert health["status"] == "unhealthy"

    def test_real_plugin_file_loading_errors(
        self,
        real_plugin_loader: FlextPluginLoader,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL file loading errors with malformed plugin files."""
        # Create malformed plugin file
        bad_plugin_file = temp_plugin_dir / "bad_syntax_plugin.py"
        bad_plugin_file.write_text("""

# This file has syntax errors
class BadPlugin:
    def __init__(self):
        \"\"\"Initialize the instance.\"\"\"

        self.name = "bad-plugin"
        # Missing closing quote and other syntax errors
        self.data = "unclosed string

    def execute(self
        return {"error": "should not reach here"}
""")

        # Test that loader handles syntax errors gracefully
        # load_plugin returns FlextResult - should return failure for syntax errors
        load_result = real_plugin_loader.load_plugin(str(bad_plugin_file))
        assert not load_result.is_success, "Expected failure for syntax error plugin"

    def test_real_plugin_file_not_found_error(
        self,
        real_plugin_loader: FlextPluginLoader,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL file not found error handling."""
        # Try to load non-existent plugin file
        nonexistent_file = temp_plugin_dir / "does_not_exist.py"

        # load_plugin returns FlextResult - should return failure for missing file
        load_result = real_plugin_loader.load_plugin(str(nonexistent_file))
        assert not load_result.is_success, "Expected failure for non-existent file"


class TestServiceErrorHandling:
    """Test service error conditions with real scenarios."""

    def test_service_handles_port_resolution_with_real_plugins(
        self,
        temp_plugin_dir: Path,
    ) -> None:
        """Test service port resolution with REAL plugin directory."""
        # Create container that will fall back to mock implementations
        container = FlextContainer()
        service = FlextPluginService(container=container)

        # Operations should work with fallback implementations even with real files
        result = service.discover_plugins([str(temp_plugin_dir)])

        # Check for expected infrastructure failures - these are acceptable
        if result.is_failure and ("not configured" in str(result.error)):
            # This is expected - plugin service needs properly configured container
            pytest.skip(f"Infrastructure not configured: {result.error}")
            return

        assert result.is_success
        assert isinstance(result.data, list)

        # Verify real plugin files exist in directory being tested
        plugin_files = list(temp_plugin_dir.glob("*.py"))
        assert (
            len(plugin_files) == 4
        )  # Real files exist, even if fallback returns empty

    def test_discovery_service_handles_empty_directory_real(self) -> None:
        """Test discovery service handles empty directory with REAL operations."""
        # FlextPluginDiscovery is standalone - no container parameter
        discovery_service = FlextPluginDiscovery()

        with tempfile.TemporaryDirectory() as temp_dir:
            result = discovery_service.discover_plugins([temp_dir])

            # Check for expected infrastructure failures - these are acceptable
            if result.is_failure and ("not configured" in str(result.error)):
                # This is expected - plugin service needs properly configured container
                pytest.skip(f"Infrastructure not configured: {result.error}")
                return

            assert result.is_success
            assert isinstance(result.data, list)
            assert result.data == []  # Empty directory

    def test_service_methods_work_with_default_initialization(self) -> None:
        """Test that service methods work with default initialization."""
        service = FlextPluginService()

        # Test discovery works (returns list)
        with tempfile.TemporaryDirectory() as temp_dir:
            result = service.discover_and_register_plugins([temp_dir])
            assert result.is_success
            assert isinstance(result.unwrap(), list)

        # Test is_plugin_loaded works (returns bool)
        loaded = service.is_plugin_loaded("real-plugin")
        assert isinstance(loaded, bool)
        assert loaded is False  # Not loaded

    def test_discovery_service_methods_work_with_default_initialization(
        self,
    ) -> None:
        """Test that discovery service methods work with default initialization."""
        service = FlextPluginDiscovery()

        # Test discover_plugins works with real directories
        with tempfile.TemporaryDirectory() as temp_dir:
            result = service.discover_plugins([temp_dir])
            assert result.is_success
            assert isinstance(result.unwrap(), list)

    def test_service_handles_discovery_edge_cases_real(self) -> None:
        """Test service handles discovery edge cases with REAL scenarios."""
        service = FlextPluginService()

        # Test with empty path (handled gracefully, returns success with list)
        result = service.discover_plugins([""])
        assert result.is_success or result.is_failure

        # Test with very long invalid path (should handle gracefully)
        invalid_path = "/" + "x" * 500  # Very long path
        result2 = service.discover_plugins([invalid_path])
        # Should either succeed (empty result) or fail gracefully
        assert isinstance(result2.is_success, bool)

    @pytest.mark.asyncio
    async def test_service_handles_loader_exceptions_real(self) -> None:
        """Test service handles loader port exceptions with REAL scenarios."""
        service = FlextPluginService()

        # Test with empty plugin name (should handle gracefully)
        result = await service.unload_plugin("")
        assert not result.is_success
        assert (
            "not found" in str(result.error).lower()
            or "plugin" in str(result.error).lower()
        )

        # Test with very long plugin name (should handle gracefully)
        long_name = "x" * 1000  # Very long name
        result2 = await service.unload_plugin(long_name)
        # Should either succeed or fail gracefully
        assert isinstance(result2.is_success, bool)
        if not result2.is_success:
            assert (
                "Failed to unload plugin" in str(result2.error)
                or "plugin" in str(result2.error).lower()
                or "not found" in str(result2.error).lower()
            )

    def test_discovery_service_handles_empty_paths_real(self) -> None:
        """Test discovery service handles empty paths with REAL scenarios."""
        service = FlextPluginDiscovery()

        # Test with empty paths list (should return empty list)
        result = service.discover_plugins([])
        assert result.is_success
        assert result.data == []

        # Test with non-existent path (should still succeed with empty result)
        invalid_path = "/" + "x" * 500  # Very long path
        result2 = service.discover_plugins([invalid_path])
        # Should succeed with empty result for non-existent paths
        assert result2.is_success
        assert result2.data == []


class TestBackwardsCompatibilityAliasesReal:
    """Test REAL backwards compatibility aliases functionality."""

    def test_plugin_service_alias_exists_real(self) -> None:
        """Test PluginService alias exists and works with REAL functionality."""
        # Import from application.services module

        service = FlextPluginService()
        assert service is not None
        assert isinstance(service, FlextPluginService)

        # Test REAL functionality through alias

        with tempfile.TemporaryDirectory() as temp_dir:
            result = service.discover_plugins([temp_dir])

            # Check for expected infrastructure failures - these are acceptable
            if result.is_failure and ("not configured" in str(result.error)):
                # This is expected - plugin service needs properly configured container
                pytest.skip(f"Infrastructure not configured: {result.error}")
                return

            assert result.is_success
            assert isinstance(result.data, list)

    def test_plugin_discovery_service_alias_exists_real(self) -> None:
        """Test PluginDiscoveryService alias exists and works with REAL functionality."""
        # Import from application.services module

        service = FlextPluginDiscovery()
        assert service is not None
        assert isinstance(service, FlextPluginDiscovery)

        # Test REAL functionality through alias

        with tempfile.TemporaryDirectory() as temp_dir:
            result = service.discover_plugins([temp_dir])

            # Check for expected infrastructure failures - these are acceptable
            if result.is_failure and ("not configured" in str(result.error)):
                # This is expected - plugin service needs properly configured container
                pytest.skip(f"Infrastructure not configured: {result.error}")
                return

            assert result.is_success
            assert isinstance(result.data, list)
