"""Test type definitions for flext-plugin.

Provides TestsFlextPluginTypes, combining TestsFlextTypes with
FlextPluginTypes for test-specific type definitions.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsTypes

from tests import FlextPluginTypes


class TestsFlextPluginTypes(FlextTestsTypes, FlextPluginTypes):
    """Test types combining TestsFlextTypes with flext-plugin types."""

    class Tests(FlextTestsTypes.Tests):
        """Internal tests declarations."""


t = TestsFlextPluginTypes
__all__: list[str] = ["TestsFlextPluginTypes", "t"]
