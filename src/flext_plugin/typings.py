"""Modern typings module for FLEXT Plugin system.

This module provides a unified interface to all type definitions
following flext-core patterns. Import from this module for consistency.
"""

from __future__ import annotations

# Re-export core FlextResult for convenience
from flext_core import FlextResult

from .flext_plugin_models import (
    FlextPluginConfigModel,
    FlextPluginMetadataModel,
    FlextPluginModel,
    PluginExecutionContextModel,
    PluginExecutionResultModel,
    PluginManagerResultModel,
    PluginStatus,
    PluginType,
)

# Import specific types from the centralized modules
from .type_definitions import (
    DirectoryPath,
    # Context Types
    ExecutionContextDict,
    ExecutionId,
    FileChangeCallback,
    HotReloadProtocol,
    PluginBoolResult,
    PluginCallback,
    # Configuration Aliases
    PluginConfigDict,
    # Data Types
    PluginData,
    PluginDataResult,
    PluginDict,
    PluginDiscoveryProtocol,
    PluginErrorCallback,
    PluginExecutorProtocol,
    # Function Aliases
    PluginFactory,
    PluginId,
    # Collection Aliases
    PluginList,
    PluginListResult,
    PluginLoaderProtocol,
    PluginMetadataDict,
    # Basic Aliases
    PluginName,
    PluginNameList,
    # Path Aliases
    PluginPath,
    # Protocols
    PluginProtocol,
    PluginRegistryProtocol,
    # Result Aliases
    PluginResult,
    PluginRuntimeDict,
    PluginStringResult,
    PluginUrl,
    PluginValidatorProtocol,
    PluginVersion,
    # Type Variables
    TPlugin,
    TPluginConfig,
    TPluginContext,
    TPluginData,
    TPluginMetadata,
    TPluginResult,
)


# PluginExecutionResult - Legacy compatible class for tests (avoiding circular imports)
class PluginExecutionResult:
    """Legacy execution result class for compatibility."""

    def __init__(
        self,
        execution_id: str,
        *,
        success: bool,
        duration_ms: int,
        output_data: dict[str, object] | None = None,
        error_message: str = "",
        **kwargs: object,
    ) -> None:
        self.execution_id = execution_id
        self.success = success
        self.duration_ms = duration_ms
        self.output_data = output_data if output_data is not None else None
        self.error_message = error_message
        # Store additional kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)


# Legacy compatibility exports (transitional)
PluginExecutionContext = ExecutionContextDict
PluginManagerResult = PluginStringResult
FlextPluginResult = PluginResult

__all__ = [
    "DirectoryPath",
    "ExecutionId",
    "FileChangeCallback",
    # Pydantic models
    "FlextPluginConfigModel",
    "FlextPluginMetadataModel",
    "FlextPluginModel",
    # Legacy compatibility (transitional)
    "FlextPluginResult",
    # FlextResult re-export
    "FlextResult",
    "HotReloadProtocol",
    "PluginBoolResult",
    "PluginCallback",
    "PluginConfigDict",
    "PluginData",
    "PluginDataResult",
    "PluginDict",
    "PluginDiscoveryProtocol",
    "PluginErrorCallback",
    "PluginExecutionContext",
    "PluginExecutionContextModel",
    "PluginExecutionResult",
    "PluginExecutionResultModel",
    "PluginExecutorProtocol",
    # Function aliases (from types.py)
    "PluginFactory",
    "PluginId",
    "PluginList",
    "PluginListResult",
    "PluginLoaderProtocol",
    "PluginManagerResult",
    "PluginManagerResultModel",
    "PluginMetadataDict",
    # Type aliases (from types.py)
    "PluginName",
    "PluginNameList",
    "PluginPath",
    # Protocols (from types.py)
    "PluginProtocol",
    "PluginRegistryProtocol",
    # Result aliases (from types.py)
    "PluginResult",
    "PluginRuntimeDict",
    # Core types and enums
    "PluginStatus",
    "PluginStringResult",
    "PluginType",
    "PluginUrl",
    "PluginValidatorProtocol",
    "PluginVersion",
    # Type variables (from types.py)
    "TPlugin",
    "TPluginConfig",
    "TPluginContext",
    "TPluginData",
    "TPluginMetadata",
    "TPluginResult",
]
