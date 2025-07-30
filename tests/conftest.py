"""Test configuration for flext-plugin.

Provides pytest fixtures and configuration for testing plugin functionality
using flext-core patterns and real plugin management.
"""

from __future__ import annotations

import os
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Generator


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


# Plugin test configuration
@pytest.fixture
def plugin_test_config() -> dict[str, object]:
    """Plugin manager configuration for testing."""
    return {
        "plugin_directory": "test_plugins",
        "auto_discover": True,
        "hot_reload": False,
        "max_plugins": 100,
        "timeout": 30,
    }


@pytest.fixture
def test_plugin_directory() -> Generator[Path]:
    """Temporary directory for test plugins."""
    with tempfile.TemporaryDirectory() as temp_dir:
        plugin_dir = Path(temp_dir) / "test_plugins"
        plugin_dir.mkdir()
        yield plugin_dir


@pytest.fixture
def sample_plugin_data() -> dict[str, object]:
    """Sample plugin data for testing."""
    return {
        "plugins": [
            {
                "name": "test-plugin-1",
                "version": "0.9.0",
                "description": "Test plugin for unit testing",
                "type": "extractor",
                "module": "test_plugin_1",
                "class": "TestPlugin1",
                "config": {"param1": "value1"},
                "dependencies": [],
                "enabled": True,
            },
            {
                "name": "test-plugin-2",
                "version": "0.9.0",
                "description": "Another test plugin",
                "type": "loader",
                "module": "test_plugin_2",
                "class": "TestPlugin2",
                "config": {"param2": "value2"},
                "dependencies": ["test-plugin-1"],
                "enabled": False,
            },
        ],
    }


# Plugin manager fixtures
@pytest.fixture
async def plugin_manager(
    plugin_test_config: dict[str, object],
    test_plugin_directory: Path,
) -> object:
    """Plugin manager for testing."""
    from flext_plugin import FlextPluginManager

    # Update config with test directory
    config = plugin_test_config.copy()
    config["plugin_directory"] = str(test_plugin_directory)

    return FlextPluginManager()

    # Note: No cleanup needed - PluginManager handles its own lifecycle


@pytest.fixture
def mock_plugin_manifest() -> dict[str, object]:
    """Mock plugin manifest for testing."""
    return {
        "name": "mock-plugin",
        "version": "0.9.0",
        "description": "Mock plugin for testing",
        "author": "Test Author",
        "license": "MIT",
        "type": "extractor",
        "entry_point": "mock_plugin:MockPlugin",
        "config_schema": {
            "type": "object",
            "properties": {
                "host": {"type": "string"},
                "port": {"type": "integer", "default": 5432},
            },
            "required": ["host"],
        },
        "dependencies": [],
        "minimum_flext_version": "0.9.0",
    }


# Plugin discovery fixtures
@pytest.fixture
def plugin_discovery_paths() -> list[str]:
    """Paths for plugin discovery testing."""
    return [
        "test_plugins",
        "additional_plugins",
        "/opt/flext/plugins",
    ]


# Plugin lifecycle fixtures
@pytest.fixture
def plugin_lifecycle_states() -> list[str]:
    """Plugin lifecycle states for testing."""
    return [
        "unloaded",
        "loading",
        "loaded",
        "starting",
        "running",
        "stopping",
        "stopped",
        "error",
    ]


# Plugin configuration fixtures
@pytest.fixture
def plugin_config_samples(tmp_path: Path) -> dict[str, dict[str, object]]:
    """Sample plugin configurations."""
    return {
        "database_extractor": {
            "host": "localhost",
            "port": 5432,
            "database": "test_db",
            "username": "test_user",
            "password": "test_pass",
            "table": "test_table",
        },
        "file_loader": {
            "file_path": str(tmp_path / "test_file.csv"),
            "format": "csv",
            "delimiter": ",",
            "encoding": "utf-8",
        },
        "api_processor": {
            "endpoint": "https://api.test.com/process",
            "timeout": 30,
            "retry_count": 3,
            "headers": {"Content-Type": "application/json"},
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


# Error handling fixtures
@pytest.fixture
def plugin_load_error() -> Exception:
    """Plugin load error for testing."""

    # Create a mock exception since module doesn't exist
    class PluginLoadError(Exception):
        pass

    return PluginLoadError("Test plugin load failed")


@pytest.fixture
def plugin_validation_error() -> Exception:
    """Plugin validation error for testing."""

    # Create a mock exception since module doesn't exist
    class PluginValidationError(Exception):
        pass

    return PluginValidationError("Test plugin validation failed")


# Mock plugin implementations
@pytest.fixture
def mock_extractor_plugin() -> object:
    """Mock extractor plugin for testing."""
    # Create a mock base class since interfaces module doesn't exist

    class ExtractorPlugin(ABC):
        @abstractmethod
        async def extract(self) -> list[dict[str, object]]:
            pass

    class MockExtractorPlugin(ExtractorPlugin):
        def __init__(self, config: dict[str, object]) -> None:
            self.config = config
            self.name = "mock-extractor"

        async def extract(self) -> list[dict[str, object]]:
            return [{"id": 1, "data": "test"}]

        async def validate_config(self) -> bool:
            return True

    return MockExtractorPlugin


@pytest.fixture
def mock_loader_plugin() -> object:
    """Mock loader plugin for testing."""
    # Create a mock base class since interfaces module doesn't exist

    class LoaderPlugin(ABC):
        @abstractmethod
        async def load(self, data: list[dict[str, object]]) -> bool:
            pass

    class MockLoaderPlugin(LoaderPlugin):
        def __init__(self, config: dict[str, object]) -> None:
            self.config = config
            self.name = "mock-loader"

        async def load(self, data: list[dict[str, object]]) -> bool:
            return True

        async def validate_config(self) -> bool:
            return True

    return MockLoaderPlugin


# Plugin dependency fixtures
@pytest.fixture
def plugin_dependency_graph() -> dict[str, list[str]]:
    """Plugin dependency graph for testing."""
    return {
        "plugin-a": [],
        "plugin-b": ["plugin-a"],
        "plugin-c": ["plugin-a", "plugin-b"],
        "plugin-d": ["plugin-c"],
        "plugin-e": ["plugin-d"],
    }


# Performance testing fixtures
@pytest.fixture
def plugin_performance_config() -> dict[str, object]:
    """Configuration for plugin performance testing."""
    return {
        "max_load_time": 5.0,  # seconds
        "max_memory_usage": 100,  # MB
        "max_cpu_usage": 50,  # percentage
        "test_iterations": 100,
    }
