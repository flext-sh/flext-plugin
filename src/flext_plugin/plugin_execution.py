"""FLEXT Plugin Execution Entity - Plugin execution domain entity.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime
from typing import cast

from flext_core import FlextLogger, FlextModels, FlextResult, FlextUtilities
from pydantic import Field


class PluginExecution(FlextModels.Entity):
    """Plugin execution entity for tracking plugin executions."""

    # Pydantic fields
    plugin_name: str = Field(
        default="",
        description="Name of the plugin being executed",
    )
    plugin_id: str = Field(
        default="",
        description="Plugin identifier",
    )
    execution_id: str = Field(
        default="",
        description="Execution identifier",
    )
    start_time: str = Field(
        default_factory=FlextUtilities.Generators.generate_iso_timestamp,
        description="Execution start time",
    )
    end_time: datetime | None = Field(
        default=None,
        description="Execution end time",
    )
    status: str = Field(default="pending", description="Execution status")
    result: object | None = Field(default=None, description="Execution result")
    error: str = Field(default="", description="Execution error message")
    error_message: str | None = Field(
        default=None,
        description="Error message (compatibility)",
    )
    input_data: dict[str, object] = Field(
        default_factory=dict,
        description="Input data for execution",
    )
    output_data: dict[str, object] = Field(
        default_factory=dict,
        description="Output data from execution",
    )
    is_success: bool = Field(
        default=True,
        description="Whether the execution was successful",
    )
    execution_time: float = Field(
        default=0.0,
        description="Execution time in seconds",
    )

    @classmethod
    def create(
        cls,
        *,
        plugin_name: str = "",
        execution_config: dict[str, object] | None = None,
        entity_id: str | None = None,
        **kwargs: object,
    ) -> PluginExecution:
        """Create plugin execution entity with proper validation."""
        final_id = entity_id or FlextUtilities.Generators.generate_entity_id()
        execution_config = execution_config or {}

        # Create instance data with all required fields including base entity fields
        instance_data: dict[str, object] = {
            "id": final_id,
            "version": kwargs.get("version", 1),
            "metadata": kwargs.get("metadata", {}),
            "plugin_name": plugin_name,
            "plugin_id": kwargs.get("plugin_id", plugin_name),
            "execution_id": kwargs.get("execution_id", final_id),
            "start_time": execution_config.get(
                "start_time",
                FlextUtilities.Generators.generate_iso_timestamp(),
            ),
            "end_time": execution_config.get("end_time"),
            "status": execution_config.get("status", "pending"),
            "result": execution_config.get("result"),
            "error": execution_config.get("error", ""),
            "error_message": execution_config.get("error_message"),
            "input_data": kwargs.get("input_data", {}),
            "output_data": execution_config.get("output_data", {}),
        }

        return cls.model_validate(instance_data)

    @property
    def execution_status(self) -> str:
        """Get execution status (compatibility alias)."""
        return self.status

    @property
    def memory_usage_mb(self) -> float:
        """Get memory usage in MB from resource tracking."""
        resource_usage = cast(
            "dict[str, object]",
            self.output_data.get("resource_usage", {}),
        )
        memory_value = resource_usage.get("memory_mb", 0.0)
        if isinstance(memory_value, (int, float)):
            return float(memory_value)
        if isinstance(memory_value, str):
            try:
                return float(memory_value)
            except ValueError as e:
                logger = FlextLogger(__name__)
                logger.exception(
                    f"Invalid memory value '{memory_value}' for plugin execution",
                )
                msg = f"Invalid memory value: {memory_value}"
                raise ValueError(msg) from e
        return 0.0

    @property
    def cpu_time_ms(self) -> float:
        """Get CPU time in milliseconds from resource tracking."""
        resource_usage = cast(
            "dict[str, object]",
            self.output_data.get("resource_usage", {}),
        )
        cpu_value = resource_usage.get("cpu_time_ms", 0.0)
        if isinstance(cpu_value, (int, float)):
            return float(cpu_value)
        if isinstance(cpu_value, str):
            try:
                return float(cpu_value)
            except ValueError as e:
                logger = FlextLogger(__name__)
                logger.exception(
                    f"Invalid CPU time value '{cpu_value}' for plugin execution",
                )
                msg = f"Invalid CPU time value: {cpu_value}"
                raise ValueError(msg) from e
        return 0.0

    @property
    def is_running(self) -> bool:
        """Check if execution is currently running."""
        return self.status == "running"

    @property
    def is_completed(self) -> bool:
        """Check if execution is completed (successful or failed)."""
        return self.status in {"completed", "failed"}

    def mark_started(self) -> None:
        """Mark execution as started."""
        setattr(self, "status", "running")
        setattr(
            self,
            "start_time",
            FlextUtilities.Generators.generate_iso_timestamp(),
        )

    def mark_completed(
        self,
        *,
        success: bool = True,
        error_message: str | None = None,
    ) -> None:
        """Mark execution as completed."""
        setattr(
            self,
            "end_time",
            FlextUtilities.Generators.generate_iso_timestamp(),
        )
        if success:
            setattr(self, "status", "completed")
        else:
            setattr(self, "status", "failed")
            if error_message:
                setattr(self, "error", error_message)
                setattr(self, "error_message", error_message)

    def update_resource_usage(
        self,
        memory_mb: float = 0.0,
        cpu_time_ms: float = 0.0,
    ) -> None:
        """Update resource usage tracking."""
        current_output = dict[str, object](self.output_data)
        current_output.update(
            {
                "resource_usage": {
                    "memory_mb": memory_mb,
                    "cpu_time_ms": cpu_time_ms,
                    "timestamp": str(
                        FlextUtilities.Generators.generate_iso_timestamp(),
                    ),
                },
            },
        )
        setattr(self, "output_data", current_output)

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate domain rules for plugin execution entity."""
        if not self.plugin_name:
            return FlextResult[None].fail("Plugin name is required")
        return FlextResult[None].ok(None)


__all__ = ["PluginExecution"]
