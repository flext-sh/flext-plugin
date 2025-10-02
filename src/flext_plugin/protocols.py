"""Plugin protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols, FlextResult


class FlextPluginProtocols(FlextProtocols):
    """Plugin protocols extending FlextProtocols with plugin-specific interfaces.

    This class provides protocol definitions for plugin discovery, loading, registration,
    execution, and lifecycle management within the FLEXT plugin ecosystem.
    """

    @runtime_checkable
    class DiscoveryProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for plugin discovery operations."""

        def discover_plugins(self, path: str) -> FlextResult[list[object]]:
            """Discover plugins in the given path.

            Args:
                path: Path to search for plugins

            Returns:
                FlextResult[list[object]]: List of discovered plugins or error
            """
            ...

        def validate_plugin(self, plugin: object) -> FlextResult[bool]:
            """Validate a plugin.

            Args:
                plugin: Plugin to validate

            Returns:
                FlextResult[bool]: Validation success status
            """
            ...

        def scan_directory(
            self, directory: str, *, recursive: bool = True, pattern: str | None = None
        ) -> FlextResult[list[str]]:
            """Scan directory for plugin files.

            Args:
                directory: Directory to scan
                recursive: Scan subdirectories recursively
                pattern: File pattern to match

            Returns:
                FlextResult[list[str]]: List of plugin file paths or error
            """
            ...

        def filter_plugins(
            self, plugins: list[object], criteria: dict[str, object]
        ) -> FlextResult[list[object]]:
            """Filter plugins by criteria.

            Args:
                plugins: List of plugins to filter
                criteria: Filter criteria

            Returns:
                FlextResult[list[object]]: Filtered plugins or error
            """
            ...

    @runtime_checkable
    class LoaderProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for plugin loading operations."""

        def load_plugin(self, plugin_path: str) -> FlextResult[object]:
            """Load plugin from path.

            Args:
                plugin_path: Path to plugin file

            Returns:
                FlextResult[object]: Loaded plugin instance or error
            """
            ...

        def unload_plugin(self, plugin: object) -> FlextResult[bool]:
            """Unload a plugin.

            Args:
                plugin: Plugin to unload

            Returns:
                FlextResult[bool]: Unload success status
            """
            ...

        def reload_plugin(self, plugin: object) -> FlextResult[object]:
            """Reload a plugin.

            Args:
                plugin: Plugin to reload

            Returns:
                FlextResult[object]: Reloaded plugin instance or error
            """
            ...

        def get_plugin_info(self, plugin: object) -> FlextResult[dict[str, object]]:
            """Get plugin information.

            Args:
                plugin: Plugin to get info for

            Returns:
                FlextResult[dict[str, object]]: Plugin information or error
            """
            ...

        def validate_plugin_dependencies(self, plugin: object) -> FlextResult[bool]:
            """Validate plugin dependencies.

            Args:
                plugin: Plugin to validate dependencies for

            Returns:
                FlextResult[bool]: Dependencies validation status
            """
            ...

    @runtime_checkable
    class RegistryProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for plugin registry operations."""

        def register_plugin(
            self, plugin: object, *, name: str | None = None
        ) -> FlextResult[str]:
            """Register a plugin.

            Args:
                plugin: Plugin to register
                name: Optional plugin name

            Returns:
                FlextResult[str]: Plugin ID or error
            """
            ...

        def unregister_plugin(self, plugin_id: str) -> FlextResult[bool]:
            """Unregister a plugin.

            Args:
                plugin_id: Plugin ID to unregister

            Returns:
                FlextResult[bool]: Unregister success status
            """
            ...

        def get_plugin(self, plugin_id: str) -> FlextResult[object]:
            """Get plugin by ID.

            Args:
                plugin_id: Plugin ID

            Returns:
                FlextResult[object]: Plugin instance or error
            """
            ...

        def list_plugins(self) -> FlextResult[list[dict[str, object]]]:
            """List all registered plugins.

            Returns:
                FlextResult[list[dict[str, object]]]: Plugin list or error
            """
            ...

        def find_plugins(
            self,
            *,
            name: str | None = None,
            category: str | None = None,
            version: str | None = None,
        ) -> FlextResult[list[object]]:
            """Find plugins by criteria.

            Args:
                name: Plugin name filter
                category: Plugin category filter
                version: Plugin version filter

            Returns:
                FlextResult[list[object]]: Matching plugins or error
            """
            ...

    @runtime_checkable
    class ExecutorProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for plugin execution operations."""

        def execute_plugin(
            self,
            plugin: object,
            method: str,
            *,
            args: list[object] | None = None,
            kwargs: dict[str, object] | None = None,
        ) -> FlextResult[object]:
            """Execute plugin method.

            Args:
                plugin: Plugin to execute
                method: Method name to execute
                args: Method arguments
                kwargs: Method keyword arguments

            Returns:
                FlextResult[object]: Execution result or error
            """
            ...

        def execute_plugin(
            self,
            plugin: object,
            method: str,
            *,
            args: list[object] | None = None,
            kwargs: dict[str, object] | None = None,
        ) -> FlextResult[object]:
            """Execute plugin method hronously.

            Args:
                plugin: Plugin to execute
                method: Method name to execute
                args: Method arguments
                kwargs: Method keyword arguments

            Returns:
                FlextResult[object]: Execution result or error
            """
            ...

        def get_execution_context(
            self, plugin: object
        ) -> FlextResult[dict[str, object]]:
            """Get plugin execution context.

            Args:
                plugin: Plugin to get context for

            Returns:
                FlextResult[dict[str, object]]: Execution context or error
            """
            ...

        def set_execution_timeout(
            self, plugin: object, timeout: float
        ) -> FlextResult[bool]:
            """Set execution timeout for plugin.

            Args:
                plugin: Plugin to set timeout for
                timeout: Timeout in seconds

            Returns:
                FlextResult[bool]: Success status
            """
            ...

    @runtime_checkable
    class ValidatorProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for plugin validation operations."""

        def validate_plugin_structure(self, plugin: object) -> FlextResult[bool]:
            """Validate plugin structure.

            Args:
                plugin: Plugin to validate

            Returns:
                FlextResult[bool]: Validation success status
            """
            ...

        def validate_plugin_metadata(self, plugin: object) -> FlextResult[bool]:
            """Validate plugin metadata.

            Args:
                plugin: Plugin to validate

            Returns:
                FlextResult[bool]: Validation success status
            """
            ...

        def validate_plugin_interface(
            self, plugin: object, interface: type
        ) -> FlextResult[bool]:
            """Validate plugin implements required interface.

            Args:
                plugin: Plugin to validate
                interface: Required interface

            Returns:
                FlextResult[bool]: Validation success status
            """
            ...

        def validate_plugin_configuration(
            self, plugin: object, config: dict[str, object]
        ) -> FlextResult[bool]:
            """Validate plugin configuration.

            Args:
                plugin: Plugin to validate
                config: Configuration to validate

            Returns:
                FlextResult[bool]: Validation success status
            """
            ...

    @runtime_checkable
    class HotReloadProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for plugin hot reload operations."""

        def enable_hot_reload(
            self, plugin: object, *, watch_path: str | None = None
        ) -> FlextResult[bool]:
            """Enable hot reload for plugin.

            Args:
                plugin: Plugin to enable hot reload for
                watch_path: Path to watch for changes

            Returns:
                FlextResult[bool]: Success status
            """
            ...

        def disable_hot_reload(self, plugin: object) -> FlextResult[bool]:
            """Disable hot reload for plugin.

            Args:
                plugin: Plugin to disable hot reload for

            Returns:
                FlextResult[bool]: Success status
            """
            ...

        def reload_on_change(
            self, plugin: object, file_path: str
        ) -> FlextResult[object]:
            """Reload plugin when file changes.

            Args:
                plugin: Plugin to reload
                file_path: Changed file path

            Returns:
                FlextResult[object]: Reloaded plugin or error
            """
            ...

        def get_watch_status(self, plugin: object) -> FlextResult[dict[str, object]]:
            """Get plugin watch status.

            Args:
                plugin: Plugin to get status for

            Returns:
                FlextResult[dict[str, object]]: Watch status or error
            """
            ...

    @runtime_checkable
    class ManagerProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for plugin management operations."""

        def initialize_plugin_system(
            self, config: dict[str, object]
        ) -> FlextResult[bool]:
            """Initialize plugin system.

            Args:
                config: System configuration

            Returns:
                FlextResult[bool]: Initialization success status
            """
            ...

        def shutdown_plugin_system(self) -> FlextResult[bool]:
            """Shutdown plugin system.

            Returns:
                FlextResult[bool]: Shutdown success status
            """
            ...

        def get_system_status(self) -> FlextResult[dict[str, object]]:
            """Get plugin system status.

            Returns:
                FlextResult[dict[str, object]]: System status or error
            """
            ...

        def configure_plugin(
            self, plugin: object, config: dict[str, object]
        ) -> FlextResult[bool]:
            """Configure a plugin.

            Args:
                plugin: Plugin to configure
                config: Configuration settings

            Returns:
                FlextResult[bool]: Configuration success status
            """
            ...

        def get_plugin_statistics(self) -> FlextResult[dict[str, object]]:
            """Get plugin system statistics.

            Returns:
                FlextResult[dict[str, object]]: Statistics or error
            """
            ...

    # Convenience aliases for easier downstream usage
    PluginDiscoveryProtocol = DiscoveryProtocol
    PluginLoaderProtocol = LoaderProtocol
    PluginRegistryProtocol = RegistryProtocol
    PluginExecutorProtocol = ExecutorProtocol
    PluginValidatorProtocol = ValidatorProtocol
    PluginHotReloadProtocol = HotReloadProtocol
    PluginManagerProtocol = ManagerProtocol


__all__ = [
    "FlextPluginProtocols",
]
