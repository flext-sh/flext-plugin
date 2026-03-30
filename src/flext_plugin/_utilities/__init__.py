# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Plugin Utilities - Internal subpackage.

Re-exports all utility namespace classes for MRO composition.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_plugin._utilities import (
        adapters as adapters,
        discovery as discovery,
        entities as entities,
        handlers as handlers,
        hot_reload as hot_reload,
        implementations as implementations,
        loader as loader,
        plugin_platform as plugin_platform,
        services as services,
    )
    from flext_plugin._utilities.adapters import (
        FlextPluginAdapters as FlextPluginAdapters,
    )
    from flext_plugin._utilities.discovery import (
        FlextPluginDiscovery as FlextPluginDiscovery,
    )
    from flext_plugin._utilities.entities import (
        FlextPluginEntities as FlextPluginEntities,
    )
    from flext_plugin._utilities.handlers import (
        FlextPluginHandlers as FlextPluginHandlers,
    )
    from flext_plugin._utilities.hot_reload import (
        FlextPluginHotReload as FlextPluginHotReload,
    )
    from flext_plugin._utilities.implementations import (
        FlextPluginImplementations as FlextPluginImplementations,
    )
    from flext_plugin._utilities.loader import FlextPluginLoader as FlextPluginLoader
    from flext_plugin._utilities.plugin_platform import (
        FlextPluginPlatform as FlextPluginPlatform,
    )
    from flext_plugin._utilities.services import (
        FlextPluginService as FlextPluginService,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextPluginAdapters": ["flext_plugin._utilities.adapters", "FlextPluginAdapters"],
    "FlextPluginDiscovery": [
        "flext_plugin._utilities.discovery",
        "FlextPluginDiscovery",
    ],
    "FlextPluginEntities": ["flext_plugin._utilities.entities", "FlextPluginEntities"],
    "FlextPluginHandlers": ["flext_plugin._utilities.handlers", "FlextPluginHandlers"],
    "FlextPluginHotReload": [
        "flext_plugin._utilities.hot_reload",
        "FlextPluginHotReload",
    ],
    "FlextPluginImplementations": [
        "flext_plugin._utilities.implementations",
        "FlextPluginImplementations",
    ],
    "FlextPluginLoader": ["flext_plugin._utilities.loader", "FlextPluginLoader"],
    "FlextPluginPlatform": [
        "flext_plugin._utilities.plugin_platform",
        "FlextPluginPlatform",
    ],
    "FlextPluginService": ["flext_plugin._utilities.services", "FlextPluginService"],
    "adapters": ["flext_plugin._utilities.adapters", ""],
    "discovery": ["flext_plugin._utilities.discovery", ""],
    "entities": ["flext_plugin._utilities.entities", ""],
    "handlers": ["flext_plugin._utilities.handlers", ""],
    "hot_reload": ["flext_plugin._utilities.hot_reload", ""],
    "implementations": ["flext_plugin._utilities.implementations", ""],
    "loader": ["flext_plugin._utilities.loader", ""],
    "plugin_platform": ["flext_plugin._utilities.plugin_platform", ""],
    "services": ["flext_plugin._utilities.services", ""],
}

_EXPORTS: Sequence[str] = [
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
