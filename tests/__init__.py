# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import (
        api,
        cli,
        config,
        d,
        e,
        h,
        install_local_packages,
        main,
        r,
        settings,
        td,
        tf,
        tk,
        tm,
        x,
    )

    from flext_plugin import (
        build_lazy_import_map,
        cleanup_submodule_namespace,
        core,
        install_lazy_exports,
        lazy,
        lazy_getattr,
        lazy_member,
        merge_lazy_imports,
        normalize_lazy_imports,
        plugin,
        resolve_lazy_members,
    )
    from tests.base import TestsFlextPluginServiceBase, s
    from tests.constants import TestsFlextPluginConstants, c
    from tests.models import TestsFlextPluginModels, m
    from tests.protocols import TestsFlextPluginProtocols, p
    from tests.settings import TestsFlextPluginSettings
    from tests.typings import TestsFlextPluginTypes, t
    from tests.utilities import TestsFlextPluginUtilities, u


__all__: tuple[str, ...] = (
    "TestsFlextPluginConstants",
    "TestsFlextPluginModels",
    "TestsFlextPluginProtocols",
    "TestsFlextPluginServiceBase",
    "TestsFlextPluginSettings",
    "TestsFlextPluginTypes",
    "TestsFlextPluginUtilities",
    "api",
    "build_lazy_import_map",
    "c",
    "cleanup_submodule_namespace",
    "cli",
    "config",
    "core",
    "d",
    "e",
    "h",
    "install_lazy_exports",
    "install_local_packages",
    "lazy",
    "lazy_getattr",
    "lazy_member",
    "m",
    "main",
    "merge_lazy_imports",
    "normalize_lazy_imports",
    "p",
    "plugin",
    "r",
    "resolve_lazy_members",
    "s",
    "settings",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "TestsFlextPluginConstants": ".constants",
        "TestsFlextPluginModels": ".models",
        "TestsFlextPluginProtocols": ".protocols",
        "TestsFlextPluginServiceBase": ".base",
        "TestsFlextPluginSettings": ".settings",
        "TestsFlextPluginTypes": ".typings",
        "TestsFlextPluginUtilities": ".utilities",
        "api": "flext_tests",
        "build_lazy_import_map": "flext_plugin",
        "c": ".constants",
        "cleanup_submodule_namespace": "flext_plugin",
        "cli": "flext_tests",
        "config": "flext_tests",
        "core": "flext_plugin",
        "d": "flext_tests",
        "e": "flext_tests",
        "h": "flext_tests",
        "install_lazy_exports": "flext_plugin",
        "install_local_packages": "flext_tests",
        "lazy": "flext_plugin",
        "lazy_getattr": "flext_plugin",
        "lazy_member": "flext_plugin",
        "m": ".models",
        "main": "flext_tests",
        "merge_lazy_imports": "flext_plugin",
        "normalize_lazy_imports": "flext_plugin",
        "p": ".protocols",
        "plugin": "flext_plugin",
        "r": "flext_tests",
        "resolve_lazy_members": "flext_plugin",
        "s": ".base",
        "settings": "flext_tests",
        "t": ".typings",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "x": "flext_tests",
    }),
    public_exports=__all__,
)
