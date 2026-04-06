# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_plugin._utilities.adapters as _flext_plugin__utilities_adapters

    adapters = _flext_plugin__utilities_adapters
    import flext_plugin._utilities.discovery as _flext_plugin__utilities_discovery
    from flext_plugin._utilities.adapters import FlextPluginAdapters

    discovery = _flext_plugin__utilities_discovery
    import flext_plugin._utilities.entities as _flext_plugin__utilities_entities
    from flext_plugin._utilities.discovery import FlextPluginDiscovery

    entities = _flext_plugin__utilities_entities
    import flext_plugin._utilities.handlers as _flext_plugin__utilities_handlers
    from flext_plugin._utilities.entities import FlextPluginEntities

    handlers = _flext_plugin__utilities_handlers
    import flext_plugin._utilities.hot_reload as _flext_plugin__utilities_hot_reload
    from flext_plugin._utilities.handlers import FlextPluginHandlers

    hot_reload = _flext_plugin__utilities_hot_reload
    import flext_plugin._utilities.implementations as _flext_plugin__utilities_implementations
    from flext_plugin._utilities.hot_reload import FlextPluginHotReload

    implementations = _flext_plugin__utilities_implementations
    import flext_plugin._utilities.loader as _flext_plugin__utilities_loader
    from flext_plugin._utilities.implementations import FlextPluginImplementations

    loader = _flext_plugin__utilities_loader
    import flext_plugin._utilities.plugin_platform as _flext_plugin__utilities_plugin_platform
    from flext_plugin._utilities.loader import FlextPluginLoader

    plugin_platform = _flext_plugin__utilities_plugin_platform
    import flext_plugin._utilities.services as _flext_plugin__utilities_services
    from flext_plugin._utilities.plugin_platform import FlextPluginPlatform

    services = _flext_plugin__utilities_services
    from flext_plugin._utilities.services import FlextPluginService
_LAZY_IMPORTS = {
    "FlextPluginAdapters": ("flext_plugin._utilities.adapters", "FlextPluginAdapters"),
    "FlextPluginDiscovery": (
        "flext_plugin._utilities.discovery",
        "FlextPluginDiscovery",
    ),
    "FlextPluginEntities": ("flext_plugin._utilities.entities", "FlextPluginEntities"),
    "FlextPluginHandlers": ("flext_plugin._utilities.handlers", "FlextPluginHandlers"),
    "FlextPluginHotReload": (
        "flext_plugin._utilities.hot_reload",
        "FlextPluginHotReload",
    ),
    "FlextPluginImplementations": (
        "flext_plugin._utilities.implementations",
        "FlextPluginImplementations",
    ),
    "FlextPluginLoader": ("flext_plugin._utilities.loader", "FlextPluginLoader"),
    "FlextPluginPlatform": (
        "flext_plugin._utilities.plugin_platform",
        "FlextPluginPlatform",
    ),
    "FlextPluginService": ("flext_plugin._utilities.services", "FlextPluginService"),
    "adapters": "flext_plugin._utilities.adapters",
    "discovery": "flext_plugin._utilities.discovery",
    "entities": "flext_plugin._utilities.entities",
    "handlers": "flext_plugin._utilities.handlers",
    "hot_reload": "flext_plugin._utilities.hot_reload",
    "implementations": "flext_plugin._utilities.implementations",
    "loader": "flext_plugin._utilities.loader",
    "plugin_platform": "flext_plugin._utilities.plugin_platform",
    "services": "flext_plugin._utilities.services",
}

__all__ = [
    "FlextPluginAdapters",
    "FlextPluginDiscovery",
    "FlextPluginEntities",
    "FlextPluginHandlers",
    "FlextPluginHotReload",
    "FlextPluginImplementations",
    "FlextPluginLoader",
    "FlextPluginPlatform",
    "FlextPluginService",
    "adapters",
    "discovery",
    "entities",
    "handlers",
    "hot_reload",
    "implementations",
    "loader",
    "plugin_platform",
    "services",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
