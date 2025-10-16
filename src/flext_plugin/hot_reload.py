"""FLEXT Plugin Hot Reload - Plugin hot reload and file monitoring.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import asyncio
import contextlib
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

from flext_core import FlextLogger, FlextResult, FlextTypes


class FlextPluginHotReload:
    """Plugin hot reload service for real-time plugin updates.

    This class provides comprehensive hot reload functionality including
    file monitoring, automatic reloading, and change detection.

    Usage:
        ```python
        from flext_plugin import FlextPluginHotReload

        # Initialize hot reload service
        hot_reload = FlextPluginHotReload()

        # Start monitoring
        result = await hot_reload.start_watching(["./plugins"])
        if result.success:
            print("Hot reload monitoring started")

        # Stop monitoring
        await hot_reload.stop_watching()
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
            watch_interval: File watching interval in seconds
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
        self._file_timestamps: dict[Path, float] = {}
        self._reload_callbacks: list[Callable[[str], object]] = []
        self._watch_task: asyncio.Task | None = None
        self._reload_history: list[FlextTypes.Dict] = []

    def _resolve_watch_path(self, path_str: str) -> Path:
        """Resolve and validate a watch path synchronously.

        Args:
            path_str: Path string to resolve

        Returns:
            Resolved Path object

        """
        return Path(path_str).expanduser().resolve()

    async def start_watching(self, paths: FlextTypes.StringList) -> FlextResult[bool]:
        """Start watching the given paths for changes.

        Args:
            paths: List of paths to monitor for changes

        Returns:
            FlextResult indicating success or failure

        """
        try:
            if self._is_watching:
                return FlextResult.fail("Hot reload is already watching")

            # Convert paths to Path objects
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

            # Start the watch task
            self._watch_task = asyncio.create_task(self._watch_loop())

            self.logger.info(
                f"Started hot reload monitoring for {len(watched_paths)} paths"
            )
            return FlextResult.ok(True)

        except Exception as e:
            self.logger.exception("Failed to start hot reload watching")
            return FlextResult.fail(f"Start watching error: {e!s}")

    async def stop_watching(self) -> FlextResult[bool]:
        """Stop watching for changes.

        Returns:
            FlextResult indicating success or failure

        """
        try:
            if not self._is_watching:
                return FlextResult.fail("Hot reload is not watching")

            self._is_watching = False

            # Cancel the watch task
            if self._watch_task and not self._watch_task.done():
                self._watch_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await self._watch_task

            self._watch_task = None
            self._watched_paths.clear()
            self._file_timestamps.clear()

            self.logger.info("Stopped hot reload monitoring")
            return FlextResult.ok(True)

        except Exception as e:
            self.logger.exception("Failed to stop hot reload watching")
            return FlextResult.fail(f"Stop watching error: {e!s}")

    async def reload_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Reload a specific plugin.

        Args:
            plugin_name: Name of the plugin to reload

        Returns:
            FlextResult indicating success or failure

        """
        try:
            # Find the plugin file
            plugin_path = None
            for watched_path in self._watched_paths:
                if watched_path.is_file() and watched_path.stem == plugin_name:
                    plugin_path = watched_path
                    break
                if watched_path.is_dir():
                    plugin_file = watched_path / f"{plugin_name}.py"
                    if plugin_file.exists():
                        plugin_path = plugin_file
                        break

            if not plugin_path:
                return FlextResult.fail(f"Plugin file not found: {plugin_name}")

            # Trigger reload callbacks
            for callback in self._reload_callbacks:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(plugin_name)
                    else:
                        callback(plugin_name)
                except Exception:
                    self.logger.exception(f"Reload callback failed for {plugin_name}")

            # Record reload in history
            reload_record = {
                "plugin_name": plugin_name,
                "plugin_path": str(plugin_path),
                "timestamp": self._get_current_timestamp(),
                "success": True,
            }
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

    def get_watched_paths(self) -> FlextTypes.StringList:
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

    def get_reload_history(self, limit: int = 100) -> list[FlextTypes.Dict]:
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

    async def _watch_loop(self) -> None:
        """Main file watching loop."""
        try:
            while self._is_watching:
                await self._check_for_changes()
                await asyncio.sleep(self.watch_interval)
        except asyncio.CancelledError:
            self.logger.debug("Watch loop cancelled")
        except Exception:
            self.logger.exception("Error in watch loop")

    async def _check_for_changes(self) -> None:
        """Check for file changes in watched paths."""
        try:
            changed_files = []

            for watched_path in self._watched_paths:
                if watched_path.is_file():
                    # Single file
                    if self._has_file_changed(watched_path):
                        changed_files.append(watched_path)
                elif watched_path.is_dir():
                    # Directory - check all Python files
                    changed_files.extend(
                        py_file
                        for py_file in watched_path.rglob("*.py")
                        if self._has_file_changed(py_file)
                    )

            # Process changed files
            for changed_file in changed_files:
                await self._handle_file_change(changed_file)

        except Exception:
            self.logger.exception("Error checking for file changes")

    def _has_file_changed(self, file_path: Path) -> bool:
        """Check if a file has changed since last check.

        Args:
            file_path: Path to the file to check

        Returns:
            True if file has changed, False otherwise

        """
        try:
            if not file_path.exists():
                return False

            current_mtime = file_path.stat().st_mtime
            last_mtime = self._file_timestamps.get(file_path, 0)

            if current_mtime > last_mtime:
                self._file_timestamps[file_path] = current_mtime
                return True

            return False

        except Exception as e:
            self.logger.debug(f"Error checking file change for {file_path}: {e}")
            return False

    async def _handle_file_change(self, file_path: Path) -> None:
        """Handle a file change event.

        Args:
            file_path: Path to the changed file

        """
        try:
            # Extract plugin name from file path
            plugin_name = file_path.stem

            # Apply debounce
            await asyncio.sleep(self.debounce_ms / 1000.0)

            # Check if file still exists and has changed (run in thread pool)
            loop = asyncio.get_event_loop()
            file_exists = await loop.run_in_executor(None, file_path.exists)
            if not file_exists:
                return

            current_mtime = await loop.run_in_executor(
                None,
                lambda: file_path.stat().st_mtime,  # noqa: ASYNC240
            )
            if self._file_timestamps.get(file_path, 0) >= current_mtime:
                return

            # Reload the plugin
            reload_result = await self.reload_plugin(plugin_name)
            if reload_result.is_success:
                self.logger.info(f"Hot reloaded plugin from file change: {file_path}")
            else:
                self.logger.warning(
                    f"Failed to hot reload plugin: {reload_result.error}"
                )

        except Exception:
            self.logger.exception(f"Error handling file change for {file_path}")

    def _get_current_timestamp(self) -> str:
        """Get current timestamp as ISO string.

        Returns:
            Current timestamp as ISO string

        """
        return datetime.now(UTC).isoformat()

    def get_hot_reload_status(self) -> FlextTypes.Dict:
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
            "recent_reloads": len(
                [r for r in self._reload_history if r.get("success", False)]
            ),
            "callback_count": len(self._reload_callbacks),
        }

    async def force_reload_all(self) -> FlextResult[dict[str, bool]]:
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
                    result = await self.reload_plugin(plugin_name)
                    reload_results[plugin_name] = result.is_success
                elif watched_path.is_dir():
                    for py_file in watched_path.rglob("*.py"):
                        plugin_name = py_file.stem
                        result = await self.reload_plugin(plugin_name)
                        reload_results[plugin_name] = result.is_success

            self.logger.info(f"Force reloaded {len(reload_results)} plugins")
            return FlextResult.ok(reload_results)

        except Exception as e:
            self.logger.exception("Failed to force reload all plugins")
            return FlextResult.fail(f"Force reload error: {e!s}")

    async def add_watch_path(self, path: str) -> FlextResult[bool]:
        """Add a new path to watch.

        Args:
            path: Path to add to watch list

        Returns:
            FlextResult indicating success or failure

        """
        try:
            # Run pathlib operations in thread pool
            loop = asyncio.get_event_loop()
            path_obj = await loop.run_in_executor(
                None,
                lambda: Path(path).expanduser().resolve(),  # noqa: ASYNC240
            )
            path_exists = await loop.run_in_executor(None, path_obj.exists)

            if not path_exists:
                return FlextResult.fail(f"Path does not exist: {path}")

            self._watched_paths.add(path_obj)
            self.logger.info(f"Added watch path: {path}")
            return FlextResult.ok(True)

        except Exception as e:
            self.logger.exception(f"Failed to add watch path: {path}")
            return FlextResult.fail(f"Add watch path error: {e!s}")

    async def remove_watch_path(self, path: str) -> FlextResult[bool]:
        """Remove a path from watch list.

        Args:
            path: Path to remove from watch list

        Returns:
            FlextResult indicating success or failure

        """
        try:
            # Run pathlib operations in thread pool
            loop = asyncio.get_event_loop()
            path_obj = await loop.run_in_executor(
                None,
                lambda: Path(path).expanduser().resolve(),  # noqa: ASYNC240
            )

            if path_obj in self._watched_paths:
                self._watched_paths.remove(path_obj)
                # Remove from timestamps
                self._file_timestamps.pop(path_obj, None)
                self.logger.info(f"Removed watch path: {path}")
                return FlextResult.ok(True)
            return FlextResult.fail(f"Path not being watched: {path}")

        except Exception as e:
            self.logger.exception(f"Failed to remove watch path: {path}")
            return FlextResult.fail(f"Remove watch path error: {e!s}")


__all__ = ["FlextPluginHotReload"]
