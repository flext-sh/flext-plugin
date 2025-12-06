"""FLEXT Plugin Protocols - Synchronous protocol composition with Pydantic models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

# Protocol methods inherit documentation from the Protocol class docstring

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from flext_core import r

if TYPE_CHECKING:
    from flext_plugin.models import FlextPluginModels


class FlextPluginProtocols:
    """Synchronous plugin protocols with Pydantic model composition."""

    # Core plugin operations
    class PluginLoader(Protocol):
        """Protocol for plugin loading operations."""

        def load_plugin(
            self,
            _plugin_path: str,
        ) -> r[FlextPluginModels.LoadData]:
            """Load a plugin from the specified path."""
            ...

        def unload_plugin(self, _plugin_name: str) -> r[bool]:
            """Unload a previously loaded plugin."""
            ...

        def is_plugin_loaded(self, _plugin_name: str) -> bool:
            """Check if a plugin is currently loaded."""
            ...

        def get_loaded_plugins(self) -> list[str]:
            """Get list of all currently loaded plugin names."""
            ...

    class PluginDiscovery(Protocol):
        """Protocol for plugin discovery operations."""

        def discover_plugins(
            self,
            paths: list[str],
        ) -> r[list[FlextPluginModels.DiscoveryData]]:
            """Discover plugins at the given paths."""
            ...

        def discover_plugin(
            self,
            _plugin_path: str,
        ) -> r[FlextPluginModels.DiscoveryData]:
            """Discover a single plugin at the specified path."""
            ...

        def validate_plugin(
            self,
            _plugin_data: FlextPluginModels.DiscoveryData,
        ) -> r[bool]:
            """Validate plugin discovery data."""
            ...

    class PluginRegistry(Protocol):
        """Protocol for plugin registry operations."""

        def register_plugin(self, _plugin: object) -> r[bool]:
            """Register a plugin."""
            ...

        def unregister_plugin(self, _plugin_name: str) -> r[bool]:
            """Unregister a plugin."""
            ...

        def get_plugin(self, _plugin_name: str) -> r[object | None]:
            """Get a registered plugin by name."""
            ...

        def list_plugins(self) -> r[list[dict[str, object]]]:
            """List all registered plugins."""
            ...

        def is_plugin_registered(self, _plugin_name: str) -> bool:
            """Check if a plugin is registered."""
            ...

    class PluginExecution(Protocol):
        """Protocol for plugin execution operations."""

        def execute_plugin(
            self,
            _plugin_name: str,
            _context: dict[str, object],
        ) -> r[dict[str, object]]:
            """Execute a plugin with the given context."""
            ...

        def stop_execution(self, _execution_id: str) -> r[bool]:
            """Stop a running execution."""
            ...

        def get_execution_status(self, _execution_id: str) -> r[str]:
            """Get the status of an execution."""
            ...

        def list_running_executions(self) -> list[str]:
            """List all currently running execution IDs."""
            ...

    class PluginSecurity(Protocol):
        """Protocol for plugin security operations."""

        def validate_plugin(self, _plugin: object) -> r[bool]:
            """Validate plugin security compliance."""
            ...

        def check_permissions(
            self,
            _plugin_name: str,
            _permissions: list[str],
        ) -> r[bool]:
            """Check if plugin has specified permissions."""
            ...

        def scan_plugin_security(
            self,
            _plugin_path: str,
        ) -> r[dict[str, object]]:
            """Scan plugin for security vulnerabilities."""
            ...

        def get_security_level(self, _plugin_name: str) -> r[str]:
            """Get security level of a plugin."""
            ...

    class PluginHotReload(Protocol):
        """Protocol for hot reload operations."""

        def start_watching(self, paths: list[str]) -> r[bool]:
            """Start watching paths for plugin changes."""
            ...

        def stop_watching(self) -> r[bool]:
            """Stop watching for plugin changes."""
            ...

        def reload_plugin(self, _plugin_name: str) -> r[bool]:
            """Reload a plugin."""
            ...

        def is_watching(self) -> bool:
            """Check if currently watching for changes."""
            ...

        def get_watched_paths(self) -> list[str]:
            """Get list of currently watched paths."""
            ...

    class PluginMonitoring(Protocol):
        """Protocol for plugin monitoring operations."""

        def start_monitoring(self, _plugin_name: str) -> r[bool]:
            """Start monitoring a plugin."""
            ...

        def stop_monitoring(self, _plugin_name: str) -> r[bool]:
            """Stop monitoring a plugin."""
            ...

        def get_plugin_metrics(
            self,
            _plugin_name: str,
        ) -> r[dict[str, object]]:
            """Get metrics for a plugin."""
            ...

        def get_plugin_health(
            self,
            _plugin_name: str,
        ) -> r[dict[str, object]]:
            """Get health status of a plugin."""
            ...

        def is_monitoring(self, _plugin_name: str) -> bool:
            """Check if a plugin is being monitored."""
            ...

    class PluginConfiguration(Protocol):
        """Protocol for plugin configuration operations."""

        def load_config(self, _plugin_name: str) -> r[dict[str, object]]:
            """Load configuration for a plugin."""
            ...

        def save_config(
            self,
            _plugin_name: str,
            config: dict[str, object],
        ) -> r[bool]:
            """Save configuration for a plugin."""
            ...

        def validate_config(self, config: dict[str, object]) -> r[bool]:
            """Validate plugin configuration."""
            ...

        def get_default_config(
            self,
            plugin_type: str,
        ) -> r[dict[str, object]]:
            """Get default configuration for a plugin type."""
            ...

    class PluginLifecycle(Protocol):
        """Protocol for plugin lifecycle operations."""

        def initialize_plugin(self, _plugin_name: str) -> r[bool]:
            """Initialize a plugin."""
            ...

        def activate_plugin(self, _plugin_name: str) -> r[bool]:
            """Activate a plugin."""
            ...

        def deactivate_plugin(self, _plugin_name: str) -> r[bool]:
            """Deactivate a plugin."""
            ...

        def destroy_plugin(self, _plugin_name: str) -> r[bool]:
            """Destroy a plugin."""
            ...

        def get_plugin_status(self, _plugin_name: str) -> r[str]:
            """Get the status of a plugin."""
            ...

        def list_plugin_statuses(self) -> r[dict[str, str]]:
            """Get status of all plugins."""
            ...

    class PluginValidation(Protocol):
        """Protocol for plugin validation operations."""

        def validate_plugin_structure(
            self,
            _plugin_data: dict[str, object],
        ) -> r[bool]:
            """Validate plugin structure."""
            ...

        def validate_plugin_dependencies(
            self,
            _plugin_name: str,
        ) -> r[bool]:
            """Validate plugin dependencies."""
            ...

        def validate_plugin_permissions(
            self,
            _plugin_name: str,
        ) -> r[bool]:
            """Validate plugin permissions."""
            ...

        def validate_plugin_compatibility(
            self,
            _plugin_name: str,
        ) -> r[bool]:
            """Validate plugin compatibility."""
            ...

    class PluginStorage(Protocol):
        """Protocol for plugin storage operations."""

        def store_plugin(
            self,
            _plugin_data: dict[str, object],
        ) -> r[bool]:
            """Store plugin data."""
            ...

        def retrieve_plugin(
            self,
            _plugin_name: str,
        ) -> r[dict[str, object] | None]:
            """Retrieve stored plugin data."""
            ...

        def delete_plugin(self, _plugin_name: str) -> r[bool]:
            """Delete stored plugin."""
            ...

        def list_stored_plugins(self) -> r[list[str]]:
            """List all stored plugin names."""
            ...

        def plugin_exists(self, _plugin_name: str) -> bool:
            """Check if plugin is stored."""
            ...

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


__all__ = ["FlextPluginProtocols"]
