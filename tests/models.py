"""Test models for flext-plugin.

Provides FlextPluginTestModels, combining FlextTestsModels with
FlextPluginModels for test-specific model definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsModels

from flext_plugin import FlextPluginModels


class FlextPluginTestModels(FlextTestsModels, FlextPluginModels):
    """Test models combining FlextTestsModels with flext-plugin models."""

    class Plugin(FlextPluginModels.Plugin):
        """Plugin test namespace."""

        class Tests:
            """Internal tests declarations."""


m = FlextPluginTestModels

__all__ = ["FlextPluginTestModels", "m"]
