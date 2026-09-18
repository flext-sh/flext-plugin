# from flext-plugin/examples/README.md:73
from __future__ import annotations

from flext_plugin import create_flext_plugin, create_flext_plugin_platform
from flext_plugin import PluginType

# Create simple plugin
plugin = create_flext_plugin(
    name="hello-world", version="0.12.0-dev", plugin_type=PluginType.UTILITY
)

# Create platform and register plugin
platform = create_flext_plugin_platform()
platform.register_plugin(plugin)
platform.activate_plugin("hello-world")
