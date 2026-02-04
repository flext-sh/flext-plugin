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
from flext_plugin.constants import FlextPluginConstants

# Layer 1: Domain Models
from flext_plugin.discovery import FlextPluginDiscovery
from flext_plugin.handlers import FlextPluginHandlers
from flext_plugin.hot_reload import FlextPluginHotReload
from flext_plugin.loader import FlextPluginLoader
from flext_plugin.models import FlextPluginModels
from flext_plugin.protocols import FlextPluginProtocols
from flext_plugin.services import FlextPluginService
from flext_plugin.typings import FlextPluginTypes

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
]
