# from flext-plugin/docs/getting-started.md:90
from __future__ import annotations

from flext_plugin import FlextPluginPlatform

platform = FlextPluginPlatform()

# Discover plugins in directory
discovery_result = platform.scan_directory("./plugins")
if discovery_result.success:
    plugins = discovery_result.value
    print(f"Found {len(plugins)} plugins")
    for plugin in plugins:
        print(f"- {plugin.name} v{plugin.plugin_version}")```
______________________________________________________________________

## Configuration

### Environment Variables

