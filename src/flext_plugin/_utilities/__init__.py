# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_plugin import (
        adapters,
        discovery,
        entities,
        handlers,
        hot_reload,
        implementations,
        loader,
        plugin_platform,
        services,
    )
    from flext_plugin.adapters import FlextPluginAdapters
    from flext_plugin.discovery import FlextPluginDiscovery
    from flext_plugin.entities import FlextPluginEntities
    from flext_plugin.handlers import FlextPluginHandlers
    from flext_plugin.hot_reload import FlextPluginHotReload
    from flext_plugin.implementations import FlextPluginImplementations
    from flext_plugin.loader import FlextPluginLoader
    from flext_plugin.plugin_platform import FlextPluginPlatform
    from flext_plugin.services import FlextPluginService

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextPluginAdapters": "flext_plugin.adapters",
    "FlextPluginDiscovery": "flext_plugin.discovery",
    "FlextPluginEntities": "flext_plugin.entities",
    "FlextPluginHandlers": "flext_plugin.handlers",
    "FlextPluginHotReload": "flext_plugin.hot_reload",
    "FlextPluginImplementations": "flext_plugin.implementations",
    "FlextPluginLoader": "flext_plugin.loader",
    "FlextPluginPlatform": "flext_plugin.plugin_platform",
    "FlextPluginService": "flext_plugin.services",
    "adapters": "flext_plugin.adapters",
    "discovery": "flext_plugin.discovery",
    "entities": "flext_plugin.entities",
    "handlers": "flext_plugin.handlers",
    "hot_reload": "flext_plugin.hot_reload",
    "implementations": "flext_plugin.implementations",
    "loader": "flext_plugin.loader",
    "plugin_platform": "flext_plugin.plugin_platform",
    "services": "flext_plugin.services",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
