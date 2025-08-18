#!/usr/bin/env python3
"""Test file to check FlextResult import and typing."""

from flext_core import FlextResult

# Test basic typing
result1: FlextResult[str] = FlextResult[str].ok("test")
result2: FlextResult[int] = FlextResult[int].ok(42)
result3: FlextResult[bool] = FlextResult[bool].fail("error")


# Test generic typing
def test_function() -> FlextResult[str]:
    return FlextResult[str].ok("success")


result4 = test_function()
