# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from tests.unit.test_config import TestFlextPluginSettings
    from tests.unit.test_constants import (
        TestFlextPluginConstants,
        TestFlextPluginConstants as c,
    )
    from tests.unit.test_models import TestFlextPluginModels, TestFlextPluginModels as m
    from tests.unit.test_types import TestFlextPluginTypes, TestFlextPluginTypes as t

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "TestFlextPluginConstants": (
        "tests.unit.test_constants",
        "TestFlextPluginConstants",
    ),
    "TestFlextPluginModels": ("tests.unit.test_models", "TestFlextPluginModels"),
    "TestFlextPluginSettings": ("tests.unit.test_config", "TestFlextPluginSettings"),
    "TestFlextPluginTypes": ("tests.unit.test_types", "TestFlextPluginTypes"),
    "c": ("tests.unit.test_constants", "TestFlextPluginConstants"),
    "m": ("tests.unit.test_models", "TestFlextPluginModels"),
    "t": ("tests.unit.test_types", "TestFlextPluginTypes"),
}

__all__ = [
    "TestFlextPluginConstants",
    "TestFlextPluginModels",
    "TestFlextPluginSettings",
    "TestFlextPluginTypes",
    "c",
    "m",
    "t",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
