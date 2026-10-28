# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin package.

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
    from flext_cli import (
        build_lazy_import_map,
        cleanup_submodule_namespace,
        cli,
        core,
        d,
        e,
        h,
        install_lazy_exports,
        lazy,
        lazy_getattr,
        lazy_member,
        merge_lazy_imports,
        normalize_lazy_imports,
        r,
        resolve_lazy_members,
        x,
    )

    from flext_plugin.__version__ import (
        FlextPluginVersion,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
    from flext_plugin._config import FlextPluginConfig, config
    from flext_plugin._settings import FlextPluginSettings, settings
    from flext_plugin.api import FlextPluginApi, plugin
    from flext_plugin.base import FlextPluginServiceBase, s
    from flext_plugin.cli import FlextPluginCli, main
    from flext_plugin.constants import FlextPluginConstants, c
    from flext_plugin.models import FlextPluginModels, m
    from flext_plugin.protocols import FlextPluginProtocols, p
    from flext_plugin.typings import FlextPluginTypes, t
    from flext_plugin.utilities import (
        FlextPluginDiscovery,
        FlextPluginPlatform,
        FlextPluginUtilities,
        u,
    )


__all__: tuple[str, ...] = (
    "FlextPluginApi",
    "FlextPluginCli",
    "FlextPluginConfig",
    "FlextPluginConstants",
    "FlextPluginDiscovery",
    "FlextPluginModels",
    "FlextPluginPlatform",
    "FlextPluginProtocols",
    "FlextPluginServiceBase",
    "FlextPluginSettings",
    "FlextPluginTypes",
    "FlextPluginUtilities",
    "FlextPluginVersion",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
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
        "FlextPluginApi": ".api",
        "FlextPluginCli": ".cli",
        "FlextPluginConfig": "._config",
        "FlextPluginConstants": ".constants",
        "FlextPluginDiscovery": ".utilities",
        "FlextPluginModels": ".models",
        "FlextPluginPlatform": ".utilities",
        "FlextPluginProtocols": ".protocols",
        "FlextPluginServiceBase": ".base",
        "FlextPluginSettings": "._settings",
        "FlextPluginTypes": ".typings",
        "FlextPluginUtilities": ".utilities",
        "FlextPluginVersion": ".__version__",
        "__author__": ".__version__",
        "__author_email__": ".__version__",
        "__description__": ".__version__",
        "__license__": ".__version__",
        "__title__": ".__version__",
        "__url__": ".__version__",
        "__version_info__": ".__version__",
        "build_lazy_import_map": "flext_cli",
        "c": ".constants",
        "cleanup_submodule_namespace": "flext_cli",
        "cli": "flext_cli",
        "config": "._config",
        "core": "flext_cli",
        "d": "flext_cli",
        "e": "flext_cli",
        "h": "flext_cli",
        "install_lazy_exports": "flext_cli",
        "lazy": "flext_cli",
        "lazy_getattr": "flext_cli",
        "lazy_member": "flext_cli",
        "m": ".models",
        "main": ".cli",
        "merge_lazy_imports": "flext_cli",
        "normalize_lazy_imports": "flext_cli",
        "p": ".protocols",
        "plugin": ".api",
        "r": "flext_cli",
        "resolve_lazy_members": "flext_cli",
        "s": ".base",
        "settings": "._settings",
        "t": ".typings",
        "u": ".utilities",
        "x": "flext_cli",
    }),
    public_exports=__all__,
)

if not TYPE_CHECKING:
    from flext_plugin.__version__ import __version__
