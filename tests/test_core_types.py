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
        assert PluginType.TAP.value == "tap"
        assert PluginType.TARGET.value == "target"
        assert PluginType.TRANSFORM.value == "transform"
        assert PluginType.UTILITY.value == "utility"

    def test_plugin_type_from_string(self) -> None:
        """Test creating PluginType from string values."""
        assert PluginType("tap") == PluginType.TAP
        assert PluginType("target") == PluginType.TARGET
        assert PluginType("transform") == PluginType.TRANSFORM
        assert PluginType("utility") == PluginType.UTILITY

    def test_plugin_type_invalid(self) -> None:
        """Test invalid plugin type raises error."""
        with pytest.raises(ValueError, match=".*invalid_type.*"):
            PluginType("invalid_type")


class TestPluginStatus:
    """Test PluginStatus enum functionality."""

    def test_plugin_status_values(self) -> None:
        """Test all plugin status enum values."""
        assert PluginStatus.UNKNOWN.value == "unknown"
        assert PluginStatus.DISCOVERED.value == "discovered"
        assert PluginStatus.LOADED.value == "loaded"
        assert PluginStatus.ACTIVE.value == "active"
        assert PluginStatus.ERROR.value == "error"

    def test_plugin_status_from_string(self) -> None:
        """Test creating PluginStatus from string values."""
        assert PluginStatus("unknown") == PluginStatus.UNKNOWN
        assert PluginStatus("discovered") == PluginStatus.DISCOVERED
        assert PluginStatus("loaded") == PluginStatus.LOADED
        assert PluginStatus("active") == PluginStatus.ACTIVE
        assert PluginStatus("error") == PluginStatus.ERROR


class TestPluginError:
    """Test PluginError exception functionality."""

    def test_plugin_error_creation(self) -> None:
        """Test creating PluginError with message."""
        error = PluginError("Test error message")
        assert str(error) == "Test error message"

    def test_plugin_error_with_plugin_id(self) -> None:
        """Test PluginError with plugin_id."""
        error = PluginError("Test error", plugin_id="test-plugin")
        assert error.plugin_id == "test-plugin"
        assert str(error) == "Test error"

    def test_plugin_error_with_error_code(self) -> None:
        """Test PluginError with error_code."""
        error = PluginError("Test error", error_code="TEST_ERROR")
        assert error.error_code == "TEST_ERROR"
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

        assert result.execution_id == "exec-123"
        assert result.success is True
        assert result.duration_ms == 150
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

        assert result.execution_id == "exec-456"
        assert result.success is False
        assert result.duration_ms == 75
        assert result.error_message == "Something went wrong"
        assert result.output_data == {}

    def test_execution_result_repr(self) -> None:
        """Test PluginExecutionResult string representation."""
        result = PluginExecutionResult(
            execution_id="test-123",
            success=True,
            duration_ms=100,
        )

        repr_str = repr(result)
        assert "test-123" in repr_str
        assert "SUCCESS" in repr_str
        assert "100ms" in repr_str
