#!/usr/bin/env python3
"""Simple test file to check FlextResult import."""

from flext_core import FlextResult

# Simple test without generic typing
result = FlextResult[str].ok("test")
print(f"Result: {result.data}, success: {result.success}")

# Test with explicit typing
result2: FlextResult[str] = FlextResult[str].ok("test2")
print(f"Result2: {result2.data}, success: {result2.success}")

# Test fail method
error_result: FlextResult[str] = FlextResult[str].fail("error")
print(f"Error result: {error_result.error}, success: {error_result.success}")
