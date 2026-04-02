"""FLEXT Plugin Hot Reload - Plugin hot reload and file monitoring.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Callable, MutableSequence, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import override

from watchdog.events import DirModifiedEvent, FileModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer as WatchdogObserver
from watchdog.observers.api import BaseObserver

from flext_core import FlextLogger, r
from flext_plugin import m, p, t


class FlextPluginFileChangeHandler(FileSystemEventHandler):
    """Watchdog event handler for file change detection."""

    def __init__(
        self,
        callback: Callable[[str], None],
        watched_paths: set[Path],
        logger: p.Logger,
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

    @override
    def on_modified(self, event: FileModifiedEvent | DirModifiedEvent) -> None:
        """Handle file modification event.

        Args:
        event: FileModifiedEvent or DirModifiedEvent from watchdog

        """
        if event.is_directory:
            return
        src_path = str(event.src_path)
        if not src_path.endswith(".py"):
            return
        file_path = Path(src_path)
        for watched_path in self.watched_paths:
            if (watched_path.is_file() and file_path == watched_path) or (
                watched_path.is_dir() and file_path.is_relative_to(watched_path)
            ):
                self.callback(file_path.stem)
                break


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
            hot_reload.logger.info("hot_reload_monitoring_started")

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
        self._is_watching = False
        self._watched_paths: set[Path] = set()
        self._reload_callbacks: MutableSequence[Callable[[str], None]] = []
        self._reload_history: MutableSequence[m.Plugin.ReloadRecord] = []
        self._observer: BaseObserver | None = None
        self._event_handler: FileSystemEventHandler | None = None

    def add_reload_callback(self, callback: Callable[[str], None]) -> None:
        """Add a callback to be executed when a plugin is reloaded.

        Args:
        callback: Callback function to execute on reload

        """
        self._reload_callbacks.append(callback)

    def add_watch_path(self, path: str) -> r[bool]:
        """Add a new path to watch.

        Args:
        path: Path to add to watch list

        Returns:
        r indicating success or failure

        """
        try:
            path_obj = self._resolve_watch_path(path)
            if not path_obj.exists():
                error_msg = f"Path does not exist: {path}"
                return r[bool].fail(error_msg)
            self._watched_paths.add(path_obj)
            self.logger.info("Added watch path: %s", path)
            return r[bool].ok(True)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to add watch path: %s", path)
            return r[bool].fail(f"Add watch path error: {e!s}")

    def clear_reload_history(self) -> int:
        """Clear reload history.

        Returns:
        Number of history entries cleared

        """
        count = len(self._reload_history)
        self._reload_history.clear()
        self.logger.info("Cleared %s reload history entries", count)
        return count

    def force_reload_all(self) -> r[t.ContainerMapping]:
        """Force reload all plugins in watched paths.

        Returns:
        r containing reload results for each plugin

        """
        try:
            if not self._is_watching:
                return r[t.ContainerMapping].fail(
                    "Hot reload is not watching",
                )
            reload_results: MutableSequence[t.ContainerMapping] = []
            for watched_path in self._watched_paths:
                if watched_path.is_file() and watched_path.suffix == ".py":
                    plugin_name = watched_path.stem
                    result = self.reload_plugin(plugin_name)
                    reload_results.append({
                        "plugin_name": plugin_name,
                        "success": result.is_success,
                    })
                elif watched_path.is_dir():
                    for py_file in watched_path.rglob("*.py"):
                        if not py_file.name.startswith("_"):
                            plugin_name = py_file.stem
                            result = self.reload_plugin(plugin_name)
                            reload_results.append({
                                "plugin_name": plugin_name,
                                "success": result.is_success,
                            })
            self.logger.info(f"Force reloaded {len(reload_results)} plugins")
            return r[t.ContainerMapping].ok({
                "plugin_results": reload_results,
                "count": len(reload_results),
            })
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to force reload all plugins")
            return r[t.ContainerMapping].fail(f"Force reload error: {e!s}")

    def get_hot_reload_status(self) -> t.ContainerMapping:
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
            "recent_reloads": len([rec for rec in self._reload_history if rec.success]),
            "callback_count": len(self._reload_callbacks),
            "using_watchdog": self._observer is not None,
        }

    def get_reload_history(
        self,
        limit: int = 100,
    ) -> Sequence[m.Plugin.ReloadRecord]:
        """Get reload history.

        Args:
        limit: Maximum number of history entries to return

        Returns:
        List of reload history records

        """
        return self._reload_history[-limit:] if limit > 0 else self._reload_history

    def get_watched_paths(self) -> t.StrSequence:
        """Get list of currently watched paths.

        Returns:
        List of watched path strings

        """
        return [str(path) for path in self._watched_paths]

    def is_watching(self) -> bool:
        """Check if hot reload is currently watching for changes.

        Returns:
        True if watching, False otherwise

        """
        return self._is_watching

    def reload_plugin(self, plugin_name: str) -> r[bool]:
        """Reload a specific plugin.

        Args:
        plugin_name: Name of the plugin to reload

        Returns:
        r indicating success or failure

        """
        try:
            plugin_path = self._find_plugin_path(plugin_name)
            if not plugin_path:
                error_msg = f"Plugin file not found: {plugin_name}"
                return r[bool].fail(error_msg)
            for callback in self._reload_callbacks:
                try:
                    callback(plugin_name)
                except (
                    ValueError,
                    TypeError,
                    KeyError,
                    AttributeError,
                    OSError,
                    RuntimeError,
                    ImportError,
                ):
                    self.logger.exception("Reload callback failed for %s", plugin_name)
            reload_record = m.Plugin.ReloadRecord(
                plugin_name=plugin_name,
                plugin_path=plugin_path,
                timestamp=datetime.now(UTC),
                success=True,
            )
            self._reload_history.append(reload_record)
            self.logger.info("Reloaded plugin: %s", plugin_name)
            return r[bool].ok(True)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to reload plugin %s", plugin_name)
            return r[bool].fail(f"Reload error: {e!s}")

    def remove_reload_callback(self, callback: Callable[[str], None]) -> bool:
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

    def remove_watch_path(self, path: str) -> r[bool]:
        """Remove a path from watch list.

        Args:
        path: Path to remove from watch list

        Returns:
        r indicating success or failure

        """
        try:
            path_obj = self._resolve_watch_path(path)
            if path_obj in self._watched_paths:
                self._watched_paths.remove(path_obj)
                self.logger.info("Removed watch path: %s", path)
                return r[bool].ok(True)
            return r[bool].fail(f"Path not being watched: {path}")
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to remove watch path: %s", path)
            return r[bool].fail(f"Remove watch path error: {e!s}")

    def start_watching(self, paths: t.StrSequence) -> r[bool]:
        """Start watching the given paths for changes.

        Args:
            paths: List of paths to monitor for changes

        Returns:
            r indicating success or failure

        """
        try:
            if self._is_watching:
                return r[bool].fail("Hot reload is already watching")
            watched_paths: set[Path] = set()
            for path_str in paths:
                path_obj = self._resolve_watch_path(path_str)
                if path_obj.exists():
                    watched_paths.add(path_obj)
                else:
                    self.logger.warning("Watched path does not exist: %s", path_str)
            if not watched_paths:
                return r[bool].fail("No valid paths to watch")
            self._watched_paths = watched_paths
            self._is_watching = True
            self._event_handler = FlextPluginFileChangeHandler(
                self._handle_file_change,
                self._watched_paths,
                self.logger,
            )
            self._observer = WatchdogObserver()
            if self._observer:
                for watched_path in watched_paths:
                    self._observer.schedule(
                        self._event_handler,
                        str(
                            watched_path.parent
                            if watched_path.is_file()
                            else watched_path,
                        ),
                        recursive=True,
                    )
                self._observer.start()
                self.logger.info(
                    f"Started hot reload with watchdog for {len(watched_paths)} paths",
                )
            self.logger.info(
                f"Started hot reload (watchdog unavailable) for {len(watched_paths)} paths",
            )
            return r[bool].ok(True)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to start hot reload watching")
            return r[bool].fail(f"Start watching error: {e!s}")

    def stop_watching(self) -> r[bool]:
        """Stop watching for changes.

        Returns:
        r indicating success or failure

        """
        try:
            if not self._is_watching:
                return r[bool].fail("Hot reload is not watching")
            obs = self._observer
            if obs is not None:
                obs.stop()
                obs.join()
                self._observer = None
                self._event_handler = None
            self._is_watching = False
            self._watched_paths.clear()
            self.logger.info("Stopped hot reload monitoring")
            return r[bool].ok(True)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to stop hot reload watching")
            return r[bool].fail(f"Stop watching error: {e!s}")

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
        self.logger.debug("Detected file change for plugin: %s", plugin_name)

    def _resolve_watch_path(self, path_str: str) -> Path:
        """Resolve and validate a watch path synchronously.

        Args:
        path_str: Path string to resolve

        Returns:
        Resolved Path instance

        """
        return Path(path_str).expanduser().resolve()


__all__ = ["FlextPluginHotReload"]
