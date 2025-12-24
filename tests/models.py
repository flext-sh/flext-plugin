"""Test models for flext-plugin.

Provides test-specific models extending FlextTestsModels and FlextPluginModels
with proper hierarchy composition.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests.models import FlextTestsModels

from flext_plugin.models import FlextPluginModels


class TestsFlextPluginModels(FlextTestsModels, FlextPluginModels):
    """Test models - composition of FlextTestsModels + FlextPluginModels.

    Hierarchy:
    - FlextTestsModels: Generic test utilities from flext-tests
    - FlextPluginModels: Domain models from flext-plugin
    - TestsFlextPluginModels: Composition + namespace .Tests

    Access patterns:
    - m.Tests.* - Project-specific test fixtures
    - m.Plugin.* - Production domain models (inherited)
    - FlextTestsModels.Tests.* - Generic test utilities
    """

    class Tests:
        """Test fixtures namespace for flext-plugin.

        Contains test-specific models and fixtures that should not
        be part of production code.
        """


# Short aliases for tests
tm = TestsFlextPluginModels
m = TestsFlextPluginModels

__all__ = ["TestsFlextPluginModels", "m", "tm"]
