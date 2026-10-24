"""Plugin domain protocols for flext-plugin.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from flext_plugin import m, p, t


class FlextPluginProtocolsPlugin:
    """Namespace of the plugin-domain protocol contracts.

    Groups the discovery, loading, execution, security,
    hot-reload, monitoring, configuration, lifecycle, validation, and
    storage protocols plus the owned plugin and execution payload contracts.

    """

    @runtime_checkable
    class Instance(p.Model, Protocol):
        """Owned plugin payload capabilities consumed by lifecycle services."""

        @property
        def name(self) -> str: ...

        @property
        def plugin_version(self) -> str: ...

        @property
        def is_enabled(self) -> bool: ...

        @property
        def metadata(self) -> t.JsonMapping: ...

    @runtime_checkable
    class Run(Protocol):
        """Observable execution record, independent of its concrete model."""

        @property
        def plugin_name(self) -> str: ...

        @property
        def execution_id(self) -> str: ...

        @property
        def input_data(self) -> t.JsonMapping: ...

        @property
        def is_running(self) -> bool: ...

        @property
        def is_completed(self) -> bool: ...

        @property
        def success(self) -> bool: ...

        @property
        def error_message(self) -> str | None: ...

        @property
        def result(self) -> t.JsonMapping | None: ...

        @property
        def started_at(self) -> str | None: ...

        @property
        def completed_at(self) -> str | None: ...

    @runtime_checkable
    class Snapshot(Protocol):
        """Transport snapshot returned by platform execution."""

        @property
        def version(self) -> str: ...

        @property
        def plugins(self) -> t.JsonMapping: ...

    @runtime_checkable
    class Discovery(Protocol):
        """Protocol for plugin discovery operations."""

        def discover_plugin(self, plugin_path: str) -> p.Result[m.Plugin.DiscoveryData]:
            """Discover a single plugin at the specified path.

            Args:
                plugin_path: Filesystem path of the plugin module.

            Returns:
                Ok with the discovery data, or Fail with the discovery error.

            """
            ...

        def discover_plugins(
            self,
            paths: t.StrSequence,
        ) -> p.Result[t.SequenceOf[m.Plugin.DiscoveryData]]:
            """Discover plugins at the given paths.

            Args:
                paths: Filesystem paths to scan for plugin modules.

            Returns:
                Ok with the discovery data records, or Fail with the
                discovery error.

            """
            ...

        def validate_plugin(
            self,
            plugin_data: m.Plugin.DiscoveryData,
        ) -> p.Result[bool]:
            """Validate plugin discovery data.

            Args:
                plugin_data: Discovery data to validate.

            Returns:
                Ok with ``True`` when the data is valid, or Fail with the
                validation error.

            """
            ...

    @runtime_checkable
    class Loader(Protocol):
        """Protocol for plugin loading operations."""

        def get_loaded_plugins(self) -> t.StrSequence:
            """List the currently loaded plugin names.

            Returns:
                Names of all currently loaded plugins.

            """
            ...

        def plugin_loaded(self, plugin_name: str) -> bool:
            """Check whether a plugin is currently loaded.

            Args:
                plugin_name: Name of the plugin to check.

            Returns:
                ``True`` when the plugin is loaded, ``False`` otherwise.

            """
            ...

        def load_plugin(self, plugin_path: str) -> p.Result[t.JsonMapping]:
            """Load a plugin from the specified path.

            Args:
                plugin_path: Filesystem path of the plugin module.

            Returns:
                Ok with the plugin metadata, or Fail with the load error.

            """
            ...

        def unload_plugin(self, plugin_name: str) -> p.Result[bool]:
            """Unload a previously loaded plugin.

            Args:
                plugin_name: Name of the plugin to unload.

            Returns:
                Ok with ``True`` when the plugin is unloaded, or Fail with
                the unload error.

            """
            ...

    @runtime_checkable
    class Execution(Protocol):
        """Protocol for plugin execution operations."""

        def execute_plugin(
            self,
            plugin_name: str,
            context: t.JsonMapping,
        ) -> p.Result[t.JsonMapping]:
            """Execute a plugin with the given context.

            Args:
                plugin_name: Name of the registered plugin to run.
                context: Input payload passed to the plugin entry point.

            Returns:
                Ok with the execution result payload, or Fail with the
                execution error.

            """
            ...

        def get_execution_status(self, execution_id: str) -> p.Result[str]:
            """Fetch the status of an execution.

            Args:
                execution_id: Identifier of the execution to inspect.

            Returns:
                Ok with the status string, or Fail when the execution is
                unknown.

            """
            ...

        def list_running_executions(self) -> t.StrSequence:
            """List all currently running execution ids.

            Returns:
                Identifiers of the currently running executions.

            """
            ...

        def stop_execution(self, execution_id: str) -> p.Result[bool]:
            """Stop a running execution.

            Args:
                execution_id: Identifier of the execution to stop.

            Returns:
                Ok with ``True`` when the execution stops, or Fail with
                the stop error.

            """
            ...

    @runtime_checkable
    class Security(Protocol):
        """Protocol for plugin security operations."""

        def check_permissions(
            self,
            plugin_name: str,
            permissions: t.StrSequence,
        ) -> bool:
            """Check whether a plugin has the specified permissions.

            Args:
                plugin_name: Name of the plugin to check.
                permissions: Permission identifiers to verify.

            Returns:
                ``True`` when the plugin holds all permissions, ``False``
                otherwise.

            """
            ...

        def get_security_level(self, plugin_name: str) -> str:
            """Fetch the security level of a plugin.

            Args:
                plugin_name: Name of the plugin to inspect.

            Returns:
                The security level assigned to the plugin.

            """
            ...

        def scan_plugin_security(self, plugin_path: str) -> t.JsonMapping:
            """Scan a plugin for security vulnerabilities.

            Args:
                plugin_path: Filesystem path of the plugin module.

            Returns:
                The scan findings payload.

            """
            ...

        def validate_plugin_security(self, plugin: m.Plugin.Entity) -> bool:
            """Validate plugin security compliance.

            Args:
                plugin: Plugin entity to validate.

            Returns:
                ``True`` when the plugin complies with security policy,
                ``False`` otherwise.

            """
            ...

    @runtime_checkable
    class HotReload(Protocol):
        """Protocol for hot reload operations."""

        def get_watched_paths(self) -> t.StrSequence:
            """List the currently watched paths.

            Returns:
                Paths watched for plugin changes.

            """
            ...

        def watching(self) -> bool:
            """Check whether changes are currently being watched.

            Returns:
                ``True`` when watching is active, ``False`` otherwise.

            """
            ...

        def reload_plugin(self, plugin_name: str) -> bool:
            """Reload a plugin.

            Args:
                plugin_name: Name of the plugin to reload.

            Returns:
                ``True`` when the plugin reloads, ``False`` otherwise.

            """
            ...

        def start_watching(self, paths: t.StrSequence) -> bool:
            """Start watching paths for plugin changes.

            Args:
                paths: Filesystem paths to watch.

            Returns:
                ``True`` when watching starts, ``False`` otherwise.

            """
            ...

        def stop_watching(self) -> bool:
            """Stop watching for plugin changes.

            Returns:
                ``True`` when watching stops, ``False`` otherwise.

            """
            ...

    @runtime_checkable
    class Monitoring(Protocol):
        """Protocol for plugin monitoring operations."""

        def fetch_plugin_health(self, plugin_name: str) -> t.JsonMapping:
            """Fetch the health status of a plugin.

            Args:
                plugin_name: Name of the plugin to inspect.

            Returns:
                The health status payload.

            """
            ...

        def fetch_plugin_metrics(self, plugin_name: str) -> t.JsonMapping:
            """Fetch metrics for a plugin.

            Args:
                plugin_name: Name of the plugin to inspect.

            Returns:
                The plugin metrics payload.

            """
            ...

        def monitoring(self, plugin_name: str) -> bool:
            """Check whether a plugin is being monitored.

            Args:
                plugin_name: Name of the plugin to check.

            Returns:
                ``True`` when the plugin is monitored, ``False`` otherwise.

            """
            ...

        def start_monitoring(self, plugin_name: str) -> bool:
            """Start monitoring a plugin.

            Args:
                plugin_name: Name of the plugin to monitor.

            Returns:
                ``True`` when monitoring starts, ``False`` otherwise.

            """
            ...

        def stop_monitoring(self, plugin_name: str) -> bool:
            """Stop monitoring a plugin.

            Args:
                plugin_name: Name of the plugin to stop monitoring.

            Returns:
                ``True`` when monitoring stops, ``False`` otherwise.

            """
            ...

    @runtime_checkable
    class Configuration(Protocol):
        """Protocol for plugin configuration operations."""

        def fetch_default_config(self, plugin_type: str) -> t.JsonValue:
            """Fetch the default configuration for a plugin type.

            Args:
                plugin_type: Plugin type whose defaults to fetch.

            Returns:
                The default configuration payload.

            """
            ...

        def load_config(self, plugin_name: str) -> t.JsonValue:
            """Load the configuration for a plugin.

            Args:
                plugin_name: Name of the plugin whose configuration to load.

            Returns:
                The plugin configuration payload.

            """
            ...

        def save_config(self, plugin_name: str, settings: t.JsonValue) -> bool:
            """Save the configuration for a plugin.

            Args:
                plugin_name: Name of the plugin to configure.
                settings: Configuration payload to persist.

            Returns:
                ``True`` when the configuration is saved, ``False``
                otherwise.

            """
            ...

        def validate_config(self, settings: t.JsonValue) -> bool:
            """Validate a plugin configuration payload.

            Args:
                settings: Configuration payload to validate.

            Returns:
                ``True`` when the payload is valid, ``False`` otherwise.

            """
            ...

    @runtime_checkable
    class Lifecycle(Protocol):
        """Protocol for plugin lifecycle operations."""

        def activate_plugin(self, plugin_name: str) -> bool:
            """Activate a plugin.

            Args:
                plugin_name: Name of the plugin to activate.

            Returns:
                ``True`` when the plugin activates, ``False`` otherwise.

            """
            ...

        def deactivate_plugin(self, plugin_name: str) -> bool:
            """Deactivate a plugin.

            Args:
                plugin_name: Name of the plugin to deactivate.

            Returns:
                ``True`` when the plugin deactivates, ``False`` otherwise.

            """
            ...

        def destroy_plugin(self, plugin_name: str) -> bool:
            """Destroy a plugin.

            Args:
                plugin_name: Name of the plugin to destroy.

            Returns:
                ``True`` when the plugin is destroyed, ``False`` otherwise.

            """
            ...

        def fetch_plugin_status(self, plugin_name: str) -> str:
            """Fetch the status of a plugin.

            Args:
                plugin_name: Name of the plugin to inspect.

            Returns:
                The status string of the plugin.

            """
            ...

        def initialize_plugin(self, plugin_name: str) -> bool:
            """Initialize a plugin.

            Args:
                plugin_name: Name of the plugin to initialize.

            Returns:
                ``True`` when the plugin initializes, ``False`` otherwise.

            """
            ...

        def list_plugin_statuses(self) -> t.StrMapping:
            """Fetch the status of every plugin.

            Returns:
                Mapping of plugin name to status string.

            """
            ...

    @runtime_checkable
    class Validation(Protocol):
        """Protocol for plugin validation operations."""

        def validate_plugin_compatibility(self, plugin_name: str) -> bool:
            """Validate plugin compatibility.

            Args:
                plugin_name: Name of the plugin to validate.

            Returns:
                ``True`` when the plugin is compatible, ``False`` otherwise.

            """
            ...

        def validate_plugin_dependencies(self, plugin_name: str) -> bool:
            """Validate plugin dependencies.

            Args:
                plugin_name: Name of the plugin to validate.

            Returns:
                ``True`` when all dependencies are satisfied, ``False``
                otherwise.

            """
            ...

        def validate_plugin_permissions(self, plugin_name: str) -> bool:
            """Validate plugin permissions.

            Args:
                plugin_name: Name of the plugin to validate.

            Returns:
                ``True`` when the permissions are valid, ``False``
                otherwise.

            """
            ...

        def validate_plugin_structure(self, plugin_data: t.JsonValue) -> bool:
            """Validate plugin structure.

            Args:
                plugin_data: Plugin payload to validate.

            Returns:
                ``True`` when the structure is valid, ``False`` otherwise.

            """
            ...

    @runtime_checkable
    class Storage(Protocol):
        """Protocol for plugin storage operations."""

        def delete_plugin(self, plugin_name: str) -> bool:
            """Delete a stored plugin.

            Args:
                plugin_name: Name of the plugin to delete.

            Returns:
                ``True`` when the plugin is deleted, ``False`` otherwise.

            """
            ...

        def list_stored_plugins(self) -> t.StrSequence:
            """List all stored plugin names.

            Returns:
                Names of the stored plugins.

            """
            ...

        def plugin_exists(self, plugin_name: str) -> bool:
            """Check whether a plugin is stored.

            Args:
                plugin_name: Name of the plugin to check.

            Returns:
                ``True`` when the plugin is stored, ``False`` otherwise.

            """
            ...

        def retrieve_plugin(self, plugin_name: str) -> t.JsonValue | None:
            """Retrieve stored plugin data.

            Args:
                plugin_name: Name of the plugin to retrieve.

            Returns:
                The stored plugin payload, or ``None`` when nothing is
                stored under the name.

            """
            ...

        def store_plugin(self, plugin_data: t.JsonValue) -> bool:
            """Store plugin data.

            Args:
                plugin_data: Plugin payload to store.

            Returns:
                ``True`` when the payload is stored, ``False`` otherwise.

            """
            ...

    @runtime_checkable
    class DiscoveryStrategy(Protocol):
        """Strategy protocol for plugin discovery."""

        def discover(
            self,
            paths: t.StrSequence,
        ) -> p.Result[t.SequenceOf[m.Plugin.DiscoveryData]]:
            """Discover plugins using this strategy.

            Args:
                paths: Filesystem paths to scan for plugin modules.

            Returns:
                Ok with the discovery data records, or Fail with the
                discovery error.

            """
            ...


__all__: list[str] = ["FlextPluginProtocolsPlugin"]
