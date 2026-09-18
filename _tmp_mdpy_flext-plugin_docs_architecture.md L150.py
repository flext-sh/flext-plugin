# from flext-plugin/docs/architecture.md:150
from __future__ import annotations


class FileSystemPluginDiscovery:
    """Discovers plugins from file system"""

    def scan_directory(self, path: str) -> p.Result[Sequence[PluginInfo]]:
        """Scan directory for plugin files"""```
#### Watchdog Integration

