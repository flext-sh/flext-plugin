"""Test extractor plugin."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class TestExtractor(ABC):
    """Simple test extractor plugin."""

    plugin_type = "extractor"

    @abstractmethod
    def execute(self, **kwargs: Any) -> dict[str, Any]:
        """Execute the test extraction."""
        return {"extracted_data": "test_data", "status": "success"}
