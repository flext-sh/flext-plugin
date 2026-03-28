# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext plugin package."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes, d, e, r, s, x

    from flext_plugin.__version__ import (
        __all__,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
    from flext_plugin._utilities.adapters import FlextPluginAdapters
    from flext_plugin._utilities.discovery import FlextPluginDiscovery
    from flext_plugin._utilities.entities import FlextPluginEntities
    from flext_plugin._utilities.handlers import (
        FlextPluginHandlers,
        FlextPluginHandlers as h,
    )
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
    "__all__": ["flext_plugin.__version__", "__all__"],
    "__author__": ["flext_plugin.__version__", "__author__"],
    "__author_email__": ["flext_plugin.__version__", "__author_email__"],
    "__description__": ["flext_plugin.__version__", "__description__"],
    "__license__": ["flext_plugin.__version__", "__license__"],
    "__title__": ["flext_plugin.__version__", "__title__"],
    "__url__": ["flext_plugin.__version__", "__url__"],
    "__version__": ["flext_plugin.__version__", "__version__"],
    "__version_info__": ["flext_plugin.__version__", "__version_info__"],
    "c": ["flext_plugin.constants", "FlextPluginConstants"],
    "d": ["flext_core", "d"],
    "e": ["flext_core", "e"],
    "h": ["flext_plugin._utilities.handlers", "FlextPluginHandlers"],
    "m": ["flext_plugin.models", "FlextPluginModels"],
    "p": ["flext_plugin.protocols", "FlextPluginProtocols"],
    "r": ["flext_core", "r"],
    "s": ["flext_core", "s"],
    "t": ["flext_plugin.typings", "FlextPluginTypes"],
    "u": ["flext_plugin.utilities", "FlextPluginUtilities"],
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
    "__all__",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
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
