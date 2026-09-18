# from flext-plugin/docs/standards/python-module-organization.md:1231
# ✅ Plugin-specific error handling with r
from __future__ import annotations

from flext_plugin import PluginError


def safe_plugin_operation(plugin: FlextPlugin) -> p.Result[bool]:
    """Plugin operation with comprehensive error handling."""
    try:
        # Validate plugin state
        if not plugin.is_valid():
            return r[bool].fail("Plugin is not in valid state")

        # Check plugin dependencies
        dependency_check = validate_plugin_dependencies(plugin)
        if dependency_check.failure:
            return dependency_check

        # Execute plugin operation
        result = plugin.execute({})

        if result.failure:
            # Log plugin-specific error
            logger.error(
                "Plugin execution failed",
                plugin_name=plugin.name,
                plugin_version=plugin.plugin_version,
                error=result.error,
            )
            return result

        return r[bool].ok(True)

    except PluginError as e:
        # Handle plugin-specific errors
        return r[bool].fail(f"Plugin error: {e}")
    except Exception as e:
        # Handle unexpected errors
        logger.exception(
            "Unexpected error in plugin operation", plugin_name=plugin.name
        )
        return r[bool].fail(f"Unexpected error: {e}")


# ✅ Plugin error hierarchy
class PluginError(e.ProcessingError):
    """Base plugin error."""

    pass


class PluginConfigurationError(PluginError):
    """Plugin configuration error."""

    pass


class PluginDependencyError(PluginError):
    """Plugin dependency error."""

    pass


class PluginExecutionError(PluginError):
    """Plugin execution error."""

    pass


# ❌ Avoid raising exceptions in plugin business logic
def bad_plugin_operation(plugin: FlextPlugin) -> None:
    if not plugin.is_valid():
        raise ValueError("Invalid plugin")  # Breaks railway pattern```
### **Plugin Documentation Standards**

