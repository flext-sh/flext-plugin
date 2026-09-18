# from flext-plugin/docs/standards/python-module-organization.md:304
# Import from main package - gets everything needed
from __future__ import annotations

from flext_plugin import (
    create_flext_plugin,
    create_flext_plugin_platform,
)
from flext_plugin import PluginType


# Use patterns directly
def deploy_plugin():
    platform = create_flext_plugin_platform()
    plugin = create_flext_plugin(
        name="data-processor", version="0.9.9", plugin_type=PluginType.PROCESSOR
    )
    return platform.register_plugin(plugin)```
#### **2. Specific Module Pattern (For Advanced Usage)**

