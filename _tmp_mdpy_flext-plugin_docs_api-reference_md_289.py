# from flext-plugin_docs/api-reference.md:289
# Singer tap plugin example
from __future__ import annotations

from flext_plugin import FlextPlugin, PluginType


class MyTapPlugin(FlextPlugin):
    def __init__(self, **kwargs):
        super().__init__(
            name="tap-my-source",
            version="0.9.9",
            settings={"plugin_type": PluginType.TAP},
            **kwargs,
        )```
______________________________________________________________________

## Usage Examples

### Basic Plugin Management

