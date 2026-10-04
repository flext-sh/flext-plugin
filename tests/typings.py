"""Test type definitions for flext-plugin.

Provides TestsFlextPluginTypes, combining TestsFlextTypes with
FlextPluginTypes for test-specific type definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_plugin import FlextPluginTypes
from flext_tests import FlextTestsTypes


class TestsFlextPluginTypes(FlextTestsTypes, FlextPluginTypes):
    """Test types combining TestsFlextTypes with flext-plugin types."""

    class Plugin(FlextPluginTypes.Plugin):
        """Plugin test namespace."""

        class Tests:
            """Internal tests declarations."""


t = TestsFlextPluginTypes
__all__: list[str] = ["TestsFlextPluginTypes", "t"]
