"""FLEXT Plugin Protocols - public facade composing from _protocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import p as cli_p

from ._protocols import FlextPluginProtocolsInternal


class FlextPluginProtocols(cli_p, FlextPluginProtocolsInternal):
    """Unified plugin protocols extending flext_cli via MRO with internal protocols.

    Extends cli_p to inherit all foundation protocols (Result, Service, etc.)
    and adds plugin-specific protocols via internal composition.

    Architecture:
    - EXTENDS: cli_p (inherits Foundation, Domain, Application, etc.)
    - ADDS: Plugin-specific protocols via FlextPluginProtocolsInternal
    - PROVIDES: Root-level alias `p` for convenient access
    """

    class Plugin:
        """Plugin domain-specific protocols (re-exported for ergonomic access)."""

        PluginDiscovery = FlextPluginProtocolsInternal.PluginDiscovery
        PluginLoader = FlextPluginProtocolsInternal.PluginLoader
        PluginRegistry = FlextPluginProtocolsInternal.PluginRegistry
        PluginExecution = FlextPluginProtocolsInternal.PluginExecution
        PluginSecurity = FlextPluginProtocolsInternal.PluginSecurity
        PluginHotReload = FlextPluginProtocolsInternal.PluginHotReload
        PluginMonitoring = FlextPluginProtocolsInternal.PluginMonitoring
        PluginConfiguration = FlextPluginProtocolsInternal.PluginConfiguration
        PluginLifecycle = FlextPluginProtocolsInternal.PluginLifecycle
        PluginValidation = FlextPluginProtocolsInternal.PluginValidation
        PluginStorage = FlextPluginProtocolsInternal.PluginStorage
        DiscoveryStrategy = FlextPluginProtocolsInternal.DiscoveryStrategy
        PlatformService = FlextPluginProtocolsInternal.PlatformService


p = FlextPluginProtocols

__all__: list[str] = ["FlextPluginProtocols", "p"]
