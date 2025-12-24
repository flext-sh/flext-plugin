"""FLEXT Plugin Discovery - Strategy-based plugin discovery with Pydantic models.

Complete plugin discovery using strategy pattern for different discovery
methods (file system, entry points). All operations return Pydantic models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib.metadata
from pathlib import Path

from flext import FlextLogger, FlextResult
from flext_plugin.models import FlextPluginModels
from flext_plugin.protocols import p


class FlextPluginDiscovery:
    """Plugin discovery using strategy pattern.

    Discovers plugins using multiple strategies (file system, entry points).
    Delegates discovery logic to strategy classes, Pydantic handles validation.
    """

    # Protocol reference from centralized protocols.py for backward compatibility
    DiscoveryStrategy = p.Plugin.DiscoveryStrategyProtocol

    def __init__(self) -> None:
        """Initialize discovery with all strategies."""
        self.logger = FlextLogger(__name__)
        self.strategies: list[FlextPluginDiscovery.DiscoveryStrategy] = [
            self.FileSystemStrategy(self.logger),  # type: ignore[assignment]
            self.EntryPointStrategy(self.logger),  # type: ignore[assignment]
        ]

    def discover_plugins(
        self,
        paths: list[str],
    ) -> FlextResult[list[FlextPluginModels.DiscoveryData]]:
        """Discover plugins using all strategies.

        Args:
        paths: List of paths to search for plugins

        Returns:
        FlextResult containing list of discovered plugins

        """
        try:
            discovered: dict[str, FlextPluginModels.DiscoveryData] = {}

            for strategy in self.strategies:
                result = strategy.discover(paths)
                if result.is_success:
                    for data in result.value:
                        if data.name not in discovered:
                            discovered[data.name] = data

            self.logger.info(f"Discovered {len(discovered)} unique plugins")
            return FlextResult.ok(list(discovered.values()))

        except Exception as e:
            self.logger.exception("Plugin discovery failed")
            return FlextResult.fail(f"Discovery error: {e!s}")

    def discover_plugin(
        self,
        plugin_path: str,
    ) -> FlextResult[FlextPluginModels.DiscoveryData]:
        """Discover single plugin at path.

        Args:
        plugin_path: Path to the plugin

        Returns:
        FlextResult containing plugin data

        """
        try:
            path_obj = Path(plugin_path).expanduser().resolve()

            # Try file system strategy first
            if path_obj.exists():
                fs_strategy = self.FileSystemStrategy(self.logger)
                result = fs_strategy.discover([plugin_path])
                if result.is_success and result.value:
                    return FlextResult.ok(result.value[0])

            # Try entry point strategy
            ep_strategy = self.EntryPointStrategy(self.logger)
            result = ep_strategy.discover([plugin_path])
            if result.is_success and result.value:
                return FlextResult.ok(result.value[0])

            return FlextResult.fail(f"Plugin not found at: {plugin_path}")

        except Exception as e:
            self.logger.exception("Failed to discover plugin at %s", plugin_path)
            return FlextResult.fail(f"Discovery error: {e!s}")

    def validate_plugin(
        self,
        plugin_data: FlextPluginModels.DiscoveryData,
    ) -> FlextResult[bool]:
        """Validate discovered plugin data.

        Pydantic automatically validates on model creation.

        Args:
        plugin_data: Plugin data to validate

        Returns:
        FlextResult indicating validation success

        """
        try:
            # Pydantic validates on model instantiation, so if we have a
            # DiscoveryData instance, it's already valid
            self.logger.debug(f"Plugin validation passed: {plugin_data.name}")
            return FlextResult.ok(True)
        except Exception as e:
            self.logger.exception("Plugin validation failed")
            return FlextResult.fail(f"Validation error: {e!s}")

    class FileSystemStrategy:
        """File system-based plugin discovery strategy."""

        def __init__(self, logger: FlextLogger) -> None:
            """Initialize strategy with logger."""
            self.logger = logger

        def discover(
            self,
            paths: list[str],
        ) -> FlextResult[list[FlextPluginModels.DiscoveryData]]:
            """Discover plugins in file system paths."""
            try:
                discovered = []

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
                return FlextResult.ok(discovered)

            except Exception as e:
                self.logger.exception("File system discovery failed")
                return FlextResult.fail(f"File discovery error: {e!s}")

        def _discover_file(
            self,
            path: Path,
        ) -> FlextPluginModels.DiscoveryData | None:
            """Discover single Python file as plugin."""
            if path.suffix != ".py":
                return None

            try:
                return FlextPluginModels.DiscoveryData(
                    name=path.stem,
                    version="1.0.0",
                    path=path,
                    discovery_type="file",
                    discovery_method="file_system",
                )
            except ValueError:
                self.logger.exception("Failed to create discovery data for %s", path)
                return None

        def _discover_directory(
            self,
            path: Path,
        ) -> list[FlextPluginModels.DiscoveryData]:
            """Recursively discover plugins in directory."""
            discovered = []

            try:
                for item in path.iterdir():
                    if (
                        item.is_file()
                        and item.suffix == ".py"
                        and not item.name.startswith("_")
                    ):
                        data = self._discover_file(item)
                        if data:
                            discovered.append(data)
                    elif item.is_dir() and not item.name.startswith("__"):
                        discovered.extend(self._discover_directory(item))

            except (OSError, PermissionError):
                self.logger.exception("Failed to discover directory %s", path)

            return discovered

    class EntryPointStrategy:
        """Entry point-based plugin discovery strategy."""

        def __init__(self, logger: FlextLogger) -> None:
            """Initialize strategy with logger."""
            self.logger = logger

        def discover(
            self,
            _paths: list[str],
        ) -> FlextResult[list[FlextPluginModels.DiscoveryData]]:
            """Discover plugins using entry points (paths ignored)."""
            try:
                discovered = []

                # Look for entry points in installed packages
                for entry_point in importlib.metadata.entry_points().select(
                    group="flext.plugins",
                ):
                    try:
                        data = FlextPluginModels.DiscoveryData(
                            name=entry_point.name,
                            version=getattr(entry_point.dist, "version", "1.0.0"),
                            path=Path(getattr(entry_point.dist, "_path", "")),
                            discovery_type="entry_point",
                            discovery_method="entry_points",
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
                return FlextResult.ok(discovered)

            except Exception as e:
                self.logger.exception("Entry point discovery failed")
                return FlextResult.fail(f"Entry point discovery error: {e!s}")


__all__ = ["FlextPluginDiscovery"]
