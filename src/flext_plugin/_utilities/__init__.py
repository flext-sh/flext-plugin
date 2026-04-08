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
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
