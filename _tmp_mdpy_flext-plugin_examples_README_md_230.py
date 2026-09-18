# from flext-plugin_examples/README.md:230
from __future__ import annotations

from flext_plugin import FlextPlugin
from flext_plugin import PluginStatus, PluginType
from flext_cli import u
from flext_core import FlextSettings


class ExamplePlugin(FlextPlugin):
    """Template for creating custom plugins."""

    def __init__(self, **kwargs):
        super().__init__(
            name="example-plugin",
            version="0.12.0-dev",
            settings={
                "plugin_type": PluginType.UTILITY,
                "description": "Example plugin template",
                "author": "Your Name",
            },
            **kwargs,
        )

    def initialize(self) -> p.Result[bool]:
        """Initialize plugin resources."""
        try:
            # Setup plugin resources
            self._setup_resources()
            return r[bool].ok(True)
        except Exception as e:
            return r[bool].fail(f"Initialization failed: {e}")

    def execute(self, data: dict) -> p.Result[dict]:
        """Execute plugin logic."""
        try:
            # Validate plugin is active
            if self.status != PluginStatus.ACTIVE:
                return r[bool].fail("Plugin not active")

            # Process data
            result = self._process_data(data)
            return r[bool].ok(result)

        except Exception as e:
            return r[bool].fail(f"Execution failed: {e}")

    def cleanup(self) -> p.Result[bool]:
        """Cleanup plugin resources."""
        try:
            self._cleanup_resources()
            return r[bool].ok(True)
        except Exception as e:
            return r[bool].fail(f"Cleanup failed: {e}")

    def _setup_resources(self):
        """Setup plugin-specific resources."""
        pass

    def _process_data(self, data: dict) -> dict:
        """Core processing logic - implement in subclass."""
        return {"processed": True, "input": data}

    def _cleanup_resources(self):
        """Cleanup plugin-specific resources."""
        pass
