"""Core type re-exports for the plugin system.

This module exposes public types from ``flext_plugin.typings`` for
downstream imports (e.g., ``from flext_plugin.core.types import PluginType``).
"""

from __future__ import annotations

from flext_plugin.typings import (
    PluginError,
    PluginExecutionContext,
    PluginExecutionResult,
    PluginManagerResult,
    PluginStatus,
    PluginType,
    SimplePluginRegistry,
    create_plugin_manager,
)

__all__: list[str] = [
    "PluginError",
    "PluginExecutionContext",
    "PluginExecutionResult",
    "PluginManagerResult",
    "PluginStatus",
    "PluginType",
    "SimplePluginRegistry",
    "create_plugin_manager",
]
