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

from flext_core import FlextCore

from flext_plugin.entities import FlextPluginEntities
from flext_plugin.typings import FlextPluginTypes


class FlextPluginPorts:
    """Domain port interfaces for plugin operations."""

    class Discovery(FlextCore.Protocols.Domain.Service):
        """Domain port interface for plugin discovery and validation operations."""

        @abstractmethod
        def discover_plugins(
            self, path: str
        ) -> FlextCore.Result[list[FlextPluginEntities.Entity]]:
            """Discover plugins in the given path.

            Args:
                path: Path to search for plugins
            Returns:
                FlextCore.Result containing list of discovered plugins

            """

        @abstractmethod
        def validate_plugin(
            self, plugin: FlextPluginEntities.Entity
        ) -> FlextCore.Result[bool]:
            """Validate a plugin.

            Args:
                plugin: Plugin to validate
            Returns:
                FlextCore.Result indicating if plugin is valid

            """

    class Loader(FlextCore.Protocols.Domain.Service):
        """Domain port interface for plugin loading and memory management operations."""

        @abstractmethod
        def load_plugin(
            self, plugin: FlextPluginEntities.Entity
        ) -> FlextCore.Result[bool]:
            """Load a plugin.

            Args:
                plugin: Plugin to load
            Returns:
                FlextCore.Result indicating if loading was successful

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def unload_plugin(self, plugin_name: str) -> FlextCore.Result[bool]:
            """Unload a plugin.

            Args:
                plugin_name: Name of plugin to unload
            Returns:
                FlextCore.Result indicating if unloading was successful

            """

        @abstractmethod
        def is_plugin_loaded(self, plugin_name: str) -> FlextCore.Result[bool]:
            """Check if a plugin is loaded.

            Args:
                plugin_name: Name of plugin to check
            Returns:
                FlextCore.Result indicating if plugin is loaded

            """

    class Manager(FlextCore.Protocols.Domain.Service):
        """Domain port interface for comprehensive plugin management and configuration."""

        @abstractmethod
        def install_plugin(
            self, plugin_path: str
        ) -> FlextCore.Result[FlextPluginEntities.Entity]:
            """Install a plugin from the given path.

            Args:
                plugin_path: Path to plugin to install
            Returns:
                FlextCore.Result containing installed plugin

            """

        @abstractmethod
        def uninstall_plugin(self, plugin_name: str) -> FlextCore.Result[bool]:
            """Uninstall a plugin.

            Args:
                plugin_name: Name of plugin to uninstall
            Returns:
                FlextCore.Result indicating if uninstallation was successful

            """

        @abstractmethod
        def enable_plugin(self, plugin_name: str) -> FlextCore.Result[bool]:
            """Enable a plugin.

            Args:
                plugin_name: Name of plugin to enable
            Returns:
                FlextCore.Result indicating if enabling was successful

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def disable_plugin(self, plugin_name: str) -> FlextCore.Result[bool]:
            """Disable a plugin.

            Args:
                plugin_name: Name of plugin to disable
            Returns:
                FlextCore.Result indicating if disabling was successful

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def get_plugin_config(
            self, plugin_name: str
        ) -> FlextCore.Result[FlextPluginEntities.Config]:
            """Get configuration for a plugin.

            Args:
                plugin_name: Name of plugin to get config for
            Returns:
                FlextCore.Result containing plugin configuration

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def update_plugin_config(
            self,
            plugin_name: str,
            config: FlextPluginEntities.Config,
        ) -> FlextCore.Result[bool]:
            """Update configuration for a plugin.

            Args:
                plugin_name: Name of plugin to update config for
                config: New plugin configuration
            Returns:
                FlextCore.Result indicating if update was successful

            """
            ...
            # Abstract method - implemented by adapters

    class Registry(FlextCore.Protocols.Domain.Service):
        """Domain port interface for plugin registry operations."""

        @abstractmethod
        def register_registry(self, registry: str) -> FlextCore.Result[bool]:
            """Register a plugin registry.

            Args:
                registry: Registry URL or identifier to register

            Returns:
                FlextCore.Result indicating if registration was successful

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def sync_registry(self, registry_name: str) -> FlextCore.Result[bool]:
            """Synchronize with a plugin registry.

            Args:
                registry_name: Name of registry to sync

            Returns:
                FlextCore.Result indicating if sync was successful

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def search_plugins(
            self,
            registry: str,
            query: str,
        ) -> FlextCore.Result[list[FlextPluginTypes.Core.PluginDict]]:
            """Search for plugins in a specific registry.

            Args:
                registry: Registry to search in
                query: Search query string

            Returns:
                FlextCore.Result containing list of plugin search results

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def download_plugin(
            self, plugin_id: str, registry: str
        ) -> FlextCore.Result[str]:
            """Download a plugin from a registry.

            Args:
                plugin_id: Plugin identifier to download
                registry: Registry to download from

            Returns:
                FlextCore.Result containing path to downloaded plugin

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def verify_plugin_signature(self, plugin_path: str) -> FlextCore.Result[bool]:
            """Verify a plugin's digital signature.

            Args:
                plugin_path: Path to plugin to verify

            Returns:
                FlextCore.Result indicating if signature is valid

            """
            ...
            # Abstract method - implemented by adapters

    class HotReload(FlextCore.Protocols.Domain.Service):
        """Domain port interface for plugin hot reload operations."""

        @abstractmethod
        def start_watching(
            self,
            watch_paths: FlextPluginTypes.Core.StringList,
        ) -> FlextCore.Result[bool]:
            """Start watching for plugin file changes.

            Args:
                watch_paths: List of paths to watch for changes

            Returns:
                FlextCore.Result indicating if watching was started successfully

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def stop_watching(self: object) -> FlextCore.Result[bool]:
            """Stop watching for plugin file changes.

            Returns:
                FlextCore.Result indicating if watching was stopped successfully

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def reload_plugin(
            self, plugin: FlextPluginEntities.Entity
        ) -> FlextCore.Result[bool]:
            """Reload a specific plugin.

            Args:
                plugin: Plugin entity to reload

            Returns:
                FlextCore.Result indicating if reload was successful

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def backup_plugin_state(
            self,
            plugin_name: str,
        ) -> FlextCore.Result[FlextPluginTypes.Core.PluginDict]:
            """Backup plugin state before reload.

            Args:
                plugin_name: Name of plugin to backup

            Returns:
                FlextCore.Result containing backed up state data

            """
            ...
            # Abstract method - implemented by adapters

        @abstractmethod
        def restore_plugin_state(
            self,
            plugin_name: str,
            state: FlextPluginTypes.Core.PluginDict,
        ) -> FlextCore.Result[bool]:
            """Restore plugin state after reload.

            Args:
                plugin_name: Name of plugin to restore
                state: State data to restore

            Returns:
                FlextCore.Result indicating if restoration was successful

            """
            ...
            # Abstract method - implemented by adapters


__all__ = [
    "FlextPluginPorts",
]
