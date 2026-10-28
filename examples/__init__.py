# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package.

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
    from examples.constants import ExamplesFlextPluginConstants
    from examples.models import ExamplesFlextPluginModels
    from examples.protocols import ExamplesFlextPluginProtocols
    from examples.typings import ExamplesFlextPluginTypes
    from examples.utilities import ExamplesFlextPluginUtilities, u
    from flext_plugin import (
        build_lazy_import_map,
        c,
        cleanup_submodule_namespace,
        cli,
        config,
        core,
        d,
        e,
        h,
        install_lazy_exports,
        lazy,
        lazy_getattr,
        lazy_member,
        m,
        main,
        merge_lazy_imports,
        normalize_lazy_imports,
        p,
        plugin,
        r,
        resolve_lazy_members,
        s,
        settings,
        t,
        x,
    )


__all__: tuple[str, ...] = (
    "ExamplesFlextPluginConstants",
    "ExamplesFlextPluginModels",
    "ExamplesFlextPluginProtocols",
    "ExamplesFlextPluginTypes",
    "ExamplesFlextPluginUtilities",
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
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "ExamplesFlextPluginConstants": ".constants",
        "ExamplesFlextPluginModels": ".models",
        "ExamplesFlextPluginProtocols": ".protocols",
        "ExamplesFlextPluginTypes": ".typings",
        "ExamplesFlextPluginUtilities": ".utilities",
        "build_lazy_import_map": "flext_plugin",
        "c": "flext_plugin",
        "cleanup_submodule_namespace": "flext_plugin",
        "cli": "flext_plugin",
        "config": "flext_plugin",
        "core": "flext_plugin",
        "d": "flext_plugin",
        "e": "flext_plugin",
        "h": "flext_plugin",
        "install_lazy_exports": "flext_plugin",
        "lazy": "flext_plugin",
        "lazy_getattr": "flext_plugin",
        "lazy_member": "flext_plugin",
        "m": "flext_plugin",
        "main": "flext_plugin",
        "merge_lazy_imports": "flext_plugin",
        "normalize_lazy_imports": "flext_plugin",
        "p": "flext_plugin",
        "plugin": "flext_plugin",
        "r": "flext_plugin",
        "resolve_lazy_members": "flext_plugin",
        "s": "flext_plugin",
        "settings": "flext_plugin",
        "t": "flext_plugin",
        "u": ".utilities",
        "x": "flext_plugin",
    }),
    public_exports=__all__,
)
