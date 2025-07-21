"""Plugin manager system for FLEXT Meltano Enterprise.

This module provides comprehensive plugin lifecycle management, orchestrating
plugin discovery, loading, execution, and integration with the application
container and universal command system.

Architecture:
    docs/architecture/003-plugin-system-architecture/04-hot-reload-system.md
Status: IMPLEMENTING MISSING CRITICAL COMPONENT

Features:
    - Complete plugin lifecycle management
    - Integration with dependency injection container
    - Plugin configuration management and validation
    - Hot-reload capabilities for development
    - Plugin execution orchestration and monitoring

Usage:
    from flext_core.plugins.manager import PluginManager, PluginConfiguration

    manager = PluginManager(container)
    await manager.discover_and_load_plugins()

    result = await manager.execute_plugin("data_processor", input_data)
"""

from __future__ import annotations

import time
import uuid

# Removed: import logging - use flext-infrastructure.monitoring.flext-observability \
# instead
from typing import TYPE_CHECKING, Any

from flext_core.domain.pydantic_base import DomainBaseModel, Field
from flext_core.domain.types import ServiceResult

# Use centralized logger from flext-infrastructure.monitoring.flext-observability
# - ELIMINATE DUPLICATION
from flext_observability.logging import get_logger
from pydantic import ConfigDict

# from flext_observability import get_logger
from flext_plugin.core.context import PluginContext
from flext_plugin.core.discovery import PluginDiscovery
from flext_plugin.core.loader import PluginLoader

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Any

    from flext_core.config import DIContainer

    from flext_plugin.core.types import PluginExecutionResult, PluginType

# Use centralized dependency injection from flext-core - ELIMINATE DUPLICATION
from flext_core.config import get_container


# Simple plugin registry implementation
class SimplePluginRegistry:
    """Simple in-memory plugin registry."""

    def __init__(self) -> None:
        self._plugins: dict[str, Any] = {}

    async def register_plugin(self, plugin: Any) -> ServiceResult[Any]:
        """Register a plugin in the registry."""
        try:
            plugin_name = plugin.metadata.name
            self._plugins[plugin_name] = plugin
            return ServiceResult.ok(plugin)
        except (AttributeError, TypeError, ValueError) as e:
            return ServiceResult.fail(f"Plugin registration failed: {e}")

    async def unregister_plugin(self, plugin_id: str) -> ServiceResult[bool]:
        """Unregister a plugin from the registry."""
        try:
            if plugin_id in self._plugins:
                del self._plugins[plugin_id]
            return ServiceResult.ok(True)
        except (KeyError, ValueError) as e:
            return ServiceResult.fail(f"Plugin unregistration failed: {e}")

    def get_plugin(self, plugin_id: str) -> Any:
        """Get a plugin by ID."""
        return self._plugins.get(plugin_id)

    def get_plugin_count(self) -> int:
        """Get total number of registered plugins."""
        return len(self._plugins)

    def list_plugins(self, plugin_type: Any = None) -> list[Any]:
        """List all registered plugins with optional type filter."""
        plugins = list(self._plugins.values())
        if plugin_type:
            plugins = [
                p
                for p in plugins
                if hasattr(p, "metadata")
                and getattr(p.metadata, "plugin_type", None) == plugin_type
            ]
        return [p.metadata for p in plugins if hasattr(p, "metadata")]

    async def cleanup_all(self) -> None:
        """Cleanup all plugins in the registry."""
        self._plugins.clear()


logger = get_logger(__name__)


class PluginConfiguration(DomainBaseModel):
    """Plugin configuration management."""

    plugin_id: str = Field(description="Plugin identifier")
    enabled: bool = Field(default=True, description="Plugin enabled status")
    configuration: dict[str, Any] = Field(
        default_factory=dict,
        description="Plugin-specific configuration",
    )
    permissions: list[str] = Field(
        default_factory=list,
        description="Plugin permissions",
    )
    auto_load: bool = Field(default=True, description="Auto-load plugin on startup")
    hot_reload: bool = Field(
        default=False,
        description="Enable hot-reload for development",
    )
    priority: int = Field(default=100, description="Plugin loading priority")

    model_config = ConfigDict(extra="allow")  # Allow additional configuration fields


class PluginExecutionContext(DomainBaseModel):
    """Context for plugin execution operations."""

    plugin_id: str = Field(description="Plugin being executed")
    execution_id: str = Field(description="Unique execution identifier")
    input_data: dict[str, Any] = Field(
        default_factory=dict,
        description="Input data for plugin",
    )
    context: dict[str, Any] = Field(
        default_factory=dict,
        description="Execution context",
    )
    timeout_seconds: int | None = Field(default=None, description="Execution timeout")

    model_config = ConfigDict(arbitrary_types_allowed=True)


class PluginManagerResult(DomainBaseModel):
    """Result of plugin manager operations."""

    operation: str = Field(description="Operation performed")
    success: bool = Field(description="Operation success status")
    plugins_affected: list[str] = Field(
        default_factory=list,
        description="Plugins affected by operation",
    )
    execution_time_ms: float = Field(description="Operation execution time")
    details: dict[str, Any] = Field(
        default_factory=dict,
        description="Operation details",
    )
    errors: list[str] = Field(default_factory=list, description="Operation errors")


class PluginManager:
    """Comprehensive plugin lifecycle management system.

    Orchestrates plugin discovery, loading, configuration, execution, and integration
    with the application container for enterprise plugin management.
    """

    def __init__(
        self,
        container: DIContainer | None = None,
        auto_discover: bool = True,
        security_enabled: bool = True,
    ) -> None:
        """Initialize plugin manager with container and configuration."""
        self.container = container or get_container()  # Use centralized container
        self.auto_discover = auto_discover
        self.security_enabled = security_enabled

        self.logger = get_logger(self.__class__.__name__)

        # Initialize plugin subsystems
        self.discovery = PluginDiscovery()
        self.loader = PluginLoader(security_enabled=security_enabled)
        self.registry = SimplePluginRegistry()
        # Security features handled by plugin loader and validation
        self.security_enabled = security_enabled

        # Plugin management state
        self._configurations: dict[str, PluginConfiguration] = {}
        self._execution_contexts: dict[str, PluginExecutionContext] = {}
        self._is_initialized = False

    async def initialize(self) -> ServiceResult[PluginManagerResult]:
        """Initialize the plugin manager and auto-discover plugins if enabled.

        Returns:
            ServiceResult containing PluginManagerResult with initialization details,
            including plugins discovered, execution time, and any errors.

        """
        start_time = time.time()

        self.logger.info(
            "Initializing plugin manager",
            auto_discover=self.auto_discover,
            security_enabled=self.security_enabled,
        )

        try:
            plugins_discovered: list[str] = []
            errors = []

            if self.auto_discover:
                # Discover and load plugins automatically
                discover_result = await self.discover_and_load_plugins()
                if discover_result.is_success and discover_result.data:
                    plugins_discovered = (
                        getattr(discover_result.data, "plugins_affected", []) or []
                    )
                else:
                    error_msg = discover_result.error or "Unknown error"
                    errors.append(f"Auto-discovery failed: {error_msg}")

            self._is_initialized = True
            execution_time_ms = (time.time() - start_time) * 1000

            result = PluginManagerResult(
                operation="initialize",
                success=len(errors) == 0,
                plugins_affected=plugins_discovered,
                execution_time_ms=execution_time_ms,
                details={
                    "auto_discover": self.auto_discover,
                    "security_enabled": self.security_enabled,
                    "plugins_discovered": len(plugins_discovered or []),
                },
                errors=errors,
            )

            self.logger.info(
                "Plugin manager initialized",
                success=result.success,
                plugins_discovered=len(plugins_discovered or []),
                execution_time_ms=execution_time_ms,
            )

            return ServiceResult.ok(result)

        except (
            ImportError,
            AttributeError,
            TypeError,
            ValueError,
            RuntimeError,
            OSError,
        ) as e:
            # Plugin manager initialization failed - ZERO TOLERANCE specific \
            # exception types
            error_msg = f"Plugin manager initialization failed: {e}"
            self.logger.exception(
                "Plugin manager initialization failed",
                error=str(e),
            )
            return ServiceResult.fail(error_msg)

    async def discover_and_load_plugins(
        self,
        plugin_types: Sequence[PluginType] | None = None,
    ) -> ServiceResult[PluginManagerResult]:
        """Discover and load plugins, optionally filtering by plugin types.

        Args:
            plugin_types: Optional sequence of plugin types to filter discovery.
                         If None, all plugin types are discovered.

        Returns:
            ServiceResult containing PluginManagerResult with details about
            plugins discovered, loaded, and any errors encountered.

        """
        start_time = time.time()

        self.logger.info("Discovering and loading plugins", filter_types=plugin_types)

        try:
            plugins_loaded: list[str] = []
            errors = []

            # Discover plugins
            discovered_plugins = await self.discovery.discover_all()
            if not discovered_plugins:
                return ServiceResult.fail("No plugins discovered")

            # Load each discovered plugin
            for plugin_id, discovered_plugin in discovered_plugins.items():
                try:
                    # Create plugin context
                    await self._create_plugin_context(plugin_id)

                    # Get plugin class and instantiate it
                    plugin_class = discovered_plugin.plugin_class
                    plugin = plugin_class()

                    # Register plugin
                    register_result = await self.registry.register_plugin(plugin)
                    if register_result.is_success:
                        if plugins_loaded is not None:
                            plugins_loaded.append(plugin.metadata.name)

                        # Store default configuration
                        self._configurations[plugin.metadata.name] = (
                            PluginConfiguration(
                                plugin_id=plugin.metadata.name,
                            )
                        )

                        self.logger.debug(
                            "Plugin loaded and registered",
                            plugin_id=plugin.metadata.name,
                        )
                    else:
                        errors.append(
                            f"Plugin registration failed for {plugin_id}: "
                            f"{register_result.error}",
                        )

                except (
                    ImportError,
                    AttributeError,
                    TypeError,
                    ValueError,
                    RuntimeError,
                    OSError,
                ) as e:
                    # Plugin loading failed - ZERO TOLERANCE specific exception types
                    error_msg = f"Failed to load plugin {plugin_id}: {e}"
                    errors.append(error_msg)
                    self.logger.exception(
                        "Plugin loading failed",
                        plugin_name=plugin_id,
                        error=str(e),
                    )

            execution_time_ms = (time.time() - start_time) * 1000

            result = PluginManagerResult(
                operation="discover_and_load",
                success=len(errors) == 0,
                plugins_affected=plugins_loaded,
                execution_time_ms=execution_time_ms,
                details={
                    "plugins_discovered": len(discovered_plugins),
                    "plugins_loaded": len(plugins_loaded or []),
                    "plugins_failed": len(errors),
                },
                errors=errors,
            )

            self.logger.info(
                "Plugin discovery and loading completed",
                plugins_loaded=len(plugins_loaded or []),
                plugins_failed=len(errors),
                execution_time_ms=execution_time_ms,
            )

            return ServiceResult.ok(result)

        except (
            ImportError,
            AttributeError,
            TypeError,
            ValueError,
            RuntimeError,
            OSError,
        ):
            # Plugin discovery and loading failed - ZERO TOLERANCE specific \
            # exception types
            error_msg = "Plugin discovery and loading failed"
            self.logger.exception("Plugin discovery and loading failed")
            return ServiceResult.fail(error_msg)

    async def execute_plugin(
        self,
        plugin_id: str,
        input_data: dict[str, Any],
        context: dict[str, Any] | None = None,
    ) -> ServiceResult[PluginExecutionResult]:
        """Execute a loaded plugin with the provided input data and context.

        Args:
            plugin_id: Unique identifier of the plugin to execute.
            input_data: Input data dictionary to pass to the plugin.
            context: Optional execution context dictionary.

        Returns:
            ServiceResult containing PluginExecutionResult with execution
            outcome, results, and metadata.

        """
        execution_id = str(uuid.uuid4())

        self.logger.info(
            "Executing plugin",
            plugin_id=plugin_id,
            execution_id=execution_id,
        )

        try:
            # Get plugin from registry
            plugin = self.registry.get_plugin(plugin_id)
            if not plugin:
                return ServiceResult.fail(
                    f"Plugin {plugin_id} not found or not loaded",
                )

            # Check if plugin is enabled
            config = self._configurations.get(plugin_id)
            if config and not config.enabled:
                return ServiceResult.fail(
                    f"Plugin {plugin_id} is disabled",
                )

            # Create execution context
            execution_context = PluginExecutionContext(
                plugin_id=plugin_id,
                execution_id=execution_id,
                input_data=input_data,
                context=context or {},
            )

            self._execution_contexts[execution_id] = execution_context

            try:
                # Execute plugin
                result = await plugin.execute(input_data, context or {})

                self.logger.info(
                    "Plugin execution completed",
                    plugin_id=plugin_id,
                    execution_id=execution_id,
                    success=result.success,
                )

                return ServiceResult.ok(result)

            finally:
                # Cleanup execution context
                self._execution_contexts.pop(execution_id, None)

        except (
            ImportError,
            AttributeError,
            TypeError,
            ValueError,
            RuntimeError,
            OSError,
            TimeoutError,
        ) as e:
            # Plugin execution failed - ZERO TOLERANCE specific exception types
            error_msg = f"Plugin execution failed: {e}"
            self.logger.exception(
                "Plugin execution failed",
                plugin_id=plugin_id,
                execution_id=execution_id,
                error=str(e),
            )
            return ServiceResult.fail(error_msg)

    async def configure_plugin(
        self,
        plugin_id: str,
        configuration: PluginConfiguration,
    ) -> ServiceResult[None]:
        """Configure a plugin with the provided configuration settings.

        Args:
            plugin_id: Unique identifier of the plugin to configure.
            configuration: PluginConfiguration object with settings to apply.

        Returns:
            ServiceResult indicating success or failure of configuration.

        """
        try:
            # Validate plugin exists
            plugin = self.registry.get_plugin(plugin_id)
            if not plugin:
                return ServiceResult.fail(
                    f"Plugin {plugin_id} not found",
                )

            # Validate configuration
            if configuration.plugin_id != plugin_id:
                return ServiceResult.fail(
                    "Configuration plugin_id mismatch",
                )

            # Store configuration
            self._configurations[plugin_id] = configuration

            self.logger.info(
                "Plugin configured successfully",
                plugin_id=plugin_id,
                enabled=configuration.enabled,
                auto_load=configuration.auto_load,
            )

            return ServiceResult.ok(None)

        except (
            ImportError,
            AttributeError,
            TypeError,
            ValueError,
            RuntimeError,
            OSError,
        ) as e:
            # Plugin configuration failed - ZERO TOLERANCE specific exception types
            error_msg = f"Plugin configuration failed: {e}"
            self.logger.exception(
                "Plugin configuration failed",
                plugin_id=plugin_id,
                error=str(e),
            )
            return ServiceResult.fail(error_msg)

    async def reload_plugin(self, plugin_id: str) -> ServiceResult[None]:
        """Reload a plugin if hot-reload is enabled for development.

        Args:
            plugin_id: Unique identifier of the plugin to reload.

        Returns:
            ServiceResult indicating success or failure of plugin reload.

        """
        try:
            # Check if hot-reload is enabled for plugin
            config = self._configurations.get(plugin_id)
            if config and not config.hot_reload:
                return ServiceResult.fail(
                    f"Hot-reload not enabled for plugin {plugin_id}",
                )

            # Unregister current plugin
            unregister_result = await self.registry.unregister_plugin(plugin_id)
            if not unregister_result.is_success:
                error_message = unregister_result.error or "Unregister failed"
                return ServiceResult.fail(error_message)

            # Get discovered plugin info for reload
            discovered_plugin = self.discovery.get_discovered_plugin(plugin_id)
            if not discovered_plugin:
                return ServiceResult.fail(f"Plugin not discovered: {plugin_id}")

            # Reload plugin
            reload_result = await self.loader.reload_plugin(
                plugin_id,
                discovered_plugin,
            )
            if not hasattr(reload_result, "metadata"):
                return ServiceResult.fail("Plugin reload failed")

            # Re-register reloaded plugin - reload_result is a LoadedPlugin instance
            reloaded_plugin = reload_result
            register_result = await self.registry.register_plugin(reloaded_plugin)
            if not register_result.is_success:
                return ServiceResult.fail(
                    str(register_result.error)
                    if register_result.error
                    else "Register failed",
                )

            self.logger.info("Plugin reloaded successfully", plugin_id=plugin_id)
            return ServiceResult.ok(None)

        except (
            ImportError,
            AttributeError,
            TypeError,
            ValueError,
            RuntimeError,
            OSError,
        ) as e:
            # Plugin reload failed - ZERO TOLERANCE specific exception types
            error_msg = f"Plugin reload failed: {e}"
            self.logger.exception(
                "Plugin reload failed",
                plugin_id=plugin_id,
                error=str(e),
            )
            return ServiceResult.fail(error_msg)

    async def unload_plugin(self, plugin_id: str) -> ServiceResult[None]:
        """Unload a plugin and remove it from the registry.

        Args:
            plugin_id: Unique identifier of the plugin to unload.

        Returns:
            ServiceResult indicating success or failure of plugin unload.

        """
        try:
            # Unregister plugin
            unregister_result = await self.registry.unregister_plugin(plugin_id)
            if not unregister_result.is_success:
                return ServiceResult.fail(
                    str(unregister_result.error)
                    if unregister_result.error
                    else "Unregister failed",
                )

            # Unload plugin - unload_plugin returns None, so just handle exception
            try:
                await self.loader.unload_plugin(plugin_id)
            except Exception as e:
                return ServiceResult.fail(f"Plugin unload failed: {e}")

            # Remove configuration
            self._configurations.pop(plugin_id, None)

            self.logger.info("Plugin unloaded successfully", plugin_id=plugin_id)
            return ServiceResult.ok(None)

        except (
            ImportError,
            AttributeError,
            TypeError,
            ValueError,
            RuntimeError,
            OSError,
        ) as e:
            # Plugin unload failed - ZERO TOLERANCE specific exception types
            error_msg = f"Plugin unload failed: {e}"
            self.logger.exception(
                "Plugin unload failed",
                plugin_id=plugin_id,
                error=str(e),
            )
            return ServiceResult.fail(error_msg)

    async def integrate_with_protocols(self) -> ServiceResult[None]:
        """Integrate plugins with universal command system and other protocols.

        Returns:
            ServiceResult indicating success or failure of protocol integration.

        """
        try:
            # Integration with universal command system would go here
            # This is a placeholder for future protocol integration

            self.logger.info(
                "Plugin protocol integration completed",
                plugin_count=self.registry.get_plugin_count(),
            )

            return ServiceResult.ok(None)

        except (
            ImportError,
            AttributeError,
            TypeError,
            ValueError,
            RuntimeError,
            OSError,
        ) as e:
            # Plugin protocol integration failed - ZERO TOLERANCE specific \
            # exception types
            error_msg = f"Plugin protocol integration failed: {e}"
            self.logger.exception("Plugin protocol integration failed", error=str(e))
            return ServiceResult.fail(error_msg)

    async def _create_plugin_context(self, plugin_name: str) -> PluginContext:
        # Create basic plugin context
        # In a full implementation, this would inject services from the container
        return PluginContext(
            plugin_name=plugin_name,
            services={},  # Would be populated from DI container
            dependencies={},
            permissions=["read", "execute"],
            security_level="standard",
        )

    def get_plugin_status(self, plugin_id: str) -> dict[str, Any]:
        """Get the current status and metadata of a plugin.

        Args:
            plugin_id: Unique identifier of the plugin to query.

        Returns:
            Dictionary containing plugin status, metadata, configuration,
            and health information.

        """
        plugin = self.registry.get_plugin(plugin_id)
        if not plugin:
            return {"status": "not_found"}

        config = self._configurations.get(plugin_id)

        return {
            "status": "loaded",
            "plugin_id": plugin_id,
            "enabled": config.enabled if config else True,
            "metadata": {
                "name": plugin.metadata.name,
                "version": plugin.metadata.version,
                "type": plugin.metadata.type.value,
                "description": plugin.metadata.description,
            },
            "configuration": config.model_dump() if config else {},
            "is_healthy": True,  # Would check plugin health in full implementation
        }

    def list_plugins(
        self,
        plugin_type: PluginType | None = None,
        enabled_only: bool = False,
    ) -> list[dict[str, Any]]:
        """List all registered plugins with optional filtering.

        Args:
            plugin_type: Optional plugin type to filter results.
            enabled_only: If True, only return enabled plugins.

        Returns:
            List of dictionaries containing plugin information including
            id, name, version, type, description, and configuration status.

        """
        plugins_metadata = self.registry.list_plugins(plugin_type)

        plugin_list = []
        for metadata in plugins_metadata:
            config = self._configurations.get(metadata.id)

            if enabled_only and config and not config.enabled:
                continue

            plugin_info = {
                "plugin_id": metadata.id,
                "name": metadata.name,
                "version": metadata.version,
                "type": metadata.type.value,
                "description": metadata.description,
                "enabled": config.enabled if config else True,
                "auto_load": config.auto_load if config else True,
            }

            plugin_list.append(plugin_info)

        return plugin_list

    async def cleanup(self) -> None:
        """Clean up the plugin manager and all associated resources.

        Unloads all plugins, clears configurations and execution contexts,
        and resets the manager to uninitialized state.
        """
        self.logger.info("Cleaning up plugin manager")

        try:
            # Cleanup all subsystems
            if hasattr(self.registry, "cleanup_all"):
                await self.registry.cleanup_all()
            # Loader cleanup - not available in current implementation

            # Clear configurations and contexts
            self._configurations.clear()
            self._execution_contexts.clear()

            self._is_initialized = False

            self.logger.info("Plugin manager cleanup completed")

        except (
            ImportError,
            AttributeError,
            TypeError,
            ValueError,
            RuntimeError,
            OSError,
        ) as e:
            # Plugin manager cleanup failed - ZERO TOLERANCE specific exception types
            self.logger.exception("Plugin manager cleanup failed", error=str(e))

    @property
    def is_initialized(self) -> bool:
        """Check if the plugin manager has been initialized.

        Returns:
            True if the manager is initialized and ready for use, False otherwise.

        """
        return self._is_initialized

    @property
    def plugin_count(self) -> int:
        """Get the total number of registered plugins.

        Returns:
            Integer count of plugins currently registered in the registry.

        """
        return self.registry.get_plugin_count()


# Factory function for creating plugin manager instances
def create_plugin_manager(
    container: DIContainer | None = None,
    auto_discover: bool = True,
    security_enabled: bool = True,
) -> PluginManager:
    """Create and configure plugin manager instance with centralized container."""
    return PluginManager(
        container=container,
        auto_discover=auto_discover,
        security_enabled=security_enabled,
    )


# Export all classes and functions
__all__ = [
    "PluginConfiguration",
    "PluginExecutionContext",
    "PluginManager",
    "PluginManagerResult",
    "create_plugin_manager",
]
