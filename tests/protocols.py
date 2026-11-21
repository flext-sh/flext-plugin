"""Test protocol definitions for flext-plugin.

Provides TestsFlextPluginProtocols, combining TestsFlextProtocols with
FlextPluginProtocols for test-specific protocol definitions.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from tests import FlextPluginProtocols


class TestsFlextPluginProtocols(FlextTestsProtocols, FlextPluginProtocols):
    """Test protocols combining TestsFlextProtocols and FlextPluginProtocols."""

    class Tests(FlextTestsProtocols.Tests):
        """Plugin-specific test protocols."""


p = TestsFlextPluginProtocols
__all__: list[str] = ["TestsFlextPluginProtocols", "p"]
