# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext plugin package."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

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

if TYPE_CHECKING:
    from flext_core import FlextTypes, d, e, h, r, s, x

    from flext_plugin import (
        _utilities,
        api,
        constants,
        models,
        protocols,
        settings,
        typings,
        utilities,
    )
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
    from flext_plugin.api import FlextPluginApi
    from flext_plugin.constants import FlextPluginConstants, FlextPluginConstants as c
    from flext_plugin.models import FlextPluginModels, FlextPluginModels as m
    from flext_plugin.protocols import FlextPluginProtocols, FlextPluginProtocols as p
    from flext_plugin.settings import FlextPluginSettings
    from flext_plugin.typings import FlextPluginTypes, FlextPluginTypes as t
    from flext_plugin.utilities import FlextPluginUtilities, FlextPluginUtilities as u

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


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
