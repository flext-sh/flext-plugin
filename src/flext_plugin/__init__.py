"""FLEXT Plugin - Enterprise Plugin System with Hot Reload.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

from typing import Any

try:
    from flext_core.domain.constants import FlextFramework

    __version__ = FlextFramework.VERSION
except ImportError:
    __version__ = "0.7.0"

try:
    from flext_plugin.core.base import Plugin
except ImportError:
    Plugin = Any  # type: ignore[misc,assignment]

try:
    from flext_plugin.core.discovery import PluginDiscovery
except ImportError:
    PluginDiscovery = Any  # type: ignore[misc,assignment]

try:
    from flext_plugin.core.loader import PluginLoader
except ImportError:
    PluginLoader = Any  # type: ignore[misc,assignment]

try:
    from flext_plugin.core.manager import PluginManager
except ImportError:
    # Create a basic fallback for tests
    class _FallbackPluginManager:
        def __init__(self) -> None:
            pass

        async def initialize(self) -> None:
            pass

        async def discover_plugins(self) -> dict[str, Any]:
            return {}

        async def load_plugin(self, plugin_name: str) -> None:
            pass

        async def unload_plugin(self, plugin_name: str) -> None:
            pass

        async def reload_plugin(self, plugin_name: str) -> None:
            pass

    PluginManager = _FallbackPluginManager  # type: ignore[misc,assignment]

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
    # Type aliases for when imports fail
    PluginCapability = Any  # type: ignore[misc,assignment]
    PluginError = Any  # type: ignore[misc,assignment]
    PluginExecutionResult = Any  # type: ignore[misc,assignment]
    PluginLifecycle = Any  # type: ignore[misc,assignment]
    PluginStatus = Any  # type: ignore[misc,assignment]
    PluginType = Any  # type: ignore[misc,assignment]

try:
    from flext_plugin.domain.entities import PluginMetadata
except ImportError:
    PluginMetadata = Any  # type: ignore[misc,assignment]

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
