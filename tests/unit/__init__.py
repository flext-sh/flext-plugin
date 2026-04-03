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
    from flext_core.constants import FlextConstants as c
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.models import FlextModels as m
    from flext_core.protocols import FlextProtocols as p
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_core.typings import FlextTypes as t
    from flext_core.utilities import FlextUtilities as u
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
    "c": ("flext_core.constants", "FlextConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("flext_core.typings", "FlextTypes"),
    "test_config": "tests.unit.test_config",
    "test_constants": "tests.unit.test_constants",
    "test_models": "tests.unit.test_models",
    "test_types": "tests.unit.test_types",
    "u": ("flext_core.utilities", "FlextUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
