# from flext-plugin/docs/standards/python-module-organization.md:456
from __future__ import annotations

from flext_plugin import create_flext_plugin
from flext_plugin import PluginType


# Factory pattern for plugin creation
def create_singer_tap_plugin(
    name: str, version: str, tap_config: dict
) -> p.Result[FlextPlugin]:
    """Create Singer tap plugin with validation."""
    try:
        plugin = create_flext_plugin(
            name=f"tap-{name}",
            version=version,
            plugin_type=PluginType.TAP,
            settings={
                **tap_config,
                "singer_spec": "0.9.9",
                "description": f"Singer tap for {name} data extraction",
            },
        )
        return r[bool].ok(plugin)
    except Exception as e:
        return r[bool].fail(f"Failed to create tap plugin: {e}")


# Usage with railway-oriented chaining
def deploy_tap_plugin(settings: dict) -> p.Result[FlextPlugin]:
    return (
        validate_tap_config(settings)
        .flat_map(
            lambda cfg: create_singer_tap_plugin(cfg["name"], cfg["version"], cfg)
        )
        .flat_map(lambda plugin: register_plugin(plugin))
        .flat_map(lambda plugin: activate_plugin(plugin.id))
    )```
### **Plugin Lifecycle Management**

