"""FLEXT Plugin - Enterprise Plugin System with Hot Reload.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

try:
    from flext_core.domain.constants import FlextFramework

    __version__ = FlextFramework.VERSION
except ImportError:
    __version__ = "0.7.0"

# Core imports with error handling for missing components
try:
    from flext_plugin.core.base import Plugin
except ImportError:
    Plugin = None

try:
    from flext_plugin.core.discovery import PluginDiscovery
except ImportError:
    PluginDiscovery = None

try:
    from flext_plugin.core.loader import PluginLoader
except ImportError:
    PluginLoader = None

try:
    from flext_plugin.core.manager import PluginManager
except ImportError:
    PluginManager = None
try:
    from flext_plugin.core.types import (
        PluginCapability,
        PluginError,
        PluginExecutionResult,
        PluginLifecycle,
        PluginStatus,
        PluginType,
    )
except ImportError:
    PluginCapability = None
    PluginError = None
    PluginExecutionResult = None
    PluginLifecycle = None
    PluginStatus = None
    PluginType = None

try:
    from flext_plugin.domain.entities import PluginMetadata
except ImportError:
    PluginMetadata = None

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
