# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
