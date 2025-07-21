"""Plugin loader with security validation and dependency resolution.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

import asyncio
import importlib.util
from typing import TYPE_CHECKING, Any

# Use centralized logger from flext-infrastructure.monitoring.flext-observability
# - ELIMINATE DUPLICATION
from flext_observability.logging import get_logger

from flext_plugin.core.types import (
    PluginDependencyError,
    PluginError,
    PluginLoadError,
    PluginSecurityError,
    PluginValidationError,
)
from flext_plugin.core.validators import PluginValidator
from flext_plugin.domain.entities import (
    PluginLifecycle,
    PluginStatus,
)

if TYPE_CHECKING:
    from flext_plugin.core.base import Plugin
    from flext_plugin.core.discovery import DiscoveredPlugin
    from flext_plugin.domain.entities import PluginMetadata

logger = get_logger(__name__)


class LoadedPlugin:
    """Container for loaded plugin instance and metadata."""

    def __init__(
        self,
        plugin_id: str,
        instance: Plugin,
        metadata: PluginMetadata,
        config: dict[str, Any],
    ) -> None:
        """Initialize loaded plugin container."""
        self.plugin_id = plugin_id
        self.instance = instance
        self.metadata = metadata
        self.config = config
        self.is_initialized = False

    async def initialize(self) -> None:
        """Initialize the loaded plugin.

        Sets up the plugin instance and updates its lifecycle state.
        """
        if not self.is_initialized:
            await self.instance.initialize()
            self.instance._initialized = True  # noqa: SLF001 - Plugin lifecycle management
            self.instance._update_lifecycle_state(PluginLifecycle.INITIALIZED)  # noqa: SLF001 - Plugin lifecycle management
            self.instance._update_status(PluginStatus.HEALTHY)  # noqa: SLF001 - Plugin lifecycle management
            self.is_initialized = True

    async def cleanup(self) -> None:
        """Clean up the loaded plugin.

        Performs cleanup operations and resets the plugin state.
        """
        if self.is_initialized:
            await self.instance.cleanup()
            self.instance._initialized = False  # noqa: SLF001 - Plugin lifecycle management
            self.instance._update_lifecycle_state(PluginLifecycle.UNLOADED)  # noqa: SLF001 - Plugin lifecycle management
            self.instance._update_status(PluginStatus.UNKNOWN)  # noqa: SLF001 - Plugin lifecycle management
            self.is_initialized = False


class PluginLoader:
    """Plugin loader with security validation and dependency resolution.

    Handles the complete plugin loading lifecycle including:
    - Security validation
    - Dependency resolution
    - Configuration validation
    - Instance creation and initialization
    """

    def __init__(
        self,
        validator: PluginValidator | None = None,
        security_enabled: bool = True,
        max_load_time: float = 30.0,
    ) -> None:
        """Initialize plugin loader with configuration."""
        self.validator = validator or PluginValidator()
        self.security_enabled = security_enabled
        self.max_load_time = max_load_time
        self._loaded_plugins: dict[str, LoadedPlugin] = {}
        self._loading_plugins: set[str] = set()

    async def load_plugin(
        self,
        discovered_plugin: DiscoveredPlugin,
        config: dict[str, Any] | None = None,
        initialize: bool = True,
    ) -> LoadedPlugin:
        """Load a discovered plugin.

        Args:
            discovered_plugin: The discovered plugin to load.
            config: Optional configuration for the plugin.
            initialize: Whether to initialize the plugin after loading.

        Returns:
            The loaded plugin instance.

        Raises:
            PluginLoadError: If the plugin cannot be loaded.
            PluginSecurityError: If security validation fails.
            PluginDependencyError: If dependencies are missing.

        """
        plugin_id = discovered_plugin.metadata.name

        # Check if already loading:
        if plugin_id in self._loading_plugins:
            msg = f"Plugin {plugin_id} is already being loaded"
            raise PluginLoadError(
                msg,
                plugin_id=plugin_id,
            )

        # Check if already loaded:
        if plugin_id in self._loaded_plugins:
            logger.info("Plugin already loaded: %s", plugin_id)
            return self._loaded_plugins[plugin_id]

        self._loading_plugins.add(plugin_id)

        try:
            # Load with timeout
            loaded = await asyncio.wait_for(
                self._load_plugin_internal(discovered_plugin, config, initialize),
                timeout=self.max_load_time,
            )

            self._loaded_plugins[plugin_id] = loaded
            logger.info("Successfully loaded plugin: %s", plugin_id)
            return loaded

        except TimeoutError as e:
            msg = f"Plugin {plugin_id} loading timed out after {self.max_load_time}s"
            raise PluginLoadError(
                msg,
                plugin_id=plugin_id,
            ) from e

        finally:
            self._loading_plugins.discard(plugin_id)

    async def _load_plugin_internal(
        self,
        discovered_plugin: DiscoveredPlugin,
        config: dict[str, Any] | None,
        initialize: bool,
    ) -> LoadedPlugin:
        """Internal plugin loading implementation.

        Args:
            discovered_plugin: The discovered plugin to load.
            config: Optional configuration for the plugin.
            initialize: Whether to initialize the plugin after loading.

        Returns:
            The loaded plugin instance.

        Raises:
            PluginSecurityError: If security validation fails.
            PluginDependencyError: If dependencies are missing.
            PluginLoadError: If loading fails.

        """
        plugin_class = discovered_plugin.plugin_class
        metadata = discovered_plugin.metadata
        plugin_id = metadata.name

        # Merge default config with provided config
        final_config = {**metadata.default_configuration}
        if config:
            final_config.update(config)

        # Validate security if enabled:
        if self.security_enabled:
            # Security validation through existing validation rules
            security_valid, security_errors = self.validator.validate_plugin(
                plugin_class,
            )
            security_violations = security_errors if not security_valid else []
            if security_violations:
                msg = f"Security validation failed for plugin {plugin_id}"
                raise PluginSecurityError(
                    msg,
                    plugin_id=plugin_id,
                    security_violations=security_violations,
                )

        # Validate dependencies
        missing_deps = await self._check_dependencies(metadata)
        if missing_deps:
            msg = f"Missing dependencies for plugin {plugin_id}: {missing_deps}"
            raise PluginDependencyError(
                msg,
                plugin_id=plugin_id,
                missing_dependencies=missing_deps,
            )

        try:
            instance = plugin_class(config=final_config)
        except (TypeError, ValueError, RuntimeError, AttributeError) as e:
            msg = f"Failed to instantiate plugin {plugin_id}: {e}"
            raise PluginLoadError(
                msg,
                plugin_id=plugin_id,
                cause=e,
            ) from e

        # Update lifecycle state
        instance._update_lifecycle_state(PluginLifecycle.LOADED)  # noqa: SLF001 - Plugin lifecycle management

        # Validate configuration
        config_errors = await instance.validate_configuration(final_config)
        if config_errors:
            msg = f"Configuration validation failed for plugin {plugin_id}: {config_errors}"
            raise PluginValidationError(
                msg,
                plugin_id=plugin_id,
                validation_failures=config_errors,
            )

        # Create loaded plugin container
        loaded = LoadedPlugin(
            plugin_id=plugin_id,
            instance=instance,
            metadata=metadata,
            config=final_config,
        )

        # Initialize if requested
        if initialize:
            try:
                await loaded.initialize()
            except (RuntimeError, ValueError, AttributeError, TypeError) as e:
                msg = f"Failed to initialize plugin {plugin_id}: {e}"
                raise PluginLoadError(
                    msg,
                    plugin_id=plugin_id,
                    cause=e,
                ) from e

        return loaded

    async def _check_dependencies(self, metadata: PluginMetadata) -> list[str]:
        """Check if plugin dependencies are available.

        Args:
            metadata: The plugin metadata containing dependencies.

        Returns:
            List of missing dependencies.

        """
        missing_deps = []

        # Check Python package dependencies
        if metadata.dependencies:
            for dep in metadata.dependencies:
                # Extract package name from requirement string
                package_name = dep.split("==")[0].split(">=")[0].split("<=")[0].strip()

                spec = importlib.util.find_spec(package_name)
                if spec is None:
                    missing_deps.append(dep)

        # Note: No Meltano plugin dependencies field in current PluginMetadata
        # This functionality can be added later if needed

        return missing_deps

    async def unload_plugin(self, plugin_id: str) -> None:
        """Unload a plugin.

        Args:
            plugin_id: The ID of the plugin to unload.

        Raises:
            PluginError: If the plugin is not loaded.

        """
        if plugin_id not in self._loaded_plugins:
            msg = f"Plugin {plugin_id} is not loaded"
            raise PluginError(
                msg,
                plugin_id=plugin_id,
                error_code="NOT_LOADED",
            )

        loaded = self._loaded_plugins[plugin_id]

        # Update lifecycle state
        loaded.instance._update_lifecycle_state(PluginLifecycle.UNLOADED)  # noqa: SLF001 - Plugin lifecycle management

        # Cleanup if initialized
        try:
            await loaded.cleanup()
        except Exception as e:
            logger.exception(
                "Error during plugin cleanup: %s",
                plugin_id,
                exc_info=e,
            )

        # Remove from loaded plugins
        del self._loaded_plugins[plugin_id]
        logger.info("Unloaded plugin: %s", plugin_id)

    async def reload_plugin(
        self,
        plugin_id: str,
        discovered_plugin: DiscoveredPlugin,
        config: dict[str, Any] | None = None,
    ) -> LoadedPlugin:
        """Reload a plugin with new configuration.

        Args:
            plugin_id: The ID of the plugin to reload.
            discovered_plugin: The discovered plugin information.
            config: Optional new configuration for the plugin.

        Returns:
            The reloaded plugin instance.

        """
        # Unload if already loaded:
        if plugin_id in self._loaded_plugins:
            await self.unload_plugin(plugin_id)

        # Load with new configuration
        return await self.load_plugin(discovered_plugin, config)

    def get_loaded_plugin(self, plugin_id: str) -> LoadedPlugin | None:
        """Get a loaded plugin by ID.

        Args:
            plugin_id: The plugin ID to retrieve.

        Returns:
            The loaded plugin or None if not found.

        """
        return self._loaded_plugins.get(plugin_id)

    def get_all_loaded_plugins(self) -> dict[str, LoadedPlugin]:
        """Get all loaded plugins.

        Returns:
            Dictionary mapping plugin IDs to loaded plugin instances.

        """
        return self._loaded_plugins.copy()

    def is_loaded(self, plugin_id: str) -> bool:
        """Check if a plugin is loaded.

        Args:
            plugin_id: The plugin ID to check.

        Returns:
            True if the plugin is loaded, False otherwise.

        """
        return plugin_id in self._loaded_plugins
