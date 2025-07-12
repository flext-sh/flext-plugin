"""Test extractor plugin."""

from abc import ABC, abstractmethod


class TestExtractor(ABC):
    """Simple test extractor plugin."""

    plugin_type = "extractor"

    def execute(self, **kwargs):
        """Execute the test extraction."""
        return {"extracted_data": "test_data", "status": "success"}
