# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext plugin package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

from flext_plugin.__version__ import (
    __author__ as __author__,
    __author_email__ as __author_email__,
    __description__ as __description__,
    __license__ as __license__,
    __title__ as __title__,
    __url__ as __url__,
    __version__ as __version__,
    __version_info__ as __version_info__,
)

if TYPE_CHECKING:
    from flext_plugin import (
        _utilities as _utilities,
        api as api,
        constants as constants,
        models as models,
        protocols as protocols,
        settings as settings,
        typings as typings,
        utilities as utilities,
    )
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
    from flext_plugin.api import FlextPluginApi as FlextPluginApi
    from flext_plugin.constants import (
        FlextPluginConstants as FlextPluginConstants,
        FlextPluginConstants as c,
    )
    from flext_plugin.models import (
        FlextPluginModels as FlextPluginModels,
        FlextPluginModels as m,
    )
    from flext_plugin.protocols import (
        FlextPluginProtocols as FlextPluginProtocols,
        FlextPluginProtocols as p,
    )
    from flext_plugin.settings import FlextPluginSettings as FlextPluginSettings
    from flext_plugin.typings import (
        FlextPluginTypes as FlextPluginTypes,
        FlextPluginTypes as t,
    )
    from flext_plugin.utilities import (
        FlextPluginUtilities as FlextPluginUtilities,
        FlextPluginUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextPluginAdapters": ["flext_plugin._utilities.adapters", "FlextPluginAdapters"],
    "FlextPluginApi": ["flext_plugin.api", "FlextPluginApi"],
    "FlextPluginConstants": ["flext_plugin.constants", "FlextPluginConstants"],
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
    "FlextPluginModels": ["flext_plugin.models", "FlextPluginModels"],
    "FlextPluginPlatform": [
        "flext_plugin._utilities.plugin_platform",
        "FlextPluginPlatform",
    ],
    "FlextPluginProtocols": ["flext_plugin.protocols", "FlextPluginProtocols"],
    "FlextPluginService": ["flext_plugin._utilities.services", "FlextPluginService"],
    "FlextPluginSettings": ["flext_plugin.settings", "FlextPluginSettings"],
    "FlextPluginTypes": ["flext_plugin.typings", "FlextPluginTypes"],
    "FlextPluginUtilities": ["flext_plugin.utilities", "FlextPluginUtilities"],
    "_utilities": ["flext_plugin._utilities", ""],
    "adapters": ["flext_plugin._utilities.adapters", ""],
    "api": ["flext_plugin.api", ""],
    "c": ["flext_plugin.constants", "FlextPluginConstants"],
    "constants": ["flext_plugin.constants", ""],
    "d": ["flext_core", "d"],
    "discovery": ["flext_plugin._utilities.discovery", ""],
    "e": ["flext_core", "e"],
    "entities": ["flext_plugin._utilities.entities", ""],
    "h": ["flext_core", "h"],
    "handlers": ["flext_plugin._utilities.handlers", ""],
    "hot_reload": ["flext_plugin._utilities.hot_reload", ""],
    "implementations": ["flext_plugin._utilities.implementations", ""],
    "loader": ["flext_plugin._utilities.loader", ""],
    "m": ["flext_plugin.models", "FlextPluginModels"],
    "models": ["flext_plugin.models", ""],
    "p": ["flext_plugin.protocols", "FlextPluginProtocols"],
    "plugin_platform": ["flext_plugin._utilities.plugin_platform", ""],
    "protocols": ["flext_plugin.protocols", ""],
    "r": ["flext_core", "r"],
    "s": ["flext_core", "s"],
    "services": ["flext_plugin._utilities.services", ""],
    "settings": ["flext_plugin.settings", ""],
    "t": ["flext_plugin.typings", "FlextPluginTypes"],
    "typings": ["flext_plugin.typings", ""],
    "u": ["flext_plugin.utilities", "FlextPluginUtilities"],
    "utilities": ["flext_plugin.utilities", ""],
    "x": ["flext_core", "x"],
}

_EXPORTS: Sequence[str] = [
    "FlextPluginAdapters",
    "FlextPluginApi",
    "FlextPluginConstants",
    "FlextPluginDiscovery",
    "FlextPluginEntities",
    "FlextPluginHandlers",
    "FlextPluginHotReload",
    "FlextPluginImplementations",
    "FlextPluginLoader",
    "FlextPluginModels",
    "FlextPluginPlatform",
    "FlextPluginProtocols",
    "FlextPluginService",
    "FlextPluginSettings",
    "FlextPluginTypes",
    "FlextPluginUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "_utilities",
    "adapters",
    "api",
    "c",
    "constants",
    "d",
    "discovery",
    "e",
    "entities",
    "h",
    "handlers",
    "hot_reload",
    "implementations",
    "loader",
    "m",
    "models",
    "p",
    "plugin_platform",
    "protocols",
    "r",
    "s",
    "services",
    "settings",
    "t",
    "typings",
    "u",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
