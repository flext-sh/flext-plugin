"""Test transformer plugin."""

from __future__ import annotations

from typing import Any

from flext_plugin.core.base import Plugin


class TestTransformer(Plugin):
    """Simple test transformer plugin."""

    plugin_type = "transformer"

    async def execute(
        self,
        input_data: Any = None,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Execute the test transformation."""
        return {"transformed_data": "processed_test_data", "status": "success"}
