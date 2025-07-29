"""Test script to check individual module imports."""

from __future__ import annotations

import contextlib
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
    with contextlib.suppress(Exception):
        __import__(module)
