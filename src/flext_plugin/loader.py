"""FLEXT Plugin Loader - Plugin loading and management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from flext_core import FlextLogger, FlextResult
from flext_plugin.types import FlextPluginTypes


class FlextPluginLoader:
    """Plugin loader service for dynamic plugin loading and management.

    This class provides comprehensive plugin loading capabilities including
    dynamic import, dependency resolution, and lifecycle management.

    Usage:
        ```python
        from flext_plugin import FlextPluginLoader

        # Initialize loader
        loader = FlextPluginLoader()

        # Load a plugin
        result = await loader.load_plugin("./my_plugin.py")
        if result.success:
            plugin_data = result.value
            print(f"Loaded plugin: {plugin_data['name']}")
        ```
    """

    def __init__(self) -> None:
        """Initialize the plugin loader."""
        self.logger = FlextLogger(__name__)
        self._loaded_plugins: Dict[str, Any] = {}
        self._plugin_metadata: Dict[str, FlextPluginTypes.Core.PluginDict] = {}

    async def load_plugin(
        self, plugin_path: str
    ) -> FlextResult[FlextPluginTypes.Core.PluginDict]:
        """Load a plugin from the specified path.

        Args:
            plugin_path: Path to the plugin to load

        Returns:
            FlextResult containing loaded plugin data
        """
        try:
            path_obj = Path(plugin_path).expanduser().resolve()
            if not path_obj.exists():
                return FlextResult.fail(f"Plugin path does not exist: {plugin_path}")

            # Determine loading strategy based on path type
            if path_obj.is_file():
                return await self._load_file_plugin(path_obj)
            elif path_obj.is_dir():
                return await self._load_directory_plugin(path_obj)
            else:
                return FlextResult.fail(f"Invalid plugin path type: {plugin_path}")

        except Exception as e:
            self.logger.exception(f"Failed to load plugin from {plugin_path}")
            return FlextResult.fail(f"Loading error: {str(e)}")

    async def unload_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Unload a plugin by name.

        Args:
            plugin_name: Name of the plugin to unload

        Returns:
            FlextResult indicating success or failure
        """
        try:
            if plugin_name not in self._loaded_plugins:
                return FlextResult.fail(f"Plugin not loaded: {plugin_name}")

            # Get plugin metadata
            metadata = self._plugin_metadata.get(plugin_name, {})
            plugin_type = metadata.get("type", "file")

            # Unload based on type
            if plugin_type == "file":
                await self._unload_file_plugin(plugin_name)
            elif plugin_type == "directory":
                await self._unload_directory_plugin(plugin_name)
            elif plugin_type == "entry_point":
                await self._unload_entry_point_plugin(plugin_name)

            # Remove from tracking
            del self._loaded_plugins[plugin_name]
            if plugin_name in self._plugin_metadata:
                del self._plugin_metadata[plugin_name]

            self.logger.info(f"Unloaded plugin: {plugin_name}")
            return FlextResult.ok(True)

        except Exception as e:
            self.logger.exception(f"Failed to unload plugin {plugin_name}")
            return FlextResult.fail(f"Unloading error: {str(e)}")

    def is_plugin_loaded(self, plugin_name: str) -> bool:
        """Check if a plugin is currently loaded.

        Args:
            plugin_name: Name of the plugin

        Returns:
            True if plugin is loaded, False otherwise
        """
        return plugin_name in self._loaded_plugins

    def get_loaded_plugins(self) -> List[str]:
        """Get list of currently loaded plugin names.

        Returns:
            List of loaded plugin names
        """
        return list(self._loaded_plugins.keys())

    def get_plugin_metadata(
        self, plugin_name: str
    ) -> Optional[FlextPluginTypes.Core.PluginDict]:
        """Get metadata for a loaded plugin.

        Args:
            plugin_name: Name of the plugin

        Returns:
            Plugin metadata if found, None otherwise
        """
        return self._plugin_metadata.get(plugin_name)

    async def reload_plugin(
        self, plugin_name: str
    ) -> FlextResult[FlextPluginTypes.Core.PluginDict]:
        """Reload a plugin by name.

        Args:
            plugin_name: Name of the plugin to reload

        Returns:
            FlextResult containing reloaded plugin data
        """
        try:
            if plugin_name not in self._loaded_plugins:
                return FlextResult.fail(f"Plugin not loaded: {plugin_name}")

            # Get original path
            metadata = self._plugin_metadata.get(plugin_name, {})
            plugin_path = metadata.get("path")
            if not plugin_path:
                return FlextResult.fail(
                    f"No path information for plugin: {plugin_name}"
                )

            # Unload and reload
            unload_result = await self.unload_plugin(plugin_name)
            if unload_result.is_failure:
                return FlextResult.fail(
                    f"Failed to unload plugin for reload: {unload_result.error}"
                )

            load_result = await self.load_plugin(plugin_path)
            if load_result.is_failure:
                return FlextResult.fail(f"Failed to reload plugin: {load_result.error}")

            self.logger.info(f"Reloaded plugin: {plugin_name}")
            return load_result

        except Exception as e:
            self.logger.exception(f"Failed to reload plugin {plugin_name}")
            return FlextResult.fail(f"Reload error: {str(e)}")

    async def _load_file_plugin(
        self, path: Path
    ) -> FlextResult[FlextPluginTypes.Core.PluginDict]:
        """Load a single file plugin.

        Args:
            path: Path to the plugin file

        Returns:
            FlextResult containing loaded plugin data
        """
        try:
            # Add parent directory to Python path
            parent_dir = str(path.parent)
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)

            # Load the module
            module_name = path.stem
            try:
                # Remove from sys.modules if already loaded to force reload
                if module_name in sys.modules:
                    del sys.modules[module_name]

                module = importlib.import_module(module_name)
                self._loaded_plugins[module_name] = module
            except Exception as e:
                return FlextResult.fail(f"Failed to import module: {str(e)}")

            # Extract plugin information
            plugin_data = {
                "name": module_name,
                "version": getattr(module, "__version__", "1.0.0"),
                "path": str(path),
                "module": module,
                "type": "file",
                "loaded_at": self._get_current_timestamp(),
            }

            # Store metadata
            self._plugin_metadata[module_name] = plugin_data

            self.logger.info(f"Loaded file plugin: {module_name}")
            return FlextResult.ok(plugin_data)

        except Exception as e:
            self.logger.exception(f"Failed to load file plugin: {path}")
            return FlextResult.fail(f"File loading error: {str(e)}")

    async def _load_directory_plugin(
        self, path: Path
    ) -> FlextResult[FlextPluginTypes.Core.PluginDict]:
        """Load a directory-based plugin.

        Args:
            path: Path to the plugin directory

        Returns:
            FlextResult containing loaded plugin data
        """
        try:
            # Look for __init__.py or main.py
            init_file = path / "__init__.py"
            main_file = path / "main.py"

            if init_file.exists():
                entry_file = init_file
            elif main_file.exists():
                entry_file = main_file
            else:
                return FlextResult.fail(f"No entry file found in directory: {path}")

            # Add directory to Python path
            directory_path = str(path)
            if directory_path not in sys.path:
                sys.path.insert(0, directory_path)

            # Load the module
            module_name = path.name
            try:
                # Remove from sys.modules if already loaded
                if module_name in sys.modules:
                    del sys.modules[module_name]

                module = importlib.import_module(module_name)
                self._loaded_plugins[module_name] = module
            except Exception as e:
                return FlextResult.fail(f"Failed to import directory module: {str(e)}")

            # Extract plugin information
            plugin_data = {
                "name": module_name,
                "version": getattr(module, "__version__", "1.0.0"),
                "path": str(path),
                "module": module,
                "type": "directory",
                "entry_file": str(entry_file),
                "loaded_at": self._get_current_timestamp(),
            }

            # Store metadata
            self._plugin_metadata[module_name] = plugin_data

            self.logger.info(f"Loaded directory plugin: {module_name}")
            return FlextResult.ok(plugin_data)

        except Exception as e:
            self.logger.exception(f"Failed to load directory plugin: {path}")
            return FlextResult.fail(f"Directory loading error: {str(e)}")

    async def _unload_file_plugin(self, plugin_name: str) -> None:
        """Unload a file-based plugin.

        Args:
            plugin_name: Name of the plugin to unload
        """
        try:
            # Remove from sys.modules
            if plugin_name in sys.modules:
                del sys.modules[plugin_name]

            # Remove from loaded plugins
            if plugin_name in self._loaded_plugins:
                del self._loaded_plugins[plugin_name]

        except Exception:
            self.logger.exception(f"Failed to unload file plugin: {plugin_name}")

    async def _unload_directory_plugin(self, plugin_name: str) -> None:
        """Unload a directory-based plugin.

        Args:
            plugin_name: Name of the plugin to unload
        """
        try:
            # Remove from sys.modules
            if plugin_name in sys.modules:
                del sys.modules[plugin_name]

            # Remove from loaded plugins
            if plugin_name in self._loaded_plugins:
                del self._loaded_plugins[plugin_name]

        except Exception:
            self.logger.exception(f"Failed to unload directory plugin: {plugin_name}")

    async def _unload_entry_point_plugin(self, plugin_name: str) -> None:
        """Unload an entry point-based plugin.

        Args:
            plugin_name: Name of the plugin to unload
        """
        try:
            # Entry point plugins are typically not unloadable
            # Just remove from tracking
            if plugin_name in self._loaded_plugins:
                del self._loaded_plugins[plugin_name]

        except Exception:
            self.logger.exception(f"Failed to unload entry point plugin: {plugin_name}")

    def _get_current_timestamp(self) -> str:
        """Get current timestamp as ISO string.

        Returns:
            Current timestamp as ISO string
        """
        from datetime import datetime, UTC

        return datetime.now(UTC).isoformat()

    def get_loader_status(self) -> Dict[str, Any]:
        """Get the current status of the plugin loader.

        Returns:
            Dictionary containing loader status information
        """
        return {
            "total_loaded_plugins": len(self._loaded_plugins),
            "loaded_plugin_names": list(self._loaded_plugins.keys()),
            "plugin_types": {
                name: metadata.get("type", "unknown")
                for name, metadata in self._plugin_metadata.items()
            },
        }

    async def validate_plugin_dependencies(self, plugin_name: str) -> FlextResult[bool]:
        """Validate dependencies for a loaded plugin.

        Args:
            plugin_name: Name of the plugin to validate

        Returns:
            FlextResult indicating validation success or failure
        """
        try:
            if plugin_name not in self._loaded_plugins:
                return FlextResult.fail(f"Plugin not loaded: {plugin_name}")

            module = self._loaded_plugins[plugin_name]

            # Check for required attributes
            required_attrs = ["__version__", "__name__"]
            for attr in required_attrs:
                if not hasattr(module, attr):
                    return FlextResult.fail(f"Missing required attribute: {attr}")

            # Check for plugin-specific attributes
            plugin_attrs = ["execute", "initialize", "cleanup"]
            available_attrs = [attr for attr in plugin_attrs if hasattr(module, attr)]

            if not available_attrs:
                self.logger.warning(
                    f"Plugin {plugin_name} has no standard plugin methods"
                )

            self.logger.info(f"Plugin dependencies validated: {plugin_name}")
            return FlextResult.ok(True)

        except Exception as e:
            self.logger.exception(f"Failed to validate dependencies for {plugin_name}")
            return FlextResult.fail(f"Dependency validation error: {str(e)}")

    async def get_plugin_info(self, plugin_name: str) -> FlextResult[Dict[str, Any]]:
        """Get detailed information about a loaded plugin.

        Args:
            plugin_name: Name of the plugin

        Returns:
            FlextResult containing plugin information
        """
        try:
            if plugin_name not in self._loaded_plugins:
                return FlextResult.fail(f"Plugin not loaded: {plugin_name}")

            module = self._loaded_plugins[plugin_name]
            metadata = self._plugin_metadata.get(plugin_name, {})

            # Extract module information
            module_info = {
                "name": getattr(module, "__name__", plugin_name),
                "version": getattr(module, "__version__", "1.0.0"),
                "doc": getattr(module, "__doc__", ""),
                "file": getattr(module, "__file__", ""),
                "package": getattr(module, "__package__", ""),
            }

            # Get available methods and attributes
            methods = [name for name in dir(module) if not name.startswith("_")]
            callable_methods = [
                name for name in methods if callable(getattr(module, name))
            ]

            plugin_info = {
                **metadata,
                **module_info,
                "available_methods": callable_methods,
                "all_attributes": methods,
            }

            return FlextResult.ok(plugin_info)

        except Exception as e:
            self.logger.exception(f"Failed to get plugin info for {plugin_name}")
            return FlextResult.fail(f"Plugin info error: {str(e)}")


__all__ = ["FlextPluginLoader"]
