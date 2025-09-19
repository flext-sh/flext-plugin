"""FLEXT Core Plugin Discovery - Advanced plugin scanning and metadata extraction.

This module implements the core layer plugin discovery functionality,
providing sophisticated plugin scanning, metadata extraction, and plugin
classification capabilities. The discovery system serves as the foundation
for plugin management operations throughout the FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

from pydantic import Field

from flext_core import (
    FlextLogger,
    FlextModels,
    FlextResult,
    FlextTypes,
    FlextUtilities,
)
from flext_plugin.flext_plugin_models import PluginType


class PluginDiscovery(FlextModels.Entity):
    """Plugin discovery system to find and scan plugin files."""

    # Pydantic fields
    plugin_directory: str = Field(
        default="/usr/local/plugins",
        description="Primary plugin directory path",
    )
    plugin_directories: FlextTypes.Core.StringList = Field(
        default_factory=list,
        description="Additional plugin directories to scan",
    )
    discovered_plugins: FlextTypes.Core.Dict = Field(
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
        plugin_directories: FlextTypes.Core.StringList | None = None,
        **_kwargs: object,
    ) -> None:
        """Initialize the instance."""
        # Generate ID if not provided using FlextUtilities
        final_entity_id = entity_id or FlextUtilities.Generators.generate_entity_id()
        # Initialize FlextModels base with required fields - use datetime for FlextModels compatibility
        datetime.now(UTC)
        # Convert types for FlextModels compatibility

        super().__init__(
            id=final_entity_id,
            version=1,
            domain_events=[],
        )
        # Set business fields directly (frozen model workaround)
        object.__setattr__(self, "plugin_directory", plugin_directory)
        object.__setattr__(self, "plugin_directories", plugin_directories or [])
        object.__setattr__(self, "discovered_plugins", {})
        object.__setattr__(self, "blacklisted_plugins", set())

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate domain rules for plugin discovery using FlextUtilities."""
        # Use FlextUtilities for validation - maintain original error message for test compatibility
        if not FlextUtilities.Validation.is_non_empty_string(self.plugin_directory):
            return FlextResult[None].fail("Plugin directory is required")
        return FlextResult[None].ok(None)

    def add_plugin_directory(self, directory: Path) -> None:
        """Add a plugin directory to scan using FlextUtilities validation."""
        directory_str = FlextUtilities.TextProcessor.safe_string(str(directory))
        if (
            FlextUtilities.Validation.is_non_empty_string(directory_str)
            and directory_str not in self.plugin_directories
        ):
            # Modify the list in place (mutable object)
            self.plugin_directories.append(directory_str)

    async def discover_all(self) -> FlextTypes.Core.Dict:
        """Discover all plugins from configured directories."""
        await self._discover_entry_points()
        await self._discover_file_system()
        return self.discovered_plugins

    async def discover_by_type(self, plugin_type: PluginType) -> FlextTypes.Core.Dict:
        """Discover plugins by type."""
        all_plugins = await self.discover_all()
        return {
            name: plugin
            for name, plugin in all_plugins.items()
            if isinstance(plugin, dict)
            and cast("FlextTypes.Core.Dict", plugin).get("type") == plugin_type
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
        # Always scan the primary plugin directory first
        if self.plugin_directory:
            primary_directory = Path(self.plugin_directory)
            await self._scan_directory(primary_directory)

        # Then scan additional directories
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

            plugin_name = py_file.stem

            # Look for manifest file
            manifest_file = py_file.with_suffix(".json")
            if manifest_file.exists():
                try:
                    # Use FlextUtilities for safe JSON parsing
                    manifest_content = manifest_file.read_text(encoding="utf-8")
                    metadata = json.loads(manifest_content)
                    plugin_name_key = FlextUtilities.TextProcessor.safe_string(
                        str(metadata.get("name", plugin_name)),
                    )
                    self.discovered_plugins[plugin_name_key] = metadata
                except Exception as e:
                    # Log manifest parsing/reading error using FlextUtilities
                    logger = FlextLogger(__name__)
                    logger.warning(
                        f"Failed to process plugin manifest {manifest_file}: {e}",
                    )
            else:
                # Create basic plugin metadata from file system information using FlextUtilities
                file_stat = py_file.stat()
                plugin_info = {
                    "name": FlextUtilities.TextProcessor.safe_string(plugin_name),
                    "path": FlextUtilities.TextProcessor.safe_string(str(py_file)),
                    "file_name": FlextUtilities.TextProcessor.safe_string(py_file.name),
                    "size": FlextUtilities.Conversions.safe_int(
                        file_stat.st_size,
                        default=0,
                    ),
                    "modified": FlextUtilities.Conversions.safe_float(
                        file_stat.st_mtime,
                        default=0.0,
                    ),
                    "module_name": FlextUtilities.TextProcessor.safe_string(
                        plugin_name,
                    ),
                    "plugin_class": "Plugin",  # Generic class name
                    "type": "generic",  # Generic type
                    "discovered_at": FlextUtilities.Generators.generate_iso_timestamp(),  # Add discovery timestamp
                    "discovery_id": FlextUtilities.Generators.generate_id(),  # Add unique discovery ID
                }
                safe_plugin_name = FlextUtilities.TextProcessor.safe_string(plugin_name)
                if FlextUtilities.Validation.is_non_empty_string(safe_plugin_name):
                    self.discovered_plugins[safe_plugin_name] = plugin_info

    def _validate_plugin_class(self, plugin_class: type) -> bool:
        """Validate if a class is a valid plugin using FlextUtilities."""
        try:
            # Check if it has required attributes using FlextUtilities
            required_methods = ["initialize", "cleanup", "health_check", "execute"]
            for method_name in required_methods:
                if not hasattr(plugin_class, method_name):
                    return False

            return True
        except (RuntimeError, ValueError, TypeError) as e:
            # Log critical validation error using FlextUtilities and proper error handling
            logger = FlextLogger(__name__)
            plugin_name = FlextUtilities.TextProcessor.safe_string(
                getattr(plugin_class, "__name__", "Unknown"),
            )
            logger.exception(f"Plugin class validation failed for {plugin_name}")
            msg = f"Plugin validation failed: {plugin_name}"
            raise RuntimeError(msg) from e


# Removed mock classes - use real implementations in tests
__all__: FlextTypes.Core.StringList = [
    "PluginDiscovery",
]
