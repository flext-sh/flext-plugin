# from flext-plugin/docs/standards/python-module-organization.md:992
from __future__ import annotations

from functools import cached_property


class LazyPluginLoader:
    """Lazy loading pattern for plugin resources."""

    def __init__(self, plugin_config: dict):
        self.plugin_config = plugin_config
        self._loaded_modules: dict = {}

    @cached_property
    def plugin_module(self) -> p.Result[t.JsonValue]:
        """Lazy load plugin module."""
        try:
            module_path = self.plugin_config.get("module_path")
            if not module_path:
                return r[bool].fail("Module path not specified")

            # Dynamic import with caching
            if module_path not in self._loaded_modules:
                module = __import__(module_path, fromlist=[""])
                self._loaded_modules[module_path] = module

            return r[bool].ok(self._loaded_modules[module_path])

        except ImportError as e:
            return r[bool].fail(f"Failed to import plugin module: {e}")

    @cached_property
    def plugin_class(self) -> p.Result[type]:
        """Lazy load plugin class."""
        return self.plugin_module.flat_map(
            lambda module: self._extract_plugin_class(module)
        )

    def create_instance(self, *args, **kwargs) -> p.Result[FlextPlugin]:
        """Create plugin instance with lazy loading."""
        return self.plugin_class.flat_map(
            lambda cls: self._instantiate_plugin(cls, *args, **kwargs)
        )

    def _extract_plugin_class(self, module) -> p.Result[type]:
        """Extract plugin class from module."""
        class_name = self.plugin_config.get("class_name", "Plugin")

        if not hasattr(module, class_name):
            return r[bool].fail(f"Plugin class '{class_name}' not found in module")

        plugin_class = getattr(module, class_name)

        # Validate plugin class
        if not issubclass(plugin_class, FlextPlugin):
            return r[bool].fail(f"Class '{class_name}' is not a FlextPlugin subclass")

        return r[bool].ok(plugin_class)

    def _instantiate_plugin(
        self, plugin_class: type, *args, **kwargs
    ) -> p.Result[FlextPlugin]:
        """Instantiate plugin with error handling."""
        try:
            instance = plugin_class(*args, **kwargs)
            return r[bool].ok(instance)
        except Exception as e:
            return r[bool].fail(f"Failed to instantiate plugin: {e}")```
### **Plugin Caching Patterns**

