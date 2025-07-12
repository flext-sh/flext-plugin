"""Basic tests for flext-plugin functionality.

Tests following flext-core patterns and standards.
"""

from __future__ import annotations

import pytest
import pytest_asyncio

try:
    from flext_plugin.domain.exceptions import PluginError
except ImportError:
    # Define basic exception as fallback for tests
    class PluginError(Exception):
        pass


def test_flext_plugin_imports() -> None:
    """Test that flext-plugin core components can be imported."""
    try:
        from flext_plugin import PluginManager, PluginType

        assert PluginManager is not None
        assert PluginType is not None
    except ImportError:
        pytest.fail("flext-plugin core components not available")


def test_flext_core_dependencies() -> None:
    """Test that flext-plugin can use flext-core dependencies."""
    from flext_core import APIResponse, ServiceResult

    # Test ServiceResult works
    result = ServiceResult.success({"plugin": "test"})
    assert result.is_success is True
    assert result.data == {"plugin": "test"}

    # Test APIResponse works
    response = APIResponse(success=True, message="Plugin test")
    assert response.success is True
    assert response.message == "Plugin test"


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
    """Test flext-plugin integration patterns."""

    async def test_plugin_load_unload(self) -> None:
        """Test plugin load/unload functionality."""
        from flext_plugin import PluginManager

        manager = PluginManager()
        await manager.initialize()

        # Test load operation exists and handles missing plugins gracefully
        try:
            await manager.load_plugin("nonexistent-plugin")
        except (PluginError, ValueError, KeyError, FileNotFoundError) as e:
            # Should get PluginError for missing plugin
            assert "not found" in str(e).lower() or "plugin" in str(e).lower()

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
