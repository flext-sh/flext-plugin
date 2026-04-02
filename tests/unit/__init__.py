# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from tests.unit import test_config, test_constants, test_models, test_types
    from tests.unit.test_config import TestFlextPluginSettings
    from tests.unit.test_constants import TestFlextPluginConstants
    from tests.unit.test_models import TestFlextPluginModels
    from tests.unit.test_types import TestFlextPluginTypes

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "TestFlextPluginConstants": "tests.unit.test_constants",
    "TestFlextPluginModels": "tests.unit.test_models",
    "TestFlextPluginSettings": "tests.unit.test_config",
    "TestFlextPluginTypes": "tests.unit.test_types",
    "test_config": "tests.unit.test_config",
    "test_constants": "tests.unit.test_constants",
    "test_models": "tests.unit.test_models",
    "test_types": "tests.unit.test_types",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
