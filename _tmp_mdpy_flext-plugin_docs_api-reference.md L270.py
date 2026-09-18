# from flext-plugin/docs/api-reference.md:270
# Use r for all operations
from __future__ import annotations


def plugin_operation() -> p.Result[bool]:
    try:
        # Plugin operation
        return r[bool].ok(True)
    except Exception as e:
        return r[bool].fail(str(e))


# Use dependency injection

container = FlextContainer()
platform = FlextPluginPlatform(container)```
### Singer Integration

