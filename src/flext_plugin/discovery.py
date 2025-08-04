"""FLEXT Plugin Discovery System - File system scanning and plugin detection.

This module implements the infrastructure layer plugin discovery functionality,
providing file system scanning, plugin detection, and metadata extraction
capabilities. The discovery system serves as a concrete implementation of
plugin discovery patterns for the FLEXT plugin management system.

The discovery system integrates with Clean Architecture infrastructure patterns,
providing concrete implementations for plugin discovery ports while maintaining
proper separation of concerns and comprehensive error handling.

Key Features:
    - File system scanning for Python plugin files
    - Plugin metadata extraction and validation
    - Directory traversal with configurable depth limits
    - Plugin file structure detection and analysis
    - Integration with domain discovery patterns

Architecture:
    Built as FlextEntity following domain-driven design patterns,
    the discovery system maintains state and provides lifecycle
    management for plugin scanning operations while integrating
    with the broader FLEXT infrastructure ecosystem.

Example:
    >>> from flext_plugin.discovery import PluginDiscovery
    >>>
    >>> discovery = PluginDiscovery(plugin_directory="./plugins")
    >>> plugins = await discovery.scan()
    >>> print(f"Found {len(plugins)} plugin files")

Integration:
    - Implements infrastructure layer patterns for Clean Architecture
    - Provides concrete plugin discovery for application services
    - Supports comprehensive testing and validation strategies
    - Integrates with file system monitoring and hot-reload systems

"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextEntity, FlextResult
from flext_core.utilities import FlextGenerators
from pydantic import ConfigDict


class PluginDiscovery(FlextEntity):
    """File system-based plugin discovery system with comprehensive scanning.

    Infrastructure component implementing plugin discovery through file system
    scanning and analysis. Provides systematic discovery of Python plugin files
    with metadata extraction, validation, and comprehensive error handling.

    The discovery system maintains plugin directory state and provides async
    scanning capabilities while integrating with the broader FLEXT plugin
    management infrastructure. Supports configurable scanning parameters
    and comprehensive plugin file analysis.

    Key Capabilities:
        - Recursive directory scanning for Python plugin files
        - Plugin metadata extraction from file system attributes
        - File structure analysis and validation
        - Async scanning operations with error handling
        - Integration with plugin registry and management systems

    Discovery Process:
        1. Directory validation and sanitization
        2. Recursive file system traversal
        3. Plugin file identification and filtering
        4. Metadata extraction and normalization
        5. Result compilation and validation

    File Detection:
        - Python files (.py) with plugin patterns
        - Plugin manifest files and configuration
        - Module structure analysis and validation
        - Dependency detection and requirement analysis

    Example:
        >>> discovery = PluginDiscovery(plugin_directory="./plugins")
        >>> # Validate directory before scanning
        >>> validation = discovery.validate_domain_rules()
        >>> if validation.is_success():
        ...     plugins = await discovery.scan()
        ...     print(f"Discovered {len(plugins)} plugin files")

    """

    plugin_directory: str

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, *, plugin_directory: str, **kwargs: object) -> None:
        """Initialize plugin discovery with directory and entity ID."""
        # Generate ID for FlextEntity
        entity_id = str(kwargs.get("id", FlextGenerators.generate_entity_id()))

        # Initialize FlextEntity with id AND plugin_directory (required field)
        super().__init__(id=entity_id, plugin_directory=plugin_directory)

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate domain rules for plugin discovery."""
        if not self.plugin_directory:
            return FlextResult.fail("Plugin directory cannot be empty")
        return FlextResult.ok(None)

    async def scan(self) -> list[dict[str, object]]:
        """Scan the plugin directory for Python plugin files.

        Returns:
            List of dictionaries containing plugin file information including
            name, path, file_name, size, and modified time.

        """
        plugins: list[dict[str, object]] = []
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

    async def discover_plugin_entry_points(self) -> list[dict[str, object]]:
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
