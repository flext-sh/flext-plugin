# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Plugin Utilities - Domain-specific utilities for plugin management.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import u, u as flext_cli_u

from flext_plugin._utilities import (
    FlextPluginDiscovery,
    FlextPluginImplementations,
    FlextPluginPlatform,
    FlextPluginUtilitiesBase,
    FlextPluginUtilitiesMetadata,
)


class FlextPluginUtilities(flext_cli_u):
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
