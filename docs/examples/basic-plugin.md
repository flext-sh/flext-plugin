# Basic Plugin Example

This example demonstrates how to create a simple, functional plugin using the FLEXT Plugin system. The example covers plugin creation, registration, lifecycle management, and basic execution patterns.

## Overview

The basic plugin example shows:

- Creating a custom plugin class
- Implementing plugin lifecycle methods
- Handling configuration and metadata
- Error handling with FlextResult pattern
- Integration with the plugin platform
- Comprehensive testing

## Plugin Implementation

### 1. Basic Plugin Class

```python
# basic_plugin.py
from flext_plugin.domain.entities import FlextPlugin
from flext_plugin.core.types import PluginStatus, PluginType
from flext_core import FlextResult
from typing import Dict, Any, Optional
import asyncio
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class BasicDataProcessorPlugin(FlextPlugin):
    """
    Basic data processing plugin demonstrating core FLEXT Plugin concepts.

    This plugin processes input data by applying simple transformations
    and returning processed results with metadata.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None, **kwargs):
        """Initialize basic plugin with configuration."""

        # Default configuration
        default_config = {
            "description": "Basic data processing plugin",
            "author": "FLEXT Team",
            "plugin_type": PluginType.PROCESSOR,
            "batch_size": 100,
            "timeout_seconds": 30,
            "enable_logging": True
        }

        # Merge with provided config
        final_config = {**default_config, **(config or {})}

        super().__init__(
            name="basic-data-processor",
            version="1.0.0",
            config=final_config,
            **kwargs
        )

        # Plugin-specific attributes
        self._processing_stats = {
            "total_processed": 0,
            "total_errors": 0,
            "last_execution": None
        }
        self._is_initialized = False

    async def initialize(self) -> FlextResult[bool]:
        """
        Initialize plugin resources and validate configuration.

        Returns:
            FlextResult[bool]: Success/failure of initialization
        """
        try:
            logger.info(f"Initializing plugin: {self.name}")

            # Validate configuration
            validation_result = await self._validate_configuration()
            if not validation_result.success():
                return validation_result

            # Setup logging if enabled
            if self._get_config_value("enable_logging", True):
                await self._setup_logging()

            # Initialize processing resources
            await self._setup_processing_resources()

            self._is_initialized = True
            logger.info(f"Plugin {self.name} initialized successfully")

            return FlextResult.ok(True)

        except Exception as e:
            error_msg: str = f"Failed to initialize plugin {self.name}: {e}"
            logger.error(error_msg)
            return FlextResult.fail(error_msg)

    async def execute(self, data: Dict[str, Any]) -> FlextResult[Dict[str, Any]]:
        """
        Execute plugin processing logic on input data.

        Args:
            data: Input data dictionary to process

        Returns:
            FlextResult[Dict[str, Any]]: Processing results or error
        """
        try:
            # Validate plugin state
            if not self._is_initialized:
                return FlextResult.fail("Plugin not initialized")

            if self.status != PluginStatus.ACTIVE:
                return FlextResult.fail("Plugin not active")

            # Validate input data
            validation_result = await self._validate_input_data(data)
            if not validation_result.success():
                return validation_result

            # Record execution start
            start_time = datetime.utcnow()
            self._processing_stats["last_execution"] = start_time

            # Process data
            processed_data = await self._process_data(data)

            # Update statistics
            self._processing_stats["total_processed"] += 1

            # Prepare result
            result = {
                "success": True,
                "processed_data": processed_data,
                "metadata": {
                    "plugin_name": self.name,
                    "plugin_version": self.plugin_version,
                    "processing_time": (datetime.utcnow() - start_time).total_seconds(),
                    "timestamp": start_time.isoformat(),
                    "statistics": self._processing_stats.copy()
                }
            }

            logger.info(f"Successfully processed data in plugin {self.name}")
            return FlextResult.ok(result)

        except Exception as e:
            self._processing_stats["total_errors"] += 1
            error_msg: str = f"Execution failed in plugin {self.name}: {e}"
            logger.error(error_msg)
            return FlextResult.fail(error_msg)

    async def cleanup(self) -> FlextResult[bool]:
        """
        Cleanup plugin resources and save final state.

        Returns:
            FlextResult[bool]: Success/failure of cleanup
        """
        try:
            logger.info(f"Cleaning up plugin: {self.name}")

            # Save processing statistics
            await self._save_statistics()

            # Cleanup resources
            await self._cleanup_processing_resources()

            # Reset state
            self._is_initialized = False

            logger.info(f"Plugin {self.name} cleaned up successfully")
            return FlextResult.ok(True)

        except Exception as e:
            error_msg: str = f"Failed to cleanup plugin {self.name}: {e}"
            logger.error(error_msg)
            return FlextResult.fail(error_msg)

    # Plugin-specific helper methods

    async def _validate_configuration(self) -> FlextResult[bool]:
        """Validate plugin configuration."""
        try:
            batch_size = self._get_config_value("batch_size", 100)
            if not isinstance(batch_size, int) or batch_size <= 0:
                return FlextResult.fail("batch_size must be a positive integer")

            timeout = self._get_config_value("timeout_seconds", 30)
            if not isinstance(timeout, int) or timeout <= 0:
                return FlextResult.fail("timeout_seconds must be a positive integer")

            return FlextResult.ok(True)

        except Exception as e:
            return FlextResult.fail(f"Configuration validation failed: {e}")

    async def _validate_input_data(self, data: Dict[str, Any]) -> FlextResult[bool]:
        """Validate input data format."""
        try:
            if not isinstance(data, dict):
                return FlextResult.fail("Input data must be a dictionary")

            if "payload" not in data:
                return FlextResult.fail("Input data must contain 'payload' key")

            return FlextResult.ok(True)

        except Exception as e:
            return FlextResult.fail(f"Input validation failed: {e}")

    async def _process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Core data processing logic."""
        payload = data.get("payload", {})

        # Simple data transformations
        processed_payload = {}

        for key, value in payload.items():
            if isinstance(value, str):
                # Transform strings to uppercase
                processed_payload[f"processed_{key}"] = value.upper()
            elif isinstance(value, (int, float)):
                # Double numeric values
                processed_payload[f"processed_{key}"] = value * 2
            elif isinstance(value, list):
                # Get list length
                processed_payload[f"processed_{key}_count"] = len(value)
            else:
                # Keep other types as-is with prefix
                processed_payload[f"processed_{key}"] = value

        return {
            "original_payload": payload,
            "processed_payload": processed_payload,
            "transformation_count": len(processed_payload)
        }

    async def _setup_logging(self):
        """Setup plugin-specific logging."""
        # Configure logger for this plugin
        plugin_logger = logging.getLogger(f"flext.plugin.{self.name}")
        plugin_logger.setLevel(logging.INFO)

        # Add file handler if needed
        # handler = logging.FileHandler(f"{self.name}.log")
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # handler.setFormatter(formatter)
        # plugin_logger.addHandler(handler)

        logger.info("Logging configured for plugin")

    async def _setup_processing_resources(self):
        """Setup resources needed for processing."""
        # Initialize any processing resources
        # For example: database connections, file handles, etc.
        logger.info("Processing resources initialized")

    async def _cleanup_processing_resources(self):
        """Cleanup processing resources."""
        # Cleanup any allocated resources
        logger.info("Processing resources cleaned up")

    async def _save_statistics(self):
        """Save processing statistics."""
        stats_file = f"{self.name}_stats.json"
        try:
            with open(stats_file, 'w') as f:
                json.dump(self._processing_stats, f, indent=2, default=str)
            logger.info(f"Statistics saved to {stats_file}")
        except Exception as e:
            logger.warning(f"Failed to save statistics: {e}")

    def _get_config_value(self, key: str, default: Any = None) -> Any:
        """Get configuration value with fallback."""
        # Access configuration from the config dict passed during initialization
        return getattr(self, '_config', {}).get(key, default)

    # Public utility methods

    def get_statistics(self) -> Dict[str, Any]:
        """Get current processing statistics."""
        return self._processing_stats.copy()

    def reset_statistics(self):
        """Reset processing statistics."""
        self._processing_stats = {
            "total_processed": 0,
            "total_errors": 0,
            "last_execution": None
        }
        logger.info("Statistics reset")
```

### 2. Plugin Usage Example

```python
# usage_example.py
import asyncio
import logging
from basic_plugin import BasicDataProcessorPlugin
from flext_plugin import create_flext_plugin_platform

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Demonstrate basic plugin usage."""

    # Create plugin with custom configuration
    plugin_config = {
        "batch_size": 50,
        "timeout_seconds": 60,
        "enable_logging": True
    }

    plugin = BasicDataProcessorPlugin(config=plugin_config)

    # Create platform
    platform = create_flext_plugin_platform(config={
        "debug": True,
        "hot_reload": False
    })

    try:
        # Register plugin
        logger.info("Registering plugin...")
        register_result = await platform.register_plugin(plugin)
        if not register_result.success():
            logger.error(f"Registration failed: {register_result.error}")
            return

        logger.info("Plugin registered successfully")

        # Activate plugin
        logger.info("Activating plugin...")
        activate_result = await platform.activate_plugin(plugin.name)
        if not activate_result.success():
            logger.error(f"Activation failed: {activate_result.error}")
            return

        logger.info("Plugin activated successfully")

        # Execute plugin with sample data
        sample_data = {
            "payload": {
                "name": "john doe",
                "age": 30,
                "scores": [85, 90, 78, 92],
                "active": True,
                "metadata": {
                    "source": "api",
                    "timestamp": "2025-01-01T12:00:00Z"
                }
            }
        }

        logger.info("Executing plugin with sample data...")
        execution_result = await platform.execute_plugin(plugin.name, sample_data)

        if execution_result.success():
            logger.info("Plugin execution successful!")

            # Extract result data
            result_data = execution_result.data
            print("\n--- Execution Results ---")
            print(f"Success: {result_data.get('success')}")
            print(f"Processing time: {result_data.get('metadata', {}).get('processing_time', 0):.3f}s")
            print("\nProcessed Data:")

            processed_data = result_data.get('processed_data', {})
            for key, value in processed_data.items():
                print(f"  {key}: {value}")

            # Show statistics
            print("\n--- Plugin Statistics ---")
            stats = plugin.get_statistics()
            for key, value in stats.items():
                print(f"  {key}: {value}")

        else:
            logger.error(f"Plugin execution failed: {execution_result.error}")

        # Test multiple executions
        logger.info("\nExecuting plugin multiple times...")
        for i in range(3):
            test_data = {
                "payload": {
                    "test_id": i,
                    "message": f"test message {i}",
                    "value": i * 10
                }
            }

            result = await platform.execute_plugin(plugin.name, test_data)
            if result.success():
                logger.info(f"Execution {i+1}: Success")
            else:
                logger.error(f"Execution {i+1}: Failed - {result.error}")

        # Show final statistics
        print("\n--- Final Statistics ---")
        final_stats = plugin.get_statistics()
        for key, value in final_stats.items():
            print(f"  {key}: {value}")

        # Deactivate plugin
        logger.info("\nDeactivating plugin...")
        deactivate_result = await platform.deactivate_plugin(plugin.name)
        if deactivate_result.success():
            logger.info("Plugin deactivated successfully")
        else:
            logger.error(f"Deactivation failed: {deactivate_result.error}")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")

    finally:
        # Cleanup platform
        logger.info("Shutting down platform...")
        await platform.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. Comprehensive Tests

```python
# test_basic_plugin.py
import pytest
import asyncio
from unittest.mock import patch, mock_open
from basic_plugin import BasicDataProcessorPlugin
from flext_plugin import create_flext_plugin_platform
from flext_plugin.core.types import PluginStatus, PluginType

class TestBasicDataProcessorPlugin:
    """Comprehensive test suite for BasicDataProcessorPlugin."""

    @pytest.fixture
    def plugin_config(self):
        """Default plugin configuration for testing."""
        return {
            "batch_size": 10,
            "timeout_seconds": 5,
            "enable_logging": False
        }

    @pytest.fixture
    def plugin(self, plugin_config):
        """Create plugin instance for testing."""
        return BasicDataProcessorPlugin(config=plugin_config)

    @pytest.fixture
    async def platform(self):
        """Create test platform."""
        platform = create_flext_plugin_platform(config={"test_mode": True})
        yield platform
        await platform.shutdown()

    # Basic Plugin Tests

    def test_plugin_creation(self, plugin):
        """Test plugin creation and basic properties."""
        assert plugin.name == "basic-data-processor"
        assert plugin.plugin_version == "1.0.0"
        assert plugin.status == PluginStatus.INACTIVE
        assert plugin.is_valid()

    def test_plugin_configuration(self, plugin):
        """Test plugin configuration handling."""
        assert plugin._get_config_value("batch_size") == 10
        assert plugin._get_config_value("timeout_seconds") == 5
        assert plugin._get_config_value("enable_logging") is False
        assert plugin._get_config_value("nonexistent", "default") == "default"

    async def test_plugin_initialization(self, plugin):
        """Test plugin initialization."""
        result = await plugin.initialize()
        assert result.success()
        assert plugin._is_initialized

    async def test_initialization_failure(self):
        """Test initialization failure with invalid config."""
        invalid_plugin = BasicDataProcessorPlugin(config={
            "batch_size": -1,  # Invalid
            "timeout_seconds": 10
        })

        result = await invalid_plugin.initialize()
        assert result.is_failure()
        assert "batch_size must be a positive integer" in result.error

    # Execution Tests

    async def test_plugin_execution_success(self, plugin):
        """Test successful plugin execution."""
        # Initialize and activate plugin
        await plugin.initialize()
        plugin.activate()

        # Test data
        test_data = {
            "payload": {
                "name": "test user",
                "age": 25,
                "scores": [1, 2, 3],
                "active": True
            }
        }

        # Execute plugin
        result = await plugin.execute(test_data)

        assert result.success()
        assert "processed_data" in result.data
        assert "metadata" in result.data

        # Check processed data
        processed_data = result.data["processed_data"]
        assert processed_data["processed_payload"]["processed_name"] == "TEST USER"
        assert processed_data["processed_payload"]["processed_age"] == 50
        assert processed_data["processed_payload"]["processed_scores_count"] == 3
        assert processed_data["transformation_count"] == 4

    async def test_execution_without_initialization(self, plugin):
        """Test execution failure when plugin not initialized."""
        plugin.activate()

        test_data = {"payload": {"test": "data"}}
        result = await plugin.execute(test_data)

        assert result.is_failure()
        assert "Plugin not initialized" in result.error

    async def test_execution_when_inactive(self, plugin):
        """Test execution failure when plugin inactive."""
        await plugin.initialize()
        # Don't activate plugin

        test_data = {"payload": {"test": "data"}}
        result = await plugin.execute(test_data)

        assert result.is_failure()
        assert "Plugin not active" in result.error

    async def test_execution_invalid_input(self, plugin):
        """Test execution with invalid input data."""
        await plugin.initialize()
        plugin.activate()

        # Test with invalid input (missing payload)
        invalid_data = {"invalid": "data"}
        result = await plugin.execute(invalid_data)

        assert result.is_failure()
        assert "Input data must contain 'payload' key" in result.error

    # Statistics Tests

    async def test_statistics_tracking(self, plugin):
        """Test statistics tracking during execution."""
        await plugin.initialize()
        plugin.activate()

        # Initial statistics
        initial_stats = plugin.get_statistics()
        assert initial_stats["total_processed"] == 0
        assert initial_stats["total_errors"] == 0

        # Execute plugin successfully
        test_data = {"payload": {"test": "data"}}
        result = await plugin.execute(test_data)
        assert result.success()

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
    async def test_plugin_cleanup(self, mock_json_dump, plugin):
        """Test plugin cleanup."""
        await plugin.initialize()

        result = await plugin.cleanup()
        assert result.success()
        assert not plugin._is_initialized

        # Verify statistics were saved
        mock_json_dump.assert_called_once()

    # Integration Tests

    async def test_full_plugin_lifecycle(self, platform):
        """Test complete plugin lifecycle through platform."""
        plugin = BasicDataProcessorPlugin(config={"enable_logging": False})

        # Register plugin
        register_result = await platform.register_plugin(plugin)
        assert register_result.success()

        # Activate plugin
        activate_result = await platform.activate_plugin(plugin.name)
        assert activate_result.success()

        # Execute plugin
        test_data = {
            "payload": {
                "message": "hello world",
                "count": 5
            }
        }

        execute_result = await platform.execute_plugin(plugin.name, test_data)
        assert execute_result.success()

        # Verify execution result
        result_data = execute_result.data
        assert result_data["success"] is True
        assert "processed_data" in result_data
        assert "metadata" in result_data

        # Check processed data
        processed = result_data["processed_data"]["processed_payload"]
        assert processed["processed_message"] == "HELLO WORLD"
        assert processed["processed_count"] == 10

        # Deactivate plugin
        deactivate_result = await platform.deactivate_plugin(plugin.name)
        assert deactivate_result.success()

    async def test_multiple_executions(self, platform):
        """Test multiple plugin executions."""
        plugin = BasicDataProcessorPlugin(config={"enable_logging": False})

        await platform.register_plugin(plugin)
        await platform.activate_plugin(plugin.name)

        # Execute multiple times
        for i in range(5):
            test_data = {
                "payload": {
                    "id": i,
                    "value": f"test_{i}"
                }
            }

            result = await platform.execute_plugin(plugin.name, test_data)
            assert result.success()

        # Check final statistics
        stats = plugin.get_statistics()
        assert stats["total_processed"] == 5
        assert stats["total_errors"] == 0

    # Error Handling Tests

    async def test_execution_error_handling(self, plugin):
        """Test error handling during execution."""
        await plugin.initialize()
        plugin.activate()

        # Force an error by providing non-dict data
        with patch.object(plugin, '_process_data', side_effect=Exception("Processing error")):
            result = await plugin.execute({"payload": {"test": "data"}})

            assert result.is_failure()
            assert "Processing error" in result.error

            # Check error statistics
            stats = plugin.get_statistics()
            assert stats["total_errors"] == 1

# Performance Tests
class TestPluginPerformance:
    """Performance tests for the plugin."""

    @pytest.fixture
    async def initialized_plugin(self):
        """Create and initialize plugin for performance testing."""
        plugin = BasicDataProcessorPlugin(config={"enable_logging": False})
        await plugin.initialize()
        plugin.activate()
        return plugin

    @pytest.mark.asyncio
    async def test_execution_performance(self, initialized_plugin):
        """Test plugin execution performance."""
        import time

        test_data = {
            "payload": {
                "large_text": "x" * 1000,  # 1KB string
                "numbers": list(range(100)),
                "nested": {"deep": {"data": "value"}}
            }
        }

        # Measure execution time
        start_time = time.time()
        result = await initialized_plugin.execute(test_data)
        execution_time = time.time() - start_time

        assert result.success()
        assert execution_time < 1.0  # Should complete in under 1 second

        # Verify processing time is recorded
        processing_time = result.data["metadata"]["processing_time"]
        assert processing_time > 0
        assert processing_time < 1.0

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
```

### 4. Configuration File

```json
{
  "plugin": {
    "name": "basic-data-processor",
    "version": "1.0.0",
    "type": "processor",
    "description": "Basic data processing plugin for demonstration",
    "author": "FLEXT Team",
    "license": "MIT"
  },
  "configuration": {
    "batch_size": 100,
    "timeout_seconds": 30,
    "enable_logging": true,
    "log_level": "INFO"
  },
  "processing": {
    "transformations": {
      "strings": "uppercase",
      "numbers": "double",
      "lists": "count",
      "objects": "preserve"
    },
    "validation": {
      "required_fields": ["payload"],
      "max_payload_size": 10485760
    }
  },
  "metadata": {
    "tags": ["basic", "processor", "demo"],
    "keywords": ["data", "processing", "transformation"],
    "homepage": "https://github.com/flext-sh/flext",
    "repository": "https://github.com/flext-sh/flext/tree/main/flext-plugin"
  }
}
```

## Running the Example

### Prerequisites

```bash
# Install FLEXT Plugin
poetry add flext-plugin

# Or for development
git clone https://github.com/flext-sh/flext.git
cd flext/flext-plugin
make setup
```

### Execution

```bash
# Save the code files in your project directory
# basic_plugin.py, usage_example.py, test_basic_plugin.py

# Run the usage example
python usage_example.py

# Run the tests
pytest test_basic_plugin.py -v

# Run with coverage
pytest test_basic_plugin.py --cov=basic_plugin --cov-report=html
```

### Expected Output

```
INFO:__main__:Registering plugin...
INFO:__main__:Plugin registered successfully
INFO:__main__:Activating plugin...
INFO:basic_plugin:Initializing plugin: basic-data-processor
INFO:basic_plugin:Processing resources initialized
INFO:basic_plugin:Plugin basic-data-processor initialized successfully
INFO:__main__:Plugin activated successfully
INFO:__main__:Executing plugin with sample data...
INFO:basic_plugin:Successfully processed data in plugin basic-data-processor
INFO:__main__:Plugin execution successful!

--- Execution Results ---
Success: True
Processing time: 0.002s

Processed Data:
  original_payload: {'name': 'john doe', 'age': 30, 'scores': [85, 90, 78, 92], 'active': True, 'metadata': {'source': 'api', 'timestamp': '2025-01-01T12:00:00Z'}}
  processed_payload: {'processed_name': 'JOHN DOE', 'processed_age': 60, 'processed_scores_count': 4, 'processed_active': True, 'processed_metadata': {'source': 'api', 'timestamp': '2025-01-01T12:00:00Z'}}
  transformation_count: 5

--- Plugin Statistics ---
  total_processed: 1
  total_errors: 0
  last_execution: 2025-01-01 12:00:00.123456
```

## Key Learning Points

### 1. Plugin Structure

- Clean separation of concerns with initialization, execution, and cleanup
- Configuration management with validation
- Error handling using FlextResult pattern
- Statistics tracking for monitoring

### 2. Lifecycle Management

- Proper initialization before execution
- Resource allocation and cleanup
- State validation at each step

### 3. Error Handling

- Comprehensive error catching and reporting
- Graceful failure with informative error messages
- Statistics tracking for errors

### 4. Testing Strategy

- Unit tests for individual methods
- Integration tests with plugin platform
- Performance testing for execution time
- Error scenario testing

### 5. Best Practices

- Type hints for all methods
- Comprehensive logging
- Configuration validation
- Resource management
- Statistics and monitoring

This basic plugin example provides a solid foundation for building more complex plugins in the FLEXT ecosystem. The patterns demonstrated here can be extended for Singer taps, service plugins, and other specialized plugin types.
