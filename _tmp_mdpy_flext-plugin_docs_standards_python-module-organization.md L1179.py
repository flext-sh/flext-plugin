# from flext-plugin/docs/standards/python-module-organization.md:1179
# ✅ Complete type annotations for plugin interfaces
from __future__ import annotations

import typing


class PluginInterface(typing.Protocol):
    """typing.Protocol defining plugin interface with complete type safety."""

    def initialize(self) -> p.Result[bool]:
        """Initialize plugin resources."""
        ...

    def execute(self, data: dict) -> p.Result[dict]:
        """Execute plugin with typed input/output."""
        ...

    def cleanup(self) -> p.Result[bool]:
        """Cleanup plugin resources."""
        ...


# ✅ Generic plugin handler with type safety
T = typing.TypeVar("T")
U = typing.TypeVar("U")


def process_plugin_data(
    plugin: PluginInterface,
    data: dict,
    transformer: collections.abc.Callable[[dict], T],
    validator: collections.abc.Callable[[T], r[U]],
) -> p.Result[U]:
    """Process plugin data with complete type safety."""
    execution_result = plugin.execute(data)

    if execution_result.failure:
        return r[bool].fail(execution_result.error)

    try:
        transformed_data = transformer(execution_result.value)
        return validator(transformed_data)
    except Exception as e:
        return r[bool].fail(f"Data processing failed: {e}")


# ❌ Avoid untyped plugin interfaces
def execute_plugin(plugin, data):  # Missing types
    return plugin.execute(data)```
### **Error Handling Standards**

