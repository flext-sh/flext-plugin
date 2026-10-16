"""FLEXT Plugin Utilities - Domain-specific utilities for plugin management.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliUtilities

from flext_plugin._utilities.base import FlextPluginUtilitiesBase
from flext_plugin._utilities.discovery import FlextPluginDiscovery
from flext_plugin._utilities.implementations import FlextPluginImplementations
from flext_plugin._utilities.metadata import FlextPluginUtilitiesMetadata
from flext_plugin._utilities.plugin_platform import FlextPluginPlatform


class FlextPluginUtilities(FlextCliUtilities):
    """composition-based utilities using Python 3.13+ patterns."""

    class Plugin(
        FlextPluginUtilitiesMetadata,
        FlextPluginUtilitiesBase,
        FlextPluginDiscovery,
        FlextPluginImplementations,
        FlextPluginPlatform,
    ):
        """Plugin discovery and validation utilities."""


u = FlextPluginUtilities

__all__: list[str] = [
    "FlextPluginDiscovery",
    "FlextPluginPlatform",
    "FlextPluginUtilities",
    "u",
]
