# from flext-plugin_docs/guides/quick-start.md:488
# Check plugin status and validation
from __future__ import annotations

print(f"Plugin valid: {plugin.is_valid()}")
print(f"Plugin status: {plugin.status}")

# Ensure plugin is initialized before activation
plugin.initialize()
plugin.activate()```
**Hot Reload Not Working**

