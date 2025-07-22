"""FLEXT Plugin - Enterprise Plugin System with simplified imports.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Version 0.7.0 - Hot Reload Plugin System with simplified public API:
- All common imports available from root: from flext_plugin import PluginManager
- Built on flext-core foundation for robust plugin architecture
- Deprecation warnings for internal imports
"""

from __future__ import annotations

import importlib.metadata
import warnings

# Import from flext-core - NO FALLBACKS OR DUPLICATES
from flext_core import (
    BaseConfig as PluginBaseConfig,  # Configuration base
    DomainBaseModel as BaseModel,  # Base for plugin models
    DomainError as PluginError,  # Plugin-specific errors
    ServiceResult,  # Plugin operation results
    ValidationError,  # Validation errors
)

# Core plugin exports - ACTUAL IMPLEMENTATIONS ONLY
from flext_plugin.core.base import Plugin
from flext_plugin.core.discovery import PluginDiscovery
from flext_plugin.core.loader import PluginLoader
from flext_plugin.core.manager import PluginManager
from flext_plugin.core.types import (
    PluginCapability,
    PluginExecutionResult,
    PluginLifecycle,
    PluginStatus,
    PluginType,
)

# Domain layer exports
from flext_plugin.domain.entities import PluginMetadata

try:
    __version__ = importlib.metadata.version("flext-plugin")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.7.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())


class FlextPluginDeprecationWarning(DeprecationWarning):
    """Custom deprecation warning for FLEXT Plugin import changes."""


def _show_deprecation_warning(old_import: str, new_import: str) -> None:
    """Show deprecation warning for import paths."""
    message_parts = [
        f"⚠️  DEPRECATED IMPORT: {old_import}",
        f"✅ USE INSTEAD: {new_import}",
        "🔗 This will be removed in version 1.0.0",
        "📖 See FLEXT Plugin docs for migration guide",
    ]
    warnings.warn(
        "\n".join(message_parts),
        FlextPluginDeprecationWarning,
        stacklevel=3,
    )

# ================================
# PUBLIC API EXPORTS
# ================================


__all__ = [
    "BaseModel",           # from flext_plugin import BaseModel
    # Deprecation utilities
    "FlextPluginDeprecationWarning",
    # Core Patterns (from flext-core)
    "Plugin",             # from flext_plugin import Plugin
    "PluginBaseConfig",   # from flext_plugin import PluginBaseConfig
    # Plugin System (simplified access)
    "PluginCapability",   # from flext_plugin import PluginCapability
    "PluginDiscovery",    # from flext_plugin import PluginDiscovery
    "PluginError",        # from flext_plugin import PluginError
    "PluginExecutionResult",  # from flext_plugin import PluginExecutionResult
    "PluginLifecycle",    # from flext_plugin import PluginLifecycle
    "PluginLoader",       # from flext_plugin import PluginLoader
    "PluginManager",      # from flext_plugin import PluginManager
    "PluginMetadata",     # from flext_plugin import PluginMetadata
    "PluginStatus",       # from flext_plugin import PluginStatus
    "PluginType",         # from flext_plugin import PluginType
    "ServiceResult",      # from flext_plugin import ServiceResult
    "ValidationError",    # from flext_plugin import ValidationError
    # Version
    "__version__",
    "__version_info__",
]
