"""Test models for flext-plugin.

Provides TestsFlextPluginModels, combining TestsFlextModels with
FlextPluginModels for test-specific model definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsModels

from flext_plugin import FlextPluginModels


class TestsFlextPluginModels(FlextTestsModels, FlextPluginModels):
    """Test models combining TestsFlextModels with flext-plugin models."""

    class Plugin(FlextPluginModels.Plugin):
        """Plugin test namespace."""

        class Tests:
            """Internal tests declarations."""


m = TestsFlextPluginModels

__all__: list[str] = ["TestsFlextPluginModels", "m"]
