"""FLEXT Plugin Constants - Plugin system constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from flext_core import FlextConstants


class FlextPluginConstants(FlextConstants):
    """Plugin system-specific constants following flext-core patterns."""

    # Plugin Discovery Configuration
    DEFAULT_PLUGIN_PATHS: ClassVar[list[str]] = [
        "/opt/flext/plugins",
        "~/.flext/plugins",
        "./plugins",
    ]

    # Plugin Types
    PLUGIN_TYPES: ClassVar[list[str]] = [
        "EXTENSION",
        "SERVICE",
        "MIDDLEWARE",
        "TAP",
        "TARGET",
    ]

    # Plugin Security Levels
    SECURITY_LEVELS: ClassVar[list[str]] = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

    # Hot Reload Configuration
    DEFAULT_RELOAD_INTERVAL = 2
    MAX_RELOAD_ATTEMPTS = 3


__all__ = ["FlextPluginConstants"]
