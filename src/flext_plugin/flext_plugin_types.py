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

# Legacy compatibility classes from services module
from .flext_plugin_services import (
    SimplePluginRegistry,
    create_plugin_manager,
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

# Legacy classes for compatibility - using aliases
PluginExecutionContext = dict[str, object]  # Type alias for execution context
PluginManagerResult = object  # Type alias for manager result

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
    # Factory functions
    "create_plugin_manager",
]
