"""Core type re-exports for the plugin system.

This module exposes public types from the centralized type modules for
downstream imports following flext-core patterns.
"""

from __future__ import annotations

from .exceptions import PluginError

# Import core types and exceptions from centralized modules
from .flext_plugin_models import (
    FlextPluginConfigModel,
    FlextPluginMetadataModel,
    FlextPluginModel,
    PluginExecutionContextModel,
    PluginExecutionResultModel,
    PluginManagerResultModel,
    PluginStatus,
    PluginType,
)
from .type_definitions import (
    PluginBoolResult,
    PluginDiscoveryProtocol,
    PluginExecutorProtocol,
    PluginLoaderProtocol,
    PluginProtocol,
    PluginRegistryProtocol,
    PluginResult,
    PluginStringResult,
    TPlugin,
    TPluginConfig,
    TPluginResult,
)

# Legacy compatibility classes will be in a separate compatibility module
from .typings_legacy import (
    PluginExecutionContext,
    PluginExecutionResult,
    PluginManagerResult,
    SimplePluginRegistry,
    create_plugin_manager,
)

__all__: list[str] = [
    "FlextPluginConfigModel",
    "FlextPluginMetadataModel",
    "FlextPluginModel",
    "PluginBoolResult",
    "PluginDiscoveryProtocol",
    # Exceptions
    "PluginError",
    # Legacy compatibility (for now)
    "PluginExecutionContext",
    "PluginExecutionContextModel",
    "PluginExecutionResult",
    "PluginExecutionResultModel",
    "PluginExecutorProtocol",
    "PluginLoaderProtocol",
    "PluginManagerResult",
    "PluginManagerResultModel",
    # Type protocols
    "PluginProtocol",
    "PluginRegistryProtocol",
    # Result types
    "PluginResult",
    # Core models
    "PluginStatus",
    "PluginStringResult",
    "PluginType",
    "SimplePluginRegistry",
    # Type variables
    "TPlugin",
    "TPluginConfig",
    "TPluginResult",
    "create_plugin_manager",
]
