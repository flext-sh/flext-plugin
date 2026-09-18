# from flext-plugin_docs/architecture/implementation.md:474
# tests/unit/test_services.py
from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock
from flext_plugin import FlextPluginServices


class TestPluginServices:
    """Test application services."""

    @pytest.fixture
    def mock_container(self):
        """Mock dependency injection container."""
        container = MagicMock()
        container.get.return_value = MagicMock()
        return container

    @pytest.fixture
    def plugin_service(self, mock_container):
        """Plugin service instance."""
        return FlextPluginServices(mock_container)

    @pytest.mark.asyncio
    async def test_discover_plugins_success(self, plugin_service):
        """Test successful plugin discovery."""
        # Mock discovery protocol
        mock_discovery = AsyncMock()
        mock_discovery.discover_plugins.return_value = r.ok([
            {
                "name": "test-plugin",
                "version": "1.0.0",
                "type": "extension",
                "author": "test",
            }
        ])

        # Execute service method
        result = await plugin_service.discover_plugins(["/plugins"], mock_discovery)

        # Verify results
        assert result.success
        plugins = result.unwrap()
        assert len(plugins) == 1
        assert plugins[0].name == "test-plugin"
        assert plugins[0].plugin_version == "1.0.0"

    @pytest.mark.asyncio
    async def test_discover_plugins_validation_failure(self, plugin_service):
        """Test plugin discovery with validation failure."""
        # Mock discovery returning invalid plugin
        mock_discovery = AsyncMock()
        mock_discovery.discover_plugins.return_value = r.ok([
            {
                "name": "",  # Invalid: empty name
                "version": "1.0.0",
            }
        ])

        result = await plugin_service.discover_plugins(["/plugins"], mock_discovery)

        # Should succeed but with empty list (invalid plugin filtered out)
        assert result.success
        plugins = result.unwrap()
        assert len(plugins) == 0```
### Integration Testing Patterns

#### **End-to-End Plugin Lifecycle Testing**

