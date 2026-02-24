"""FLEXT Plugin System - plugin management for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Version - acceptable exception for __init__.py (foundation module importing version)
from flext_plugin.__version__ import __version__, __version_info__

# Layer 3: Application Facade
from flext_plugin.api import FlextPluginApi

# Layer 0: Constants & Types (Foundation only - no services/api imports)
from flext_core.decorators import FlextDecorators
from flext_core.exceptions import FlextExceptions
from flext_core.handlers import FlextHandlers
from flext_core.mixins import FlextMixins
from flext_core.result import FlextResult
from flext_core.service import FlextService
from flext_plugin.constants import FlextPluginConstants
from flext_plugin.typings import FlextPluginTypes

# Layer 1: Domain Models
from flext_plugin.discovery import FlextPluginDiscovery
from flext_plugin.handlers import FlextPluginHandlers
from flext_plugin.hot_reload import FlextPluginHotReload
from flext_plugin.loader import FlextPluginLoader
from flext_plugin.models import FlextPluginModels
from flext_plugin.protocols import FlextPluginProtocols
from flext_plugin.services import FlextPluginService
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
