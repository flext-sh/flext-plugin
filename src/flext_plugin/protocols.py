"""FLEXT Plugin Protocols - Synchronous protocol composition with Pydantic models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols
from flext_core.result import FlextResult

from flext_plugin.models import FlextPluginModels
from flext_plugin.typings import t


class FlextPluginProtocols(FlextProtocols):
    """Unified plugin protocols extending FlextProtocols.

    Extends FlextProtocols to inherit all foundation protocols (Result, Service, etc.)
    and adds plugin-specific protocols in the Plugin namespace.

    Architecture:
    - EXTENDS: FlextProtocols (inherits Foundation, Domain, Application, etc.)
    - ADDS: Plugin-specific protocols in Plugin namespace
    - PROVIDES: Root-level alias `p` for convenient access

    Usage:
    from flext_plugin.protocols import p

    # Foundation protocols (inherited)
    result: p.Result[str]
    service: p.Service[str]

    # Plugin-specific protocols
    loader: p.Plugin.PluginLoader
    discovery: p.Plugin.PluginDiscovery
    """

    class Plugin:
        """Plugin domain-specific protocols."""

        @runtime_checkable
        class PluginLoader(Protocol):
            """Protocol for plugin loading operations."""

            def load_plugin(
                self,
                _plugin_path: str,
            ) -> FlextResult[Mapping[str, t.GeneralValueType]]:
                """Load a plugin from the specified path."""
                # INTERFACE
                # INTERFACE
                ...

            def unload_plugin(self, _plugin_name: str) -> FlextResult[bool]:
                """Unload a previously loaded plugin."""
                # INTERFACE
                # INTERFACE
                ...

            def is_plugin_loaded(self, _plugin_name: str) -> bool:
                """Check if a plugin is currently loaded."""
                # INTERFACE
                # INTERFACE
                ...

            def get_loaded_plugins(self) -> list[str]:
                """Get list of all currently loaded plugin names."""
                # INTERFACE
                ...

        @runtime_checkable
        class PluginDiscovery(Protocol):
            """Protocol for plugin discovery operations."""

            def discover_plugins(
                self,
                paths: list[str],
            ) -> FlextResult[list[Mapping[str, t.GeneralValueType]]]:
                """Discover plugins at the given paths."""
                # INTERFACE
                ...

            def discover_plugin(
                self,
                _plugin_path: str,
            ) -> FlextResult[Mapping[str, t.GeneralValueType]]:
                """Discover a single plugin at the specified path."""
                # INTERFACE
                ...

            def validate_plugin(
                self,
                _plugin_data: Mapping[str, t.GeneralValueType],
            ) -> FlextResult[bool]:
                """Validate plugin discovery data."""
                # INTERFACE
                ...

        @runtime_checkable
        class PluginRegistry(Protocol):
            """Protocol for plugin registry operations."""

            def register_plugin(self, _plugin: t.GeneralValueType) -> FlextResult[bool]:
                """Register a plugin."""
                # INTERFACE
                ...

            def unregister_plugin(self, _plugin_name: str) -> FlextResult[bool]:
                """Unregister a plugin."""
                # INTERFACE
                ...

            def get_plugin(
                self, _plugin_name: str
            ) -> FlextResult[t.GeneralValueType | None]:
                """Get a registered plugin by name."""
                # INTERFACE
                ...

            def list_plugins(
                self,
            ) -> FlextResult[list[Mapping[str, t.GeneralValueType]]]:
                """List all registered plugins."""
                # INTERFACE
                ...

            def is_plugin_registered(self, _plugin_name: str) -> bool:
                """Check if a plugin is registered."""
                # INTERFACE
                ...

        @runtime_checkable
        class PluginExecution(Protocol):
            """Protocol for plugin execution operations."""

            def execute_plugin(
                self,
                _plugin_name: str,
                _context: Mapping[str, t.GeneralValueType],
            ) -> FlextResult[Mapping[str, t.GeneralValueType]]:
                """Execute a plugin with the given context."""
                # INTERFACE
                ...

            def stop_execution(self, _execution_id: str) -> FlextResult[bool]:
                """Stop a running execution."""
                # INTERFACE
                ...

            def get_execution_status(self, _execution_id: str) -> FlextResult[str]:
                """Get the status of an execution."""
                # INTERFACE
                ...

            def list_running_executions(self) -> list[str]:
                """List all currently running execution IDs."""
                # INTERFACE
                ...

        @runtime_checkable
        class PluginSecurity(Protocol):
            """Protocol for plugin security operations."""

            def validate_plugin_security(
                self, _plugin: t.GeneralValueType
            ) -> FlextResult[bool]:
                """Validate plugin security compliance."""
                # INTERFACE
                ...

            def check_permissions(
                self,
                _plugin_name: str,
                _permissions: list[str],
            ) -> FlextResult[bool]:
                """Check if plugin has specified permissions."""
                # INTERFACE
                ...

            def scan_plugin_security(
                self,
                _plugin_path: str,
            ) -> FlextResult[Mapping[str, t.GeneralValueType]]:
                """Scan plugin for security vulnerabilities."""
                # INTERFACE
                ...

            def get_security_level(self, _plugin_name: str) -> FlextResult[str]:
                """Get security level of a plugin."""
                # INTERFACE
                ...

        @runtime_checkable
        class PluginHotReload(Protocol):
            """Protocol for hot reload operations."""

            def start_watching(self, paths: list[str]) -> FlextResult[bool]:
                """Start watching paths for plugin changes."""
                # INTERFACE
                ...

            def stop_watching(self) -> FlextResult[bool]:
                """Stop watching for plugin changes."""
                # INTERFACE
                ...

            def reload_plugin(self, _plugin_name: str) -> FlextResult[bool]:
                """Reload a plugin."""
                # INTERFACE
                ...

            def is_watching(self) -> bool:
                """Check if currently watching for changes."""
                # INTERFACE
                ...

            def get_watched_paths(self) -> list[str]:
                """Get list of currently watched paths."""
                # INTERFACE
                ...

        @runtime_checkable
        class PluginMonitoring(Protocol):
            """Protocol for plugin monitoring operations."""

            def start_monitoring(self, _plugin_name: str) -> FlextResult[bool]:
                """Start monitoring a plugin."""
                # INTERFACE
                ...

            def stop_monitoring(self, _plugin_name: str) -> FlextResult[bool]:
                """Stop monitoring a plugin."""
                # INTERFACE
                ...

            def get_plugin_metrics(
                self,
                _plugin_name: str,
            ) -> FlextResult[Mapping[str, t.GeneralValueType]]:
                """Get metrics for a plugin."""
                # INTERFACE
                ...

            def get_plugin_health(
                self,
                _plugin_name: str,
            ) -> FlextResult[Mapping[str, t.GeneralValueType]]:
                """Get health status of a plugin."""
                # INTERFACE
                ...

            def is_monitoring(self, _plugin_name: str) -> bool:
                """Check if a plugin is being monitored."""
                # INTERFACE
                ...

        @runtime_checkable
        class PluginConfiguration(Protocol):
            """Protocol for plugin configuration operations."""

            def load_config(self, _plugin_name: str) -> FlextResult[t.JsonDict]:
                """Load configuration for a plugin."""
                # INTERFACE
                ...

            def save_config(
                self,
                _plugin_name: str,
                config: t.JsonDict,
            ) -> FlextResult[bool]:
                """Save configuration for a plugin."""
                # INTERFACE
                ...

            def validate_config(self, config: t.JsonDict) -> FlextResult[bool]:
                """Validate plugin configuration."""
                # INTERFACE
                ...

            def get_default_config(
                self,
                plugin_type: str,
            ) -> FlextResult[t.JsonDict]:
                """Get default configuration for a plugin type."""
                # INTERFACE
                ...

        @runtime_checkable
        class PluginLifecycle(Protocol):
            """Protocol for plugin lifecycle operations."""

            def initialize_plugin(self, _plugin_name: str) -> FlextResult[bool]:
                """Initialize a plugin."""
                # INTERFACE
                ...

            def activate_plugin(self, _plugin_name: str) -> FlextResult[bool]:
                """Activate a plugin."""
                # INTERFACE
                ...

            def deactivate_plugin(self, _plugin_name: str) -> FlextResult[bool]:
                """Deactivate a plugin."""
                # INTERFACE
                ...

            def destroy_plugin(self, _plugin_name: str) -> FlextResult[bool]:
                """Destroy a plugin."""
                # INTERFACE
                ...

            def get_plugin_status(self, _plugin_name: str) -> FlextResult[str]:
                """Get the status of a plugin."""
                # INTERFACE
                ...

            def list_plugin_statuses(self) -> FlextResult[Mapping[str, str]]:
                """Get status of all plugins."""
                # INTERFACE
                ...

        @runtime_checkable
        class PluginValidation(Protocol):
            """Protocol for plugin validation operations."""

            def validate_plugin_structure(
                self,
                _plugin_data: t.JsonDict,
            ) -> FlextResult[bool]:
                """Validate plugin structure."""
                # INTERFACE
                ...

            def validate_plugin_dependencies(
                self,
                _plugin_name: str,
            ) -> FlextResult[bool]:
                """Validate plugin dependencies."""
                # INTERFACE
                ...

            def validate_plugin_permissions(
                self,
                _plugin_name: str,
            ) -> FlextResult[bool]:
                """Validate plugin permissions."""
                # INTERFACE
                ...

            def validate_plugin_compatibility(
                self,
                _plugin_name: str,
            ) -> FlextResult[bool]:
                """Validate plugin compatibility."""
                # INTERFACE
                ...

        @runtime_checkable
        class PluginStorage(Protocol):
            """Protocol for plugin storage operations."""

            def store_plugin(
                self,
                _plugin_data: t.JsonDict,
            ) -> FlextResult[bool]:
                """Store plugin data."""
                # INTERFACE
                ...

            def retrieve_plugin(
                self,
                _plugin_name: str,
            ) -> FlextResult[t.JsonDict | None]:
                """Retrieve stored plugin data."""
                # INTERFACE
                ...

            def delete_plugin(self, _plugin_name: str) -> FlextResult[bool]:
                """Delete stored plugin."""
                # INTERFACE
                ...

            def list_stored_plugins(self) -> FlextResult[list[str]]:
                """List all stored plugin names."""
                # INTERFACE
                ...

            def plugin_exists(self, _plugin_name: str) -> bool:
                """Check if plugin is stored."""
                # INTERFACE
                ...

        @runtime_checkable
        class LoggerProtocol(Protocol):
            """Protocol for logging operations."""

            def critical(
                self,
                message: str,
                *args: t.GeneralValueType,
                **kwargs: t.GeneralValueType,
            ) -> None:
                """Log critical message."""
                # INTERFACE
                ...

            def error(
                self,
                message: str,
                *args: t.GeneralValueType,
                **kwargs: t.GeneralValueType,
            ) -> None:
                """Log error message."""
                # INTERFACE
                ...

            def warning(
                self,
                message: str,
                *args: t.GeneralValueType,
                **kwargs: t.GeneralValueType,
            ) -> None:
                """Log warning message."""
                # INTERFACE
                ...

            def info(
                self,
                message: str,
                *args: t.GeneralValueType,
                **kwargs: t.GeneralValueType,
            ) -> None:
                """Log info message."""
                # INTERFACE
                ...

            def debug(
                self,
                message: str,
                *args: t.GeneralValueType,
                **kwargs: t.GeneralValueType,
            ) -> None:
                """Log debug message."""
                # INTERFACE
                ...

        # =====================================================================
        # DUCK TYPING PROTOCOLS
        # =====================================================================
        # Protocols for duck typing common plugin patterns.

        @runtime_checkable
        class PluginLoaderProtocol(Protocol):
            """Protocol for plugin loader interface."""

            def load_plugin(
                self, plugin_path: str | t.GeneralValueType
            ) -> FlextResult[t.GeneralValueType]:
                """Load plugin from path."""
                # INTERFACE
                ...

        @runtime_checkable
        class PluginRegistryProtocol(Protocol):
            """Protocol for plugin registry interface."""

            def register(self, plugin: t.GeneralValueType) -> FlextResult[None]:
                """Register a plugin."""
                # INTERFACE
                ...

            def get_plugin(self, plugin_name: str) -> FlextResult[t.GeneralValueType]:
                """Get plugin by name."""
                # INTERFACE
                ...

        @runtime_checkable
        class DiscoveryStrategyProtocol(Protocol):
            """Strategy protocol for plugin discovery."""

            def discover(
                self,
                paths: list[str],
            ) -> FlextResult[list[FlextPluginModels.Plugin.DiscoveryData]]:
                """Discover plugins using this strategy."""
                # INTERFACE
                ...


p = FlextPluginProtocols

__all__ = [
    "FlextPluginProtocols",
    "p",
]
