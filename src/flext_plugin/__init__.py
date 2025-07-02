"""FLEXT Plugin - Enterprise Plugin System with Hot Reload.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

__version__ = "0.1.0"

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

__all__ = [
    # Core
    "Plugin",
    "PluginCapability",
    "PluginDiscovery",
    "PluginError",
    "PluginExecutionResult",
    "PluginLifecycle",
    "PluginLoader",
    "PluginManager",
    "PluginMetadata",
    "PluginStatus",
    # Types
    "PluginType",
    # Version
    "__version__",
]
