"""Base plugin interface and metadata classes for the enterprise plugin system.

REFACTORED:
    Uses flext-core domain entities, mixins, and types - NO duplication.
Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import UTC, datetime
from typing import TYPE_CHECKING, ClassVar

from flext_plugin.domain.entities import (
    PluginConfiguration,
    PluginLifecycle,
    PluginStatus,
)

if TYPE_CHECKING:
    import jsonschema  # type: ignore
    import psutil  # type: ignore

    from flext_plugin.domain.value_objects import PluginMetadata
    from flext_plugin.types import (
        ConfigurationDict,
        PluginContext,
        PluginData,
        PluginResult,
    )
else:
    try:
        import jsonschema
        import psutil
    except ImportError:
        jsonschema = None  # type: ignore
        psutil = None  # type: ignore


class Plugin(ABC):
    """Abstract base class for all FLEXT enterprise plugins.

    Defines the contract that all plugins must implement for proper
    integration with the enterprise plugin system, including lifecycle
    management, configuration, and execution patterns.
    """

    # Plugin metadata - must be defined by concrete implementations
    METADATA: ClassVar[PluginMetadata]

    def __init__(self, config: ConfigurationDict | None = None) -> None:
        """Initialize plugin with configuration.

        Args:
            config: Optional configuration dictionary for the plugin.

        """
        self._config = config or {}
        self._lifecycle_state = PluginLifecycle.UNREGISTERED
        self._status = PluginStatus.UNKNOWN
        self._initialized = False
        self._last_health_check = datetime.now(UTC)

        # Create configuration instance
        self._configuration = PluginConfiguration(**(config or {}))

    @property
    def metadata(self) -> PluginMetadata:
        """Get plugin metadata.

        Returns:
            Plugin metadata instance containing name, version, and capabilities.

        """
        return self.METADATA

    @property
    def lifecycle_state(self) -> PluginLifecycle:
        """Get current plugin lifecycle state.

        Returns:
            Current lifecycle state of the plugin.

        """
        return self._lifecycle_state

    @property
    def status(self) -> PluginStatus:
        """Get current plugin status.

        Returns:
            Current operational status of the plugin.

        """
        return self._status

    @property
    def config(self) -> ConfigurationDict:
        """Get plugin configuration as dictionary.

        Returns:
            Copy of the plugin configuration dictionary.

        """
        return self._config.copy()

    @property
    def configuration(self) -> PluginConfiguration:
        """Get plugin configuration instance.

        Returns:
            Plugin configuration domain object.

        """
        return self._configuration

    @property
    def is_initialized(self) -> bool:
        """Check if plugin is initialized.

        Returns:
            True if plugin has been initialized, False otherwise.

        """
        return self._initialized

    def _update_lifecycle_state(self, state: PluginLifecycle) -> None:
        """Update plugin lifecycle state.

        Args:
            state: New lifecycle state to set.

        """
        self._lifecycle_state = state

    def _update_status(self, status: PluginStatus) -> None:
        """Update plugin status and health check timestamp.

        Args:
            status: New plugin status to set.

        """
        self._status = status
        self._last_health_check = datetime.now(UTC)

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the plugin.

        Performs plugin initialization including resource setup,
        configuration validation, and dependency loading.

        Raises:
            PluginInitializationError: If initialization fails.

        """
        ...

    @abstractmethod
    async def cleanup(self) -> None:
        """Clean up plugin resources.

        Performs graceful shutdown of the plugin including
        resource cleanup and connection termination.

        Raises:
            PluginCleanupError: If cleanup fails.

        """
        ...

    @abstractmethod
    async def health_check(self) -> ConfigurationDict:
        """Perform plugin health check.

        Returns:
            Dictionary containing health status and diagnostic information.

        Raises:
            PluginHealthCheckError: If health check fails.

        """
        ...

    @abstractmethod
    async def execute(
        self,
        input_data: PluginData,
        context: PluginContext,
    ) -> PluginResult:
        """Execute plugin with input data and context.

        Args:
            input_data: Input data for plugin execution.
            context: Execution context and parameters.

        Returns:
            Plugin execution result.

        Raises:
            PluginExecutionError: If execution fails.

        """
        ...

    async def validate_configuration(self, config: ConfigurationDict) -> list[str]:
        """Validate plugin configuration.

        Args:
            config: Configuration dictionary to validate.

        Returns:
            List of validation error messages, empty if valid.

        """
        # Basic validation - can be overridden by concrete implementations
        errors = []

        if not isinstance(config, dict):
            errors.append("Configuration must be a dictionary")
            return errors

        # Validate against configuration schema if available:
        schema = self.metadata.configuration_schema
        if schema:
            if jsonschema:
                try:
                    jsonschema.validate(instance=config, schema=schema)
                except jsonschema.ValidationError as e:
                    errors.append(f"Configuration validation failed: {e.message}")
                except jsonschema.SchemaError as e:
                    errors.append(f"Invalid configuration schema: {e.message}")
            else:
                errors.append(
                    "jsonschema not available - cannot validate configuration",
                )

        return errors

    async def get_capabilities(self) -> list[str]:
        """Get list of plugin capabilities.

        Returns:
            List of capability strings that this plugin supports.

        """
        return [str(capability) for capability in self.metadata.capabilities]

    async def get_resource_usage(self) -> ConfigurationDict:
        """Get current resource usage statistics.

        Returns:
            Dictionary containing memory, CPU, and other resource metrics.

        """
        if psutil:
            process = psutil.Process()
            MB_TO_BYTES = 1024 * 1024

            return {
                "memory_mb": process.memory_info().rss / MB_TO_BYTES,
                "cpu_percent": process.cpu_percent(),
                "open_files": len(process.open_files()),
                "threads": process.num_threads(),
                "status": process.status(),
            }
        return {
            "memory_mb": 0.0,
            "cpu_percent": 0.0,
            "open_files": 0,
            "threads": 0,
            "status": "unknown",
        }


class BaseExtractorPlugin(Plugin):
    """Base class for data extractor plugins.

    Specialized base class for plugins that extract data from various
    sources including databases, APIs, files, and streaming systems.
    """

    @abstractmethod
    async def extract(self, source_config: ConfigurationDict) -> PluginResult:
        """Extract data from configured source.

        Args:
            source_config: Source configuration parameters.

        Returns:
            Extracted data in appropriate format.

        Raises:
            PluginExtractionError: If data extraction fails.

        """
        ...

    async def execute(
        self,
        _input_data: PluginData,
        context: PluginContext,
    ) -> PluginResult:
        """Execute extractor plugin by extracting from source.

        Args:
            _input_data: Unused input data (extractors read from source).
            context: Execution context containing source_config.

        Returns:
            Extracted data from the configured source.

        """
        source_config = context.get("source_config", {})
        return await self.extract(source_config)


class BaseLoaderPlugin(Plugin):
    """Base class for data loader plugins.

    Specialized base class for plugins that load data into various
    destinations including databases, data warehouses, and file systems.
    """

    @abstractmethod
    async def load(
        self,
        data: PluginData,
        destination_config: ConfigurationDict,
    ) -> ConfigurationDict:
        """Load data to configured destination.

        Args:
            data: Data to load to the destination.
            destination_config: Destination configuration parameters.

        Returns:
            Dictionary containing load results and statistics.

        Raises:
            PluginLoadError: If data loading fails.

        """
        ...

    async def execute(
        self,
        input_data: PluginData,
        context: PluginContext,
    ) -> PluginResult:
        """Execute loader plugin by loading data to destination.

        Args:
            input_data: Data to load to the destination.
            context: Execution context containing destination_config.

        Returns:
            Load results and statistics from the destination.

        """
        destination_config = context.get("destination_config", {})
        return await self.load(input_data, destination_config)


class BaseTransformerPlugin(Plugin):
    """Base class for data transformer plugins.

    Specialized base class for plugins that transform, validate,
    and enrich data during pipeline processing.
    """

    @abstractmethod
    async def transform(
        self,
        data: PluginData,
        transform_config: ConfigurationDict,
    ) -> PluginResult:
        """Transform input data according to configuration.

        Args:
            data: Input data to transform.
            transform_config: Transformation configuration parameters.

        Returns:
            Transformed data in the target format.

        Raises:
            PluginTransformError: If data transformation fails.

        """
        ...

    async def execute(
        self,
        input_data: PluginData,
        context: PluginContext,
    ) -> PluginResult:
        """Execute transformer plugin by transforming input data.

        Args:
            input_data: Data to transform.
            context: Execution context containing transform_config.

        Returns:
            Transformed data according to configuration.

        """
        transform_config = context.get("transform_config", {})
        return await self.transform(input_data, transform_config)
