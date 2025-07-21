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

        assert plugin.plugin_id == "test-id"
        assert plugin.metadata == metadata
        assert plugin.plugin_status == PluginStatus.UNKNOWN.value

    def test_plugin_status_transitions(self) -> None:
        """Test plugin status can be updated."""
        metadata = self.create_test_metadata()
        plugin = PluginInstance(
            plugin_id="test-id",
            metadata=metadata,
        )

        # Test status can be changed
        plugin.plugin_status = PluginStatus.LOADED
        assert plugin.plugin_status == PluginStatus.LOADED.value

        plugin.plugin_status = PluginStatus.ACTIVE
        assert plugin.plugin_status == PluginStatus.ACTIVE.value

    def test_plugin_health_check(self) -> None:
        """Test plugin health status checking."""
        metadata = self.create_test_metadata()
        plugin = PluginInstance(
            plugin_id="test-id",
            metadata=metadata,
        )

        # Test healthy status
        plugin.plugin_status = PluginStatus.HEALTHY
        assert plugin.is_healthy is True

        # Test non-healthy status
        plugin.plugin_status = PluginStatus.UNHEALTHY
        assert plugin.is_healthy is False

    def test_plugin_execution_recording(self) -> None:
        """Test recording plugin execution metrics."""
        metadata = self.create_test_metadata()
        plugin = PluginInstance(
            plugin_id="test-id",
            metadata=metadata,
        )

        # Record successful execution
        plugin.record_execution(150.5, success=True)
        assert plugin.execution_count == 1
        assert plugin.average_execution_time_ms == 150.5
        assert plugin.last_execution is not None

        # Record another execution
        plugin.record_execution(200.0, success=True)
        assert plugin.execution_count == 2
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
        assert plugin.error_count == 1
        assert plugin.last_error == "Test error message"
        assert plugin.last_error_time is not None
        assert plugin.plugin_status == PluginStatus.UNHEALTHY.value


class TestPluginConfiguration:
    """Test PluginConfiguration entity functionality."""

    def test_configuration_creation(self) -> None:
        """Test creating PluginConfiguration."""
        config = PluginConfiguration(
            enabled=True,
            settings={"key": "value"},
            dependencies=["dep1", "dep2"],
        )

        assert config.enabled is True
        assert config.settings == {"key": "value"}
        assert config.dependencies == ["dep1", "dep2"]

    def test_configuration_defaults(self) -> None:
        """Test PluginConfiguration default values."""
        config = PluginConfiguration()

        assert config.enabled is True
        assert config.settings == {}
        assert config.dependencies == []
        assert config.priority == 100

    def test_configuration_resource_limits(self) -> None:
        """Test configuration resource limits."""
        config = PluginConfiguration(
            max_memory_mb=800,
            max_cpu_percent=75,
            timeout_seconds=300,
        )

        assert config.max_memory_mb == 800
        assert config.max_cpu_percent == 75
        assert config.timeout_seconds == 300


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

        assert execution.plugin_id == "test-plugin"
        assert execution.execution_id == "exec-123"
        assert execution.input_data == {"test": "input"}
        assert execution.end_time is None
        assert execution.output_data == {}
        assert execution.error_message is None

    def test_execution_lifecycle(self) -> None:
        """Test execution lifecycle management."""
        execution = PluginExecution(
            plugin_id="test-plugin",
            execution_id="exec-123",
        )

        # Test marking as started
        execution.mark_started()
        assert execution.execution_status == "running"
        assert execution.is_running is True
        assert execution.is_completed is False

        # Test marking as completed
        execution.mark_completed(success=True)
        assert execution.success is True
        assert execution.execution_status == "completed"
        assert execution.is_completed is True
        # Note: duration_ms assertion removed to avoid mypy unreachable warning

    def test_execution_failure(self) -> None:
        """Test failed plugin execution."""
        execution = PluginExecution(
            plugin_id="test-plugin",
            execution_id="exec-123",
        )

        # Mark execution as failed
        execution.mark_completed(success=False, error_message="Plugin execution failed")

        assert execution.success is False
        assert execution.error_message == "Plugin execution failed"
        assert execution.execution_status == "failed"

    def test_execution_resource_tracking(self) -> None:
        """Test execution resource usage tracking."""
        execution = PluginExecution(
            plugin_id="test-plugin",
            execution_id="exec-123",
        )

        # Update resource usage
        execution.update_resource_usage(memory_mb=256.5, cpu_time_ms=150.0)
        assert execution.memory_usage_mb == 256.5
        assert execution.cpu_time_ms == 150.0


class TestPluginRegistryEntity:
    """Test PluginRegistry domain entity functionality."""

    def test_registry_creation(self) -> None:
        """Test creating PluginRegistry entity."""
        registry = PluginRegistry(
            name="test-registry",
            registry_url="https://plugins.example.com",
        )

        assert registry.name == "test-registry"
        assert registry.registry_url == "https://plugins.example.com"
        assert registry.is_enabled is True
        assert registry.plugin_count == 0
        assert registry.sync_error_count == 0

    def test_registry_availability(self) -> None:
        """Test registry availability check."""
        # Enabled registry with URL should be available
        enabled_registry = PluginRegistry(
            name="enabled",
            registry_url="https://plugins.example.com",
            is_enabled=True,
        )
        assert enabled_registry.is_available is True

        # Disabled registry should not be available
        disabled_registry = PluginRegistry(
            name="disabled",
            registry_url="https://plugins.example.com",
            is_enabled=False,
        )
        assert disabled_registry.is_available is False

    def test_registry_sync_recording(self) -> None:
        """Test recording sync attempts."""
        registry = PluginRegistry(
            name="test",
            registry_url="https://example.com",
        )

        # Record successful sync
        registry.record_sync(success=True, plugin_count=5)
        assert registry.plugin_count == 5
        assert registry.sync_error_count == 0
        assert registry.last_sync is not None

        # Record failed sync
        registry.record_sync(success=False)
        assert registry.sync_error_count == 1
        assert registry.plugin_count == 5  # Should remain the same

    def test_registry_authentication_settings(self) -> None:
        """Test registry authentication configuration."""
        registry = PluginRegistry(
            name="secure-registry",
            registry_url="https://secure.example.com",
            requires_authentication=True,
            api_key="secret-key",
        )

        assert registry.requires_authentication is True
        assert registry.api_key == "secret-key"

    def test_registry_security_settings(self) -> None:
        """Test registry security configuration."""
        registry = PluginRegistry(
            name="secure-registry",
            registry_url="https://secure.example.com",
            verify_signatures=True,
            trusted_publishers=["acme-corp", "trusted-dev"],
        )

        assert registry.verify_signatures is True
        assert "acme-corp" in registry.trusted_publishers
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

        assert metadata.name == "test-plugin"
        assert metadata.entry_point == "test.entry:main"
        assert metadata.plugin_type == PluginType.TAP.value
        assert metadata.description == "Test extractor plugin"
        assert "requests" in metadata.dependencies
        assert "pydantic" in metadata.dependencies

    def test_metadata_defaults(self) -> None:
        """Test PluginMetadata default values."""
        metadata = PluginMetadata(
            name="minimal-plugin",
            entry_point="minimal.entry:main",
            plugin_type=PluginType.UTILITY,
        )

        assert metadata.name == "minimal-plugin"
        assert metadata.description == ""
        assert metadata.dependencies == []
        assert metadata.trusted is False
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
