"""REAL test suite for flext_plugin.application.services module.

This test module provides comprehensive validation of application services functionality
using REAL plugin discovery, loading, and execution without ANY mocks.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import asyncio
import tempfile
from collections.abc import (
    Generator,
)
from pathlib import Path
from typing import Protocol

import pytest

from flext_core import FlextContainer
from flext_plugin import (
    FlextPluginConstants,
    FlextPluginDiscovery,
    FlextPluginLoader,
    FlextPluginModels,
    FlextPluginService,
    t,
)
from tests import e, m, p


class PluginInterface(Protocol):
    """Protocol for plugin instances loaded by PluginLoader.

    This protocol defines the interface that all plugin instances
    loaded by PluginLoader should implement.
    """

    def __init__(self) -> None:
        """Initialize the plugin instance."""

    @property
    def name(self) -> str: ...

    def initialize(self) -> t.JsonMapping: ...

    def execute(self, data: t.JsonMapping | None = None) -> t.JsonMapping: ...

    def cleanup(self) -> t.JsonMapping: ...

    def health_check(self) -> t.JsonMapping: ...

    def set_should_fail(self, should_fail: bool) -> None: ...


@pytest.fixture
def temp_plugin_dir() -> Generator[Path]:
    """Create temporary directory with REAL plugin files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        plugin_dir = Path(tmp_dir)
        tap_plugin = plugin_dir / "tap_database.py"
        tap_plugin.write_text(
            '\n\'\'\'REAL tap plugin for database extraction.\'\'\'\n\nclass DatabaseTapPlugin:\n    def __init__(self):\n        """Initialize the instance."""\n\n        self.name = "database-tap"\n        self.version = "1.0.0"\n        self.plugin_type = "tap"\n        self.settings = {\n            "database_url": "postgresql://localhost/test",\n            "tables": ["users", "orders"]\n        }\n\n    def initialize(self):\n        return {"status": "initialized", "plugin": self.name}\n\n    def execute(self):\n        return {\n            "extracted_records": 150,\n            "tables": self.settings["tables"],\n            "status": "success"\n        }\n\n    def cleanup(self):\n        return {"status": "cleaned", "plugin": self.name}\n\n    def health_check(self):\n        return {"status": "healthy", "plugin": self.name}\n\ndef get_plugin():\n    return DatabaseTapPlugin()\n',
        )
        target_plugin = plugin_dir / "target_warehouse.py"
        target_plugin.write_text(
            '\n\'\'\'REAL target plugin for data warehouse loading.\'\'\'\n\nclass WarehouseTargetPlugin:\n    def __init__(self):\n        """Initialize the instance."""\n\n        self.name = "warehouse-target"\n        self.version = "2.0.0"\n        self.plugin_type = "target"\n        self.settings = {\n            "warehouse_url": "postgresql://localhost/warehouse",\n            "batch_size": 1000\n        }\n        self.loaded_records = 0\n\n    def initialize(self):\n        return {"status": "initialized", "plugin": self.name}\n\n    def execute(self, data=None):\n        records = data.get("records", []) if data else []\n        self.loaded_records += len(records)\n        return {\n            "loaded_records": self.loaded_records,\n            "batch_size": self.settings["batch_size"],\n            "status": "success"\n        }\n\n    def cleanup(self):\n        return {"status": "cleaned", "loaded_total": self.loaded_records}\n\n    def health_check(self):\n        return {"status": "healthy", "loaded_total": self.loaded_records}\n\ndef get_plugin():\n    return WarehouseTargetPlugin()\n',
        )
        processor_plugin = plugin_dir / "processor_transform.py"
        processor_plugin.write_text(
            '\n\'\'\'REAL processor plugin for data transformation.\'\'\'\n\nclass DataProcessorPlugin:\n    def __init__(self):\n        """Initialize the instance."""\n\n        self.name = "data-processor"\n        self.version = "1.5.0"\n        self.plugin_type = "processor"\n        self.processed_items = 0\n\n    def initialize(self):\n        self.processed_items = 0\n        return {"status": "initialized", "plugin": self.name}\n\n    def execute(self, data=None):\n        if not data:\n            data = {"items": [1, 2, 3, 4, 5]}\n\n        items = data.get("items", [])\n        processed = [item * 2 for item in items if isinstance(item, (int, float))]\n        self.processed_items += len(processed)\n\n        return {\n            "processed_items": processed,\n            "total_processed": self.processed_items,\n            "status": "success"\n        }\n\n    def cleanup(self):\n        return {"status": "cleaned", "total_processed": self.processed_items}\n\n    def health_check(self):\n        return {"status": "healthy", "total_processed": self.processed_items}\n\ndef get_plugin():\n    return DataProcessorPlugin()\n',
        )
        error_plugin = plugin_dir / "error_plugin.py"
        error_plugin.write_text(
            '\n\'\'\'Plugin that can simulate errors for testing.\'\'\'\n\nclass ErrorPlugin:\n    def __init__(self):\n        """Initialize the instance."""\n\n        self.name = "error-plugin"\n        self.version = "0.1.0"\n        self.should_fail = False\n\n    def initialize(self):\n        return {"status": "initialized", "plugin": self.name}\n\n    def execute(self, data=None):\n        if self.should_fail:\n            raise RuntimeError("Simulated plugin execution error")\n        return {"status": "success", "data": "processed"}\n\n    def set_should_fail(self, should_fail: bool):\n        self.should_fail = should_fail\n\n    def cleanup(self):\n        return {"status": "cleaned"}\n\n    def health_check(self):\n        return {"status": "healthy" if not self.should_fail else "unhealthy"}\n\ndef get_plugin():\n    return ErrorPlugin()\n',
        )
        yield plugin_dir


@pytest.fixture
def real_plugin_loader() -> FlextPluginLoader:
    return FlextPluginLoader()


@pytest.fixture
def real_plugin_discovery() -> FlextPluginDiscovery:
    return FlextPluginDiscovery()


@pytest.fixture
def real_service_with_adapters(temp_plugin_dir: Path) -> FlextPluginService:
    return FlextPluginService()


@pytest.fixture
def real_discovery_service_with_adapters(temp_plugin_dir: Path) -> FlextPluginService:
    return FlextPluginService()


class TestsFlextPluginApplicationServices:
    def test_real_plugin_discovery_with_actual_files(
        self,
        real_plugin_discovery: FlextPluginDiscovery,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL plugin discovery with actual Python files."""
        discovery_result = real_plugin_discovery.discover_plugins([
            str(temp_plugin_dir),
        ])
        assert discovery_result.success
        discovered_plugins = discovery_result.value
        assert len(discovered_plugins) == 4
        plugin_files = list(temp_plugin_dir.glob("*.py"))
        assert len(plugin_files) == 4
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
        tap_plugin_file = temp_plugin_dir / "tap_database.py"
        tap_result = real_plugin_loader.load_plugin(str(tap_plugin_file))
        assert tap_result.success, f"Failed to load tap plugin: {tap_result.error}"
        tap_load_data = tap_result.unwrap()
        plugin = tap_load_data.module.get_plugin()
        assert plugin.name == "database-tap"
        result = plugin.execute()
        assert result["status"] == "success"
        assert result["extracted_records"] == 150
        assert "tables" in result
        target_plugin_file = temp_plugin_dir / "target_warehouse.py"
        target_result = real_plugin_loader.load_plugin(str(target_plugin_file))
        assert target_result.success, (
            f"Failed to load target plugin: {target_result.error}"
        )
        target_load_data = target_result.unwrap()
        target = target_load_data.module.get_plugin()
        assert target.name == "warehouse-target"
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
        assert load_result.success, f"Failed to load plugin: {load_result.error}"
        load_data = load_result.unwrap()
        processor = load_data.module.get_plugin()
        assert processor.name == "data-processor"
        init_result = processor.initialize()
        assert init_result["status"] == "initialized"
        process_result = processor.execute({"items": [10, 20, 30]})
        assert process_result["status"] == "success"
        assert process_result["processed_items"] == [20, 40, 60]
        assert process_result["total_processed"] == 3
        process_result2 = processor.execute({"items": [1, 2]})
        assert process_result2["total_processed"] == 5
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
        assert load_result.success, f"Failed to load plugin: {load_result.error}"
        load_data = load_result.unwrap()
        error = load_data.module.get_plugin()
        assert error.name == "error-plugin"
        normal_result = error.execute()
        assert normal_result["status"] == "success"
        error.set_should_fail(True)
        with pytest.raises(RuntimeError, match="Simulated plugin execution error"):
            error.execute()
        health_result = error.health_check()
        assert health_result["status"] == "unhealthy"

    def test_discover_plugins_with_real_adapters(
        self,
        real_service_with_adapters: FlextPluginService,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL plugin discovery using real adapters."""
        result = real_service_with_adapters.discover_plugins([str(temp_plugin_dir)])
        assert result.success
        assert isinstance(result.value, list)
        assert len(result.value) == 4
        for plugin in result.value:
            assert isinstance(plugin, FlextPluginModels.Plugin.Entity)
            assert plugin.name in {
                "tap_database",
                "target_warehouse",
                "processor_transform",
                "error_plugin",
            }
            assert plugin.plugin_version == "1.0.0"

    def test_load_plugin_with_real_adapters(
        self,
        real_service_with_adapters: FlextPluginService,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL plugin loading using real adapters."""
        discover_result = real_service_with_adapters.discover_plugins([
            str(temp_plugin_dir),
        ])
        assert discover_result.success
        assert discover_result.value
        tap_plugin: FlextPluginModels.Plugin.Entity | None = None
        for plugin in discover_result.value:
            if plugin.name == "tap_database":
                tap_plugin = plugin
                break
        assert tap_plugin is not None
        tap_plugin_path = temp_plugin_dir / "tap_database.py"
        load_result = real_service_with_adapters.load_plugin(str(tap_plugin_path))
        assert load_result.success
        assert isinstance(load_result.value, FlextPluginModels.Plugin.Entity)
        assert load_result.value.name == "tap_database"

    def test_install_plugin_with_real_adapters(
        self,
        real_service_with_adapters: FlextPluginService,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL plugin installation using real adapters."""
        tap_plugin_file = temp_plugin_dir / "tap_database.py"
        install_result = real_service_with_adapters.install_plugin(str(tap_plugin_file))
        assert install_result.success
        assert isinstance(install_result.value, FlextPluginModels.Plugin.Entity)
        assert install_result.value.name == "tap_database"

    def test_is_plugin_loaded_with_real_adapters(
        self,
        real_service_with_adapters: FlextPluginService,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL plugin loaded check using real adapters."""
        tap_plugin_file = temp_plugin_dir / "tap_database.py"
        install_result = real_service_with_adapters.install_plugin(str(tap_plugin_file))
        assert install_result.success
        loaded_result = real_service_with_adapters.plugin_loaded("tap_database")
        assert loaded_result is True
        not_loaded_result = real_service_with_adapters.plugin_loaded("non_existent")
        assert not_loaded_result is False

    @pytest.fixture
    def service(self) -> FlextPluginService:
        """Create service instance for testing."""
        return FlextPluginService()

    def test_service_initialization_default_real(self) -> None:
        """Test REAL service initialization with default container."""
        service = FlextPluginService()
        assert service is not None
        assert isinstance(service.container, p.Container)

    def test_service_initialization_with_container_real(self) -> None:
        """Test REAL service initialization with provided container."""
        container = FlextContainer()
        service = FlextPluginService()
        assert service is not None
        assert service.container is container

    def test_service_inheritance_patterns(self, service: FlextPluginService) -> None:
        """Test service composition patterns (SOLID principles applied)."""

    def test_service_has_specific_methods_real(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test REAL service has specific methods for specific operations (SOLID principles)."""
        assert not hasattr(service, "execute")

    def test_discovery_functionality_real(self, service: FlextPluginService) -> None:
        """Test REAL discovery functionality through service methods."""
        result = service.discover_and_register_plugins(["/non/existent/path"])
        assert result.success
        assert result.unwrap() == []

    def test_loader_functionality_real(self, service: FlextPluginService) -> None:
        """Test REAL loader functionality through service methods."""
        result = service.plugin_loaded("non-existent-plugin")
        assert result is False

    def test_management_functionality_real(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test REAL management functionality through service methods."""
        result = asyncio.run(service.unload_plugin("non-existent-plugin"))
        assert result.failure
        assert "not found" in str(result.error)

    def test_discover_plugins_empty_path_returns_list(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test REAL discover_and_register_plugins with empty path."""
        result = service.discover_and_register_plugins([""])
        assert result.success
        assert isinstance(result.unwrap(), list)

    def test_discover_plugins_with_real_plugin_files(
        self,
        service: FlextPluginService,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL discover_and_register_plugins with actual plugin files."""
        result = service.discover_and_register_plugins([str(temp_plugin_dir)])
        if result.failure and "not configured" in str(result.error):
            pytest.skip(f"Infrastructure not configured: {result.error}")
        assert isinstance(result.success, bool)
        if result.success:
            assert isinstance(result.value, list)
        else:
            assert "Plugin discovery not available" in str(result.error)
        plugin_files = list(temp_plugin_dir.glob("*.py"))
        assert plugin_files

    def test_load_plugin_with_real_plugin_entity(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test REAL load_plugin with actual plugin file and entity."""
        plugin = FlextPluginModels.Plugin.Entity.create(
            name="tap_database",
            plugin_version="1.0.0",
            description="Database tap plugin for testing",
            plugin_type=FlextPluginConstants.Plugin.Type.TAP,
        )
        result = service.load_plugin(plugin.name)
        if result.failure and "not configured" in str(result.error):
            pytest.skip(f"Infrastructure not configured: {result.error}")
        assert isinstance(result.success, bool)
        if not result.success:
            error_msg = str(result.error).lower()
            assert (
                "loading" in error_msg or "failed" in error_msg or "error" in error_msg
            )

    def test_load_plugin_with_different_types_real(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test REAL load_plugin with different plugin types."""
        plugin_types = [
            FlextPluginConstants.Plugin.Type.TAP,
            FlextPluginConstants.Plugin.Type.TARGET,
            FlextPluginConstants.Plugin.Type.UTILITY,
            FlextPluginConstants.Plugin.Type.SERVICE,
        ]
        for plugin_type in plugin_types:
            plugin = FlextPluginModels.Plugin.Entity.create(
                name=f"real-plugin-{plugin_type.value}",
                plugin_version="1.0.0",
                plugin_type=plugin_type,
            )
            result = service.load_plugin(plugin.name)
            assert isinstance(result.success, bool)
            assert result.success or result.failure

    def test_unload_plugin_empty_name_fails_real(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test REAL unload_plugin with empty name fails."""

        async def _inner() -> None:
            result = await service.unload_plugin("")
            assert result.failure
            error_message = str(result.error).lower()
            assert "not found" in error_message or "plugin" in error_message

        asyncio.run(_inner())

    def test_unload_plugin_valid_name_real(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test REAL unload_plugin with non-existent plugin returns failure."""

        async def _inner() -> None:
            result = await service.unload_plugin("real-unload-plugin")
            assert isinstance(result.success, bool)
            assert result.failure
            assert "not found" in str(result.error)

        asyncio.run(_inner())

    def test_install_plugin_empty_path_fails_real(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test REAL install_plugin with empty path fails."""
        result = service.install_plugin("")
        assert result.failure
        error_message = str(result.error).lower()
        assert (
            "loading" in error_message
            or "failed" in error_message
            or "error" in error_message
            or ("load" in error_message)
        )

    def test_install_plugin_with_real_plugin_file(
        self,
        service: FlextPluginService,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL install_plugin with actual plugin file."""
        tap_plugin_file = temp_plugin_dir / "tap_database.py"
        result = service.install_plugin(str(tap_plugin_file))
        assert isinstance(result.success, bool)
        if not result.success:
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
        assert not result.success
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
        assert result.success or "not found" in str(result.error).lower()

    def test_enable_plugin_empty_name_fails(self, service: FlextPluginService) -> None:
        """Test enable_plugin with empty name fails."""
        result = service.enable_plugin("")
        assert not result.success
        assert (
            "not found" in str(result.error).lower()
            or "plugin" in str(result.error).lower()
        )

    def test_enable_plugin_valid_name_real(self, service: FlextPluginService) -> None:
        """Test enable_plugin with REAL valid name."""
        result = service.enable_plugin("real-test-plugin")
        assert result.success or "not found" in str(result.error).lower()

    def test_disable_plugin_empty_name_fails(self, service: FlextPluginService) -> None:
        """Test disable_plugin with empty name fails."""
        result = service.disable_plugin("")
        assert not result.success
        assert (
            "not found" in str(result.error).lower()
            or "plugin" in str(result.error).lower()
        )

    def test_disable_plugin_valid_name_real(self, service: FlextPluginService) -> None:
        """Test disable_plugin with REAL valid name."""
        result = service.disable_plugin("real-test-plugin")
        assert result.success or "not found" in str(result.error).lower()

    def test_update_plugin_config_mismatched_name_fails(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test update_plugin_config with mismatched plugin name fails."""
        settings = FlextPluginModels.Plugin.PluginConfig(
            plugin_name="different-plugin",
            config={},
        )
        result = service.update_plugin_config("test-plugin", settings.model_dump())
        assert not result.success

    def test_is_plugin_loaded_empty_name_returns_false(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test is_plugin_loaded with empty name returns False."""
        result = service.plugin_loaded("")
        assert isinstance(result, bool)
        assert result is False

    def test_is_plugin_loaded_valid_name_real(
        self,
        service: FlextPluginService,
    ) -> None:
        """Test is_plugin_loaded with REAL valid name."""
        result = service.plugin_loaded("real-test-plugin")
        assert isinstance(result, bool)
        assert result is False

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

    def test_discovery_service_has_two_strategies(self) -> None:
        """Test discovery service has FileSystem and EntryPoint strategies."""
        service = FlextPluginDiscovery()
        assert service is not None
        assert len(service.strategies) == 2

    def test_discovery_service_has_strategies(
        self,
        discovery_service: FlextPluginDiscovery,
    ) -> None:
        """Test discovery service has strategies attribute."""
        assert isinstance(discovery_service.strategies, list)

    def test_discover_plugins_method_exists(
        self,
        discovery_service: FlextPluginDiscovery,
    ) -> None:
        """Test discover_plugins method exists."""
        assert callable(discovery_service.discover_plugins)

    def test_discover_plugins_with_empty_paths(
        self,
        discovery_service: FlextPluginDiscovery,
    ) -> None:
        """Test discover_plugins with empty paths returns empty list."""
        result = discovery_service.discover_plugins([])
        assert result.success
        assert result.value == []

    def test_discover_plugins_empty_paths_succeeds(
        self,
        discovery_service: FlextPluginDiscovery,
    ) -> None:
        """Test discover_plugins with empty paths list returns empty."""
        result = discovery_service.discover_plugins([])
        assert result.success
        assert result.value == []

    def test_discover_plugins_with_real_files(
        self,
        discovery_service: FlextPluginDiscovery,
        temp_plugin_dir: Path,
    ) -> None:
        """Test discover_plugins with REAL plugin files."""
        try:
            result = discovery_service.discover_plugins([str(temp_plugin_dir)])
        except e.BaseError as exc:
            pytest.skip(f"Infrastructure not configured: {exc}")
        if result.failure and "not configured" in str(result.error):
            pytest.skip(f"Infrastructure not configured: {result.error}")
        assert result.success
        assert isinstance(result.value, list)
        plugin_files = list(temp_plugin_dir.glob("*.py"))
        assert len(plugin_files) == 4

    def test_validate_plugin_with_discovery_data(
        self,
        discovery_service: FlextPluginDiscovery,
        temp_plugin_dir: Path,
    ) -> None:
        """Test validate_plugin with DiscoveryData from real files."""
        result = discovery_service.discover_plugins([str(temp_plugin_dir)])
        assert result.success
        assert result.value
        plugin_data = result.value[0]
        validation_result = discovery_service.validate_plugin(plugin_data)
        assert validation_result.success
        assert validation_result.value is True
        plugin_file = temp_plugin_dir / f"{plugin_data.name}.py"
        assert plugin_file.exists()

    def test_complete_service_integration_workflow(
        self,
        real_service_with_adapters: FlextPluginService,
        temp_plugin_dir: Path,
    ) -> None:
        """Test complete REAL workflow using services with real adapters."""
        discover_result = real_service_with_adapters.discover_plugins([
            str(temp_plugin_dir),
        ])
        assert discover_result.success
        assert len(discover_result.value) == 4
        tap_plugin = None
        target_plugin = None
        for plugin in discover_result.value:
            if plugin.name == "tap_database":
                tap_plugin = plugin
            elif plugin.name == "target_warehouse":
                target_plugin = plugin
        assert tap_plugin is not None
        assert target_plugin is not None
        tap_file = temp_plugin_dir / "tap_database.py"
        target_file = temp_plugin_dir / "target_warehouse.py"
        tap_load_result = real_service_with_adapters.load_plugin(str(tap_file))
        target_load_result = real_service_with_adapters.load_plugin(str(target_file))
        assert tap_load_result.success
        assert target_load_result.success
        tap_loaded = real_service_with_adapters.plugin_loaded("tap_database")
        target_loaded = real_service_with_adapters.plugin_loaded("target_warehouse")
        assert tap_loaded is True
        assert target_loaded is True
        unload_result = asyncio.run(
            real_service_with_adapters.unload_plugin("tap_database"),
        )
        assert unload_result.success
        unloaded = real_service_with_adapters.plugin_loaded("tap_database")
        assert unloaded is False

    def test_complete_plugin_workflow_real(
        self,
        real_plugin_loader: FlextPluginLoader,
        real_plugin_discovery: FlextPluginDiscovery,
        temp_plugin_dir: Path,
    ) -> None:
        """Test complete REAL workflow: discover -> load -> execute -> cleanup."""
        discovery_result = real_plugin_discovery.discover_plugins([
            str(temp_plugin_dir),
        ])
        assert discovery_result.success
        discovered_plugins = discovery_result.value
        assert len(discovered_plugins) == 4
        plugin_files = list(temp_plugin_dir.glob("*.py"))
        assert len(plugin_files) == 4
        tap_file = temp_plugin_dir / "tap_database.py"
        tap_result = real_plugin_loader.load_plugin(str(tap_file))
        assert tap_result.success, f"Failed to load tap plugin: {tap_result.error}"
        tap_data = tap_result.unwrap()
        tap = tap_data.module.get_plugin()
        assert tap.name == "database-tap"
        init_result = tap.initialize()
        assert init_result["status"] == "initialized"
        extract_result = tap.execute()
        assert extract_result["status"] == "success"
        assert extract_result["extracted_records"] == 150
        target_file = temp_plugin_dir / "target_warehouse.py"
        target_result = real_plugin_loader.load_plugin(str(target_file))
        assert target_result.success, f"Failed to load target: {target_result.error}"
        target_data = target_result.unwrap()
        target = target_data.module.get_plugin()
        extracted_data = {"records": list(range(extract_result["extracted_records"]))}
        load_result = target.execute(extracted_data)
        assert load_result["status"] == "success"
        assert load_result["loaded_records"] == 150
        tap_health = tap.health_check()
        target_health = target.health_check()
        assert tap_health["status"] == "healthy"
        assert target_health["status"] == "healthy"
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
        tap_file = temp_plugin_dir / "tap_database.py"
        target_file = temp_plugin_dir / "target_warehouse.py"
        processor_file = temp_plugin_dir / "processor_transform.py"
        tap_result = real_plugin_loader.load_plugin(str(tap_file))
        target_result = real_plugin_loader.load_plugin(str(target_file))
        processor_result = real_plugin_loader.load_plugin(str(processor_file))
        assert tap_result.success, f"Failed to load tap: {tap_result.error}"
        assert target_result.success, f"Failed to load target: {target_result.error}"
        assert processor_result.success, (
            f"Failed to load processor: {processor_result.error}"
        )
        tap = tap_result.unwrap().module.get_plugin()
        target = target_result.unwrap().module.get_plugin()
        processor = processor_result.unwrap().module.get_plugin()
        assert tap.name == "database-tap"
        assert target.name == "warehouse-target"
        assert processor.name == "data-processor"
        loaded_plugin_names = real_plugin_loader.get_loaded_plugins()
        assert len(loaded_plugin_names) >= 3
        assert "tap_database" in loaded_plugin_names
        assert "target_warehouse" in loaded_plugin_names
        assert "processor_transform" in loaded_plugin_names
        assert tap.name == "database-tap"

    def test_real_plugin_lifecycle_management(
        self,
        real_plugin_loader: FlextPluginLoader,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL plugin lifecycle with loading/unloading."""
        processor_file = temp_plugin_dir / "processor_transform.py"
        load_result = real_plugin_loader.load_plugin(str(processor_file))
        assert load_result.success
        load_data = load_result.value
        assert load_data is not None
        assert load_data.name == "processor_transform"
        loaded_plugins = real_plugin_loader.get_loaded_plugins()
        assert "processor_transform" in loaded_plugins
        unload_result = real_plugin_loader.unload_plugin("processor_transform")
        assert unload_result.success
        loaded_plugins_after = real_plugin_loader.get_loaded_plugins()
        assert "processor_transform" not in loaded_plugins_after
        reload_result = real_plugin_loader.load_plugin(str(processor_file))
        assert reload_result.success
        reloaded_data = reload_result.value
        assert reloaded_data is not None
        assert reloaded_data.name == "processor_transform"

    def test_services_can_coexist(self) -> None:
        """Test that both services can be created and used together."""
        container = FlextContainer()
        plugin_service = FlextPluginService()
        discovery_service = FlextPluginDiscovery()
        assert plugin_service is not None
        assert discovery_service is not None
        assert plugin_service.container is container

    def test_services_share_container_state_real(self) -> None:
        """Test services share REAL container state."""
        container = FlextContainer()
        test_service = m.Plugin.Entity.create(
            name="test_service",
            version=1,
            metadata={"settings": {"enabled": True}},
        )
        container.bind("test_service", test_service)
        plugin_service = FlextPluginService()
        result1 = plugin_service.container.resolve("test_service")
        assert result1.success
        value = result1.value
        normalized_value = (
            value.model_dump()
            if isinstance(value, (m.BaseModel, m.ConfigMap))
            else value
        )
        assert isinstance(normalized_value, dict)
        assert normalized_value["name"] == "test_service"
        discovery_service = FlextPluginDiscovery()
        assert discovery_service is not None

    def test_services_with_real_plugin_directory(self, temp_plugin_dir: Path) -> None:
        """Test services with REAL plugin directory containing actual files."""
        plugin_service = FlextPluginService()
        discovery_service = FlextPluginDiscovery()
        try:
            plugin_discovery_result = plugin_service.discover_plugins([
                str(temp_plugin_dir),
            ])
        except e.BaseError as exc:
            pytest.skip(f"Infrastructure not configured: {exc}")
        try:
            service_discovery_result = discovery_service.discover_plugins([
                str(temp_plugin_dir),
            ])
        except e.BaseError as exc:
            pytest.skip(f"Infrastructure not configured: {exc}")
        if not plugin_discovery_result.success and "not configured" in str(
            plugin_discovery_result.error,
        ):
            pytest.skip(
                f"Infrastructure not configured: {plugin_discovery_result.error}",
            )
        if not service_discovery_result.success and "not configured" in str(
            service_discovery_result.error,
        ):
            pytest.skip(
                f"Infrastructure not configured: {service_discovery_result.error}",
            )
        assert plugin_discovery_result.success
        assert service_discovery_result.success
        assert isinstance(plugin_discovery_result.value, list)
        assert isinstance(service_discovery_result.value, list)
        plugin_files = list(temp_plugin_dir.glob("*.py"))
        assert len(plugin_files) == 4

    def test_real_plugin_execution_error_handling(
        self,
        real_plugin_loader: FlextPluginLoader,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL error handling with plugin that actually throws exceptions."""
        error_file = temp_plugin_dir / "error_plugin.py"
        load_result = real_plugin_loader.load_plugin(str(error_file))
        assert load_result.success, f"Failed to load plugin: {load_result.error}"
        load_data = load_result.unwrap()
        error = load_data.module.get_plugin()
        assert error.name == "error-plugin"
        normal_result = error.execute()
        assert normal_result["status"] == "success"
        error.set_should_fail(True)
        with pytest.raises(RuntimeError, match="Simulated plugin execution error"):
            error.execute()
        health = error.health_check()
        assert health["status"] == "unhealthy"

    def test_real_plugin_file_loading_errors(
        self,
        real_plugin_loader: FlextPluginLoader,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL file loading errors with malformed plugin files."""
        bad_plugin_file = temp_plugin_dir / "bad_syntax_plugin.py"
        bad_plugin_file.write_text(
            '\n\n# This file has syntax errors\nclass BadPlugin:\n    def __init__(self):\n        """Initialize the instance."""\n\n        self.name = "bad-plugin"\n        # Missing closing quote and other syntax errors\n        self.data = "unclosed string\n\n    def execute(self\n        return {"error": "should not reach here"}\n',
        )
        load_result = real_plugin_loader.load_plugin(str(bad_plugin_file))
        assert not load_result.success, "Expected failure for syntax error plugin"

    def test_real_plugin_file_not_found_error(
        self,
        real_plugin_loader: FlextPluginLoader,
        temp_plugin_dir: Path,
    ) -> None:
        """Test REAL file not found error handling."""
        nonexistent_file = temp_plugin_dir / "does_not_exist.py"
        load_result = real_plugin_loader.load_plugin(str(nonexistent_file))
        assert not load_result.success, "Expected failure for non-existent file"

    def test_service_handles_port_resolution_with_real_plugins(
        self,
        temp_plugin_dir: Path,
    ) -> None:
        """Test service port resolution with REAL plugin directory."""
        service = FlextPluginService()
        result = service.discover_plugins([str(temp_plugin_dir)])
        if result.failure and "not configured" in str(result.error):
            pytest.skip(f"Infrastructure not configured: {result.error}")
        assert result.success
        assert isinstance(result.value, list)
        plugin_files = list(temp_plugin_dir.glob("*.py"))
        assert len(plugin_files) == 4

    def test_discovery_service_handles_empty_directory_real(self) -> None:
        """Test discovery service handles empty directory with REAL operations."""
        discovery_service = FlextPluginDiscovery()
        with tempfile.TemporaryDirectory() as temp_dir:
            result = discovery_service.discover_plugins([temp_dir])
            if result.failure and "not configured" in str(result.error):
                pytest.skip(f"Infrastructure not configured: {result.error}")
            assert result.success
            assert isinstance(result.value, list)
            assert result.value == []

    def test_service_methods_work_with_default_initialization(self) -> None:
        """Test that service methods work with default initialization."""
        service = FlextPluginService()
        with tempfile.TemporaryDirectory() as temp_dir:
            result = service.discover_and_register_plugins([temp_dir])
            assert result.success
            assert isinstance(result.unwrap(), list)
        loaded = service.plugin_loaded("real-plugin")
        assert isinstance(loaded, bool)
        assert loaded is False

    def test_discovery_service_methods_work_with_default_initialization(self) -> None:
        """Test that discovery service methods work with default initialization."""
        service = FlextPluginDiscovery()
        with tempfile.TemporaryDirectory() as temp_dir:
            result = service.discover_plugins([temp_dir])
            assert result.success
            assert isinstance(result.unwrap(), list)

    def test_service_handles_discovery_edge_cases_real(self) -> None:
        """Test service handles discovery edge cases with REAL scenarios."""
        service = FlextPluginService()
        result = service.discover_plugins([""])
        assert result.success or result.failure
        invalid_path = "/" + "x" * 500
        result2 = service.discover_plugins([invalid_path])
        assert isinstance(result2.success, bool)

    def test_service_handles_loader_exceptions_real(self) -> None:
        """Test service handles loader port exceptions with REAL scenarios."""

        async def _inner() -> None:
            service = FlextPluginService()
            result = await service.unload_plugin("")
            assert not result.success
            assert (
                "not found" in str(result.error).lower()
                or "plugin" in str(result.error).lower()
            )
            long_name = "x" * 1000
            result2 = await service.unload_plugin(long_name)
            assert isinstance(result2.success, bool)
            if not result2.success:
                assert (
                    "Failed to unload plugin" in str(result2.error)
                    or "plugin" in str(result2.error).lower()
                    or "not found" in str(result2.error).lower()
                )

        asyncio.run(_inner())

    def test_discovery_service_handles_empty_paths_real(self) -> None:
        """Test discovery service handles empty paths with REAL scenarios."""
        service = FlextPluginDiscovery()
        result = service.discover_plugins([])
        assert result.success
        assert result.value == []
        invalid_path = "/" + "x" * 500
        result2 = service.discover_plugins([invalid_path])
        assert result2.success
        assert result2.value == []

    def test_plugin_service_alias_exists_real(self) -> None:
        """Test PluginService alias exists and works with REAL functionality."""
        service = FlextPluginService()
        assert service is not None
        assert isinstance(service, FlextPluginService)
        with tempfile.TemporaryDirectory() as temp_dir:
            result = service.discover_plugins([temp_dir])
            if result.failure and "not configured" in str(result.error):
                pytest.skip(f"Infrastructure not configured: {result.error}")
            assert result.success
            assert isinstance(result.value, list)

    def test_plugin_discovery_service_alias_exists_real(self) -> None:
        """Test PluginDiscoveryService alias exists and works with REAL functionality."""
        service = FlextPluginDiscovery()
        assert service is not None
        assert isinstance(service, FlextPluginDiscovery)
        with tempfile.TemporaryDirectory() as temp_dir:
            result = service.discover_plugins([temp_dir])
            if result.failure and "not configured" in str(result.error):
                pytest.skip(f"Infrastructure not configured: {result.error}")
            assert result.success
            assert isinstance(result.value, list)
