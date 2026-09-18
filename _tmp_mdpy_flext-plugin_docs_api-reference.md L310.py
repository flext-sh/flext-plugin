# from flext-plugin/docs/api-reference.md:310
from __future__ import annotations

from flext_plugin import FlextPluginPlatform, create_flext_plugin

# Create platform
platform = FlextPluginPlatform()

# Create and load plugin
plugin = create_flext_plugin("my-plugin", "0.9.9")
result = platform.load_plugin(plugin)

if result.success:
    # Enable plugin
    enable_result = platform.enable_plugin("my-plugin")
    if enable_result.success:
        print("Plugin ready for use")```
### Plugin Discovery

