# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext plugin package."""

from __future__ import annotations

import typing as _t

from flext_core.decorators import FlextDecorators as d
from flext_core.exceptions import FlextExceptions as e
from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_core.mixins import FlextMixins as x
from flext_core.result import FlextResult as r
from flext_core.service import FlextService as s
from flext_plugin.__version__ import *
from flext_plugin.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if _t.TYPE_CHECKING:
    import flext_plugin._utilities as _flext_plugin__utilities

    _utilities = _flext_plugin__utilities
    import flext_plugin._utilities.adapters as _flext_plugin__utilities_adapters

    adapters = _flext_plugin__utilities_adapters
    import flext_plugin._utilities.discovery as _flext_plugin__utilities_discovery

    discovery = _flext_plugin__utilities_discovery
    import flext_plugin._utilities.entities as _flext_plugin__utilities_entities

    entities = _flext_plugin__utilities_entities
    import flext_plugin._utilities.handlers as _flext_plugin__utilities_handlers

    handlers = _flext_plugin__utilities_handlers
    import flext_plugin._utilities.hot_reload as _flext_plugin__utilities_hot_reload

    hot_reload = _flext_plugin__utilities_hot_reload
    import flext_plugin._utilities.implementations as _flext_plugin__utilities_implementations

    implementations = _flext_plugin__utilities_implementations
    import flext_plugin._utilities.loader as _flext_plugin__utilities_loader

    loader = _flext_plugin__utilities_loader
    import flext_plugin._utilities.plugin_platform as _flext_plugin__utilities_plugin_platform

    plugin_platform = _flext_plugin__utilities_plugin_platform
    import flext_plugin._utilities.services as _flext_plugin__utilities_services

    services = _flext_plugin__utilities_services
    import flext_plugin.api as _flext_plugin_api

    api = _flext_plugin_api
    import flext_plugin.constants as _flext_plugin_constants

    constants = _flext_plugin_constants
    import flext_plugin.models as _flext_plugin_models

    models = _flext_plugin_models
    import flext_plugin.protocols as _flext_plugin_protocols

    protocols = _flext_plugin_protocols
    import flext_plugin.settings as _flext_plugin_settings

    settings = _flext_plugin_settings
    import flext_plugin.typings as _flext_plugin_typings

    typings = _flext_plugin_typings
    import flext_plugin.utilities as _flext_plugin_utilities

    utilities = _flext_plugin_utilities

    _ = (
        FlextPluginAdapters,
        FlextPluginApi,
        FlextPluginConstants,
        FlextPluginDiscovery,
        FlextPluginEntities,
        FlextPluginHandlers,
        FlextPluginHotReload,
        FlextPluginImplementations,
        FlextPluginLoader,
        FlextPluginModels,
        FlextPluginPlatform,
        FlextPluginProtocols,
        FlextPluginService,
        FlextPluginSettings,
        FlextPluginTypes,
        FlextPluginUtilities,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
        _utilities,
        adapters,
        api,
        c,
        constants,
        d,
        discovery,
        e,
        entities,
        h,
        handlers,
        hot_reload,
        implementations,
        loader,
        m,
        models,
        p,
        plugin_platform,
        protocols,
        r,
        s,
        services,
        settings,
        t,
        typings,
        u,
        utilities,
        x,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    ("flext_plugin._utilities",),
    {
        "FlextPluginApi": "flext_plugin.api",
        "FlextPluginConstants": "flext_plugin.constants",
        "FlextPluginModels": "flext_plugin.models",
        "FlextPluginProtocols": "flext_plugin.protocols",
        "FlextPluginSettings": "flext_plugin.settings",
        "FlextPluginTypes": "flext_plugin.typings",
        "FlextPluginUtilities": "flext_plugin.utilities",
        "__author__": "flext_plugin.__version__",
        "__author_email__": "flext_plugin.__version__",
        "__description__": "flext_plugin.__version__",
        "__license__": "flext_plugin.__version__",
        "__title__": "flext_plugin.__version__",
        "__url__": "flext_plugin.__version__",
        "__version__": "flext_plugin.__version__",
        "__version_info__": "flext_plugin.__version__",
        "_utilities": "flext_plugin._utilities",
        "api": "flext_plugin.api",
        "c": ("flext_plugin.constants", "FlextPluginConstants"),
        "constants": "flext_plugin.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "m": ("flext_plugin.models", "FlextPluginModels"),
        "models": "flext_plugin.models",
        "p": ("flext_plugin.protocols", "FlextPluginProtocols"),
        "protocols": "flext_plugin.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "settings": "flext_plugin.settings",
        "t": ("flext_plugin.typings", "FlextPluginTypes"),
        "typings": "flext_plugin.typings",
        "u": ("flext_plugin.utilities", "FlextPluginUtilities"),
        "utilities": "flext_plugin.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)

__all__ = [
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
