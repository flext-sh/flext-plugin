"""FLEXT Plugin Domain Ports - Clean Architecture interfaces for external dependencies.

This module defines the domain ports (interfaces) that establish contracts
between the domain layer and external infrastructure concerns. Following
Clean Architecture principles, these ports ensure proper dependency inversion
and enable testability through interface segregation.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from abc import abstractmethod

from flext_core import FlextProtocols, FlextResult

from flext_plugin.entities import FlextPluginEntities
from flext_plugin.typings import FlextPluginTypes


class FlextPluginPorts:
    class Discovery(FlextProtocols.Domain.Service):
        """Domain port interface for plugin discovery and validation operations."""

        @abstractmethod
        def discover_plugins(
            self, path: str
        ) -> FlextResult[list[FlextPluginEntities.Entity]]:
            """Discover plugins in the given path.

            Args:
                path: Path to search for plugins
            Returns:
                FlextResult containing list of discovered plugins

            """

        @abstractmethod
        def validate_plugin(
            self, plugin: FlextPluginEntities.Entity
        ) -> FlextResult[bool]:
            """Validate a plugin.

            Args:
                plugin: Plugin to validate
            Returns:
                FlextResult indicating if plugin is valid

            """

    class Loader(FlextProtocols.Domain.Service):
        """Domain port interface for plugin loading and memory management operations."""

        @abstractmethod
        def load_plugin(self, plugin: FlextPluginEntities.Entity) -> FlextResult[bool]:
            """Load a plugin.

            Args:
                plugin: Plugin to load
            Returns:
                FlextResult indicating if loading was successful

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def unload_plugin(self, plugin_name: str) -> FlextResult[bool]:
            """Unload a plugin.

            Args:
                plugin_name: Name of plugin to unload
            Returns:
                FlextResult indicating if unloading was successful

            """

        @abstractmethod
        def is_plugin_loaded(self, plugin_name: str) -> FlextResult[bool]:
            """Check if a plugin is loaded.

            Args:
                plugin_name: Name of plugin to check
            Returns:
                FlextResult indicating if plugin is loaded

            """

    class Manager(FlextProtocols.Domain.Service):
        """Domain port interface for comprehensive plugin management and configuration."""

        @abstractmethod
        def install_plugin(
            self, plugin_path: str
        ) -> FlextResult[FlextPluginEntities.Entity]:
            """Install a plugin from the given path.

            Args:
                plugin_path: Path to plugin to install
            Returns:
                FlextResult containing installed plugin

            """

        @abstractmethod
        def uninstall_plugin(self, plugin_name: str) -> FlextResult[bool]:
            """Uninstall a plugin.

            Args:
                plugin_name: Name of plugin to uninstall
            Returns:
                FlextResult indicating if uninstallation was successful

            """

        @abstractmethod
        def enable_plugin(self, plugin_name: str) -> FlextResult[bool]:
            """Enable a plugin.

            Args:
                plugin_name: Name of plugin to enable
            Returns:
                FlextResult indicating if enabling was successful

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def disable_plugin(self, plugin_name: str) -> FlextResult[bool]:
            """Disable a plugin.

            Args:
                plugin_name: Name of plugin to disable
            Returns:
                FlextResult indicating if disabling was successful

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def get_plugin_config(
            self, plugin_name: str
        ) -> FlextResult[FlextPluginEntities.Config]:
            """Get configuration for a plugin.

            Args:
                plugin_name: Name of plugin to get config for
            Returns:
                FlextResult containing plugin configuration

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def update_plugin_config(
            self,
            plugin_name: str,
            config: FlextPluginEntities.Config,
        ) -> FlextResult[bool]:
            """Update configuration for a plugin.

            Args:
                plugin_name: Name of plugin to update config for
                config: New plugin configuration
            Returns:
                FlextResult indicating if update was successful

            """
            ...
            # Abstract method - implemented by adapters

    class Registry(FlextProtocols.Domain.Service):
        """Domain port interface for plugin registry operations."""

        @abstractmethod
        def register_registry(self, registry: str) -> FlextResult[bool]:
            """Register a plugin registry.

            Args:
                registry: Registry URL or identifier to register

            Returns:
                FlextResult indicating if registration was successful

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def sync_registry(self, registry_name: str) -> FlextResult[bool]:
            """Synchronize with a plugin registry.

            Args:
                registry_name: Name of registry to sync

            Returns:
                FlextResult indicating if sync was successful

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def search_plugins(
            self,
            registry: str,
            query: str,
        ) -> FlextResult[list[FlextPluginTypes.Core.PluginDict]]:
            """Search for plugins in a specific registry.

            Args:
                registry: Registry to search in
                query: Search query string

            Returns:
                FlextResult containing list of plugin search results

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def download_plugin(self, plugin_id: str, registry: str) -> FlextResult[str]:
            """Download a plugin from a registry.

            Args:
                plugin_id: Plugin identifier to download
                registry: Registry to download from

            Returns:
                FlextResult containing path to downloaded plugin

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def verify_plugin_signature(self, plugin_path: str) -> FlextResult[bool]:
            """Verify a plugin's digital signature.

            Args:
                plugin_path: Path to plugin to verify

            Returns:
                FlextResult indicating if signature is valid

            """
            ...
            # Abstract method - implemented by adapters

    class HotReload(FlextProtocols.Domain.Service):
        """Domain port interface for plugin hot reload operations."""

        @abstractmethod
        def start_watching(
            self,
            watch_paths: FlextPluginTypes.Core.StringList,
        ) -> FlextResult[bool]:
            """Start watching for plugin file changes.

            Args:
                watch_paths: List of paths to watch for changes

            Returns:
                FlextResult indicating if watching was started successfully

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def stop_watching(self: object) -> FlextResult[bool]:
            """Stop watching for plugin file changes.

            Returns:
                FlextResult indicating if watching was stopped successfully

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def reload_plugin(
            self, plugin: FlextPluginEntities.Entity
        ) -> FlextResult[bool]:
            """Reload a specific plugin.

            Args:
                plugin: Plugin entity to reload

            Returns:
                FlextResult indicating if reload was successful

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def backup_plugin_state(
            self,
            plugin_name: str,
        ) -> FlextResult[FlextPluginTypes.Core.PluginDict]:
            """Backup plugin state before reload.

            Args:
                plugin_name: Name of plugin to backup

            Returns:
                FlextResult containing backed up state data

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def restore_plugin_state(
            self,
            plugin_name: str,
            state: FlextPluginTypes.Core.PluginDict,
        ) -> FlextResult[bool]:
            """Restore plugin state after reload.

            Args:
                plugin_name: Name of plugin to restore
                state: State data to restore

            Returns:
                FlextResult indicating if restoration was successful

            """
            ...
            # Abstract method - implemented by adapters


__all__ = [
    "FlextPluginPorts",
]
