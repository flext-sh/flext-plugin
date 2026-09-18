# from flext-plugin_examples/basic-plugin.md:22
# basic_plugin.py
from __future__ import annotations

from flext_plugin import FlextPlugin
from flext_plugin import PluginStatus, PluginType
from flext_cli import u
from flext_core import FlextSettings

import json
from datetime import datetime

logger = logging.getLogger(__name__)


class BasicDataProcessorPlugin(FlextPlugin):
    """
    Basic data processing plugin demonstrating core FLEXT Plugin concepts.

    This plugin processes input data by applying simple transformations
    and returning processed results with metadata.
    """

    def __init__(self, settings: (dict | None) = None, **kwargs):
        """Initialize basic plugin with configuration."""

        # Default configuration
        default_config = {
            "description": "Basic data processing plugin",
            "author": "FLEXT Team",
            "plugin_type": PluginType.PROCESSOR,
            "batch_size": 100,
            "timeout_seconds": 30,
            "enable_logging": True,
        }

        # Merge with provided settings
        final_config = {**default_config, **(settings or {})}

        super().__init__(
            name="basic-data-processor",
            version="0.9.9",
            settings=final_config,
            **kwargs,
        )

        # Plugin-specific attributes
        self._processing_stats = {
            "total_processed": 0,
            "total_errors": 0,
            "last_execution": None,
        }
        self._is_initialized = False

    def initialize(self) -> p.Result[bool]:
        """
        Initialize plugin resources and validate configuration.

        Returns:
            r[bool]: Success/failure of initialization
        """
        try:
            logger.info(f"Initializing plugin: {self.name}")

            # Validate configuration
            validation_result = self._validate_configuration()
            if validation_result.failure:
                return validation_result

            # Setup logging if enabled
            if self._get_config_value("enable_logging", True):
                self._setup_logging()

            # Initialize processing resources
            self._setup_processing_resources()

            self._is_initialized = True
            logger.info(f"Plugin {self.name} initialized successfully")

            return r[bool].ok(True)

        except Exception as e:
            error_msg: str = f"Failed to initialize plugin {self.name}: {e}"
            logger.error(error_msg)
            return r[bool].fail(error_msg)

    def execute(self, data: dict) -> p.Result[dict]:
        """
        Execute plugin processing logic on input data.

        Args:
            data: Input data dictionary to process

        Returns:
            r[dict]: Processing results or error
        """
        try:
            # Validate plugin state
            if not self._is_initialized:
                return r[bool].fail("Plugin not initialized")

            if self.status != PluginStatus.ACTIVE:
                return r[bool].fail("Plugin not active")

            # Validate input data
            validation_result = self._validate_input_data(data)
            if validation_result.failure:
                return validation_result

            # Record execution start
            start_time = datetime.utcnow()
            self._processing_stats["last_execution"] = start_time

            # Process data
            processed_data = self._process_data(data)

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
                    "statistics": self._processing_stats.copy(),
                },
            }

            logger.info(f"Successfully processed data in plugin {self.name}")
            return r[bool].ok(result)

        except Exception as e:
            self._processing_stats["total_errors"] += 1
            error_msg: str = f"Execution failed in plugin {self.name}: {e}"
            logger.error(error_msg)
            return r[bool].fail(error_msg)

    def cleanup(self) -> p.Result[bool]:
        """
        Cleanup plugin resources and save final state.

        Returns:
            r[bool]: Success/failure of cleanup
        """
        try:
            logger.info(f"Cleaning up plugin: {self.name}")

            # Save processing statistics
            self._save_statistics()

            # Cleanup resources
            self._cleanup_processing_resources()

            # Reset state
            self._is_initialized = False

            logger.info(f"Plugin {self.name} cleaned up successfully")
            return r[bool].ok(True)

        except Exception as e:
            error_msg: str = f"Failed to cleanup plugin {self.name}: {e}"
            logger.error(error_msg)
            return r[bool].fail(error_msg)

    # Plugin-specific helper methods

    def _validate_configuration(self) -> p.Result[bool]:
        """Validate plugin configuration."""
        try:
            batch_size = self._get_config_value("batch_size", 100)
            if not isinstance(batch_size, int) or batch_size <= 0:
                return r[bool].fail("batch_size must be a positive integer")

            timeout = self._get_config_value("timeout_seconds", 30)
            if not isinstance(timeout, int) or timeout <= 0:
                return r[bool].fail("timeout_seconds must be a positive integer")

            return r[bool].ok(True)

        except Exception as e:
            return r[bool].fail(f"Configuration validation failed: {e}")

    def _validate_input_data(self, data: dict) -> p.Result[bool]:
        """Validate input data format."""
        try:
            if not isinstance(data, dict):
                return r[bool].fail("Input data must be a dictionary")

            if "payload" not in data:
                return r[bool].fail("Input data must contain 'payload' key")

            return r[bool].ok(True)

        except Exception as e:
            return r[bool].fail(f"Input validation failed: {e}")

    def _process_data(self, data: dict) -> dict:
        """Core data processing logic."""
        payload = data.get("payload", {})

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
            "transformation_count": len(processed_payload),
        }

    def _setup_logging(self):
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

    def _setup_processing_resources(self):
        """Setup resources needed for processing."""
        # Initialize any processing resources
        # For example: database connections, file handles, etc.
        logger.info("Processing resources initialized")

    def _cleanup_processing_resources(self):
        """Cleanup processing resources."""
        # Cleanup any allocated resources
        logger.info("Processing resources cleaned up")

    def _save_statistics(self):
        """Save processing statistics."""
        stats_file = f"{self.name}_stats.json"
        try:
            with open(stats_file, "w") as f:
                json.dump(self._processing_stats, f, indent=2, default=str)
            logger.info(f"Statistics saved to {stats_file}")
        except Exception as e:
            logger.warning(f"Failed to save statistics: {e}")

    def _get_config_value(self, key: str, default=None):
        """Get configuration value with fallback."""
        # Access configuration from the settings t.JsonMapping passed during initialization
        return getattr(self, "config", {}).get(key, default)

    # Public utility methods

    def get_statistics(self) -> dict:
        """Get current processing statistics."""
        return self._processing_stats.copy()

    def reset_statistics(self):
        """Reset processing statistics."""
        self._processing_stats = {
            "total_processed": 0,
            "total_errors": 0,
            "last_execution": None,
        }
        logger.info("Statistics reset")
