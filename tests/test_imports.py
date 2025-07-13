#!/usr/bin/env python3
"""Test script to check individual module imports."""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

modules_to_test = [
    "flext_plugin.logging_fallback",
    "flext_plugin.core.types",
    "flext_plugin.domain.entities",
]

for module in modules_to_test:
    try:
        __import__(module)
        print(f"✅ {module} - OK")
    except Exception as e:
        print(f"❌ {module} - ERROR: {e}")
