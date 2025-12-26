"""Test suite for flext_plugin manager components.

Tests the actual plugin service and manager functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_plugin import FlextPluginService


class TestFlextPluginService:
    """Tests for FlextPluginService class."""

    @pytest.fixture
    def service(self) -> FlextPluginService:
        """Create service instance for testing."""
        return FlextPluginService()

    def test_initialization(self, service: FlextPluginService) -> None:
        """Test service initialization."""
        assert service is not None
        assert hasattr(service, "logger")

    def test_class_exists(self) -> None:
        """Test that FlextPluginService class exists and is callable."""
        assert FlextPluginService is not None
        assert callable(FlextPluginService)
