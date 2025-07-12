"""Plugin domain value objects."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
            from flext_plugin.core.types import PluginType


class PluginMetadata(BaseModel):
    """Plugin metadata containing all information about a plugin."""

    id: str
    name: str
    version: str
    description: str
    plugin_type: PluginType
    capabilities: list[str] = []
    configuration_schema: dict[str, Any] | None = None

    model_config = ConfigDict(frozen=True)
