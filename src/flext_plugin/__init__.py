"""FLEXT Plugin System - Enterprise-grade plugin management for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

This module provides comprehensive plugin management capabilities including:
- Plugin discovery and loading
- Plugin execution and lifecycle management
- Hot reload and file monitoring
- Security validation and sandboxing
- Event handling and monitoring
- Clean Architecture and DDD patterns

Usage:
    ```python
    from flext_plugin import FlextPluginApi


    # Initialize plugin system
    container = FlextContainer()
    api = FlextPluginApi(container)

    # Discover and load plugins
    result = api.discover_plugins(["./plugins"])
    if result.success:
        plugins = result.value
        print(f"Discovered {len(plugins)} plugins")

    # Execute a plugin
    execution_result = api.execute_plugin("my-plugin", {"input": "data"})
    ```
"""

from __future__ import annotations

from typing import Final

from flext_plugin.__version__ import __version__, __version_info__
from flext_plugin.adapters import FlextPluginAdapters
from flext_plugin.api import FlextPluginApi
from flext_plugin.config import FlextPluginConfig
from flext_plugin.constants import FlextPluginConstants
from flext_plugin.handlers import FlextPluginHandlers
from flext_plugin.hot_reload import FlextPluginHotReload
from flext_plugin.loader import FlextPluginLoader

# Models consolidated into entities for generic design
from flext_plugin.platform import FlextPluginPlatform
from flext_plugin.plugin import Plugin, PluginStatus, PluginType
from flext_plugin.plugin_config import PluginConfig
from flext_plugin.plugin_execution import PluginExecution
from flext_plugin.plugin_metadata import PluginMetadata
from flext_plugin.plugin_registry import PluginRegistry
from flext_plugin.protocols import FlextPluginProtocols
from flext_plugin.services import FlextPluginService
from flext_plugin.types import FlextPluginTypes
from flext_plugin.version import VERSION, FlextPluginVersion

# Version information
PROJECT_VERSION: Final[FlextPluginVersion] = VERSION

# Main API exports
__all__ = [
    "PROJECT_VERSION",
    # Version information
    "VERSION",
    "FlextPluginAdapters",
    # Core API
    "FlextPluginApi",
    "FlextPluginConfig",
    # Core classes following [Project][Module] pattern
    "FlextPluginConstants",
    "FlextPluginHandlers",
    "FlextPluginHotReload",
    "FlextPluginLoader",
    "FlextPluginPlatform",
    "FlextPluginProtocols",
    "FlextPluginService",
    "FlextPluginTypes",
    # Domain entities
    "Plugin",
    "PluginConfig",
    "PluginExecution",
    "PluginMetadata",
    "PluginRegistry",
    "PluginStatus",
    "PluginType",
    "__version__",
    "__version_info__",
]
