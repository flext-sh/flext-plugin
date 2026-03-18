"""Test models for flext-plugin.

Provides test-specific models extending m and FlextPluginModels
with proper hierarchy composition.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import m

from flext_plugin import FlextPluginModels


class TestsFlextPluginModels(m, FlextPluginModels):
    """Test models - composition of m + FlextPluginModels.

    Hierarchy:
    - m: Generic test utilities from flext-tests
    - FlextPluginModels: Domain models from flext-plugin
    - TestsFlextPluginModels: Composition + namespace .Tests

    Access patterns:
    - m.Tests.* - Project-specific test fixtures
    - m.Plugin.* - Production domain models (inherited)
    - m.Tests.* - Generic test utilities
    """


# Short aliases for tests
tm = TestsFlextPluginModels
m = TestsFlextPluginModels

__all__ = ["TestsFlextPluginModels", "m", "tm"]
