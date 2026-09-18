# from flext-plugin/docs/api-reference.md:175
from __future__ import annotations


def create_flext_plugin(
    name: str,
    version: str,
    settings: dict | None = None,
    plugin_type: PluginType = PluginType.UTILITY,
    **kwargs,
) -> FlextPluginModels.Entity:
    """Create a new plugin entity"""```
### create_flext_plugin_platform

