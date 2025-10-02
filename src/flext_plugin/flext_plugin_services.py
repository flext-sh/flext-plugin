"""FLEXT Plugin Services - Single CONSOLIDATED Class Following FLEXT Patterns.

This module implements the CONSOLIDATED service pattern with a single FlextPluginServices
class containing ALL plugin service definitions as nested classes. Maintains backward
compatibility through property re-exports and follows FLEXT architectural standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar, override

from flext_core import (
    FlextContainer,
    FlextExceptions,
    FlextResult,
    FlextService,
    FlextTypes,
)
from flext_plugin.entities import FlextPluginConfig, FlextPluginEntity
from flext_plugin.ports import (
    FlextPluginDiscoveryPort,
    FlextPluginLoaderPort,
    FlextPluginManagerPort,
)


class FlextPluginServices(FlextService[object]):
    """Single CONSOLIDATED class containing ALL plugin services.

    Consolidates ALL service definitions into one class following FLEXT patterns.
    Individual services available as nested classes for organization while maintaining
    backward compatibility through direct exports.

    This approach follows FLEXT architectural standards for single consolidated classes
    per module while preserving existing API surface for seamless migration.
    """

    class PluginService(FlextService[object]):
        """Core plugin management service orchestrating plugin lifecycle operations.

        Application service providing comprehensive plugin management capabilities
        through coordination of domain entities and infrastructure ports. Implements
        the application layer of Clean Architecture, handling use cases and workflows
        without containing business logic.
        """

        container: FlextContainer
        model_config: ClassVar = {"arbitrary_types_allowed": "True", "frozen": "False"}

        def __init__(self, **kwargs: object) -> None:
            """Initialize plugin management service with dependency injection container."""
            # Extract container from kwargs or create default
            container_arg = kwargs.pop("container", None)
            if container_arg is not None and isinstance(container_arg, FlextContainer):
                container = container_arg
            else:
                container = FlextContainer()

            # Initialize Pydantic model with container field
            super().__init__(**kwargs)
            object.__setattr__(self, "container", container)
            object.__setattr__(self, "_discovery_port", None)
            object.__setattr__(self, "_loader_port", None)
            object.__setattr__(self, "_manager_port", None)

        @override
        def execute(self: object) -> FlextResult[object]:
            """Execute service operation (required by FlextService)."""
            return FlextResult[object].fail(
                "Use specific service methods instead of execute",
            )

        @property
        def discovery_port(self: object) -> FlextPluginDiscoveryPort:
            """Get plugin discovery port."""
            discovery_port = getattr(self, "_discovery_port", None)
            if discovery_port is None:
                result: FlextResult[object] = self.container.get(
                    "plugin_discovery_port"
                )
                if result.success and isinstance(result.data, FlextPluginDiscoveryPort):
                    discovery_port_data: FlextPluginDiscoveryPort = result.data
                    setattr(self, "_discovery_port", discovery_port_data)
                    return discovery_port_data
            if isinstance(discovery_port, FlextPluginDiscoveryPort):
                return discovery_port

            # FLEXT COMPLIANCE: No mocks allowed - fail fast if port not configured
            msg = "Plugin discovery port not configured in container"
            raise FlextExceptions.BaseError(msg)

        @property
        def loader_port(self: object) -> FlextPluginLoaderPort:
            """Get plugin loader port."""
            loader_port = getattr(self, "_loader_port", None)
            if loader_port is None:
                result: FlextResult[object] = self.container.get("plugin_loader_port")
                if result.success and isinstance(result.data, FlextPluginLoaderPort):
                    loader_port_data: FlextPluginLoaderPort = result.data
                    setattr(self, "_loader_port", loader_port_data)
                    return loader_port_data
            if isinstance(loader_port, FlextPluginLoaderPort):
                return loader_port

            # FLEXT COMPLIANCE: No mocks allowed - fail fast if port not configured
            msg = "Plugin loader port not configured in container"
            raise FlextExceptions.BaseError(msg)

        @property
        def manager_port(self: object) -> FlextPluginManagerPort:
            """Get plugin manager port."""
            manager_port = getattr(self, "_manager_port", None)
            if manager_port is None:
                result: FlextResult[object] = self.container.get("plugin_manager_port")
                if result.success and isinstance(result.data, FlextPluginManagerPort):
                    manager_port_data: FlextPluginManagerPort = result.data
                    setattr(self, "_manager_port", manager_port_data)
                    return manager_port_data
            if isinstance(manager_port, FlextPluginManagerPort):
                return manager_port

            # FLEXT COMPLIANCE: No mocks allowed - fail fast if port not configured
            msg = "Plugin manager port not configured in container"
            raise FlextExceptions.BaseError(msg)

        def discover_plugins(self, path: str) -> FlextResult[list[FlextPluginEntity]]:
            """Discover plugins in the given path."""
            try:
                if not path:
                    return FlextResult[list[FlextPluginEntity]].fail(
                        "Path is required for plugin discovery",
                    )
                return self.discovery_port.discover_plugins(path)
            except (RuntimeError, ValueError, TypeError) as e:
                return FlextResult[list[FlextPluginEntity]].fail(
                    f"Failed to discover plugins: {e}",
                )

        def load_plugin(self, plugin: FlextPluginEntity) -> FlextResult[bool]:
            """Load a plugin."""
            try:
                if not plugin.is_valid():
                    return FlextResult[bool].fail("Invalid plugin")
                # Validate plugin first
                validation_result: FlextResult[object] = (
                    self.discovery_port.validate_plugin(plugin)
                )
                validation_data: bool = (
                    validation_result.data
                    if validation_result.data is not None
                    else False
                )
                if not validation_result.success or not validation_data:
                    return FlextResult[bool].fail("Plugin validation failed")
                return self.loader_port.load_plugin(plugin)
            except (
                RuntimeError,
                ValueError,
                TypeError,
                FlextExceptions.BaseError,
            ) as e:
                return FlextResult[bool].fail(f"Failed to load plugin: {e}")

        def unload_plugin(self, plugin_name: str) -> FlextResult[bool]:
            """Unload a plugin."""
            try:
                if not plugin_name:
                    return FlextResult[bool].fail("Plugin name is required")
                return self.loader_port.unload_plugin(plugin_name)
            except (
                RuntimeError,
                ValueError,
                TypeError,
                FlextExceptions.BaseError,
            ) as e:
                return FlextResult[bool].fail(f"Failed to unload plugin: {e}")

        def install_plugin(self, plugin_path: str) -> FlextResult[FlextPluginEntity]:
            """Install a plugin from the given path."""
            try:
                if not plugin_path:
                    return FlextResult[FlextPluginEntity].fail(
                        "Plugin path is required",
                    )
                return self.manager_port.install_plugin(plugin_path)
            except (RuntimeError, ValueError, TypeError) as e:
                return FlextResult[FlextPluginEntity].fail(
                    f"Failed to install plugin: {e}",
                )

        def uninstall_plugin(self, plugin_name: str) -> FlextResult[bool]:
            """Uninstall a plugin."""
            try:
                if not plugin_name:
                    return FlextResult[bool].fail("Plugin name is required")
                return self.manager_port.uninstall_plugin(plugin_name)
            except (RuntimeError, ValueError, TypeError) as e:
                return FlextResult[bool].fail(f"Failed to uninstall plugin: {e}")

        def enable_plugin(self, plugin_name: str) -> FlextResult[bool]:
            """Enable a plugin."""
            try:
                if not plugin_name:
                    return FlextResult[bool].fail("Plugin name is required")
                return self.manager_port.enable_plugin(plugin_name)
            except (RuntimeError, ValueError, TypeError) as e:
                return FlextResult[bool].fail(f"Failed to enable plugin: {e}")

        def disable_plugin(self, plugin_name: str) -> FlextResult[bool]:
            """Disable a plugin."""
            try:
                if not plugin_name:
                    return FlextResult[bool].fail("Plugin name is required")
                return self.manager_port.disable_plugin(plugin_name)
            except (RuntimeError, ValueError, TypeError) as e:
                return FlextResult[bool].fail(f"Failed to disable plugin: {e}")

        def get_plugin_config(self, plugin_name: str) -> FlextResult[FlextPluginConfig]:
            """Get configuration for a plugin."""
            try:
                if not plugin_name:
                    return FlextResult[FlextPluginConfig].fail(
                        "Plugin name is required",
                    )
                return self.manager_port.get_plugin_config(plugin_name)
            except (RuntimeError, ValueError, TypeError) as e:
                return FlextResult[FlextPluginConfig].fail(
                    f"Failed to get plugin config: {e}",
                )

        def update_plugin_config(
            self,
            plugin_name: str,
            config: FlextPluginConfig,
        ) -> FlextResult[bool]:
            """Update configuration for a plugin."""
            try:
                if not plugin_name:
                    return FlextResult[bool].fail("Plugin name is required")
                if not config.is_valid():
                    return FlextResult[bool].fail("Invalid plugin configuration")
                return self.manager_port.update_plugin_config(plugin_name, config)
            except (RuntimeError, ValueError, TypeError) as e:
                return FlextResult[bool].fail(f"Failed to update plugin config: {e}")

        def is_plugin_loaded(self, plugin_name: str) -> FlextResult[bool]:
            """Check if a plugin is loaded."""
            try:
                if not plugin_name:
                    return FlextResult[bool].fail("Plugin name is required")
                return self.loader_port.is_plugin_loaded(plugin_name)
            except (RuntimeError, ValueError, TypeError) as e:
                return FlextResult[bool].fail(f"Failed to check plugin status: {e}")

    class DiscoveryService(FlextService[object]):
        """Specialized service for plugin discovery and validation operations."""

        container: FlextContainer
        model_config: ClassVar = {"arbitrary_types_allowed": "True", "frozen": "False"}

        def __init__(self, **kwargs: object) -> None:
            """Initialize plugin discovery service with dependency injection container."""
            # Extract container from kwargs or create default
            container_arg = kwargs.pop("container", None)
            if container_arg is not None and isinstance(container_arg, FlextContainer):
                container = container_arg
            else:
                container = FlextContainer()

            # Initialize Pydantic model
            super().__init__(**kwargs)
            object.__setattr__(self, "container", container)
            # Store private attributes
            object.__setattr__(self, "_discovery_port", None)

        @override
        def execute(self: object) -> FlextResult[object]:
            """Execute service operation (required by FlextService)."""
            return FlextResult[object].fail(
                "Use specific service methods instead of execute",
            )

        @property
        def discovery_port(self: object) -> FlextPluginDiscoveryPort:
            """Get plugin discovery port."""
            discovery_port = getattr(self, "_discovery_port", None)
            if discovery_port is None:
                result: FlextResult[object] = self.container.get(
                    "plugin_discovery_port"
                )
                if result.success and isinstance(result.data, FlextPluginDiscoveryPort):
                    discovery_port_data: FlextPluginDiscoveryPort = result.data
                    setattr(self, "_discovery_port", discovery_port_data)
                    return discovery_port_data
            if isinstance(discovery_port, FlextPluginDiscoveryPort):
                return discovery_port

            # FLEXT COMPLIANCE: No mocks allowed - fail fast if port not configured
            msg = "Plugin discovery port not configured in container"
            raise FlextExceptions.BaseError(msg)

        def scan_directory(
            self,
            directory_path: str,
        ) -> FlextResult[list[FlextPluginEntity]]:
            """Scan directory for plugins."""
            try:
                if not directory_path:
                    return FlextResult[list[FlextPluginEntity]].fail(
                        "Directory path is required",
                    )
                return self.discovery_port.discover_plugins(directory_path)
            except (RuntimeError, ValueError, TypeError) as e:
                return FlextResult[list[FlextPluginEntity]].fail(
                    f"Failed to scan directory: {e}",
                )

        def validate_plugin_integrity(
            self,
            plugin: FlextPluginEntity | None,
        ) -> FlextResult[bool]:
            """Validate plugin integrity."""
            try:
                if not plugin:
                    return FlextResult[bool].fail("Plugin is required")
                return self.discovery_port.validate_plugin(plugin)
            except (
                RuntimeError,
                ValueError,
                TypeError,
                FlextExceptions.BaseError,
            ) as e:
                return FlextResult[bool].fail(f"Failed to validate plugin: {e}")

    class RegistryService(FlextService[object]):
        """Simple plugin registry service for legacy compatibility."""

        container: FlextContainer
        model_config: ClassVar = {"arbitrary_types_allowed": "True", "frozen": "False"}

        def __init__(self, **kwargs: object) -> None:
            """Initialize plugin registry service."""
            # Extract container from kwargs or create default
            container_arg = kwargs.pop("container", None)
            if container_arg is not None and isinstance(container_arg, FlextContainer):
                container = container_arg
            else:
                container = FlextContainer()

            # Initialize Pydantic model
            super().__init__(**kwargs)
            object.__setattr__(self, "container", container)
            # Store private registry
            object.__setattr__(self, "_plugins", {})

        @override
        def execute(self: object) -> FlextResult[object]:
            """Execute service operation (required by FlextService)."""
            return FlextResult[object].fail(
                "Use specific service methods instead of execute",
            )

        def register_plugin(
            self,
            plugin: FlextPluginEntity,
        ) -> FlextResult[FlextPluginEntity]:
            """Register plugin instance ensuring required fields."""
            try:
                if not hasattr(plugin, "name"):
                    return FlextResult[FlextPluginEntity].fail(
                        "Plugin registration failed: missing name",
                    )
                plugins: dict[str, FlextPluginEntity] = getattr(self, "_plugins", {})
                plugin_name: str = plugin.name
                plugins[plugin_name] = plugin
                return FlextResult[FlextPluginEntity].ok(plugin)
            except Exception as e:
                return FlextResult[FlextPluginEntity].fail(
                    f"Plugin registration failed: {e}",
                )

        def unregister_plugin(self, plugin_name: str) -> FlextResult[bool]:
            """Unregister plugin by name."""
            plugins: dict[str, FlextPluginEntity] = getattr(self, "_plugins", {})
            plugins.pop(plugin_name, None)
            return FlextResult[bool].ok(data=True)

        def get_plugin(self, plugin_name: str) -> FlextPluginEntity | None:
            """Get plugin instance by name."""
            plugins: dict[str, FlextPluginEntity] = getattr(self, "_plugins", {})
            return plugins.get(plugin_name)

        def get_plugin_count(self: object) -> int:
            """Return number of registered plugins."""
            plugins: dict[str, FlextPluginEntity] = getattr(self, "_plugins", {})
            return len(plugins)

        def list_plugins(
            self,
            plugin_type: object | None = None,
        ) -> FlextTypes.Core.List:
            """List plugin metadata optionally filtered by type."""
            plugins: dict[str, FlextPluginEntity] = getattr(self, "_plugins", {})
            if plugin_type is None:
                return list(plugins.values())
            return [
                p
                for p in plugins.values()
                if hasattr(p, "plugin_type") and p.plugin_type == plugin_type
            ]

        def cleanup_all(self) -> None:
            """Clear all registered plugins."""
            plugins: dict[str, FlextPluginEntity] = getattr(self, "_plugins", {})
            plugins.clear()


# Export consolidated class and individual services for backward compatibility
FlextPluginService = FlextPluginServices.PluginService
FlextPluginDiscoveryService = FlextPluginServices.DiscoveryService
SimplePluginRegistry = FlextPluginServices.RegistryService

# Legacy aliases
PluginService = FlextPluginService
PluginDiscoveryService = FlextPluginDiscoveryService


def create_plugin_manager(
    _container: object | None = None,
    *,
    _auto_discover: bool = True,
    _security_enabled: bool = True,
) -> SimplePluginRegistry:
    """Legacy factory function for backwards compatibility."""
    return SimplePluginRegistry()


__all__ = [
    # Legacy backward compatibility exports
    "FlextPluginDiscoveryService",
    "FlextPluginService",
    # CONSOLIDATED class (FLEXT pattern)
    "FlextPluginServices",
    "PluginDiscoveryService",
    "PluginService",
    "SimplePluginRegistry",
    "create_plugin_manager",
]
