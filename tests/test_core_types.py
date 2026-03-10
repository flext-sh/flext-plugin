"""Comprehensive test suite for flext_plugin.core.types module.

This test module validates all core type definitions, enumerations, and foundational
classes that form the backbone of the FLEXT plugin system. Tests ensure type safety,
proper enum behavior, error handling, and integration patterns across all core types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_core import FlextExceptions

from flext_plugin import FlextPluginConstants


class TestFlextPluginConstantsPluginType:
    """Test FlextPluginConstants.Plugin.PluginType enum functionality."""

    def test_plugin_type_values(self) -> None:
        """Test all plugin type enum values."""
        if FlextPluginConstants.Plugin.PluginType.TAP.value != "tap":
            error_message = f"Expected {'tap'}, got {FlextPluginConstants.Plugin.PluginType.TAP.value}"
            raise AssertionError(error_message)
        assert FlextPluginConstants.Plugin.PluginType.TARGET.value == "target"
        if FlextPluginConstants.Plugin.PluginType.TRANSFORM.value != "transform":
            error_message = f"Expected {'transform'}, got {FlextPluginConstants.Plugin.PluginType.TRANSFORM.value}"
            raise AssertionError(error_message)
        assert FlextPluginConstants.Plugin.PluginType.UTILITY.value == "utility"

    def test_plugin_type_from_string(self) -> None:
        """Test creating FlextPluginConstants.Plugin.PluginType from string values."""
        if (
            FlextPluginConstants.Plugin.PluginType("tap")
            != FlextPluginConstants.Plugin.PluginType.TAP
        ):
            error_message = f"Expected {FlextPluginConstants.Plugin.PluginType.TAP}, got {FlextPluginConstants.Plugin.PluginType('tap')}"
            raise AssertionError(error_message)
        assert (
            FlextPluginConstants.Plugin.PluginType("target")
            == FlextPluginConstants.Plugin.PluginType.TARGET
        )
        if (
            FlextPluginConstants.Plugin.PluginType("transform")
            != FlextPluginConstants.Plugin.PluginType.TRANSFORM
        ):
            error_message = f"Expected {FlextPluginConstants.Plugin.PluginType.TRANSFORM}, got {FlextPluginConstants.Plugin.PluginType('transform')}"
            raise AssertionError(error_message)
        assert (
            FlextPluginConstants.Plugin.PluginType("utility")
            == FlextPluginConstants.Plugin.PluginType.UTILITY
        )

    def test_plugin_type_invalid(self) -> None:
        """Test invalid plugin type raises error."""
        with pytest.raises(ValueError, match=r".*invalid_type.*"):
            FlextPluginConstants.Plugin.PluginType("invalid_type")


class TestFlextPluginConstantsLifecycle:
    """Test FlextPluginConstants.Plugin.PluginStatus enum functionality."""

    def test_plugin_status_values(self) -> None:
        """Test all plugin status enum values."""
        if FlextPluginConstants.Plugin.PluginStatus.UNKNOWN.value != "unknown":
            msg = f"Expected {'unknown'}, got {FlextPluginConstants.Plugin.PluginStatus.UNKNOWN.value}"
            raise AssertionError(msg)
        assert FlextPluginConstants.Plugin.PluginStatus.DISCOVERED.value == "discovered"
        if FlextPluginConstants.Plugin.PluginStatus.LOADED.value != "loaded":
            msg = f"Expected {'loaded'}, got {FlextPluginConstants.Plugin.PluginStatus.LOADED.value}"
            raise AssertionError(msg)
        assert FlextPluginConstants.Plugin.PluginStatus.ACTIVE.value == "active"
        if FlextPluginConstants.Plugin.PluginStatus.ERROR.value != "error":
            msg = f"Expected {'error'}, got {FlextPluginConstants.Plugin.PluginStatus.ERROR.value}"
            raise AssertionError(msg)

    def test_plugin_status_from_string(self) -> None:
        """Test creating FlextPluginConstants.Plugin.PluginStatus from string values."""
        if (
            FlextPluginConstants.Plugin.PluginStatus("unknown")
            != FlextPluginConstants.Plugin.PluginStatus.UNKNOWN
        ):
            msg = f"Expected {FlextPluginConstants.Plugin.PluginStatus.UNKNOWN}, got {FlextPluginConstants.Plugin.PluginStatus('unknown')}"
            raise AssertionError(msg)
        assert (
            FlextPluginConstants.Plugin.PluginStatus("discovered")
            == FlextPluginConstants.Plugin.PluginStatus.DISCOVERED
        )
        if (
            FlextPluginConstants.Plugin.PluginStatus("loaded")
            != FlextPluginConstants.Plugin.PluginStatus.LOADED
        ):
            msg = f"Expected {FlextPluginConstants.Plugin.PluginStatus.LOADED}, got {FlextPluginConstants.Plugin.PluginStatus('loaded')}"
            raise AssertionError(msg)
        assert (
            FlextPluginConstants.Plugin.PluginStatus("active")
            == FlextPluginConstants.Plugin.PluginStatus.ACTIVE
        )
        if (
            FlextPluginConstants.Plugin.PluginStatus("error")
            != FlextPluginConstants.Plugin.PluginStatus.ERROR
        ):
            msg = f"Expected {FlextPluginConstants.Plugin.PluginStatus.ERROR}, got {FlextPluginConstants.Plugin.PluginStatus('error')}"
            raise AssertionError(msg)


class TestPluginError:
    """Test PluginError exception functionality."""

    def test_plugin_error_creation(self) -> None:
        """Test creating PluginError with message."""
        error = FlextExceptions.BaseError("Test error message")
        assert "Test error message" in str(error)
        assert isinstance(error, Exception)

    def test_plugin_error_with_plugin_id(self) -> None:
        """Test PluginError with plugin_id."""
        error = FlextExceptions.BaseError("Test error")
        assert "Test error" in str(error)
        assert isinstance(error, Exception)

    def test_plugin_error_with_error_code(self) -> None:
        """Test PluginError with error_code."""
        error = FlextExceptions.BaseError("Test error")
        assert "Test error" in str(error)
        assert isinstance(error, Exception)

    def test_plugin_error_inheritance(self) -> None:
        """Test PluginError is proper Exception subclass."""
        error = FlextExceptions.BaseError("Test")
        assert isinstance(error, Exception)
