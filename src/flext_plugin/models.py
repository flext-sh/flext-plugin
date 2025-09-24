"""Models for plugin operations.

This module provides data models for plugin operations.
"""

from flext_core import FlextModels


class FlextPluginModels:
    """Models for plugin system operations."""

    Core = FlextModels

    PluginMetadata = dict[str, object]
    PluginRegistry = dict[str, PluginMetadata]
