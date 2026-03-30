# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from tests.unit import (
        test_config as test_config,
        test_constants as test_constants,
        test_models as test_models,
        test_types as test_types,
    )
    from tests.unit.test_config import (
        TestFlextPluginSettings as TestFlextPluginSettings,
    )
    from tests.unit.test_constants import (
        TestFlextPluginConstants as TestFlextPluginConstants,
    )
    from tests.unit.test_models import TestFlextPluginModels as TestFlextPluginModels
    from tests.unit.test_types import TestFlextPluginTypes as TestFlextPluginTypes

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "TestFlextPluginConstants": [
        "tests.unit.test_constants",
        "TestFlextPluginConstants",
    ],
    "TestFlextPluginModels": ["tests.unit.test_models", "TestFlextPluginModels"],
    "TestFlextPluginSettings": ["tests.unit.test_config", "TestFlextPluginSettings"],
    "TestFlextPluginTypes": ["tests.unit.test_types", "TestFlextPluginTypes"],
    "test_config": ["tests.unit.test_config", ""],
    "test_constants": ["tests.unit.test_constants", ""],
    "test_models": ["tests.unit.test_models", ""],
    "test_types": ["tests.unit.test_types", ""],
}

_EXPORTS: Sequence[str] = [
    "TestFlextPluginConstants",
    "TestFlextPluginModels",
    "TestFlextPluginSettings",
    "TestFlextPluginTypes",
    "test_config",
    "test_constants",
    "test_models",
    "test_types",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
