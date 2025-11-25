"""FLEXT Plugin Protocols - Synchronous protocol composition with Pydantic models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

# Protocol methods inherit documentation from the Protocol class docstring

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from flext_core import FlextResult

if TYPE_CHECKING:
    from flext_plugin.models import FlextPluginModels


class FlextPluginProtocols:
    """Synchronous plugin protocols with Pydantic model composition."""

    # Core plugin operations
    class PluginLoader(Protocol):
        """Protocol for plugin loading operations."""

        def load_plugin(
            self, _plugin_path: str
        ) -> FlextResult[FlextPluginModels.LoadData]: ...

        def unload_plugin(self, _plugin_name: str) -> FlextResult[bool]: ...

        def is_plugin_loaded(self, _plugin_name: str) -> bool: ...

        def get_loaded_plugins(self) -> list[str]: ...

    class PluginDiscovery(Protocol):
        """Protocol for plugin discovery operations."""

        def discover_plugins(
            self, paths: list[str]
        ) -> FlextResult[list[FlextPluginModels.DiscoveryData]]: ...

        def discover_plugin(
            self, _plugin_path: str
        ) -> FlextResult[FlextPluginModels.DiscoveryData]: ...

        def validate_plugin(
            self, _plugin_data: FlextPluginModels.DiscoveryData
        ) -> FlextResult[bool]: ...

    class PluginRegistry(Protocol):
        """Protocol for plugin registry operations."""

        def register_plugin(self, _plugin: object) -> FlextResult[bool]: ...

        def unregister_plugin(self, _plugin_name: str) -> FlextResult[bool]: ...

        def get_plugin(self, _plugin_name: str) -> FlextResult[object | None]: ...

        def list_plugins(self) -> FlextResult[list[dict[str, object]]]: ...

        def is_plugin_registered(self, _plugin_name: str) -> bool: ...

    class PluginExecution(Protocol):
        """Protocol for plugin execution operations."""

        def execute_plugin(
            self, _plugin_name: str, _context: dict[str, object]
        ) -> FlextResult[dict[str, object]]: ...

        def stop_execution(self, _execution_id: str) -> FlextResult[bool]: ...

        def get_execution_status(self, _execution_id: str) -> FlextResult[str]: ...

        def list_running_executions(self) -> list[str]: ...

    class PluginSecurity(Protocol):
        """Protocol for plugin security operations."""

        def validate_plugin(self, _plugin: object) -> FlextResult[bool]: ...

        def check_permissions(
            self, _plugin_name: str, _permissions: list[str]
        ) -> FlextResult[bool]: ...

        def scan_plugin_security(
            self, _plugin_path: str
        ) -> FlextResult[dict[str, object]]: ...

        def get_security_level(self, _plugin_name: str) -> FlextResult[str]: ...

    class PluginHotReload(Protocol):
        """Protocol for hot reload operations."""

        def start_watching(self, paths: list[str]) -> FlextResult[bool]: ...

        def stop_watching(self) -> FlextResult[bool]: ...

        def reload_plugin(self, _plugin_name: str) -> FlextResult[bool]: ...

        def is_watching(self) -> bool: ...

        def get_watched_paths(self) -> list[str]: ...

    class PluginMonitoring(Protocol):
        """Protocol for plugin monitoring operations."""

        def start_monitoring(self, _plugin_name: str) -> FlextResult[bool]: ...

        def stop_monitoring(self, _plugin_name: str) -> FlextResult[bool]: ...

        def get_plugin_metrics(
            self, _plugin_name: str
        ) -> FlextResult[dict[str, object]]: ...

        def get_plugin_health(
            self, _plugin_name: str
        ) -> FlextResult[dict[str, object]]: ...

        def is_monitoring(self, _plugin_name: str) -> bool: ...

    class PluginConfiguration(Protocol):
        """Protocol for plugin configuration operations."""

        def load_config(self, _plugin_name: str) -> FlextResult[dict[str, object]]: ...

        def save_config(
            self, _plugin_name: str, config: dict[str, object]
        ) -> FlextResult[bool]: ...

        def validate_config(self, config: dict[str, object]) -> FlextResult[bool]: ...

        def get_default_config(
            self, plugin_type: str
        ) -> FlextResult[dict[str, object]]: ...

    class PluginLifecycle(Protocol):
        """Protocol for plugin lifecycle operations."""

        def initialize_plugin(self, _plugin_name: str) -> FlextResult[bool]: ...

        def activate_plugin(self, _plugin_name: str) -> FlextResult[bool]: ...

        def deactivate_plugin(self, _plugin_name: str) -> FlextResult[bool]: ...

        def destroy_plugin(self, _plugin_name: str) -> FlextResult[bool]: ...

        def get_plugin_status(self, _plugin_name: str) -> FlextResult[str]: ...

        def list_plugin_statuses(self) -> FlextResult[dict[str, str]]: ...

    class PluginValidation(Protocol):
        """Protocol for plugin validation operations."""

        def validate_plugin_structure(
            self, _plugin_data: dict[str, object]
        ) -> FlextResult[bool]: ...

        def validate_plugin_dependencies(
            self, _plugin_name: str
        ) -> FlextResult[bool]: ...

        def validate_plugin_permissions(
            self, _plugin_name: str
        ) -> FlextResult[bool]: ...

        def validate_plugin_compatibility(
            self, _plugin_name: str
        ) -> FlextResult[bool]: ...

    class PluginStorage(Protocol):
        """Protocol for plugin storage operations."""

        def store_plugin(
            self, _plugin_data: dict[str, object]
        ) -> FlextResult[bool]: ...

        def retrieve_plugin(
            self, _plugin_name: str
        ) -> FlextResult[dict[str, object] | None]: ...

        def delete_plugin(self, _plugin_name: str) -> FlextResult[bool]: ...

        def list_stored_plugins(self) -> FlextResult[list[str]]: ...

        def plugin_exists(self, _plugin_name: str) -> bool: ...

    class LoggerProtocol(Protocol):
        """Protocol for logging operations."""

        def critical(self, message: str, *args: object, **kwargs: object) -> None: ...

        def error(self, message: str, *args: object, **kwargs: object) -> None: ...

        def warning(self, message: str, *args: object, **kwargs: object) -> None: ...

        def info(self, message: str, *args: object, **kwargs: object) -> None: ...

        def debug(self, message: str, *args: object, **kwargs: object) -> None: ...


__all__ = ["FlextPluginProtocols"]
