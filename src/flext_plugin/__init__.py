"""FLEXT Plugin System - Enterprise-grade plugin management for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Version
from flext_plugin.__version__ import __version__, __version_info__

# Layer 3: Infrastructure
from flext_plugin.adapters import FlextPluginAdapters

# Layer 4: Facade & Configuration
from flext_plugin.api import FlextPluginApi
from flext_plugin.config import FlextPluginConfig

# Layer 0: Constants & Types
from flext_plugin.constants import FlextPluginConstants

# Layer 2: Application Services
from flext_plugin.discovery import FlextPluginDiscovery
from flext_plugin.handlers import FlextPluginHandlers
from flext_plugin.hot_reload import FlextPluginHotReload
from flext_plugin.loader import FlextPluginLoader

# Layer 1: Domain Models
from flext_plugin.models import FlextPluginModels
from flext_plugin.platform import FlextPluginPlatform
from flext_plugin.protocols import FlextPluginProtocols
from flext_plugin.services import FlextPluginService
from flext_plugin.types import FlextPluginTypes
from flext_plugin.utilities import FlextPluginUtilities

__all__ = [
    # Layer 3
    "FlextPluginAdapters",
    # Layer 4
    "FlextPluginApi",
    "FlextPluginConfig",
    # Layer 0
    "FlextPluginConstants",
    # Layer 2
    "FlextPluginDiscovery",
    "FlextPluginHandlers",
    "FlextPluginHotReload",
    "FlextPluginLoader",
    # Layer 1
    "FlextPluginModels",
    "FlextPluginPlatform",
    "FlextPluginProtocols",
    "FlextPluginService",
    "FlextPluginTypes",
    "FlextPluginUtilities",
    # Version
    "__version__",
    "__version_info__",
]
