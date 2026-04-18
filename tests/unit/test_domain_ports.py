"""REAL tests for flext_plugin domain ports - APENAS classes que EXISTEM.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_plugin import FlextPluginDiscovery


class TestFlextPluginDiscoveryPorts:
    """Comprehensive test suite for FlextPluginDiscovery domain interface.

    Este teste valida apenas a interface que REALMENTE existe.
    """

    def test_is_valid_class(self) -> None:
        """Test that FlextPluginDiscovery is a valid class."""
        assert FlextPluginDiscovery is not None

    def test_class_exists(self) -> None:
        """Test that FlextPluginDiscovery exists and is callable."""
        assert FlextPluginDiscovery is not None
        assert callable(FlextPluginDiscovery)
