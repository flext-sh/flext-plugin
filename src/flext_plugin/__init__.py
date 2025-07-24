"""FLEXT Plugin - Simple Plugin System Library."""

from __future__ import annotations

# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container for flext-core imports
from flext_plugin.infrastructure.di_container import get_service_result
from flext_plugin.simple_plugin import (
    Plugin,
    PluginRegistry,
    create_registry,
    load_plugin,
)

ServiceResult = get_service_result()

__version__ = "1.0.0"

__all__ = [
    "Plugin",
    "PluginRegistry",
    "ServiceResult",
    "__version__",
    "create_registry",
    "load_plugin",
]
