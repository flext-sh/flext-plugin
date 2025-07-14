"""Enhanced Pipeline Executor with Real Plugin Integration.

This module provides a pipeline executor that can execute real plugins
with actual data flow, replacing the simulation-based approach with working plugin execution.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from flext_plugin.data_flow import DataFlowContext, DataFlowManager
from flext_plugin.types import (
    PluginContext,
    PluginData,
    PluginError,
    PluginResult,
    PluginType,
)

if TYPE_CHECKING:
    from flext_plugin.base import PluginInterface
    from flext_plugin.manager import PluginManager


class PipelineStep:
    """Represents a single step in a pipeline."""

    def __init__(
        self,
        step_id: str,
        plugin_id: str,
        step_type: PluginType,
        configuration: dict[str, Any] | None = None,
        dependencies: list[str] | None = None,
    ) -> None:
        """Initialize pipeline step with configuration and dependencies."""
        self.step_id = step_id
        self.plugin_id = plugin_id
        self.step_type = step_type
        self.configuration = configuration or {}
        self.dependencies = dependencies or []


class Pipeline:
    """Represents a complete data pipeline."""

    def __init__(
        self,
        pipeline_id: str,
        name: str,
        steps: list[PipelineStep],
        configuration: dict[str, Any] | None = None,
    ) -> None:
        """Initialize pipeline with steps and configuration."""
        self.pipeline_id = pipeline_id
        self.name = name
        self.steps = steps
        self.configuration = configuration or {}

        # Validate step dependencies
        self._validate_dependencies()

    def _validate_dependencies(self) -> None:
        step_ids = {step.step_id for step in self.steps}

        for step in self.steps:
            for dep_id in step.dependencies:
                if dep_id not in step_ids:
                    msg = f"Step {step.step_id} depends on non-existent step {dep_id}"
                    raise ValueError(msg)


class RealPluginPipelineExecutor:
    """Pipeline executor that uses real plugins for data processing.

    This executor integrates with the plugin manager to load and execute actual plugins, managing data flow between steps and handling errors.
    """

    def __init__(self, plugin_manager: PluginManager) -> None:
        """Initialize pipeline executor with plugin manager."""
        self.plugin_manager = plugin_manager
        self._active_executions: dict[str, DataFlowManager] = {}

    async def execute_pipeline(
        self,
        pipeline: Pipeline,
        user_id: str | None = None,
        environment: str = "development",
        global_variables: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Execute complete pipeline with context and error handling."""
        execution_id = str(uuid.uuid4())

        # Create execution context
        context = DataFlowContext(
            pipeline_id=pipeline.pipeline_id,
            execution_id=execution_id,
            step_id="",  # Will be updated for each step
            user_id=user_id,
            environment=environment,
            pipeline_config=pipeline.configuration,
            global_variables=global_variables or {},
        )

        # Initialize data flow manager
        flow_manager = DataFlowManager(pipeline.pipeline_id, execution_id, context)
        flow_manager.pipeline_flow.total_steps = len(pipeline.steps)
        self._active_executions[execution_id] = flow_manager

        try:
            # Execute steps in order
            for step in pipeline.steps:
                if not flow_manager.should_continue_execution():
                    break

                # Wait for step dependencies
                await self._wait_for_dependencies(step, flow_manager)

                # Execute the step
                await self._execute_step(step, flow_manager)

            # Get final results
            execution_summary = flow_manager.get_execution_summary()
            final_data = flow_manager.get_current_data()

            return {
                "execution_id": execution_id,
                "pipeline_id": pipeline.pipeline_id,
                "success": flow_manager.should_continue_execution()
                and flow_manager.pipeline_flow.failed_steps == 0,
                "execution_summary": execution_summary,
                "final_data": final_data.get_data_summary() if final_data else None,
                "output_data": final_data.data if final_data else None,
                "completed_at": datetime.now(UTC).isoformat(),
            }

        except (PluginError, RuntimeError, ValueError, AttributeError, TypeError) as e:
            # Handle execution errors
            flow_manager.abort_execution(f"Pipeline execution failed: {e}")

            return {
                "execution_id": execution_id,
                "pipeline_id": pipeline.pipeline_id,
                "success": False,
                "error": str(e),
                "execution_summary": flow_manager.get_execution_summary(),
                "completed_at": datetime.now(UTC).isoformat(),
            }

        finally:
            # Cleanup
            self._active_executions.pop(execution_id, None)

    async def _execute_step(
        self,
        step: PipelineStep,
        flow_manager: DataFlowManager,
    ) -> None:
        # Start step execution
        step_result = flow_manager.start_step_execution(
            step.step_id,
            step.plugin_id,
            step.step_type,
        )

        try:
            # Get plugin instance from manager
            plugin = await self._get_plugin_instance(step.plugin_id)
            if not plugin:
                msg = f"Plugin {step.plugin_id} not found or not loaded"
                raise PluginError(
                    msg,
                    plugin_id=step.plugin_id,
                    error_code="PLUGIN_NOT_FOUND",
                )

            # Prepare input data and context
            input_data = self._prepare_step_input(step, flow_manager)
            execution_context = self._prepare_execution_context(step, flow_manager)

            # Execute plugin based on type
            if step.step_type == PluginType.EXTRACTOR:
                output = await self._execute_extractor(plugin, step, execution_context)
            elif step.step_type == PluginType.TRANSFORMER:
                output = await self._execute_transformer(
                    plugin,
                    step,
                    input_data,
                    execution_context,
                )
            elif step.step_type == PluginType.LOADER:
                output = await self._execute_loader(
                    plugin,
                    step,
                    input_data,
                    execution_context,
                )
            else:
                msg = f"Unsupported plugin type: {step.step_type}"
                raise PluginError(
                    msg,
                    plugin_id=step.plugin_id,
                    error_code="UNSUPPORTED_PLUGIN_TYPE",
                )

            # Complete step successfully
            flow_manager.complete_step_execution(step_result, output)

        except Exception as e:
            # Complete step with error
            error_message = f"Step {step.step_id} failed: {e}"
            flow_manager.complete_step_execution(step_result, error=error_message)
            raise

    async def _execute_extractor(
        self,
        plugin: PluginInterface,
        step: PipelineStep,
        context: PluginContext,
    ) -> PluginResult:
        # Extractors don't take input data, they generate data from sources
        source_config = step.configuration.copy()
        source_config.update(context.get("source_config", {}))

        if hasattr(plugin, "extract"):
            # Use specialized extractor method
            return await plugin.extract(source_config)
        # Fall back to generic execute method
        return await plugin.execute(None, {"source_config": source_config, **context})

    async def _execute_transformer(
        self,
        plugin: PluginInterface,
        step: PipelineStep,
        input_data: PluginData,
        context: PluginContext,
    ) -> PluginResult:
        transform_config = step.configuration.copy()
        transform_config.update(context.get("transform_config", {}))

        if hasattr(plugin, "transform"):
            # Use specialized transformer method
            return await plugin.transform(input_data, transform_config)
        # Fall back to generic execute method
        return await plugin.execute(
            input_data,
            {"transform_config": transform_config, **context},
        )

    async def _execute_loader(
        self,
        plugin: PluginInterface,
        step: PipelineStep,
        input_data: PluginData,
        context: PluginContext,
    ) -> PluginResult:
        destination_config = step.configuration.copy()
        destination_config.update(context.get("destination_config", {}))

        if hasattr(plugin, "load"):
            # Use specialized loader method
            return await plugin.load(input_data, destination_config)
        # Fall back to generic execute method
        return await plugin.execute(
            input_data,
            {"destination_config": destination_config, **context},
        )

    async def _get_plugin_instance(self, plugin_id: str) -> PluginInterface | None:
        # This would integrate with the actual plugin manager's registry
        # For now, returning None to indicate plugin loading needs to be implemented
        return self.plugin_manager.registry.get_plugin(plugin_id)

    def _prepare_step_input(
        self,
        step: PipelineStep,
        flow_manager: DataFlowManager,
    ) -> PluginData:
        current_data = flow_manager.get_current_data()

        if current_data is None:
            # First step (extractor) - no input data
            return None

        # Return the actual data payload
        return current_data.data

    def _prepare_execution_context(
        self,
        step: PipelineStep,
        flow_manager: DataFlowManager,
    ) -> dict[str, Any]:
        context = flow_manager.pipeline_flow.context

        # Update context for current step
        context.model_copy(
            update={"step_id": step.step_id, "step_config": step.configuration},
        )

        return {
            "execution_id": context.execution_id,
            "pipeline_id": context.pipeline_id,
            "step_id": step.step_id,
            "user_id": context.user_id,
            "environment": context.environment,
            "global_variables": context.global_variables,
            "step_config": step.configuration,
            "execution_time": datetime.now(UTC).isoformat(),
        }

    async def _wait_for_dependencies(
        self,
        step: PipelineStep,
        flow_manager: DataFlowManager,
    ) -> None:
        # In this simple implementation, we execute steps sequentially
        # In a more advanced implementation, you could run independent steps in parallel

        for dep_step_id in step.dependencies:
            dep_step = flow_manager.pipeline_flow.get_step_by_id(dep_step_id)
            if not dep_step or not dep_step.success:
                msg = f"Dependency step {dep_step_id} not completed successfully"
                raise PluginError(
                    msg,
                    plugin_id=step.plugin_id,
                    error_code="DEPENDENCY_FAILED",
                )

    def get_execution_status(self, execution_id: str) -> dict[str, Any] | None:
        """Get status of active execution by ID."""
        flow_manager = self._active_executions.get(execution_id)
        if flow_manager:
            return flow_manager.get_execution_summary()
        return None

    def list_active_executions(self) -> list[str]:
        """List IDs of all active executions."""
        return list(self._active_executions.keys())

    async def cancel_execution(self, execution_id: str) -> bool:
        """Cancel active execution by ID."""
        flow_manager = self._active_executions.get(execution_id)
        if flow_manager:
            flow_manager.abort_execution("Execution cancelled by user")
            return True
        return False


# Factory function for creating pipeline executor
def create_pipeline_executor(
    plugin_manager: PluginManager,
) -> RealPluginPipelineExecutor:
    """Factory function to create pipeline executor with plugin manager."""
    return RealPluginPipelineExecutor(plugin_manager)


# Export all classes
__all__ = [
    "Pipeline",
    "PipelineStep",
    "RealPluginPipelineExecutor",
    "create_pipeline_executor",
]
