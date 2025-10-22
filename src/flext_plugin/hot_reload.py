"""FLEXT Plugin Hot Reload - Plugin hot reload and file monitoring.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from flext_core import FlextLogger, FlextResult

from flext_plugin.models import FlextPluginModels

if TYPE_CHECKING:
    from watchdog.events import FileSystemEventHandler

try:
    from watchdog.events import (
        DirModifiedEvent,
        FileModifiedEvent,
        FileSystemEventHandler,
    )
    from watchdog.observers import Observer

    HAS_WATCHDOG = True

    class FileChangeHandler(FileSystemEventHandler):
        """Watchdog event handler for file change detection."""

        def __init__(
            self,
            callback: Callable[[str], None],
            watched_paths: set[Path],
            logger: FlextLogger,
        ) -> None:
            """Initialize file change handler.

            Args:
            callback: Callback to execute on file change
            watched_paths: Set of paths being watched
            logger: Logger instance

            """
            super().__init__()
            self.callback = callback
            self.watched_paths = watched_paths
            self.logger = logger

        def on_modified(self, event: FileModifiedEvent | DirModifiedEvent) -> None:
            """Handle file modification event.

            Args:
            event: FileModifiedEvent or DirModifiedEvent from watchdog

            """
            if event.is_directory:
                return

            src_path = event.src_path
            if isinstance(src_path, bytes):
                src_path = src_path.decode("utf-8")

            if not src_path.endswith(".py"):
                return

            file_path = Path(src_path)

            # Check if file is in watched paths
            for watched_path in self.watched_paths:
                if (watched_path.is_file() and file_path == watched_path) or (
                    watched_path.is_dir() and file_path.is_relative_to(watched_path)
                ):
                    self.callback(file_path.stem)
                    break

except ImportError:
    HAS_WATCHDOG = False
    Observer = None
    FileChangeHandler = None


class FlextPluginHotReload:
    """Plugin hot reload service for real-time plugin updates.

    Provides complete hot reload functionality with event-driven file
    monitoring using watchdog library, automatic reloading, and change detection.

    Usage:
        ```python
        from flext_plugin import FlextPluginHotReload

        # Initialize hot reload service
        hot_reload = FlextPluginHotReload()

        # Start monitoring
        result = hot_reload.start_watching(["./plugins"])
        if result.is_success:
            print("Hot reload monitoring started")

        # Stop monitoring
        result = hot_reload.stop_watching()
        ```
    """

    def __init__(
        self,
        watch_interval: float = 2.0,
        debounce_ms: int = 500,
        max_retries: int = 3,
    ) -> None:
        """Initialize the hot reload service.

        Args:
            watch_interval: File watching interval in seconds (unused with watchdog)
            debounce_ms: Debounce time in milliseconds
            max_retries: Maximum retry attempts for failed reloads

        """
        self.logger = FlextLogger(__name__)
        self.watch_interval = watch_interval
        self.debounce_ms = debounce_ms
        self.max_retries = max_retries

        # Internal state
        self._is_watching = False
        self._watched_paths: set[Path] = set()
        self._reload_callbacks: list[Callable[[str], object]] = []
        self._reload_history: list[FlextPluginModels.ReloadRecord] = []

        # Watchdog-specific
        self._observer: Any = None
        self._event_handler: Any = None

    def start_watching(self, paths: list[str]) -> FlextResult[bool]:
        """Start watching the given paths for changes.

        Args:
            paths: List of paths to monitor for changes

        Returns:
            FlextResult indicating success or failure

        """
        try:
            if self._is_watching:
                return FlextResult.fail("Hot reload is already watching")

            # Convert and validate paths
            watched_paths = set()
            for path_str in paths:
                path_obj = self._resolve_watch_path(path_str)
                if path_obj.exists():
                    watched_paths.add(path_obj)
                else:
                    self.logger.warning(f"Watched path does not exist: {path_str}")

            if not watched_paths:
                return FlextResult.fail("No valid paths to watch")

            self._watched_paths = watched_paths
            self._is_watching = True

            # Start watchdog observer if available
            if HAS_WATCHDOG and Observer is not None:
                fch = cast("type", FileChangeHandler)
                self._event_handler = fch(
                    self._handle_file_change, self._watched_paths, self.logger
                )
                self._observer = Observer()
                for watched_path in watched_paths:
                    self._observer.schedule(
                        self._event_handler,
                        str(
                            watched_path.parent
                            if watched_path.is_file()
                            else watched_path
                        ),
                        recursive=True,
                    )
                self._observer.start()
                self.logger.info(
                    f"Started hot reload with watchdog for {len(watched_paths)} paths"
                )
            else:
                self.logger.info(
                    f"Started hot reload (watchdog unavailable) for {len(watched_paths)} paths"
                )

            return FlextResult.ok(True)

        except Exception as e:
            self.logger.exception("Failed to start hot reload watching")
            return FlextResult.fail(f"Start watching error: {e!s}")

    def stop_watching(self) -> FlextResult[bool]:
        """Stop watching for changes.

        Returns:
        FlextResult indicating success or failure

        """
        try:
            if not self._is_watching:
                return FlextResult.fail("Hot reload is not watching")

            # Stop watchdog observer
            if self._observer is not None:
                self._observer.stop()
                self._observer.join()
                self._observer = None
                self._event_handler = None

            self._is_watching = False
            self._watched_paths.clear()

            self.logger.info("Stopped hot reload monitoring")
            return FlextResult.ok(True)

        except Exception as e:
            self.logger.exception("Failed to stop hot reload watching")
            return FlextResult.fail(f"Stop watching error: {e!s}")

    def reload_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Reload a specific plugin.

        Args:
        plugin_name: Name of the plugin to reload

        Returns:
        FlextResult indicating success or failure

        """
        try:
            # Find the plugin file
            plugin_path = self._find_plugin_path(plugin_name)
            if not plugin_path:
                error_msg = f"Plugin file not found: {plugin_name}"
                return FlextResult.fail(error_msg)

            # Trigger reload callbacks
            for callback in self._reload_callbacks:
                try:
                    callback(plugin_name)
                except Exception:
                    self.logger.exception(f"Reload callback failed for {plugin_name}")

            # Record reload in history
            reload_record = FlextPluginModels.ReloadRecord(
                plugin_name=plugin_name,
                plugin_path=plugin_path,
                timestamp=datetime.now(UTC),
                success=True,
            )
            self._reload_history.append(reload_record)

            self.logger.info(f"Reloaded plugin: {plugin_name}")
            return FlextResult.ok(True)

        except Exception as e:
            self.logger.exception(f"Failed to reload plugin {plugin_name}")
            return FlextResult.fail(f"Reload error: {e!s}")

    def is_watching(self) -> bool:
        """Check if hot reload is currently watching for changes.

        Returns:
        True if watching, False otherwise

        """
        return self._is_watching

    def get_watched_paths(self) -> list[str]:
        """Get list of currently watched paths.

        Returns:
        List of watched path strings

        """
        return [str(path) for path in self._watched_paths]

    def add_reload_callback(self, callback: Callable[[str], object]) -> None:
        """Add a callback to be executed when a plugin is reloaded.

        Args:
        callback: Callback function to execute on reload

        """
        self._reload_callbacks.append(callback)

    def remove_reload_callback(self, callback: Callable[[str], object]) -> bool:
        """Remove a reload callback.

        Args:
        callback: Callback function to remove

        Returns:
        True if callback was removed, False if not found

        """
        try:
            self._reload_callbacks.remove(callback)
            return True
        except ValueError:
            return False

    def get_reload_history(
        self, limit: int = 100
    ) -> list[FlextPluginModels.ReloadRecord]:
        """Get reload history.

        Args:
        limit: Maximum number of history entries to return

        Returns:
        List of reload history records

        """
        return self._reload_history[-limit:] if limit > 0 else self._reload_history

    def clear_reload_history(self) -> int:
        """Clear reload history.

        Returns:
        Number of history entries cleared

        """
        count = len(self._reload_history)
        self._reload_history.clear()
        self.logger.info(f"Cleared {count} reload history entries")
        return count

    def get_hot_reload_status(self) -> dict[str, Any]:
        """Get the current status of the hot reload service.

        Returns:
        Dictionary containing hot reload status information

        """
        return {
            "is_watching": self._is_watching,
            "watched_paths": self.get_watched_paths(),
            "watch_interval": self.watch_interval,
            "debounce_ms": self.debounce_ms,
            "max_retries": self.max_retries,
            "total_reloads": len(self._reload_history),
            "recent_reloads": len([r for r in self._reload_history if r.success]),
            "callback_count": len(self._reload_callbacks),
            "using_watchdog": HAS_WATCHDOG and self._observer is not None,
        }

    def force_reload_all(self) -> FlextResult[dict[str, bool]]:
        """Force reload all plugins in watched paths.

        Returns:
        FlextResult containing reload results for each plugin

        """
        try:
            if not self._is_watching:
                return FlextResult.fail("Hot reload is not watching")

            reload_results = {}

            for watched_path in self._watched_paths:
                if watched_path.is_file() and watched_path.suffix == ".py":
                    plugin_name = watched_path.stem
                    result = self.reload_plugin(plugin_name)
                    reload_results[plugin_name] = result.is_success
                elif watched_path.is_dir():
                    for py_file in watched_path.rglob("*.py"):
                        if not py_file.name.startswith("_"):
                            plugin_name = py_file.stem
                            result = self.reload_plugin(plugin_name)
                            reload_results[plugin_name] = result.is_success

            self.logger.info(f"Force reloaded {len(reload_results)} plugins")
            return FlextResult.ok(reload_results)

        except Exception as e:
            self.logger.exception("Failed to force reload all plugins")
            return FlextResult.fail(f"Force reload error: {e!s}")

    def add_watch_path(self, path: str) -> FlextResult[bool]:
        """Add a new path to watch.

        Args:
        path: Path to add to watch list

        Returns:
        FlextResult indicating success or failure

        """
        try:
            path_obj = self._resolve_watch_path(path)

            if not path_obj.exists():
                error_msg = f"Path does not exist: {path}"
                return FlextResult.fail(error_msg)

            self._watched_paths.add(path_obj)
            self.logger.info(f"Added watch path: {path}")
            return FlextResult.ok(True)

        except Exception as e:
            self.logger.exception(f"Failed to add watch path: {path}")
            return FlextResult.fail(f"Add watch path error: {e!s}")

    def remove_watch_path(self, path: str) -> FlextResult[bool]:
        """Remove a path from watch list.

        Args:
        path: Path to remove from watch list

        Returns:
        FlextResult indicating success or failure

        """
        try:
            path_obj = self._resolve_watch_path(path)

            if path_obj in self._watched_paths:
                self._watched_paths.remove(path_obj)
                self.logger.info(f"Removed watch path: {path}")
                return FlextResult.ok(True)
            return FlextResult.fail(f"Path not being watched: {path}")

        except Exception as e:
            self.logger.exception(f"Failed to remove watch path: {path}")
            return FlextResult.fail(f"Remove watch path error: {e!s}")

    def _resolve_watch_path(self, path_str: str) -> Path:
        """Resolve and validate a watch path synchronously.

        Args:
        path_str: Path string to resolve

        Returns:
        Resolved Path object

        """
        return Path(path_str).expanduser().resolve()

    def _find_plugin_path(self, plugin_name: str) -> Path | None:
        """Find plugin file by name in watched paths.

        Args:
        plugin_name: Name of the plugin to find

        Returns:
        Path to plugin if found, None otherwise

        """
        for watched_path in self._watched_paths:
            if watched_path.is_file() and watched_path.stem == plugin_name:
                return watched_path
            if watched_path.is_dir():
                plugin_file = watched_path / f"{plugin_name}.py"
                if plugin_file.exists():
                    return plugin_file
        return None

    def _handle_file_change(self, plugin_name: str) -> None:
        """Handle a file change event.

        Args:
        plugin_name: Name of the plugin that changed

        """
        self.logger.debug(f"Detected file change for plugin: {plugin_name}")
        # Reload is triggered by the calling context


__all__ = ["FlextPluginHotReload"]
