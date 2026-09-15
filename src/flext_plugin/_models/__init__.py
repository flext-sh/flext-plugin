"""Models implementation for flext-plugin."""

from __future__ import annotations

from .base import FlextPluginModelsBase
from .plugin import (
    FlextPluginModelsPluginDiscoveryData,
    FlextPluginModelsPluginEntity,
    FlextPluginModelsPluginMetadata,
    FlextPluginModelsPluginRegistry,
)


class FlextPluginModelsInternal(
    FlextPluginModelsBase,
    FlextPluginModelsPluginEntity,
    FlextPluginModelsPluginDiscoveryData,
    FlextPluginModelsPluginMetadata,
    FlextPluginModelsPluginRegistry,
):
    """Internal models composition for flext-plugin."""

    class Plugin:
        """Plugin domain namespace."""

        Entity = FlextPluginModelsPluginEntity
        DiscoveryData = FlextPluginModelsPluginDiscoveryData
        PluginMetadata = FlextPluginModelsPluginMetadata
        PluginRegistry = FlextPluginModelsPluginRegistry


__all__: list[str] = [
    "FlextPluginModelsBase",
    "FlextPluginModelsInternal",
    "FlextPluginModelsPluginDiscoveryData",
    "FlextPluginModelsPluginEntity",
    "FlextPluginModelsPluginMetadata",
    "FlextPluginModelsPluginRegistry",
]
