# from flext-plugin_docs/standards/python-module-organization.md:337
# Use factory functions for common operations
from __future__ import annotations

from flext_plugin import (
    create_flext_plugin,
)

# Simplified plugin creation
plugin = create_flext_plugin(
    name="api-gateway",
    version="2.1.0",
    plugin_type=PluginType.API,
    settings={
        "description": "API Gateway plugin",
        "author": "FLEXT Team",
        "endpoints": ["/api/v1/*", "/api/v2/*"],
    },
)```
### **Anti-Patterns (Forbidden)**

