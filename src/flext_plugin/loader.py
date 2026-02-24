"""FLEXT Plugin Loader - Plugin loading and management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import importlib.util
from collections.abc import Callable, Mapping
from datetime import UTC, datetime
from pathlib import Path

from flext_core import FlextLogger, FlextResult

from flext_plugin.models import FlextPluginModels
from flext_plugin.typings import t


class FlextPluginLoader:
    """Plugin loader service for dynamic plugin loading and management.

    Provides complete plugin loading with safe spec-based module loading,
    automatic entry file discovery, and lifecycle management. Uses strategy
    pattern for file and directory-based plugins with composition.

    Usage:
        ```python
        from flext_plugin import FlextPluginLoader

        # Initialize loader
        loader = FlextPluginLoader()

        # Load a plugin
        result = loader.load_plugin("./my_plugin.py")
        if result.is_success:
            load_data = result.value
            print(f"Loaded plugin: {load_data.name}")
        ```
    """

    def __init__(self) -> None:
        """Initialize the plugin loader."""
        self.logger = FlextLogger(__name__)
        self._loaded_plugins: dict[str, object] = {}
        self._loader_strategies: list[
            Callable[[Path], FlextPluginModels.Plugin.LoadData | None]
        ] = [
            self.FilePluginLoader(self.logger).load,
            self.DirectoryPluginLoader(self.logger).load,
        ]

    def load_plugin(
        self, plugin_path: str
    ) -> FlextResult[FlextPluginModels.Plugin.LoadData]:
        """Load a plugin from the specified path.

        Args:
            plugin_path: Path to the plugin to load

        Returns:
            FlextResult containing loaded plugin data

        """
        try:
            path_obj = Path(plugin_path).expanduser().resolve()

            if not path_obj.exists():
                error_msg = f"Plugin path does not exist: {plugin_path}"
                return FlextResult.fail(error_msg)

            # Try each loader strategy
            for loader_strategy in self._loader_strategies:
                load_data = loader_strategy(path_obj)
                if load_data:
                    self._loaded_plugins[load_data.name] = load_data.module
                    return FlextResult.ok(load_data)

            error_msg = f"Invalid plugin path type: {plugin_path}"
            return FlextResult.fail(error_msg)

        except Exception as e:
            self.logger.exception(f"Failed to load plugin from {plugin_path}")
            return FlextResult.fail(f"Loading error: {e!s}")

    def unload_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Unload a plugin by name.

        Args:
        plugin_name: Name of the plugin to unload

        Returns:
        FlextResult indicating success or failure

        """
        try:
            if plugin_name not in self._loaded_plugins:
                error_msg = f"Plugin not loaded: {plugin_name}"
                return FlextResult.fail(error_msg)

            # Remove from tracking
            del self._loaded_plugins[plugin_name]

            self.logger.info("Unloaded plugin: %s", plugin_name)
            return FlextResult.ok(True)

        except Exception as e:
            self.logger.exception(f"Failed to unload plugin {plugin_name}")
            return FlextResult.fail(f"Unloading error: {e!s}")

    def is_plugin_loaded(self, plugin_name: str) -> bool:
        """Check if a plugin is currently loaded.

        Args:
        plugin_name: Name of the plugin

        Returns:
        True if plugin is loaded, False otherwise

        """
        return plugin_name in self._loaded_plugins

    def get_loaded_plugins(self) -> list[str]:
        """Get list of currently loaded plugin names.

        Returns:
        List of loaded plugin names

        """
        return list(self._loaded_plugins.keys())

    def reload_plugin(
        self,
        plugin_name: str,
    ) -> FlextResult[FlextPluginModels.Plugin.LoadData]:
        """Reload a plugin by name.

        Args:
        plugin_name: Name of the plugin to reload

        Returns:
        FlextResult containing reloaded plugin data

        """
        try:
            if plugin_name not in self._loaded_plugins:
                error_msg = f"Plugin not loaded: {plugin_name}"
                return FlextResult.fail(error_msg)

            # Get original plugin module for path extraction
            module = self._loaded_plugins.get(plugin_name)
            module_file = getattr(module, "__file__", None)
            if not module or module_file is None:
                error_msg = f"No path information for plugin: {plugin_name}"
                return FlextResult.fail(error_msg)

            plugin_path = module_file
            if not plugin_path:
                error_msg = f"Cannot determine plugin path for: {plugin_name}"
                return FlextResult.fail(error_msg)

            # Unload and reload
            unload_result = self.unload_plugin(plugin_name)
            if unload_result.is_failure:
                error_msg = f"Failed to unload plugin for reload: {unload_result.error}"
                return FlextResult.fail(error_msg)

            load_result = self.load_plugin(str(plugin_path))
            if load_result.is_failure:
                return FlextResult.fail(f"Failed to reload plugin: {load_result.error}")

            self.logger.info("Reloaded plugin: %s", plugin_name)
            return load_result

        except Exception as e:
            self.logger.exception(f"Failed to reload plugin {plugin_name}")
            return FlextResult.fail(f"Reload error: {e!s}")

    def validate_plugin_dependencies(self, plugin_name: str) -> FlextResult[bool]:
        """Validate dependencies for a loaded plugin.

        Args:
        plugin_name: Name of the plugin to validate

        Returns:
        FlextResult indicating validation success or failure

        """
        try:
            if plugin_name not in self._loaded_plugins:
                error_msg = f"Plugin not loaded: {plugin_name}"
                return FlextResult.fail(error_msg)

            module = self._loaded_plugins[plugin_name]

            # Check for required attributes
            required_attrs = ["__version__", "__name__"]
            for attr in required_attrs:
                if getattr(module, attr, None) is None:
                    return FlextResult.fail(f"Missing required attribute: {attr}")

            # Check for plugin-specific attributes
            plugin_attrs = ["execute", "initialize", "cleanup"]
            available_attrs = [
                attr for attr in plugin_attrs if getattr(module, attr, None) is not None
            ]

            if not available_attrs:
                self.logger.warning(
                    "Plugin %s has no standard plugin methods",
                    plugin_name,
                )

            self.logger.info("Plugin dependencies validated: %s", plugin_name)
            return FlextResult.ok(True)

        except Exception as e:
            self.logger.exception(f"Failed to validate dependencies for {plugin_name}")
            return FlextResult.fail(f"Dependency validation error: {e!s}")

    def get_plugin_info(
        self, plugin_name: str
    ) -> FlextResult[Mapping[str, t.GeneralValueType]]:
        """Get detailed information about a loaded plugin.

        Args:
        plugin_name: Name of the plugin

        Returns:
        FlextResult containing plugin information

        """
        try:
            if plugin_name not in self._loaded_plugins:
                error_msg = f"Plugin not loaded: {plugin_name}"
                return FlextResult.fail(error_msg)

            module = self._loaded_plugins[plugin_name]

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
                **module_info,
                "available_methods": callable_methods,
                "all_attributes": methods,
            }

            return FlextResult.ok(plugin_info)

        except Exception as e:
            self.logger.exception(f"Failed to get plugin info for {plugin_name}")
            return FlextResult.fail(f"Plugin info error: {e!s}")

    class FilePluginLoader:
        """File-based plugin loader using safe spec-based module loading."""

        def __init__(self, logger: FlextLogger) -> None:
            """Initialize file loader with logger."""
            self.logger = logger

        def load(self, path: Path) -> FlextPluginModels.Plugin.LoadData | None:
            """Load a single file plugin safely.

            Uses importlib.util.spec_from_file_location for safe loading
            without sys.path pollution.

            Args:
            path: Path to the plugin file

            Returns:
            LoadData if successfully loaded, None otherwise

            """
            if not path.is_file() or path.suffix != ".py":
                return None

            try:
                spec = importlib.util.spec_from_file_location(path.stem, path)
                if not spec or not spec.loader:
                    return None

                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                return FlextPluginModels.Plugin.LoadData(
                    name=path.stem,
                    version=getattr(module, "__version__", "1.0.0"),
                    path=path,
                    module=module,
                    load_type="file",
                    loaded_at=datetime.now(UTC),
                )
            except Exception:
                self.logger.exception(f"Failed to load file plugin: {path}")
                return None

    class DirectoryPluginLoader:
        """Directory-based plugin loader with entry file discovery."""

        def __init__(self, logger: FlextLogger) -> None:
            """Initialize directory loader with logger."""
            self.logger = logger

        def load(self, path: Path) -> FlextPluginModels.Plugin.LoadData | None:
            """Load a directory-based plugin.

            Searches for __init__.py or main.py entry files.

            Args:
            path: Path to the plugin directory

            Returns:
            LoadData if successfully loaded, None otherwise

            """
            if not path.is_dir():
                return None

            try:
                # Find entry file
                entry_file = self._find_entry_file(path)
                if not entry_file:
                    return None

                # Load using spec-based approach
                spec = importlib.util.spec_from_file_location(path.name, entry_file)
                if not spec or not spec.loader:
                    return None

                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                return FlextPluginModels.Plugin.LoadData(
                    name=path.name,
                    version=getattr(module, "__version__", "1.0.0"),
                    path=path,
                    module=module,
                    load_type="directory",
                    loaded_at=datetime.now(UTC),
                    entry_file=entry_file,
                )
            except Exception:
                self.logger.exception(f"Failed to load directory plugin: {path}")
                return None

        def _find_entry_file(self, path: Path) -> Path | None:
            """Find entry file in directory (__init__.py or main.py).

            Args:
            path: Directory path to search

            Returns:
            Path to entry file if found, None otherwise

            """
            init_file = path / "__init__.py"
            main_file = path / "main.py"

            if init_file.exists():
                return init_file
            if main_file.exists():
                return main_file
            return None


__all__ = ["FlextPluginLoader"]
