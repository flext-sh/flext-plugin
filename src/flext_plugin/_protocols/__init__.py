# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin. Protocols package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .base import FlextPluginProtocolsBase
    from .platform import FlextPluginProtocolsPlatformService
    from .plugin import (
        FlextPluginProtocolsDiscoveryStrategy,
        FlextPluginProtocolsPluginConfiguration,
        FlextPluginProtocolsPluginDiscovery,
        FlextPluginProtocolsPluginExecution,
        FlextPluginProtocolsPluginHotReload,
        FlextPluginProtocolsPluginLifecycle,
        FlextPluginProtocolsPluginLoader,
        FlextPluginProtocolsPluginMonitoring,
        FlextPluginProtocolsPluginRegistry,
        FlextPluginProtocolsPluginSecurity,
        FlextPluginProtocolsPluginStorage,
        FlextPluginProtocolsPluginValidation,
    )
__all__: tuple[str, ...] = (
    "FlextPluginProtocolsBase",
    "FlextPluginProtocolsDiscoveryStrategy",
    "FlextPluginProtocolsPlatformService",
    "FlextPluginProtocolsPluginConfiguration",
    "FlextPluginProtocolsPluginDiscovery",
    "FlextPluginProtocolsPluginExecution",
    "FlextPluginProtocolsPluginHotReload",
    "FlextPluginProtocolsPluginLifecycle",
    "FlextPluginProtocolsPluginLoader",
    "FlextPluginProtocolsPluginMonitoring",
    "FlextPluginProtocolsPluginRegistry",
    "FlextPluginProtocolsPluginSecurity",
    "FlextPluginProtocolsPluginStorage",
    "FlextPluginProtocolsPluginValidation",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("FlextPluginProtocolsBase",),
            ".platform": ("FlextPluginProtocolsPlatformService",),
            ".plugin": (
                "FlextPluginProtocolsDiscoveryStrategy",
                "FlextPluginProtocolsPluginConfiguration",
                "FlextPluginProtocolsPluginDiscovery",
                "FlextPluginProtocolsPluginExecution",
                "FlextPluginProtocolsPluginHotReload",
                "FlextPluginProtocolsPluginLifecycle",
                "FlextPluginProtocolsPluginLoader",
                "FlextPluginProtocolsPluginMonitoring",
                "FlextPluginProtocolsPluginRegistry",
                "FlextPluginProtocolsPluginSecurity",
                "FlextPluginProtocolsPluginStorage",
                "FlextPluginProtocolsPluginValidation",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
