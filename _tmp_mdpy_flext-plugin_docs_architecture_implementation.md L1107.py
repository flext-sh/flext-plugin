# from flext-plugin/docs/architecture/implementation.md:1107
# flext_plugin/executor.py
from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from flext_plugin import FlextPluginModels


class FlextPluginExecutor:
    """Asynchronous plugin execution with concurrency control."""

    def __init__(self, max_concurrent: int = 10, thread_pool_size: int = 4):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.executor = ThreadPoolExecutor(max_workers=thread_pool_size)

    async def execute_plugins_concurrent(
        self, plugins: list[FlextPluginModels.Plugin], context: dict[str, t.JsonValue]
    ) -> p.Result[list[FlextPluginModels.Execution]]:
        """Execute multiple plugins concurrently with resource limits."""

        async def execute_single_plugin(plugin: FlextPluginModels.Plugin):
            async with self.semaphore:  # Limit concurrency
                return await self._execute_plugin_safe(plugin, context)

        # Execute all plugins concurrently
        tasks = [execute_single_plugin(plugin) for plugin in plugins]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        executions = []
        errors = []

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                errors.append(f"Plugin {plugins[i].name}: {result}")
            elif result.failure:
                errors.append(f"Plugin {plugins[i].name}: {result.error}")
            else:
                executions.append(result.unwrap())

        if errors:
            return r.fail(f"Execution errors: {errors}")

        return r.ok(executions)

    async def _execute_plugin_safe(
        self, plugin: FlextPluginModels.Plugin, context: dict[str, t.JsonValue]
    ) -> p.Result[FlextPluginModels.Execution]:
        """Execute single plugin with error isolation."""
        try:
            # Create execution entity
            execution = FlextPluginModels.Execution.create(
                plugin_name=plugin.name, context=context
            )

            execution.mark_started()

            # Execute in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor, self._execute_plugin_sync, plugin, context
            )

            execution.mark_completed(result)
            return r.ok(execution)

        except Exception as e:
            execution = FlextPluginModels.Execution.create(
                plugin_name=plugin.name, context=context
            )
            execution.mark_failed(str(e))
            return r.ok(execution)  # Return failed execution, not error

    def _execute_plugin_sync(
        self, plugin: FlextPluginModels.Plugin, context: dict[str, t.JsonValue]
    ):
        """Synchronous plugin execution (runs in thread pool)."""
        # Actual plugin execution logic
        # This would integrate with the plugin loading system
        return {"status": "completed", "result": "mock result"}```
______________________________________________________________________

## 🎯 Implementation Best Practices

### Code Quality Standards

#### **Type Safety First**

- Use Python 3.13+ advanced typing features
- 100% type coverage for all public APIs
- Pydantic models for data validation
- Protocol-based dependency injection

#### **Error Handling Patterns**

- Railway pattern (r[T]) throughout
- Structured error messages with context
- Comprehensive exception logging
- Graceful degradation for non-critical failures

#### **Testing Standards**

- Unit tests for domain logic and utilities
- Integration tests for component interactions
- End-to-end tests for complete workflows
- 90%+ coverage target with quality assertions

### Performance Optimization

#### **Caching Strategy**

- Multi-level caching (memory + file + database)
- TTL-based expiration with configurable policies
- Cache invalidation on data changes
- Performance monitoring and metrics

#### **Resource Management**

- Connection pooling for external services
- Resource limits per plugin execution
- Automatic cleanup of temporary resources
- Memory usage monitoring and alerts

### Security Implementation

#### **Defense in Depth**

- Input validation at all entry points
- Sandboxing for plugin execution
- Audit logging for all operations
- Access control with role-based permissions

#### **Secure Coding Practices**

- No dynamic code execution without validation
- Secure deserialization practices
- Cryptographic verification of plugin integrity
- Safe file operations with path validation

______________________________________________________________________

**Implementation Guide** - Comprehensive development patterns, architectural practices, and workflow guidance for FLEXT Plugin system implementation.
