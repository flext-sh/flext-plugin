"""Plugin manager for orchestrating plugin lifecycle and operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

import asyncio
import contextlib
from typing import TYPE_CHECKING, Any
from uuid import uuid4

# Use centralized logger from flext-observability - ELIMINATE DUPLICATION
from flext_observability.logging import get_logger
from flext_plugin.core.discovery import PluginDiscovery
from flext_plugin.core.loader import PluginLoader
from flext_plugin.core.types import (
    PluginError,
    PluginExecutionError,
    PluginExecutionResult,
    PluginStatus,
)
from flext_plugin.core.validators import PluginValidator

if TYPE_CHECKING:
    from pathlib import Path

    from flext_plugin.core.discovery import DiscoveredPlugin
    from flext_plugin.core.loader import LoadedPlugin
    from flext_plugin.core.types import (
        PluginType,
    )
    from flext_plugin.types import PluginContext, PluginData, PluginResult

logger = get_logger(__name__)


class PluginManager:
    """Central plugin management system.

    Orchestrates the complete plugin lifecycle including:
        - Discovery and registration
        - Loading and initialization
        - Execution and monitoring
        - Unloading and cleanup
    """

    def __init__(
        self,
        plugin_directories: list[Path] | None = None,
        entry_point_groups: list[str] | None = None,
        security_enabled: bool = True,
        auto_discover: bool = True,
    ) -> None:
        """Initialize plugin manager.

        Args:
            plugin_directories: List of directories to search for plugins.
            entry_point_groups: List of entry point groups to discover.
            security_enabled: Whether to enable security validations.
            auto_discover: Whether to automatically discover plugins on init.

        """
        self.discovery = PluginDiscovery(plugin_directories, entry_point_groups)
        self.loader = PluginLoader(
            validator=PluginValidator(),
            security_enabled=security_enabled,
        )
        self.auto_discover = auto_discover
        self._discovered_plugins: dict[str, DiscoveredPlugin] = {}
        self._execution_tasks: dict[str, asyncio.Task[Any]] = {}

    async def initialize(self) -> None:
        """Initialize the plugin manager.

        Performs plugin discovery if auto_discover is enabled.
        """
        if self.auto_discover:
            await self.discover_plugins()

    async def discover_plugins(self) -> dict[str, DiscoveredPlugin]:
        """Discover all available plugins.

        Returns:
            Dictionary mapping plugin IDs to discovered plugin info.

        """
        self._discovered_plugins = await self.discovery.discover_all()
        logger.info("Discovered %d plugins", len(self._discovered_plugins))
        return self._discovered_plugins

    async def load_plugin(
        self,
        plugin_id: str,
        config: dict[str, Any] | None = None,
        initialize: bool = True,
    ) -> LoadedPlugin:
        """Load a plugin by ID.

        Args:
            plugin_id: The plugin ID to load.
            config: Optional configuration for the plugin.
            initialize: Whether to initialize the plugin after loading.

        Returns:
            The loaded plugin instance.

        Raises:
            PluginError: If plugin is not found or cannot be loaded.

        """
        if plugin_id not in self._discovered_plugins:
            # Try to discover plugins if not already done
            if not self._discovered_plugins:
                await self.discover_plugins()

            if plugin_id not in self._discovered_plugins:
                msg = f"Plugin not found: {plugin_id}"
                raise PluginError(
                    msg,
                    plugin_id=plugin_id,
                )

        discovered = self._discovered_plugins[plugin_id]
        return await self.loader.load_plugin(discovered, config, initialize)

    async def unload_plugin(self, plugin_id: str) -> None:
        """Unload a plugin by ID.

        Args:
            plugin_id: The plugin ID to unload.

        """
        # Cancel any running executions
        if plugin_id in self._execution_tasks:
            task = self._execution_tasks[plugin_id]
            if not task.done():
                task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await task
            del self._execution_tasks[plugin_id]

        # Unload the plugin
        await self.loader.unload_plugin(plugin_id)

    async def reload_plugin(
        self,
        plugin_id: str,
        config: dict[str, Any] | None = None,
    ) -> LoadedPlugin:
        """Reload a plugin by ID.

        Args:
            plugin_id: The plugin ID to reload.
            config: Optional new configuration for the plugin.

        Returns:
            The reloaded plugin instance.

        Raises:
            PluginError: If plugin is not found or cannot be reloaded.

        """
        if plugin_id not in self._discovered_plugins:
            msg = f"Plugin not found: {plugin_id}"
            raise PluginError(
                msg,
                plugin_id=plugin_id,
            )

        discovered = self._discovered_plugins[plugin_id]
        return await self.loader.reload_plugin(plugin_id, discovered, config)

    async def execute_plugin(
        self,
        plugin_id: str,
        input_data: PluginData = None,
        context: PluginContext | None = None,
    ) -> PluginExecutionResult:
        """Execute a plugin with input data.

        Args:
            plugin_id: The plugin ID to execute.
            input_data: Input data to pass to the plugin.
            context: Additional execution context.

        Returns:
            The execution result.

        Raises:
            PluginExecutionError: If plugin execution fails.

        """
        # Get loaded plugin
        loaded = self.loader.get_loaded_plugin(plugin_id)
        if not loaded:
            # Try to load the plugin
            loaded = await self.load_plugin(plugin_id)

        # Create execution ID

        execution_id = str(uuid4())

        # Create execution context
        exec_context = {
            "execution_id": execution_id,
            "plugin_id": plugin_id,
            **(context or {}),
        }

        # Create execution result
        result = PluginExecutionResult(
            success=False,
            plugin_id=plugin_id,
            execution_id=execution_id,
            execution_context=exec_context,
        )

        try:
            # Execute plugin
            plugin_result = await loaded.instance.execute(input_data, exec_context)

            # Update result
            result.success = True
            result.result = plugin_result

        except (PluginError, RuntimeError, ValueError, AttributeError, TypeError) as e:
            # Update result with error
            result.success = False
            result.error = str(e)

            msg = f"Plugin execution failed {plugin_id}"
            raise PluginExecutionError(
                msg,
                plugin_id=plugin_id,
                execution_id=execution_id,
                cause=e,
            )

        finally:
            # Mark execution completed
            result.mark_completed(
                result.result if result.success else None,
                result.error if not result.success else None,
            )

        return result

    async def execute_plugin_async(
        self,
        plugin_id: str,
        input_data: PluginData = None,
        context: PluginContext | None = None,
    ) -> asyncio.Task[PluginResult]:
        """Execute a plugin asynchronously.

        Args:
            plugin_id: The plugin ID to execute.
            input_data: Input data to pass to the plugin.
            context: Additional execution context.

        Returns:
            The async task for the execution.

        """
        # Cancel any existing execution
        if plugin_id in self._execution_tasks:
            existing_task = self._execution_tasks[plugin_id]
            if not existing_task.done():
                existing_task.cancel()

        # Create new execution task
        task = asyncio.create_task(self.execute_plugin(plugin_id, input_data, context))
        self._execution_tasks[plugin_id] = task

        return task

    async def get_plugin_status(self, plugin_id: str) -> PluginStatus:
        """Get the status of a plugin.

        Args:
            plugin_id: The plugin ID to check.

        Returns:
            The plugin status.

        """
        loaded = self.loader.get_loaded_plugin(plugin_id)
        if not loaded:
            return PluginStatus.UNKNOWN

        return loaded.instance.plugin_status

    async def get_plugin_health(self, plugin_id: str) -> dict[str, Any]:
        """Get the health status of a plugin.

        Args:
            plugin_id: The plugin ID to check.

        Returns:
            Dictionary containing health information.

        """
        loaded = self.loader.get_loaded_plugin(plugin_id)
        if not loaded:
            return {
                "status": "unknown",
                "error": "Plugin not loaded",
            }

        try:
            return await loaded.instance.health_check()
        except (RuntimeError, ValueError, AttributeError, TypeError, OSError) as e:
            return {
                "status": "unhealthy",
                "error": str(e),
            }

    async def list_plugins(
        self,
        plugin_type: PluginType | None = None,
        status: PluginStatus | None = None,
    ) -> list[dict[str, Any]]:
        """List available plugins with optional filtering.

        Args:
            plugin_type: Optional plugin type filter.
            status: Optional plugin status filter.

        Returns:
            List of plugin information dictionaries.

        """
        plugins = []

        for plugin_id, discovered in self._discovered_plugins.items():
            # Apply type filter
            if plugin_type and str(discovered.metadata.plugin_type) != str(plugin_type):
                continue

            # Get loaded status
            loaded = self.loader.get_loaded_plugin(plugin_id)
            current_status = (
                loaded.instance.plugin_status if loaded else PluginStatus.UNKNOWN
            )

            # Apply status filter
            if status and current_status != status:
                continue

            # Build plugin info
            plugin_info = {
                "id": plugin_id,
                "name": discovered.metadata.name,
                "version": discovered.metadata.version,
                "type": discovered.metadata.plugin_type.value,
                "status": current_status.value,
                "loaded": loaded is not None,
                "initialized": loaded.is_initialized if loaded else False,
                "source": discovered.source,
                "capabilities": discovered.metadata.capabilities,
            }

            plugins.append(plugin_info)

        return plugins

    def get_discovered_plugin(self, plugin_id: str) -> DiscoveredPlugin | None:
        """Get a discovered plugin by ID.

        Args:
            plugin_id: The plugin ID to retrieve.

        Returns:
            The discovered plugin info or None if not found.

        """
        return self._discovered_plugins.get(plugin_id)

    def get_loaded_plugin(self, plugin_id: str) -> LoadedPlugin | None:
        """Get a loaded plugin by ID.

        Args:
            plugin_id: The plugin ID to retrieve.

        Returns:
            The loaded plugin or None if not loaded.

        """
        return self.loader.get_loaded_plugin(plugin_id)

    def is_plugin_loaded(self, plugin_id: str) -> bool:
        """Check if a plugin is loaded.

        Args:
            plugin_id: The plugin ID to check.

        Returns:
            True if the plugin is loaded, False otherwise.

        """
        return self.loader.is_loaded(plugin_id)

    async def shutdown(self) -> None:
        """Shutdown the plugin manager.

        Cancels all running executions and unloads all plugins.
        """
        # Cancel all running executions
        for task in self._execution_tasks.values():
            if not task.done():
                task.cancel()

        # Wait for all tasks to complete
        if self._execution_tasks:
            await asyncio.gather(
                *self._execution_tasks.values(),
                return_exceptions=True,
            )

        # Unload all plugins
        loaded_plugins = list(self.loader.get_all_loaded_plugins().keys())
        for plugin_id in loaded_plugins:
            try:
                await self.unload_plugin(plugin_id)
            except Exception as e:
                logger.exception("Error unloading plugin %s: %s", plugin_id, e)

        logger.info("Plugin manager shutdown complete")
