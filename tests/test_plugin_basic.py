"""Basic tests for flext-infrastructure.plugins.flext-plugin functionality.

Tests following flext-core patterns and standards.
"""

from __future__ import annotations

import pytest


def test_flext_plugin_imports() -> None:
    """Test that flext-infrastructure.plugins.flext-plugin core components can be imported.

    This verifies that the core plugin components are available for import.
    """
    try:
        from flext_plugin import PluginManager, PluginType

        assert PluginManager is not None
        assert PluginType is not None
    except ImportError:
        pytest.fail(
            "flext-infrastructure.plugins.flext-plugin core components not available",
        )


def test_flext_core_dependencies() -> None:
    """Test that flext-infrastructure.plugins.flext-plugin can use flext-core dependencies.

    This verifies that flext-core types and patterns are accessible.
    """
    from flext_core import ServiceResult

    # Test ServiceResult works
    result = ServiceResult.ok({"test": "data"})
    assert result.is_success
    assert result.data == {"test": "data"}


def test_plugin_type_enum() -> None:
    """Test PluginType enum from flext-core."""
    from flext_core.domain.types import PluginType

    # Test standard plugin types
    assert PluginType.TAP.value == "tap"
    assert PluginType.TARGET.value == "target"
    assert PluginType.TRANSFORM.value == "transform"
    assert PluginType.UTILITY.value == "utility"


async def test_plugin_manager_basic() -> None:
    """Test PluginManager basic functionality."""
    from flext_plugin import PluginManager

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
        from flext_plugin import PluginManager

        manager = PluginManager()
        await manager.initialize()

        # Test load operation exists and handles missing plugins gracefully
        result = await manager.load_plugin("nonexistent-plugin")

        assert not result.is_success
        assert result.error is not None
        assert "not found" in result.error.lower()

    async def test_plugin_discovery(self) -> None:
        """Test plugin discovery functionality."""
        from flext_plugin import PluginManager

        manager = PluginManager()

        # Test discovery doesn't crash
        available = await manager.discover_plugins()
        assert isinstance(available, dict)

    def test_plugin_lifecycle(self) -> None:
        """Test basic plugin lifecycle operations."""
        from flext_plugin import PluginManager

        manager = PluginManager()

        # Test operations exist based on real API
        assert hasattr(manager, "load_plugin")
        assert hasattr(manager, "unload_plugin")
        assert hasattr(manager, "reload_plugin")
        assert hasattr(manager, "discover_plugins")
