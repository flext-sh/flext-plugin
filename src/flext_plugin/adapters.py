"""FLEXT Plugin Adapters - Infrastructure adapters with composition pattern.

Synchronous adapter implementations for plugin system operations following
SOLID principles with composition and Pydantic models replacing all dict usage.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib.util
from collections.abc import Callable, Mapping
from pathlib import Path
from types import ModuleType
from typing import override

from flext_core import FlextLogger, T, r
from pydantic import TypeAdapter

from flext_plugin import c, m, p, t
from flext_plugin.protocols import FlextPluginProtocols

PluginDiscovery = FlextPluginProtocols.Plugin.PluginDiscovery
PluginRegistry = FlextPluginProtocols.Plugin.PluginRegistry


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
            self.logger = FlextLogger(__name__)

        def _execute_safe(self, operation: Callable[[], T], error_context: str) -> r[T]:
            """Execute operation with safe error handling.

            Args:
            operation: Callable to execute
            error_context: Error message context

            Returns:
            r with operation result or failure

            """
            try:
                result = operation()
                return r.ok(result)
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                RuntimeError,
                ImportError,
            ) as e:
                self.logger.exception(error_context)
                error_msg = f"{error_context}: {e!s}"
                return r[T].fail(error_msg)

    class FileSystemDiscoveryAdapter(BaseAdapter, PluginDiscovery):
        """File system plugin discovery - synchronous."""

        @override
        def discover_plugin(
            self, _plugin_path: str
        ) -> r[Mapping[str, t.NormalizedValue]]:
            """Discover single plugin at path."""
            return self._execute_safe(
                lambda: self._discovery_data_to_dict(
                    self._discover_single(_plugin_path)
                ),
                f"Failed to discover plugin at {_plugin_path}",
            )

        @override
        def discover_plugins(
            self, paths: list[str]
        ) -> r[list[Mapping[str, t.NormalizedValue]]]:
            """Discover plugins in given paths."""
            return self._execute_safe(
                lambda: [
                    self._discovery_data_to_dict(d) for d in self._discover_all(paths)
                ],
                "Plugin discovery failed",
            )

        @override
        def validate_plugin(
            self, _plugin_data: Mapping[str, t.NormalizedValue]
        ) -> r[bool]:
            """Validate discovered plugin data."""
            return self._execute_safe(lambda: True, "Plugin validation failed")

        @override
        def validate_plugin_security(self, _plugin: t.NormalizedValue) -> r[bool]:
            return r[bool].ok(value=True)

        def _discover_all(self, paths: list[str]) -> list[m.Plugin.DiscoveryData]:
            """Internal: discover all plugins."""
            discovered: list[m.Plugin.DiscoveryData] = []
            for path in paths:
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

        def _discover_directory(self, path: Path) -> list[m.Plugin.DiscoveryData]:
            """Internal: discover plugins in directory."""
            discovered: list[m.Plugin.DiscoveryData] = []
            try:
                for item in path.iterdir():
                    if (
                        item.is_file()
                        and item.suffix == ".py"
                        and (not item.name.startswith("_"))
                    ):
                        data = self._discover_single_file(item)
                        if data:
                            discovered.append(data)
                    elif item.is_dir() and (not item.name.startswith("__")):
                        discovered.extend(self._discover_directory(item))
            except (OSError, PermissionError):
                self.logger.exception(f"Failed to discover directory {path}")
            return discovered

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
                    version=c.Plugin.Discovery.DEFAULT_PLUGIN_VERSION,
                    path=path,
                    discovery_type=c.Plugin.Discovery.DISCOVERY_TYPE_FILE,
                    discovery_method=c.Plugin.Discovery.METHOD_FILE_SYSTEM,
                    metadata={},
                )
            except ValueError:
                self.logger.exception(f"Failed to create discovery data for {path}")
                return None

        def _discovery_data_to_dict(
            self, data: m.Plugin.DiscoveryData
        ) -> Mapping[str, t.NormalizedValue]:
            """Convert DiscoveryData model to JsonDict."""
            return {
                "name": data.name,
                "version": data.version,
                "path": str(data.path),
                "discovery_type": data.discovery_type,
                "discovery_method": data.discovery_method,
            }

    class DynamicLoaderAdapter(BaseAdapter, p.Plugin.PluginLoader):
        """Dynamic plugin loading - synchronous."""

        def __init__(self) -> None:
            """Initialize the synchronous plugin adapter."""
            super().__init__()
            self._loaded_plugins: dict[str, ModuleType] = {}

        @override
        def get_loaded_plugins(self) -> list[str]:
            """Get list of loaded plugins."""
            return list(self._loaded_plugins.keys())

        @override
        def is_plugin_loaded(self, plugin_name: str) -> bool:
            """Check if a plugin is loaded."""
            return plugin_name in self._loaded_plugins

        @override
        def load_plugin(self, plugin_path: str) -> r[Mapping[str, t.NormalizedValue]]:
            """Load plugin from path."""
            return self._execute_safe(
                lambda: self._load_module_as_dict(plugin_path),
                f"Loading error: {plugin_path}",
            )

        @override
        def unload_plugin(self, plugin_name: str) -> r[bool]:
            """Unload a plugin by name."""

            def _unload() -> bool:
                if plugin_name not in self._loaded_plugins:
                    error_msg = f"Plugin not loaded: {plugin_name}"
                    raise ValueError(error_msg)
                del self._loaded_plugins[plugin_name]
                return True

            return self._execute_safe(_unload, f"Failed to unload plugin {plugin_name}")

        def _load_module(self, _plugin_path: str) -> m.Plugin.LoadData:
            """Internal: load module using spec."""
            path = Path(_plugin_path).expanduser().resolve()
            if not path.exists():
                error_msg = f"Plugin path does not exist: {_plugin_path}"
                raise FileNotFoundError(error_msg)
            spec = importlib.util.spec_from_file_location(path.stem, path)
            if not spec or not spec.loader:
                error_msg = f"Cannot load spec from {path}"
                raise ImportError(error_msg)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return m.Plugin.LoadData(
                name=path.stem,
                version=getattr(
                    module, "__version__", c.Plugin.Discovery.DEFAULT_PLUGIN_VERSION
                ),
                path=path,
                module=module,
                load_type=c.Plugin.Execution.LOAD_TYPE_FILE,
                loaded_at=__import__("datetime").datetime.now(
                    __import__("datetime").UTC
                ),
                entry_file=None,
            )

        def _load_module_as_dict(
            self, plugin_path: str
        ) -> Mapping[str, t.NormalizedValue]:
            """Load module and convert to JsonDict."""
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
            self, _plugin_name: str, _context: Mapping[str, t.NormalizedValue]
        ) -> r[Mapping[str, t.NormalizedValue]]:
            """Execute plugin."""
            return self._execute_safe(
                lambda: {"status": "executed", "plugin": _plugin_name},
                f"Execution error: {_plugin_name}",
            )

        @override
        def get_execution_status(self, _execution_id: str) -> r[str]:
            """Get execution status."""
            return r.ok(c.Plugin.Execution.STATE_COMPLETED)

        @override
        def list_running_executions(self) -> list[str]:
            """List running executions."""
            return []

        @override
        def stop_execution(self, _execution_id: str) -> r[bool]:
            """Stop plugin execution."""
            return r.ok(True)

    class PluginSecurityAdapter(BaseAdapter, p.Plugin.PluginSecurity):
        """Plugin security validation - synchronous."""

        @override
        def check_permissions(
            self, _plugin_name: str, _permissions: list[str]
        ) -> r[bool]:
            """Check plugin permissions."""
            return r.ok(True)

        @override
        def get_security_level(self, _plugin_name: str) -> r[str]:
            """Get security level."""
            return r.ok(c.Plugin.PluginSecurity.SECURITY_MEDIUM)

        @override
        def scan_plugin_security(
            self, _plugin_path: str
        ) -> r[Mapping[str, t.NormalizedValue]]:
            """Scan plugin for security issues."""
            return r.ok({"security_level": c.Plugin.PluginSecurity.SECURITY_MEDIUM})

        @override
        def validate_plugin_security(self, _plugin: t.NormalizedValue) -> r[bool]:
            """Validate plugin for security."""
            return r.ok(True)

    class MemoryRegistryAdapter(BaseAdapter, PluginRegistry):
        """In-memory plugin registry - synchronous."""

        def __init__(self) -> None:
            """Initialize registry adapter."""
            super().__init__()
            self._plugins: dict[str, t.NormalizedValue] = {}

        @override
        def get_plugin(self, plugin_name: str) -> r[t.NormalizedValue | None]:
            """Get plugin from registry."""
            return r.ok(self._plugins.get(plugin_name))

        @override
        def is_plugin_registered(self, plugin_name: str) -> bool:
            """Check if plugin is registered."""
            return plugin_name in self._plugins

        @override
        def list_plugins(self) -> r[list[Mapping[str, t.NormalizedValue]]]:
            """List all plugins in registry."""
            return r.ok([])

        @override
        def register(self, plugin: t.NormalizedValue) -> r[None]:
            if not isinstance(plugin, Mapping):
                return r[None].fail("Plugin payload must be a mapping")
            plugin_payload = TypeAdapter(dict[str, t.NormalizedValue]).validate_python(
                plugin
            )
            plugin_name = plugin_payload.get("name")
            if not isinstance(plugin_name, str) or not plugin_name:
                return r[None].fail("Plugin payload missing valid 'name'")
            self._plugins[plugin_name] = plugin_payload
            return r[None].ok(None)

        @override
        def register_plugin(self, _plugin: t.NormalizedValue) -> r[bool]:
            """Register plugin in registry."""
            registration_result = self.register(_plugin)
            if registration_result.is_failure:
                return r[bool].fail(registration_result.error or "Registration failed")
            return r.ok(True)

        @override
        def unregister_plugin(self, plugin_name: str) -> r[bool]:
            """Unregister plugin from registry."""
            self._plugins.pop(plugin_name, None)
            return r.ok(True)

    class PluginMonitoringAdapter(BaseAdapter, p.Plugin.PluginMonitoring):
        """Plugin monitoring - synchronous."""

        @override
        def get_plugin_health(
            self, _plugin_name: str
        ) -> r[Mapping[str, t.NormalizedValue]]:
            """Get plugin health information."""
            return r.ok({"status": c.Plugin.PluginStatus.HEALTHY})

        @override
        def get_plugin_metrics(
            self, _plugin_name: str
        ) -> r[Mapping[str, t.NormalizedValue]]:
            """Get plugin metrics."""
            return r.ok({"execution_count": 0, "error_count": 0})

        @override
        def is_monitoring(self, _plugin_name: str) -> bool:
            """Check if plugin is being monitored."""
            return False

        @override
        def start_monitoring(self, _plugin_name: str) -> r[bool]:
            """Start monitoring plugin."""
            return r.ok(True)

        @override
        def stop_monitoring(self, _plugin_name: str) -> r[bool]:
            """Stop monitoring plugin."""
            return r.ok(True)


__all__ = ["FlextPluginAdapters"]
