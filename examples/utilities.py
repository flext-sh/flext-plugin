"""Utility functions for flextplugin.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Why: FlextPluginUtilities is owned by flext_plugin, not flext_core (pyrefly missing-module-attribute).
from flext_plugin import FlextPluginUtilities


class ExamplesFlextPluginUtilities(FlextPluginUtilities):
    """Utility functions for flextplugin."""


__all__: list[str] = ["ExamplesFlextPluginUtilities"]
