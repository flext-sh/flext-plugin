"""FLEXT Plugin Utilities - Internal subpackage.

Re-exports all utility namespace classes for MRO composition.
"""

from __future__ import annotations

from flext_plugin._utilities.adapters import FlextPluginAdapters
from flext_plugin._utilities.discovery import FlextPluginDiscovery
from flext_plugin._utilities.entities import FlextPluginEntities
from flext_plugin._utilities.handlers import FlextPluginHandlers
from flext_plugin._utilities.hot_reload import (
    FlextPluginFileChangeHandler,
    FlextPluginHotReload,
)
from flext_plugin._utilities.implementations import FlextPluginImplementations
from flext_plugin._utilities.loader import FlextPluginLoader
from flext_plugin._utilities.plugin_platform import FlextPluginPlatform
from flext_plugin._utilities.services import FlextPluginService

__all__ = [
    "FlextPluginAdapters",
    "FlextPluginDiscovery",
    "FlextPluginEntities",
    "FlextPluginFileChangeHandler",
    "FlextPluginHandlers",
    "FlextPluginHotReload",
    "FlextPluginImplementations",
    "FlextPluginLoader",
    "FlextPluginPlatform",
    "FlextPluginService",
]
