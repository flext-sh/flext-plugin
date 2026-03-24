"""REAL Test Configuration for FLEXT Plugin System.

This module provides REAL pytest fixtures for testing the FLEXT plugin system
without mocks. All fixtures create actual plugin files, directories, and real
instances for comprehensive functionality testing.

NOTE: Contains test classes defined in strings for creating real plugins.
These violate facade rules but are acceptable for test fixtures.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os
import tempfile
from collections.abc import Sequence, Generator, Mapping
from pathlib import Path

import pytest
from flext_core import FlextContainer

from flext_plugin import FlextPluginAdapters, FlextPluginModels
from tests import t


@pytest.fixture(autouse=True)
def set_test_environment() -> Generator[None]:
    """Set test environment variables."""
    os.environ["FLEXT_ENV"] = "test"
    os.environ["FLEXT_LOG_LEVEL"] = "DEBUG"
    yield
    os.environ.pop("FLEXT_ENV", None)
    os.environ.pop("FLEXT_LOG_LEVEL", None)


@pytest.fixture
def real_plugin_config() -> t.ContainerMapping:
    """REAL plugin configuration for testing."""
    return {
        "plugin_directory": tempfile.mkdtemp(prefix="test_plugins_"),
        "auto_discover": True,
        "hot_reload": True,
        "security_enabled": False,
        "max_plugins": 50,
        "timeout": 10,
    }


@pytest.fixture
def simple_plugin_directory() -> Generator[Path]:
    """Simple temporary directory for basic tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        plugin_dir = Path(temp_dir) / "test_plugins"
        plugin_dir.mkdir()
        yield plugin_dir


@pytest.fixture
def real_plugin_data() -> t.ContainerMapping:
    """REAL plugin data matching actual plugin files."""
    return {
        "plugins": [
            {
                "name": "tap_database",
                "version": "1.0.0",
                "description": "REAL tap plugin for database extraction",
                "type": "tap",
                "config": {"tables": ["users", "orders"]},
                "enabled": True,
            },
            {
                "name": "target_warehouse",
                "version": "1.0.0",
                "description": "REAL target plugin for warehouse loading",
                "type": "target",
                "config": {"batch_size": 1000},
                "enabled": True,
            },
            {
                "name": "processor_transform",
                "version": "1.0.0",
                "description": "REAL processor plugin for transformations",
                "type": "processor",
                "config": {"transform_rules": ["uppercase", "trim"]},
                "enabled": True,
            },
        ]
    }


@pytest.fixture
def real_plugin_directory() -> Generator[Path]:
    """Create temporary directory with REAL plugin files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        plugin_dir = Path(tmp_dir)
        tap_plugin = plugin_dir / "tap_database.py"
        tap_plugin.write_text(
            '\n"""REAL tap plugin for database extraction."""\n\n# TEST CLASS - Acceptable exception for conftest.py\nclass DatabaseTapPlugin:\n    def __init__(self):\n        """Initialize the instance."""\n\n        self.name = "database-tap"\n        self.version = "1.0.0"\n        self.plugin_type = "tap"\n        self.config = {"tables": ["users", "orders"]}\n\n    def execute(self):\n        return {\n            "extracted_records": 150,\n            "tables": self.config["tables"],\n            "status": "success"\n        }\n\ndef get_plugin():\n    return DatabaseTapPlugin()\n'
        )
        target_plugin = plugin_dir / "target_warehouse.py"
        target_plugin.write_text(
            '\n"""REAL target plugin for data warehouse loading."""\n\n# TEST CLASS - Acceptable exception for conftest.py\nclass WarehouseTargetPlugin:\n    def __init__(self):\n        """Initialize the instance."""\n\n        self.name = "warehouse-target"\n        self.version = "1.0.0"\n        self.plugin_type = "target"\n        self.config = {"batch_size": 1000}\n\n    def execute(self):\n        return {\n            "loaded_records": 150,\n            "batch_size": self.config["batch_size"],\n            "status": "success"\n        }\n\n    def cleanup(self):\n        """Clean up warehouse resources."""\n        # Reset batch size and clear any pending batches\n        self.config["batch_size"] = 1000\n        self.config.clear()\n\ndef get_plugin():\n    return WarehouseTargetPlugin()\n'
        )
        processor_plugin = plugin_dir / "processor_transform.py"
        processor_plugin.write_text(
            '\n"""REAL processor plugin for data transformation."""\n\n# TEST CLASS - Acceptable exception for conftest.py\nclass TransformProcessorPlugin:\n    def __init__(self):\n        """Initialize the instance."""\n\n        self.name = "transform-processor"\n        self.version = "1.0.0"\n        self.plugin_type = "processor"\n        self.config = {"transform_rules": ["uppercase", "trim"]}\n\n    def execute(self):\n        return {\n            "processed_records": 150,\n            "transforms": len(self.config["transform_rules"]),\n            "status": "success"\n        }\n\n    def cleanup(self):\n        """Clean up processor resources."""\n        # Reset transform rules and clear any cached state\n        self.config["transform_rules"] = []\n        self.config.clear()\n\ndef get_plugin():\n    return TransformProcessorPlugin()\n'
        )
        yield plugin_dir


@pytest.fixture
def real_container_with_adapters() -> FlextContainer:
    """Create FlextContainer with REAL adapters registered."""
    container = FlextContainer()
    discovery_adapter = FlextPluginAdapters.FileSystemDiscoveryAdapter()
    loader_adapter = FlextPluginAdapters.DynamicLoaderAdapter()
    manager_adapter = FlextPluginAdapters.PluginExecutorAdapter()
    container.register("plugin_discovery_port", discovery_adapter)
    container.register("plugin_loader_port", loader_adapter)
    container.register("plugin_manager_port", manager_adapter)
    return container


@pytest.fixture
def real_plugin_entity() -> FlextPluginModels.Plugin.Plugin:
    """Create REAL FlextPluginModels.Plugin for testing."""
    return FlextPluginModels.Plugin.Plugin(
        name="real-test-plugin",
        plugin_version="1.0.0",
        description="Real plugin entity for comprehensive testing",
        author="test-suite",
        plugin_type="utility",
        is_enabled=True,
        metadata={},
    )


@pytest.fixture
def real_discovery_adapter() -> FlextPluginAdapters.FileSystemDiscoveryAdapter:
    """Create REAL discovery adapter."""
    return FlextPluginAdapters.FileSystemDiscoveryAdapter()


@pytest.fixture
def real_loader_adapter() -> FlextPluginAdapters.DynamicLoaderAdapter:
    """Create REAL loader adapter."""
    return FlextPluginAdapters.DynamicLoaderAdapter()


@pytest.fixture
def real_manager_adapter() -> FlextPluginAdapters.PluginExecutorAdapter:
    """Create REAL manager adapter."""
    return FlextPluginAdapters.PluginExecutorAdapter()


@pytest.fixture
def real_plugin_configs() -> Mapping[
    str,
    Mapping[str, t.ContainerMapping | Sequence[str] | t.NormalizedValue],
]:
    """REAL plugin configurations matching plugin files."""
    return {
        "tap_database": {
            "tables": ["users", "orders", "products"],
            "connection": {"host": "localhost", "port": 5432, "database": "test_db"},
        },
        "target_warehouse": {
            "batch_size": 1000,
            "connection": {
                "host": "warehouse.example.com",
                "port": 5432,
                "database": "analytics",
            },
        },
        "processor_transform": {
            "transform_rules": ["uppercase", "trim", "normalize"],
            "batch_processing": True,
            "parallel_workers": 4,
        },
    }


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "plugin: Plugin-specific tests")
    config.addinivalue_line("markers", "discovery: Plugin discovery tests")
    config.addinivalue_line("markers", "lifecycle: Plugin lifecycle tests")
    config.addinivalue_line("markers", "hot_reload: Hot reload tests")
    config.addinivalue_line("markers", "slow: Slow tests")


@pytest.fixture
def real_tap_plugin() -> FlextPluginModels.Plugin.Plugin:
    """Create REAL tap plugin entity."""
    return FlextPluginModels.Plugin.Plugin(
        name="tap-database",
        plugin_version="1.0.0",
        description="Real database tap plugin",
        author="test-suite",
        plugin_type=FlextPluginModels.PluginType.TAP,
        is_enabled=True,
        metadata={},
    )


@pytest.fixture
def real_target_plugin() -> FlextPluginModels.Plugin.Plugin:
    """Create REAL target plugin entity."""
    return FlextPluginModels.Plugin.Plugin(
        name="target-warehouse",
        plugin_version="1.0.0",
        description="Real warehouse target plugin",
        author="test-suite",
        plugin_type=FlextPluginModels.PluginType.TARGET,
        is_enabled=True,
        metadata={},
    )


@pytest.fixture
def real_processor_plugin() -> FlextPluginModels.Plugin.Plugin:
    """Create REAL processor plugin entity."""
    return FlextPluginModels.Plugin.Plugin(
        name="processor-transform",
        plugin_version="1.0.0",
        description="Real transform processor plugin",
        author="test-suite",
        plugin_type=FlextPluginModels.PluginType.PROCESSOR,
        is_enabled=True,
        metadata={},
    )


@pytest.fixture
def real_plugin_dependencies() -> Mapping[str, Sequence[str]]:
    """REAL plugin dependency graph."""
    return {
        "tap_database": [],
        "processor_transform": ["tap_database"],
        "target_warehouse": ["processor_transform"],
    }


@pytest.fixture
def performance_config() -> t.ContainerMapping:
    """Configuration for REAL plugin performance testing."""
    return {
        "max_load_time": 2.0,
        "max_memory_usage": 50,
        "max_cpu_usage": 25,
        "test_iterations": 10,
    }
