# from flext-plugin_docs/api-reference.md:233
from __future__ import annotations

result = platform.load_plugin(plugin)
if result.success:
    # Plugin loaded successfully
    plugin_data = result.value
else:
    # Handle error
    error_message = result.error
    print(f"Failed to load plugin: {error_message}")```
### Exception Types

