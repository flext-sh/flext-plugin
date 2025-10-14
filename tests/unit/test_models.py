"""Unit tests for FlextPluginModels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from datetime import datetime

import pytest

from flext_plugin.models import FlextPluginModels, PluginStatus, PluginType


class TestFlextPluginModels:
    """Test cases for FlextPluginModels."""

    def test_models_initialization(self) -> None:
        """Test that models can be initialized."""
        models = FlextPluginModels()
        assert models is not None

    def test_plugin_status_enum(self) -> None:
        """Test PluginStatus enum values and methods."""
        # Test enum values
        assert PluginStatus.UNKNOWN == "unknown"
        assert PluginStatus.DISCOVERED == "discovered"
        assert PluginStatus.LOADED == "loaded"
        assert PluginStatus.ACTIVE == "active"
        assert PluginStatus.INACTIVE == "inactive"
        assert PluginStatus.LOADING == "loading"
        assert PluginStatus.ERROR == "error"
        assert PluginStatus.DISABLED == "disabled"
        assert PluginStatus.HEALTHY == "healthy"
        assert PluginStatus.UNHEALTHY == "unhealthy"

        # Test class methods
        operational_statuses = PluginStatus.get_operational_statuses()
        assert PluginStatus.ACTIVE in operational_statuses
        assert PluginStatus.HEALTHY in operational_statuses
        assert PluginStatus.LOADED in operational_statuses

        error_statuses = PluginStatus.get_error_statuses()
        assert PluginStatus.ERROR in error_statuses
        assert PluginStatus.UNHEALTHY in error_statuses
        assert PluginStatus.DISABLED in error_statuses

        # Test instance methods
        assert PluginStatus.ACTIVE.is_operational()
        assert not PluginStatus.ERROR.is_operational()
        assert PluginStatus.ERROR.is_error_state()
        assert not PluginStatus.ACTIVE.is_error_state()

    def test_plugin_type_enum(self) -> None:
        """Test PluginType enum values and methods."""
        # Test ETL types
        assert PluginType.TAP == "tap"
        assert PluginType.TARGET == "target"
        assert PluginType.TRANSFORM == "transform"

        # Test architecture types
        assert PluginType.EXTENSION == "extension"
        assert PluginType.SERVICE == "service"
        assert PluginType.MIDDLEWARE == "middleware"
        assert PluginType.TRANSFORMER == "transformer"

        # Test integration types
        assert PluginType.API == "api"
        assert PluginType.DATABASE == "database"
        assert PluginType.NOTIFICATION == "notification"
        assert PluginType.AUTHENTICATION == "authentication"
        assert PluginType.AUTHORIZATION == "authorization"

        # Test utility types
        assert PluginType.UTILITY == "utility"
        assert PluginType.TOOL == "tool"
        assert PluginType.HANDLER == "handler"
        assert PluginType.PROCESSOR == "processor"

        # Test additional types
        assert PluginType.CORE == "core"
        assert PluginType.ADDON == "addon"
        assert PluginType.THEME == "theme"
        assert PluginType.LANGUAGE == "language"

        # Test class methods
        etl_types = PluginType.get_etl_types()
        assert PluginType.TAP in etl_types
        assert PluginType.TARGET in etl_types
        assert PluginType.TRANSFORM in etl_types

        arch_types = PluginType.get_architectural_types()
        assert PluginType.EXTENSION in arch_types
        assert PluginType.SERVICE in arch_types
        assert PluginType.MIDDLEWARE in arch_types
        assert PluginType.TRANSFORMER in arch_types

        # Test instance methods
        assert PluginType.TAP.is_etl_plugin()
        assert not PluginType.EXTENSION.is_etl_plugin()
        assert PluginType.EXTENSION.is_architectural_plugin()
        assert not PluginType.TAP.is_architectural_plugin()

    def test_plugin_model_creation(self) -> None:
        """Test PluginModel creation and validation."""
        # Test valid plugin creation
        plugin = FlextPluginModels.PluginModel(
            name="test-plugin",
            plugin_version="1.0.0",
            plugin_type=PluginType.UTILITY,
            status=PluginStatus.INACTIVE,
        )

        assert plugin.name == "test-plugin"
        assert plugin.plugin_version == "1.0.0"
        assert plugin.plugin_type == PluginType.UTILITY
        assert plugin.status == PluginStatus.INACTIVE
        assert plugin.enabled is True
        assert plugin.dependencies == []
        assert plugin.tags == []
        assert isinstance(plugin.created_at, datetime)

    def test_plugin_model_validation(self) -> None:
        """Test PluginModel validation rules."""
        # Test valid plugin
        plugin = FlextPluginModels.PluginModel(
            name="valid-plugin",
            plugin_version="1.0.0",
            plugin_type=PluginType.UTILITY,
            status=PluginStatus.INACTIVE,
        )
        assert plugin.is_valid()

        # Test invalid plugin name
        with pytest.raises(ValueError):
            FlextPluginModels.PluginModel(
                name="",  # Empty name should fail
                plugin_version="1.0.0",
                plugin_type=PluginType.UTILITY,
                status=PluginStatus.INACTIVE,
            )

        # Test invalid version format
        with pytest.raises(ValueError):
            FlextPluginModels.PluginModel(
                name="test-plugin",
                plugin_version="invalid-version",  # Invalid format
                plugin_type=PluginType.UTILITY,
                status=PluginStatus.INACTIVE,
            )

    def test_plugin_model_consistency_validation(self) -> None:
        """Test PluginModel consistency validation."""
        # Test active plugin cannot be disabled
        with pytest.raises(ValueError):
            FlextPluginModels.PluginModel(
                name="test-plugin",
                plugin_version="1.0.0",
                plugin_type=PluginType.UTILITY,
                status=PluginStatus.ACTIVE,
                enabled=False,  # Active plugin cannot be disabled
            )

        # Test plugin cannot depend on itself
        with pytest.raises(ValueError):
            FlextPluginModels.PluginModel(
                name="test-plugin",
                plugin_version="1.0.0",
                plugin_type=PluginType.UTILITY,
                status=PluginStatus.INACTIVE,
                dependencies=["test-plugin"],  # Cannot depend on itself
            )

    def test_config_model_creation(self) -> None:
        """Test ConfigModel creation and validation."""
        config = FlextPluginModels.ConfigModel(
            enabled=True,
            priority=50,
            timeout_seconds=30,
            max_memory_mb=256,
            max_cpu_percent=50,
        )

        assert config.enabled is True
        assert config.priority == 50
        assert config.timeout_seconds == 30
        assert config.max_memory_mb == 256
        assert config.max_cpu_percent == 50
        assert config.auto_restart is True
        assert config.retry_attempts == 3

    def test_config_model_validation(self) -> None:
        """Test ConfigModel validation rules."""
        # Test valid config
        config = FlextPluginModels.ConfigModel(priority=50)
        assert (
            config.is_high_performance is False
        )  # Default values don't meet high performance

        # Test high performance config
        config = FlextPluginModels.ConfigModel(
            timeout_seconds=30, max_memory_mb=256, max_cpu_percent=50
        )
        assert config.is_high_performance is True

        # Test invalid priority range
        with pytest.raises(ValueError):
            FlextPluginModels.ConfigModel(priority=150)  # Above 100

        with pytest.raises(ValueError):
            FlextPluginModels.ConfigModel(priority=-10)  # Below 0

        # Test invalid memory limits
        with pytest.raises(ValueError):
            FlextPluginModels.ConfigModel(max_memory_mb=2000)  # Above production limit

        with pytest.raises(ValueError):
            FlextPluginModels.ConfigModel(max_memory_mb=32)  # Below minimum

    def test_security_model_creation(self) -> None:
        """Test SecurityModel creation and validation."""
        security = FlextPluginModels.SecurityModel(
            security_level="high",
            permissions=["network", "filesystem"],
            sandboxed=True,
            network_access=False,
            file_access=True,
            encrypted_data=True,
            audit_logging=True,
            signature_verified=True,
        )

        assert security.security_level == "high"
        assert security.permissions == ["network", "filesystem"]
        assert security.sandboxed is True
        assert security.network_access is False
        assert security.file_access is True
        assert security.encrypted_data is True
        assert security.audit_logging is True
        assert security.signature_verified is True

    def test_security_model_validation(self) -> None:
        """Test SecurityModel validation rules."""
        # Test secure configuration
        security = FlextPluginModels.SecurityModel(
            sandboxed=True,
            network_access=False,
            file_access=False,
            encrypted_data=True,
            audit_logging=True,
        )
        assert security.is_secure is True

        # Test insecure configuration
        security = FlextPluginModels.SecurityModel(
            sandboxed=False,
            network_access=True,
            file_access=True,
            encrypted_data=False,
            audit_logging=False,
        )
        assert security.is_secure is False

        # Test invalid security level
        with pytest.raises(ValueError):
            FlextPluginModels.SecurityModel(security_level="invalid")

    def test_monitoring_model_creation(self) -> None:
        """Test MonitoringModel creation and validation."""
        monitoring = FlextPluginModels.MonitoringModel(
            metrics_enabled=True,
            health_checks=True,
            performance_tracking=True,
            error_tracking=True,
            log_level="INFO",
            retention_days=30,
        )

        assert monitoring.metrics_enabled is True
        assert monitoring.health_checks is True
        assert monitoring.performance_tracking is True
        assert monitoring.error_tracking is True
        assert monitoring.log_level == "INFO"
        assert monitoring.retention_days == 30

    def test_monitoring_model_validation(self) -> None:
        """Test MonitoringModel validation rules."""
        # Test basic monitoring check
        monitoring = FlextPluginModels.MonitoringModel(
            metrics_enabled=True, health_checks=True, error_tracking=True
        )
        assert monitoring.has_basic_monitoring is True

        # Test missing basic monitoring
        monitoring = FlextPluginModels.MonitoringModel(
            metrics_enabled=False, health_checks=True, error_tracking=True
        )
        assert monitoring.has_basic_monitoring is False

        # Test invalid log level
        with pytest.raises(ValueError):
            FlextPluginModels.MonitoringModel(log_level="INVALID")

        # Test invalid retention days
        with pytest.raises(ValueError):
            FlextPluginModels.MonitoringModel(retention_days=0)

        with pytest.raises(ValueError):
            FlextPluginModels.MonitoringModel(retention_days=400)

    def test_alert_thresholds_validation(self) -> None:
        """Test alert thresholds validation."""
        # Test valid thresholds
        monitoring = FlextPluginModels.MonitoringModel(
            alert_thresholds={
                "cpu_percent": 80.0,
                "memory_percent": 85.0,
                "error_rate": 5.0,
                "response_time_ms": 5000.0,
            }
        )
        assert monitoring.alert_thresholds["cpu_percent"] == 80.0

        # Test missing required thresholds
        with pytest.raises(ValueError):
            FlextPluginModels.MonitoringModel(
                alert_thresholds={
                    "cpu_percent": 80.0,
                    # Missing other required thresholds
                }
            )

        # Test invalid percentage thresholds
        with pytest.raises(ValueError):
            FlextPluginModels.MonitoringModel(
                alert_thresholds={
                    "cpu_percent": 150.0,  # Above 100
                    "memory_percent": 85.0,
                    "error_rate": 5.0,
                    "response_time_ms": 5000.0,
                }
            )

        # Test negative thresholds
        with pytest.raises(ValueError):
            FlextPluginModels.MonitoringModel(
                alert_thresholds={
                    "cpu_percent": 80.0,
                    "memory_percent": 85.0,
                    "error_rate": -5.0,  # Negative
                    "response_time_ms": 5000.0,
                }
            )

    def test_metadata_model_creation(self) -> None:
        """Test MetadataModel creation and validation."""
        metadata = FlextPluginModels.MetadataModel(
            plugin_id="test-plugin-123",
            homepage="https://example.com",
            repository="https://github.com/example/plugin",
            documentation="https://docs.example.com",
            license="MIT",
            keywords=["test", "plugin"],
            maintainers=["developer@example.com"],
            platform_version="0.9.9",
            python_version="3.13",
        )

        assert metadata.plugin_id == "test-plugin-123"
        assert metadata.homepage == "https://example.com"
        assert metadata.repository == "https://github.com/example/plugin"
        assert metadata.documentation == "https://docs.example.com"
        assert metadata.license == "MIT"
        assert metadata.keywords == ["test", "plugin"]
        assert metadata.maintainers == ["developer@example.com"]
        assert metadata.platform_version == "0.9.9"
        assert metadata.python_version == "3.13"
        assert isinstance(metadata.created_at, datetime)

    def test_execution_context_model_creation(self) -> None:
        """Test ExecutionContextModel creation and validation."""
        context = FlextPluginModels.ExecutionContextModel(
            plugin_id="test-plugin-123",
            execution_id="exec-456",
            input_data={"key": "value"},
            context={"config": "test"},
            timeout_seconds=30,
        )

        assert context.plugin_id == "test-plugin-123"
        assert context.execution_id == "exec-456"
        assert context.input_data == {"key": "value"}
        assert context.context == {"config": "test"}
        assert context.timeout_seconds == 30
        assert isinstance(context.started_at, datetime)

    def test_execution_result_model_creation(self) -> None:
        """Test ExecutionResultModel creation and validation."""
        result = FlextPluginModels.ExecutionResultModel(
            success=True,
            data={"output": "result"},
            error="",
            plugin_name="test-plugin",
            execution_time=1.5,
            execution_id="exec-456",
        )

        assert result.success is True
        assert result.data == {"output": "result"}
        assert not result.error
        assert result.plugin_name == "test-plugin"
        assert result.execution_time == 1.5
        assert result.execution_id == "exec-456"
        assert result.duration_ms == 1500.0
        assert result.is_failure() is False

    def test_execution_result_model_failure(self) -> None:
        """Test ExecutionResultModel failure case."""
        result = FlextPluginModels.ExecutionResultModel(
            success=False,
            data=None,
            error="Plugin execution failed",
            plugin_name="test-plugin",
            execution_time=0.5,
            execution_id="exec-456",
        )

        assert result.success is False
        assert result.error == "Plugin execution failed"
        assert result.is_failure() is True

    def test_manager_result_model_creation(self) -> None:
        """Test ManagerResultModel creation and validation."""
        result = FlextPluginModels.ManagerResultModel(
            operation="load_plugins",
            success=True,
            plugins_affected=["plugin1", "plugin2"],
            execution_time_ms=100.0,
            details={"loaded_count": 2},
            errors=[],
        )

        assert result.operation == "load_plugins"
        assert result.success is True
        assert result.plugins_affected == ["plugin1", "plugin2"]
        assert result.execution_time_ms == 100.0
        assert result.details == {"loaded_count": 2}
        assert result.errors == []
        assert isinstance(result.completed_at, datetime)
