"""FLEXT Plugin Protocols - Synchronous protocol composition with Pydantic models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_core import FlextProtocols
from flext_plugin import t

if TYPE_CHECKING:
    from flext_plugin import m


class FlextPluginProtocols(FlextProtocols):
    """Unified plugin protocols extending FlextProtocols.

    Extends FlextProtocols to inherit all foundation protocols (Result, Service, etc.)
    and adds plugin-specific protocols in the Plugin namespace.

    Architecture:
    - EXTENDS: FlextProtocols (inherits Foundation, Domain, Application, etc.)
    - ADDS: Plugin-specific protocols in Plugin namespace
    - PROVIDES: Root-level alias `p` for convenient access

    Usage:
    from flext_core import p

    # Foundation protocols (inherited)
    result: p.Result[str]
    service: p.Service[str]

    # Plugin-specific protocols
    loader: p.Plugin.PluginLoader
    discovery: p.Plugin.PluginDiscovery
    """

    @runtime_checkable
    class Plugin(Protocol):
        """Plugin domain-specific protocols."""

        @runtime_checkable
        class PluginLoader(Protocol):
            """Protocol for plugin loading operations."""

            def get_loaded_plugins(self) -> t.StrSequence:
                """Get list of all currently loaded plugin names."""
                ...

            def plugin_loaded(self, plugin_name: str) -> bool:
                """Check if a plugin is currently loaded."""
                ...

            def load_plugin(
                self,
                plugin_path: str,
            ) -> p.Result[t.RecursiveContainerMapping]:
                """Load a plugin from the specified path."""
                ...

            def unload_plugin(self, plugin_name: str) -> p.Result[bool]:
                """Unload a previously loaded plugin."""
                ...

        @runtime_checkable
        class PluginDiscovery(Protocol):
            """Protocol for plugin discovery operations."""

            def discover_plugin(
                self,
                _plugin_path: str,
            ) -> p.Result[t.RecursiveContainerMapping]:
                """Discover a single plugin at the specified path."""
                ...

            def discover_plugins(
                self,
                paths: t.StrSequence,
            ) -> p.Result[Sequence[t.RecursiveContainerMapping]]:
                """Discover plugins at the given paths."""
                ...

            def validate_plugin(
                self,
                _plugin_data: t.RecursiveContainerMapping,
            ) -> p.Result[bool]:
                """Validate plugin discovery data."""
                ...

            def validate_plugin_security(
                self, _plugin: t.RecursiveContainer
            ) -> p.Result[bool]:
                """Validate plugin for security."""
                ...

        @runtime_checkable
        class PluginRegistry(Protocol):
            """Protocol for plugin registry operations."""

            def fetch_plugin(
                self, plugin_name: str
            ) -> p.Result[t.RecursiveContainer | None]:
                """Fetch a registered plugin by name."""
                ...

            def plugin_registered(self, plugin_name: str) -> bool:
                """Check if a plugin is registered."""
                ...

            def list_plugins(self) -> p.Result[Sequence[t.RecursiveContainerMapping]]:
                """List all registered plugins."""
                ...

            def register_plugin(
                self,
                _plugin: m.Plugin.Plugin | t.RecursiveContainer,
            ) -> p.Result[bool]:
                """Register a plugin."""
                ...

            def register(
                self, plugin: m.Plugin.Plugin | t.RecursiveContainer
            ) -> p.Result[None]:
                """Register a plugin with normalized API."""
                ...

            def unregister_plugin(self, plugin_name: str) -> p.Result[bool]:
                """Unregister a plugin."""
                ...

        @runtime_checkable
        class PluginExecution(Protocol):
            """Protocol for plugin execution operations."""

            def execute_plugin(
                self,
                _plugin_name: str,
                _context: t.RecursiveContainerMapping,
            ) -> p.Result[t.RecursiveContainerMapping]:
                """Execute a plugin with the given context."""
                ...

            def get_execution_status(self, _execution_id: str) -> p.Result[str]:
                """Get the status of an execution."""
                ...

            def list_running_executions(self) -> t.StrSequence:
                """List all currently running execution IDs."""
                ...

            def stop_execution(self, _execution_id: str) -> p.Result[bool]:
                """Stop a running execution."""
                ...

        @runtime_checkable
        class PluginSecurity(Protocol):
            """Protocol for plugin security operations."""

            def check_permissions(
                self,
                _plugin_name: str,
                _permissions: t.StrSequence,
            ) -> p.Result[bool]:
                """Check if plugin has specified permissions."""
                ...

            def get_security_level(self, _plugin_name: str) -> p.Result[str]:
                """Get security level of a plugin."""
                ...

            def scan_plugin_security(
                self,
                _plugin_path: str,
            ) -> p.Result[t.RecursiveContainerMapping]:
                """Scan plugin for security vulnerabilities."""
                ...

            def validate_plugin_security(
                self, _plugin: t.RecursiveContainer
            ) -> p.Result[bool]:
                """Validate plugin security compliance."""
                ...

        @runtime_checkable
        class PluginHotReload(Protocol):
            """Protocol for hot reload operations."""

            def get_watched_paths(self) -> t.StrSequence:
                """Get list of currently watched paths."""
                ...

            def watching(self) -> bool:
                """Check if currently watching for changes."""
                ...

            def reload_plugin(self, _plugin_name: str) -> p.Result[bool]:
                """Reload a plugin."""
                ...

            def start_watching(self, paths: t.StrSequence) -> p.Result[bool]:
                """Start watching paths for plugin changes."""
                ...

            def stop_watching(self) -> p.Result[bool]:
                """Stop watching for plugin changes."""
                ...

        @runtime_checkable
        class PluginMonitoring(Protocol):
            """Protocol for plugin monitoring operations."""

            def fetch_plugin_health(
                self,
                _plugin_name: str,
            ) -> p.Result[t.RecursiveContainerMapping]:
                """Get health status of a plugin."""
                ...

            def fetch_plugin_metrics(
                self,
                _plugin_name: str,
            ) -> p.Result[t.RecursiveContainerMapping]:
                """Get metrics for a plugin."""
                ...

            def monitoring(self, _plugin_name: str) -> bool:
                """Check if a plugin is being monitored."""
                ...

            def start_monitoring(self, _plugin_name: str) -> p.Result[bool]:
                """Start monitoring a plugin."""
                ...

            def stop_monitoring(self, _plugin_name: str) -> p.Result[bool]:
                """Stop monitoring a plugin."""
                ...

        @runtime_checkable
        class PluginConfiguration(Protocol):
            """Protocol for plugin configuration operations."""

            def fetch_default_config(
                self, plugin_type: str
            ) -> p.Result[t.RecursiveContainer]:
                """Get default configuration for a plugin type."""
                ...

            def load_config(self, _plugin_name: str) -> p.Result[t.RecursiveContainer]:
                """Load configuration for a plugin."""
                ...

            def save_config(
                self,
                _plugin_name: str,
                settings: t.RecursiveContainer,
            ) -> p.Result[bool]:
                """Save configuration for a plugin."""
                ...

            def validate_config(self, settings: t.RecursiveContainer) -> p.Result[bool]:
                """Validate plugin configuration."""
                ...

        @runtime_checkable
        class PluginLifecycle(Protocol):
            """Protocol for plugin lifecycle operations."""

            def activate_plugin(self, _plugin_name: str) -> p.Result[bool]:
                """Activate a plugin."""
                ...

            def deactivate_plugin(self, _plugin_name: str) -> p.Result[bool]:
                """Deactivate a plugin."""
                ...

            def destroy_plugin(self, _plugin_name: str) -> p.Result[bool]:
                """Destroy a plugin."""
                ...

            def fetch_plugin_status(self, _plugin_name: str) -> p.Result[str]:
                """Fetch the status of a plugin."""
                ...

            def initialize_plugin(self, _plugin_name: str) -> p.Result[bool]:
                """Initialize a plugin."""
                ...

            def list_plugin_statuses(self) -> p.Result[t.StrMapping]:
                """Get status of all plugins."""
                ...

        @runtime_checkable
        class PluginValidation(Protocol):
            """Protocol for plugin validation operations."""

            def validate_plugin_compatibility(
                self, _plugin_name: str
            ) -> p.Result[bool]:
                """Validate plugin compatibility."""
                ...

            def validate_plugin_dependencies(self, _plugin_name: str) -> p.Result[bool]:
                """Validate plugin dependencies."""
                ...

            def validate_plugin_permissions(self, _plugin_name: str) -> p.Result[bool]:
                """Validate plugin permissions."""
                ...

            def validate_plugin_structure(
                self,
                _plugin_data: t.RecursiveContainer,
            ) -> p.Result[bool]:
                """Validate plugin structure."""
                ...

        @runtime_checkable
        class PluginStorage(Protocol):
            """Protocol for plugin storage operations."""

            def delete_plugin(self, _plugin_name: str) -> p.Result[bool]:
                """Delete stored plugin."""
                ...

            def list_stored_plugins(self) -> p.Result[t.StrSequence]:
                """List all stored plugin names."""
                ...

            def plugin_exists(self, _plugin_name: str) -> bool:
                """Check if plugin is stored."""
                ...

            def retrieve_plugin(
                self, _plugin_name: str
            ) -> p.Result[t.ContainerValue | None]:
                """Retrieve stored plugin data."""
                ...

            def store_plugin(
                self, _plugin_data: t.RecursiveContainer
            ) -> p.Result[bool]:
                """Store plugin data."""
                ...

        @runtime_checkable
        class Logger(Protocol):
            """Protocol for logging operations."""

            def critical(
                self,
                message: str,
                *args: t.RecursiveContainer,
                **kwargs: t.Scalar,
            ) -> None:
                """Log critical message."""
                ...

            def debug(
                self,
                message: str,
                *args: t.RecursiveContainer,
                **kwargs: t.Scalar,
            ) -> None:
                """Log debug message."""
                ...

            def error(
                self,
                message: str,
                *args: t.RecursiveContainer,
                **kwargs: t.Scalar,
            ) -> None:
                """Log error message."""
                ...

            def info(
                self,
                message: str,
                *args: t.RecursiveContainer,
                **kwargs: t.Scalar,
            ) -> None:
                """Log info message."""
                ...

            def warning(
                self,
                message: str,
                *args: t.RecursiveContainer,
                **kwargs: t.Scalar,
            ) -> None:
                """Log warning message."""
                ...

        @runtime_checkable
        class DiscoveryStrategy(Protocol):
            """Strategy protocol for plugin discovery."""

            def discover(
                self,
                paths: t.StrSequence,
            ) -> p.Result[Sequence[m.Plugin.DiscoveryData]]:
                """Discover plugins using this strategy."""
                ...


p = FlextPluginProtocols

__all__: list[str] = ["FlextPluginProtocols", "p"]
