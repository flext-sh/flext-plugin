# from flext-plugin/examples/basic-plugin.md:306
# usage_example.py
from __future__ import annotations

from basic_plugin import BasicDataProcessorPlugin
from flext_plugin import create_flext_plugin_platform

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Demonstrate basic plugin usage."""

    # Create plugin with custom configuration
    plugin_config = {"batch_size": 50, "timeout_seconds": 60, "enable_logging": True}

    plugin = BasicDataProcessorPlugin(settings=plugin_config)

    # Create platform
    platform = create_flext_plugin_platform(
        settings={"debug": True, "hot_reload": False}
    )

    try:
        # Register plugin
        logger.info("Registering plugin...")
        register_result = platform.register_plugin(plugin)
        if register_result.failure:
            logger.error(f"Registration failed: {register_result.error}")
            return

        logger.info("Plugin registered successfully")

        # Activate plugin
        logger.info("Activating plugin...")
        activate_result = platform.activate_plugin(plugin.name)
        if activate_result.failure:
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
                "metadata": {"source": "api", "timestamp": "2025-01-01T12:00:00Z"},
            }
        }

        logger.info("Executing plugin with sample data...")
        execution_result = platform.execute_plugin(plugin.name, sample_data)

        if execution_result.success:
            logger.info("Plugin execution successful!")

            # Extract result data
            result_data = execution_result.value
            print("\n--- Execution Results ---")
            print(f"Success: {result_data.get('success')}")
            print(
                f"Processing time: {result_data.get('metadata', {}).get('processing_time', 0):.3f}s"
            )
            print("\nProcessed Data:")

            processed_data = result_data.get("processed_data", {})
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
                    "value": i * 10,
                }
            }

            result = platform.execute_plugin(plugin.name, test_data)
            if result.success:
                logger.info(f"Execution {i + 1}: Success")
            else:
                logger.error(f"Execution {i + 1}: Failed - {result.error}")

        # Show final statistics
        print("\n--- Final Statistics ---")
        final_stats = plugin.get_statistics()
        for key, value in final_stats.items():
            print(f"  {key}: {value}")

        # Deactivate plugin
        logger.info("\nDeactivating plugin...")
        deactivate_result = platform.deactivate_plugin(plugin.name)
        if deactivate_result.success:
            logger.info("Plugin deactivated successfully")
        else:
            logger.error(f"Deactivation failed: {deactivate_result.error}")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")

    finally:
        # Cleanup platform
        logger.info("Shutting down platform...")
        platform.shutdown()


if __name__ == "__main__":
    run(main())
