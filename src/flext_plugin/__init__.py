"""FLEXT Plugin System - Enterprise-grade plugin management for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Final

from flext_plugin.api import FlextPlugin
from flext_plugin.version import VERSION, FlextPluginVersion
from flext_plugin.config import FlextPluginConfig
from flext_plugin.constants import FlextPluginConstants
from flext_plugin.entities import (
    FlextPluginEntity,
    FlextPluginMetadata,
    FlextPluginRegistry,
    Plugin,
    PluginMetadata,
    PluginRegistry,
)
from flext_plugin.exceptions import FlextPluginError, FlextPluginExceptions
from flext_plugin.flext_plugin_platform import FlextPluginPlatform
from flext_plugin.flext_plugin_services import FlextPluginService, FlextPluginDiscoveryService
from flext_plugin.models import PluginStatus, PluginType, FlextPluginModels
from flext_plugin.simple_api import FlextPluginSimpleApi

PROJECT_VERSION: Final[FlextPluginVersion] = VERSION

__version__: str = VERSION.version
__version_info__: tuple[int | str, ...] = VERSION.version_info

# Legacy aliases for backward compatibility
PluginConfig = FlextPluginConfig
PluginConfiguration = FlextPluginConfig
PluginInstance = FlextPluginEntity

# Backward compatibility for simple API functions
create_flext_plugin = FlextPluginSimpleApi.create_flext_plugin
create_flext_plugin_config = FlextPluginSimpleApi.create_flext_plugin_config
create_flext_plugin_metadata = FlextPluginSimpleApi.create_flext_plugin_metadata
create_flext_plugin_registry = FlextPluginSimpleApi.create_flext_plugin_registry
create_plugin_from_dict = FlextPluginSimpleApi.create_plugin_from_dict
create_plugin_config_from_dict = FlextPluginSimpleApi.create_plugin_config_from_dict

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

    # Configuration and constants
    "FlextPluginConfig",
    "FlextPluginConstants",

    # Exceptions
    "FlextPluginError",
    "FlextPluginExceptions",

    # Legacy aliases
    "Plugin",
    "PluginMetadata",
    "PluginRegistry",
    "PluginConfig",
    "PluginConfiguration",
    "PluginInstance",

    # Backward compatibility for simple API
    "create_flext_plugin",
    "create_flext_plugin_config",
    "create_flext_plugin_metadata",
    "create_flext_plugin_registry",
    "create_plugin_from_dict",
    "create_plugin_config_from_dict",

    # Version info
    "__version__",
    "__version_info__",
]
