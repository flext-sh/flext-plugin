"""Test utilities for flext-plugin.

Provides TestsFlextPluginUtilities, combining TestsFlextUtilities with
FlextPluginUtilities for test-specific utility definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsUtilities

from flext_plugin import FlextPluginUtilities


class TestsFlextPluginUtilities(FlextTestsUtilities, FlextPluginUtilities):
    """Test utilities combining TestsFlextUtilities with flext-plugin utilities."""

    class Plugin(FlextPluginUtilities.Plugin):
        """Plugin test utilities namespace."""

        class Tests:
            """Internal tests declarations."""


u = TestsFlextPluginUtilities
__all__: list[str] = ["TestsFlextPluginUtilities", "u"]
