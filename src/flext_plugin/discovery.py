"""Plugin discovery system for scanning and finding plugins."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from flext_core.domain.pydantic_base import DomainBaseModel


class PluginDiscovery(DomainBaseModel):
    """Plugin discovery system to find and scan plugin files."""

    plugin_directory: str

    model_config = {"arbitrary_types_allowed": True}

    async def scan(self) -> list[dict[str, Any]]:
        """Scan the plugin directory for Python plugin files.

        Returns:
            List of dictionaries containing plugin file information including
            name, path, file_name, size, and modified time.

        """
        plugins: list[Any] = []
        plugin_path = Path(self.plugin_directory)

        if not plugin_path.exists():
            return plugins

        for py_file in plugin_path.glob("*.py"):
            if py_file.name.startswith("__"):
                continue

            plugin_info = {
                "name": py_file.stem,
                "path": py_file,
                "file_name": py_file.name,
                "size": py_file.stat().st_size,
                "modified": py_file.stat().st_mtime,
            }
            plugins.append(plugin_info)

        return plugins

    async def discover_plugin_entry_points(self) -> list[dict[str, Any]]:
        """Discover plugin entry points from scanned plugin files.

        Returns:
            List of dictionaries containing entry point information including
            name, module_name, plugin_class, path, and type.

        """
        plugins = await self.scan()
        entry_points = []

        for plugin in plugins:
            entry_point = {
                "name": plugin["name"],
                "module_name": plugin["name"],
                "plugin_class": "Plugin",  # Default class name
                "path": plugin["path"],
                "type": "generic",
            }
            entry_points.append(entry_point)

        return entry_points
