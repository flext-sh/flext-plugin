# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests.constants import (
        TestsFlextPluginConstants,
        TestsFlextPluginConstants as c,
    )
    from tests.models import TestsFlextPluginModels, TestsFlextPluginModels as m
    from tests.protocols import (
        TestsFlextPluginProtocols,
        TestsFlextPluginProtocols as p,
    )
    from tests.typings import TestsFlextPluginTypes, TestsFlextPluginTypes as t
    from tests.utilities import (
        TestsFlextPluginUtilities,
        TestsFlextPluginUtilities as u,
    )
_LAZY_IMPORTS = {
    "TestsFlextPluginConstants": ("tests.constants", "TestsFlextPluginConstants"),
    "TestsFlextPluginModels": ("tests.models", "TestsFlextPluginModels"),
    "TestsFlextPluginProtocols": ("tests.protocols", "TestsFlextPluginProtocols"),
    "TestsFlextPluginTypes": ("tests.typings", "TestsFlextPluginTypes"),
    "TestsFlextPluginUtilities": ("tests.utilities", "TestsFlextPluginUtilities"),
    "c": ("tests.constants", "TestsFlextPluginConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("tests.models", "TestsFlextPluginModels"),
    "p": ("tests.protocols", "TestsFlextPluginProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("tests.typings", "TestsFlextPluginTypes"),
    "u": ("tests.utilities", "TestsFlextPluginUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "TestsFlextPluginConstants",
    "TestsFlextPluginModels",
    "TestsFlextPluginProtocols",
    "TestsFlextPluginTypes",
    "TestsFlextPluginUtilities",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
