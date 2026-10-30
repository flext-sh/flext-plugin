"""Plugin discovery utility for flext-plugin.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import importlib.metadata
from collections.abc import Callable, MutableMapping, MutableSequence, Sequence
from pathlib import Path

from flext_cli import u

from flext_plugin import c, m, p, r


class FlextPluginDiscovery:
    """Plugin discovery using strategy pattern.

    Discovers plugins using multiple strategies (file system, entry points).
    Delegates discovery logic to strategy classes, Pydantic handles validation.

    """

    def __init__(self) -> None:
        """Initialize discovery with all strategies."""
        self.logger = u.fetch_logger(__name__)
        self.strategies: Sequence[p.Plugin.DiscoveryStrategy] = [
            self.FileSystemStrategy(self.logger),
            self.EntryPointStrategy(self.logger),
        ]

    @staticmethod
    def discover_python_plugins_in_directory[TDiscovery](
        path: Path,
        discover_file: Callable[[Path], TDiscovery | None],
        logger: p.Logger,
    ) -> Sequence[TDiscovery]:
        """Discover Python plugins recursively in a directory.

        Args:
            path: Directory to scan recursively for ``*.py`` files.
            discover_file: Callable producing discovery data for one
                candidate file, or ``None`` to skip it.
            logger: Logger for discovery failures.

        Returns:
            The discovered plugin data records; empty when the directory
            cannot be read.

        """
        discovered: MutableSequence[TDiscovery] = []
        try:
            items = tuple(path.iterdir())
        except OSError:
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

    def discover_plugin(self, plugin_path: str) -> p.Result[m.Plugin.DiscoveryData]:
        """Discover single plugin at path.

        Args:
            plugin_path: Path to the plugin.

        Returns:
            Ok with the plugin data, or Fail when the plugin is not
            found.

        """
        try:
            path_obj = Path(plugin_path).expanduser().resolve()
            discovered = self._discover_existing_or_entry_point(plugin_path, path_obj)
            if discovered is not None:
                return r[m.Plugin.DiscoveryData].ok(value=discovered)
            return r[m.Plugin.DiscoveryData].fail(f"Plugin not found at: {plugin_path}")
        except c.EXC_BROAD_IO_TYPE as error:
            self.logger.exception("Failed to discover plugin at %s", plugin_path)
            return r[m.Plugin.DiscoveryData].fail(
                f"Discovery error: {error!s}",
                exception=error,
            )

    def discover_plugins(
        self,
        paths: Sequence[str],
    ) -> p.Result[Sequence[m.Plugin.DiscoveryData]]:
        """Discover plugins using all strategies.

        Args:
            paths: Paths to search for plugins.

        Returns:
            Ok with the discovered plugins, or Fail with the discovery
            error.

        """
        try:
            discovered = self._discover_unique_plugins(paths)
            self.logger.info("Discovered %s unique plugins", len(discovered))
            return r[Sequence[m.Plugin.DiscoveryData]].ok(
                value=list(discovered.values()),
            )
        except c.EXC_BROAD_IO_TYPE as error:
            self.logger.exception("Plugin discovery failed")
            return r[Sequence[m.Plugin.DiscoveryData]].fail(
                f"Discovery error: {error!s}",
                exception=error,
            )

    def validate_plugin(self, plugin_data: m.Plugin.DiscoveryData) -> p.Result[bool]:
        """Validate discovered plugin data.

        Pydantic automatically validates on model creation.

        Args:
            plugin_data: Plugin data to validate.

        Returns:
            Ok with ``True`` when validation passes, or Fail with the
            validation error.

        """
        try:
            self.logger.debug("Plugin validation passed: %s", plugin_data.name)
            return r[bool].ok(value=True)
        except c.EXC_BROAD_IO_TYPE as error:
            self.logger.exception("Plugin validation failed")
            return r[bool].fail(f"Validation error: {error!s}", exception=error)

    def _discover_existing_or_entry_point(
        self,
        plugin_path: str,
        path_obj: Path,
    ) -> m.Plugin.DiscoveryData | None:
        """Discover one plugin from filesystem first, then entry points.

        Args:
            plugin_path: Path string used by the strategy lookup.
            path_obj: Resolved filesystem path of the plugin.

        Returns:
            The discovery data from the first matching strategy, or
            ``None`` when no strategy discovers the path.

        """
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
        paths: Sequence[str],
    ) -> MutableMapping[str, m.Plugin.DiscoveryData]:
        """Discover unique plugins across all configured strategies.

        Args:
            paths: Paths to search for plugins.

        Returns:
            Mapping of plugin name to its first discovered data record.

        """
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
        """Return the first discovery hit for one strategy.

        Args:
            strategy: Discovery strategy to run.
            plugin_path: Path to discover.

        Returns:
            The first discovered data record, or ``None`` when the
            strategy finds nothing.

        """
        result = strategy.discover([plugin_path])
        if result.success and result.value:
            data: m.Plugin.DiscoveryData = result.value[0]
            return data
        return None

    class _DiscoveryStrategyBase:
        """Shared base for plugin discovery strategies."""

        def __init__(self, logger: p.Logger) -> None:
            """Initialize strategy with logger.

            Args:
                logger: Logger used for discovery traceability.

            """
            self.logger = logger

    class FileSystemStrategy(_DiscoveryStrategyBase):
        """File system-based plugin discovery strategy."""

        def discover(
            self,
            paths: Sequence[str],
        ) -> p.Result[Sequence[m.Plugin.DiscoveryData]]:
            """Discover plugins in file system paths.

            Args:
                paths: Paths to scan for plugin modules.

            Returns:
                Ok with the discovered plugins, or Fail with the
                discovery error.

            """
            try:
                discovered = self._discover_paths(paths)
                self.logger.info(
                    "File system discovery found %s plugins",
                    len(discovered),
                )
                return r[Sequence[m.Plugin.DiscoveryData]].ok(value=discovered)
            except c.EXC_BROAD_IO_TYPE as error:
                self.logger.exception("File system discovery failed")
                return r[Sequence[m.Plugin.DiscoveryData]].fail(
                    f"File discovery error: {error!s}",
                    exception=error,
                )

        def _discover_directory(
            self,
            path: Path,
        ) -> Sequence[m.Plugin.DiscoveryData]:
            """Recursively discover plugins in directory.

            Args:
                path: Directory to scan recursively.

            Returns:
                The discovered plugin data records.

            """
            return FlextPluginDiscovery.discover_python_plugins_in_directory(
                path,
                self._discover_file,
                self.logger,
            )

        @staticmethod
        def _discover_file(path: Path) -> m.Plugin.DiscoveryData | None:
            """Discover single Python file as plugin.

            # Why: DiscoveryData construction failure is a real defect, not a
            # skip condition; it propagates instead of being masked as None.

            Args:
                path: Candidate file path.

            Returns:
                The discovery data for the file, or ``None`` when the
                file is not a ``.py`` module.

            """
            if path.suffix != ".py":
                return None
            return m.Plugin.DiscoveryData(
                name=path.stem,
                version=c.Plugin.DEFAULT_PLUGIN_VERSION,
                path=path,
                discovery_type=c.Plugin.DiscoveryTypeLiteral.FILE,
                discovery_method=c.Plugin.DiscoveryMethodLiteral.FILE_SYSTEM,
                metadata={},
            )

        def _discover_path(self, path_str: str) -> Sequence[m.Plugin.DiscoveryData]:
            """Discover plugins from one path string.

            Args:
                path_str: Path string to resolve and scan.

            Returns:
                The discovered plugin data records; empty for blank,
                missing, or unsupported paths.

            """
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
            paths: Sequence[str],
        ) -> Sequence[m.Plugin.DiscoveryData]:
            """Discover plugins from all path strings.

            Args:
                paths: Path strings to resolve and scan.

            Returns:
                The discovered plugin data records.

            """
            discovered: MutableSequence[m.Plugin.DiscoveryData] = []
            for path_str in paths:
                discovered.extend(self._discover_path(path_str))
            return discovered

    class EntryPointStrategy(_DiscoveryStrategyBase):
        """Entry point-based plugin discovery strategy."""

        def discover(
            self,
            paths: Sequence[str],
        ) -> p.Result[Sequence[m.Plugin.DiscoveryData]]:
            """Discover plugins using entry points (paths ignored).

            Args:
                paths: Accepted for protocol compatibility; ignored.

            Returns:
                Ok with the discovered plugins, or Fail with the
                discovery error.

            """
            _ = paths
            try:
                discovered = self._discover_entry_points()
                self.logger.info(
                    "Entry point discovery found %s plugins",
                    len(discovered),
                )
                return r[Sequence[m.Plugin.DiscoveryData]].ok(value=discovered)
            except c.EXC_BROAD_IO_TYPE as error:
                self.logger.exception("Entry point discovery failed")
                return r[Sequence[m.Plugin.DiscoveryData]].fail(
                    f"Entry point discovery error: {error!s}",
                    exception=error,
                )

        @staticmethod
        def _discover_entry_point(
            entry_point: importlib.metadata.EntryPoint,
        ) -> m.Plugin.DiscoveryData | None:
            """Build discovery data for one entry point.

            # Why: an invalid entry point is a real defect, not a skip
            # condition; construction failure propagates instead of being
            # masked as None.

            Args:
                entry_point: Entry point to convert.

            Returns:
                The discovery data for the entry point, or ``None`` when
                it has no distribution.

            """
            distribution = entry_point.dist
            if distribution is None:
                return None
            version = (
                getattr(distribution, "version", c.Plugin.DEFAULT_PLUGIN_VERSION)
                or c.Plugin.DEFAULT_PLUGIN_VERSION
            )
            return m.Plugin.DiscoveryData(
                name=entry_point.name,
                version=version,
                path=Path(str(distribution.locate_file(""))),
                discovery_type=c.Plugin.DiscoveryTypeLiteral.ENTRY_POINT,
                discovery_method=c.Plugin.DiscoveryMethodLiteral.ENTRY_POINTS,
                metadata={"entry_point": f"{entry_point.module}:{entry_point.attr}"},
            )

        def _discover_entry_points(self) -> Sequence[m.Plugin.DiscoveryData]:
            """Discover plugins from the installed entry point registry.

            Returns:
                The discovery data records of all ``flext.plugins`` entry
                points with a distribution.

            """
            discovered: MutableSequence[m.Plugin.DiscoveryData] = []
            for entry_point in importlib.metadata.entry_points().select(
                group="flext.plugins",
            ):
                data = self._discover_entry_point(entry_point)
                if data is not None:
                    discovered.append(data)
            return discovered


__all__: list[str] = ["FlextPluginDiscovery"]
