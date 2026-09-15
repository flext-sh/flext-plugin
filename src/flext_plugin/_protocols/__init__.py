"""Protocols implementation for flext-plugin."""

from __future__ import annotations

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


class FlextPluginProtocolsInternal(
    FlextPluginProtocolsBase,
    FlextPluginProtocolsPluginDiscovery,
    FlextPluginProtocolsPluginLoader,
    FlextPluginProtocolsPluginRegistry,
    FlextPluginProtocolsPluginExecution,
    FlextPluginProtocolsPluginSecurity,
    FlextPluginProtocolsPluginHotReload,
    FlextPluginProtocolsPluginMonitoring,
    FlextPluginProtocolsPluginConfiguration,
    FlextPluginProtocolsPluginLifecycle,
    FlextPluginProtocolsPluginValidation,
    FlextPluginProtocolsPluginStorage,
    FlextPluginProtocolsDiscoveryStrategy,
    FlextPluginProtocolsPlatformService,
):
    """Internal protocols composition for flext-plugin."""


__all__: list[str] = [
    "FlextPluginProtocolsBase",
    "FlextPluginProtocolsDiscoveryStrategy",
    "FlextPluginProtocolsInternal",
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
]
