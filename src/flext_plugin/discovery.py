"""FLEXT Plugin Discovery - Plugin discovery mechanisms.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import asyncio
import importlib
import importlib.metadata
import os
import re
from pathlib import Path

from flext_core import FlextConstants, FlextLogger, FlextResult, FlextTypes

from flext_plugin.protocols import FlextPluginProtocols
from flext_plugin.types import FlextPluginTypes


class FlextPluginDiscovery:
    """Plugin discovery service implementing comprehensive plugin discovery mechanisms.

    This class provides multiple discovery strategies including file system scanning,
    entry point discovery, and package-based discovery for maximum flexibility.

    Usage:
        ```python
        from flext_plugin import FlextPluginDiscovery

        # Initialize discovery service
        discovery = FlextPluginDiscovery()

        # Discover plugins in multiple paths
        result = await discovery.discover_plugins(["./plugins", "/opt/flext/plugins"])
        if result.success:
            plugins = result.value
            print(f"Discovered {len(plugins)} plugins")
        ```
    """

    def __init__(
        self,
        file_discovery: FlextPluginProtocols.PluginDiscovery | None = None,
        entry_point_discovery: FlextPluginProtocols.PluginDiscovery | None = None,
    ) -> None:
        """Initialize the plugin discovery service.

        Args:
            file_discovery: File system discovery implementation
            entry_point_discovery: Entry point discovery implementation

        """
        self.logger = FlextLogger(__name__)
        self._file_discovery = file_discovery or self.FileSystemDiscovery()
        self._entry_point_discovery = (
            entry_point_discovery or self.EntryPointDiscovery()
        )

    def _resolve_plugin_path(self, plugin_path: str) -> Path:
        """Resolve and validate a plugin path synchronously.

        Args:
            plugin_path: Path to resolve

        Returns:
            Resolved Path object

        """
        return Path(plugin_path).expanduser().resolve()

    def _read_file_sync(self, path: Path) -> str:
        """Read file content synchronously.

        Args:
            path: Path to the file

        Returns:
            File content as string

        """
        with path.open(encoding="utf-8") as f:
            return f.read()

    async def discover_plugins(
        self, paths: FlextTypes.StringList
    ) -> FlextResult[list[FlextPluginTypes.Core.PluginDict]]:
        """Discover plugins using multiple discovery strategies.

        Args:
            paths: List of paths to search for plugins

        Returns:
            FlextResult containing list of discovered plugins

        """
        try:
            all_plugins = []
            discovered_plugins = set()  # Track unique plugins by name

            # File system discovery
            file_result = await self._file_discovery.discover_plugins(paths)
            if file_result.is_success:
                for plugin in file_result.value:
                    plugin_name = plugin.get("name")
                    if plugin_name and plugin_name not in discovered_plugins:
                        all_plugins.append(plugin)
                        discovered_plugins.add(plugin_name)

            # Entry point discovery
            entry_point_result = await self._entry_point_discovery.discover_plugins(
                paths
            )
            if entry_point_result.is_success:
                for plugin in entry_point_result.value:
                    plugin_name = plugin.get("name")
                    if plugin_name and plugin_name not in discovered_plugins:
                        all_plugins.append(plugin)
                        discovered_plugins.add(plugin_name)

            self.logger.info(f"Discovered {len(all_plugins)} unique plugins")
            return FlextResult.ok(all_plugins)

        except Exception as e:
            self.logger.exception("Plugin discovery failed")
            return FlextResult.fail(f"Discovery error: {e!s}")

    async def discover_plugin(
        self, plugin_path: str
    ) -> FlextResult[FlextPluginTypes.Core.PluginDict]:
        """Discover a single plugin at the given path.

        Args:
            plugin_path: Path to the plugin

        Returns:
            FlextResult containing plugin data

        """
        try:
            path_obj = self._resolve_plugin_path(plugin_path)

            # Try file system discovery first
            if path_obj.exists():
                file_result = await self._file_discovery.discover_plugin(plugin_path)
                if file_result.is_success:
                    return file_result

            # Try entry point discovery
            entry_point_result = await self._entry_point_discovery.discover_plugin(
                plugin_path
            )
            if entry_point_result.is_success:
                return entry_point_result

            return FlextResult.fail(f"Plugin not found at: {plugin_path}")

        except Exception as e:
            self.logger.exception(f"Failed to discover plugin at {plugin_path}")
            return FlextResult.fail(f"Discovery error: {e!s}")

    async def validate_plugin(
        self, plugin_data: FlextPluginTypes.Core.PluginDict
    ) -> FlextResult[bool]:
        """Validate discovered plugin data.

        Args:
            plugin_data: Plugin data to validate

        Returns:
            FlextResult indicating validation success or failure

        """
        try:
            # Validate required fields
            required_fields = ["name", "version"]
            for field in required_fields:
                if field not in plugin_data:
                    return FlextResult.fail(f"Missing required field: {field}")

            # Validate plugin name format
            plugin_name = plugin_data["name"]
            if not self._is_valid_plugin_name(plugin_name):
                return FlextResult.fail(f"Invalid plugin name format: {plugin_name}")

            # Validate version format
            version = plugin_data["version"]
            if not self._is_valid_version(version):
                return FlextResult.fail(f"Invalid version format: {version}")

            self.logger.debug(f"Plugin validation passed: {plugin_name}")
            return FlextResult.ok(True)

        except Exception as e:
            self.logger.exception("Plugin validation failed")
            return FlextResult.fail(f"Validation error: {e!s}")

    def _is_valid_plugin_name(self, name: str) -> bool:
        """Check if plugin name follows valid format.

        Args:
            name: Plugin name to validate

        Returns:
            True if name is valid, False otherwise

        """
        pattern = r"^[a-zA-Z][a-zA-Z0-9_-]*$"
        return (
            bool(re.match(pattern, name))
            and FlextConstants.Validation.MIN_NAME_LENGTH
            <= len(name)
            <= FlextConstants.Validation.MAX_NAME_LENGTH
        )

    def _is_valid_version(self, version: str) -> bool:
        """Check if version follows semantic versioning format.

        Args:
            version: Version string to validate

        Returns:
            True if version is valid, False otherwise

        """
        pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$"
        return bool(re.match(pattern, version))

    class FileSystemDiscovery:
        """File system-based plugin discovery implementation."""

        def __init__(self) -> None:
            """Initialize file system discovery."""
            self.logger = FlextLogger(__name__)

        async def discover_plugins(
            self, paths: FlextTypes.StringList
        ) -> FlextResult[list[FlextPluginTypes.Core.PluginDict]]:
            """Discover plugins in file system paths.

            Args:
                paths: List of paths to search

            Returns:
                FlextResult containing list of discovered plugins

            """
            try:
                discovered_plugins = []

                for path in paths:
                    path_obj = self._resolve_plugin_path(path)
                    if not path_obj.exists():
                        self.logger.warning(f"Path does not exist: {path}")
                        continue

                    if path_obj.is_file():
                        # Single file plugin
                        plugin_data = await self._discover_single_file(path_obj)
                        if plugin_data:
                            discovered_plugins.append(plugin_data)
                    elif path_obj.is_dir():
                        # Directory with multiple plugins
                        plugins = await self._discover_directory(path_obj)
                        discovered_plugins.extend(plugins)

                self.logger.info(
                    f"File system discovery found {len(discovered_plugins)} plugins"
                )
                return FlextResult.ok(discovered_plugins)

            except Exception as e:
                self.logger.exception("File system discovery failed")
                return FlextResult.fail(f"File discovery error: {e!s}")

        async def discover_plugin(
            self, plugin_path: str
        ) -> FlextResult[FlextPluginTypes.Core.PluginDict]:
            """Discover a single plugin file.

            Args:
                plugin_path: Path to the plugin file

            Returns:
                FlextResult containing plugin data

            """
            try:
                path_obj = self._resolve_plugin_path(plugin_path)
                if not path_obj.exists():
                    return FlextResult.fail(
                        f"Plugin path does not exist: {plugin_path}"
                    )

                plugin_data = await self._discover_single_file(path_obj)
                if not plugin_data:
                    return FlextResult.fail(
                        f"Failed to discover plugin at: {plugin_path}"
                    )

                return FlextResult.ok(plugin_data)

            except Exception as e:
                self.logger.exception(f"Failed to discover plugin at {plugin_path}")
                return FlextResult.fail(f"File discovery error: {e!s}")

        async def validate_plugin(
            self, plugin_data: FlextPluginTypes.Core.PluginDict
        ) -> FlextResult[bool]:
            """Validate file-based plugin data.

            Args:
                plugin_data: Plugin data to validate

            Returns:
                FlextResult indicating validation success or failure

            """
            try:
                # Check if plugin file exists and is readable
                plugin_path = plugin_data.get("path")
                if not plugin_path:
                    return FlextResult.fail("Plugin path is required")

                path_obj = self._resolve_plugin_path(plugin_path)
                if not path_obj.exists() or not path_obj.is_file():
                    return FlextResult.fail(
                        f"Plugin file does not exist: {plugin_path}"
                    )

                if not os.access(path_obj, os.R_OK):
                    return FlextResult.fail(
                        f"Plugin file is not readable: {plugin_path}"
                    )

                return FlextResult.ok(True)

            except Exception as e:
                self.logger.exception("File plugin validation failed")
                return FlextResult.fail(f"File validation error: {e!s}")

        async def _discover_single_file(
            self, path: Path
        ) -> FlextPluginTypes.Core.PluginDict | None:
            """Discover a single plugin file.

            Args:
                path: Path to the plugin file

            Returns:
                Plugin data if discovered, None otherwise

            """
            try:
                if path.suffix != ".py":
                    return None

                # Extract plugin name from filename
                plugin_name = path.stem

                # Try to extract version from file
                version = await self._extract_version_from_file(path)

                # Basic plugin data
                return {
                    "name": plugin_name,
                    "version": version,
                    "path": str(path),
                    "type": "file",
                    "discovery_method": "file_system",
                }

            except Exception:
                self.logger.exception(f"Failed to discover single file: {path}")
                return None

        async def _discover_directory(
            self, path: Path
        ) -> list[FlextPluginTypes.Core.PluginDict]:
            """Discover plugins in a directory.

            Args:
                path: Path to the directory

            Returns:
                List of discovered plugin data

            """
            try:
                discovered_plugins = []

                # Run pathlib operations in thread pool
                loop = asyncio.get_event_loop()
                items = await loop.run_in_executor(None, list, path.iterdir())  # noqa: ASYNC240

                for item in items:
                    if (
                        item.is_file()
                        and item.suffix == ".py"
                        and not item.name.startswith("_")
                    ):
                        plugin_data = await self._discover_single_file(item)
                        if plugin_data:
                            discovered_plugins.append(plugin_data)
                    elif item.is_dir() and not item.name.startswith("__"):
                        # Recursively discover in subdirectories
                        sub_plugins = await self._discover_directory(item)
                        discovered_plugins.extend(sub_plugins)

                return discovered_plugins

            except Exception:
                self.logger.exception(f"Failed to discover directory: {path}")
                return []

        async def _extract_version_from_file(self, path: Path) -> str:
            """Extract version information from a plugin file.

            Args:
                path: Path to the plugin file

            Returns:
                Version string (defaults to "1.0.0" if not found)

            """
            try:
                # Read file asynchronously using thread pool
                loop = asyncio.get_event_loop()
                content = await loop.run_in_executor(None, self._read_file_sync, path)

                # Look for version patterns
                version_patterns = [
                    r'__version__\s*=\s*["\']([^"\']+)["\']',
                    r'version\s*=\s*["\']([^"\']+)["\']',
                    r'VERSION\s*=\s*["\']([^"\']+)["\']',
                ]

                for pattern in version_patterns:
                    match = re.search(pattern, content)
                    if match:
                        return match.group(1)

                return "1.0.0"

            except Exception as e:
                self.logger.debug(f"Failed to extract version from {path}: {e}")
                return "1.0.0"

    class EntryPointDiscovery:
        """Entry point-based plugin discovery implementation."""

        def __init__(self) -> None:
            """Initialize entry point discovery."""
            self.logger = FlextLogger(__name__)

        async def discover_plugins(
            self,
            paths: FlextTypes.StringList,  # noqa: ARG002
        ) -> FlextResult[list[FlextPluginTypes.Core.PluginDict]]:
            """Discover plugins using entry points.

            Args:
                paths: List of paths to search (not used for entry points)

            Returns:
                FlextResult containing list of discovered plugins

            """
            try:
                discovered_plugins = []

                # Look for entry points in installed packages
                for entry_point in importlib.metadata.entry_points().select(
                    group="flext.plugins"
                ):
                    plugin_data = {
                        "name": entry_point.name,
                        "version": getattr(entry_point.dist, "version", "1.0.0"),
                        "entry_point": f"{entry_point.module}:{entry_point.attr}",
                        "type": "entry_point",
                        "discovery_method": "entry_points",
                    }
                    discovered_plugins.append(plugin_data)

                self.logger.info(
                    f"Entry point discovery found {len(discovered_plugins)} plugins"
                )
                return FlextResult.ok(discovered_plugins)

            except Exception as e:
                self.logger.exception("Entry point discovery failed")
                return FlextResult.fail(f"Entry point discovery error: {e!s}")

        async def discover_plugin(
            self, plugin_path: str
        ) -> FlextResult[FlextPluginTypes.Core.PluginDict]:
            """Discover a single plugin using entry points.

            Args:
                plugin_path: Plugin identifier (not used for entry points)

            Returns:
                FlextResult containing plugin data

            """
            try:
                # For entry points, we search by name
                plugin_name = plugin_path

                entry_points = list(
                    importlib.metadata.entry_points().select(
                        group="flext.plugins", name=plugin_name
                    )
                )

                if not entry_points:
                    return FlextResult.fail(f"Entry point not found: {plugin_name}")

                entry_point = entry_points[0]
                plugin_data = {
                    "name": entry_point.name,
                    "version": getattr(entry_point.dist, "version", "1.0.0"),
                    "entry_point": f"{entry_point.module}:{entry_point.attr}",
                    "type": "entry_point",
                    "discovery_method": "entry_points",
                }

                return FlextResult.ok(plugin_data)

            except Exception as e:
                self.logger.exception(
                    f"Failed to discover entry point plugin: {plugin_path}"
                )
                return FlextResult.fail(f"Entry point discovery error: {e!s}")

        async def validate_plugin(
            self, plugin_data: FlextPluginTypes.Core.PluginDict
        ) -> FlextResult[bool]:
            """Validate entry point-based plugin data.

            Args:
                plugin_data: Plugin data to validate

            Returns:
                FlextResult indicating validation success or failure

            """
            try:
                # Check if entry point is valid
                entry_point = plugin_data.get("entry_point")
                if not entry_point:
                    return FlextResult.fail("Entry point is required")

                # Validate entry point format
                if ":" not in entry_point:
                    return FlextResult.fail("Invalid entry point format")

                module_name, attr_name = entry_point.split(":", 1)
                if not module_name or not attr_name:
                    return FlextResult.fail("Invalid entry point format")

                # Try to import the module to validate it exists
                importlib.import_module(module_name)

                return FlextResult.ok(True)

            except Exception as e:
                self.logger.exception("Entry point plugin validation failed")
                return FlextResult.fail(f"Entry point validation error: {e!s}")


__all__ = ["FlextPluginDiscovery"]
