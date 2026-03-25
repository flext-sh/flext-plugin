"""Test type definitions for flext-plugin.

Provides FlextPluginTestTypes, combining FlextTestsTypes with
FlextPluginTypes for test-specific type definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsTypes

from flext_plugin import FlextPluginTypes


class FlextPluginTestTypes(FlextTestsTypes, FlextPluginTypes):
    """Test types combining FlextTestsTypes with flext-plugin types."""

    class Plugin(FlextPluginTypes.Plugin):
        """Plugin test namespace."""

        class Tests:
            """Internal tests declarations."""


t = FlextPluginTestTypes
__all__ = ["FlextPluginTestTypes", "t"]
