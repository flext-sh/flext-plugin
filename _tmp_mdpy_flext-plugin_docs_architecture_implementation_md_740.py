# from flext-plugin_docs/architecture/implementation.md:740
# Railway pattern for complex operations
from __future__ import annotations


async def complex_operation(
    self, input_data: FlextPluginTypes.ComplexInput
) -> p.Result[FlextPluginTypes.ComplexOutput]:
    """Complex operation using railway pattern."""
    return (
        self
        ._validate_input(input_data)
        .flat_map(lambda data: self._enrich_data(data))
        .flat_map(lambda data: self._process_data(data))
        .flat_map(lambda data: self._validate_output(data))
        .map(lambda data: self._format_output(data))
        .map_error(lambda error: self._handle_error(error, input_data))
    )


def _handle_error(self, error: str, input_data: FlextPluginTypes.ComplexInput) -> str:
    """Centralized error handling and logging."""
    self.logger.error(f"Complex operation failed for input {input_data.id}: {error}")

    # Add context-specific error handling
    if "validation" in error.lower():
        return f"Input validation failed: {error}"
    if "processing" in error.lower():
        return f"Data processing failed: {error}"
    return f"Operation failed: {error}"```
### Configuration Management

#### **Pydantic Configuration Pattern**

