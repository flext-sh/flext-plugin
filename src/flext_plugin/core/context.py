"""Simple plugin context for flext-infrastructure.plugins.flext-plugin."""

from __future__ import annotations

from typing import Any


class PluginContext:
    """Simple plugin execution context."""

    def __init__(
        self,
        plugin_name: str,
        services: dict[str, Any] | None = None,
        dependencies: dict[str, Any] | None = None,
        permissions: list[str] | None = None,
        security_level: str = "standard",
    ) -> None:
        """Initialize plugin context."""
        self.plugin_name = plugin_name
        self.services = services or {}
        self.dependencies = dependencies or {}
        self.permissions = permissions or []
        self.security_level = security_level
