# from flext-plugin/docs/api-reference.md:246
from __future__ import annotations


class FlextPluginError(Exception):
    """Base plugin system error"""


class FlextPluginConfigurationError(FlextPluginError):
    """Plugin configuration error"""


class FlextPluginLoadingError(FlextPluginError):
    """Plugin loading error"""


class FlextPluginExecutionError(FlextPluginError):
    """Plugin execution error"""```
______________________________________________________________________

## Integration Patterns

### FLEXT-Core Integration

