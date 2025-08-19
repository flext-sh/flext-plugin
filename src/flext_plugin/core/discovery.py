"""FLEXT Core Plugin Discovery - Advanced plugin scanning and metadata extraction.

This module implements the core layer plugin discovery functionality,
providing sophisticated plugin scanning, metadata extraction, and plugin
classification capabilities. The discovery system serves as the foundation
for plugin management operations throughout the FLEXT ecosystem.
"""

from __future__ import annotations

import json
from pathlib import Path

from flext_core import FlextEntity, FlextGenerators, FlextResult, get_logger
from pydantic import Field

from flext_plugin.core.types import PluginType


class PluginDiscovery(FlextEntity):
    """Plugin discovery system to find and scan plugin files."""

    # Pydantic fields
    plugin_directory: str = Field(
        default="/usr/local/plugins",
        description="Primary plugin directory path",
    )
    plugin_directories: list[str] = Field(
        default_factory=list,
        description="Additional plugin directories to scan",
    )
    discovered_plugins: dict[str, object] = Field(
        default_factory=dict,
        description="Cache of discovered plugins",
        exclude=True,
    )
    blacklisted_plugins: set[str] = Field(
        default_factory=set,
        description="Set of blacklisted plugin IDs",
        exclude=True,
    )

    def __init__(
        self,
        *,
        entity_id: str | None = None,
        plugin_directory: str = "/usr/local/plugins",
        plugin_directories: list[str] | None = None,
        **_kwargs: object,
    ) -> None:
        """Initialize plugin discovery system."""
        # Generate ID if not provided
        final_entity_id = entity_id or FlextGenerators.generate_entity_id()
        # Initialize FlextEntity base with required fields
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        # Convert types for FlextEntity compatibility
        from typing import cast
        from flext_core.root_models import FlextEntityId, FlextVersion, FlextEventList, FlextMetadata, FlextTimestamp
        
        super().__init__(
            id=cast(FlextEntityId, final_entity_id),
            version=cast(FlextVersion, 1),
            domain_events=cast(FlextEventList, []),
            metadata=cast(FlextMetadata, {}),
            created_at=cast(FlextTimestamp, now),
            updated_at=cast(FlextTimestamp, now)
        )
        # Set business fields directly (frozen model workaround)
        object.__setattr__(self, "plugin_directory", plugin_directory)
        object.__setattr__(self, "plugin_directories", plugin_directories or [])
        object.__setattr__(self, "discovered_plugins", {})
        object.__setattr__(self, "blacklisted_plugins", set())

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate domain rules for plugin discovery."""
        if not self.plugin_directory:
            return FlextResult[None].fail("Plugin directory is required")
        return FlextResult[None].ok(None)

    def add_plugin_directory(self, directory: Path) -> None:
        """Add a plugin directory to scan."""
        directory_str = str(directory)
        if directory_str not in self.plugin_directories:
            # Modify the list in place (mutable object)
            self.plugin_directories.append(directory_str)

    async def discover_all(self) -> dict[str, object]:
        """Discover all plugins from configured directories."""
        await self._discover_entry_points()
        await self._discover_file_system()
        return self.discovered_plugins

    async def discover_by_type(self, plugin_type: PluginType) -> dict[str, object]:
        """Discover plugins by type."""
        all_plugins = await self.discover_all()
        from typing import cast
        return {
            name: plugin
            for name, plugin in all_plugins.items()
            if isinstance(plugin, dict) and cast("dict[str, object]", plugin).get("type") == plugin_type
        }

    def get_discovered_plugin(self, plugin_name: str) -> object | None:
        """Get a discovered plugin by name."""
        return self.discovered_plugins.get(plugin_name)

    def blacklist_plugin(self, plugin_id: str) -> None:
        """Blacklist a plugin."""
        self.blacklisted_plugins.add(plugin_id)

    def is_blacklisted(self, plugin_id: str) -> bool:
        """Check if a plugin is blacklisted."""
        return plugin_id in self.blacklisted_plugins

    def register_plugin(self, plugin_class: type) -> None:
        """Manually register a plugin class."""
        if self._validate_plugin_class(plugin_class):
            # Create plugin instance directly from class
            plugin_name = getattr(plugin_class, "METADATA", {}).get(
                "name",
                plugin_class.__name__,
            )
            plugin_instance = plugin_class()
            self.discovered_plugins[plugin_name] = plugin_instance

    async def _discover_entry_points(self) -> None:
        """Discover plugins from entry points."""
        # Entry point discovery implementation

    async def _discover_file_system(self) -> None:
        """Discover plugins from file system."""
        for directory_str in self.plugin_directories:
            directory = Path(directory_str)
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
                        self.discovered_plugins[metadata.get("name", py_file.stem)] = (
                            metadata
                        )
                except (json.JSONDecodeError, OSError) as e:
                    # Log manifest parsing error but continue discovery process
                    logger = get_logger(__name__)
                    logger.warning(
                        f"Failed to parse plugin manifest {manifest_file}: {e}",
                    )

    def _validate_plugin_class(self, plugin_class: type) -> bool:
        """Validate if a class is a valid plugin."""
        try:
            # Mock validation - check if it has required attributes
            required_methods = ["initialize", "cleanup", "health_check", "execute"]
            return all(hasattr(plugin_class, method) for method in required_methods)
        except (RuntimeError, ValueError, TypeError) as e:
            # Log critical validation error and raise proper exception instead of returning fake data
            logger = get_logger(__name__)
            logger.exception(f"Plugin class validation failed for {plugin_class}")
            msg = f"Plugin validation failed: {plugin_class}"
            raise RuntimeError(msg) from e


# Removed mock classes - use real implementations in tests
__all__: list[str] = [
    "PluginDiscovery",
]
