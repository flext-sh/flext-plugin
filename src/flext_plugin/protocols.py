"""FLEXT Plugin Protocols - Plugin system protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Protocol

from flext_core import FlextCore

from flext_plugin.types import FlextPluginTypes


class FlextPluginProtocols:
    """Plugin system protocol definitions for dependency injection and testing.

    Defines abstract interfaces that concrete implementations must follow,
    enabling clean architecture and testability through dependency inversion.
    This class contains all protocols as nested classes following the
    [Project][Module] pattern.
    """

    class PluginLoader(Protocol):
        """Protocol for plugin loading implementations."""

        async def load_plugin(
            self, plugin_path: str
        ) -> FlextCore.Result[FlextPluginTypes.Core.PluginDict]:
            """Load a plugin from the given path."""
            ...

        async def unload_plugin(self, plugin_name: str) -> FlextCore.Result[bool]:
            """Unload a plugin by name."""
            ...

        def is_plugin_loaded(self, plugin_name: str) -> bool:
            """Check if a plugin is currently loaded."""
            ...

        def get_loaded_plugins(self) -> FlextCore.Types.StringList:
            """Get list of currently loaded plugin names."""
            ...

    class PluginDiscovery(Protocol):
        """Protocol for plugin discovery implementations."""

        async def discover_plugins(
            self, paths: FlextPluginTypes.Core.StringList
        ) -> FlextCore.Result[FlextPluginTypes.Core.PluginList]:
            """Discover plugins in the given paths."""
            ...

        async def discover_plugin(
            self, plugin_path: str
        ) -> FlextCore.Result[FlextPluginTypes.Core.PluginDict]:
            """Discover a single plugin at the given path."""
            ...

        async def validate_plugin(
            self, plugin_data: FlextPluginTypes.Core.PluginDict
        ) -> FlextCore.Result[bool]:
            """Validate discovered plugin data."""
            ...

    class PluginRegistry(Protocol):
        """Protocol for plugin registry implementations."""

        async def register_plugin(
            self, plugin: FlextPluginTypes.Core.PluginEntity
        ) -> FlextCore.Result[bool]:
            """Register a plugin in the registry."""
            ...

        async def unregister_plugin(self, plugin_name: str) -> FlextCore.Result[bool]:
            """Unregister a plugin from the registry."""
            ...

        async def get_plugin(
            self, plugin_name: str
        ) -> FlextCore.Result[FlextPluginTypes.Core.PluginEntity | None]:
            """Get a plugin by name."""
            ...

        async def list_plugins(
            self,
        ) -> FlextCore.Result[FlextPluginTypes.Core.PluginList]:
            """List all registered plugins."""
            ...

        def is_plugin_registered(self, plugin_name: str) -> bool:
            """Check if a plugin is registered."""
            ...

    class PluginExecution(Protocol):
        """Protocol for plugin execution implementations."""

        async def execute_plugin(
            self,
            plugin_name: str,
            context: FlextPluginTypes.Execution.ExecutionContext,
        ) -> FlextCore.Result[FlextPluginTypes.Execution.ExecutionResult]:
            """Execute a plugin with the given context."""
            ...

        async def stop_execution(self, execution_id: str) -> FlextCore.Result[bool]:
            """Stop a running execution."""
            ...

        async def get_execution_status(
            self, execution_id: str
        ) -> FlextCore.Result[str]:
            """Get the status of a running execution."""
            ...

        def list_running_executions(self) -> FlextCore.Types.StringList:
            """List all currently running execution IDs."""
            ...

    class PluginSecurity(Protocol):
        """Protocol for plugin security implementations."""

        async def validate_plugin(
            self, plugin: FlextPluginTypes.Core.PluginEntity
        ) -> FlextCore.Result[bool]:
            """Validate a plugin for security compliance."""
            ...

        async def check_permissions(
            self, plugin_name: str, permissions: FlextPluginTypes.Core.StringList
        ) -> FlextCore.Result[bool]:
            """Check if a plugin has the required permissions."""
            ...

        async def scan_plugin_security(
            self, plugin_path: str
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Perform security scan on a plugin."""
            ...

        async def get_security_level(self, plugin_name: str) -> FlextCore.Result[str]:
            """Get the security level of a plugin."""
            ...

    class PluginHotReload(Protocol):
        """Protocol for plugin hot reload implementations."""

        def start_watching(
            self, paths: FlextPluginTypes.Core.StringList
        ) -> FlextCore.Result[bool]:
            """Start watching the given paths for changes."""
            ...

        def stop_watching(self) -> FlextCore.Result[bool]:
            """Stop watching for changes."""
            ...

        def reload_plugin(self, plugin_name: str) -> FlextCore.Result[bool]:
            """Reload a specific plugin."""
            ...

        def is_watching(self) -> bool:
            """Check if hot reload is currently watching for changes."""
            ...

        def get_watched_paths(self) -> FlextCore.Types.StringList:
            """Get list of currently watched paths."""
            ...

    class PluginMonitoring(Protocol):
        """Protocol for plugin monitoring implementations."""

        async def start_monitoring(self, plugin_name: str) -> FlextCore.Result[bool]:
            """Start monitoring a plugin."""
            ...

        async def stop_monitoring(self, plugin_name: str) -> FlextCore.Result[bool]:
            """Stop monitoring a plugin."""
            ...

        async def get_plugin_metrics(
            self, plugin_name: str
        ) -> FlextCore.Result[FlextPluginTypes.Performance.Metrics]:
            """Get metrics for a plugin."""
            ...

        async def get_plugin_health(
            self, plugin_name: str
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Get health status for a plugin."""
            ...

        def is_monitoring(self, plugin_name: str) -> bool:
            """Check if a plugin is being monitored."""
            ...

    class PluginConfiguration(Protocol):
        """Protocol for plugin configuration implementations."""

        def load_config(
            self, plugin_name: str
        ) -> FlextCore.Result[FlextPluginTypes.Core.ConfigDict]:
            """Load configuration for a plugin."""
            ...

        def save_config(
            self, plugin_name: str, config: FlextPluginTypes.Core.ConfigDict
        ) -> FlextCore.Result[bool]:
            """Save configuration for a plugin."""
            ...

        def validate_config(
            self, config: FlextPluginTypes.Core.ConfigDict
        ) -> FlextCore.Result[bool]:
            """Validate plugin configuration."""
            ...

        def get_default_config(
            self, plugin_type: str
        ) -> FlextCore.Result[FlextPluginTypes.Core.ConfigDict]:
            """Get default configuration for a plugin type."""
            ...

    class PluginLifecycle(Protocol):
        """Protocol for plugin lifecycle management implementations."""

        def initialize_plugin(self, plugin_name: str) -> FlextCore.Result[bool]:
            """Initialize a plugin."""
            ...

        def activate_plugin(self, plugin_name: str) -> FlextCore.Result[bool]:
            """Activate a plugin."""
            ...

        def deactivate_plugin(self, plugin_name: str) -> FlextCore.Result[bool]:
            """Deactivate a plugin."""
            ...

        def destroy_plugin(self, plugin_name: str) -> FlextCore.Result[bool]:
            """Destroy a plugin."""
            ...

        def get_plugin_status(self, plugin_name: str) -> FlextCore.Result[str]:
            """Get the current status of a plugin."""
            ...

        def list_plugin_statuses(self) -> FlextCore.Result[dict[str, str]]:
            """Get status of all plugins."""
            ...

    class PluginValidation(Protocol):
        """Protocol for plugin validation implementations."""

        def validate_plugin_structure(
            self, plugin_data: FlextPluginTypes.Core.PluginDict
        ) -> FlextCore.Result[bool]:
            """Validate plugin data structure."""
            ...

        def validate_plugin_dependencies(
            self, plugin_name: str
        ) -> FlextCore.Result[bool]:
            """Validate plugin dependencies."""
            ...

        def validate_plugin_permissions(
            self, plugin_name: str
        ) -> FlextCore.Result[bool]:
            """Validate plugin permissions."""
            ...

        def validate_plugin_compatibility(
            self, plugin_name: str
        ) -> FlextCore.Result[bool]:
            """Validate plugin compatibility with platform."""
            ...

    class PluginStorage(Protocol):
        """Protocol for plugin storage implementations."""

        def store_plugin(
            self, plugin_data: FlextPluginTypes.Core.PluginDict
        ) -> FlextCore.Result[bool]:
            """Store plugin data."""
            ...

        def retrieve_plugin(
            self, plugin_name: str
        ) -> FlextCore.Result[FlextPluginTypes.Core.PluginDict | None]:
            """Retrieve plugin data."""
            ...

        def delete_plugin(self, plugin_name: str) -> FlextCore.Result[bool]:
            """Delete plugin data."""
            ...

        def list_stored_plugins(self) -> FlextCore.Result[FlextCore.Types.StringList]:
            """List all stored plugin names."""
            ...

        def plugin_exists(self, plugin_name: str) -> bool:
            """Check if plugin data exists."""
            ...


__all__ = ["FlextPluginProtocols"]
