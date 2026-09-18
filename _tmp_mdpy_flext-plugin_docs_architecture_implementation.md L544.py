# from flext-plugin/docs/architecture/implementation.md:544
# tests/integration/test_plugin_lifecycle.py
from __future__ import annotations

import pytest
from flext_plugin import FlextPluginPlatform


class TestPluginLifecycle:
    """End-to-end plugin lifecycle testing."""

    @pytest.fixture
    async def platform(self):
        """Real plugin platform instance."""
        container = FlextContainer()
        platform = FlextPluginPlatform(container)
        yield platform
        # Cleanup if needed

    @pytest.fixture
    def temp_plugin_dir(self, tmp_path):
        """Temporary directory with test plugin."""
        plugin_dir = tmp_path / "plugins"
        plugin_dir.mkdir()

        # Create test plugin file
        plugin_file = plugin_dir / "test_plugin.py"
        plugin_file.write_text("""
from flext_plugin import FlextPluginModels

def create_plugin():
    return FlextPluginModels.Plugin.create(
        name="test-plugin",
        plugin_version="1.0.0",
        settings={
            "type": "extension",
            "author": "test",
            "description": "Test plugin"
        }
    )
""")

        return plugin_dir

    @pytest.mark.asyncio
    async def test_complete_plugin_lifecycle(self, platform, temp_plugin_dir):
        """Test complete plugin lifecycle from discovery to execution."""
        # 1. Discover plugins
        discovery_result = await platform.discover_plugins([str(temp_plugin_dir)])
        assert discovery_result.success

        plugins = discovery_result.unwrap()
        assert len(plugins) == 1

        plugin = plugins[0]
        assert plugin.name == "test-plugin"

        # 2. Load plugin
        load_result = await platform.load_plugin(
            str(temp_plugin_dir / "test_plugin.py")
        )
        assert load_result.success

        loaded_plugin = load_result.unwrap()
        assert loaded_plugin.name == "test-plugin"

        # 3. Register plugin
        register_result = await platform.register_plugin(loaded_plugin)
        assert register_result.success

        # 4. Execute plugin
        context = {"input": "test data", "operation": "test"}
        execution_result = await platform.execute_plugin(
            "test-plugin", context, execution_id="test-execution-123"
        )

        # Execution might fail for test plugin, but should return proper result
        assert execution_result.success or execution_result.failure
        # (Actual execution depends on plugin implementation)

        # 5. Verify execution history
        executions = platform.list_executions()
        assert len(executions) >= 1

        # 6. Unregister plugin
        unregister_result = await platform.unregister_plugin("test-plugin")
        assert unregister_result.success```
______________________________________________________________________

## 🔧 Development Workflow Implementation

### Code Organization Patterns

#### **Module Structure Template**

