# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Plugin Utilities - Internal subpackage.

Re-exports all utility namespace classes for MRO composition.
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
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

__all__ = [
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
