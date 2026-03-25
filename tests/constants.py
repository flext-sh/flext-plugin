"""Test constants for flext-plugin tests.

Provides FlextPluginTestConstants, extending FlextTestsConstants with
flext-plugin-specific constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_plugins import FlextPluginsConstants
from flext_tests import FlextTestsConstants


class FlextPluginTestConstants(FlextTestsConstants, FlextPluginsConstants):
    """Test constants for flext-plugin."""

    class Plugin(FlextPluginsConstants.Plugin):
        """Plugin test namespace."""

        class Tests:
            """Internal tests declarations."""


c = FlextPluginTestConstants
__all__ = ["FlextPluginTestConstants", "c"]
