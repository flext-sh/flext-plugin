# from flext-plugin/docs/architecture.md:196
from __future__ import annotations


def _setup_services(self) -> None:
    """Register services in DI container"""
    self.container.bind("plugin_service", FlextPluginService(container=self.container))```
### Singer Ecosystem Integration

Plugins can implement Singer tap/target patterns:

