"""FLEXT Plugin Discovery - Strategy-based plugin discovery with Pydantic models.

Complete plugin discovery using strategy pattern for different discovery
methods (file system, entry points). All operations return Pydantic models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib.metadata
from collections.abc import Callable
from pathlib import Path
from typing import TypeVar

from flext_core import FlextLogger, r

from flext_plugin import FlextPluginModels, c, p

TDiscovery = TypeVar("TDiscovery")


def discover_python_plugins_in_directory[TDiscovery](
    path: Path,
    discover_file: Callable[[Path], TDiscovery | None],
    logger: FlextLogger,
) -> list[TDiscovery]:
    discovered: list[TDiscovery] = []
    try:
        for item in path.iterdir():
            if (
                item.is_file()
                and item.suffix == ".py"
                and (not item.name.startswith("_"))
            ):
                data = discover_file(item)
                if data:
                    discovered.append(data)
            elif item.is_dir() and (not item.name.startswith("__")):
                discovered.extend(
                    discover_python_plugins_in_directory(item, discover_file, logger),
                )
    except (OSError, PermissionError):
        logger.exception("Failed to discover directory %s", path)
    return discovered


class FlextPluginDiscovery:
    """Plugin discovery using strategy pattern.

    Discovers plugins using multiple strategies (file system, entry points).
    Delegates discovery logic to strategy classes, Pydantic handles validation.
    """

    def __init__(self) -> None:
        """Initialize discovery with all strategies."""
        self.logger = FlextLogger(__name__)
        self.strategies: list[p.Plugin.DiscoveryStrategy] = [
            self.FileSystemStrategy(self.logger),
            self.EntryPointStrategy(self.logger),
        ]

    def discover_plugin(
        self,
        plugin_path: str,
    ) -> r[FlextPluginModels.Plugin.DiscoveryData]:
        """Discover single plugin at path.

        Args:
        plugin_path: Path to the plugin

        Returns:
        r containing plugin data

        """
        try:
            path_obj = Path(plugin_path).expanduser().resolve()
            if path_obj.exists():
                fs_strategy = self.FileSystemStrategy(self.logger)
                result = fs_strategy.discover([plugin_path])
                if result.is_success and result.value:
                    return r[FlextPluginModels.Plugin.DiscoveryData].ok(
                        value=result.value[0],
                    )
            ep_strategy = self.EntryPointStrategy(self.logger)
            result = ep_strategy.discover([plugin_path])
            if result.is_success and result.value:
                return r[FlextPluginModels.Plugin.DiscoveryData].ok(
                    value=result.value[0],
                )
            return r[FlextPluginModels.Plugin.DiscoveryData].fail(
                f"Plugin not found at: {plugin_path}",
            )
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to discover plugin at %s", plugin_path)
            return r[FlextPluginModels.Plugin.DiscoveryData].fail(
                f"Discovery error: {e!s}",
            )

    def discover_plugins(
        self,
        paths: list[str],
    ) -> r[list[FlextPluginModels.Plugin.DiscoveryData]]:
        """Discover plugins using all strategies.

        Args:
        paths: List of paths to search for plugins

        Returns:
        r containing list of discovered plugins

        """
        try:
            discovered: dict[str, FlextPluginModels.Plugin.DiscoveryData] = {}
            for strategy in self.strategies:
                result = strategy.discover(paths)
                if result.is_success:
                    for data in result.value:
                        if data.name not in discovered:
                            discovered[data.name] = data
            self.logger.info(f"Discovered {len(discovered)} unique plugins")
            return r[list[FlextPluginModels.Plugin.DiscoveryData]].ok(
                value=list(discovered.values()),
            )
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Plugin discovery failed")
            return r[list[FlextPluginModels.Plugin.DiscoveryData]].fail(
                f"Discovery error: {e!s}",
            )

    def validate_plugin(
        self,
        plugin_data: FlextPluginModels.Plugin.DiscoveryData,
    ) -> r[bool]:
        """Validate discovered plugin data.

        Pydantic automatically validates on model creation.

        Args:
        plugin_data: Plugin data to validate

        Returns:
        r indicating validation success

        """
        try:
            self.logger.debug(f"Plugin validation passed: {plugin_data.name}")
            return r[bool].ok(value=True)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Plugin validation failed")
            return r[bool].fail(f"Validation error: {e!s}")

    class FileSystemStrategy:
        """File system-based plugin discovery strategy."""

        def __init__(self, logger: FlextLogger) -> None:
            """Initialize strategy with logger."""
            self.logger = logger

        def discover(
            self,
            paths: list[str],
        ) -> r[list[FlextPluginModels.Plugin.DiscoveryData]]:
            """Discover plugins in file system paths."""
            try:
                discovered: list[FlextPluginModels.Plugin.DiscoveryData] = []
                for path_str in paths:
                    path = Path(path_str).expanduser().resolve()
                    if not path.exists():
                        self.logger.warning("Path does not exist: %s", path_str)
                        continue
                    if path.is_file():
                        data = self._discover_file(path)
                        if data:
                            discovered.append(data)
                    elif path.is_dir():
                        discovered.extend(self._discover_directory(path))
                self.logger.info(
                    f"File system discovery found {len(discovered)} plugins",
                )
                return r[list[FlextPluginModels.Plugin.DiscoveryData]].ok(
                    value=discovered,
                )
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                RuntimeError,
                ImportError,
            ) as e:
                self.logger.exception("File system discovery failed")
                return r[list[FlextPluginModels.Plugin.DiscoveryData]].fail(
                    f"File discovery error: {e!s}",
                )

        def _discover_directory(
            self,
            path: Path,
        ) -> list[FlextPluginModels.Plugin.DiscoveryData]:
            """Recursively discover plugins in directory."""
            return discover_python_plugins_in_directory(
                path,
                self._discover_file,
                self.logger,
            )

        def _discover_file(
            self,
            path: Path,
        ) -> FlextPluginModels.Plugin.DiscoveryData | None:
            """Discover single Python file as plugin."""
            if path.suffix != ".py":
                return None
            try:
                return FlextPluginModels.Plugin.DiscoveryData(
                    name=path.stem,
                    version=c.Plugin.Discovery.DEFAULT_PLUGIN_VERSION,
                    path=path,
                    discovery_type=c.Plugin.Discovery.DISCOVERY_TYPE_FILE,
                    discovery_method=c.Plugin.Discovery.METHOD_FILE_SYSTEM,
                    metadata={},
                )
            except ValueError:
                self.logger.exception("Failed to create discovery data for %s", path)
                return None

    class EntryPointStrategy:
        """Entry point-based plugin discovery strategy."""

        def __init__(self, logger: FlextLogger) -> None:
            """Initialize strategy with logger."""
            self.logger = logger

        def discover(
            self,
            paths: list[str],
        ) -> r[list[FlextPluginModels.Plugin.DiscoveryData]]:
            """Discover plugins using entry points (paths ignored)."""
            _ = paths
            try:
                discovered: list[FlextPluginModels.Plugin.DiscoveryData] = []
                for entry_point in importlib.metadata.entry_points().select(
                    group="flext.plugins",
                ):
                    try:
                        data = FlextPluginModels.Plugin.DiscoveryData(
                            name=entry_point.name,
                            version=getattr(
                                entry_point.dist,
                                "version",
                                c.Plugin.Discovery.DEFAULT_PLUGIN_VERSION,
                            )
                            or c.Plugin.Discovery.DEFAULT_PLUGIN_VERSION,
                            path=Path(getattr(entry_point.dist, "_path", "")),
                            discovery_type=c.Plugin.Discovery.DISCOVERY_TYPE_ENTRY_POINT,
                            discovery_method=c.Plugin.Discovery.METHOD_ENTRY_POINTS,
                            metadata={
                                "entry_point": f"{entry_point.module}:{entry_point.attr}",
                            },
                        )
                        discovered.append(data)
                    except ValueError:
                        self.logger.debug(f"Invalid entry point: {entry_point.name}")
                        continue
                self.logger.info(
                    f"Entry point discovery found {len(discovered)} plugins",
                )
                return r[list[FlextPluginModels.Plugin.DiscoveryData]].ok(
                    value=discovered,
                )
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                RuntimeError,
                ImportError,
            ) as e:
                self.logger.exception("Entry point discovery failed")
                return r[list[FlextPluginModels.Plugin.DiscoveryData]].fail(
                    f"Entry point discovery error: {e!s}",
                )


__all__ = ["FlextPluginDiscovery"]
