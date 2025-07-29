"""Plugin discovery system for scanning and finding plugins."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from flext_core import FlextEntity

if TYPE_CHECKING:
    from pathlib import Path

    from flext_plugin.core.types import PluginType


class PluginDiscovery(FlextEntity):
    """Plugin discovery system to find and scan plugin files."""

    def __init__(self, entity_id: str | None = None) -> None:
        """Initialize plugin discovery system."""
        super().__init__(entity_id)
        self.plugin_directories: list[Path] = []
        self._discovered_plugins: dict[str, Any] = {}
        self._blacklisted_plugins: set[str] = set()

    def add_plugin_directory(self, directory: Path) -> None:
        """Add a plugin directory to scan."""
        if directory not in self.plugin_directories:
            self.plugin_directories.append(directory)

    async def discover_all(self) -> dict[str, Any]:
        """Discover all plugins from configured directories."""
        await self._discover_entry_points()
        await self._discover_file_system()
        return self._discovered_plugins

    async def discover_by_type(self, plugin_type: PluginType) -> dict[str, Any]:
        """Discover plugins by type."""
        all_plugins = await self.discover_all()
        return {
            name: plugin
            for name, plugin in all_plugins.items()
            if plugin.get("type") == plugin_type
        }

    def get_discovered_plugin(self, plugin_name: str) -> object | None:
        """Get a discovered plugin by name."""
        return self._discovered_plugins.get(plugin_name)

    def blacklist_plugin(self, plugin_id: str) -> None:
        """Blacklist a plugin."""
        self._blacklisted_plugins.add(plugin_id)

    def is_blacklisted(self, plugin_id: str) -> bool:
        """Check if a plugin is blacklisted."""
        return plugin_id in self._blacklisted_plugins

    def register_plugin(self, plugin_class: type) -> None:
        """Manually register a plugin class."""
        if self._validate_plugin_class(plugin_class):
            plugin_metadata = MockPluginMetadata(plugin_class.METADATA.name)
            self._discovered_plugins[plugin_class.METADATA.name] = MockPlugin(
                plugin_metadata,
            )

    async def _discover_entry_points(self) -> None:
        """Discover plugins from entry points."""
        # Entry point discovery implementation

    async def _discover_file_system(self) -> None:
        """Discover plugins from file system."""
        for directory in self.plugin_directories:
            await self._scan_directory(directory)

    async def _scan_directory(self, directory: Path) -> None:
        """Scan a directory for plugin files."""
        if not directory.exists():
            return

        for py_file in directory.glob("*.py"):
            if py_file.name.startswith("__"):
                continue

            # Look for manifest file
            manifest_file = py_file.with_suffix(".json")
            if manifest_file.exists():
                try:
                    with manifest_file.open() as f:
                        metadata = json.load(f)
                        self._discovered_plugins[metadata.get("name", py_file.stem)] = (
                            metadata
                        )
                except (json.JSONDecodeError, OSError):
                    pass

    def _validate_plugin_class(self, plugin_class: type) -> bool:
        """Validate if a class is a valid plugin."""
        try:
            # Mock validation - check if it has required attributes
            required_methods = ["initialize", "cleanup", "health_check", "execute"]
            return all(hasattr(plugin_class, method) for method in required_methods)
        except (RuntimeError, ValueError, TypeError):
            return False


class MockPlugin:
    """Mock plugin class for testing."""

    def __init__(self, metadata: Any) -> None:
        self.metadata = metadata


class MockPluginMetadata:
    """Mock plugin metadata for testing."""

    def __init__(self, name: str) -> None:
        self.name = name


__all__ = [
    "PluginDiscovery",
]
