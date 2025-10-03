"""Plugin protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols, FlextResult, FlextTypes


class FlextPluginProtocols:
    """Unified plugin protocols following FLEXT domain extension pattern.

    This class consolidates plugin management protocols while explicitly
    re-exporting foundation protocols for backward compatibility and clean access.

    Architecture:
        - RE-EXPORTS: Foundation protocols from flext-core for unified access
        - EXTENDS: Plugin-specific protocols in Plugin namespace
        - MAINTAINS: Zero breaking changes through explicit re-export pattern

    Usage:
        from flext_plugin.protocols import FlextPluginProtocols

        # Foundation access (re-exported)
        FlextPluginProtocols.Foundation.ResultProtocol

        # Plugin-specific access
        FlextPluginProtocols.Plugin.DiscoveryProtocol
    """

    # =========================================================================
    # FOUNDATION PROTOCOL RE-EXPORTS (from flext-core)
    # =========================================================================
    # Explicitly re-export foundation protocols for unified access.
    # This maintains backward compatibility while providing clean namespace access.

    Foundation = FlextProtocols.Foundation
    Domain = FlextProtocols.Domain
    Application = FlextProtocols.Application
    Infrastructure = FlextProtocols.Infrastructure
    Extensions = FlextProtocols.Extensions
    Commands = FlextProtocols.Commands

    # =========================================================================
    # PLUGIN-SPECIFIC PROTOCOLS
    # =========================================================================
    # Domain-specific protocols for plugin discovery, loading, registry,
    # execution, validation, hot-reload, and management operations.

    class Plugin:
        """Plugin domain-specific protocols.

        Provides protocols for plugin discovery, loading, registration,
        execution, validation, hot-reload, and lifecycle management.
        """

        @runtime_checkable
        class DiscoveryProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for plugin discovery operations."""

            def discover_plugins(self, path: str) -> FlextResult[FlextTypes.List]:
                """Discover plugins in the given path."""
                ...

            def validate_plugin(self, plugin: object) -> FlextResult[bool]:
                """Validate a plugin."""
                ...

            def scan_directory(
                self,
                directory: str,
                *,
                recursive: bool = True,
                pattern: str | None = None,
            ) -> FlextResult[FlextTypes.StringList]:
                """Scan directory for plugin files."""
                ...

            def filter_plugins(
                self, plugins: FlextTypes.List, criteria: FlextTypes.Dict
            ) -> FlextResult[FlextTypes.List]:
                """Filter plugins by criteria."""
                ...

        @runtime_checkable
        class LoaderProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for plugin loading operations."""

            def load_plugin(self, plugin_path: str) -> FlextResult[object]:
                """Load plugin from path."""
                ...

            def unload_plugin(self, plugin: object) -> FlextResult[bool]:
                """Unload a plugin."""
                ...

            def reload_plugin(self, plugin: object) -> FlextResult[object]:
                """Reload a plugin."""
                ...

            def get_plugin_info(self, plugin: object) -> FlextResult[FlextTypes.Dict]:
                """Get plugin information."""
                ...

            def validate_plugin_dependencies(self, plugin: object) -> FlextResult[bool]:
                """Validate plugin dependencies."""
                ...

        @runtime_checkable
        class RegistryProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for plugin registry operations."""

            def register_plugin(
                self, plugin: object, *, name: str | None = None
            ) -> FlextResult[str]:
                """Register a plugin."""
                ...

            def unregister_plugin(self, plugin_id: str) -> FlextResult[bool]:
                """Unregister a plugin."""
                ...

            def get_plugin(self, plugin_id: str) -> FlextResult[object]:
                """Get plugin by ID."""
                ...

            def list_plugins(self) -> FlextResult[list[FlextTypes.Dict]]:
                """List all registered plugins."""
                ...

            def find_plugins(
                self,
                *,
                name: str | None = None,
                category: str | None = None,
                version: str | None = None,
            ) -> FlextResult[FlextTypes.List]:
                """Find plugins by criteria."""
                ...

        @runtime_checkable
        class ExecutorProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for plugin execution operations."""

            def execute_plugin(
                self,
                plugin: object,
                method: str,
                *,
                args: FlextTypes.List | None = None,
                kwargs: FlextTypes.Dict | None = None,
            ) -> FlextResult[object]:
                """Execute plugin method."""
                ...

            def get_execution_context(
                self, plugin: object
            ) -> FlextResult[FlextTypes.Dict]:
                """Get plugin execution context."""
                ...

            def set_execution_timeout(
                self, plugin: object, timeout: float
            ) -> FlextResult[bool]:
                """Set execution timeout for plugin."""
                ...

        @runtime_checkable
        class ValidatorProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for plugin validation operations."""

            def validate_plugin_structure(self, plugin: object) -> FlextResult[bool]:
                """Validate plugin structure."""
                ...

            def validate_plugin_metadata(self, plugin: object) -> FlextResult[bool]:
                """Validate plugin metadata."""
                ...

            def validate_plugin_interface(
                self, plugin: object, interface: type
            ) -> FlextResult[bool]:
                """Validate plugin implements required interface."""
                ...

            def validate_plugin_configuration(
                self, plugin: object, config: FlextTypes.Dict
            ) -> FlextResult[bool]:
                """Validate plugin configuration."""
                ...

        @runtime_checkable
        class HotReloadProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for plugin hot reload operations."""

            def enable_hot_reload(
                self, plugin: object, *, watch_path: str | None = None
            ) -> FlextResult[bool]:
                """Enable hot reload for plugin."""
                ...

            def disable_hot_reload(self, plugin: object) -> FlextResult[bool]:
                """Disable hot reload for plugin."""
                ...

            def reload_on_change(
                self, plugin: object, file_path: str
            ) -> FlextResult[object]:
                """Reload plugin when file changes."""
                ...

            def get_watch_status(self, plugin: object) -> FlextResult[FlextTypes.Dict]:
                """Get plugin watch status."""
                ...

        @runtime_checkable
        class ManagerProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for plugin management operations."""

            def initialize_plugin_system(
                self, config: FlextTypes.Dict
            ) -> FlextResult[bool]:
                """Initialize plugin system."""
                ...

            def shutdown_plugin_system(self) -> FlextResult[bool]:
                """Shutdown plugin system."""
                ...

            def get_system_status(self) -> FlextResult[FlextTypes.Dict]:
                """Get plugin system status."""
                ...

            def configure_plugin(
                self, plugin: object, config: FlextTypes.Dict
            ) -> FlextResult[bool]:
                """Configure a plugin."""
                ...

            def get_plugin_statistics(self) -> FlextResult[FlextTypes.Dict]:
                """Get plugin system statistics."""
                ...

    # =========================================================================
    # BACKWARD COMPATIBILITY ALIASES
    # =========================================================================
    # Maintain existing attribute names for zero breaking changes.

    DiscoveryProtocol = Plugin.DiscoveryProtocol
    LoaderProtocol = Plugin.LoaderProtocol
    RegistryProtocol = Plugin.RegistryProtocol
    ExecutorProtocol = Plugin.ExecutorProtocol
    ValidatorProtocol = Plugin.ValidatorProtocol
    HotReloadProtocol = Plugin.HotReloadProtocol
    ManagerProtocol = Plugin.ManagerProtocol

    # Additional convenience aliases
    PluginDiscoveryProtocol = Plugin.DiscoveryProtocol
    PluginLoaderProtocol = Plugin.LoaderProtocol
    PluginRegistryProtocol = Plugin.RegistryProtocol
    PluginExecutorProtocol = Plugin.ExecutorProtocol
    PluginValidatorProtocol = Plugin.ValidatorProtocol
    PluginHotReloadProtocol = Plugin.HotReloadProtocol
    PluginManagerProtocol = Plugin.ManagerProtocol


__all__ = [
    "FlextPluginProtocols",
]
