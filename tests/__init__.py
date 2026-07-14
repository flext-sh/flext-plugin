# AUTO-GENERATED FILE — canonical lazy tests facade. Regenerate with: make gen
"""Test package facade exposing the project test aliases lazily."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from tests.base import (
        TestsFlextPluginServiceBase as TestsFlextPluginServiceBase,
        s as s,
    )
    from tests.constants import (
        TestsFlextPluginConstants as TestsFlextPluginConstants,
        c as c,
    )
    from tests.models import TestsFlextPluginModels as TestsFlextPluginModels, m as m
    from tests.protocols import (
        TestsFlextPluginProtocols as TestsFlextPluginProtocols,
        p as p,
    )
    from tests.typings import TestsFlextPluginTypes as TestsFlextPluginTypes, t as t
    from tests.utilities import (
        TestsFlextPluginUtilities as TestsFlextPluginUtilities,
        u as u,
    )

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".constants": ("TestsFlextPluginConstants", "c"),
        ".typings": ("TestsFlextPluginTypes", "t"),
        ".protocols": ("TestsFlextPluginProtocols", "p"),
        ".models": ("TestsFlextPluginModels", "m"),
        ".utilities": ("TestsFlextPluginUtilities", "u"),
        ".base": ("TestsFlextPluginServiceBase", "s"),
    },
)

install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
