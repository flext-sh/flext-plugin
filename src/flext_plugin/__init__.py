"""FLEXT Plugin System - plugin management for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import (
        FlextDecorators as d,
        FlextExceptions as e,
        FlextHandlers as h,
        FlextMixins as x,
        FlextResult as r,
        FlextService as s,
    )

    from flext_plugin.__version__ import __version__, __version_info__
    from flext_plugin.adapters import FlextPluginAdapters
    from flext_plugin.api import FlextPluginApi
    from flext_plugin.constants import FlextPluginConstants, FlextPluginConstants as c
    from flext_plugin.discovery import FlextPluginDiscovery
    from flext_plugin.handlers import FlextPluginHandlers
    from flext_plugin.hot_reload import FlextPluginHotReload
    from flext_plugin.loader import FlextPluginLoader
    from flext_plugin.models import FlextPluginModels, FlextPluginModels as m
    from flext_plugin.platform import FlextPluginPlatform
    from flext_plugin.protocols import FlextPluginProtocols, FlextPluginProtocols as p
    from flext_plugin.services import FlextPluginService
    from flext_plugin.settings import FlextPluginSettings
    from flext_plugin.typings import FlextPluginTypes, FlextPluginTypes as t
    from flext_plugin.utilities import FlextPluginUtilities, FlextPluginUtilities as u
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FlextPluginAdapters": ("flext_plugin.adapters", "FlextPluginAdapters"),
    "FlextPluginApi": ("flext_plugin.api", "FlextPluginApi"),
    "FlextPluginConstants": ("flext_plugin.constants", "FlextPluginConstants"),
    "FlextPluginDiscovery": ("flext_plugin.discovery", "FlextPluginDiscovery"),
    "FlextPluginHandlers": ("flext_plugin.handlers", "FlextPluginHandlers"),
    "FlextPluginHotReload": ("flext_plugin.hot_reload", "FlextPluginHotReload"),
    "FlextPluginLoader": ("flext_plugin.loader", "FlextPluginLoader"),
    "FlextPluginModels": ("flext_plugin.models", "FlextPluginModels"),
    "FlextPluginPlatform": ("flext_plugin.platform", "FlextPluginPlatform"),
    "FlextPluginProtocols": ("flext_plugin.protocols", "FlextPluginProtocols"),
    "FlextPluginService": ("flext_plugin.services", "FlextPluginService"),
    "FlextPluginSettings": ("flext_plugin.settings", "FlextPluginSettings"),
    "FlextPluginTypes": ("flext_plugin.typings", "FlextPluginTypes"),
    "FlextPluginUtilities": ("flext_plugin.utilities", "FlextPluginUtilities"),
    "__version__": ("flext_plugin.__version__", "__version__"),
    "__version_info__": ("flext_plugin.__version__", "__version_info__"),
    "c": ("flext_plugin.constants", "FlextPluginConstants"),
    "d": ("flext_core", "FlextDecorators"),
    "e": ("flext_core", "FlextExceptions"),
    "h": ("flext_core", "FlextHandlers"),
    "m": ("flext_plugin.models", "FlextPluginModels"),
    "p": ("flext_plugin.protocols", "FlextPluginProtocols"),
    "r": ("flext_core", "FlextResult"),
    "s": ("flext_core", "FlextService"),
    "t": ("flext_plugin.typings", "FlextPluginTypes"),
    "u": ("flext_plugin.utilities", "FlextPluginUtilities"),
    "x": ("flext_core", "FlextMixins"),
}
__all__ = [
    "FlextPluginAdapters",
    "FlextPluginApi",
    "FlextPluginConstants",
    "FlextPluginDiscovery",
    "FlextPluginHandlers",
    "FlextPluginHotReload",
    "FlextPluginLoader",
    "FlextPluginModels",
    "FlextPluginPlatform",
    "FlextPluginProtocols",
    "FlextPluginService",
    "FlextPluginSettings",
    "FlextPluginTypes",
    "FlextPluginUtilities",
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


def __getattr__(name: str) -> Any:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
