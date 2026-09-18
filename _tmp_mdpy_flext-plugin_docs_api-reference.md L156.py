# from flext-plugin/docs/api-reference.md:156
from __future__ import annotations


class PluginType(str, Enum):
    """Plugin type classification"""

    UTILITY = "UTILITY"  # General utility plugin
    SERVICE = "SERVICE"  # Service plugin
    MIDDLEWARE = "MIDDLEWARE"  # Middleware plugin
    TAP = "TAP"  # Singer tap plugin
    TARGET = "TARGET"  # Singer target plugin
    TRANSFORM = "TRANSFORM"  # DBT transform plugin```
______________________________________________________________________

## Factory Functions

### create_flext_plugin

