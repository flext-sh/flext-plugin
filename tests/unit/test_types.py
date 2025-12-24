"""Unit tests for t_plugin.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext import t

from flext_plugin.protocols import FlextPluginProtocols
from flext_plugin.typings import t as t_plugin


class TestFlextPluginTypes:
    """Test cases for t_plugin."""

    def test_types_initialization(self) -> None:
        """Test that types can be initialized."""
        types = t_plugin()
        assert types is not None

    def test_core_types(self) -> None:
        """Test core type definitions."""
        # Test string collections
        assert t_plugin.Plugin.StringList == list[str]
        assert t_plugin.Plugin.StringSet == set[str]
        assert t_plugin.Plugin.StringDict == dict[str, str]

        # Test numeric collections
        assert t_plugin.Plugin.IntList == t.IntList
        assert t_plugin.Plugin.FloatList == t.FloatList
        assert t_plugin.Plugin.IntDict == dict[str, int]
        assert t_plugin.Plugin.FloatDict == dict[str, float]

        # Test mixed collections
        assert t_plugin.Plugin.AnyList == list[object]
        assert t_plugin.Plugin.AnyDict == dict[str, object]

        # Test plugin-specific collections
        assert t_plugin.Plugin.PluginList == list[dict[str, object]]
        assert t_plugin.Plugin.PluginDict == dict[str, object]
        assert t_plugin.Plugin.ConfigDict == dict[str, object]
        assert t_plugin.Plugin.SettingsDict == dict[str, object]
        assert t_plugin.Plugin.MetadataDict == dict[str, object]
        assert t_plugin.Plugin.InputDict == dict[str, object]
        assert t_plugin.Plugin.OutputDict == dict[str, object]

    def test_lifecycle_types(self) -> None:
        """Test lifecycle type definitions."""
        # Test type aliases
        assert t_plugin.Lifecycle.PluginStatus is str
        assert t_plugin.Lifecycle.PluginType is str
        assert t_plugin.Lifecycle.LifecycleState is str
        assert t_plugin.Lifecycle.ExecutionStatus is str

        # Test status values
        assert t_plugin.Lifecycle.STATUS_UNKNOWN == "unknown"
        assert t_plugin.Lifecycle.STATUS_DISCOVERED == "discovered"
        assert t_plugin.Lifecycle.STATUS_LOADED == "loaded"
        assert t_plugin.Lifecycle.STATUS_ACTIVE == "active"
        assert t_plugin.Lifecycle.STATUS_INACTIVE == "inactive"
        assert t_plugin.Lifecycle.STATUS_LOADING == "loading"
        assert t_plugin.Lifecycle.STATUS_ERROR == "error"
        assert t_plugin.Lifecycle.STATUS_DISABLED == "disabled"
        assert t_plugin.Lifecycle.STATUS_HEALTHY == "healthy"
        assert t_plugin.Lifecycle.STATUS_UNHEALTHY == "unhealthy"

        # Test type values
        assert t_plugin.Lifecycle.TYPE_TAP == "tap"
        assert t_plugin.Lifecycle.TYPE_TARGET == "target"
        assert t_plugin.Lifecycle.TYPE_TRANSFORM == "transform"
        assert t_plugin.Lifecycle.TYPE_EXTENSION == "extension"
        assert t_plugin.Lifecycle.TYPE_SERVICE == "service"
        assert t_plugin.Lifecycle.TYPE_MIDDLEWARE == "middleware"
        assert t_plugin.Lifecycle.TYPE_TRANSFORMER == "transformer"
        assert t_plugin.Lifecycle.TYPE_API == "api"
        assert t_plugin.Lifecycle.TYPE_DATABASE == "database"
        assert t_plugin.Lifecycle.TYPE_NOTIFICATION == "notification"
        assert t_plugin.Lifecycle.TYPE_AUTHENTICATION == "authentication"
        assert t_plugin.Lifecycle.TYPE_AUTHORIZATION == "authorization"
        assert t_plugin.Lifecycle.TYPE_UTILITY == "utility"
        assert t_plugin.Lifecycle.TYPE_TOOL == "tool"
        assert t_plugin.Lifecycle.TYPE_HANDLER == "handler"
        assert t_plugin.Lifecycle.TYPE_PROCESSOR == "processor"
        assert t_plugin.Lifecycle.TYPE_CORE == "core"
        assert t_plugin.Lifecycle.TYPE_ADDON == "addon"
        assert t_plugin.Lifecycle.TYPE_THEME == "theme"
        assert t_plugin.Lifecycle.TYPE_LANGUAGE == "language"

    def test_security_types(self) -> None:
        """Test security type definitions."""
        # Test type aliases
        assert t_plugin.Security.SecurityLevel is str
        assert t_plugin.Security.Permission is str
        assert t_plugin.Security.SecurityConfig is dict[str, object]

        # Test security levels
        assert t_plugin.Security.SECURITY_LOW == "low"
        assert t_plugin.Security.SECURITY_MEDIUM == "medium"
        assert t_plugin.Security.SECURITY_HIGH == "high"
        assert t_plugin.Security.SECURITY_CRITICAL == "critical"

        # Test permissions
        assert t_plugin.Security.PERMISSION_NETWORK == "network"
        assert t_plugin.Security.PERMISSION_FILESYSTEM == "filesystem"
        assert t_plugin.Security.PERMISSION_DATABASE == "database"
        assert t_plugin.Security.PERMISSION_EXTERNAL_API == "external_api"

    def test_performance_types(self) -> None:
        """Test performance type definitions."""
        # Test type aliases
        assert t_plugin.Performance.Metrics == dict[str, object]
        assert t_plugin.Performance.PerformanceData == dict[str, object]
        assert t_plugin.Performance.ResourceUsage == dict[str, object]

        # Test performance thresholds
        assert t_plugin.Performance.EXCELLENT_SUCCESS_RATE == 95.0
        assert t_plugin.Performance.GOOD_SUCCESS_RATE == 90.0
        assert t_plugin.Performance.FAIR_SUCCESS_RATE == 80.0

        # Test time thresholds
        assert t_plugin.Performance.EXCELLENT_TIME_MS == 1000
        assert t_plugin.Performance.GOOD_TIME_MS == 2000
        assert t_plugin.Performance.FAIR_TIME_MS == 5000

    def test_discovery_types(self) -> None:
        """Test discovery type definitions."""
        # Test type aliases
        assert t_plugin.Discovery.DiscoveryPath is str
        assert t_plugin.Discovery.DiscoveryResult is dict[str, object]
        assert t_plugin.Discovery.PluginLoader is object
        assert t_plugin.Discovery.EntryPoint is str

        # Test discovery methods
        assert t_plugin.Discovery.METHOD_FILE_SYSTEM == "file_system"
        assert t_plugin.Discovery.METHOD_ENTRY_POINTS == "entry_points"
        assert t_plugin.Discovery.METHOD_PACKAGE_SCAN == "package_scan"

    def test_execution_types(self) -> None:
        """Test execution type definitions."""
        # Test type aliases
        assert t_plugin.Execution.ExecutionContext == dict[str, object]
        assert t_plugin.Execution.ExecutionResult == dict[str, object]
        assert t_plugin.Execution.ExecutionError is str
        assert t_plugin.Execution.ResourceLimits == dict[str, object]

        # Test execution states
        assert t_plugin.Execution.STATE_PENDING == "pending"
        assert t_plugin.Execution.STATE_RUNNING == "running"
        assert t_plugin.Execution.STATE_COMPLETED == "completed"
        assert t_plugin.Execution.STATE_FAILED == "failed"
        assert t_plugin.Execution.STATE_CANCELLED == "cancelled"

    def test_registry_types(self) -> None:
        """Test registry type definitions."""
        # Test type aliases
        assert t_plugin.Registry.RegistryConfig == dict[str, object]
        assert t_plugin.Registry.RegistryEntry == dict[str, object]
        assert t_plugin.Registry.RegistrySync == dict[str, object]

        # Test registry types
        assert t_plugin.Registry.TYPE_LOCAL == "local"
        assert t_plugin.Registry.TYPE_REMOTE == "remote"
        assert t_plugin.Registry.TYPE_HYBRID == "hybrid"

    def test_hot_reload_types(self) -> None:
        """Test hot reload type definitions."""
        # Test type aliases
        assert t_plugin.HotReload.WatchConfig == dict[str, object]
        assert t_plugin.HotReload.ReloadEvent == dict[str, object]
        assert t_plugin.HotReload.FileWatcher is object

        # Test watch events
        assert t_plugin.HotReload.EVENT_CREATED == "created"
        assert t_plugin.HotReload.EVENT_MODIFIED == "modified"
        assert t_plugin.HotReload.EVENT_DELETED == "deleted"
        assert t_plugin.HotReload.EVENT_MOVED == "moved"


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
