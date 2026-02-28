"""Unit tests for FlextPluginTypes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_plugin import FlextPluginTypes, t


class TestFlextPluginTypes:
    """Test cases for FlextPluginTypes."""

    def test_types_initialization(self) -> None:
        """Test that types can be initialized."""
        types = FlextPluginTypes()
        assert types is not None

    def test_types_alias_exists(self) -> None:
        """Test that t alias exists."""
        assert t is FlextPluginTypes

    def test_plugin_class_exists(self) -> None:
        """Test that Plugin nested class exists."""
        assert hasattr(FlextPluginTypes, "Plugin")
        assert FlextPluginTypes.Plugin is not None

    def test_discovery_class_exists(self) -> None:
        """Test that Discovery nested class exists."""
        assert hasattr(FlextPluginTypes, "Discovery")
        assert FlextPluginTypes.Discovery is not None

    def test_execution_class_exists(self) -> None:
        """Test that Execution nested class exists."""
        assert hasattr(FlextPluginTypes, "Execution")
        assert FlextPluginTypes.Execution is not None

    def test_registry_class_exists(self) -> None:
        """Test that Registry nested class exists."""
        assert hasattr(FlextPluginTypes, "Registry")
        assert FlextPluginTypes.Registry is not None

    def test_discovery_type_aliases(self) -> None:
        """Test Discovery type aliases exist."""
        assert hasattr(FlextPluginTypes.Discovery, "DiscoveryPath")
        assert hasattr(FlextPluginTypes.Discovery, "DiscoveryResult")
        assert hasattr(FlextPluginTypes.Discovery, "PluginLoader")
        assert hasattr(FlextPluginTypes.Discovery, "EntryPoint")

    def test_execution_type_aliases(self) -> None:
        """Test Execution type aliases exist."""
        assert hasattr(FlextPluginTypes.Execution, "ExecutionContext")
        assert hasattr(FlextPluginTypes.Execution, "ExecutionResult")
        assert hasattr(FlextPluginTypes.Execution, "ExecutionError")
        assert hasattr(FlextPluginTypes.Execution, "ResourceLimits")

    def test_registry_type_aliases(self) -> None:
        """Test Registry type aliases exist."""
        assert hasattr(FlextPluginTypes.Registry, "RegistryConfig")
        assert hasattr(FlextPluginTypes.Registry, "RegistryEntry")
