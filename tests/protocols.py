"""Test protocol definitions for flext-plugin.

Provides TestsFlextPluginProtocols, combining FlextTestsProtocols with
FlextPluginProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests.protocols import FlextTestsProtocols

from flext_plugin.protocols import FlextPluginProtocols


class TestsFlextPluginProtocols(FlextTestsProtocols, FlextPluginProtocols):
    """Test protocols combining FlextTestsProtocols and FlextPluginProtocols.

    Provides access to:
    - p.Tests.Docker.* (from FlextTestsProtocols)
    - p.Tests.Factory.* (from FlextTestsProtocols)
    - p.Plugin.* (from FlextPluginProtocols)
    """

    pass


# Runtime aliases
p = TestsFlextPluginProtocols
p = TestsFlextPluginProtocols

__all__ = ["TestsFlextPluginProtocols", "p"]
