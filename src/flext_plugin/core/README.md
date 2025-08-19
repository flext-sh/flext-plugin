# FLEXT Plugin Core Module

**Core type definitions and foundational patterns for the FLEXT plugin system.**

This module provides the fundamental building blocks that define plugin behavior, categorization, lifecycle management, and execution context throughout the FLEXT ecosystem.

## Module Contents

### Core Types

#### `PluginStatus` Enum

Plugin lifecycle and health status management.

```python
from flext_plugin.core.types import PluginStatus

# Lifecycle progression
status = PluginStatus.DISCOVERED  # Plugin found
status = PluginStatus.LOADED      # Plugin loaded into memory
status = PluginStatus.ACTIVE      # Plugin ready for execution
```

**States:**

- **Lifecycle**: UNKNOWN → DISCOVERED → LOADED → ACTIVE ↔ INACTIVE
- **Error States**: ERROR, DISABLED
- **Health States**: HEALTHY, UNHEALTHY

#### `PluginType` Enum

Comprehensive plugin categorization system.

```python
from flext_plugin.core.types import PluginType

# Singer ecosystem integration
tap_plugin = PluginType.TAP        # Data extraction
target_plugin = PluginType.TARGET  # Data loading
transform_plugin = PluginType.TRANSFORM  # Data transformation

# Architecture integration
service_plugin = PluginType.SERVICE     # Microservice components
api_plugin = PluginType.API            # REST/GraphQL endpoints
db_plugin = PluginType.DATABASE        # Database connectivity
```

**Categories:**

- **Singer ETL**: TAP, TARGET, TRANSFORM (Meltano integration)
- **Architecture**: SERVICE, MIDDLEWARE, EXTENSION
- **Integration**: API, DATABASE, AUTHENTICATION, AUTHORIZATION
- **Utility**: UTILITY, TOOL, HANDLER, PROCESSOR
- **System**: CORE, ADDON, THEME, LANGUAGE

### Error Handling

#### `PluginError` Exception

Base exception for plugin-related errors.

```python
from flext_plugin.core.types import PluginError

try:
    plugin.execute(data)
except PluginError as e:
    logger.error(f"Plugin {e.plugin_name} failed: {e}")
```

**Features:**

- Plugin identification context
- Integration with FlextProcessingError hierarchy
- Detailed error metadata for debugging

### Execution Management

#### `PluginExecutionResult` Class

Comprehensive result container for plugin operations.

```python
from flext_plugin.core.types import PluginExecutionResult

result = PluginExecutionResult(
    success=True,
    data={"processed": 100, "errors": 0},
    plugin_name="data-processor",
    execution_time=0.5
)

if result.success():
    print(f"Processed in {result.execution_time}s")
```

**Attributes:**

- `success`: Execution outcome boolean
- `data`: Result payload (any serializable object)
- `error`: Error message for failures
- `execution_time`: Performance metrics
- `plugin_name`: Plugin identification

#### `PluginExecutionContext` Class

Execution context and metadata container.

```python
from flext_plugin.core.types import PluginExecutionContext

context = PluginExecutionContext(
    plugin_id="data-processor",
    execution_id="exec-001",
    input_data={"batch_size": 1000},
    timeout_seconds=300
)
```

### Discovery Module

#### Plugin Discovery Engine

Core discovery algorithms and scanning logic.

```python
from flext_plugin.core.discovery import PluginDiscovery

discovery = PluginDiscovery()
plugins = discovery.discover_in_directory("./plugins")
```

**Features:**

- Directory scanning and plugin identification
- Metadata extraction and validation
- Integration with plugin registry systems

## Architecture Integration

### Clean Architecture Positioning

The core module sits at the foundation layer of the Clean Architecture:

```
Application Layer → Domain Layer → Core Layer (THIS MODULE) → Foundation
```

**Dependencies:**

- **Inbound**: Used by domain, application, and platform layers
- **Outbound**: Depends only on flext-core foundation patterns

### Design Patterns

#### Type Safety

All types include comprehensive type annotations:

```python
def process_plugin(
    plugin_type: PluginType,
    status: PluginStatus
) -> PluginExecutionResult:
    # Implementation with full type safety
```

#### Error Handling

Follows railway-oriented programming with FlextResult integration:

```python
from flext_core import FlextResult
from flext_plugin.core.types import PluginError

def safe_operation() -> FlextResult[PluginExecutionResult]:
    try:
        result = execute_plugin()
        return FlextResult[None].ok(result)
    except PluginError as e:
        return FlextResult[None].fail(str(e))
```

## Usage Patterns

### Plugin Status Management

```python
from flext_plugin.core.types import PluginStatus

def transition_plugin_state(current: PluginStatus, target: PluginStatus) -> bool:
    """Validate plugin state transitions."""
    valid_transitions = {
        PluginStatus.DISCOVERED: [PluginStatus.LOADED, PluginStatus.ERROR],
        PluginStatus.LOADED: [PluginStatus.ACTIVE, PluginStatus.INACTIVE],
        PluginStatus.ACTIVE: [PluginStatus.INACTIVE, PluginStatus.ERROR],
        PluginStatus.INACTIVE: [PluginStatus.ACTIVE, PluginStatus.DISABLED]
    }
    return target in valid_transitions.get(current, [])
```

### Plugin Type Validation

```python
from flext_plugin.core.types import PluginType

def is_singer_plugin(plugin_type: PluginType) -> bool:
    """Check if plugin type is part of Singer ecosystem."""
    return plugin_type in [
        PluginType.TAP,
        PluginType.TARGET,
        PluginType.TRANSFORM
    ]

def is_integration_plugin(plugin_type: PluginType) -> bool:
    """Check if plugin provides external system integration."""
    return plugin_type in [
        PluginType.API,
        PluginType.DATABASE,
        PluginType.AUTHENTICATION,
        PluginType.AUTHORIZATION
    ]
```

### Result Handling

```python
def handle_execution_result(result: PluginExecutionResult) -> None:
    """Process plugin execution results with comprehensive handling."""
    if result.success():
        logger.info(
            f"Plugin {result.plugin_name} executed successfully",
            execution_time=result.execution_time,
            data_size=len(str(result.data))
        )
    else:
        logger.error(
            f"Plugin {result.plugin_name} failed",
            error=result.error,
            execution_time=result.execution_time
        )
```

## Quality Standards

### Type Annotation Coverage

- **100% type coverage** for all public APIs
- **Strict MyPy compliance** with no type: ignore comments
- **Generic types** where appropriate for flexibility

### Documentation Standards

- **Comprehensive docstrings** for all classes and methods
- **Usage examples** in docstrings and README
- **Architecture context** explaining integration patterns

### Testing Requirements

- **Unit tests** for all type validation logic
- **Integration tests** with domain layer components
- **Performance tests** for execution result handling

## Development Guidelines

### Adding New Types

1. Follow existing naming conventions (PluginXxx pattern)
2. Include comprehensive docstrings with examples
3. Add appropriate type annotations
4. Update this README with new type documentation

### Error Handling Extensions

1. Extend PluginError for specific error categories
2. Include plugin context in all error scenarios
3. Maintain consistency with FlextProcessingError patterns

### Performance Considerations

- Types are lightweight and designed for frequent instantiation
- Execution results support large data payloads efficiently
- Context objects minimize memory overhead

---

**Integration**: This module integrates with all other flext-plugin modules and serves as the foundation for plugin system operations across the FLEXT ecosystem.
