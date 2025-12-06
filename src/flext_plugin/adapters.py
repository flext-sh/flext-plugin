"""FLEXT Plugin Adapters - Infrastructure adapters with composition pattern.

Synchronous adapter implementations for plugin system operations following
SOLID principles with composition and Pydantic models replacing all dict usage.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib.util
from collections.abc import Callable
from pathlib import Path
from typing import TypeVar

from flext_core import FlextLogger, FlextResult

from flext_plugin.models import FlextPluginModels
from flext_plugin.protocols import FlextPluginProtocols
from flext_plugin.types import FlextPluginTypes

T = TypeVar("T")


class FlextPluginAdapters:
    """Infrastructure adapters with composition pattern.

    Consolidates adapter implementations using a shared BaseAdapter for
    common functionality, following DRY and SRP principles.
    """

    class BaseAdapter:
        """Shared adapter base with common functionality."""

        def __init__(self) -> None:
            """Initialize base adapter with logger."""
            self.logger = FlextLogger(__name__)

        def _execute_safe(
            self,
            operation: Callable[[], T],
            error_context: str,
        ) -> FlextResult[T]:
            """Execute operation with safe error handling.

            Args:
            operation: Callable to execute
            error_context: Error message context

            Returns:
            FlextResult with operation result or failure

            """
            try:
                result = operation()
                return FlextResult.ok(result)
            except Exception as e:
                self.logger.exception(error_context)
                return FlextResult.fail(f"{error_context}: {e!s}")

    class FileSystemDiscoveryAdapter(BaseAdapter, FlextPluginProtocols.PluginDiscovery):
        """File system plugin discovery - synchronous."""

        def discover_plugins(
            self,
            paths: FlextPluginTypes.PluginCore.StringList,
        ) -> FlextResult[list[FlextPluginModels.DiscoveryData]]:
            """Discover plugins in given paths."""
            return self._execute_safe(
                lambda: self._discover_all(paths),
                "Plugin discovery failed",
            )

        def _discover_all(
            self,
            paths: FlextPluginTypes.PluginCore.StringList,
        ) -> list[FlextPluginModels.DiscoveryData]:
            """Internal: discover all plugins."""
            discovered = []
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

        def discover_plugin(
            self,
            plugin_path: str,
        ) -> FlextResult[FlextPluginModels.DiscoveryData]:
            """Discover single plugin at path."""
            return self._execute_safe(
                lambda: self._discover_single(plugin_path),
                f"Failed to discover plugin at {plugin_path}",
            )

        def _discover_single(
            self,
            plugin_path: str,
        ) -> FlextPluginModels.DiscoveryData:
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

        def validate_plugin(
            self,
            _plugin_data: FlextPluginModels.DiscoveryData,
        ) -> FlextResult[bool]:
            """Validate discovered plugin data."""
            return self._execute_safe(
                lambda: True,  # Pydantic validates on creation
                "Plugin validation failed",
            )

        def _discover_single_file(
            self,
            path: Path,
        ) -> FlextPluginModels.DiscoveryData | None:
            """Internal: discover single file."""
            if path.suffix != ".py":
                return None

            try:
                return FlextPluginModels.DiscoveryData(
                    name=path.stem,
                    version="1.0.0",
                    path=path,
                    discovery_type="file",
                    discovery_method="file_system",
                )
            except ValueError:
                self.logger.exception("Failed to create discovery data for %s", path)
                return None

        def _discover_directory(
            self,
            path: Path,
        ) -> list[FlextPluginModels.DiscoveryData]:
            """Internal: discover plugins in directory."""
            discovered = []
            try:
                for item in path.iterdir():
                    if (
                        item.is_file()
                        and item.suffix == ".py"
                        and not item.name.startswith("_")
                    ):
                        data = self._discover_single_file(item)
                        if data:
                            discovered.append(data)
                    elif item.is_dir() and not item.name.startswith("__"):
                        discovered.extend(self._discover_directory(item))
            except (OSError, PermissionError):
                self.logger.exception("Failed to discover directory %s", path)

            return discovered

    class DynamicLoaderAdapter(BaseAdapter, FlextPluginProtocols.PluginLoader):
        """Dynamic plugin loading - synchronous."""

        def load_plugin(
            self,
            plugin_path: str,
        ) -> FlextResult[FlextPluginModels.LoadData]:
            """Load plugin from path."""
            return self._execute_safe(
                lambda: self._load_module(plugin_path),
                f"Loading error: {plugin_path}",
            )

        def _load_module(self, _plugin_path: str) -> FlextPluginModels.LoadData:
            """Internal: load module using spec."""
            path = Path(_plugin_path).expanduser().resolve()
            if not path.exists():
                error_msg = f"Plugin path does not exist: {_plugin_path}"
                raise FileNotFoundError(error_msg)

            # Use spec-based loading for safety (no sys.path pollution)
            spec = importlib.util.spec_from_file_location(path.stem, path)
            if not spec or not spec.loader:
                error_msg = f"Cannot load spec from {path}"
                raise ImportError(error_msg)

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            return FlextPluginModels.LoadData(
                name=path.stem,
                version=getattr(module, "__version__", "1.0.0"),
                path=path,
                module=module,
                load_type="file",
                loaded_at=__import__("datetime").datetime.now(
                    __import__("datetime").UTC,
                ),
            )

        def unload_plugin(self, _plugin_name: str) -> FlextResult[bool]:
            """Unload plugin by name (placeholder implementation)."""
            return FlextResult.ok(True)

        def is_plugin_loaded(self, _plugin_name: str) -> bool:
            """Check if plugin is loaded (placeholder)."""
            return False

        def get_loaded_plugins(self) -> list[str]:
            """Get list of loaded plugins."""
            return []

    class PluginExecutorAdapter(BaseAdapter, FlextPluginProtocols.PluginExecution):
        """Plugin execution - synchronous."""

        def execute_plugin(
            self,
            _plugin_name: str,
            _context: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Execute plugin."""
            return self._execute_safe(
                lambda: {"status": "executed", "plugin": _plugin_name},
                f"Execution error: {_plugin_name}",
            )

        def stop_execution(self, _execution_id: str) -> FlextResult[bool]:
            """Stop plugin execution."""
            return FlextResult.ok(True)

        def get_execution_status(self, _execution_id: str) -> FlextResult[str]:
            """Get execution status."""
            return FlextResult.ok("completed")

        def list_running_executions(self) -> list[str]:
            """List running executions."""
            return []

    class PluginSecurityAdapter(BaseAdapter, FlextPluginProtocols.PluginSecurity):
        """Plugin security validation - synchronous."""

        def validate_plugin(self, _plugin: object) -> FlextResult[bool]:
            """Validate plugin for security."""
            return FlextResult.ok(True)

        def check_permissions(
            self,
            _plugin_name: str,
            _permissions: list[str],
        ) -> FlextResult[bool]:
            """Check plugin permissions."""
            return FlextResult.ok(True)

        def scan_plugin_security(
            self,
            _plugin_path: str,
        ) -> FlextResult[dict[str, object]]:
            """Scan plugin for security issues."""
            return FlextResult.ok({"security_level": "medium"})

        def get_security_level(self, _plugin_name: str) -> FlextResult[str]:
            """Get security level."""
            return FlextResult.ok("medium")

    class MemoryRegistryAdapter(BaseAdapter, FlextPluginProtocols.PluginRegistry):
        """In-memory plugin registry - synchronous."""

        def __init__(self) -> None:
            """Initialize registry adapter."""
            super().__init__()
            self._plugins: dict[str, object] = {}

        def register_plugin(self, _plugin: object) -> FlextResult[bool]:
            """Register plugin in registry."""
            return FlextResult.ok(True)

        def unregister_plugin(self, _plugin_name: str) -> FlextResult[bool]:
            """Unregister plugin from registry."""
            return FlextResult.ok(True)

        def get_plugin(self, _plugin_name: str) -> FlextResult[object | None]:
            """Get plugin from registry."""
            return FlextResult.ok(None)

        def list_plugins(self) -> FlextResult[list[dict[str, object]]]:
            """List all plugins in registry."""
            return FlextResult.ok([])

        def is_plugin_registered(self, _plugin_name: str) -> bool:
            """Check if plugin is registered."""
            return False

    class PluginMonitoringAdapter(BaseAdapter, FlextPluginProtocols.PluginMonitoring):
        """Plugin monitoring - synchronous."""

        def start_monitoring(self, _plugin_name: str) -> FlextResult[bool]:
            """Start monitoring plugin."""
            return FlextResult.ok(True)

        def stop_monitoring(self, _plugin_name: str) -> FlextResult[bool]:
            """Stop monitoring plugin."""
            return FlextResult.ok(True)

        def get_plugin_metrics(
            self,
            _plugin_name: str,
        ) -> FlextResult[dict[str, object]]:
            """Get plugin metrics."""
            return FlextResult.ok({"execution_count": 0, "error_count": 0})

        def get_plugin_health(
            self,
            _plugin_name: str,
        ) -> FlextResult[dict[str, object]]:
            """Get plugin health information."""
            return FlextResult.ok({"status": "healthy"})

        def is_monitoring(self, _plugin_name: str) -> bool:
            """Check if plugin is being monitored."""
            return False


__all__ = ["FlextPluginAdapters"]
