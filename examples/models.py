"""Domain models for flextplugin.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Why: FlextPluginModels is owned by flext_plugin, not flext_core (pyrefly).
from flext_plugin import FlextPluginModels


class ExamplesFlextPluginModels(FlextPluginModels):
    """Domain models for flextplugin."""


__all__: list[str] = ["ExamplesFlextPluginModels"]
