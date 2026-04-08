# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext plugin package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_plugin.__version__ import *

if _t.TYPE_CHECKING:
    import flext_plugin._utilities as _flext_plugin__utilities

    _utilities = _flext_plugin__utilities
    import flext_plugin.api as _flext_plugin_api
    from flext_plugin._utilities import (
        FlextPluginAdapters,
        FlextPluginDiscovery,
        FlextPluginEntities,
        FlextPluginHandlers,
        FlextPluginHandlers as h,
        FlextPluginHotReload,
        FlextPluginImplementations,
        FlextPluginLoader,
        FlextPluginPlatform,
        FlextPluginService,
    )

    api = _flext_plugin_api
    import flext_plugin.constants as _flext_plugin_constants
    from flext_plugin.api import FlextPluginApi

    constants = _flext_plugin_constants
    import flext_plugin.models as _flext_plugin_models
    from flext_plugin.constants import FlextPluginConstants, FlextPluginConstants as c

    models = _flext_plugin_models
    import flext_plugin.protocols as _flext_plugin_protocols
    from flext_plugin.models import FlextPluginModels, FlextPluginModels as m

    protocols = _flext_plugin_protocols
    import flext_plugin.settings as _flext_plugin_settings
    from flext_plugin.protocols import FlextPluginProtocols, FlextPluginProtocols as p

    settings = _flext_plugin_settings
    import flext_plugin.typings as _flext_plugin_typings
    from flext_plugin.settings import FlextPluginSettings

    typings = _flext_plugin_typings
    import flext_plugin.utilities as _flext_plugin_utilities
    from flext_plugin.typings import FlextPluginTypes, FlextPluginTypes as t

    utilities = _flext_plugin_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_plugin.utilities import FlextPluginUtilities, FlextPluginUtilities as u
_LAZY_IMPORTS = merge_lazy_imports(
    ("flext_plugin._utilities",),
    {
        "FlextPluginApi": ("flext_plugin.api", "FlextPluginApi"),
        "FlextPluginConstants": ("flext_plugin.constants", "FlextPluginConstants"),
        "FlextPluginModels": ("flext_plugin.models", "FlextPluginModels"),
        "FlextPluginProtocols": ("flext_plugin.protocols", "FlextPluginProtocols"),
        "FlextPluginSettings": ("flext_plugin.settings", "FlextPluginSettings"),
        "FlextPluginTypes": ("flext_plugin.typings", "FlextPluginTypes"),
        "FlextPluginUtilities": ("flext_plugin.utilities", "FlextPluginUtilities"),
        "__author__": ("flext_plugin.__version__", "__author__"),
        "__author_email__": ("flext_plugin.__version__", "__author_email__"),
        "__description__": ("flext_plugin.__version__", "__description__"),
        "__license__": ("flext_plugin.__version__", "__license__"),
        "__title__": ("flext_plugin.__version__", "__title__"),
        "__url__": ("flext_plugin.__version__", "__url__"),
        "__version__": ("flext_plugin.__version__", "__version__"),
        "__version_info__": ("flext_plugin.__version__", "__version_info__"),
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
_ = _LAZY_IMPORTS.pop("cleanup_submodule_namespace", None)
_ = _LAZY_IMPORTS.pop("install_lazy_exports", None)
_ = _LAZY_IMPORTS.pop("lazy_getattr", None)
_ = _LAZY_IMPORTS.pop("merge_lazy_imports", None)
_ = _LAZY_IMPORTS.pop("output", None)
_ = _LAZY_IMPORTS.pop("output_reporting", None)

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
    "api",
    "c",
    "constants",
    "d",
    "e",
    "h",
    "m",
    "models",
    "p",
    "protocols",
    "r",
    "s",
    "settings",
    "t",
    "typings",
    "u",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
