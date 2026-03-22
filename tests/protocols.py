"""Test protocol definitions for flext-plugin.

Provides FlextPluginTestProtocols, combining FlextTestsProtocols with
FlextPluginProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from flext_plugin import FlextPluginProtocols


class FlextPluginTestProtocols(FlextTestsProtocols, FlextPluginProtocols):
    """Test protocols combining FlextTestsProtocols and FlextPluginProtocols."""

    class Plugin(FlextPluginProtocols.Plugin):
        """Plugin test protocols namespace."""

        class Tests:
            """Plugin-specific test protocols."""


p = FlextPluginTestProtocols
__all__ = ["FlextPluginTestProtocols", "p"]
