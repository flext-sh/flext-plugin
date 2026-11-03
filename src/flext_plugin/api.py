"""Public plugin composition root and MRO service facade.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextRegistry

from flext_plugin import p
from flext_plugin._utilities import FlextPluginPlatform


class FlextPluginApi(FlextPluginPlatform.PluginPlatformService):
    """Compose one registry per API unless the caller explicitly shares a port."""

    def __init__(
        self,
        *,
        registry: p.Registry | None = None,
        discovery: p.Plugin.Discovery | None = None,
        loader: p.Plugin.Loader | None = None,
        executor: p.Plugin.Executor | None = None,
        runtime_settings: p.Settings | None = None,
    ) -> None:
        """Wire collaborators without discovery, registration, or execution effects."""
        super().__init__(
            registry=FlextRegistry.create() if registry is None else registry,
            discovery=discovery,
            loader=loader,
            executor=executor,
            runtime_settings=runtime_settings,
        )


plugin: p.Plugin.PlatformService = FlextPluginApi()
"""Explicitly composed public plugin instance."""

__all__: list[str] = ["FlextPluginApi", "plugin"]
