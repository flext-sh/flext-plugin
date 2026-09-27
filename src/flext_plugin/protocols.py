"""FLEXT Plugin Protocols - public facade composing from _protocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliProtocols

from ._protocols.platform import FlextPluginProtocolsPlatformService
from ._protocols.plugin import FlextPluginProtocolsPlugin


class FlextPluginProtocols(FlextCliProtocols):
    """Unified plugin protocols extending flext_cli via MRO with internal protocols.

    Extends cli_p to inherit all foundation protocols (Result, Service, etc.)
    and adds plugin-specific protocols via internal composition.

    Architecture:
    - EXTENDS: cli_p (inherits Foundation, Domain, Application, etc.)
    - ADDS: Plugin-specific protocols via FlextPluginProtocolsPlugin
    - PROVIDES: Root-level alias `p` for convenient access
    """

    class Plugin(FlextPluginProtocolsPlugin):
        """Plugin domain-specific protocols.

        PlatformService is re-exported here from its separate owner module
        so consumers access it as ``p.Plugin.PlatformService``.
        """

        PlatformService = FlextPluginProtocolsPlatformService


p = FlextPluginProtocols

__all__: list[str] = ["FlextPluginProtocols", "p"]
