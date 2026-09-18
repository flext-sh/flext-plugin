# from flext-plugin_examples/README.md:92
from __future__ import annotations

from flext_plugin import PluginType

# Create Singer tap plugin
tap_plugin = create_flext_plugin(
    name="tap-example-api",
    version="0.12.0-dev",
    plugin_type=PluginType.TAP,
    settings={
        "description": "Extract data from Example API",
        "schema_file": "tap_schema.json",
        "singer_spec": "0.12.0-dev",
    },
)
