"""REAL Test Configuration for FLEXT Plugin System.

This module provides REAL pytest fixtures for testing the FLEXT plugin system
without mocks. All fixtures create actual plugin files, directories, and real
instances for comprehensive functionality testing.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from flext_plugin import (
    FlextPluginEntities,
    PluginType,
    RealPluginDiscoveryAdapter,
    RealPluginLoaderAdapter,
    RealPluginManagerAdapter,
)

from flext_core import FlextContainer, FlextTypes


# Test environment setup
@pytest.fixture(autouse=True)
def set_test_environment() -> Generator[None]:
    """Set test environment variables."""
    os.environ["FLEXT_ENV"] = "test"
    os.environ["FLEXT_LOG_LEVEL"] = "debug"
    yield
    # Cleanup
    os.environ.pop("FLEXT_ENV", None)
    os.environ.pop("FLEXT_LOG_LEVEL", None)


# REAL Plugin test configuration
@pytest.fixture
def real_plugin_config() -> FlextTypes.Dict:
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
def real_plugin_data() -> FlextTypes.Dict:
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
        ],
    }


# REAL Plugin fixtures
@pytest.fixture
def real_plugin_directory() -> Generator[Path]:
    """Create temporary directory with REAL plugin files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        plugin_dir = Path(tmp_dir)

        # Create REAL working plugin files
        tap_plugin = plugin_dir / "tap_database.py"
        tap_plugin.write_text('''
"""REAL tap plugin for database extraction."""

class DatabaseTapPlugin:
    def __init__(self):
        """Initialize the instance."""

        self.name = "database-tap"
        self.version = "1.0.0"
        self.plugin_type = "tap"
        self.config = {"tables": ["users", "orders"]}

    def execute(self):
        return {
            "extracted_records": 150,
            "tables": self.config["tables"],
            "status": "success"
        }

def get_plugin():
    return DatabaseTapPlugin()
''')

        target_plugin = plugin_dir / "target_warehouse.py"
        target_plugin.write_text('''
"""REAL target plugin for data warehouse loading."""

class WarehouseTargetPlugin:
    def __init__(self):
        """Initialize the instance."""

        self.name = "warehouse-target"
        self.version = "1.0.0"
        self.plugin_type = "target"
        self.config = {"batch_size": 1000}

    def execute(self):
        return {
            "loaded_records": 150,
            "batch_size": self.config["batch_size"],
            "status": "success"
        }

    def cleanup(self):
        pass

def get_plugin():
    return WarehouseTargetPlugin()
''')

        processor_plugin = plugin_dir / "processor_transform.py"
        processor_plugin.write_text('''
"""REAL processor plugin for data transformation."""

class TransformProcessorPlugin:
    def __init__(self):
        """Initialize the instance."""

        self.name = "transform-processor"
        self.version = "1.0.0"
        self.plugin_type = "processor"
        self.config = {"transform_rules": ["uppercase", "trim"]}

    def execute(self):
        return {
            "processed_records": 150,
            "transforms": len(self.config["transform_rules"]),
            "status": "success"
        }

    def cleanup(self):
        pass

def get_plugin():
    return TransformProcessorPlugin()
''')

        yield plugin_dir


@pytest.fixture
def real_container_with_adapters(real_plugin_directory: Path) -> FlextContainer:
    """Create FlextContainer with REAL adapters registered."""
    container = FlextContainer()

    # Register REAL implementations
    plugin_dir_str = str(real_plugin_directory)
    discovery_adapter = RealPluginDiscoveryAdapter(plugin_dir_str)
    loader_adapter = RealPluginLoaderAdapter(plugin_dir_str)
    manager_adapter = RealPluginManagerAdapter(plugin_dir_str)

    container.register("plugin_discovery_port", discovery_adapter)
    container.register("plugin_loader_port", loader_adapter)
    container.register("plugin_manager_port", manager_adapter)

    return container


@pytest.fixture
def real_plugin_entity() -> FlextPluginEntities.Entity:
    """Create REAL FlextPluginEntities.Entity for testing."""
    return FlextPluginEntities.Entity.create(
        name="real-test-plugin",
        plugin_version="1.0.0",
        description="Real plugin entity for comprehensive testing",
        plugin_type=PluginType.UTILITY,
    )


# REAL Discovery fixtures
@pytest.fixture
def real_discovery_adapter(real_plugin_directory: Path) -> RealPluginDiscoveryAdapter:
    """Create REAL discovery adapter with plugin directory."""
    return RealPluginDiscoveryAdapter(str(real_plugin_directory))


# REAL Loader fixtures
@pytest.fixture
def real_loader_adapter(real_plugin_directory: Path) -> RealPluginLoaderAdapter:
    """Create REAL loader adapter with plugin directory."""
    return RealPluginLoaderAdapter(str(real_plugin_directory))


@pytest.fixture
def real_manager_adapter(real_plugin_directory: Path) -> RealPluginManagerAdapter:
    """Create REAL manager adapter with plugin directory."""
    return RealPluginManagerAdapter(str(real_plugin_directory))


# REAL Configuration fixtures
@pytest.fixture
def real_plugin_configs() -> FlextTypes.NestedDict:
    """REAL plugin configurations matching plugin files."""
    return {
        "tap_database": {
            "tables": ["users", "orders", "products"],
            "connection": {
                "host": "localhost",
                "port": 5432,
                "database": "test_db",
            },
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


# Pytest markers for test categorization
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


# REAL Plugin Entity fixtures
@pytest.fixture
def real_tap_plugin() -> FlextPluginEntities.Entity:
    """Create REAL tap plugin entity."""
    return FlextPluginEntities.Entity.create(
        name="tap-database",
        plugin_version="1.0.0",
        description="Real database tap plugin",
        plugin_type=PluginType.TAP,
    )


@pytest.fixture
def real_target_plugin() -> FlextPluginEntities.Entity:
    """Create REAL target plugin entity."""
    return FlextPluginEntities.Entity.create(
        name="target-warehouse",
        plugin_version="1.0.0",
        description="Real warehouse target plugin",
        plugin_type=PluginType.TARGET,
    )


@pytest.fixture
def real_processor_plugin() -> FlextPluginEntities.Entity:
    """Create REAL processor plugin entity."""
    return FlextPluginEntities.Entity.create(
        name="processor-transform",
        plugin_version="1.0.0",
        description="Real transform processor plugin",
        plugin_type=PluginType.PROCESSOR,
    )


# REAL Dependency fixtures
@pytest.fixture
def real_plugin_dependencies() -> dict[str, FlextTypes.StringList]:
    """REAL plugin dependency graph."""
    return {
        "tap_database": [],
        "processor_transform": ["tap_database"],
        "target_warehouse": ["processor_transform"],
    }


# Performance testing fixtures
@pytest.fixture
def performance_config() -> FlextTypes.Dict:
    """Configuration for REAL plugin performance testing."""
    return {
        "max_load_time": 2.0,  # seconds for real plugins
        "max_memory_usage": 50,  # MB
        "max_cpu_usage": 25,  # percentage
        "test_iterations": 10,  # Reduced for real testing
    }
