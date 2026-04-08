# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "test_config": "tests.unit.test_config",
    "test_constants": "tests.unit.test_constants",
    "test_models": "tests.unit.test_models",
    "test_types": "tests.unit.test_types",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
