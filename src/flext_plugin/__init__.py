"""FLEXT Plugin System - Enterprise-grade plugin management for FLEXT ecosystem."""

from __future__ import annotations

# Core types and models
from .flext_plugin_models import PluginStatus, PluginType
from .entities import (
    FlextPluginEntity,
    FlextPluginConfig,
    FlextPluginMetadata,
    FlextPluginRegistry,
)

# Services and handlers
from .flext_plugin_services import FlextPluginService, FlextPluginDiscoveryService
from .flext_plugin_handlers import FlextPluginHandler, FlextPluginEventHandler

# Platform and core components
from .flext_plugin_platform import FlextPluginPlatform
from .discovery import PluginDiscovery
from .loader import PluginLoader

# Simple API and utilities
from .simple_api import (
    create_flext_plugin,
    create_flext_plugin_config,
    create_flext_plugin_metadata,
    create_flext_plugin_registry,
)
from .simple_plugin import Plugin, PluginRegistry

# Hot reload functionality
from .hot_reload import HotReloadManager, PluginFileHandler

# Ports/interfaces
from .ports import (
    FlextPluginDiscoveryPort,
    FlextPluginLoaderPort,
    FlextPluginManagerPort,
    FlextPluginRegistryPort,
    FlextPluginHotReloadPort,
)

# Legacy compatibility - Import from CONSOLIDATED FlextPluginModels
from .flext_plugin_models import (
    PluginExecutionContextModel,
    PluginExecutionResultModel,
    PluginManagerResultModel,
)

# Legacy aliases for backward compatibility
PluginExecutionContext = PluginExecutionContextModel
PluginExecutionResult = PluginExecutionResultModel
PluginManagerResult = PluginManagerResultModel

# Legacy registry - imported from CONSOLIDATED FlextPluginServices
from .flext_plugin_services import SimplePluginRegistry, create_plugin_manager

__all__ = [
    # Core types
    "PluginStatus",
    "PluginType",
    # Domain entities
    "FlextPluginEntity",
    "FlextPluginConfig",
    "FlextPluginMetadata",
    "FlextPluginRegistry",
    # Services
    "FlextPluginService",
    "FlextPluginDiscoveryService",
    # Handlers
    "FlextPluginHandler",
    "FlextPluginEventHandler",
    # Platform
    "FlextPluginPlatform",
    "PluginDiscovery",
    "PluginLoader",
    # Simple API
    "create_flext_plugin",
    "create_flext_plugin_config",
    "create_flext_plugin_metadata",
    "create_flext_plugin_registry",
    "Plugin",
    "PluginRegistry",
    # Hot reload
    "HotReloadManager",
    "PluginFileHandler",
    # Ports
    "FlextPluginDiscoveryPort",
    "FlextPluginLoaderPort",
    "FlextPluginManagerPort",
    "FlextPluginRegistryPort",
    "FlextPluginHotReloadPort",
    # Legacy
    "PluginExecutionContext",
    "PluginExecutionResult",
    "PluginManagerResult",
    "SimplePluginRegistry",
    "create_plugin_manager",
]
