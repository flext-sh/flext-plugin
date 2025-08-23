#!/usr/bin/env python3
"""Test file to check FlextResult generic typing."""

from typing import TypeVar

from flext_core import FlextResult

# Test with explicit type variables
T = TypeVar("T")


def test_generic_function[T](data: T) -> FlextResult[T]:
    """Test function with generic typing."""
    return FlextResult[T].ok(data)


# Test with specific types
def test_string_function() -> FlextResult[str]:
    """Test function returning FlextResult[str]."""
    return FlextResult[str].ok("success")


def test_int_function() -> FlextResult[int]:
    """Test function returning FlextResult[int]."""
    return FlextResult[int].ok(42)


def test_bool_function() -> FlextResult[bool]:
    """Test function returning FlextResult[bool]."""
    return FlextResult[bool].ok(data=True)


# Test calls
result1 = test_string_function()
result2 = test_int_function()
result3 = test_bool_function()


# Test generic function
generic_result = test_generic_function("generic test")
