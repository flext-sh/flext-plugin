"""Data Flow Management for Plugin Pipeline Execution.

This module provides data structures and mechanisms for managing data flow
between pipeline steps, including data validation, transformation tracking, and step communication protocols.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from flext_core.domain.pydantic_base import DomainBaseModel, Field

if TYPE_CHECKING:
    from flext_plugin.types import PluginData, PluginExecutionResult, PluginType


class DataFlowContext(DomainBaseModel):
    """Context information for data flow between pipeline steps."""

    model_config = {"frozen": True}

    # Execution identifiers
    pipeline_id: str = Field(description="Pipeline execution identifier")
    execution_id: str = Field(description="Current execution identifier")
    step_id: str = Field(description="Current step identifier")

    # Data flow tracking
    source_step_id: str | None = Field(
        default=None,
        description="Source step that produced this data",
    )
    data_lineage: list[str] = Field(
        default_factory=list,
        description="Chain of steps that processed this data",
    )

    # Metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    user_id: str | None = Field(
        default=None,
        description="User who initiated the pipeline",
    )
    environment: str = Field(default="development", description="Execution environment")

    # Configuration and state
    pipeline_config: dict[str, Any] = Field(
        default_factory=dict,
        description="Pipeline configuration",
    )
    step_config: dict[str, Any] = Field(
        default_factory=dict,
        description="Current step configuration",
    )
    global_variables: dict[str, Any] = Field(
        default_factory=dict,
        description="Global pipeline variables",
    )


class DataPacket(DomainBaseModel):
    """Container for data flowing between pipeline steps."""

    model_config = {"frozen": False}  # Allow mutations for data transformation

    # Data payload
    data: Any = Field(description="The actual data payload")
    data_schema: dict[str, Any] | None = Field(
        default=None,
        description="Data schema information",
    )

    # Metadata
    packet_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique packet identifier",
    )
    size_bytes: int | None = Field(default=None, description="Data size in bytes")
    row_count: int | None = Field(
        default=None,
        description="Number of records (if applicable)",
    )

    # Processing information
    source_plugin_id: str | None = Field(
        default=None,
        description="Plugin that generated this data",
    )
    source_plugin_type: PluginType | None = Field(
        default=None,
        description="Type of source plugin",
    )
    processing_metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Processing metadata",
    )

    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_modified_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Validation and quality
    validation_errors: list[str] = Field(
        default_factory=list,
        description="Data validation errors",
    )
    quality_metrics: dict[str, Any] = Field(
        default_factory=dict,
        description="Data quality metrics",
    )

    def update_data(
        self,
        new_data: PluginData,
        plugin_id: str,
        processing_info: dict[str, Any] | None = None,
    ) -> None:
        """Update packet data with new content and metadata."""
        self.data = new_data
        self.source_plugin_id = plugin_id
        self.last_modified_at = datetime.now(UTC)

        if processing_info:
            self.processing_metadata.update(processing_info)

        # Update size and row count if possible:
        self._update_metrics()

    def add_validation_error(self, error: str) -> None:
        """Add validation error to packet."""
        if error not in self.validation_errors:
            self.validation_errors.append(error)

    def is_valid(self) -> bool:
        """Check if packet has no validation errors."""
        return len(self.validation_errors) == 0

    def get_data_summary(self) -> dict[str, Any]:
        """Get summary information about the data packet."""
        return {
            "packet_id": self.packet_id,
            "source_plugin": self.source_plugin_id,
            "size_bytes": self.size_bytes,
            "row_count": self.row_count,
            "has_schema": self.data_schema is not None,
            "is_valid": self.is_valid(),
            "validation_errors_count": len(self.validation_errors),
            "created_at": self.created_at.isoformat(),
            "last_modified_at": self.last_modified_at.isoformat(),
        }

    def _update_metrics(self) -> None:
        try:
            # Estimate size in bytes
            if isinstance(self.data, str):
                self.size_bytes = len(self.data.encode("utf-8"))
            elif isinstance(self.data, list | dict):
                # Rough estimate using JSON serialization
                self.size_bytes = len(
                    json.dumps(self.data, default=str).encode("utf-8"),
                )

            # Count rows if data is a list:
            if isinstance(self.data, list):
                self.row_count = len(self.data)
            elif (
                isinstance(self.data, dict)
                and "data" in self.data
                and isinstance(self.data["data"], list)
            ):
                self.row_count = len(self.data["data"])
        except (ValueError, TypeError, OSError, OverflowError):
            # If metrics calculation fails, just skip it
            pass


class StepResult(DomainBaseModel):
    """Result of executing a single pipeline step."""

    model_config = {"frozen": True}

    # Step identification
    step_id: str = Field(description="Step identifier")
    plugin_id: str = Field(description="Plugin identifier that executed")
    plugin_type: PluginType = Field(description="Type of plugin")

    # Execution results
    success: bool = Field(description="Whether step executed successfully")
    execution_result: PluginExecutionResult | None = Field(
        default=None,
        description="Plugin execution result",
    )
    output_data: DataPacket | None = Field(
        default=None,
        description="Output data packet",
    )

    # Timing and performance
    start_time: datetime = Field(default_factory=lambda: datetime.now(UTC))
    end_time: datetime | None = Field(default=None, description="Step completion time")
    duration_ms: int | None = Field(
        default=None,
        description="Execution duration in milliseconds",
    )

    # Error information
    error_message: str | None = Field(
        default=None,
        description="Error message if step failed",
    )
    error_details: dict[str, Any] = Field(
        default_factory=dict,
        description="Detailed error information",
    )

    # Metrics and monitoring
    memory_usage_mb: float | None = Field(default=None, description="Peak memory usage")
    cpu_time_ms: float | None = Field(default=None, description="CPU time consumed")

    def mark_completed(
        self,
        output_data: DataPacket | None = None,
        error: str | None = None,
    ) -> None:
        """Mark step as completed with optional output data or error."""
        if not self.model_config.get("frozen"):
            self.end_time = datetime.now(UTC)
            if self.start_time:
                duration = (self.end_time - self.start_time).total_seconds() * 1000
                self.duration_ms = int(duration)

            if error:
                self.success = False
                self.error_message = error
            else:
                self.success = True
                self.output_data = output_data


class PipelineDataFlow(DomainBaseModel):
    """Manages data flow through an entire pipeline execution."""

    model_config = {"frozen": False}

    # Pipeline identification
    pipeline_id: str = Field(description="Pipeline identifier")
    execution_id: str = Field(description="Execution identifier")

    # Data flow state
    current_step_index: int = Field(
        default=0,
        description="Current step being executed",
    )
    step_results: list[StepResult] = Field(
        default_factory=list,
        description="Results of completed steps",
    )
    current_data: DataPacket | None = Field(
        default=None,
        description="Current data flowing through pipeline",
    )

    # Context and configuration
    context: DataFlowContext = Field(description="Pipeline execution context")

    # Flow control
    should_continue: bool = Field(
        default=True,
        description="Whether pipeline should continue execution",
    )
    abort_reason: str | None = Field(
        default=None,
        description="Reason for aborting pipeline",
    )

    # Statistics and monitoring
    total_steps: int = Field(default=0, description="Total number of steps in pipeline")
    completed_steps: int = Field(default=0, description="Number of completed steps")
    failed_steps: int = Field(default=0, description="Number of failed steps")

    def start_step(
        self, step_id: str, plugin_id: str, plugin_type: PluginType,
    ) -> StepResult:
        """Start execution of a new pipeline step."""
        step_result = StepResult(
            step_id=step_id,
            plugin_id=plugin_id,
            plugin_type=plugin_type,
            success=False,
        )

        self.step_results.append(step_result)
        return step_result

    def complete_step(
        self,
        step_result: StepResult,
        output_data: DataPacket | None = None,
    ) -> None:
        """Complete pipeline step and update flow state."""
        step_result.mark_completed(output_data)

        if step_result.success:
            self.completed_steps += 1
            if output_data:
                self.current_data = output_data
        else:
            self.failed_steps += 1
            # Stop pipeline execution on failure
            self.should_continue = False
            self.abort_reason = (
                f"Step {step_result.step_id} failed: {step_result.error_message}"
            )

        self.current_step_index += 1

    def abort_pipeline(self, reason: str) -> None:
        """Abort pipeline execution with specified reason."""
        self.should_continue = False
        self.abort_reason = reason

    def get_step_by_id(self, step_id: str) -> StepResult | None:
        """Find step result by step ID."""
        for step in self.step_results:
            if step.step_id == step_id:
                return step
        return None

    def get_last_successful_step(self) -> StepResult | None:
        """Get the most recent successful step result."""
        for step in reversed(self.step_results):
            if step.success:
                return step
        return None

    def get_execution_summary(self) -> dict[str, Any]:
        """Get comprehensive pipeline execution summary."""
        total_duration = 0
        if self.step_results:
            for step in self.step_results:
                if step.duration_ms:
                    total_duration += step.duration_ms
        return {
            "pipeline_id": self.pipeline_id,
            "execution_id": self.execution_id,
            "total_steps": self.total_steps,
            "completed_steps": self.completed_steps,
            "failed_steps": self.failed_steps,
            "current_step_index": self.current_step_index,
            "should_continue": self.should_continue,
            "abort_reason": self.abort_reason,
            "total_duration_ms": total_duration,
            "has_output_data": self.current_data is not None,
            "execution_context": {
                "user_id": self.context.user_id,
                "environment": self.context.environment,
                "created_at": self.context.created_at.isoformat(),
            },
        }


class DataValidator:
    """Validates data flowing through pipeline steps."""

    @staticmethod
    def validate_data_packet(
        packet: DataPacket,
        expected_schema: dict[str, Any] | None = None,
    ) -> list[str]:
        """Validate data packet against optional schema."""
        errors = []

        # Basic validation
        if packet.data is None:
            errors.append("Data payload is None")
            return errors

        # Schema validation if provided:
        if expected_schema:
            schema_errors = DataValidator._validate_against_schema(
                packet.data,
                expected_schema,
            )
            errors.extend(schema_errors)

        # Data type validation
        if isinstance(packet.data, dict):
            if "data" in packet.data:
                # Plugin result format
                if not isinstance(packet.data["data"], list | dict):
                    errors.append("Invalid data format in plugin result")
            elif "error" in packet.data:
                errors.append(f"Data contains error: {packet.data['error']}")

        return errors

    @staticmethod
    def _validate_against_schema(data: PluginData, schema: dict[str, Any]) -> list[str]:
        errors = []

        try:
            # This is a simplified schema validation
            # In a full implementation, you would use jsonschema library
            schema_type = schema.get("type")

            if schema_type == "object" and not isinstance(data, dict):
                errors.append(f"Expected object, got {type(data).__name__}")
            elif schema_type == "array" and not isinstance(data, list):
                errors.append(f"Expected array, got {type(data).__name__}")
            elif schema_type == "string" and not isinstance(data, str):
                errors.append(f"Expected string, got {type(data).__name__}")
            elif schema_type == "number" and not isinstance(data, int | float):
                errors.append(f"Expected number, got {type(data).__name__}")

            # Validate required fields for objects
            if schema_type == "object" and isinstance(data, dict):
                required_fields = schema.get("required", [])
                errors.extend(
                    f"Required field '{field}' is missing"
                    for field in required_fields
                    if field not in data
                )

        except (ValueError, TypeError, KeyError, AttributeError) as e:
            errors.append(f"Schema validation error: {e}")

        return errors


class DataFlowManager:
    """Manages data flow and step execution in a pipeline."""

    def __init__(
        self, pipeline_id: str, execution_id: str, context: DataFlowContext,
    ) -> None:
        """Initialize data flow manager with pipeline context."""
        self.pipeline_flow = PipelineDataFlow(
            pipeline_id=pipeline_id,
            execution_id=execution_id,
            context=context,
        )
        self.validator = DataValidator()

    def create_data_packet(
        self, data: PluginData, plugin_id: str, plugin_type: PluginType,
    ) -> DataPacket:
        """Create and validate data packet from plugin output."""
        packet = DataPacket(
            data=data,
            source_plugin_id=plugin_id,
            source_plugin_type=plugin_type,
        )

        # Validate the packet
        validation_errors = self.validator.validate_data_packet(packet)
        for error in validation_errors:
            packet.add_validation_error(error)

        return packet

    def start_step_execution(
        self, step_id: str, plugin_id: str, plugin_type: PluginType,
    ) -> StepResult:
        """Start new step execution and return result tracker."""
        return self.pipeline_flow.start_step(step_id, plugin_id, plugin_type)

    def complete_step_execution(
        self,
        step_result: StepResult,
        output_data: PluginData = None,
        error: str | None = None,
    ) -> None:
        """Complete step execution with result data or error."""
        if output_data is not None and error is None:
            # Create data packet for successful step output
            data_packet = self.create_data_packet(
                output_data,
                step_result.plugin_id,
                step_result.plugin_type,
            )
            self.pipeline_flow.complete_step(step_result, data_packet)
        else:
            # Step failed
            if error:
                step_result.error_message = error
            self.pipeline_flow.complete_step(step_result)

    def get_current_data(self) -> DataPacket | None:
        """Get current data packet in pipeline flow."""
        return self.pipeline_flow.current_data

    def should_continue_execution(self) -> bool:
        """Check if pipeline execution should continue."""
        return self.pipeline_flow.should_continue

    def get_execution_summary(self) -> dict[str, Any]:
        """Get pipeline execution summary from flow manager."""
        return self.pipeline_flow.get_execution_summary()

    def abort_execution(self, reason: str) -> None:
        """Abort pipeline execution with specified reason."""
        self.pipeline_flow.abort_pipeline(reason)


# Export all classes
__all__ = [
    "DataFlowContext",
    "DataFlowManager",
    "DataPacket",
    "DataValidator",
    "PipelineDataFlow",
    "StepResult",
]
