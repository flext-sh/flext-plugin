"""FLEXT Plugin Core Module - Core plugin types and utilities.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Core types and utilities for the plugin system.
"""

from __future__ import annotations

from flext_plugin.core.types import (
    PluginError,
    PluginExecutionResult,
    PluginStatus,
    PluginType,
)

__all__: list[str] = [
    "PluginError",
    "PluginExecutionResult",
    "PluginStatus",
    "PluginType",
]
