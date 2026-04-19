"""Test constants for flext-plugin tests.

Provides TestsFlextPluginConstants, extending FlextTestsConstants with
flext-plugin-specific constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_plugin import FlextPluginConstants
from flext_tests import FlextTestsConstants


class TestsFlextPluginConstants(FlextTestsConstants, FlextPluginConstants):
    """Test constants for flext-plugin."""

    class Plugin(FlextPluginConstants.Plugin):
        """Plugin test namespace."""

        class Tests:
            """Internal tests declarations."""


c = TestsFlextPluginConstants
__all__: list[str] = ["TestsFlextPluginConstants", "c"]
