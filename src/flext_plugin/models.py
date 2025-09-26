"""Module docstring."""

from __future__ import annotations

"""Models for plugin operations.

This module provides data models for plugin operations.
"""

from flext_core import FlextModels


class FlextPluginModels(FlextModels):
    """Models for plugin system operations.

    Extends FlextModels to avoid duplication and ensure consistency.
    All plugin system models benefit from FlextModels patterns.
    """

    PluginMetadata = dict["str", "object"]
    PluginRegistry = dict["str", "PluginMetadata"]
