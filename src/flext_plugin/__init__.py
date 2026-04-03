# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext plugin package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports
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

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_plugin import (
        _utilities,
        adapters,
        api,
        constants,
        discovery,
        entities,
        handlers,
        hot_reload,
        implementations,
        loader,
        models,
        plugin_platform,
        protocols,
        services,
        settings,
        typings,
        utilities,
    )
    from flext_plugin._utilities import (
        FlextPluginAdapters,
        FlextPluginDiscovery,
        FlextPluginEntities,
        FlextPluginHandlers,
        FlextPluginHotReload,
        FlextPluginImplementations,
        FlextPluginLoader,
        FlextPluginPlatform,
        FlextPluginService,
    )
    from flext_plugin.api import FlextPluginApi
    from flext_plugin.constants import FlextPluginConstants, FlextPluginConstants as c
    from flext_plugin.models import FlextPluginModels, FlextPluginModels as m
    from flext_plugin.protocols import FlextPluginProtocols, FlextPluginProtocols as p
    from flext_plugin.settings import FlextPluginSettings
    from flext_plugin.typings import FlextPluginTypes, FlextPluginTypes as t
    from flext_plugin.utilities import FlextPluginUtilities, FlextPluginUtilities as u

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
    ("flext_plugin._utilities",),
    {
        "FlextPluginApi": "flext_plugin.api",
        "FlextPluginConstants": "flext_plugin.constants",
        "FlextPluginModels": "flext_plugin.models",
        "FlextPluginProtocols": "flext_plugin.protocols",
        "FlextPluginSettings": "flext_plugin.settings",
        "FlextPluginTypes": "flext_plugin.typings",
        "FlextPluginUtilities": "flext_plugin.utilities",
        "_utilities": "flext_plugin._utilities",
        "adapters": "flext_plugin.adapters",
        "api": "flext_plugin.api",
        "c": ("flext_plugin.constants", "FlextPluginConstants"),
        "constants": "flext_plugin.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "discovery": "flext_plugin.discovery",
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "entities": "flext_plugin.entities",
        "h": ("flext_core.handlers", "FlextHandlers"),
        "handlers": "flext_plugin.handlers",
        "hot_reload": "flext_plugin.hot_reload",
        "implementations": "flext_plugin.implementations",
        "loader": "flext_plugin.loader",
        "m": ("flext_plugin.models", "FlextPluginModels"),
        "models": "flext_plugin.models",
        "p": ("flext_plugin.protocols", "FlextPluginProtocols"),
        "plugin_platform": "flext_plugin.plugin_platform",
        "protocols": "flext_plugin.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "services": "flext_plugin.services",
        "settings": "flext_plugin.settings",
        "t": ("flext_plugin.typings", "FlextPluginTypes"),
        "typings": "flext_plugin.typings",
        "u": ("flext_plugin.utilities", "FlextPluginUtilities"),
        "utilities": "flext_plugin.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    [
        "__all__",
        "__author__",
        "__author_email__",
        "__description__",
        "__license__",
        "__title__",
        "__url__",
        "__version__",
        "__version_info__",
    ],
)
