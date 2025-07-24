"""Simple Plugin System."""

from __future__ import annotations

import importlib

# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container for flext-core imports
from flext_plugin.infrastructure.di_container import get_service_result

ServiceResult = get_service_result()


class Plugin:
    """Simple plugin base class."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.active = False

    def activate(self) -> ServiceResult[None]:
        """Activate plugin."""
        try:
            self.active = True
            return ServiceResult.ok(None)
        except Exception as e:
            return ServiceResult.fail(f"Plugin activation failed: {e}")

    def deactivate(self) -> ServiceResult[None]:
        """Deactivate plugin."""
        try:
            self.active = False
            return ServiceResult.ok(None)
        except Exception as e:
            return ServiceResult.fail(f"Plugin deactivation failed: {e}")


class PluginRegistry:
    """Simple plugin registry."""

    def __init__(self) -> None:
        self.plugins: dict[str, Plugin] = {}

    def register(self, plugin: Plugin) -> ServiceResult[None]:
        """Register a plugin."""
        try:
            self.plugins[plugin.name] = plugin
            return ServiceResult.ok(None)
        except Exception as e:
            return ServiceResult.fail(f"Plugin registration failed: {e}")

    def unregister(self, name: str) -> ServiceResult[None]:
        """Unregister a plugin."""
        try:
            if name in self.plugins:
                del self.plugins[name]
            return ServiceResult.ok(None)
        except Exception as e:
            return ServiceResult.fail(f"Plugin unregistration failed: {e}")

    def get(self, name: str) -> Plugin | None:
        """Get a plugin by name."""
        return self.plugins.get(name)

    def list_plugins(self) -> list[str]:
        """List all registered plugins."""
        return list(self.plugins.keys())


def load_plugin(module_name: str, class_name: str = "Plugin") -> ServiceResult[Plugin]:
    """Load a plugin from module."""
    try:
        module = importlib.import_module(module_name)
        plugin_class = getattr(module, class_name)
        plugin = plugin_class()
        return ServiceResult.ok(plugin)
    except ImportError as e:
        return ServiceResult.fail(f"Module import failed: {e}")
    except AttributeError as e:
        return ServiceResult.fail(f"Plugin class not found: {e}")
    except Exception as e:
        return ServiceResult.fail(f"Plugin loading failed: {e}")


def create_registry() -> PluginRegistry:
    """Create a new plugin registry."""
    return PluginRegistry()
