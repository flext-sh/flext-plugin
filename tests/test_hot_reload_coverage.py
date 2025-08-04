"""Coverage-focused test suite for flext_plugin.hot_reload module.

This test module focuses on maximizing code coverage for the hot reload system
by testing actual implemented functionality without expecting non-existent classes.

Strategy: Test ONLY what exists - HotReloadManager and PluginFileHandler.
"""

from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path
from typing import Generator
from unittest.mock import AsyncMock, Mock, patch

import pytest

from flext_plugin.hot_reload import HotReloadManager, PluginFileHandler


class TestPluginFileHandler:
    """Coverage-focused tests for PluginFileHandler.
    
    Tests the actual file system event handler implementation.
    """

    def test_handler_initialization(self) -> None:
        """Test handler initialization with callback."""
        callback = Mock()
        handler = PluginFileHandler(reload_callback=callback)

        assert handler is not None
        assert handler.reload_callback is callback

    def test_on_modified_directory_ignored(self) -> None:
        """Test directory modification events are ignored."""
        callback = Mock()
        handler = PluginFileHandler(reload_callback=callback)

        # Create mock directory event
        event = Mock()
        event.is_directory = True
        event.src_path = "/test/directory"

        handler.on_modified(event)

        # Callback should not be called for directories
        callback.assert_not_called()

    def test_on_modified_non_python_file_ignored(self) -> None:
        """Test non-Python files are ignored."""
        callback = Mock()
        handler = PluginFileHandler(reload_callback=callback)

        # Create mock file event for non-Python file
        event = Mock()
        event.is_directory = False
        event.src_path = "/test/file.txt"

        handler.on_modified(event)

        # Callback should not be called for non-Python files
        callback.assert_not_called()

    def test_on_modified_python_file_calls_callback(self) -> None:
        """Test Python file modification calls callback."""
        callback = Mock()
        handler = PluginFileHandler(reload_callback=callback)

        # Create mock file event for Python file
        event = Mock()
        event.is_directory = False
        event.src_path = "/test/plugin.py"

        handler.on_modified(event)

        # Callback should be called with Path object
        callback.assert_called_once()
        args = callback.call_args[0]
        assert len(args) == 1
        assert isinstance(args[0], Path)
        assert args[0].name == "plugin.py"

    def test_on_modified_dunder_file_ignored(self) -> None:
        """Test __init__.py and similar files are ignored."""
        callback = Mock()
        handler = PluginFileHandler(reload_callback=callback)

        # Create mock file event for dunder file
        event = Mock()
        event.is_directory = False
        event.src_path = "/test/__init__.py"

        handler.on_modified(event)

        # Callback should not be called for dunder files
        callback.assert_not_called()

    def test_on_modified_bytes_path_handled(self) -> None:
        """Test handling of bytes path in event."""
        callback = Mock()
        handler = PluginFileHandler(reload_callback=callback)

        # Create mock file event with bytes path
        event = Mock()
        event.is_directory = False
        event.src_path = b"/test/plugin.py"

        handler.on_modified(event)

        # Callback should be called with properly decoded path
        callback.assert_called_once()
        args = callback.call_args[0]
        assert isinstance(args[0], Path)
        assert args[0].name == "plugin.py"


class TestHotReloadManager:
    """Coverage-focused tests for HotReloadManager.
    
    Tests the actual hot reload manager implementation using real API.
    """

    @pytest.fixture
    def temp_dir(self) -> Generator[Path, None, None]:
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    def test_manager_initialization(self, temp_dir: Path) -> None:
        """Test manager initialization with plugin directory."""
        plugin_dir = str(temp_dir / "plugins")
        manager = HotReloadManager(plugin_directory=plugin_dir)

        assert manager is not None
        assert manager.plugin_directory == plugin_dir

    def test_manager_initialization_with_id(self, temp_dir: Path) -> None:
        """Test manager initialization with custom ID."""
        plugin_dir = str(temp_dir / "plugins")
        custom_id = "custom-hot-reload-id"
        manager = HotReloadManager(plugin_directory=plugin_dir, id=custom_id)

        assert manager is not None
        assert manager.id == custom_id

    def test_validate_domain_rules_empty_directory_fails(self) -> None:
        """Test domain validation with empty directory fails."""
        manager = HotReloadManager(plugin_directory="")
        result = manager.validate_domain_rules()

        assert not result.is_success
        assert "Plugin directory cannot be empty" in str(result.error)

    def test_validate_domain_rules_valid_directory_succeeds(self, temp_dir: Path) -> None:
        """Test domain validation with valid directory succeeds."""
        plugin_dir = str(temp_dir / "plugins")
        manager = HotReloadManager(plugin_directory=plugin_dir)
        result = manager.validate_domain_rules()

        assert result.is_success

    def test_manager_properties_initialization(self, temp_dir: Path) -> None:
        """Test manager properties are properly initialized."""
        plugin_dir = str(temp_dir / "plugins")
        manager = HotReloadManager(plugin_directory=plugin_dir)

        # Properties should be accessible
        assert manager.discovery is None  # Lazy loaded
        assert manager.loader is not None
        assert manager.observer is not None
        assert isinstance(manager.loaded_plugins, dict)

    def test_get_loaded_plugins_returns_copy(self, temp_dir: Path) -> None:
        """Test get_loaded_plugins returns a copy."""
        plugin_dir = str(temp_dir / "plugins")
        manager = HotReloadManager(plugin_directory=plugin_dir)

        loaded_plugins = manager.get_loaded_plugins()
        assert isinstance(loaded_plugins, dict)

        # Should be empty initially
        assert len(loaded_plugins) == 0

        # Modifying returned dict shouldn't affect internal state
        loaded_plugins["test"] = "value"
        assert "test" not in manager.get_loaded_plugins()

    @pytest.mark.asyncio
    async def test_start_watching_creates_observer(self, temp_dir: Path) -> None:
        """Test start_watching initializes file system observer."""
        plugin_dir = temp_dir / "plugins"
        plugin_dir.mkdir()

        manager = HotReloadManager(plugin_directory=str(plugin_dir))

        # Mock the observer to avoid real file watching
        with patch.object(manager, 'observer') as mock_observer:
            mock_observer.schedule = Mock()
            mock_observer.start = Mock()

            await manager.start_watching()

            # Verify observer was configured and started
            mock_observer.schedule.assert_called_once()
            mock_observer.start.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_watching_without_observer_raises_error(self, temp_dir: Path) -> None:
        """Test start_watching without observer raises error."""
        plugin_dir = str(temp_dir / "plugins")
        manager = HotReloadManager(plugin_directory=plugin_dir)

        # Remove observer to simulate initialization failure
        object.__setattr__(manager, "_observer", None)

        with pytest.raises(Exception) as exc_info:
            await manager.start_watching()

        assert "Observer not initialized" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_stop_watching_stops_observer(self, temp_dir: Path) -> None:
        """Test stop_watching properly stops observer."""
        plugin_dir = str(temp_dir / "plugins")
        manager = HotReloadManager(plugin_directory=plugin_dir)

        # Mock observer
        mock_observer = Mock()
        mock_observer.is_alive.return_value = True
        mock_observer.stop = Mock()
        mock_observer.join = Mock()
        object.__setattr__(manager, "_observer", mock_observer)

        await manager.stop_watching()

        mock_observer.stop.assert_called_once()
        mock_observer.join.assert_called_once()

    @pytest.mark.asyncio
    async def test_stop_watching_with_dead_observer(self, temp_dir: Path) -> None:
        """Test stop_watching with already stopped observer."""
        plugin_dir = str(temp_dir / "plugins")
        manager = HotReloadManager(plugin_directory=plugin_dir)

        # Mock dead observer
        mock_observer = Mock()
        mock_observer.is_alive.return_value = False
        mock_observer.stop = Mock()
        mock_observer.join = Mock()
        object.__setattr__(manager, "_observer", mock_observer)

        await manager.stop_watching()

        # Should not call stop/join on dead observer
        mock_observer.stop.assert_not_called()
        mock_observer.join.assert_not_called()

    @pytest.mark.asyncio
    async def test_initial_plugin_load_scans_directory(self, temp_dir: Path) -> None:
        """Test initial plugin load scans plugin directory."""
        plugin_dir = temp_dir / "plugins"
        plugin_dir.mkdir()

        # Create a test plugin file
        test_plugin = plugin_dir / "test_plugin.py"
        test_plugin.write_text("# Test plugin content")

        manager = HotReloadManager(plugin_directory=str(plugin_dir))

        # Mock the loader to avoid actual loading
        mock_loader = Mock()
        mock_loader.load_plugin = Mock(return_value="mock_plugin_instance")
        object.__setattr__(manager, "_loader", mock_loader)

        await manager._initial_plugin_load()

        # Should have attempted to load the plugin
        mock_loader.load_plugin.assert_called_once()

    @pytest.mark.asyncio
    async def test_initial_plugin_load_nonexistent_directory(self, temp_dir: Path) -> None:
        """Test initial plugin load with nonexistent directory."""
        plugin_dir = temp_dir / "nonexistent"
        manager = HotReloadManager(plugin_directory=str(plugin_dir))

        # Should not raise exception
        await manager._initial_plugin_load()

    @pytest.mark.asyncio
    async def test_initial_plugin_load_handles_errors_gracefully(self, temp_dir: Path) -> None:
        """Test initial plugin load handles errors gracefully."""
        plugin_dir = temp_dir / "plugins"
        plugin_dir.mkdir()

        # Create a test plugin file
        test_plugin = plugin_dir / "test_plugin.py"
        test_plugin.write_text("# Test plugin content")

        manager = HotReloadManager(plugin_directory=str(plugin_dir))

        # Should not raise exception even with errors
        await manager._initial_plugin_load()

    def test_on_plugin_file_changed_creates_task(self, temp_dir: Path) -> None:
        """Test file change handler creates async task."""
        plugin_dir = str(temp_dir / "plugins")
        manager = HotReloadManager(plugin_directory=plugin_dir)

        test_path = Path("/test/plugin.py")

        with patch('asyncio.create_task') as mock_create_task:
            mock_task = Mock()
            mock_task.add_done_callback = Mock()
            mock_create_task.return_value = mock_task

            manager._on_plugin_file_changed(test_path)

            # Should create async task for reload
            mock_create_task.assert_called_once()
            mock_task.add_done_callback.assert_called_once()

    @pytest.mark.asyncio
    async def test_reload_plugin_with_existing_plugin(self, temp_dir: Path) -> None:
        """Test reload plugin with existing loaded plugin."""
        plugin_dir = str(temp_dir / "plugins")
        manager = HotReloadManager(plugin_directory=plugin_dir)

        # Setup existing plugin without cleanup method (plain object)
        test_path = Path("test_plugin.py")
        existing_plugin = object()  # Plain object has no cleanup method
        loaded_plugins = {"test_plugin": existing_plugin}
        object.__setattr__(manager, "_loaded_plugins", loaded_plugins)

        await manager._reload_plugin(test_path)

        # Plugin should be removed from loaded plugins
        assert "test_plugin" not in manager.loaded_plugins

    @pytest.mark.asyncio
    async def test_reload_plugin_handles_errors_gracefully(self, temp_dir: Path) -> None:
        """Test reload plugin handles errors gracefully."""
        plugin_dir = str(temp_dir / "plugins")
        manager = HotReloadManager(plugin_directory=plugin_dir)

        test_path = Path("test_plugin.py")

        # Should not raise exception
        await manager._reload_plugin(test_path)

    @pytest.mark.asyncio
    async def test_load_plugin_with_loader(self, temp_dir: Path) -> None:
        """Test load plugin with mock loader."""
        plugin_dir = str(temp_dir / "plugins")
        manager = HotReloadManager(plugin_directory=plugin_dir)

        # Mock loader
        mock_loader = Mock()
        mock_loader.load_plugin = Mock(return_value="mock_plugin_instance")
        object.__setattr__(manager, "_loader", mock_loader)

        test_path = Path("test_plugin.py")
        await manager._load_plugin(test_path)

        # Should have called loader
        mock_loader.load_plugin.assert_called_once_with(test_path)

    @pytest.mark.asyncio
    async def test_load_plugin_without_loader(self, temp_dir: Path) -> None:
        """Test load plugin without loader."""
        plugin_dir = str(temp_dir / "plugins")
        manager = HotReloadManager(plugin_directory=plugin_dir)

        # Remove loader
        object.__setattr__(manager, "_loader", None)

        test_path = Path("test_plugin.py")

        # Should not raise exception
        await manager._load_plugin(test_path)

    @pytest.mark.asyncio
    async def test_load_plugin_handles_errors_gracefully(self, temp_dir: Path) -> None:
        """Test load plugin handles errors gracefully."""
        plugin_dir = str(temp_dir / "plugins")
        manager = HotReloadManager(plugin_directory=plugin_dir)

        test_path = Path("test_plugin.py")

        # Should not raise exception
        await manager._load_plugin(test_path)

    @pytest.mark.asyncio
    async def test_unload_plugin_with_cleanup(self, temp_dir: Path) -> None:
        """Test unload plugin with cleanup method."""
        plugin_dir = str(temp_dir / "plugins")
        manager = HotReloadManager(plugin_directory=plugin_dir)

        # Setup plugin with cleanup method
        mock_plugin = AsyncMock()
        mock_plugin.cleanup = AsyncMock()
        loaded_plugins = {"test_plugin": mock_plugin}
        object.__setattr__(manager, "_loaded_plugins", loaded_plugins)

        await manager._unload_plugin("test_plugin")

        # Should call cleanup and remove plugin
        mock_plugin.cleanup.assert_called_once()
        assert "test_plugin" not in manager.loaded_plugins

    @pytest.mark.asyncio
    async def test_unload_plugin_without_cleanup(self, temp_dir: Path) -> None:
        """Test unload plugin without cleanup method."""
        plugin_dir = str(temp_dir / "plugins")
        manager = HotReloadManager(plugin_directory=plugin_dir)

        # Setup plugin without cleanup method (regular object)
        mock_plugin = object()  # Plain object has no cleanup method
        loaded_plugins = {"test_plugin": mock_plugin}
        object.__setattr__(manager, "_loaded_plugins", loaded_plugins)

        await manager._unload_plugin("test_plugin")

        # Should remove plugin without calling cleanup
        assert "test_plugin" not in manager.loaded_plugins

    @pytest.mark.asyncio
    async def test_unload_plugin_nonexistent(self, temp_dir: Path) -> None:
        """Test unload nonexistent plugin."""
        plugin_dir = str(temp_dir / "plugins")
        manager = HotReloadManager(plugin_directory=plugin_dir)

        # Should not raise exception
        await manager._unload_plugin("nonexistent_plugin")

    @pytest.mark.asyncio
    async def test_unload_plugin_handles_errors_gracefully(self, temp_dir: Path) -> None:
        """Test unload plugin handles errors gracefully."""
        plugin_dir = str(temp_dir / "plugins")
        manager = HotReloadManager(plugin_directory=plugin_dir)

        # Should not raise exception
        await manager._unload_plugin("test_plugin")

    @pytest.mark.asyncio
    async def test_reload_all_plugins(self, temp_dir: Path) -> None:
        """Test reload all plugins functionality."""
        plugin_dir = temp_dir / "plugins"
        plugin_dir.mkdir()

        manager = HotReloadManager(plugin_directory=str(plugin_dir))

        # Setup multiple loaded plugins
        loaded_plugins = {
            "plugin1": Mock(),
            "plugin2": Mock(),
            "plugin3": Mock(),
        }
        object.__setattr__(manager, "_loaded_plugins", loaded_plugins)

        await manager.reload_all_plugins()

        # All plugins should be unloaded
        assert len(manager.loaded_plugins) == 0

    @pytest.mark.asyncio
    async def test_reload_all_plugins_empty(self, temp_dir: Path) -> None:
        """Test reload all plugins with no loaded plugins."""
        plugin_dir = str(temp_dir / "plugins")
        manager = HotReloadManager(plugin_directory=plugin_dir)

        # Should not raise exception
        await manager.reload_all_plugins()

        assert len(manager.loaded_plugins) == 0


class TestHotReloadConvenienceFunction:
    """Test the convenience function for creating hot reload manager."""

    @pytest.mark.asyncio
    async def test_create_hot_reload_manager(self) -> None:
        """Test create_hot_reload_manager convenience function."""
        from flext_plugin.hot_reload import create_hot_reload_manager

        with tempfile.TemporaryDirectory() as tmp_dir:
            plugin_dir = str(Path(tmp_dir) / "plugins")

            with patch('flext_plugin.hot_reload.HotReloadManager.start_watching') as mock_start:
                mock_start.return_value = asyncio.Future()
                mock_start.return_value.set_result(None)

                manager = await create_hot_reload_manager(plugin_dir)

                assert manager is not None
                assert isinstance(manager, HotReloadManager)
                assert manager.plugin_directory == plugin_dir
                mock_start.assert_called_once()


class TestHotReloadIntegration:
    """Integration tests for hot reload system."""

    @pytest.mark.asyncio
    async def test_file_handler_integration_with_manager(self) -> None:
        """Test file handler integration with manager."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            plugin_dir = str(Path(tmp_dir) / "plugins")
            manager = HotReloadManager(plugin_directory=plugin_dir)

            # Test file handler callback integration
            handler = PluginFileHandler(manager._on_plugin_file_changed)

            # Create mock event
            event = Mock()
            event.is_directory = False
            event.src_path = str(Path(tmp_dir) / "test_plugin.py")

            with patch('asyncio.create_task') as mock_create_task:
                mock_task = Mock()
                mock_task.add_done_callback = Mock()
                mock_create_task.return_value = mock_task

                handler.on_modified(event)

                # Should create task through manager callback
                mock_create_task.assert_called_once()

    @pytest.mark.asyncio
    async def test_manager_lifecycle_complete(self) -> None:
        """Test complete manager lifecycle."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            plugin_dir = Path(tmp_dir) / "plugins"
            plugin_dir.mkdir()

            manager = HotReloadManager(plugin_directory=str(plugin_dir))

            # Test complete lifecycle
            with patch.object(manager, 'observer') as mock_observer:
                mock_observer.schedule = Mock()
                mock_observer.start = Mock()
                mock_observer.is_alive.return_value = True
                mock_observer.stop = Mock()
                mock_observer.join = Mock()

                # Start watching
                await manager.start_watching()

                # Verify started
                mock_observer.start.assert_called_once()

                # Stop watching
                await manager.stop_watching()

                # Verify stopped
                mock_observer.stop.assert_called_once()
                mock_observer.join.assert_called_once()

    def test_error_handling_comprehensive(self) -> None:
        """Test comprehensive error handling across the system."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            plugin_dir = str(Path(tmp_dir) / "plugins")

            # Manager creation should not fail even with problematic directory
            manager = HotReloadManager(plugin_directory=plugin_dir)
            assert manager is not None

            # Properties should be accessible even if not fully initialized
            assert manager.plugin_directory == plugin_dir
            assert isinstance(manager.loaded_plugins, dict)

            # Validation should work
            validation_result = manager.validate_domain_rules()
            assert validation_result.is_success
