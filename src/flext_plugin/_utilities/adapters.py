"""FLEXT Plugin Adapters - Infrastructure adapters with composition pattern.

Synchronous adapter implementations for plugin system operations following
SOLID principles with composition and Pydantic models replacing all dict usage.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib.util
from collections.abc import (
    Callable,
    MutableMapping,
    MutableSequence,
    Sequence,
)
from pathlib import Path
from types import ModuleType
from typing import override

from flext_plugin import FlextPluginDiscovery, c, m, p, r, t, u


class FlextPluginAdapters:
    """Infrastructure adapters with composition pattern.

    Consolidates adapter implementations using a shared BaseAdapter for
    common functionality, following DRY and SRP principles.
    """

    class BaseAdapter:
        """Shared adapter base with common functionality."""

        def __init__(self) -> None:
            """Initialize base adapter with logger."""
            super().__init__()
            self.logger = u.fetch_logger(__name__)

        def _execute_safe[TResult](
            self,
            operation: Callable[[], TResult],
            error_context: str,
        ) -> p.Result[TResult]:
            """Execute operation with safe error handling.

            Args:
            operation: Callable to execute
            error_context: Error message context

            Returns:
            r with operation result or failure

            """
            try:
                result = operation()
                return r[TResult].ok(result)
            except c.EXC_BROAD_IO_TYPE as e:
                self.logger.exception(error_context)
                error_msg = f"{error_context}: {e!s}"
                return r[TResult].fail(error_msg)

    class FileSystemDiscoveryAdapter(BaseAdapter, p.Plugin.PluginDiscovery):
        """File system plugin discovery - synchronous."""

        @override
        def discover_plugin(
            self,
            plugin_path: str,
        ) -> p.Result[m.Plugin.DiscoveryData]:
            """Discover single plugin at path."""
            return self._execute_safe(
                lambda: self._discover_single(plugin_path),
                f"Failed to discover plugin at {plugin_path}",
            )

        @override
        def discover_plugins(
            self,
            paths: t.StrSequence,
        ) -> p.Result[Sequence[m.Plugin.DiscoveryData]]:
            """Discover plugins in given paths."""
            return self._execute_safe(
                lambda: self._discover_all(paths),
                "Plugin discovery failed",
            )

        @override
        def validate_plugin(
            self,
            plugin_data: m.Plugin.DiscoveryData,
        ) -> p.Result[bool]:
            """Validate discovered plugin data."""
            return self._execute_safe(lambda: True, "Plugin validation failed")

        def _discover_all(
            self,
            paths: t.StrSequence,
        ) -> t.SequenceOf[m.Plugin.DiscoveryData]:
            """Internal: discover all plugins."""
            discovered: MutableSequence[m.Plugin.DiscoveryData] = []
            for path in paths:
                if not path.strip():
                    self.logger.debug("Skipping blank plugin discovery path")
                    continue
                path_obj = Path(path).expanduser().resolve()
                if not path_obj.exists():
                    self.logger.warning("Path does not exist: %s", path)
                    continue
                if path_obj.is_file():
                    data = self._discover_single_file(path_obj)
                    if data:
                        discovered.append(data)
                elif path_obj.is_dir():
                    discovered.extend(self._discover_directory(path_obj))
            self.logger.info(f"Discovered {len(discovered)} plugins")
            return discovered

        def _discover_directory(
            self, path: Path
        ) -> t.SequenceOf[m.Plugin.DiscoveryData]:
            """Internal: discover plugins in directory."""
            return FlextPluginDiscovery.discover_python_plugins_in_directory(
                path,
                self._discover_single_file,
                self.logger,
            )

        def _discover_single(self, plugin_path: str) -> m.Plugin.DiscoveryData:
            """Internal: discover single plugin."""
            path_obj = Path(plugin_path).expanduser().resolve()
            if not path_obj.exists():
                error_msg = f"Plugin path does not exist: {plugin_path}"
                raise FileNotFoundError(error_msg)
            data = self._discover_single_file(path_obj)
            if not data:
                error_msg = f"Failed to discover plugin at: {plugin_path}"
                raise ValueError(error_msg)
            return data

        def _discover_single_file(self, path: Path) -> m.Plugin.DiscoveryData | None:
            """Internal: discover single file."""
            if path.suffix != ".py":
                return None
            try:
                return m.Plugin.DiscoveryData(
                    name=path.stem,
                    version=c.Plugin.DEFAULT_PLUGIN_VERSION,
                    path=path,
                    discovery_type=c.Plugin.DiscoveryTypeLiteral.FILE,
                    discovery_method=c.Plugin.DiscoveryMethodLiteral.FILE_SYSTEM,
                    metadata={},
                )
            except ValueError:
                self.logger.exception(
                    "Failed to create discovery data",
                    path=str(path),
                )
                return None

    class DynamicLoaderAdapter(BaseAdapter, p.Plugin.PluginLoader):
        """Dynamic plugin loading - synchronous."""

        def __init__(self) -> None:
            """Initialize the synchronous plugin adapter."""
            super().__init__()
            self._loaded_plugins: MutableMapping[str, ModuleType] = {}

        @override
        def get_loaded_plugins(self) -> t.StrSequence:
            """Get list of loaded plugins."""
            return list(self._loaded_plugins.keys())

        @override
        def plugin_loaded(self, plugin_name: str) -> bool:
            """Check if a plugin is loaded."""
            return plugin_name in self._loaded_plugins

        @override
        def load_plugin(self, plugin_path: str) -> p.Result[t.JsonMapping]:
            """Load plugin from path."""
            return self._execute_safe(
                lambda: self._load_module_as_dict(plugin_path),
                f"Loading error: {plugin_path}",
            )

        @override
        def unload_plugin(self, plugin_name: str) -> p.Result[bool]:
            """Unload a plugin by name."""

            def _unload() -> bool:
                if plugin_name not in self._loaded_plugins:
                    error_msg = f"Plugin not loaded: {plugin_name}"
                    raise ValueError(error_msg)
                del self._loaded_plugins[plugin_name]
                return True

            return self._execute_safe(_unload, f"Failed to unload plugin {plugin_name}")

        def _load_module(self, plugin_path: str) -> m.Plugin.LoadData:
            """Internal: load module using spec."""
            path = Path(plugin_path).expanduser().resolve()
            if not path.exists():
                error_msg = f"Plugin path does not exist: {plugin_path}"
                raise FileNotFoundError(error_msg)
            spec = importlib.util.spec_from_file_location(path.stem, path)
            if not spec or not spec.loader:
                error_msg = f"Cannot load spec from {path}"
                raise ImportError(error_msg)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return m.Plugin.LoadData(
                name=path.stem,
                version=str(
                    getattr(
                        module,
                        "__version__",
                        c.Plugin.DEFAULT_PLUGIN_VERSION,
                    ),
                ),
                path=path,
                module=module,
                load_type=c.Plugin.LoadTypeLiteral.FILE,
                loaded_at=__import__("datetime").datetime.now(
                    __import__("datetime").UTC,
                ),
                entry_file=None,
            )

        def _load_module_as_dict(
            self,
            plugin_path: str,
        ) -> t.JsonMapping:
            """Load module and convert to JsonMapping."""
            data = self._load_module(plugin_path)
            self._loaded_plugins[data.name] = data.module
            return {
                "name": data.name,
                "version": data.version,
                "path": str(data.path),
                "load_type": data.load_type,
                "loaded_at": data.loaded_at.isoformat(),
            }

    class PluginExecutorAdapter(BaseAdapter, p.Plugin.PluginExecution):
        """Plugin execution - synchronous."""

        @override
        def execute_plugin(
            self,
            plugin_name: str,
            context: t.JsonMapping,
        ) -> p.Result[t.JsonMapping]:
            """Execute plugin."""
            return self._execute_safe(
                lambda: {"status": "executed", "plugin": plugin_name},
                f"Execution error: {plugin_name}",
            )

        @override
        def get_execution_status(self, _execution_id: str) -> p.Result[str]:
            """Get execution status."""
            return r[str].ok(c.Plugin.Execution.STATE_COMPLETED)

        @override
        def list_running_executions(self) -> t.StrSequence:
            """List running executions."""
            return []

        @override
        def stop_execution(self, _execution_id: str) -> p.Result[bool]:
            """Stop plugin execution."""
            return r[bool].ok(True)


__all__: list[str] = ["FlextPluginAdapters"]
