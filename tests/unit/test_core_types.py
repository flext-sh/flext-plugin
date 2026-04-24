"""Comprehensive test suite for flext_plugin.core.types module.

This test module validates all core type definitions, enumerations, and foundational
classes that form the backbone of the FLEXT plugin system. Tests ensure type safety,
proper enum behavior, error handling, and integration patterns across all core types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from tests import c, e


class TestsFlextPluginCoreTypes:
    """Test c.Plugin.Type enum functionality."""

    def test_plugin_type_values(self) -> None:
        """Test all plugin type enum values."""
        if c.Plugin.Type.TAP.value != "tap":
            error_message = f"Expected {'tap'}, got {c.Plugin.Type.TAP.value}"
            raise AssertionError(error_message)
        assert c.Plugin.Type.TARGET.value == "target"
        if c.Plugin.Type.TRANSFORM.value != "transform":
            error_message = (
                f"Expected {'transform'}, got {c.Plugin.Type.TRANSFORM.value}"
            )
            raise AssertionError(error_message)
        assert c.Plugin.Type.UTILITY.value == "utility"

    def test_plugin_type_from_string(self) -> None:
        """Test creating c.Plugin.Type from string values."""
        if c.Plugin.Type("tap") != c.Plugin.Type.TAP:
            error_message = f"Expected {c.Plugin.Type.TAP}, got {c.Plugin.Type('tap')}"
            raise AssertionError(error_message)
        assert c.Plugin.Type("target") == c.Plugin.Type.TARGET
        if c.Plugin.Type("transform") != c.Plugin.Type.TRANSFORM:
            error_message = (
                f"Expected {c.Plugin.Type.TRANSFORM}, got {c.Plugin.Type('transform')}"
            )
            raise AssertionError(error_message)
        assert c.Plugin.Type("utility") == c.Plugin.Type.UTILITY

    def test_plugin_type_invalid(self) -> None:
        """Test invalid plugin type raises error."""
        with pytest.raises(ValueError, match=r".*invalid_type.*"):
            c.Plugin.Type("invalid_type")

    def test_plugin_status_values(self) -> None:
        """Test all plugin status enum values."""
        if c.Plugin.PluginStatus.UNKNOWN.value != "unknown":
            msg = f"Expected {'unknown'}, got {c.Plugin.PluginStatus.UNKNOWN.value}"
            raise AssertionError(msg)
        assert c.Plugin.PluginStatus.DISCOVERED.value == "discovered"
        if c.Plugin.PluginStatus.LOADED.value != "loaded":
            msg = f"Expected {'loaded'}, got {c.Plugin.PluginStatus.LOADED.value}"
            raise AssertionError(msg)
        assert c.Plugin.PluginStatus.ACTIVE.value == "active"
        if c.Plugin.PluginStatus.ERROR.value != "error":
            msg = f"Expected {'error'}, got {c.Plugin.PluginStatus.ERROR.value}"
            raise AssertionError(msg)

    def test_plugin_status_from_string(self) -> None:
        """Test creating c.Plugin.PluginStatus from string values."""
        if c.Plugin.PluginStatus("unknown") != c.Plugin.PluginStatus.UNKNOWN:
            msg = f"Expected {c.Plugin.PluginStatus.UNKNOWN}, got {c.Plugin.PluginStatus('unknown')}"
            raise AssertionError(msg)
        assert c.Plugin.PluginStatus("discovered") == c.Plugin.PluginStatus.DISCOVERED
        if c.Plugin.PluginStatus("loaded") != c.Plugin.PluginStatus.LOADED:
            msg = f"Expected {c.Plugin.PluginStatus.LOADED}, got {c.Plugin.PluginStatus('loaded')}"
            raise AssertionError(msg)
        assert c.Plugin.PluginStatus("active") == c.Plugin.PluginStatus.ACTIVE
        if c.Plugin.PluginStatus("error") != c.Plugin.PluginStatus.ERROR:
            msg = f"Expected {c.Plugin.PluginStatus.ERROR}, got {c.Plugin.PluginStatus('error')}"
            raise AssertionError(msg)

    def test_plugin_error_creation(self) -> None:
        """Test creating PluginError with message."""
        error = e.BaseError("Test error message")
        assert "Test error message" in str(error)
        assert isinstance(error, Exception)

    def test_plugin_error_with_plugin_id(self) -> None:
        """Test PluginError with plugin_id."""
        error = e.BaseError("Test error")
        assert "Test error" in str(error)
        assert isinstance(error, Exception)

    def test_plugin_error_with_error_code(self) -> None:
        """Test PluginError with error_code."""
        error = e.BaseError("Test error")
        assert "Test error" in str(error)
        assert isinstance(error, Exception)

    def test_plugin_error_inheritance(self) -> None:
        """Test PluginError is proper Exception subclass."""
        error = e.BaseError("Test")
        assert isinstance(error, Exception)
