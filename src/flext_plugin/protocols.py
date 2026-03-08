"""FLEXT Plugin Protocols - Synchronous protocol composition with Pydantic models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols, FlextResult

from flext_plugin import FlextPluginModels, t


class FlextPluginProtocols(FlextProtocols):
    """Unified plugin protocols extending FlextProtocols.

    Extends FlextProtocols to inherit all foundation protocols (Result, Service, etc.)
    and adds plugin-specific protocols in the Plugin namespace.

    Architecture:
    - EXTENDS: FlextProtocols (inherits Foundation, Domain, Application, etc.)
    - ADDS: Plugin-specific protocols in Plugin namespace
    - PROVIDES: Root-level alias `p` for convenient access

    Usage:
    from flext_plugin import p

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

            def get_loaded_plugins(self) -> list[str]:
                """Get list of all currently loaded plugin names."""
                ...

            def is_plugin_loaded(self, _plugin_name: str) -> bool:
                """Check if a plugin is currently loaded."""
                ...

            def load_plugin(
                self, _plugin_path: str
            ) -> FlextResult[Mapping[str, t.ContainerValue]]:
                """Load a plugin from the specified path."""
                ...

            def unload_plugin(self, _plugin_name: str) -> FlextResult[bool]:
                """Unload a previously loaded plugin."""
                ...

        @runtime_checkable
        class PluginDiscovery(Protocol):
            """Protocol for plugin discovery operations."""

            def discover_plugin(
                self, _plugin_path: str
            ) -> FlextResult[Mapping[str, t.ContainerValue]]:
                """Discover a single plugin at the specified path."""
                ...

            def discover_plugins(
                self, paths: list[str]
            ) -> FlextResult[list[Mapping[str, t.ContainerValue]]]:
                """Discover plugins at the given paths."""
                ...

            def validate_plugin(
                self, _plugin_data: Mapping[str, t.ContainerValue]
            ) -> FlextResult[bool]:
                """Validate plugin discovery data."""
                ...

        @runtime_checkable
        class PluginRegistry(Protocol):
            """Protocol for plugin registry operations."""

            def get_plugin(
                self, _plugin_name: str
            ) -> FlextResult[t.ContainerValue | None]:
                """Get a registered plugin by name."""
                ...

            def is_plugin_registered(self, _plugin_name: str) -> bool:
                """Check if a plugin is registered."""
                ...

            def list_plugins(self) -> FlextResult[list[Mapping[str, t.ContainerValue]]]:
                """List all registered plugins."""
                ...

            def register_plugin(self, _plugin: t.ContainerValue) -> FlextResult[bool]:
                """Register a plugin."""
                ...

            def unregister_plugin(self, _plugin_name: str) -> FlextResult[bool]:
                """Unregister a plugin."""
                ...

        @runtime_checkable
        class PluginExecution(Protocol):
            """Protocol for plugin execution operations."""

            def execute_plugin(
                self, _plugin_name: str, _context: Mapping[str, t.ContainerValue]
            ) -> FlextResult[Mapping[str, t.ContainerValue]]:
                """Execute a plugin with the given context."""
                ...

            def get_execution_status(self, _execution_id: str) -> FlextResult[str]:
                """Get the status of an execution."""
                ...

            def list_running_executions(self) -> list[str]:
                """List all currently running execution IDs."""
                ...

            def stop_execution(self, _execution_id: str) -> FlextResult[bool]:
                """Stop a running execution."""
                ...

        @runtime_checkable
        class PluginSecurity(Protocol):
            """Protocol for plugin security operations."""

            def check_permissions(
                self, _plugin_name: str, _permissions: list[str]
            ) -> FlextResult[bool]:
                """Check if plugin has specified permissions."""
                ...

            def get_security_level(self, _plugin_name: str) -> FlextResult[str]:
                """Get security level of a plugin."""
                ...

            def scan_plugin_security(
                self, _plugin_path: str
            ) -> FlextResult[Mapping[str, t.ContainerValue]]:
                """Scan plugin for security vulnerabilities."""
                ...

            def validate_plugin_security(
                self, _plugin: t.ContainerValue
            ) -> FlextResult[bool]:
                """Validate plugin security compliance."""
                ...

        @runtime_checkable
        class PluginHotReload(Protocol):
            """Protocol for hot reload operations."""

            def get_watched_paths(self) -> list[str]:
                """Get list of currently watched paths."""
                ...

            def is_watching(self) -> bool:
                """Check if currently watching for changes."""
                ...

            def reload_plugin(self, _plugin_name: str) -> FlextResult[bool]:
                """Reload a plugin."""
                ...

            def start_watching(self, paths: list[str]) -> FlextResult[bool]:
                """Start watching paths for plugin changes."""
                ...

            def stop_watching(self) -> FlextResult[bool]:
                """Stop watching for plugin changes."""
                ...

        @runtime_checkable
        class PluginMonitoring(Protocol):
            """Protocol for plugin monitoring operations."""

            def get_plugin_health(
                self, _plugin_name: str
            ) -> FlextResult[Mapping[str, t.ContainerValue]]:
                """Get health status of a plugin."""
                ...

            def get_plugin_metrics(
                self, _plugin_name: str
            ) -> FlextResult[Mapping[str, t.ContainerValue]]:
                """Get metrics for a plugin."""
                ...

            def is_monitoring(self, _plugin_name: str) -> bool:
                """Check if a plugin is being monitored."""
                ...

            def start_monitoring(self, _plugin_name: str) -> FlextResult[bool]:
                """Start monitoring a plugin."""
                ...

            def stop_monitoring(self, _plugin_name: str) -> FlextResult[bool]:
                """Stop monitoring a plugin."""
                ...

        @runtime_checkable
        class PluginConfiguration(Protocol):
            """Protocol for plugin configuration operations."""

            def get_default_config(self, plugin_type: str) -> FlextResult[t.JsonDict]:
                """Get default configuration for a plugin type."""
                ...

            def load_config(self, _plugin_name: str) -> FlextResult[t.JsonDict]:
                """Load configuration for a plugin."""
                ...

            def save_config(
                self, _plugin_name: str, config: t.JsonDict
            ) -> FlextResult[bool]:
                """Save configuration for a plugin."""
                ...

            def validate_config(self, config: t.JsonDict) -> FlextResult[bool]:
                """Validate plugin configuration."""
                ...

        @runtime_checkable
        class PluginLifecycle(Protocol):
            """Protocol for plugin lifecycle operations."""

            def activate_plugin(self, _plugin_name: str) -> FlextResult[bool]:
                """Activate a plugin."""
                ...

            def deactivate_plugin(self, _plugin_name: str) -> FlextResult[bool]:
                """Deactivate a plugin."""
                ...

            def destroy_plugin(self, _plugin_name: str) -> FlextResult[bool]:
                """Destroy a plugin."""
                ...

            def get_plugin_status(self, _plugin_name: str) -> FlextResult[str]:
                """Get the status of a plugin."""
                ...

            def initialize_plugin(self, _plugin_name: str) -> FlextResult[bool]:
                """Initialize a plugin."""
                ...

            def list_plugin_statuses(self) -> FlextResult[Mapping[str, str]]:
                """Get status of all plugins."""
                ...

        @runtime_checkable
        class PluginValidation(Protocol):
            """Protocol for plugin validation operations."""

            def validate_plugin_compatibility(
                self, _plugin_name: str
            ) -> FlextResult[bool]:
                """Validate plugin compatibility."""
                ...

            def validate_plugin_dependencies(
                self, _plugin_name: str
            ) -> FlextResult[bool]:
                """Validate plugin dependencies."""
                ...

            def validate_plugin_permissions(
                self, _plugin_name: str
            ) -> FlextResult[bool]:
                """Validate plugin permissions."""
                ...

            def validate_plugin_structure(
                self, _plugin_data: t.JsonDict
            ) -> FlextResult[bool]:
                """Validate plugin structure."""
                ...

        @runtime_checkable
        class PluginStorage(Protocol):
            """Protocol for plugin storage operations."""

            def delete_plugin(self, _plugin_name: str) -> FlextResult[bool]:
                """Delete stored plugin."""
                ...

            def list_stored_plugins(self) -> FlextResult[list[str]]:
                """List all stored plugin names."""
                ...

            def plugin_exists(self, _plugin_name: str) -> bool:
                """Check if plugin is stored."""
                ...

            def retrieve_plugin(
                self, _plugin_name: str
            ) -> FlextResult[t.JsonDict | None]:
                """Retrieve stored plugin data."""
                ...

            def store_plugin(self, _plugin_data: t.JsonDict) -> FlextResult[bool]:
                """Store plugin data."""
                ...

        @runtime_checkable
        class LoggerProtocol(Protocol):
            """Protocol for logging operations."""

            def critical(
                self, message: str, *args: t.ContainerValue, **kwargs: t.ContainerValue
            ) -> None:
                """Log critical message."""
                ...

            def debug(
                self, message: str, *args: t.ContainerValue, **kwargs: t.ContainerValue
            ) -> None:
                """Log debug message."""
                ...

            def error(
                self, message: str, *args: t.ContainerValue, **kwargs: t.ContainerValue
            ) -> None:
                """Log error message."""
                ...

            def info(
                self, message: str, *args: t.ContainerValue, **kwargs: t.ContainerValue
            ) -> None:
                """Log info message."""
                ...

            def warning(
                self, message: str, *args: t.ContainerValue, **kwargs: t.ContainerValue
            ) -> None:
                """Log warning message."""
                ...

        @runtime_checkable
        class PluginLoaderProtocol(Protocol):
            """Protocol for plugin loader interface."""

            def load_plugin(
                self, plugin_path: str | t.ContainerValue
            ) -> FlextResult[t.ContainerValue]:
                """Load plugin from path."""
                ...

        @runtime_checkable
        class PluginRegistryProtocol(Protocol):
            """Protocol for plugin registry interface."""

            def get_plugin(self, plugin_name: str) -> FlextResult[t.ContainerValue]:
                """Get plugin by name."""
                ...

            def register(self, plugin: t.ContainerValue) -> FlextResult[None]:
                """Register a plugin."""
                ...

        @runtime_checkable
        class DiscoveryStrategyProtocol(Protocol):
            """Strategy protocol for plugin discovery."""

            def discover(
                self, paths: list[str]
            ) -> FlextResult[list[FlextPluginModels.Plugin.DiscoveryData]]:
                """Discover plugins using this strategy."""
                ...


p = FlextPluginProtocols
__all__ = ["FlextPluginProtocols", "p"]
