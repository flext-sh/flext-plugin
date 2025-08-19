#!/usr/bin/env python3
"""Simple test file to check FlextResult import."""

from flext_core import FlextResult

# Simple test without generic typing
result = FlextResult[str].ok("test")

# Test with explicit typing
result2: FlextResult[str] = FlextResult[str].ok("test2")

# Test fail method
error_result: FlextResult[str] = FlextResult[str].fail("error")
