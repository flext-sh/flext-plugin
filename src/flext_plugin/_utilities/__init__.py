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
    from flext_plugin._utilities.adapters import *
    from flext_plugin._utilities.discovery import *
    from flext_plugin._utilities.entities import *
    from flext_plugin._utilities.handlers import *
    from flext_plugin._utilities.hot_reload import *
    from flext_plugin._utilities.implementations import *
    from flext_plugin._utilities.loader import *
    from flext_plugin._utilities.plugin_platform import *
    from flext_plugin._utilities.services import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextPluginAdapters": "flext_plugin._utilities.adapters",
    "FlextPluginDiscovery": "flext_plugin._utilities.discovery",
    "FlextPluginEntities": "flext_plugin._utilities.entities",
    "FlextPluginHandlers": "flext_plugin._utilities.handlers",
    "FlextPluginHotReload": "flext_plugin._utilities.hot_reload",
    "FlextPluginImplementations": "flext_plugin._utilities.implementations",
    "FlextPluginLoader": "flext_plugin._utilities.loader",
    "FlextPluginPlatform": "flext_plugin._utilities.plugin_platform",
    "FlextPluginService": "flext_plugin._utilities.services",
    "adapters": "flext_plugin._utilities.adapters",
    "discovery": "flext_plugin._utilities.discovery",
    "entities": "flext_plugin._utilities.entities",
    "handlers": "flext_plugin._utilities.handlers",
    "hot_reload": "flext_plugin._utilities.hot_reload",
    "implementations": "flext_plugin._utilities.implementations",
    "loader": "flext_plugin._utilities.loader",
    "plugin_platform": "flext_plugin._utilities.plugin_platform",
    "services": "flext_plugin._utilities.services",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
