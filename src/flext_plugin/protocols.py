"""FLEXT Plugin Protocols - Synchronous protocol composition with Pydantic models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    Sequence,
)
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

if TYPE_CHECKING:
    from flext_plugin import FlextPluginModels, FlextPluginTypes


class FlextPluginProtocols(FlextCliProtocols):
    """Unified plugin protocols extending FlextCliProtocols.

    Extends p to inherit all foundation protocols (Result, Service, etc.)
    and adds plugin-specific protocols in the Plugin namespace.

    Architecture:
    - EXTENDS: FlextCliProtocols (inherits Foundation, Domain, Application, etc.)
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

            def get_loaded_plugins(self) -> FlextPluginTypes.StrSequence:
                """Get list of all currently loaded plugin names."""
                ...

            def plugin_loaded(self, plugin_name: str) -> bool:
                """Check if a plugin is currently loaded."""
                ...

            def load_plugin(
                self,
                plugin_path: str,
            ) -> FlextCliProtocols.Result[FlextPluginTypes.JsonMapping]:
                """Load a plugin from the specified path."""
                ...

            def unload_plugin(
                self,
                plugin_name: str,
            ) -> FlextCliProtocols.Result[bool]:
                """Unload a previously loaded plugin."""
                ...

        @runtime_checkable
        class PluginDiscovery(Protocol):
            """Protocol for plugin discovery operations."""

            def discover_plugin(
                self,
                plugin_path: str,
            ) -> FlextCliProtocols.Result[FlextPluginModels.Plugin.DiscoveryData]:
                """Discover a single plugin at the specified path."""
                ...

            def discover_plugins(
                self,
                paths: FlextPluginTypes.StrSequence,
            ) -> FlextCliProtocols.Result[
                Sequence[FlextPluginModels.Plugin.DiscoveryData]
            ]:
                """Discover plugins at the given paths."""
                ...

            def validate_plugin(
                self,
                plugin_data: FlextPluginModels.Plugin.DiscoveryData,
            ) -> FlextCliProtocols.Result[bool]:
                """Validate plugin discovery data."""
                ...

        @runtime_checkable
        class PluginRegistry(Protocol):
            """Protocol for plugin registry operations."""

            def fetch_plugin(
                self,
                plugin_name: str,
            ) -> FlextCliProtocols.Result[FlextPluginTypes.JsonValue | None]:
                """Fetch a registered plugin by name."""
                ...

            def plugin_registered(self, plugin_name: str) -> bool:
                """Check if a plugin is registered."""
                ...

            def list_plugins(
                self,
            ) -> FlextCliProtocols.Result[Sequence[FlextPluginTypes.JsonMapping]]:
                """List all registered plugins."""
                ...

            def register_plugin(
                self,
                plugin: FlextPluginModels.Plugin.Entity | FlextPluginTypes.JsonValue,
            ) -> FlextCliProtocols.Result[bool]:
                """Register a plugin."""
                ...

            def register(
                self,
                plugin: FlextPluginModels.Plugin.Entity,
            ) -> FlextCliProtocols.Result[None]:
                """Register a plugin with normalized API."""
                ...

            def unregister_plugin(
                self,
                plugin_name: str,
            ) -> FlextCliProtocols.Result[bool]:
                """Unregister a plugin."""
                ...

        @runtime_checkable
        class PluginExecution(Protocol):
            """Protocol for plugin execution operations."""

            def execute_plugin(
                self,
                plugin_name: str,
                context: FlextPluginTypes.JsonMapping,
            ) -> FlextCliProtocols.Result[FlextPluginTypes.JsonMapping]:
                """Execute a plugin with the given context."""
                ...

            def get_execution_status(
                self,
                _execution_id: str,
            ) -> FlextCliProtocols.Result[str]:
                """Get the status of an execution."""
                ...

            def list_running_executions(self) -> FlextPluginTypes.StrSequence:
                """List all currently running execution IDs."""
                ...

            def stop_execution(
                self,
                _execution_id: str,
            ) -> FlextCliProtocols.Result[bool]:
                """Stop a running execution."""
                ...

        @runtime_checkable
        class PluginSecurity(Protocol):
            """Protocol for plugin security operations."""

            def check_permissions(
                self,
                plugin_name: str,
                permissions: FlextPluginTypes.StrSequence,
            ) -> FlextCliProtocols.Result[bool]:
                """Check if plugin has specified permissions."""
                ...

            def get_security_level(
                self,
                plugin_name: str,
            ) -> FlextCliProtocols.Result[str]:
                """Get security level of a plugin."""
                ...

            def scan_plugin_security(
                self,
                plugin_path: str,
            ) -> FlextCliProtocols.Result[FlextPluginTypes.JsonMapping]:
                """Scan plugin for security vulnerabilities."""
                ...

            def validate_plugin_security(
                self,
                plugin: FlextPluginModels.Plugin.Entity,
            ) -> FlextCliProtocols.Result[bool]:
                """Validate plugin security compliance."""
                ...

        @runtime_checkable
        class PluginHotReload(Protocol):
            """Protocol for hot reload operations."""

            def get_watched_paths(self) -> FlextPluginTypes.StrSequence:
                """Get list of currently watched paths."""
                ...

            def watching(self) -> bool:
                """Check if currently watching for changes."""
                ...

            def reload_plugin(
                self,
                plugin_name: str,
            ) -> FlextCliProtocols.Result[bool]:
                """Reload a plugin."""
                ...

            def start_watching(
                self,
                paths: FlextPluginTypes.StrSequence,
            ) -> FlextCliProtocols.Result[bool]:
                """Start watching paths for plugin changes."""
                ...

            def stop_watching(self) -> FlextCliProtocols.Result[bool]:
                """Stop watching for plugin changes."""
                ...

        @runtime_checkable
        class PluginMonitoring(Protocol):
            """Protocol for plugin monitoring operations."""

            def fetch_plugin_health(
                self,
                plugin_name: str,
            ) -> FlextCliProtocols.Result[FlextPluginTypes.JsonMapping]:
                """Get health status of a plugin."""
                ...

            def fetch_plugin_metrics(
                self,
                plugin_name: str,
            ) -> FlextCliProtocols.Result[FlextPluginTypes.JsonMapping]:
                """Get metrics for a plugin."""
                ...

            def monitoring(self, plugin_name: str) -> bool:
                """Check if a plugin is being monitored."""
                ...

            def start_monitoring(
                self,
                plugin_name: str,
            ) -> FlextCliProtocols.Result[bool]:
                """Start monitoring a plugin."""
                ...

            def stop_monitoring(
                self,
                plugin_name: str,
            ) -> FlextCliProtocols.Result[bool]:
                """Stop monitoring a plugin."""
                ...

        @runtime_checkable
        class PluginConfiguration(Protocol):
            """Protocol for plugin configuration operations."""

            def fetch_default_config(
                self,
                plugin_type: str,
            ) -> FlextCliProtocols.Result[FlextPluginTypes.JsonValue]:
                """Get default configuration for a plugin type."""
                ...

            def load_config(
                self,
                plugin_name: str,
            ) -> FlextCliProtocols.Result[FlextPluginTypes.JsonValue]:
                """Load configuration for a plugin."""
                ...

            def save_config(
                self,
                plugin_name: str,
                settings: FlextPluginTypes.JsonValue,
            ) -> FlextCliProtocols.Result[bool]:
                """Save configuration for a plugin."""
                ...

            def validate_config(
                self,
                settings: FlextPluginTypes.JsonValue,
            ) -> FlextCliProtocols.Result[bool]:
                """Validate plugin configuration."""
                ...

        @runtime_checkable
        class PluginLifecycle(Protocol):
            """Protocol for plugin lifecycle operations."""

            def activate_plugin(
                self,
                plugin_name: str,
            ) -> FlextCliProtocols.Result[bool]:
                """Activate a plugin."""
                ...

            def deactivate_plugin(
                self,
                plugin_name: str,
            ) -> FlextCliProtocols.Result[bool]:
                """Deactivate a plugin."""
                ...

            def destroy_plugin(
                self,
                plugin_name: str,
            ) -> FlextCliProtocols.Result[bool]:
                """Destroy a plugin."""
                ...

            def fetch_plugin_status(
                self,
                plugin_name: str,
            ) -> FlextCliProtocols.Result[str]:
                """Fetch the status of a plugin."""
                ...

            def initialize_plugin(
                self,
                plugin_name: str,
            ) -> FlextCliProtocols.Result[bool]:
                """Initialize a plugin."""
                ...

            def list_plugin_statuses(
                self,
            ) -> FlextCliProtocols.Result[FlextPluginTypes.StrMapping]:
                """Get status of all plugins."""
                ...

        @runtime_checkable
        class PluginValidation(Protocol):
            """Protocol for plugin validation operations."""

            def validate_plugin_compatibility(
                self, plugin_name: str
            ) -> FlextCliProtocols.Result[bool]:
                """Validate plugin compatibility."""
                ...

            def validate_plugin_dependencies(
                self,
                plugin_name: str,
            ) -> FlextCliProtocols.Result[bool]:
                """Validate plugin dependencies."""
                ...

            def validate_plugin_permissions(
                self,
                plugin_name: str,
            ) -> FlextCliProtocols.Result[bool]:
                """Validate plugin permissions."""
                ...

            def validate_plugin_structure(
                self,
                plugin_data: FlextPluginTypes.JsonValue,
            ) -> FlextCliProtocols.Result[bool]:
                """Validate plugin structure."""
                ...

        @runtime_checkable
        class PluginStorage(Protocol):
            """Protocol for plugin storage operations."""

            def delete_plugin(
                self,
                plugin_name: str,
            ) -> FlextCliProtocols.Result[bool]:
                """Delete stored plugin."""
                ...

            def list_stored_plugins(
                self,
            ) -> FlextCliProtocols.Result[FlextPluginTypes.StrSequence]:
                """List all stored plugin names."""
                ...

            def plugin_exists(self, plugin_name: str) -> bool:
                """Check if plugin is stored."""
                ...

            def retrieve_plugin(
                self, plugin_name: str
            ) -> FlextCliProtocols.Result[FlextPluginTypes.JsonValue | None]:
                """Retrieve stored plugin data."""
                ...

            def store_plugin(
                self,
                plugin_data: FlextPluginTypes.JsonValue,
            ) -> FlextCliProtocols.Result[bool]:
                """Store plugin data."""
                ...

        @runtime_checkable
        class Logger(Protocol):
            """Protocol for logging operations."""

            def critical(
                self,
                message: str,
                *args: FlextPluginTypes.JsonValue,
                **kwargs: FlextPluginTypes.Scalar,
            ) -> None:
                """Log critical message."""
                ...

            def debug(
                self,
                message: str,
                *args: FlextPluginTypes.JsonValue,
                **kwargs: FlextPluginTypes.Scalar,
            ) -> None:
                """Log debug message."""
                ...

            def error(
                self,
                message: str,
                *args: FlextPluginTypes.JsonValue,
                **kwargs: FlextPluginTypes.Scalar,
            ) -> None:
                """Log error message."""
                ...

            def info(
                self,
                message: str,
                *args: FlextPluginTypes.JsonValue,
                **kwargs: FlextPluginTypes.Scalar,
            ) -> None:
                """Log info message."""
                ...

            def warning(
                self,
                message: str,
                *args: FlextPluginTypes.JsonValue,
                **kwargs: FlextPluginTypes.Scalar,
            ) -> None:
                """Log warning message."""
                ...

        @runtime_checkable
        class DiscoveryStrategy(Protocol):
            """Strategy protocol for plugin discovery."""

            def discover(
                self,
                paths: FlextPluginTypes.StrSequence,
            ) -> FlextCliProtocols.Result[
                Sequence[FlextPluginModels.Plugin.DiscoveryData]
            ]:
                """Discover plugins using this strategy."""
                ...


p: type[FlextPluginProtocols] = FlextPluginProtocols

__all__: list[str] = ["FlextPluginProtocols", "p"]
