# AUTO-GENERATED FILE — Regenerate with: make gen
"""Utilities package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".adapters": ("FlextPluginAdapters",),
        ".discovery": ("FlextPluginDiscovery",),
        ".entities": ("FlextPluginEntities",),
        ".handlers": ("FlextPluginHandlers",),
        ".hot_reload": ("FlextPluginHotReload",),
        ".implementations": ("FlextPluginImplementations",),
        ".loader": ("FlextPluginLoader",),
        ".plugin_platform": ("FlextPluginPlatform",),
        ".services": ("FlextPluginService",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
