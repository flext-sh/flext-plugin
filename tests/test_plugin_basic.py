"""Basic tests for flext-infrastructure.plugins.flext-plugin functionality.

Tests following flext-core patterns and standards.
"""

from __future__ import annotations

import pytest
from flext_core import FlextResult

from flext_plugin import FlextPluginManager as PluginManager
from flext_plugin.core.types import PluginType


def test_flext_plugin_imports() -> None:
    """Test that flext-plugin core components can be imported.

    This verifies that the core plugin components are available for import.
    """
    try:
        assert PluginManager is not None
        assert PluginType is not None
    except ImportError:
        pytest.fail(
            "flext-infrastructure.plugins.flext-plugin core components not available",
        )


def test_flext_core_dependencies() -> None:
    """Test that flext-plugin can use flext-core dependencies.

    This verifies that flext-core types and patterns are accessible.
    """
    # 🚨 ARCHITECTURAL COMPLIANCE: Using módulo raiz imports

    # Test FlextResult works
    result = FlextResult.ok({"test": "data"})
    assert result.is_success
    expected_data = {"test": "data"}
    if result.data != expected_data:
        raise AssertionError(f"Expected {expected_data}, got {result.data}")


def test_plugin_type_enum() -> None:
    """Test PluginType enum from flext_plugin."""

    # Test standard plugin types
    if PluginType.TAP.value != "tap":
        raise AssertionError(f"Expected {'tap'}, got {PluginType.TAP.value}")
    assert PluginType.TARGET.value == "target"
    if PluginType.TRANSFORM.value != "transform":
        raise AssertionError(
            f"Expected {'transform'}, got {PluginType.TRANSFORM.value}"
        )
    assert PluginType.UTILITY.value == "utility"


async def test_plugin_manager_basic() -> None:
    """Test PluginManager basic functionality."""

    manager = PluginManager()
    assert manager is not None

    # Test basic operations don't crash
    await manager.initialize()
    plugins = await manager.discover_plugins()
    assert isinstance(plugins, dict)


class TestFlextPluginIntegration:
    """Test flext-infrastructure.plugins.flext-plugin integration patterns."""

    async def test_plugin_load_unload(self) -> None:
        """Test plugin load/unload functionality."""

        manager = PluginManager()
        await manager.initialize()

        # Test load operation exists and handles missing plugins gracefully
        result = await manager.load_plugin("nonexistent-plugin")

        assert not result.success
        assert result.error is not None
        if "not found" not in result.error.lower():
            raise AssertionError(f"Expected {'not found'} in {result.error.lower()}")

    async def test_plugin_discovery(self) -> None:
        """Test plugin discovery functionality."""

        manager = PluginManager()

        # Test discovery doesn't crash
        available = await manager.discover_plugins()
        assert isinstance(available, dict)

    def test_plugin_lifecycle(self) -> None:
        """Test basic plugin lifecycle operations."""

        manager = PluginManager()

        # Test operations exist based on real API
        assert hasattr(manager, "load_plugin")
        assert hasattr(manager, "unload_plugin")
        assert hasattr(manager, "reload_plugin")
        assert hasattr(manager, "discover_plugins")
