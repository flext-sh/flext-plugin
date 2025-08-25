"""Enterprise-grade plugin management system for FLEXT ecosystem."""

from __future__ import annotations

import uuid

from flext_core import FlextContainer, FlextResult

from flext_plugin.flext_plugin_services import FlextPluginDiscoveryService, FlextPluginService
from flext_plugin.flext_plugin_platform import FlextPluginPlatform
from flext_plugin.simple_api import (
    create_flext_plugin,
    create_flext_plugin_config,
    create_flext_plugin_metadata,
    create_flext_plugin_registry,
    create_plugin_from_dict,
    create_plugin_config_from_dict,
)
from flext_plugin.flext_plugin_models import PluginStatus, PluginType
from flext_plugin.typings_legacy import (
    PluginExecutionContext,
    PluginExecutionResult,
    PluginManagerResult,
    SimplePluginRegistry,
    create_plugin_manager,
)
from flext_plugin.entities import (
    FlextPluginEntity,
    FlextPluginConfig,
    FlextPluginMetadata,
    FlextPluginRegistry,
)
from flext_plugin.ports import (
    FlextPluginDiscoveryPort,
    FlextPluginHotReloadPort,
    FlextPluginLoaderPort,
    FlextPluginManagerPort,
    FlextPluginRegistryPort,
)
from flext_plugin.flext_plugin_handlers import (
    FlextPluginEventHandler,
    FlextPluginHandler,
)
from flext_plugin.discovery import PluginDiscovery
from flext_plugin.loader import PluginLoader
from flext_plugin.hot_reload import (
    HotReloadManager,
    PluginFileHandler,
    create_hot_reload_manager,
)
from flext_plugin.simple_plugin import (
    Plugin,
    PluginRegistry,
)

# Main platform facade - orchestration only
def create_flext_plugin_platform(config: dict[str, object] | None = None) -> FlextPluginPlatform:
    """Create a FlextPluginPlatform with dependency injection."""
    _ = config  # Reserved for future configuration options
    container = FlextContainer()
    return FlextPluginPlatform(container)


__all__ = [
    # Core types
    "PluginStatus",
    "PluginType",
    # Domain entities
    "FlextPluginConfig",
    "FlextPluginEntity",
    "FlextPluginMetadata",
    "FlextPluginRegistry",
    # Ports
    "FlextPluginDiscoveryPort",
    "FlextPluginHotReloadPort",
    "FlextPluginLoaderPort",
    "FlextPluginManagerPort",
    "FlextPluginRegistryPort",
    # Services
    "FlextPluginDiscoveryService",
    "FlextPluginService",
    # Handlers
    "FlextPluginEventHandler",
    "FlextPluginHandler",
    # Infrastructure
    "PluginDiscovery",
    "PluginLoader",
    "HotReloadManager",
    "PluginFileHandler",
    "create_hot_reload_manager",
    # Simple API
    "create_flext_plugin",
    "create_flext_plugin_config",
    "create_flext_plugin_metadata",
    "create_flext_plugin_registry",
    "create_plugin_from_dict",
    "create_plugin_config_from_dict",
    # Simple plugins
    "Plugin",
    "PluginRegistry",
    # Legacy compatibility
    "PluginExecutionContext",
    "PluginExecutionResult",
    "PluginManagerResult",
    "SimplePluginRegistry",
    "create_plugin_manager",
    # Platform
    "FlextPluginPlatform",
    "create_flext_plugin_platform",
    # Core utilities
    "FlextContainer",
    "FlextResult",
]
