"""FLEXT Plugin System - plugin management for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import (
    FlextDecorators,
    FlextExceptions,
    FlextHandlers,
    FlextMixins,
    FlextResult,
    FlextService,
)

from flext_plugin.__version__ import __version__, __version_info__
from flext_plugin.api import FlextPluginApi
from flext_plugin.constants import FlextPluginConstants
from flext_plugin.discovery import FlextPluginDiscovery
from flext_plugin.handlers import FlextPluginHandlers
from flext_plugin.hot_reload import FlextPluginHotReload
from flext_plugin.loader import FlextPluginLoader
from flext_plugin.models import FlextPluginModels
from flext_plugin.protocols import FlextPluginProtocols
from flext_plugin.services import FlextPluginService
from flext_plugin.typings import FlextPluginTypes
from flext_plugin.utilities import FlextPluginUtilities

# Standard aliases (11 required)
c = FlextPluginConstants
d = FlextDecorators
e = FlextExceptions
h = FlextHandlers
m = FlextPluginModels
p = FlextPluginProtocols
r = FlextResult
s = FlextService
t = FlextPluginTypes
u = FlextPluginUtilities
x = FlextMixins

__all__ = [
    "FlextPluginApi",
    "FlextPluginConstants",
    "FlextPluginDiscovery",
    "FlextPluginHandlers",
    "FlextPluginHotReload",
    "FlextPluginLoader",
    "FlextPluginModels",
    "FlextPluginProtocols",
    "FlextPluginService",
    "FlextPluginTypes",
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
