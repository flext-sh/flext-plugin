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
from collections.abc import Generator
from pathlib import Path

import pytest
from flext_core import FlextContainer, t

from flext_plugin.adapters import FlextPluginAdapters
from flext_plugin.models import FlextPluginModels


# Test environment setup
@pytest.fixture(autouse=True)
def set_test_environment() -> Generator[None]:
    """Set test environment variables."""
    os.environ["FLEXT_ENV"] = "test"
    os.environ["FLEXT_LOG_LEVEL"] = "DEBUG"
    yield
    # Cleanup
    os.environ.pop("FLEXT_ENV", None)
    os.environ.pop("FLEXT_LOG_LEVEL", None)


# REAL Plugin test configuration
@pytest.fixture
def real_plugin_config() -> dict[str, t.GeneralValueType]:
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
def real_plugin_data() -> dict[str, t.GeneralValueType]:
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

# TEST CLASS - Acceptable exception for conftest.py
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

# TEST CLASS - Acceptable exception for conftest.py
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
        # STUB - Test implementation
        pass

def get_plugin():
    return WarehouseTargetPlugin()
''')

        processor_plugin = plugin_dir / "processor_transform.py"
        processor_plugin.write_text('''
"""REAL processor plugin for data transformation."""

# TEST CLASS - Acceptable exception for conftest.py
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
        # STUB - Test implementation
        pass

def get_plugin():
    return TransformProcessorPlugin()
''')

        yield plugin_dir


@pytest.fixture
def real_container_with_adapters() -> FlextContainer:
    """Create FlextContainer with REAL adapters registered."""
    container = FlextContainer()

    # Register REAL implementations
    discovery_adapter = FlextPluginAdapters.FileSystemDiscoveryAdapter()
    loader_adapter = FlextPluginAdapters.DynamicLoaderAdapter()
    manager_adapter = FlextPluginAdapters.PluginExecutorAdapter()

    container.with_service("plugin_discovery_port", discovery_adapter)
    container.with_service("plugin_loader_port", loader_adapter)
    container.with_service("plugin_manager_port", manager_adapter)

    return container


@pytest.fixture
def real_plugin_entity() -> FlextPluginModels.Plugin:
    """Create REAL FlextPluginModels.Plugin for testing."""
    return FlextPluginModels.Plugin.create(
        name="real-test-plugin",
        plugin_version="1.0.0",
        description="Real plugin entity for comprehensive testing",
        plugin_type=FlextPluginModels.PluginType.UTILITY,
    )


# REAL Discovery fixtures
@pytest.fixture
def real_discovery_adapter() -> FlextPluginAdapters.FileSystemDiscoveryAdapter:
    """Create REAL discovery adapter."""
    return FlextPluginAdapters.FileSystemDiscoveryAdapter()


# REAL Loader fixtures
@pytest.fixture
def real_loader_adapter() -> FlextPluginAdapters.DynamicLoaderAdapter:
    """Create REAL loader adapter."""
    return FlextPluginAdapters.DynamicLoaderAdapter()


@pytest.fixture
def real_manager_adapter() -> FlextPluginAdapters.PluginExecutorAdapter:
    """Create REAL manager adapter."""
    return FlextPluginAdapters.PluginExecutorAdapter()


# REAL Configuration fixtures
@pytest.fixture
def real_plugin_configs() -> dict[
    str,
    dict[str, dict[str, t.GeneralValueType] | list[str] | object],
]:
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
def real_tap_plugin() -> FlextPluginModels.Plugin:
    """Create REAL tap plugin entity."""
    return FlextPluginModels.Plugin.create(
        name="tap-database",
        plugin_version="1.0.0",
        description="Real database tap plugin",
        plugin_type=FlextPluginModels.PluginType.TAP,
    )


@pytest.fixture
def real_target_plugin() -> FlextPluginModels.Plugin:
    """Create REAL target plugin entity."""
    return FlextPluginModels.Plugin.create(
        name="target-warehouse",
        plugin_version="1.0.0",
        description="Real warehouse target plugin",
        plugin_type=FlextPluginModels.PluginType.TARGET,
    )


@pytest.fixture
def real_processor_plugin() -> FlextPluginModels.Plugin:
    """Create REAL processor plugin entity."""
    return FlextPluginModels.Plugin.create(
        name="processor-transform",
        plugin_version="1.0.0",
        description="Real transform processor plugin",
        plugin_type=FlextPluginModels.PluginType.PROCESSOR,
    )


# REAL Dependency fixtures
@pytest.fixture
def real_plugin_dependencies() -> dict[str, list[str]]:
    """REAL plugin dependency graph."""
    return {
        "tap_database": [],
        "processor_transform": ["tap_database"],
        "target_warehouse": ["processor_transform"],
    }


# Performance testing fixtures
@pytest.fixture
def performance_config() -> dict[str, t.GeneralValueType]:
    """Configuration for REAL plugin performance testing."""
    return {
        "max_load_time": 2.0,  # seconds for real plugins
        "max_memory_usage": 50,  # MB
        "max_cpu_usage": 25,  # percentage
        "test_iterations": 10,  # Reduced for real testing
    }


# PYTHON_VERSION_GUARD — Do not remove. Managed by scripts/maintenance/enforce_python_version.py
import sys as _sys

if _sys.version_info[:2] != (3, 13):
    _v = (
        f"{_sys.version_info.major}.{_sys.version_info.minor}.{_sys.version_info.micro}"
    )
    raise RuntimeError(
        f"\n{'=' * 72}\n"
        f"FATAL: Python {_v} detected — this project requires Python 3.13.\n"
        f"\n"
        f"The virtual environment was created with the WRONG Python interpreter.\n"
        f"\n"
        f"Fix:\n"
        f"  1. rm -rf .venv\n"
        f"  2. poetry env use python3.13\n"
        f"  3. poetry install\n"
        f"\n"
        f"Or use the workspace Makefile:\n"
        f"  make setup PROJECT=<project-name>\n"
        f"{'=' * 72}\n"
    )
del _sys
# PYTHON_VERSION_GUARD_END
