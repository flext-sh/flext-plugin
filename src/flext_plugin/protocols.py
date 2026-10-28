# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Plugin Protocols - public facade composing from _protocols.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import p as flext_cli_p

from flext_plugin._protocols import (
    FlextPluginProtocolsBase,
    FlextPluginProtocolsPlatform,
    FlextPluginProtocolsPlugin,
)


class FlextPluginProtocols(flext_cli_p):
    """Unified plugin protocols extending flext_cli via MRO with internal protocols.

    Extends cli_p to inherit all foundation protocols (Result, Service, etc.)
    and adds plugin-specific protocols via internal composition.

    Architecture:
    - EXTENDS: cli_p (inherits Foundation, Domain, Application, etc.)
    - ADDS: Plugin-specific protocols via FlextPluginProtocolsPlugin
    - PROVIDES: Root-level alias `p` for convenient access
    """

    class Plugin(
        FlextPluginProtocolsBase,
        FlextPluginProtocolsPlugin,
        FlextPluginProtocolsPlatform,
    ):
        """Plugin domain-specific protocols.

        ``PlatformService`` is contributed through
        ``FlextPluginProtocolsPlatform`` so consumers access it as
        ``p.Plugin.PlatformService``.
        """


p = FlextPluginProtocols
__all__: list[str] = ["FlextPluginProtocols", "p"]
