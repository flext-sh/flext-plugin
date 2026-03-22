"""Test constants for flext-plugin tests.

Provides FlextPluginTestConstants, extending FlextTestsConstants with
flext-plugin-specific constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsConstants


class FlextPluginTestConstants(FlextTestsConstants):
    """Test constants for flext-plugin."""


c = FlextPluginTestConstants
__all__ = ["FlextPluginTestConstants", "c"]
