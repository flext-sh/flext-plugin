# from flext-plugin/docs/architecture.md:182
from __future__ import annotations


def load_plugin(self, plugin: FlextPluginModels.Entity) -> p.Result[bool]:
    try:
        # Plugin loading logic
        return r[bool].ok(True)
    except Exception as e:
        return r[bool].fail(f"Loading failed: {e}")```
#### Dependency Injection

Uses FlextContainer for service management:

