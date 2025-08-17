#!/usr/bin/env python3
"""Test file to check FlextResult import and typing."""

from flext_core import FlextResult

# Test basic typing
result1: FlextResult[str] = FlextResult[str].ok("test")
result2: FlextResult[int] = FlextResult[int].ok(42)
result3: FlextResult[bool] = FlextResult[bool].fail("error")

print(f"Result 1: {result1.data}, success: {result1.success}")
print(f"Result 2: {result2.data}, success: {result2.success}")
print(f"Result 3: error: {result3.error}, success: {result3.success}")


# Test generic typing
def test_function() -> FlextResult[str]:
    return FlextResult[str].ok("success")


result4 = test_function()
print(f"Result 4: {result4.data}, success: {result4.success}")
