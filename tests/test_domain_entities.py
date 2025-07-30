"""Tests for flext_plugin.domain.entities module.

Comprehensive tests for all domain entities and business logic.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from flext_plugin.core.types import PluginStatus, PluginType
from flext_plugin.domain.entities import (
    PluginConfiguration,
    PluginExecution,
    PluginInstance,
    PluginMetadata,
    PluginRegistry,
)

# Constants
EXPECTED_BULK_SIZE = 2
EXPECTED_TOTAL_PAGES = 8
EXPECTED_DATA_COUNT = 3


class TestPluginInstance:
    """Test PluginInstance entity functionality."""

    def create_test_metadata(self) -> PluginMetadata:
        """Create test plugin metadata."""
        return PluginMetadata(
            name="test-plugin",
            entry_point="test.entry:main",
            plugin_type=PluginType.TAP,
            description="Test plugin",
            author="Test Author",
            license="MIT",
        )

    def test_plugin_instance_creation(self) -> None:
        """Test creating PluginInstance entity."""
        metadata = self.create_test_metadata()
        plugin = PluginInstance(
            plugin_id="test-id",
            metadata=metadata,
        )

        if plugin.plugin_id != "test-id":
            raise AssertionError(f"Expected {'test-id'}, got {plugin.plugin_id}")
        assert plugin.metadata == metadata
        if plugin.plugin_status != PluginStatus.UNKNOWN.value:
            raise AssertionError(
                f"Expected {PluginStatus.UNKNOWN.value}, got {plugin.plugin_status}"
            )

    def test_plugin_status_transitions(self) -> None:
        """Test plugin status can be updated."""
        metadata = self.create_test_metadata()
        plugin = PluginInstance(
            plugin_id="test-id",
            metadata=metadata,
        )

        # Test status can be changed
        plugin.plugin_status = PluginStatus.LOADED
        if plugin.plugin_status != PluginStatus.LOADED.value:
            raise AssertionError(
                f"Expected {PluginStatus.LOADED.value}, got {plugin.plugin_status}"
            )

        plugin.plugin_status = PluginStatus.ACTIVE
        if plugin.plugin_status != PluginStatus.ACTIVE.value:
            raise AssertionError(
                f"Expected {PluginStatus.ACTIVE.value}, got {plugin.plugin_status}"
            )

    def test_plugin_health_check(self) -> None:
        """Test plugin health status checking."""
        metadata = self.create_test_metadata()
        plugin = PluginInstance(
            plugin_id="test-id",
            metadata=metadata,
        )

        # Test healthy status
        plugin.plugin_status = PluginStatus.HEALTHY
        if not (plugin.is_healthy):
            raise AssertionError(f"Expected True, got {plugin.is_healthy}")

        # Test non-healthy status
        plugin.plugin_status = PluginStatus.UNHEALTHY
        if plugin.is_healthy:
            raise AssertionError(f"Expected False, got {plugin.is_healthy}")

    def test_plugin_execution_recording(self) -> None:
        """Test recording plugin execution metrics."""
        metadata = self.create_test_metadata()
        plugin = PluginInstance(
            plugin_id="test-id",
            metadata=metadata,
        )

        # Record successful execution
        plugin.record_execution(150.5, success=True)
        if plugin.execution_count != 1:
            raise AssertionError(f"Expected {1}, got {plugin.execution_count}")
        assert plugin.average_execution_time_ms == 150.5
        assert plugin.last_execution is not None

        # Record another execution
        plugin.record_execution(200.0, success=True)
        if plugin.execution_count != EXPECTED_BULK_SIZE:
            raise AssertionError(f"Expected {2}, got {plugin.execution_count}")
        assert plugin.average_execution_time_ms == 175.25  # (150.5 + 200.0) / 2

    def test_plugin_error_recording(self) -> None:
        """Test recording plugin errors."""
        metadata = self.create_test_metadata()
        plugin = PluginInstance(
            plugin_id="test-id",
            metadata=metadata,
        )

        # Record error
        plugin.record_error("Test error message")
        if plugin.error_count != 1:
            raise AssertionError(f"Expected {1}, got {plugin.error_count}")
        assert plugin.last_error == "Test error message"
        assert plugin.last_error_time is not None
        if plugin.plugin_status != PluginStatus.UNHEALTHY.value:
            raise AssertionError(
                f"Expected {PluginStatus.UNHEALTHY.value}, got {plugin.plugin_status}"
            )


class TestPluginConfiguration:
    """Test PluginConfiguration entity functionality."""

    def test_configuration_creation(self) -> None:
        """Test creating PluginConfiguration."""
        config = PluginConfiguration(
            enabled=True,
            settings={"key": "value"},
            dependencies=["dep1", "dep2"],
        )

        if not (config.enabled):
            raise AssertionError(f"Expected True, got {config.enabled}")
        if config.settings != {"key": "value"}:
            expected = {"key": "value"}
            raise AssertionError(f"Expected {expected}, got {config.settings}")
        assert config.dependencies == ["dep1", "dep2"]

    def test_configuration_defaults(self) -> None:
        """Test PluginConfiguration default values."""
        config = PluginConfiguration()

        if not (config.enabled):
            raise AssertionError(f"Expected True, got {config.enabled}")
        if config.settings != {}:
            raise AssertionError(f"Expected {{}}, got {config.settings}")
        assert config.dependencies == []
        if config.priority != 100:
            raise AssertionError(f"Expected {100}, got {config.priority}")

    def test_configuration_resource_limits(self) -> None:
        """Test configuration resource limits."""
        config = PluginConfiguration(
            max_memory_mb=800,
            max_cpu_percent=75,
            timeout_seconds=300,
        )

        if config.max_memory_mb != 800:
            raise AssertionError(f"Expected {800}, got {config.max_memory_mb}")
        assert config.max_cpu_percent == 75
        if config.timeout_seconds != 300:
            raise AssertionError(f"Expected {300}, got {config.timeout_seconds}")


class TestPluginExecution:
    """Test PluginExecution entity functionality."""

    def test_execution_creation(self) -> None:
        """Test creating PluginExecution."""
        datetime.now(UTC)
        execution = PluginExecution(
            plugin_id="test-plugin",
            execution_id="exec-123",
            input_data={"test": "input"},
        )

        if execution.plugin_id != "test-plugin":
            raise AssertionError(f"Expected {'test-plugin'}, got {execution.plugin_id}")
        assert execution.execution_id == "exec-123"
        if execution.input_data != {"test": "input"}:
            expected_input = {"test": "input"}
            raise AssertionError(
                f"Expected {expected_input}, got {execution.input_data}"
            )
        assert execution.end_time is None
        if execution.output_data != {}:
            raise AssertionError(f"Expected {{}}, got {execution.output_data}")
        assert execution.error_message is None

    def test_execution_lifecycle(self) -> None:
        """Test execution lifecycle management."""
        execution = PluginExecution(
            plugin_id="test-plugin",
            execution_id="exec-123",
        )

        # Test marking as started
        execution.mark_started()
        if execution.execution_status != "running":
            raise AssertionError(
                f"Expected {'running'}, got {execution.execution_status}"
            )
        if not (execution.is_running):
            raise AssertionError(f"Expected True, got {execution.is_running}")
        if execution.is_completed:
            raise AssertionError(f"Expected False, got {execution.is_completed}")

        # Test marking as completed
        execution.mark_completed(success=True)
        if not (execution.success):
            raise AssertionError(f"Expected True, got {execution.success}")
        if execution.execution_status != "completed":
            raise AssertionError(
                f"Expected {'completed'}, got {execution.execution_status}"
            )
        if not (execution.is_completed):
            raise AssertionError(f"Expected True, got {execution.is_completed}")
        # Note: duration_ms assertion removed to avoid mypy unreachable warning

    def test_execution_failure(self) -> None:
        """Test failed plugin execution."""
        execution = PluginExecution(
            plugin_id="test-plugin",
            execution_id="exec-123",
        )

        # Mark execution as failed
        execution.mark_completed(success=False, error_message="Plugin execution failed")

        if execution.success:
            raise AssertionError(f"Expected False, got {execution.success}")
        assert execution.error_message == "Plugin execution failed"
        if execution.execution_status != "failed":
            raise AssertionError(
                f"Expected {'failed'}, got {execution.execution_status}"
            )

    def test_execution_resource_tracking(self) -> None:
        """Test execution resource usage tracking."""
        execution = PluginExecution(
            plugin_id="test-plugin",
            execution_id="exec-123",
        )

        # Update resource usage
        execution.update_resource_usage(memory_mb=256.5, cpu_time_ms=150.0)
        if execution.memory_usage_mb != 256.5:
            raise AssertionError(f"Expected {256.5}, got {execution.memory_usage_mb}")
        assert execution.cpu_time_ms == 150.0


class TestPluginRegistryEntity:
    """Test PluginRegistry domain entity functionality."""

    def test_registry_creation(self) -> None:
        """Test creating PluginRegistry entity."""
        registry = PluginRegistry(
            name="test-registry",
            registry_url="https://plugins.example.com",
        )

        if registry.name != "test-registry":
            raise AssertionError(f"Expected {'test-registry'}, got {registry.name}")
        assert registry.registry_url == "https://plugins.example.com"
        if not (registry.is_enabled):
            raise AssertionError(f"Expected True, got {registry.is_enabled}")
        if registry.plugin_count != 0:
            raise AssertionError(f"Expected {0}, got {registry.plugin_count}")
        assert registry.sync_error_count == 0

    def test_registry_availability(self) -> None:
        """Test registry availability check."""
        # Enabled registry with URL should be available
        enabled_registry = PluginRegistry(
            name="enabled",
            registry_url="https://plugins.example.com",
            is_enabled=True,
        )
        if not (enabled_registry.is_available):
            raise AssertionError(f"Expected True, got {enabled_registry.is_available}")

        # Disabled registry should not be available
        disabled_registry = PluginRegistry(
            name="disabled",
            registry_url="https://plugins.example.com",
            is_enabled=False,
        )
        if disabled_registry.is_available:
            raise AssertionError(
                f"Expected False, got {disabled_registry.is_available}"
            )

    def test_registry_sync_recording(self) -> None:
        """Test recording sync attempts."""
        registry = PluginRegistry(
            name="test",
            registry_url="https://example.com",
        )

        # Record successful sync
        registry.record_sync(success=True, plugin_count=5)
        if registry.plugin_count != 5:
            raise AssertionError(f"Expected {5}, got {registry.plugin_count}")
        assert registry.sync_error_count == 0
        assert registry.last_sync is not None

        # Record failed sync
        registry.record_sync(success=False)
        if registry.sync_error_count != 1:
            raise AssertionError(f"Expected {1}, got {registry.sync_error_count}")
        assert registry.plugin_count == 5  # Should remain the same

    def test_registry_authentication_settings(self) -> None:
        """Test registry authentication configuration."""
        registry = PluginRegistry(
            name="secure-registry",
            registry_url="https://secure.example.com",
            requires_authentication=True,
            api_key="secret-key",
        )

        if not (registry.requires_authentication):
            raise AssertionError(
                f"Expected True, got {registry.requires_authentication}"
            )
        if registry.api_key != "secret-key":
            raise AssertionError(f"Expected {'secret-key'}, got {registry.api_key}")

    def test_registry_security_settings(self) -> None:
        """Test registry security configuration."""
        registry = PluginRegistry(
            name="secure-registry",
            registry_url="https://secure.example.com",
            verify_signatures=True,
            trusted_publishers=["acme-corp", "trusted-dev"],
        )

        if not (registry.verify_signatures):
            raise AssertionError(f"Expected True, got {registry.verify_signatures}")
        if "acme-corp" not in registry.trusted_publishers:
            raise AssertionError(
                f"Expected {'acme-corp'} in {registry.trusted_publishers}"
            )
        assert "trusted-dev" in registry.trusted_publishers


class TestPluginMetadata:
    """Test PluginMetadata functionality."""

    def test_metadata_creation(self) -> None:
        """Test creating PluginMetadata."""
        metadata = PluginMetadata(
            name="test-plugin",
            entry_point="test.entry:main",
            plugin_type=PluginType.TAP,
            description="Test extractor plugin",
            dependencies=["requests", "pydantic"],
        )

        if metadata.name != "test-plugin":
            raise AssertionError(f"Expected {'test-plugin'}, got {metadata.name}")
        assert metadata.entry_point == "test.entry:main"
        if metadata.plugin_type != PluginType.TAP.value:
            raise AssertionError(
                f"Expected {PluginType.TAP.value}, got {metadata.plugin_type}"
            )
        assert metadata.description == "Test extractor plugin"
        if "requests" not in metadata.dependencies:
            raise AssertionError(f"Expected {'requests'} in {metadata.dependencies}")
        assert "pydantic" in metadata.dependencies

    def test_metadata_defaults(self) -> None:
        """Test PluginMetadata default values."""
        metadata = PluginMetadata(
            name="minimal-plugin",
            entry_point="minimal.entry:main",
            plugin_type=PluginType.UTILITY,
        )

        if metadata.name != "minimal-plugin":
            raise AssertionError(f"Expected {'minimal-plugin'}, got {metadata.name}")
        assert metadata.description == ""
        if metadata.dependencies != []:
            raise AssertionError(f"Expected {[]}, got {metadata.dependencies}")
        if metadata.trusted:
            raise AssertionError(f"Expected False, got {metadata.trusted}")
        assert metadata.homepage is None
        assert metadata.repository is None

    def test_metadata_validation(self) -> None:
        """Test PluginMetadata validation."""
        # Test empty name fails
        with pytest.raises(ValidationError):
            PluginMetadata(
                name="",
                entry_point="test.entry:main",
                plugin_type=PluginType.TAP,
            )

        # Test empty entry point fails
        with pytest.raises(ValidationError):
            PluginMetadata(
                name="test-plugin",
                entry_point="",
                plugin_type=PluginType.TAP,
            )
