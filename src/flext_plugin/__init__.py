"""FLEXT Plugin System - Enterprise-grade plugin management for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Final

from flext_plugin.api import FlextPlugin
from flext_plugin.config import FlextPluginConfig
from flext_plugin.constants import FlextPluginConstants
from flext_plugin.entities import (
    FlextPluginEntity,
    FlextPluginMetadata,
    FlextPluginRegistry,
    FlextPluginExecution,
    Plugin,
    PluginMetadata,
)
from flext_plugin.discovery import PluginDiscovery
from flext_plugin.hot_reload import HotReloadManager
from flext_plugin.loader import PluginLoader
from flext_plugin.ports import FlextPluginLoaderPort
from flext_plugin.exceptions import FlextPluginError, FlextPluginExceptions
from flext_plugin.flext_plugin_platform import FlextPluginPlatform
from flext_plugin.flext_plugin_services import (
    FlextPluginDiscoveryService,
    FlextPluginService,
)
from flext_plugin.flext_plugin_handlers import (
    FlextPluginEventHandler,
    FlextPluginHandler,
)
from flext_plugin.models import FlextPluginModels, PluginStatus, PluginType
from flext_plugin.real_adapters import (
    RealPluginDiscoveryAdapter,
    RealPluginLoaderAdapter,
    RealPluginManagerAdapter,
)
from flext_plugin.simple_api import FlextPluginSimpleApi
from flext_plugin.simple_plugin import PluginRegistry
from flext_plugin.version import VERSION, FlextPluginVersion

PROJECT_VERSION: Final[FlextPluginVersion] = VERSION

__version__: str = VERSION.version
__version_info__: tuple[int | str, ...] = VERSION.version_info

# Legacy aliases for backward compatibility
PluginConfig = FlextPluginConfig
PluginConfiguration = FlextPluginConfig
PluginInstance = FlextPluginEntity
PluginError = FlextPluginError
PluginExecutionContextModel = FlextPluginModels.ExecutionContextModel
PluginExecutionResultModel = FlextPluginModels.ExecutionResultModel
PluginManagerResultModel = FlextPluginModels.ManagerResultModel
create_registry = PluginRegistry.create_registry
create_flext_plugin = FlextPluginSimpleApi.create_flext_plugin
create_flext_plugin_config = FlextPluginSimpleApi.create_flext_plugin_config
create_flext_plugin_metadata = FlextPluginSimpleApi.create_flext_plugin_metadata
create_flext_plugin_registry = FlextPluginSimpleApi.create_flext_plugin_registry
create_plugin_from_dict = FlextPluginSimpleApi.create_plugin_from_dict
create_plugin_config_from_dict = FlextPluginSimpleApi.create_plugin_config_from_dict
# Legacy aliases
create_plugin = create_flext_plugin
create_plugin_config = create_flext_plugin_config
create_plugin_metadata = create_flext_plugin_metadata
create_plugin_registry = create_flext_plugin_registry
PluginDiscoveryService = FlextPluginDiscoveryService


__all__ = [
    # Main API facade
    "FlextPlugin",
    # Core platform and services
    "FlextPluginPlatform",
    "FlextPluginService",
    "FlextPluginDiscoveryService",
    # Core entities
    "FlextPluginEntity",
    "FlextPluginMetadata",
    "FlextPluginRegistry",
    # Core models
    "FlextPluginModels",
    "PluginStatus",
    "PluginType",
    # Discovery and loading
    "PluginDiscovery",
    "PluginLoader",
    # Hot reload
    "HotReloadManager",
    # Event handlers
    "FlextPluginEventHandler",
    "FlextPluginHandler",
    # Adapters
    "RealPluginDiscoveryAdapter",
    "RealPluginLoaderAdapter",
    "RealPluginManagerAdapter",
    # Configuration and constants
    "FlextPluginConfig",
    "FlextPluginConstants",
    # Exceptions
    "FlextPluginError",
    "FlextPluginExceptions",
    "PluginError",
    # Simple API
    "FlextPluginSimpleApi",
    # Legacy aliases
    "Plugin",
    "PluginMetadata",
    "PluginRegistry",
    "PluginConfig",
    "PluginConfiguration",
    "PluginInstance",
    "FlextPluginExecution",
    "PluginExecutionContextModel",
    "PluginExecutionResultModel",
    "PluginManagerResultModel",
    "FlextPluginLoaderPort",
    # Factory functions
    "create_flext_plugin",
    "create_flext_plugin_config",
    "create_flext_plugin_metadata",
    "create_flext_plugin_registry",
    "create_plugin_from_dict",
    "create_plugin_config_from_dict",
    "create_registry",
    # Version info
    "__version__",
    "__version_info__",
    "FlextPluginLoaderPort",
]
