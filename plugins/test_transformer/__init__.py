"""Test transformer plugin."""

from flext_plugin.core.base import Plugin
from flext_plugin.core.types import PluginType


class TestTransformer(Plugin):
    """Simple test transformer plugin."""

    plugin_type = PluginType.TRANSFORMER

    def execute(self, **kwargs):
        """Execute the test transformation."""
        return {"transformed_data": "processed_test_data", "status": "success"}
