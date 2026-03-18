"""Test protocol definitions for flext-plugin.

Provides TestsFlextPluginProtocols, combining p with
FlextPluginProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import p

from flext_plugin import FlextPluginProtocols


class TestsFlextPluginProtocols(p, FlextPluginProtocols):
    """Test protocols combining p and FlextPluginProtocols.

    Provides access to:
    - p.Tests.Docker.* (from p)
    - p.Tests.Factory.* (from p)
    - p.Plugin.* (from FlextPluginProtocols)
    """


p: type[TestsFlextPluginProtocols] = TestsFlextPluginProtocols
__all__ = ["TestsFlextPluginProtocols", "p"]

p = TestsFlextPluginProtocols
