"""Tests for flext_plugin.core.types module.

Comprehensive tests for all plugin types and core functionality.
"""

from __future__ import annotations

import pytest

from flext_plugin.core.types import (
    PluginError,
    PluginExecutionResult,
    PluginStatus,
    PluginType,
)


class TestPluginType:
    """Test PluginType enum functionality."""

    def test_plugin_type_values(self) -> None:
        """Test all plugin type enum values."""
        if PluginType.TAP.value != "tap":
            raise AssertionError(f"Expected {"tap"}, got {PluginType.TAP.value}")
        assert PluginType.TARGET.value == "target"
        if PluginType.TRANSFORM.value != "transform":
            raise AssertionError(f"Expected {"transform"}, got {PluginType.TRANSFORM.value}")
        assert PluginType.UTILITY.value == "utility"

    def test_plugin_type_from_string(self) -> None:
        """Test creating PluginType from string values."""
        if PluginType("tap") != PluginType.TAP:
            raise AssertionError(f"Expected {PluginType.TAP}, got {PluginType("tap")}")
        assert PluginType("target") == PluginType.TARGET
        if PluginType("transform") != PluginType.TRANSFORM:
            raise AssertionError(f"Expected {PluginType.TRANSFORM}, got {PluginType("transform")}")
        assert PluginType("utility") == PluginType.UTILITY

    def test_plugin_type_invalid(self) -> None:
        """Test invalid plugin type raises error."""
        with pytest.raises(ValueError, match=".*invalid_type.*"):
            PluginType("invalid_type")


class TestPluginStatus:
    """Test PluginStatus enum functionality."""

    def test_plugin_status_values(self) -> None:
        """Test all plugin status enum values."""
        if PluginStatus.UNKNOWN.value != "unknown":
            raise AssertionError(f"Expected {"unknown"}, got {PluginStatus.UNKNOWN.value}")
        assert PluginStatus.DISCOVERED.value == "discovered"
        if PluginStatus.LOADED.value != "loaded":
            raise AssertionError(f"Expected {"loaded"}, got {PluginStatus.LOADED.value}")
        assert PluginStatus.ACTIVE.value == "active"
        if PluginStatus.ERROR.value != "error":
            raise AssertionError(f"Expected {"error"}, got {PluginStatus.ERROR.value}")

    def test_plugin_status_from_string(self) -> None:
        """Test creating PluginStatus from string values."""
        if PluginStatus("unknown") != PluginStatus.UNKNOWN:
            raise AssertionError(f"Expected {PluginStatus.UNKNOWN}, got {PluginStatus("unknown")}")
        assert PluginStatus("discovered") == PluginStatus.DISCOVERED
        if PluginStatus("loaded") != PluginStatus.LOADED:
            raise AssertionError(f"Expected {PluginStatus.LOADED}, got {PluginStatus("loaded")}")
        assert PluginStatus("active") == PluginStatus.ACTIVE
        if PluginStatus("error") != PluginStatus.ERROR:
            raise AssertionError(f"Expected {PluginStatus.ERROR}, got {PluginStatus("error")}")


class TestPluginError:
    """Test PluginError exception functionality."""

    def test_plugin_error_creation(self) -> None:
        """Test creating PluginError with message."""
        error = PluginError("Test error message")
        if str(error) != "Test error message":
            raise AssertionError(f"Expected {"Test error message"}, got {str(error)}")

    def test_plugin_error_with_plugin_id(self) -> None:
        """Test PluginError with plugin_id."""
        error = PluginError("Test error", plugin_id="test-plugin")
        if error.plugin_id != "test-plugin":
            raise AssertionError(f"Expected {"test-plugin"}, got {error.plugin_id}")
        assert str(error) == "Test error"

    def test_plugin_error_with_error_code(self) -> None:
        """Test PluginError with error_code."""
        error = PluginError("Test error", error_code="TEST_ERROR")
        if error.error_code != "TEST_ERROR":
            raise AssertionError(f"Expected {"TEST_ERROR"}, got {error.error_code}")
        assert str(error) == "Test error"

    def test_plugin_error_inheritance(self) -> None:
        """Test PluginError is proper Exception subclass."""
        error = PluginError("Test")
        assert isinstance(error, Exception)


class TestPluginExecutionResult:
    """Test PluginExecutionResult functionality."""

    def test_execution_result_success(self) -> None:
        """Test successful PluginExecutionResult."""
        result = PluginExecutionResult(
            execution_id="exec-123",
            success=True,
            duration_ms=150,
            output_data={"key": "value"},
        )

        if result.execution_id != "exec-123":

            raise AssertionError(f"Expected {"exec-123"}, got {result.execution_id}")
        if not (result.success):
            raise AssertionError(f"Expected True, got {result.success}")
        if result.duration_ms != 150:
            raise AssertionError(f"Expected {150}, got {result.duration_ms}")
        assert result.output_data == {"key": "value"}
        assert result.error_message is None

    def test_execution_result_failure(self) -> None:
        """Test failed PluginExecutionResult."""
        result = PluginExecutionResult(
            execution_id="exec-456",
            success=False,
            duration_ms=75,
            error_message="Something went wrong",
        )

        if result.execution_id != "exec-456":

            raise AssertionError(f"Expected {"exec-456"}, got {result.execution_id}")
        if result.success:
            raise AssertionError(f"Expected False, got {result.success}")\ n        assert result.duration_ms == 75
        if result.error_message != "Something went wrong":
            raise AssertionError(f"Expected {"Something went wrong"}, got {result.error_message}")
        assert result.output_data == {}

    def test_execution_result_repr(self) -> None:
        """Test PluginExecutionResult string representation."""
        result = PluginExecutionResult(
            execution_id="test-123",
            success=True,
            duration_ms=100,
        )

        repr_str = repr(result)
        if "test-123" not in repr_str:
            raise AssertionError(f"Expected {"test-123"} in {repr_str}")
        assert "SUCCESS" in repr_str
        if "100ms" not in repr_str:
            raise AssertionError(f"Expected {"100ms"} in {repr_str}")
