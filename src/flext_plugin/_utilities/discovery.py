"""FLEXT Plugin Discovery - Strategy-based plugin discovery with Pydantic models.

Complete plugin discovery using strategy pattern for different discovery
methods (file system, entry points). All operations return Pydantic models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib.metadata
from collections.abc import Callable, MutableMapping, MutableSequence, Sequence
from pathlib import Path

from flext_cli import u
from flext_plugin import c, m, p, r, t


class FlextPluginDiscovery:
    """Plugin discovery using strategy pattern.

    Discovers plugins using multiple strategies (file system, entry points).
    Delegates discovery logic to strategy classes, Pydantic handles validation.
    """

    def __init__(self) -> None:
        """Initialize discovery with all strategies."""
        self.logger = u.fetch_logger(__name__)
        self.strategies: t.SequenceOf[p.Plugin.DiscoveryStrategy] = [
            self.FileSystemStrategy(self.logger),
            self.EntryPointStrategy(self.logger),
        ]

    @staticmethod
    def discover_python_plugins_in_directory[TDiscovery](
        path: Path,
        discover_file: Callable[[Path], TDiscovery | None],
        logger: p.Logger,
    ) -> t.SequenceOf[TDiscovery]:
        """Discover Python plugins recursively in a directory."""
        discovered: MutableSequence[TDiscovery] = []
        try:
            items = tuple(path.iterdir())
        except (OSError, PermissionError):
            logger.exception("Failed to discover directory %s", path)
            return discovered
        for item in items:
            if (
                item.is_file()
                and item.suffix == ".py"
                and not item.name.startswith("_")
            ):
                data = discover_file(item)
                if data:
                    discovered.append(data)
            elif item.is_dir() and not item.name.startswith("__"):
                discovered.extend(
                    FlextPluginDiscovery.discover_python_plugins_in_directory(
                        item,
                        discover_file,
                        logger,
                    ),
                )
        return discovered

    def discover_plugin(
        self,
        plugin_path: str,
    ) -> p.Result[m.Plugin.DiscoveryData]:
        """Discover single plugin at path.

        Args:
        plugin_path: Path to the plugin

        Returns:
        r containing plugin data

        """
        try:
            path_obj = Path(plugin_path).expanduser().resolve()
            discovered = self._discover_existing_or_entry_point(plugin_path, path_obj)
            if discovered is not None:
                return r[m.Plugin.DiscoveryData].ok(value=discovered)
            return r[m.Plugin.DiscoveryData].fail(
                f"Plugin not found at: {plugin_path}",
            )
        except c.EXC_BROAD_IO_TYPE as e:
            self.logger.exception("Failed to discover plugin at %s", plugin_path)
            return r[m.Plugin.DiscoveryData].fail(
                f"Discovery error: {e!s}",
            )

    def discover_plugins(
        self,
        paths: t.StrSequence,
    ) -> p.Result[Sequence[m.Plugin.DiscoveryData]]:
        """Discover plugins using all strategies.

        Args:
        paths: List of paths to search for plugins

        Returns:
        r containing list of discovered plugins

        """
        try:
            discovered = self._discover_unique_plugins(paths)
            self.logger.info(f"Discovered {len(discovered)} unique plugins")
            return r[Sequence[m.Plugin.DiscoveryData]].ok(
                value=list(discovered.values()),
            )
        except c.EXC_BROAD_IO_TYPE as e:
            self.logger.exception("Plugin discovery failed")
            return r[Sequence[m.Plugin.DiscoveryData]].fail(
                f"Discovery error: {e!s}",
            )

    def validate_plugin(
        self,
        plugin_data: m.Plugin.DiscoveryData,
    ) -> p.Result[bool]:
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
        except c.EXC_BROAD_IO_TYPE as e:
            self.logger.exception("Plugin validation failed")
            return r[bool].fail(f"Validation error: {e!s}")

    def _discover_existing_or_entry_point(
        self,
        plugin_path: str,
        path_obj: Path,
    ) -> m.Plugin.DiscoveryData | None:
        """Discover one plugin from filesystem first, then entry points."""
        if path_obj.exists():
            file_discovered = self._first_discovery(
                self.FileSystemStrategy(self.logger),
                plugin_path,
            )
            if file_discovered is not None:
                return file_discovered
        return self._first_discovery(self.EntryPointStrategy(self.logger), plugin_path)

    def _discover_unique_plugins(
        self,
        paths: t.StrSequence,
    ) -> MutableMapping[str, m.Plugin.DiscoveryData]:
        """Discover unique plugins across all configured strategies."""
        discovered: MutableMapping[str, m.Plugin.DiscoveryData] = {}
        for strategy in self.strategies:
            result = strategy.discover(paths)
            if result.success:
                for data in result.value:
                    if data.name not in discovered:
                        discovered[data.name] = data
        return discovered

    @staticmethod
    def _first_discovery(
        strategy: p.Plugin.DiscoveryStrategy,
        plugin_path: str,
    ) -> m.Plugin.DiscoveryData | None:
        """Return the first discovery hit for one strategy."""
        result = strategy.discover([plugin_path])
        if result.success and result.value:
            return result.value[0]
        return None

    class FileSystemStrategy:
        """File system-based plugin discovery strategy."""

        def __init__(self, logger: p.Logger) -> None:
            """Initialize strategy with logger."""
            self.logger = logger

        def discover(
            self,
            paths: t.StrSequence,
        ) -> p.Result[Sequence[m.Plugin.DiscoveryData]]:
            """Discover plugins in file system paths."""
            try:
                discovered = self._discover_paths(paths)
                self.logger.info(
                    f"File system discovery found {len(discovered)} plugins",
                )
                return r[Sequence[m.Plugin.DiscoveryData]].ok(
                    value=discovered,
                )
            except c.EXC_BROAD_IO_TYPE as e:
                self.logger.exception("File system discovery failed")
                return r[Sequence[m.Plugin.DiscoveryData]].fail(
                    f"File discovery error: {e!s}",
                )

        def _discover_directory(
            self,
            path: Path,
        ) -> t.SequenceOf[m.Plugin.DiscoveryData]:
            """Recursively discover plugins in directory."""
            return FlextPluginDiscovery.discover_python_plugins_in_directory(
                path,
                self._discover_file,
                self.logger,
            )

        def _discover_file(
            self,
            path: Path,
        ) -> m.Plugin.DiscoveryData | None:
            """Discover single Python file as plugin."""
            if path.suffix != ".py":
                return None
            try:
                return m.Plugin.DiscoveryData(
                    name=path.stem,
                    version=c.Plugin.DEFAULT_PLUGIN_VERSION,
                    path=path,
                    discovery_type=c.Plugin.DiscoveryTypeLiteral.FILE,
                    discovery_method=c.Plugin.DiscoveryMethodLiteral.FILE_SYSTEM,
                    metadata={},
                )
            except ValueError:
                self.logger.exception("Failed to create discovery data for %s", path)
                return None

        def _discover_path(self, path_str: str) -> t.SequenceOf[m.Plugin.DiscoveryData]:
            """Discover plugins from one path string."""
            if not path_str.strip():
                self.logger.debug("Skipping blank plugin discovery path")
                return ()
            path = Path(path_str).expanduser().resolve()
            if not path.exists():
                self.logger.warning("Path does not exist: %s", path_str)
                return ()
            if path.is_file():
                data = self._discover_file(path)
                return (data,) if data is not None else ()
            if path.is_dir():
                return self._discover_directory(path)
            return ()

        def _discover_paths(
            self,
            paths: t.StrSequence,
        ) -> t.SequenceOf[m.Plugin.DiscoveryData]:
            """Discover plugins from all path strings."""
            discovered: MutableSequence[m.Plugin.DiscoveryData] = []
            for path_str in paths:
                discovered.extend(self._discover_path(path_str))
            return discovered

    class EntryPointStrategy:
        """Entry point-based plugin discovery strategy."""

        def __init__(self, logger: p.Logger) -> None:
            """Initialize strategy with logger."""
            self.logger = logger

        def discover(
            self,
            paths: t.StrSequence,
        ) -> p.Result[Sequence[m.Plugin.DiscoveryData]]:
            """Discover plugins using entry points (paths ignored)."""
            _ = paths
            try:
                discovered = self._discover_entry_points()
                self.logger.info(
                    f"Entry point discovery found {len(discovered)} plugins",
                )
                return r[Sequence[m.Plugin.DiscoveryData]].ok(
                    value=discovered,
                )
            except c.EXC_BROAD_IO_TYPE as e:
                self.logger.exception("Entry point discovery failed")
                return r[Sequence[m.Plugin.DiscoveryData]].fail(
                    f"Entry point discovery error: {e!s}",
                )

        def _discover_entry_point(
            self,
            entry_point: importlib.metadata.EntryPoint,
        ) -> m.Plugin.DiscoveryData | None:
            """Build discovery data for one entry point."""
            try:
                return m.Plugin.DiscoveryData(
                    name=entry_point.name,
                    version=getattr(
                        entry_point.dist,
                        "version",
                        c.Plugin.DEFAULT_PLUGIN_VERSION,
                    )
                    or c.Plugin.DEFAULT_PLUGIN_VERSION,
                    path=Path(getattr(entry_point.dist, "_path", "")),
                    discovery_type=c.Plugin.DiscoveryTypeLiteral.ENTRY_POINT,
                    discovery_method=c.Plugin.DiscoveryMethodLiteral.ENTRY_POINTS,
                    metadata={
                        "entry_point": f"{entry_point.module}:{entry_point.attr}",
                    },
                )
            except ValueError:
                self.logger.debug(f"Invalid entry point: {entry_point.name}")
                return None

        def _discover_entry_points(self) -> t.SequenceOf[m.Plugin.DiscoveryData]:
            """Discover plugins from the installed entry point registry."""
            discovered: MutableSequence[m.Plugin.DiscoveryData] = []
            for entry_point in importlib.metadata.entry_points().select(
                group="flext.plugins",
            ):
                data = self._discover_entry_point(entry_point)
                if data is not None:
                    discovered.append(data)
            return discovered


__all__: list[str] = ["FlextPluginDiscovery"]
