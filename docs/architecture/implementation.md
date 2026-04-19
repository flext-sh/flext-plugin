# Implementation Guide

<!-- TOC START -->
- [🛠️ Implementation Overview](#implementation-overview)
  - [Implementation Philosophy](#implementation-philosophy)
- [🏗️ Architecture Implementation Patterns](#architecture-implementation-patterns)
  - [Clean Architecture Layer Implementation](#clean-architecture-layer-implementation)
  - [Protocol-Based Architecture Implementation](#protocol-based-architecture-implementation)
  - [Railway Pattern Implementation](#railway-pattern-implementation)
- [🧪 Testing Implementation Patterns](#testing-implementation-patterns)
  - [Unit Testing Patterns](#unit-testing-patterns)
  - [Integration Testing Patterns](#integration-testing-patterns)
- [🔧 Development Workflow Implementation](#development-workflow-implementation)
  - [Code Organization Patterns](#code-organization-patterns)
  - [Error Handling Patterns](#error-handling-patterns)
  - [Configuration Management](#configuration-management)
- [🚀 Deployment and Operations](#deployment-and-operations)
  - [Container Configuration](#container-configuration)
  - [Monitoring and Observability](#monitoring-and-observability)
- [📊 Performance Optimization Implementation](#performance-optimization-implementation)
  - [Caching Strategies](#caching-strategies)
  - [Asynchronous Processing](#asynchronous-processing)
- [🎯 Implementation Best Practices](#implementation-best-practices)
  - [Code Quality Standards](#code-quality-standards)
  - [Performance Optimization](#performance-optimization)
  - [Security Implementation](#security-implementation)
<!-- TOC END -->

**Development Patterns, Practices, and Workflow** | **Version**: 0.9.0 | **Last Updated**: October 2025

______________________________________________________________________

## 🛠️ Implementation Overview

This guide provides practical implementation guidance for developing with the FLEXT Plugin system. It covers architectural patterns, development practices, and workflow recommendations based on the established Clean Architecture foundation.

### Implementation Philosophy

- **Clean Architecture First**: Domain-driven design with clear layer boundaries
- **Type Safety**: 100% type annotations with Python 3.13+ features
- **Railway Pattern**: p.Result[T] for composable error handling
- **Single Responsibility**: One class per module following FLEXT standards
- **Test-Driven Development**: Comprehensive testing with high coverage targets

______________________________________________________________________

## 🏗️ Architecture Implementation Patterns

### Clean Architecture Layer Implementation

#### **Domain Layer Implementation**

```python
# flext_plugin/entities.py - Domain entities with business rules
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r, p
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u
from typing import List, Optional


class FlextPluginModels:
    """Domain entities following FLEXT single-class-per-module pattern."""

    class Plugin(FlextModels.Entity):
        """Plugin domain entity with business rules."""

        def __init__(
            self,
            name: str,
            plugin_version: str,
            settings: m.Dict,
        ) -> None:
            super().__init__()
            self.name = name
            self.plugin_version = plugin_version
            self.settings = settings
            self._status = PluginStatus.INACTIVE

        def validate_business_rules(self) -> p.Result[bool]:
            """Domain business rule validation."""
            if not self.name or not self.name.strip():
                return r.fail("Plugin name cannot be empty")

            if not self.plugin_version:
                return r.fail("Plugin version is required")

            # Additional business rules...
            return r.ok(True)

        def activate(self) -> p.Result[bool]:
            """Business logic for plugin activation."""
            validation = self.validate_business_rules()
            if validation.failure:
                return validation

            self._status = PluginStatus.ACTIVE
            return r.ok(True)

    class Execution(FlextModels.Entity):
        """Plugin execution entity."""

        def __init__(
            self,
            plugin_name: str,
            context: m.Dict,
            execution_id: Optional[str] = None,
        ) -> None:
            super().__init__()
            self.plugin_name = plugin_name
            self.context = context
            self.execution_id = execution_id or self._generate_id()
            self._status = ExecutionStatus.PENDING
            self._start_time: Optional[datetime] = None
            self._end_time: Optional[datetime] = None

        def mark_started(self) -> None:
            """Mark execution as started."""
            self._start_time = datetime.now(UTC)
            self._status = ExecutionStatus.RUNNING

        def mark_completed(self, result) -> None:
            """Mark execution as completed."""
            self._end_time = datetime.now(UTC)
            self._status = ExecutionStatus.COMPLETED
            self.result = result
```

#### **Application Layer Implementation**

```python
# flext_plugin/services.py - Application services
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r, p
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u
from flext_plugin import FlextPluginModels
from typing import List, Protocol


class FlextPluginServices:
    """Application services following Clean Architecture."""

    def __init__(self, container: FlextContainer) -> None:
        self.container = container

    async def discover_plugins(
        self, paths: t.StringList, discovery_service: PluginDiscovery
    ) -> p.Result[List[FlextPluginModels.Plugin]]:
        """Application service orchestrating plugin discovery."""

        try:
            # Use domain service (infrastructure adapter)
            discovery_result = await discovery_service.discover_plugins(paths)
            if discovery_result.failure:
                return discovery_result

            plugin_configs = discovery_result.unwrap()
            plugins = []

            for settings in plugin_configs:
                # Create domain entity
                plugin = FlextPluginModels.Plugin.create(
                    name=settings["name"],
                    plugin_version=settings.get("version", "1.0.0"),
                    settings=settings,
                )

                # Validate business rules
                validation = plugin.validate_business_rules()
                if validation.success:
                    plugins.append(plugin)
                else:
                    # Log validation failure but continue
                    self.logger.warning(
                        f"Plugin {plugin.name} validation failed: {validation.error}"
                    )

            return r.ok(plugins)

        except Exception as e:
            return r.fail(f"Plugin discovery failed: {e!s}")

    async def execute_plugin(
        self,
        plugin: FlextPluginModels.Plugin,
        context: m.Dict,
        executor: PluginExecution,
    ) -> p.Result[FlextPluginModels.Execution]:
        """Application service orchestrating plugin execution."""

        try:
            # Create execution entity
            execution = FlextPluginModels.Execution.create(
                plugin_name=plugin.name, context=context
            )

            # Mark as started
            execution.mark_started()

            # Execute via infrastructure
            execution_result = await executor.execute_plugin(plugin, context)
            if execution_result.success:
                execution.mark_completed(execution_result.unwrap())
            else:
                execution.mark_failed(execution_result.error)

            return r.ok(execution)

        except Exception as e:
            return r.fail(f"Plugin execution failed: {e!s}")
```

#### **Infrastructure Layer Implementation**

```python
# flext_plugin/discovery.py - Infrastructure adapters
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r, p
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u
from flext_plugin import FlextPluginProtocols
import os
from pathlib import Path
from typing import List, Dict, t.Container



class FlextPluginDiscovery:
    """Infrastructure adapter for file-based plugin discovery."""

    def __init__(self, container: FlextContainer) -> None:
        self.container = container
        self.logger = container.resolve("logger").unwrap()

    async def discover_plugins(self, paths: t.StringList) -> p.Result[List[Dict[str, t.Container]]]:
        """Discover plugins from file system."""

        try:
            discovered_plugins = []

            for path_str in paths:
                path = Path(path_str)

                if not path.exists():
                    self.logger.warning(f"Plugin path does not exist: {path}")
                    continue

                # Scan for plugin files
                plugin_files = self._scan_plugin_files(path)
                self.logger.info(f"Found {len(plugin_files)} plugin files in {path}")

                for plugin_file in plugin_files:
                    try:
                        plugin_config = self._parse_plugin_file(plugin_file)
                        if plugin_config:
                            discovered_plugins.append(plugin_config)
                    except Exception as e:
                        self.logger.error(
                            f"Failed to parse plugin file {plugin_file}: {e}"
                        )
                        continue

            self.logger.info(f"Discovered {len(discovered_plugins)} plugins")
            return r.ok(discovered_plugins)

        except Exception as e:
            self.logger.exception("Plugin discovery failed")
            return r.fail(f"Discovery error: {e!s}")

    def _scan_plugin_files(self, path: Path) -> List[Path]:
        """Scan directory for plugin files."""
        plugin_files = []

        if path.is_file():
            if self._is_plugin_file(path):
                plugin_files.append(path)
        else:
            # Recursive scan
            for file_path in path.rglob("*"):
                if file_path.is_file() and self._is_plugin_file(file_path):
                    plugin_files.append(file_path)

        return plugin_files

    def _is_plugin_file(self, file_path: Path) -> bool:
        """Check if file is a valid plugin file."""
        if file_path.suffix.lower() not in [".py", ".json", ".yaml", ".yml"]:
            return False

        # Additional validation logic...
        return True

    def _parse_plugin_file(self, file_path: Path) -> Optional[Dict[str, t.Container]]:
        """Parse plugin configuration from file."""
        try:
            if file_path.suffix.lower() == ".py":
                return self._parse_python_plugin(file_path)
            elif file_path.suffix.lower() in [".json"]:
                return self._parse_json_plugin(file_path)
            elif file_path.suffix.lower() in [".yaml", ".yml"]:
                return self._parse_yaml_plugin(file_path)
        except Exception as e:
            self.logger.error(f"Failed to parse {file_path}: {e}")

        return None
```

### Protocol-Based Architecture Implementation

#### **Protocol Definitions**

```python
# flext_plugin/protocols.py - Structural typing protocols
from typing import Protocol, List, Dict, t.Container, Optional
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r, p
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u
from flext_plugin import FlextPluginModels



class FlextPluginProtocols:
    """Protocol definitions for plugin system interfaces."""

    class PluginDiscovery(Protocol):
        """Protocol for plugin discovery mechanisms."""

        async def discover_plugins(
            self, paths: t.StringList
        ) -> p.Result[List[Dict[str, t.Container]]]:
            """Discover plugins from specified paths."""
            ...

    class PluginLoader(Protocol):
        """Protocol for plugin loading mechanisms."""

        async def load_plugin(self, plugin_path: str) -> p.Result[FlextPluginModels.Plugin]:
            """Load plugin from specified path."""
            ...

    class PluginExecution(Protocol):
        """Protocol for plugin execution mechanisms."""

        async def execute_plugin(
            self, plugin: FlextPluginModels.Plugin, context: Dict[str, t.Container]
        ) -> p.Result[t.Container]:
            """Execute plugin with given context."""
            ...

    class PluginSecurity(Protocol):
        """Protocol for plugin security validation."""

        async def validate_plugin(self, plugin: FlextPluginModels.Plugin) -> p.Result[bool]:
            """Validate plugin security."""
            ...

    class PluginHotReload(Protocol):
        """Protocol for plugin hot reload functionality."""

        async def start_watching(self, paths: t.StringList) -> p.Result[bool]:
            """Start watching paths for plugin changes."""
            ...

        async def stop_watching(self) -> p.Result[bool]:
            """Stop watching for plugin changes."""
            ...
```

#### **Protocol Implementation**

```python
# Example protocol implementation
from flext_plugin import FlextPluginProtocols


class FilePluginDiscovery(FlextPluginProtocols.PluginDiscovery):
    """Concrete implementation of plugin discovery protocol."""

    async def discover_plugins(
        self, paths: t.StringList
    ) -> p.Result[List[Dict[str, t.Container]]]:
        """File-based plugin discovery implementation."""
        # Implementation details...
        return r.ok([])
```

### Railway Pattern Implementation

#### **r[T] Error Handling**

```python
# Railway pattern throughout the system
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r, p
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u
from typing import List


async def process_plugins_workflow(
    self, plugin_names: t.StringList
) -> p.Result[t.List]:
    """Complete plugin processing workflow using railway pattern."""

    # Chain operations with automatic error propagation
    return (
        self
        ._validate_plugin_names(plugin_names)
        .flat_map(lambda names: self._load_plugins(names))
        .flat_map(lambda plugins: self._validate_plugins(plugins))
        .flat_map(lambda plugins: self._execute_plugins(plugins))
        .map(lambda results: self._format_results(results))
    )


def _validate_plugin_names(self, names: t.StringList) -> p.Result[t.StringList]:
    """Validate plugin names."""
    if not names:
        return r.fail("No plugin names provided")

    invalid_names = [name for name in names if not self._is_valid_name(name)]
    if invalid_names:
        return r.fail(f"Invalid plugin names: {invalid_names}")

    return r.ok(names)


async def _load_plugins(
    self, names: t.StringList
) -> p.Result[List[FlextPluginModels.Plugin]]:
    """Load plugins by name."""
    plugins = []
    for name in names:
        plugin_result = await self._load_single_plugin(name)
        if plugin_result.failure:
            return plugin_result  # Early return on failure
        plugins.append(plugin_result.unwrap())

    return r.ok(plugins)
```

______________________________________________________________________

## 🧪 Testing Implementation Patterns

### Unit Testing Patterns

#### **Domain Entity Testing**

```python
# tests/unit/test_entities.py
import pytest
from flext_plugin import FlextPluginModels


class TestPluginEntity:
    """Test plugin domain entity business rules."""

    def test_plugin_creation_success(self):
        """Test successful plugin creation."""
        plugin = FlextPluginModels.Plugin.create(
            name="test-plugin", plugin_version="1.0.0", settings={"type": "extension"}
        )

        assert plugin.name == "test-plugin"
        assert plugin.plugin_version == "1.0.0"
        assert plugin.status == PluginStatus.INACTIVE

    def test_plugin_validation_business_rules(self):
        """Test plugin business rule validation."""
        # Valid plugin
        plugin = FlextPluginModels.Plugin.create(
            name="valid-plugin", plugin_version="1.0.0", settings={}
        )
        result = plugin.validate_business_rules()
        assert result.success

        # Invalid plugin (empty name)
        plugin = FlextPluginModels.Plugin.create(
            name="", plugin_version="1.0.0", settings={}
        )
        result = plugin.validate_business_rules()
        assert result.failure
        assert "name cannot be empty" in result.error

    def test_plugin_activation_workflow(self):
        """Test plugin activation business workflow."""
        plugin = FlextPluginModels.Plugin.create(
            name="test-plugin", plugin_version="1.0.0", settings={"type": "extension"}
        )

        # Should fail validation initially
        result = plugin.validate_business_rules()
        assert result.failure

        # Fix configuration and activate
        plugin.settings = {"type": "extension", "author": "test"}
        result = plugin.validate_business_rules()
        assert result.success

        activation_result = plugin.activate()
        assert activation_result.success
        assert plugin.status == PluginStatus.ACTIVE
```

#### **Application Service Testing**

```python
# tests/unit/test_services.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from flext_plugin import FlextPluginServices


class TestPluginServices:
    """Test application services."""

    @pytest.fixture
    def mock_container(self):
        """Mock dependency injection container."""
        container = MagicMock()
        container.get.return_value = MagicMock()
        return container

    @pytest.fixture
    def plugin_service(self, mock_container):
        """Plugin service instance."""
        return FlextPluginServices(mock_container)

    @pytest.mark.asyncio
    async def test_discover_plugins_success(self, plugin_service):
        """Test successful plugin discovery."""
        # Mock discovery protocol
        mock_discovery = AsyncMock()
        mock_discovery.discover_plugins.return_value = r.ok([
            {
                "name": "test-plugin",
                "version": "1.0.0",
                "type": "extension",
                "author": "test",
            }
        ])

        # Execute service method
        result = await plugin_service.discover_plugins(["/plugins"], mock_discovery)

        # Verify results
        assert result.success
        plugins = result.unwrap()
        assert len(plugins) == 1
        assert plugins[0].name == "test-plugin"
        assert plugins[0].plugin_version == "1.0.0"

    @pytest.mark.asyncio
    async def test_discover_plugins_validation_failure(self, plugin_service):
        """Test plugin discovery with validation failure."""
        # Mock discovery returning invalid plugin
        mock_discovery = AsyncMock()
        mock_discovery.discover_plugins.return_value = r.ok([
            {
                "name": "",  # Invalid: empty name
                "version": "1.0.0",
            }
        ])

        result = await plugin_service.discover_plugins(["/plugins"], mock_discovery)

        # Should succeed but with empty list (invalid plugin filtered out)
        assert result.success
        plugins = result.unwrap()
        assert len(plugins) == 0
```

### Integration Testing Patterns

#### **End-to-End Plugin Lifecycle Testing**

```python
# tests/integration/test_plugin_lifecycle.py
import pytest
from pathlib import Path
import tempfile
from flext_plugin import FlextPluginPlatform
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r, p
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u


class TestPluginLifecycle:
    """End-to-end plugin lifecycle testing."""

    @pytest.fixture
    async def platform(self):
        """Real plugin platform instance."""
        container = FlextContainer()
        platform = FlextPluginPlatform(container)
        yield platform
        # Cleanup if needed

    @pytest.fixture
    def temp_plugin_dir(self, tmp_path):
        """Temporary directory with test plugin."""
        plugin_dir = tmp_path / "plugins"
        plugin_dir.mkdir()

        # Create test plugin file
        plugin_file = plugin_dir / "test_plugin.py"
        plugin_file.write_text("""
from flext_plugin import FlextPluginModels

def create_plugin():
    return FlextPluginModels.Plugin.create(
        name="test-plugin",
        plugin_version="1.0.0",
        settings={
            "type": "extension",
            "author": "test",
            "description": "Test plugin"
        }
    )
""")

        return plugin_dir

    @pytest.mark.asyncio
    async def test_complete_plugin_lifecycle(self, platform, temp_plugin_dir):
        """Test complete plugin lifecycle from discovery to execution."""
        # 1. Discover plugins
        discovery_result = await platform.discover_plugins([str(temp_plugin_dir)])
        assert discovery_result.success

        plugins = discovery_result.unwrap()
        assert len(plugins) == 1

        plugin = plugins[0]
        assert plugin.name == "test-plugin"

        # 2. Load plugin
        load_result = await platform.load_plugin(
            str(temp_plugin_dir / "test_plugin.py")
        )
        assert load_result.success

        loaded_plugin = load_result.unwrap()
        assert loaded_plugin.name == "test-plugin"

        # 3. Register plugin
        register_result = await platform.register_plugin(loaded_plugin)
        assert register_result.success

        # 4. Execute plugin
        context = {"input": "test data", "operation": "test"}
        execution_result = await platform.execute_plugin(
            "test-plugin", context, execution_id="test-execution-123"
        )

        # Execution might fail for test plugin, but should return proper result
        assert execution_result.success or execution_result.failure
        # (Actual execution depends on plugin implementation)

        # 5. Verify execution history
        executions = platform.list_executions()
        assert len(executions) >= 1

        # 6. Unregister plugin
        unregister_result = await platform.unregister_plugin("test-plugin")
        assert unregister_result.success
```

______________________________________________________________________

## 🔧 Development Workflow Implementation

### Code Organization Patterns

#### **Module Structure Template**

```python
# Template for FLEXT single-class-per-module pattern
"""
Module: flext_plugin/[module_name].py

Description: [Brief module description]

Author: FLEXT Team
License: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from flext_core import FlextBus

from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r, p
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u

# Standard imports
from typing import TYPE_CHECKING

# FLEXT ecosystem imports
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r, p
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u

# Local imports (after FLEXT imports)
from flext_plugin import FlextPluginConstants
from flext_plugin import FlextPluginTypes

# Type checking imports
if TYPE_CHECKING:
    from flext_plugin import FlextPluginModels


class FlextPlugin[ModuleName]:
    """Single main class following FLEXT naming convention.

    This class encapsulates all functionality for [module responsibility].
    Nested helper classes are used for complex internal structures.
    """

    def __init__(self, container: FlextContainer) -> None:
        """Initialize module with dependency injection."""
        self.container = container
        self.logger = container.resolve("logger").unwrap()
        self.settings = container.resolve("settings").unwrap()

    # Public API methods
    async def public_method(
        self, param: FlextPluginTypes.SomeType
    ) -> p.Result[FlextPluginModels.SomeEntity]:
        """Public method with comprehensive documentation."""
        try:
            # Validation
            validation = self._validate_param(param)
            if validation.failure:
                return validation

            # Business logic
            result = await self._execute_business_logic(param)

            # Return result
            return r.ok(result)

        except Exception as e:
            self.logger.exception(f"Method execution failed: {param}")
            return r.fail(f"Execution error: {e!s}")

    # Private helper methods
    def _validate_param(
        self, param: FlextPluginTypes.SomeType
    ) -> p.Result[FlextPluginTypes.SomeType]:
        """Validate method parameters."""
        if not param:
            return r.fail("Parameter cannot be empty")

        # Additional validation logic...
        return r.ok(param)

    async def _execute_business_logic(
        self, param: FlextPluginTypes.SomeType
    ) -> FlextPluginModels.SomeEntity:
        """Execute core business logic."""
        # Implementation details...
        pass

    # Nested helper classes for complex structures
    class HelperClass:
        """Nested helper class for internal complexity."""

        def helper_method(self) -> p.Result[str]:
            """Helper method implementation."""
            return r.ok("helper result")


# Module constants (if needed)
DEFAULT_TIMEOUT: int = 30
MAX_RETRIES: int = 3

# Export main class
__all__: list[str] = ["FlextPlugin[ModuleName]"]
```

### Error Handling Patterns

#### **Railway Pattern Throughout**

```python
# Railway pattern for complex operations
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
    elif "processing" in error.lower():
        return f"Data processing failed: {error}"
    else:
        return f"Operation failed: {error}"
```

### Configuration Management

#### **Pydantic Configuration Pattern**

```python
# flext_plugin/settings.py
from pydantic import BaseModel, u.Field, validator
from typing import List, Optional
from flext_plugin import FlextPluginConstants


class FlextPluginSettings:
    """Plugin system configuration using Pydantic."""

    # Plugin discovery settings
    plugin_paths: t.StringList = u.Field(
        default_factory=lambda: ["./plugins", "~/.flext/plugins", "/opt/flext/plugins"]
    )

    # Security settings
    security_level: str = u.Field(default="HIGH", regex="^(LOW|MEDIUM|HIGH)$")

    enable_plugin_validation: bool = u.Field(default=True)
    enable_sandboxing: bool = u.Field(default=True)

    # Performance settings
    max_concurrent_plugins: int = u.Field(default=100, ge=1, le=1000)
    plugin_timeout_seconds: int = u.Field(default=300, ge=1, le=3600)

    # Hot reload settings
    enable_hot_reload: bool = u.Field(default=True)
    hot_reload_interval: int = u.Field(default=2, ge=1, le=60)

    # Monitoring settings
    enable_metrics: bool = u.Field(default=True)
    enable_tracing: bool = u.Field(default=True)
    metrics_interval: int = u.Field(default=60, ge=10, le=3600)

    @validator("plugin_paths")
    def validate_plugin_paths(cls, paths):
        """Validate plugin paths exist or are valid."""
        for path in paths:
            if not (
                path.startswith("./") or path.startswith("~/") or path.startswith("/")
            ):
                raise ValueError(f"Invalid plugin path format: {path}")
        return paths

    def get_plugin_paths(self) -> t.StringList:
        """Get resolved plugin paths."""
        import os
        from pathlib import Path

        resolved_paths = []
        for path in self.plugin_paths:
            resolved = os.path.expanduser(path)
            if Path(resolved).exists() or path.startswith("./"):
                resolved_paths.append(resolved)

        return resolved_paths

    def is_security_enabled(self) -> bool:
        """Check if security features are enabled."""
        return self.security_level in ["MEDIUM", "HIGH"]

    def is_monitoring_enabled(self) -> bool:
        """Check if monitoring features are enabled."""
        return self.enable_metrics or self.enable_tracing
```

______________________________________________________________________

## 🚀 Deployment and Operations

### Container Configuration

#### **Docker Deployment**

```dockerfile
# Dockerfile for FLEXT Plugin system
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set up Python environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src
WORKDIR /app

# Install Python dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry settings virtualenvs.create false
RUN poetry install --no-dev --no-interaction

# Copy source code
COPY src/ ./src/

# Create plugin directories
RUN mkdir -p /app/plugins /app/logs /app/cache

# Set up non-root user
RUN useradd --create-home --shell /bin/bash flext
RUN chown -R flext:flext /app
USER flext

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from flext_plugin import FlextPluginApi; print('OK')" || exit 1

# Default command
CMD ["python", "-m", "flext_plugin.cli", "--help"]
```

#### **Kubernetes Deployment**

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flext-plugin
  labels:
    app: flext-plugin
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flext-plugin
  template:
    metadata:
      labels:
        app: flext-plugin
    spec:
      containers:
        - name: flext-plugin
          image: flext/flext-plugin:0.9.0
          ports:
            - containerPort: 8000
              name: api
          env:
            - name: PYTHONPATH
              value: "/app/src"
            - name: FLEXT_PLUGIN_SECURITY_LEVEL
              value: "HIGH"
            - name: FLEXT_PLUGIN_MAX_CONCURRENT_PLUGINS
              value: "100"
          volumeMounts:
            - name: plugin-storage
              mountPath: /app/plugins
            - name: cache-storage
              mountPath: /app/cache
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
      volumes:
        - name: plugin-storage
          persistentVolumeClaim:
            claimName: flext-plugin-storage
        - name: cache-storage
          emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: flext-plugin-service
spec:
  selector:
    app: flext-plugin
  ports:
    - name: api
      port: 8000
      targetPort: 8000
  type: ClusterIP
```

### Monitoring and Observability

#### **Health Checks Implementation**

```python
# flext_plugin/health.py
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r, p
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u
from typing import Dict, t.Container



class FlextPluginHealth:
    """Health check implementation for FLEXT Plugin system."""

    def __init__(self, platform: FlextPluginPlatform):
        self.platform = platform

    async def check_overall_health(self) -> p.Result[Dict[str, t.Container]]:
        """Comprehensive health check."""
        try:
            health_status = {
                "status": "healthy",
                "timestamp": datetime.now(UTC).isoformat(),
                "checks": {},
            }

            # Platform health
            platform_health = await self._check_platform_health()
            health_status["checks"]["platform"] = platform_health

            # Plugin health
            plugin_health = await self._check_plugin_health()
            health_status["checks"]["plugins"] = plugin_health

            # Registry health
            registry_health = await self._check_registry_health()
            health_status["checks"]["registry"] = registry_health

            # Determine overall status
            all_healthy = all(
                check.get("status") == "healthy"
                for check in health_status["checks"].values()
            )

            if not all_healthy:
                health_status["status"] = "unhealthy"

            return r.ok(health_status)

        except Exception as e:
            return r.fail(f"Health check failed: {e!s}")

    async def _check_platform_health(self) -> Dict[str, t.Container]:
        """Check platform operational health."""
        try:
            # Test basic platform operations
            status = self.platform.get_platform_status()

            return {
                "status": "healthy",
                "details": status,
                "response_time_ms": 10,  # Mock timing
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    async def _check_plugin_health(self) -> Dict[str, t.Container]:
        """Check plugin system health."""
        try:
            plugins = self.platform.list_plugins()
            active_plugins = [p for p in plugins if p.is_active()]

            return {
                "status": "healthy",
                "total_plugins": len(plugins),
                "active_plugins": len(active_plugins),
                "inactive_plugins": len(plugins) - len(active_plugins),
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    async def _check_registry_health(self) -> Dict[str, t.Container]:
        """Check plugin registry health."""
        try:
            # Test registry operations
            registry_status = {
                "can_read": True,
                "can_write": True,
                "last_backup": "2025-10-01T00:00:00Z",  # Mock data
            }

            return {"status": "healthy", "details": registry_status}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
```

______________________________________________________________________

## 📊 Performance Optimization Implementation

### Caching Strategies

#### **Multi-Level Caching**

```python
# flext_plugin/cache.py
from typing import Dict, t.Container, Optional
import asyncio
from datetime import datetime, timedelta
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r, p
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u


class FlextPluginCache:
    """Multi-level caching for plugin system performance."""

    def __init__(self, max_memory_items: int = 1000, ttl_seconds: int = 3600):
        self.memory_cache: Dict[str, Dict[str, t.Container]] = {}
        self.max_memory_items = max_memory_items
        self.ttl_seconds = ttl_seconds
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[t.Container]:
        """Get item from cache with TTL check."""
        async with self._lock:
            if key in self.memory_cache:
                entry = self.memory_cache[key]
                if not self._is_expired(entry):
                    return entry["value"]
                else:
                    # Remove expired entry
                    del self.memory_cache[key]

        return None

    async def set(self, key: str, value) -> None:
        """Set item in cache with TTL."""
        async with self._lock:
            # Implement LRU eviction if needed
            if len(self.memory_cache) >= self.max_memory_items:
                self._evict_lru()

            self.memory_cache[key] = {
                "value": value,
                "timestamp": datetime.now(UTC),
                "ttl": timedelta(seconds=self.ttl_seconds),
            }

    def _is_expired(self, entry: Dict[str, t.Container]) -> bool:
        """Check if cache entry is expired."""
        return datetime.now(UTC) > entry["timestamp"] + entry["ttl"]

    def _evict_lru(self) -> None:
        """Evict least recently used items."""
        # Simple FIFO eviction for demonstration
        oldest_key = next(iter(self.memory_cache))
        del self.memory_cache[oldest_key]
```

### Asynchronous Processing

#### **Concurrent Plugin Operations**

```python
# flext_plugin/executor.py
import asyncio
from typing import List, Dict, t.Container
from concurrent.futures import ThreadPoolExecutor
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r, p
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u
from flext_plugin import FlextPluginModels



class FlextPluginExecutor:
    """Asynchronous plugin execution with concurrency control."""

    def __init__(self, max_concurrent: int = 10, thread_pool_size: int = 4):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.executor = ThreadPoolExecutor(max_workers=thread_pool_size)

    async def execute_plugins_concurrent(
        self, plugins: List[FlextPluginModels.Plugin], context: Dict[str, t.Container]
    ) -> p.Result[List[FlextPluginModels.Execution]]:
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
        self, plugin: FlextPluginModels.Plugin, context: Dict[str, t.Container]
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
        self, plugin: FlextPluginModels.Plugin, context: Dict[str, t.Container]
    ):
        """Synchronous plugin execution (runs in thread pool)."""
        # Actual plugin execution logic
        # This would integrate with the plugin loading system
        return {"status": "completed", "result": "mock result"}
```

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
