"""Unit tests for FlextPluginTypes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from flext_plugin.types import FlextPluginProtocols, FlextPluginTypes


class TestFlextPluginTypes:
    """Test cases for FlextPluginTypes."""

    def test_types_initialization(self) -> None:
        """Test that types can be initialized."""
        types = FlextPluginTypes()
        assert types is not None

    def test_core_types(self) -> None:
        """Test core type definitions."""
        # Test string collections
        assert FlextPluginTypes.Core.StringList == list[str]
        assert FlextPluginTypes.Core.StringSet == set[str]
        assert FlextPluginTypes.Core.StringDict == dict[str, str]

        # Test numeric collections
        assert FlextPluginTypes.Core.IntList == list[int]
        assert FlextPluginTypes.Core.FloatList == list[float]
        assert FlextPluginTypes.Core.IntDict == dict[str, int]
        assert FlextPluginTypes.Core.FloatDict == dict[str, float]

        # Test mixed collections
        assert FlextPluginTypes.Core.AnyList == list[object]
        assert FlextPluginTypes.Core.AnyDict == dict[str, object]

        # Test plugin-specific collections
        assert FlextPluginTypes.Core.PluginList == list[dict[str, object]]
        assert FlextPluginTypes.Core.PluginDict == dict[str, object]
        assert FlextPluginTypes.Core.ConfigDict == dict[str, object]
        assert FlextPluginTypes.Core.SettingsDict == dict[str, object]
        assert FlextPluginTypes.Core.MetadataDict == dict[str, object]
        assert FlextPluginTypes.Core.InputDict == dict[str, object]
        assert FlextPluginTypes.Core.OutputDict == dict[str, object]

    def test_lifecycle_types(self) -> None:
        """Test lifecycle type definitions."""
        # Test type aliases
        assert FlextPluginTypes.Lifecycle.PluginStatus is str
        assert FlextPluginTypes.Lifecycle.PluginType is str
        assert FlextPluginTypes.Lifecycle.LifecycleState is str
        assert FlextPluginTypes.Lifecycle.ExecutionStatus is str

        # Test status values
        assert FlextPluginTypes.Lifecycle.STATUS_UNKNOWN == "unknown"
        assert FlextPluginTypes.Lifecycle.STATUS_DISCOVERED == "discovered"
        assert FlextPluginTypes.Lifecycle.STATUS_LOADED == "loaded"
        assert FlextPluginTypes.Lifecycle.STATUS_ACTIVE == "active"
        assert FlextPluginTypes.Lifecycle.STATUS_INACTIVE == "inactive"
        assert FlextPluginTypes.Lifecycle.STATUS_LOADING == "loading"
        assert FlextPluginTypes.Lifecycle.STATUS_ERROR == "error"
        assert FlextPluginTypes.Lifecycle.STATUS_DISABLED == "disabled"
        assert FlextPluginTypes.Lifecycle.STATUS_HEALTHY == "healthy"
        assert FlextPluginTypes.Lifecycle.STATUS_UNHEALTHY == "unhealthy"

        # Test type values
        assert FlextPluginTypes.Lifecycle.TYPE_TAP == "tap"
        assert FlextPluginTypes.Lifecycle.TYPE_TARGET == "target"
        assert FlextPluginTypes.Lifecycle.TYPE_TRANSFORM == "transform"
        assert FlextPluginTypes.Lifecycle.TYPE_EXTENSION == "extension"
        assert FlextPluginTypes.Lifecycle.TYPE_SERVICE == "service"
        assert FlextPluginTypes.Lifecycle.TYPE_MIDDLEWARE == "middleware"
        assert FlextPluginTypes.Lifecycle.TYPE_TRANSFORMER == "transformer"
        assert FlextPluginTypes.Lifecycle.TYPE_API == "api"
        assert FlextPluginTypes.Lifecycle.TYPE_DATABASE == "database"
        assert FlextPluginTypes.Lifecycle.TYPE_NOTIFICATION == "notification"
        assert FlextPluginTypes.Lifecycle.TYPE_AUTHENTICATION == "authentication"
        assert FlextPluginTypes.Lifecycle.TYPE_AUTHORIZATION == "authorization"
        assert FlextPluginTypes.Lifecycle.TYPE_UTILITY == "utility"
        assert FlextPluginTypes.Lifecycle.TYPE_TOOL == "tool"
        assert FlextPluginTypes.Lifecycle.TYPE_HANDLER == "handler"
        assert FlextPluginTypes.Lifecycle.TYPE_PROCESSOR == "processor"
        assert FlextPluginTypes.Lifecycle.TYPE_CORE == "core"
        assert FlextPluginTypes.Lifecycle.TYPE_ADDON == "addon"
        assert FlextPluginTypes.Lifecycle.TYPE_THEME == "theme"
        assert FlextPluginTypes.Lifecycle.TYPE_LANGUAGE == "language"

    def test_security_types(self) -> None:
        """Test security type definitions."""
        # Test type aliases
        assert FlextPluginTypes.Security.SecurityLevel is str
        assert FlextPluginTypes.Security.Permission is str
        assert FlextPluginTypes.Security.SecurityConfig is dict[str, object]

        # Test security levels
        assert FlextPluginTypes.Security.SECURITY_LOW == "low"
        assert FlextPluginTypes.Security.SECURITY_MEDIUM == "medium"
        assert FlextPluginTypes.Security.SECURITY_HIGH == "high"
        assert FlextPluginTypes.Security.SECURITY_CRITICAL == "critical"

        # Test permissions
        assert FlextPluginTypes.Security.PERMISSION_NETWORK == "network"
        assert FlextPluginTypes.Security.PERMISSION_FILESYSTEM == "filesystem"
        assert FlextPluginTypes.Security.PERMISSION_DATABASE == "database"
        assert FlextPluginTypes.Security.PERMISSION_EXTERNAL_API == "external_api"

    def test_performance_types(self) -> None:
        """Test performance type definitions."""
        # Test type aliases
        assert FlextPluginTypes.Performance.Metrics == dict[str, object]
        assert FlextPluginTypes.Performance.PerformanceData == dict[str, object]
        assert FlextPluginTypes.Performance.ResourceUsage == dict[str, object]

        # Test performance thresholds
        assert FlextPluginTypes.Performance.EXCELLENT_SUCCESS_RATE == 95.0
        assert FlextPluginTypes.Performance.GOOD_SUCCESS_RATE == 90.0
        assert FlextPluginTypes.Performance.FAIR_SUCCESS_RATE == 80.0

        # Test time thresholds
        assert FlextPluginTypes.Performance.EXCELLENT_TIME_MS == 1000
        assert FlextPluginTypes.Performance.GOOD_TIME_MS == 2000
        assert FlextPluginTypes.Performance.FAIR_TIME_MS == 5000

    def test_discovery_types(self) -> None:
        """Test discovery type definitions."""
        # Test type aliases
        assert FlextPluginTypes.Discovery.DiscoveryPath is str
        assert FlextPluginTypes.Discovery.DiscoveryResult is dict[str, object]
        assert FlextPluginTypes.Discovery.PluginLoader is object
        assert FlextPluginTypes.Discovery.EntryPoint is str

        # Test discovery methods
        assert FlextPluginTypes.Discovery.METHOD_FILE_SYSTEM == "file_system"
        assert FlextPluginTypes.Discovery.METHOD_ENTRY_POINTS == "entry_points"
        assert FlextPluginTypes.Discovery.METHOD_PACKAGE_SCAN == "package_scan"

    def test_execution_types(self) -> None:
        """Test execution type definitions."""
        # Test type aliases
        assert FlextPluginTypes.Execution.ExecutionContext == dict[str, object]
        assert FlextPluginTypes.Execution.ExecutionResult == dict[str, object]
        assert FlextPluginTypes.Execution.ExecutionError is str
        assert FlextPluginTypes.Execution.ResourceLimits == dict[str, object]

        # Test execution states
        assert FlextPluginTypes.Execution.STATE_PENDING == "pending"
        assert FlextPluginTypes.Execution.STATE_RUNNING == "running"
        assert FlextPluginTypes.Execution.STATE_COMPLETED == "completed"
        assert FlextPluginTypes.Execution.STATE_FAILED == "failed"
        assert FlextPluginTypes.Execution.STATE_CANCELLED == "cancelled"

    def test_registry_types(self) -> None:
        """Test registry type definitions."""
        # Test type aliases
        assert FlextPluginTypes.Registry.RegistryConfig == dict[str, object]
        assert FlextPluginTypes.Registry.RegistryEntry == dict[str, object]
        assert FlextPluginTypes.Registry.RegistrySync == dict[str, object]

        # Test registry types
        assert FlextPluginTypes.Registry.TYPE_LOCAL == "local"
        assert FlextPluginTypes.Registry.TYPE_REMOTE == "remote"
        assert FlextPluginTypes.Registry.TYPE_HYBRID == "hybrid"

    def test_hot_reload_types(self) -> None:
        """Test hot reload type definitions."""
        # Test type aliases
        assert FlextPluginTypes.HotReload.WatchConfig == dict[str, object]
        assert FlextPluginTypes.HotReload.ReloadEvent == dict[str, object]
        assert FlextPluginTypes.HotReload.FileWatcher is object

        # Test watch events
        assert FlextPluginTypes.HotReload.EVENT_CREATED == "created"
        assert FlextPluginTypes.HotReload.EVENT_MODIFIED == "modified"
        assert FlextPluginTypes.HotReload.EVENT_DELETED == "deleted"
        assert FlextPluginTypes.HotReload.EVENT_MOVED == "moved"


class TestFlextPluginProtocols:
    """Test cases for FlextPluginProtocols."""

    def test_protocols_initialization(self) -> None:
        """Test that protocols can be initialized."""
        protocols = FlextPluginProtocols()
        assert protocols is not None

    def test_plugin_loader_protocol(self) -> None:
        """Test PluginLoader protocol definition."""
        # This test ensures the protocol is properly defined
        # In practice, you would test with actual implementations
        assert hasattr(FlextPluginProtocols.PluginLoader, "__annotations__")

    def test_plugin_discovery_protocol(self) -> None:
        """Test PluginDiscovery protocol definition."""
        assert hasattr(FlextPluginProtocols.PluginDiscovery, "__annotations__")

    def test_plugin_registry_protocol(self) -> None:
        """Test PluginRegistry protocol definition."""
        assert hasattr(FlextPluginProtocols.PluginRegistry, "__annotations__")

    def test_plugin_execution_protocol(self) -> None:
        """Test PluginExecution protocol definition."""
        assert hasattr(FlextPluginProtocols.PluginExecution, "__annotations__")

    def test_plugin_security_protocol(self) -> None:
        """Test PluginSecurity protocol definition."""
        assert hasattr(FlextPluginProtocols.PluginSecurity, "__annotations__")

    def test_plugin_hot_reload_protocol(self) -> None:
        """Test PluginHotReload protocol definition."""
        assert hasattr(FlextPluginProtocols.PluginHotReload, "__annotations__")

    def test_plugin_monitoring_protocol(self) -> None:
        """Test PluginMonitoring protocol definition."""
        assert hasattr(FlextPluginProtocols.PluginMonitoring, "__annotations__")

    def test_plugin_configuration_protocol(self) -> None:
        """Test PluginConfiguration protocol definition."""
        assert hasattr(FlextPluginProtocols.PluginConfiguration, "__annotations__")

    def test_plugin_lifecycle_protocol(self) -> None:
        """Test PluginLifecycle protocol definition."""
        assert hasattr(FlextPluginProtocols.PluginLifecycle, "__annotations__")

    def test_plugin_validation_protocol(self) -> None:
        """Test PluginValidation protocol definition."""
        assert hasattr(FlextPluginProtocols.PluginValidation, "__annotations__")

    def test_plugin_storage_protocol(self) -> None:
        """Test PluginStorage protocol definition."""
        assert hasattr(FlextPluginProtocols.PluginStorage, "__annotations__")
