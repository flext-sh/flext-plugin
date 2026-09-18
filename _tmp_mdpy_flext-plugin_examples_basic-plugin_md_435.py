# from flext-plugin_examples/basic-plugin.md:435
# test_basic_plugin.py
from __future__ import annotations

import pytest
from unittest.mock import patch, mock_open
from basic_plugin import BasicDataProcessorPlugin
from flext_plugin import create_flext_plugin_platform
from flext_plugin import PluginStatus, PluginType


class TestBasicDataProcessorPlugin:
    """Comprehensive test suite for BasicDataProcessorPlugin."""

    @pytest.fixture
    def plugin_config(self):
        """Default plugin configuration for testing."""
        return {"batch_size": 10, "timeout_seconds": 5, "enable_logging": False}

    @pytest.fixture
    def plugin(self, plugin_config):
        """Create plugin instance for testing."""
        return BasicDataProcessorPlugin(settings=plugin_config)

    @pytest.fixture
    def platform(self):
        """Create test platform."""
        platform = create_flext_plugin_platform(settings={"test_mode": True})
        yield platform
        platform.shutdown()

    # Basic Plugin Tests

    def test_plugin_creation(self, plugin):
        """Test plugin creation and basic properties."""
        assert plugin.name == "basic-data-processor"
        assert plugin.plugin_version == "0.9.9"
        assert plugin.status == PluginStatus.INACTIVE
        assert plugin.is_valid()

    def test_plugin_configuration(self, plugin):
        """Test plugin configuration handling."""
        assert plugin._get_config_value("batch_size") == 10
        assert plugin._get_config_value("timeout_seconds") == 5
        assert plugin._get_config_value("enable_logging") is False
        assert plugin._get_config_value("nonexistent", "default") == "default"

    def test_plugin_initialization(self, plugin):
        """Test plugin initialization."""
        result = plugin.initialize()
        assert result.success
        assert plugin._is_initialized

    def test_initialization_failure(self):
        """Test initialization failure with invalid settings."""
        invalid_plugin = BasicDataProcessorPlugin(
            settings={
                "batch_size": -1,  # Invalid
                "timeout_seconds": 10,
            }
        )

        result = invalid_plugin.initialize()
        assert result.failure
        assert "batch_size must be a positive integer" in result.error

    # Execution Tests

    def test_plugin_execution_success(self, plugin):
        """Test successful plugin execution."""
        # Initialize and activate plugin
        plugin.initialize()
        plugin.activate()

        # Test data
        test_data = {
            "payload": {
                "name": "test user",
                "age": 25,
                "scores": [1, 2, 3],
                "active": True,
            }
        }

        # Execute plugin
        result = plugin.execute(test_data)

        assert result.success
        assert "processed_data" in result.value
        assert "metadata" in result.value

        # Check processed data
        processed_data = result.value["processed_data"]
        assert processed_data["processed_payload"]["processed_name"] == "TEST USER"
        assert processed_data["processed_payload"]["processed_age"] == 50
        assert processed_data["processed_payload"]["processed_scores_count"] == 3
        assert processed_data["transformation_count"] == 4

    def test_execution_without_initialization(self, plugin):
        """Test execution failure when plugin not initialized."""
        plugin.activate()

        test_data = {"payload": {"test": "data"}}
        result = plugin.execute(test_data)

        assert result.failure
        assert "Plugin not initialized" in result.error

    def test_execution_when_inactive(self, plugin):
        """Test execution failure when plugin inactive."""
        plugin.initialize()
        # Don't activate plugin

        test_data = {"payload": {"test": "data"}}
        result = plugin.execute(test_data)

        assert result.failure
        assert "Plugin not active" in result.error

    def test_execution_invalid_input(self, plugin):
        """Test execution with invalid input data."""
        plugin.initialize()
        plugin.activate()

        # Test with invalid input (missing payload)
        invalid_data = {"invalid": "data"}
        result = plugin.execute(invalid_data)

        assert result.failure
        assert "Input data must contain 'payload' key" in result.error

    # Statistics Tests

    def test_statistics_tracking(self, plugin):
        """Test statistics tracking during execution."""
        plugin.initialize()
        plugin.activate()

        # Initial statistics
        initial_stats = plugin.get_statistics()
        assert initial_stats["total_processed"] == 0
        assert initial_stats["total_errors"] == 0

        # Execute plugin successfully
        test_data = {"payload": {"test": "data"}}
        result = plugin.execute(test_data)
        assert result.success

        # Check updated statistics
        updated_stats = plugin.get_statistics()
        assert updated_stats["total_processed"] == 1
        assert updated_stats["total_errors"] == 0
        assert updated_stats["last_execution"] is not None

    def test_statistics_reset(self, plugin):
        """Test statistics reset functionality."""
        # Modify statistics
        plugin._processing_stats["total_processed"] = 5
        plugin._processing_stats["total_errors"] = 2

        # Reset statistics
        plugin.reset_statistics()

        stats = plugin.get_statistics()
        assert stats["total_processed"] == 0
        assert stats["total_errors"] == 0
        assert stats["last_execution"] is None

    # Cleanup Tests

    @patch("builtins.open", mock_open())
    @patch("json.dump")
    def test_plugin_cleanup(self, mock_json_dump, plugin):
        """Test plugin cleanup."""
        plugin.initialize()

        result = plugin.cleanup()
        assert result.success
        assert not plugin._is_initialized

        # Verify statistics were saved
        mock_json_dump.assert_called_once()

    # Integration Tests

    def test_full_plugin_lifecycle(self, platform):
        """Test complete plugin lifecycle through platform."""
        plugin = BasicDataProcessorPlugin(settings={"enable_logging": False})

        # Register plugin
        register_result = platform.register_plugin(plugin)
        assert register_result.success

        # Activate plugin
        activate_result = platform.activate_plugin(plugin.name)
        assert activate_result.success

        # Execute plugin
        test_data = {"payload": {"message": "hello world", "count": 5}}

        execute_result = platform.execute_plugin(plugin.name, test_data)
        assert execute_result.success

        # Verify execution result
        result_data = execute_result.value
        assert result_data["success"] is True
        assert "processed_data" in result_data
        assert "metadata" in result_data

        # Check processed data
        processed = result_data["processed_data"]["processed_payload"]
        assert processed["processed_message"] == "HELLO WORLD"
        assert processed["processed_count"] == 10

        # Deactivate plugin
        deactivate_result = platform.deactivate_plugin(plugin.name)
        assert deactivate_result.success

    def test_multiple_executions(self, platform):
        """Test multiple plugin executions."""
        plugin = BasicDataProcessorPlugin(settings={"enable_logging": False})

        platform.register_plugin(plugin)
        platform.activate_plugin(plugin.name)

        # Execute multiple times
        for i in range(5):
            test_data = {"payload": {"id": i, "value": f"test_{i}"}}

            result = platform.execute_plugin(plugin.name, test_data)
            assert result.success

        # Check final statistics
        stats = plugin.get_statistics()
        assert stats["total_processed"] == 5
        assert stats["total_errors"] == 0

    # Error Handling Tests

    def test_execution_error_handling(self, plugin):
        """Test error handling during execution."""
        plugin.initialize()
        plugin.activate()

        # Force an error by providing non-dict data
        with patch.t.JsonValue(
            plugin, "_process_data", side_effect=Exception("Processing error")
        ):
            result = plugin.execute({"payload": {"test": "data"}})

            assert result.failure
            assert "Processing error" in result.error

            # Check error statistics
            stats = plugin.get_statistics()
            assert stats["total_errors"] == 1


# Performance Tests
class TestPluginPerformance:
    """Performance tests for the plugin."""

    @pytest.fixture
    def initialized_plugin(self):
        """Create and initialize plugin for performance testing."""
        plugin = BasicDataProcessorPlugin(settings={"enable_logging": False})
        plugin.initialize()
        plugin.activate()
        return plugin

    @pytest.mark.io
    def test_execution_performance(self, initialized_plugin):
        """Test plugin execution performance."""
        import time

        test_data = {
            "payload": {
                "large_text": "x" * 1000,  # 1KB string
                "numbers": list(range(100)),
                "nested": {"deep": {"data": "value"}},
            }
        }

        # Measure execution time
        start_time = time.time()
        result = initialized_plugin.execute(test_data)
        execution_time = time.time() - start_time

        assert result.success
        assert execution_time < 1.0  # Should complete in under 1 second

        # Verify processing time is recorded
        processing_time = result.value["metadata"]["processing_time"]
        assert processing_time > 0
        assert processing_time < 1.0


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
