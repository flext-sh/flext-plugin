"""FLEXT Plugin System - Enterprise-grade plugin management for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

This module provides comprehensive plugin management capabilities including:
- Plugin discovery and loading
- Plugin execution and lifecycle management
- Hot reload and file monitoring
- Security validation and sandboxing
- Event handling and monitoring
- Clean Architecture and DDD patterns

Usage:
    ```python
    from flext_plugin import FlextPluginApi
    from flext_core import FlextContainer

    # Initialize plugin system
    container = FlextContainer()
    api = FlextPluginApi(container)

    # Discover and load plugins
    result = api.discover_plugins(["./plugins"])
    if result.success:
        plugins = result.value
        print(f"Discovered {len(plugins)} plugins")

    # Execute a plugin
    execution_result = api.execute_plugin("my-plugin", {"input": "data"})
    ```
"""

from __future__ import annotations

from typing import Final

from flext_plugin.__version__ import __version__, __version_info__
from flext_plugin.api import FlextPluginApi
from flext_plugin.config import FlextPluginConfig
from flext_plugin.constants import FlextPluginConstants
from flext_plugin.entities import FlextPluginEntities
from flext_plugin.handlers import FlextPluginHandlers
from flext_plugin.hot_reload import FlextPluginHotReload
from flext_plugin.loader import FlextPluginLoader
from flext_plugin.models import FlextPluginModels
from flext_plugin.platform import FlextPluginPlatform
from flext_plugin.protocols import FlextPluginProtocols
from flext_plugin.services import FlextPluginService
from flext_plugin.types import FlextPluginTypes
from flext_plugin.version import VERSION, FlextPluginVersion

# Version information
PROJECT_VERSION: Final[FlextPluginVersion] = VERSION

__version__: str = VERSION.version
__version_info__: tuple[int | str, ...] = VERSION.version_info

# Main API exports
__all__ = [
    "PROJECT_VERSION",
    # Version information
    "VERSION",
    # Core API
    "FlextPluginApi",
    "FlextPluginConfig",
    # Core classes following [Project][Module] pattern
    "FlextPluginConstants",
    "FlextPluginEntities",
    "FlextPluginHandlers",
    "FlextPluginHotReload",
    "FlextPluginLoader",
    "FlextPluginModels",
    "FlextPluginPlatform",
    "FlextPluginProtocols",
    "FlextPluginService",
    "FlextPluginTypes",
    "__version__",
    "__version_info__",
]
