# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Plugin Utilities - Internal subpackage.

Re-exports all utility namespace classes for MRO composition.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_plugin._utilities import (
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
    from flext_plugin._utilities.adapters import FlextPluginAdapters
    from flext_plugin._utilities.discovery import FlextPluginDiscovery
    from flext_plugin._utilities.entities import FlextPluginEntities
    from flext_plugin._utilities.handlers import FlextPluginHandlers
    from flext_plugin._utilities.hot_reload import FlextPluginHotReload
    from flext_plugin._utilities.implementations import FlextPluginImplementations
    from flext_plugin._utilities.loader import FlextPluginLoader
    from flext_plugin._utilities.plugin_platform import FlextPluginPlatform
    from flext_plugin._utilities.services import FlextPluginService

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextPluginAdapters": "flext_plugin._utilities.adapters",
    "FlextPluginDiscovery": "flext_plugin._utilities.discovery",
    "FlextPluginEntities": "flext_plugin._utilities.entities",
    "FlextPluginHandlers": "flext_plugin._utilities.handlers",
    "FlextPluginHotReload": "flext_plugin._utilities.hot_reload",
    "FlextPluginImplementations": "flext_plugin._utilities.implementations",
    "FlextPluginLoader": "flext_plugin._utilities.loader",
    "FlextPluginPlatform": "flext_plugin._utilities.plugin_platform",
    "FlextPluginService": "flext_plugin._utilities.services",
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
