# from flext-plugin_docs/architecture.md:161
from __future__ import annotations

from collections.abc import Callable


class WatchdogHotReload:
    """File system monitoring for hot reload"""

    def watch_directory(self, path: str, callback: Callable):
        """Monitor directory for changes"""```
______________________________________________________________________

## Integration Patterns

### FLEXT-Core Integration

#### r Pattern

All operations return `r[T]` for railway-oriented programming:

