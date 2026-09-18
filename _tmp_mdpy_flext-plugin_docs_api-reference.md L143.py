# from flext-plugin/docs/api-reference.md:143
from __future__ import annotations


class PluginStatus(str, Enum):
    """Plugin lifecycle status"""

    INACTIVE = "INACTIVE"  # Plugin created but not loaded
    LOADED = "LOADED"  # Plugin loaded but not active
    ACTIVE = "ACTIVE"  # Plugin active and running
    ERROR = "ERROR"  # Plugin in error state```
### PluginType

