"""Plugin domain protocols for flext-plugin.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Sequence

    from flext_plugin import m, p, t
    from flext_plugin._utilities import FlextPluginUtilitiesPluginPlatform


class FlextPluginProtocolsPlugin:
    """Plugin domain-specific protocols namespace."""

    @runtime_checkable
    class Discovery(Protocol):
        """Protocol for plugin discovery operations."""

        def discover_plugin(self, plugin_path: str) -> p.Result[m.Plugin.DiscoveryData]:
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
    class Loader(Protocol):
        """Protocol for plugin loading operations."""

        def get_loaded_plugins(self) -> t.StrSequence:
            """Get list of all currently loaded plugin names."""
            ...

        def plugin_loaded(self, plugin_name: str) -> bool:
            """Check if a plugin is currently loaded."""
            ...

        def load_plugin(self, plugin_path: str) -> p.Result[t.JsonMapping]:
            """Load a plugin from the specified path."""
            ...

        def unload_plugin(self, plugin_name: str) -> p.Result[bool]:
            """Unload a previously loaded plugin."""
            ...

    @runtime_checkable
    class Registry(Protocol):
        """Protocol for plugin registry operations."""

        def fetch_plugin(self, plugin_name: str) -> t.JsonValue | None:
            """Fetch a registered plugin by name."""
            ...

        def plugin_registered(self, plugin_name: str) -> bool:
            """Check if a plugin is registered."""
            ...

        def list_plugins(self) -> t.SequenceOf[t.JsonMapping]:
            """List all registered plugins."""
            ...

        def register_plugin(self, plugin: m.Plugin.Entity | t.JsonValue) -> bool:
            """Register a plugin."""
            ...

        def register(self, plugin: m.Plugin.Entity) -> bool:
            """Register a plugin with normalized API."""
            ...

        def unregister_plugin(self, plugin_name: str) -> bool:
            """Unregister a plugin."""
            ...

    @runtime_checkable
    class Execution(Protocol):
        """Protocol for plugin execution operations."""

        def execute_plugin(
            self,
            plugin_name: str,
            context: t.JsonMapping,
        ) -> p.Result[t.JsonMapping]:
            """Execute a plugin with the given context."""
            ...

        def get_execution_status(self, execution_id: str) -> p.Result[str]:
            """Get the status of an execution."""
            ...

        def list_running_executions(self) -> t.StrSequence:
            """List all currently running execution IDs."""
            ...

        def stop_execution(self, execution_id: str) -> p.Result[bool]:
            """Stop a running execution."""
            ...

    @runtime_checkable
    class Security(Protocol):
        """Protocol for plugin security operations."""

        def check_permissions(
            self,
            plugin_name: str,
            permissions: t.StrSequence,
        ) -> bool:
            """Check if plugin has specified permissions."""
            ...

        def get_security_level(self, plugin_name: str) -> str:
            """Get security level of a plugin."""
            ...

        def scan_plugin_security(self, plugin_path: str) -> t.JsonMapping:
            """Scan plugin for security vulnerabilities."""
            ...

        def validate_plugin_security(self, plugin: m.Plugin.Entity) -> bool:
            """Validate plugin security compliance."""
            ...

    @runtime_checkable
    class HotReload(Protocol):
        """Protocol for hot reload operations."""

        def get_watched_paths(self) -> t.StrSequence:
            """Get list of currently watched paths."""
            ...

        def watching(self) -> bool:
            """Check if currently watching for changes."""
            ...

        def reload_plugin(self, plugin_name: str) -> bool:
            """Reload a plugin."""
            ...

        def start_watching(self, paths: t.StrSequence) -> bool:
            """Start watching paths for plugin changes."""
            ...

        def stop_watching(self) -> bool:
            """Stop watching for plugin changes."""
            ...

    @runtime_checkable
    class Monitoring(Protocol):
        """Protocol for plugin monitoring operations."""

        def fetch_plugin_health(self, plugin_name: str) -> t.JsonMapping:
            """Get health status of a plugin."""
            ...

        def fetch_plugin_metrics(self, plugin_name: str) -> t.JsonMapping:
            """Get metrics for a plugin."""
            ...

        def monitoring(self, plugin_name: str) -> bool:
            """Check if a plugin is being monitored."""
            ...

        def start_monitoring(self, plugin_name: str) -> bool:
            """Start monitoring a plugin."""
            ...

        def stop_monitoring(self, plugin_name: str) -> bool:
            """Stop monitoring a plugin."""
            ...

    @runtime_checkable
    class Configuration(Protocol):
        """Protocol for plugin configuration operations."""

        def fetch_default_config(self, plugin_type: str) -> t.JsonValue:
            """Get default configuration for a plugin type."""
            ...

        def load_config(self, plugin_name: str) -> t.JsonValue:
            """Load configuration for a plugin."""
            ...

        def save_config(self, plugin_name: str, settings: t.JsonValue) -> bool:
            """Save configuration for a plugin."""
            ...

        def validate_config(self, settings: t.JsonValue) -> bool:
            """Validate plugin configuration."""
            ...

    @runtime_checkable
    class Lifecycle(Protocol):
        """Protocol for plugin lifecycle operations."""

        def activate_plugin(self, plugin_name: str) -> bool:
            """Activate a plugin."""
            ...

        def deactivate_plugin(self, plugin_name: str) -> bool:
            """Deactivate a plugin."""
            ...

        def destroy_plugin(self, plugin_name: str) -> bool:
            """Destroy a plugin."""
            ...

        def fetch_plugin_status(self, plugin_name: str) -> str:
            """Fetch the status of a plugin."""
            ...

        def initialize_plugin(self, plugin_name: str) -> bool:
            """Initialize a plugin."""
            ...

        def list_plugin_statuses(self) -> t.StrMapping:
            """Get status of all plugins."""
            ...

    @runtime_checkable
    class Validation(Protocol):
        """Protocol for plugin validation operations."""

        def validate_plugin_compatibility(self, plugin_name: str) -> bool:
            """Validate plugin compatibility."""
            ...

        def validate_plugin_dependencies(self, plugin_name: str) -> bool:
            """Validate plugin dependencies."""
            ...

        def validate_plugin_permissions(self, plugin_name: str) -> bool:
            """Validate plugin permissions."""
            ...

        def validate_plugin_structure(self, plugin_data: t.JsonValue) -> bool:
            """Validate plugin structure."""
            ...

    @runtime_checkable
    class Storage(Protocol):
        """Protocol for plugin storage operations."""

        def delete_plugin(self, plugin_name: str) -> bool:
            """Delete stored plugin."""
            ...

        def list_stored_plugins(self) -> t.StrSequence:
            """List all stored plugin names."""
            ...

        def plugin_exists(self, plugin_name: str) -> bool:
            """Check if plugin is stored."""
            ...

        def retrieve_plugin(self, plugin_name: str) -> t.JsonValue | None:
            """Retrieve stored plugin data."""
            ...

        def store_plugin(self, plugin_data: t.JsonValue) -> bool:
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

    @runtime_checkable
    class LifecycleHost(Protocol):
        """Structure required by the platform lifecycle operations."""

        @property
        def discovery(self) -> p.Plugin.Discovery | None:
            """The configured discovery protocol implementation."""
            ...

        @property
        def loader(self) -> p.Plugin.Loader | None:
            """The configured loader protocol implementation."""
            ...

        @property
        def registry(
            self,
        ) -> FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.PluginRegistry:
            """The plugin registry."""
            ...

        @property
        def plugins(
            self,
        ) -> t.MappingKV[
            str, FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin
        ]:
            """The registered plugins by name."""
            ...

        def fetch_plugin(
            self, name: str
        ) -> FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin | None:
            """Fetch a plugin by name."""
            ...

        def require_protocol(
            self,
            protocol: p.Plugin.Discovery | p.Plugin.Loader | p.Plugin.Execution | None,
            name: str,
        ) -> p.Result[bool]: ...

        def get_plugin(
            self, name: str
        ) -> p.Result[
            FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin
        ]: ...

        def create_execution(
            self,
            plugin: FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin,
            context: t.JsonMapping,
            execution_id: str | None,
        ) -> p.Result[
            FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.PluginExecution
        ]: ...

        def prepare_execution(
            self,
            execution: (
                FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.PluginExecution
            ),
        ) -> p.Result[
            FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.PluginExecution
        ]: ...

        def execute_with_executor(
            self,
            execution: (
                FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.PluginExecution
            ),
        ) -> p.Result[
            FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.PluginExecution
        ]: ...

        def validate_and_create_plugin(
            self,
            plugin_data: t.JsonMapping,
        ) -> p.Result[
            FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin
        ]: ...

        def validate_and_create_plugins(
            self,
            plugin_data: t.SequenceOf[m.Plugin.DiscoveryData],
        ) -> p.Result[
            Sequence[FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin]
        ]: ...

        def register_all(
            self,
            plugins: t.SequenceOf[
                FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin
            ],
        ) -> t.SequenceOf[
            FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin
        ]: ...

        def register_single(
            self, plugin: FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin
        ) -> FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin: ...

        def add_to_plugins(
            self, plugin: FlextPluginUtilitiesPluginPlatform.FlextPluginPlatform.Plugin
        ) -> bool: ...

        def remove_from_plugins(self, plugin_name: str) -> bool: ...


__all__: list[str] = ["FlextPluginProtocolsPlugin"]
