"""Constants implementation for flext-plugin."""

from __future__ import annotations

from .api import FlextPluginConstantsApi
from .base import FlextPluginConstantsBase
from .config import FlextPluginConstantsConfig
from .plugin import FlextPluginConstantsPlugin


class FlextPluginConstants(
    FlextPluginConstantsBase,
    FlextPluginConstantsApi,
    FlextPluginConstantsConfig,
    FlextPluginConstantsPlugin,
):
    """FLEXT Plugin Constants - composed constant definitions."""


__all__: list[str] = [
    "FlextPluginConstants",
    "FlextPluginConstantsApi",
    "FlextPluginConstantsBase",
    "FlextPluginConstantsConfig",
    "FlextPluginConstantsPlugin",
]
