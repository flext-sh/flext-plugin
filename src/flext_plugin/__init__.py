# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""FLEXT Plugin System - plugin management for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

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
    from flext_plugin.adapters import FlextPluginAdapters
    from flext_plugin.api import FlextPluginApi
    from flext_plugin.constants import FlextPluginConstants, c
    from flext_plugin.discovery import FlextPluginDiscovery
    from flext_plugin.entities import FlextPluginEntities
    from flext_plugin.handlers import FlextPluginHandlers, FlextPluginHandlers as h
    from flext_plugin.hot_reload import FlextPluginHotReload
    from flext_plugin.implementations import FlextPluginImplementations
    from flext_plugin.loader import FlextPluginLoader
    from flext_plugin.models import FlextPluginModels, m
    from flext_plugin.platform import (
        FlextPluginPlatform,
        Plugin,
        PluginExecution,
        PluginRegistry,
    )
    from flext_plugin.protocols import FlextPluginProtocols, p
    from flext_plugin.services import FlextPluginService, FlextPluginService as s
    from flext_plugin.settings import FlextPluginSettings
    from flext_plugin.typings import FlextPluginTypes, t
    from flext_plugin.utilities import FlextPluginUtilities, u

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FlextPluginAdapters": ("flext_plugin.adapters", "FlextPluginAdapters"),
    "FlextPluginApi": ("flext_plugin.api", "FlextPluginApi"),
    "FlextPluginConstants": ("flext_plugin.constants", "FlextPluginConstants"),
    "FlextPluginDiscovery": ("flext_plugin.discovery", "FlextPluginDiscovery"),
    "FlextPluginEntities": ("flext_plugin.entities", "FlextPluginEntities"),
    "FlextPluginHandlers": ("flext_plugin.handlers", "FlextPluginHandlers"),
    "FlextPluginHotReload": ("flext_plugin.hot_reload", "FlextPluginHotReload"),
    "FlextPluginImplementations": (
        "flext_plugin.implementations",
        "FlextPluginImplementations",
    ),
    "FlextPluginLoader": ("flext_plugin.loader", "FlextPluginLoader"),
    "FlextPluginModels": ("flext_plugin.models", "FlextPluginModels"),
    "FlextPluginPlatform": ("flext_plugin.platform", "FlextPluginPlatform"),
    "FlextPluginProtocols": ("flext_plugin.protocols", "FlextPluginProtocols"),
    "FlextPluginService": ("flext_plugin.services", "FlextPluginService"),
    "FlextPluginSettings": ("flext_plugin.settings", "FlextPluginSettings"),
    "FlextPluginTypes": ("flext_plugin.typings", "FlextPluginTypes"),
    "FlextPluginUtilities": ("flext_plugin.utilities", "FlextPluginUtilities"),
    "Plugin": ("flext_plugin.platform", "Plugin"),
    "PluginExecution": ("flext_plugin.platform", "PluginExecution"),
    "PluginRegistry": ("flext_plugin.platform", "PluginRegistry"),
    "__all__": ("flext_plugin.__version__", "__all__"),
    "__author__": ("flext_plugin.__version__", "__author__"),
    "__author_email__": ("flext_plugin.__version__", "__author_email__"),
    "__description__": ("flext_plugin.__version__", "__description__"),
    "__license__": ("flext_plugin.__version__", "__license__"),
    "__title__": ("flext_plugin.__version__", "__title__"),
    "__url__": ("flext_plugin.__version__", "__url__"),
    "__version__": ("flext_plugin.__version__", "__version__"),
    "__version_info__": ("flext_plugin.__version__", "__version_info__"),
    "c": ("flext_plugin.constants", "c"),
    "h": ("flext_plugin.handlers", "FlextPluginHandlers"),
    "m": ("flext_plugin.models", "m"),
    "p": ("flext_plugin.protocols", "p"),
    "s": ("flext_plugin.services", "FlextPluginService"),
    "t": ("flext_plugin.typings", "t"),
    "u": ("flext_plugin.utilities", "u"),
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
    "Plugin",
    "PluginExecution",
    "PluginRegistry",
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
    "h",
    "m",
    "p",
    "s",
    "t",
    "u",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
