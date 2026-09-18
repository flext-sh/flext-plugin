# from flext-plugin/docs/architecture/implementation.md:365
# Railway pattern throughout the system
from __future__ import annotations


async def process_plugins_workflow(
    self, plugin_names: t.StringList
) -> p.Result[t.list]:
    """Complete plugin processing workflow using railway pattern."""
    # Chain operations with automatic error propagation
    return (
        self
        ._validate_plugin_names(plugin_names)
        .flat_map(lambda names: self._load_plugins(names))
        .flat_map(lambda plugins: self._validate_plugins(plugins))
        .flat_map(lambda plugins: self._execute_plugins(plugins))
        .map(lambda results: self._format_results(results))
    )


def _validate_plugin_names(self, names: t.StringList) -> p.Result[t.StringList]:
    """Validate plugin names."""
    if not names:
        return r.fail("No plugin names provided")

    invalid_names = [name for name in names if not self._is_valid_name(name)]
    if invalid_names:
        return r.fail(f"Invalid plugin names: {invalid_names}")

    return r.ok(names)


async def _load_plugins(
    self, names: t.StringList
) -> p.Result[list[FlextPluginModels.Plugin]]:
    """Load plugins by name."""
    plugins = []
    for name in names:
        plugin_result = await self._load_single_plugin(name)
        if plugin_result.failure:
            return plugin_result  # Early return on failure
        plugins.append(plugin_result.unwrap())

    return r.ok(plugins)```
______________________________________________________________________

## 🧪 Testing Implementation Patterns

### Unit Testing Patterns

#### **Domain Entity Testing**

