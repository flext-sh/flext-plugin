"""Runtime settings for flext-plugin tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_plugin import FlextPluginSettings
from flext_tests import FlextTestsSettings


class TestsFlextPluginSettings(FlextPluginSettings, FlextTestsSettings):
    """Plugin settings extended with the shared test namespace."""


__all__: list[str] = ["TestsFlextPluginSettings"]
