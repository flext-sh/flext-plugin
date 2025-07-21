"""Tests for flext_plugin.hot_reload package.

Professional tests for hot reload functionality using real implementations.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, Mock, patch

import pytest

from flext_plugin.hot_reload import (
    HotReloadManager,
    PluginState,
    PluginWatcher,
    ReloadEvent,
    RollbackManager,
    StateManager,
)

if TYPE_CHECKING:
    from collections.abc import Generator


class TestPluginState:
    """Test PluginState functionality."""

    def test_plugin_state_creation(self) -> None:
        """Test creating plugin state."""
        state = PluginState(
            plugin_id="test-plugin",
            plugin_version="1.0.0",
            state_data={"key": "value"},
        )

        assert state.plugin_id == "test-plugin"
        assert state.plugin_version == "1.0.0"
        assert state.state_data["key"] == "value"

    def test_plugin_state_default_values(self) -> None:
        """Test plugin state with default values."""
        state = PluginState(
            plugin_id="minimal-plugin",
            plugin_version="0.1.0",
        )

        assert state.state_data == {}
        assert state.metadata == {}
        assert state.saved_at is not None


class TestReloadEvent:
    """Test ReloadEvent functionality."""

    def test_reload_event_creation(self) -> None:
        """Test creating reload event."""
        event = ReloadEvent(
            event_type="file_changed",
            plugin_id="test-plugin",
            plugin_path=Path("/test/plugin.py"),
        )

        assert event.event_type == "file_changed"
        assert event.plugin_id == "test-plugin"
        assert event.plugin_path == Path("/test/plugin.py")
        assert not event.success  # Default value
        assert event.error is None


class TestPluginWatcher:
    """Test PluginWatcher functionality."""

    @pytest.fixture
    def temp_dir(self) -> Generator[Path]:
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    @pytest.fixture
    def watcher(self, temp_dir: Path) -> PluginWatcher:
        """Create plugin watcher for testing."""
        watch_dir = temp_dir / "plugins"
        watch_dir.mkdir(exist_ok=True)
        return PluginWatcher(watch_directories=[watch_dir])

    def test_watcher_initialization(
        self,
        watcher: PluginWatcher,
        temp_dir: Path,
    ) -> None:
        """Test plugin watcher initialization."""
        expected_dir = temp_dir / "plugins"
        assert expected_dir in watcher.watch_directories

    def test_watcher_properties(self, watcher: PluginWatcher) -> None:
        """Test watcher properties."""
        assert hasattr(watcher, "watch_directories")
        assert isinstance(watcher.watch_directories, list)

    def test_get_watched_files(self, watcher: PluginWatcher) -> None:
        """Test getting watched files."""
        watched_files = watcher.get_watched_files()
        assert isinstance(watched_files, list)


class TestStateManager:
    """Test StateManager functionality."""

    @pytest.fixture
    def temp_dir(self) -> Generator[Path]:
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    @pytest.fixture
    def state_manager(self, temp_dir: Path) -> StateManager:
        """Create state manager for testing."""
        return StateManager(state_directory=temp_dir / "states")

    def test_state_manager_initialization(
        self,
        state_manager: StateManager,
        temp_dir: Path,
    ) -> None:
        """Test state manager initialization."""
        assert state_manager.state_directory == temp_dir / "states"
        assert state_manager.enable_persistence is True

    async def test_save_plugin_state_without_plugin(
        self,
        state_manager: StateManager,
    ) -> None:
        """Test saving plugin state with mock plugin."""
        # Create a mock plugin that has the required attributes
        mock_plugin = Mock()
        mock_plugin.metadata.name = "test-plugin"
        mock_plugin.metadata.version = "1.0.0"
        mock_plugin.metadata.plugin_type.value = "tap"
        mock_plugin.metadata.capabilities = ["read", "extract"]
        mock_plugin.get_state = AsyncMock(return_value={"key": "value"})

        state = await state_manager.save_plugin_state(mock_plugin)

        assert state.plugin_id == "test-plugin"

    async def test_create_snapshot(self, state_manager: StateManager) -> None:
        """Test creating state snapshot."""
        snapshot_id = await state_manager.create_snapshot("Test snapshot")

        assert snapshot_id is not None
        assert isinstance(snapshot_id, str)

    def test_list_snapshots(self, state_manager: StateManager) -> None:
        """Test listing snapshots."""
        snapshots = state_manager.list_snapshots()
        assert isinstance(snapshots, list)


class TestRollbackManager:
    """Test RollbackManager functionality."""

    @pytest.fixture
    def temp_dir(self) -> Generator[Path]:
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    @pytest.fixture
    def state_manager(self, temp_dir: Path) -> StateManager:
        """Create real state manager for testing."""
        return StateManager(state_directory=temp_dir / "rollback_states")

    @pytest.fixture
    def rollback_manager(self, state_manager: StateManager) -> RollbackManager:
        """Create rollback manager for testing."""
        return RollbackManager(state_manager=state_manager)

    def test_rollback_manager_initialization(
        self,
        rollback_manager: RollbackManager,
    ) -> None:
        """Test rollback manager initialization."""
        assert hasattr(rollback_manager, "state_manager")

    async def test_create_rollback_point(
        self,
        rollback_manager: RollbackManager,
    ) -> None:
        """Test creating rollback point."""
        # Create a mock plugin
        mock_plugin = Mock()
        mock_plugin.metadata = Mock()
        mock_plugin.metadata.name = "test-plugin"

        rollback_id = await rollback_manager.create_rollback_point(
            mock_plugin,
            "Test rollback point",
        )

        assert rollback_id is not None
        assert isinstance(rollback_id, str)

    def test_get_rollback_history(self, rollback_manager: RollbackManager) -> None:
        """Test getting rollback history."""
        # This is a synchronous method, not async
        history = rollback_manager.get_rollback_history("test-plugin")
        # history can be None if no history exists
        assert history is None or hasattr(history, "plugin_id")


class TestHotReloadManager:
    """Test HotReloadManager functionality."""

    @pytest.fixture
    def temp_dir(self) -> Generator[Path]:
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    @pytest.fixture
    def mock_plugin_manager(self) -> Mock:
        """Create mock plugin manager."""
        return Mock()

    @pytest.fixture
    def hot_reload_manager(
        self,
        mock_plugin_manager: Mock,
        temp_dir: Path,
    ) -> HotReloadManager:
        """Create hot reload manager for testing."""
        return HotReloadManager(
            plugin_manager=mock_plugin_manager,
            watch_directories=[temp_dir / "plugins"],
            state_backup_dir=temp_dir / "backup",
        )

    def test_manager_initialization(
        self,
        hot_reload_manager: HotReloadManager,
        temp_dir: Path,
    ) -> None:
        """Test hot reload manager initialization."""
        assert hot_reload_manager is not None
        assert hasattr(hot_reload_manager, "plugin_manager")
        assert hasattr(hot_reload_manager, "state_manager")
        assert hasattr(hot_reload_manager, "rollback_manager")
        assert hasattr(hot_reload_manager, "watcher")

    async def test_watching_lifecycle(
        self,
        hot_reload_manager: HotReloadManager,
    ) -> None:
        """Test starting and stopping watching."""
        # Should be able to start and stop watching without errors
        await hot_reload_manager.start_watching()
        await hot_reload_manager.stop_watching()

    async def test_reload_plugin(self, hot_reload_manager: HotReloadManager) -> None:
        """Test reloading specific plugin."""
        plugin_id = "test-plugin"

        # Mock the plugin manager's reload method using patch
        with patch.object(
            hot_reload_manager.plugin_manager,
            "reload_plugin",
            new_callable=AsyncMock,
        ) as mock_reload:
            mock_reload.return_value = True
            result = await hot_reload_manager.reload_plugin(plugin_id)
            assert isinstance(result, ReloadEvent)

    async def test_handle_plugin_change(
        self,
        hot_reload_manager: HotReloadManager,
    ) -> None:
        """Test handling plugin change event."""
        # Create a proper WatchEvent instead of Path
        from datetime import UTC, datetime

        from flext_plugin.hot_reload.watcher import WatchEvent, WatchEventType

        watch_event = WatchEvent(
            event_type=WatchEventType.MODIFIED,
            path=Path("/test/plugins/test_plugin.py"),
            timestamp=datetime.now(UTC),
        )

        # This method returns None
        await hot_reload_manager._handle_plugin_change(watch_event)
        # Test passes if no exception is raised

    def test_hot_reload_manager_properties(
        self,
        hot_reload_manager: HotReloadManager,
    ) -> None:
        """Test hot reload manager properties."""
        # Test basic properties exist
        assert hasattr(hot_reload_manager, "plugin_manager")
        assert hasattr(hot_reload_manager, "state_manager")
        assert hasattr(hot_reload_manager, "rollback_manager")
        assert hasattr(hot_reload_manager, "watcher")

    async def test_error_handling_graceful_failures(
        self,
        hot_reload_manager: HotReloadManager,
    ) -> None:
        """Test error handling with graceful failures."""
        plugin_id = "non-existent-plugin"

        # Mock plugin manager to raise exception using patch
        with patch.object(
            hot_reload_manager.plugin_manager,
            "reload_plugin",
            new_callable=AsyncMock,
        ) as mock_reload:
            mock_reload.side_effect = Exception("Plugin not found")

            # Should handle non-existent plugin gracefully
            result = await hot_reload_manager.reload_plugin(plugin_id)

            # Should return a ReloadEvent with error information
            assert isinstance(result, ReloadEvent)
            assert not result.success
            assert result.error is not None
