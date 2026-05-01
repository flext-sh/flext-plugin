"""FLEXT Plugin Protocols - Synchronous protocol composition with Pydantic models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    Sequence,
)
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import p

if TYPE_CHECKING:
    from flext_plugin import m, t


class FlextPluginProtocols(p):
    """Unified plugin protocols extending p.

    Extends p to inherit all foundation protocols (Result, Service, etc.)
    and adds plugin-specific protocols in the Plugin namespace.

    Architecture:
    - EXTENDS: p (inherits Foundation, Domain, Application, etc.)
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
            ) -> p.Result[t.JsonMapping]:
                """Load a plugin from the specified path."""
                ...

            def unload_plugin(
                self,
                plugin_name: str,
            ) -> p.Result[bool]:
                """Unload a previously loaded plugin."""
                ...

        @runtime_checkable
        class PluginDiscovery(Protocol):
            """Protocol for plugin discovery operations."""

            def discover_plugin(
                self,
                plugin_path: str,
            ) -> p.Result[m.Plugin.DiscoveryData]:
                """Discover a single plugin at the specified path."""
                ...

            def discover_plugins(
                self,
                paths: t.StrSequence,
            ) -> p.Result[t.SequenceOf[m.Plugin.DiscoveryData]]:
                """Discover plugins at the given paths."""
                ...

            def validate_plugin(
                self,
                plugin_data: m.Plugin.DiscoveryData,
            ) -> p.Result[bool]:
                """Validate plugin discovery data."""
                ...

        @runtime_checkable
        class PluginRegistry(Protocol):
            """Protocol for plugin registry operations."""

            def fetch_plugin(
                self,
                plugin_name: str,
            ) -> p.Result[t.JsonValue | None]:
                """Fetch a registered plugin by name."""
                ...

            def plugin_registered(self, plugin_name: str) -> bool:
                """Check if a plugin is registered."""
                ...

            def list_plugins(
                self,
            ) -> p.Result[Sequence[t.JsonMapping]]:
                """List all registered plugins."""
                ...

            def register_plugin(
                self,
                plugin: m.Plugin.Entity | t.JsonValue,
            ) -> p.Result[bool]:
                """Register a plugin."""
                ...

            def register(
                self,
                plugin: m.Plugin.Entity,
            ) -> p.Result[None]:
                """Register a plugin with normalized API."""
                ...

            def unregister_plugin(
                self,
                plugin_name: str,
            ) -> p.Result[bool]:
                """Unregister a plugin."""
                ...

        @runtime_checkable
        class PluginExecution(Protocol):
            """Protocol for plugin execution operations."""

            def execute_plugin(
                self,
                plugin_name: str,
                context: t.JsonMapping,
            ) -> p.Result[t.JsonMapping]:
                """Execute a plugin with the given context."""
                ...

            def get_execution_status(
                self,
                _execution_id: str,
            ) -> p.Result[str]:
                """Get the status of an execution."""
                ...

            def list_running_executions(self) -> t.StrSequence:
                """List all currently running execution IDs."""
                ...

            def stop_execution(
                self,
                _execution_id: str,
            ) -> p.Result[bool]:
                """Stop a running execution."""
                ...

        @runtime_checkable
        class PluginSecurity(Protocol):
            """Protocol for plugin security operations."""

            def check_permissions(
                self,
                plugin_name: str,
                permissions: t.StrSequence,
            ) -> p.Result[bool]:
                """Check if plugin has specified permissions."""
                ...

            def get_security_level(
                self,
                plugin_name: str,
            ) -> p.Result[str]:
                """Get security level of a plugin."""
                ...

            def scan_plugin_security(
                self,
                plugin_path: str,
            ) -> p.Result[t.JsonMapping]:
                """Scan plugin for security vulnerabilities."""
                ...

            def validate_plugin_security(
                self,
                plugin: m.Plugin.Entity,
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

            def reload_plugin(
                self,
                plugin_name: str,
            ) -> p.Result[bool]:
                """Reload a plugin."""
                ...

            def start_watching(
                self,
                paths: t.StrSequence,
            ) -> p.Result[bool]:
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
                plugin_name: str,
            ) -> p.Result[t.JsonMapping]:
                """Get health status of a plugin."""
                ...

            def fetch_plugin_metrics(
                self,
                plugin_name: str,
            ) -> p.Result[t.JsonMapping]:
                """Get metrics for a plugin."""
                ...

            def monitoring(self, plugin_name: str) -> bool:
                """Check if a plugin is being monitored."""
                ...

            def start_monitoring(
                self,
                plugin_name: str,
            ) -> p.Result[bool]:
                """Start monitoring a plugin."""
                ...

            def stop_monitoring(
                self,
                plugin_name: str,
            ) -> p.Result[bool]:
                """Stop monitoring a plugin."""
                ...

        @runtime_checkable
        class PluginConfiguration(Protocol):
            """Protocol for plugin configuration operations."""

            def fetch_default_config(
                self,
                plugin_type: str,
            ) -> p.Result[t.JsonValue]:
                """Get default configuration for a plugin type."""
                ...

            def load_config(
                self,
                plugin_name: str,
            ) -> p.Result[t.JsonValue]:
                """Load configuration for a plugin."""
                ...

            def save_config(
                self,
                plugin_name: str,
                settings: t.JsonValue,
            ) -> p.Result[bool]:
                """Save configuration for a plugin."""
                ...

            def validate_config(
                self,
                settings: t.JsonValue,
            ) -> p.Result[bool]:
                """Validate plugin configuration."""
                ...

        @runtime_checkable
        class PluginLifecycle(Protocol):
            """Protocol for plugin lifecycle operations."""

            def activate_plugin(
                self,
                plugin_name: str,
            ) -> p.Result[bool]:
                """Activate a plugin."""
                ...

            def deactivate_plugin(
                self,
                plugin_name: str,
            ) -> p.Result[bool]:
                """Deactivate a plugin."""
                ...

            def destroy_plugin(
                self,
                plugin_name: str,
            ) -> p.Result[bool]:
                """Destroy a plugin."""
                ...

            def fetch_plugin_status(
                self,
                plugin_name: str,
            ) -> p.Result[str]:
                """Fetch the status of a plugin."""
                ...

            def initialize_plugin(
                self,
                plugin_name: str,
            ) -> p.Result[bool]:
                """Initialize a plugin."""
                ...

            def list_plugin_statuses(
                self,
            ) -> p.Result[t.StrMapping]:
                """Get status of all plugins."""
                ...

        @runtime_checkable
        class PluginValidation(Protocol):
            """Protocol for plugin validation operations."""

            def validate_plugin_compatibility(self, plugin_name: str) -> p.Result[bool]:
                """Validate plugin compatibility."""
                ...

            def validate_plugin_dependencies(
                self,
                plugin_name: str,
            ) -> p.Result[bool]:
                """Validate plugin dependencies."""
                ...

            def validate_plugin_permissions(
                self,
                plugin_name: str,
            ) -> p.Result[bool]:
                """Validate plugin permissions."""
                ...

            def validate_plugin_structure(
                self,
                plugin_data: t.JsonValue,
            ) -> p.Result[bool]:
                """Validate plugin structure."""
                ...

        @runtime_checkable
        class PluginStorage(Protocol):
            """Protocol for plugin storage operations."""

            def delete_plugin(
                self,
                plugin_name: str,
            ) -> p.Result[bool]:
                """Delete stored plugin."""
                ...

            def list_stored_plugins(
                self,
            ) -> p.Result[t.StrSequence]:
                """List all stored plugin names."""
                ...

            def plugin_exists(self, plugin_name: str) -> bool:
                """Check if plugin is stored."""
                ...

            def retrieve_plugin(self, plugin_name: str) -> p.Result[t.JsonValue | None]:
                """Retrieve stored plugin data."""
                ...

            def store_plugin(
                self,
                plugin_data: t.JsonValue,
            ) -> p.Result[bool]:
                """Store plugin data."""
                ...

        @runtime_checkable
        class DiscoveryStrategy(Protocol):
            """Strategy protocol for plugin discovery."""

            def discover(
                self,
                paths: t.StrSequence,
            ) -> p.Result[t.SequenceOf[m.Plugin.DiscoveryData]]:
                """Discover plugins using this strategy."""
                ...


p: type[FlextPluginProtocols] = FlextPluginProtocols

__all__: list[str] = ["FlextPluginProtocols", "p"]
