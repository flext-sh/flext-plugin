"""FLEXT Plugin Core - Core plugin system components.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from flext_plugin.core.base import Plugin, PluginMetadata
from flext_plugin.core.discovery import PluginDiscovery
from flext_plugin.core.loader import PluginLoader
from flext_plugin.core.manager import PluginManager
from flext_plugin.core.types import (
    PluginCapability,
    PluginError,
    PluginExecutionResult,
    PluginLifecycle,
    PluginStatus,
    PluginType,
)
from flext_plugin.core.validators import PluginValidator

__all__ = [
    "Plugin",
    "PluginMetadata",
    "PluginDiscovery",
    "PluginLoader",
    "PluginManager",
    "PluginValidator",
    "PluginType",
    "PluginCapability",
    "PluginLifecycle",
    "PluginStatus",
    "PluginError",
    "PluginExecutionResult",
]
