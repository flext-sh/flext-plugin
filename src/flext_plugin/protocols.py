"""FLEXT Plugin Protocols - Synchronous protocol composition with Pydantic models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

# Protocol methods inherit documentation from the Protocol class docstring

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_core.protocols import FlextProtocols as m_core


class FlextPluginProtocols(m_core):
    """Unified plugin protocols extending m_core.

    Extends m_core to inherit all foundation protocols (Result, Service, etc.)
    and adds plugin-specific protocols in the Plugin namespace.

    Architecture:
    - EXTENDS: m_core (inherits Foundation, Domain, Application, etc.)
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
        ) -> m_core.Result[dict[str, object]]:
            """Load a plugin from the specified path."""

        def unload_plugin(self, _plugin_name: str) -> m_core.Result[bool]:
            """Unload a previously loaded plugin."""

        def is_plugin_loaded(self, _plugin_name: str) -> bool:
            """Check if a plugin is currently loaded."""

        def get_loaded_plugins(self) -> list[str]:
            """Get list of all currently loaded plugin names."""

        @runtime_checkable
        class PluginDiscovery(Protocol):
            """Protocol for plugin discovery operations."""

        def discover_plugins(
            self,
            paths: list[str],
        ) -> m_core.Result[list[dict[str, object]]]:
            """Discover plugins at the given paths."""

        def discover_plugin(
            self,
            _plugin_path: str,
        ) -> m_core.Result[dict[str, object]]:
            """Discover a single plugin at the specified path."""

        def validate_plugin(
            self,
            _plugin_data: dict[str, object],
        ) -> m_core.Result[bool]:
            """Validate plugin discovery data."""

        @runtime_checkable
        class PluginRegistry(Protocol):
            """Protocol for plugin registry operations."""

        def register_plugin(self, _plugin: object) -> m_core.Result[bool]:
            """Register a plugin."""

        def unregister_plugin(self, _plugin_name: str) -> m_core.Result[bool]:
            """Unregister a plugin."""

        def get_plugin(self, _plugin_name: str) -> m_core.Result[object | None]:
            """Get a registered plugin by name."""

        def list_plugins(self) -> m_core.Result[list[dict[str, object]]]:
            """List all registered plugins."""

        def is_plugin_registered(self, _plugin_name: str) -> bool:
            """Check if a plugin is registered."""

        @runtime_checkable
        class PluginExecution(Protocol):
            """Protocol for plugin execution operations."""

            def execute_plugin(
                self,
                _plugin_name: str,
                _context: dict[str, object],
            ) -> m_core.Result[dict[str, object]]:
                """Execute a plugin with the given context."""
                ...

            def stop_execution(self, _execution_id: str) -> m_core.Result[bool]:
                """Stop a running execution."""
                ...

            def get_execution_status(self, _execution_id: str) -> m_core.Result[str]:
                """Get the status of an execution."""
                ...

            def list_running_executions(self) -> list[str]:
                """List all currently running execution IDs."""
                ...

        @runtime_checkable
        class PluginSecurity(Protocol):
            """Protocol for plugin security operations."""

        def validate_plugin_security(self, _plugin: object) -> m_core.Result[bool]:
            """Validate plugin security compliance."""

        def check_permissions(
            self,
            _plugin_name: str,
            _permissions: list[str],
        ) -> m_core.Result[bool]:
            """Check if plugin has specified permissions."""

        def scan_plugin_security(
            self,
            _plugin_path: str,
        ) -> m_core.Result[dict[str, object]]:
            """Scan plugin for security vulnerabilities."""

        def get_security_level(self, _plugin_name: str) -> m_core.Result[str]:
            """Get security level of a plugin."""

        @runtime_checkable
        class PluginHotReload(Protocol):
            """Protocol for hot reload operations."""

        def start_watching(self, paths: list[str]) -> m_core.Result[bool]:
            """Start watching paths for plugin changes."""

        def stop_watching(self) -> m_core.Result[bool]:
            """Stop watching for plugin changes."""

        def reload_plugin(self, _plugin_name: str) -> m_core.Result[bool]:
            """Reload a plugin."""

        def is_watching(self) -> bool:
            """Check if currently watching for changes."""

        def get_watched_paths(self) -> list[str]:
            """Get list of currently watched paths."""

        @runtime_checkable
        class PluginMonitoring(Protocol):
            """Protocol for plugin monitoring operations."""

        def start_monitoring(self, _plugin_name: str) -> m_core.Result[bool]:
            """Start monitoring a plugin."""

        def stop_monitoring(self, _plugin_name: str) -> m_core.Result[bool]:
            """Stop monitoring a plugin."""

        def get_plugin_metrics(
            self,
            _plugin_name: str,
        ) -> m_core.Result[dict[str, object]]:
            """Get metrics for a plugin."""

        def get_plugin_health(
            self,
            _plugin_name: str,
        ) -> m_core.Result[dict[str, object]]:
            """Get health status of a plugin."""

        def is_monitoring(self, _plugin_name: str) -> bool:
            """Check if a plugin is being monitored."""

        @runtime_checkable
        class PluginConfiguration(Protocol):
            """Protocol for plugin configuration operations."""

        def load_config(self, _plugin_name: str) -> m_core.Result[dict[str, object]]:
            """Load configuration for a plugin."""

        def save_config(
            self,
            _plugin_name: str,
            config: dict[str, object],
        ) -> m_core.Result[bool]:
            """Save configuration for a plugin."""

        def validate_config(self, config: dict[str, object]) -> m_core.Result[bool]:
            """Validate plugin configuration."""

        def get_default_config(
            self,
            plugin_type: str,
        ) -> m_core.Result[dict[str, object]]:
            """Get default configuration for a plugin type."""

        @runtime_checkable
        class PluginLifecycle(Protocol):
            """Protocol for plugin lifecycle operations."""

        def initialize_plugin(self, _plugin_name: str) -> m_core.Result[bool]:
            """Initialize a plugin."""

        def activate_plugin(self, _plugin_name: str) -> m_core.Result[bool]:
            """Activate a plugin."""

        def deactivate_plugin(self, _plugin_name: str) -> m_core.Result[bool]:
            """Deactivate a plugin."""

        def destroy_plugin(self, _plugin_name: str) -> m_core.Result[bool]:
            """Destroy a plugin."""

        def get_plugin_status(self, _plugin_name: str) -> m_core.Result[str]:
            """Get the status of a plugin."""

        def list_plugin_statuses(self) -> m_core.Result[dict[str, str]]:
            """Get status of all plugins."""

        @runtime_checkable
        class PluginValidation(Protocol):
            """Protocol for plugin validation operations."""

        def validate_plugin_structure(
            self,
            _plugin_data: dict[str, object],
        ) -> m_core.Result[bool]:
            """Validate plugin structure."""

        def validate_plugin_dependencies(
            self,
            _plugin_name: str,
        ) -> m_core.Result[bool]:
            """Validate plugin dependencies."""

        def validate_plugin_permissions(
            self,
            _plugin_name: str,
        ) -> m_core.Result[bool]:
            """Validate plugin permissions."""

        def validate_plugin_compatibility(
            self,
            _plugin_name: str,
        ) -> m_core.Result[bool]:
            """Validate plugin compatibility."""

        @runtime_checkable
        class PluginStorage(Protocol):
            """Protocol for plugin storage operations."""

        def store_plugin(
            self,
            _plugin_data: dict[str, object],
        ) -> m_core.Result[bool]:
            """Store plugin data."""

        def retrieve_plugin(
            self,
            _plugin_name: str,
        ) -> m_core.Result[dict[str, object] | None]:
            """Retrieve stored plugin data."""

        def delete_plugin(self, _plugin_name: str) -> m_core.Result[bool]:
            """Delete stored plugin."""

        def list_stored_plugins(self) -> m_core.Result[list[str]]:
            """List all stored plugin names."""

        def plugin_exists(self, _plugin_name: str) -> bool:
            """Check if plugin is stored."""

        @runtime_checkable
        class LoggerProtocol(Protocol):
            """Protocol for logging operations."""

            def critical(self, message: str, *args: object, **kwargs: object) -> None:
                """Log critical message."""
                ...

            def error(self, message: str, *args: object, **kwargs: object) -> None:
                """Log error message."""
                ...

            def warning(self, message: str, *args: object, **kwargs: object) -> None:
                """Log warning message."""
                ...

            def info(self, message: str, *args: object, **kwargs: object) -> None:
                """Log info message."""
                ...

            def debug(self, message: str, *args: object, **kwargs: object) -> None:
                """Log debug message."""
                ...

        # =====================================================================
        # DUCK TYPING PROTOCOLS
        # =====================================================================
        # Protocols for duck typing common plugin patterns.

        @runtime_checkable
        class PluginLoaderProtocol(Protocol):
            """Protocol for plugin loader interface."""

            def load_plugin(self, plugin_path: str | object) -> m_core.Result[object]:
                """Load plugin from path."""
                ...

        @runtime_checkable
        class PluginRegistryProtocol(Protocol):
            """Protocol for plugin registry interface."""

            def register(self, plugin: object) -> m_core.Result[None]:
                """Register a plugin."""
                ...

            def get_plugin(self, plugin_name: str) -> m_core.Result[object]:
                """Get plugin by name."""
                ...

        @runtime_checkable
        class DiscoveryStrategyProtocol(Protocol):
            """Strategy protocol for plugin discovery."""

            def discover(
                self,
                paths: list[str],
            ) -> m_core.Result[list[object]]:
                """Discover plugins using this strategy."""
                ...


p = FlextPluginProtocols

__all__ = [
    "FlextPluginProtocols",
    "p",
]
