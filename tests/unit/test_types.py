"""Unit tests for FlextPluginTypes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import tm

from flext_plugin import FlextPluginTypes, t


class TestFlextPluginTypes:
    """Test cases for FlextPluginTypes."""

    def test_types_initialization(self) -> None:
        """Test that types can be initialized."""
        types = FlextPluginTypes()
        assert types is not None

    def test_types_alias_exists(self) -> None:
        """Test that t alias exists."""
        tm.that(t is FlextPluginTypes, eq=True)

    def test_plugin_class_exists(self) -> None:
        """Test that Plugin nested class exists."""
        tm.that(hasattr(FlextPluginTypes, "Plugin"), eq=True)
        tm.that(FlextPluginTypes.Plugin, none=False)

    def test_discovery_class_exists(self) -> None:
        """Test that Discovery nested class exists."""
        tm.that(hasattr(FlextPluginTypes, "Discovery"), eq=True)
        tm.that(FlextPluginTypes.Discovery, none=False)

    def test_execution_class_exists(self) -> None:
        """Test that Execution nested class exists."""
        tm.that(hasattr(FlextPluginTypes, "Execution"), eq=True)
        tm.that(FlextPluginTypes.Execution, none=False)

    def test_registry_class_exists(self) -> None:
        """Test that Registry nested class exists."""
        tm.that(hasattr(FlextPluginTypes, "Registry"), eq=True)
        tm.that(FlextPluginTypes.Registry, none=False)

    def test_discovery_type_aliases(self) -> None:
        """Test Discovery type aliases exist."""
        tm.that(hasattr(FlextPluginTypes.Discovery, "DiscoveryPath"), eq=True)
        tm.that(hasattr(FlextPluginTypes.Discovery, "DiscoveryResult"), eq=True)
        tm.that(hasattr(FlextPluginTypes.Discovery, "PluginLoader"), eq=True)
        tm.that(hasattr(FlextPluginTypes.Discovery, "EntryPoint"), eq=True)

    def test_execution_type_aliases(self) -> None:
        """Test Execution type aliases exist."""
        tm.that(hasattr(FlextPluginTypes.Execution, "ExecutionContext"), eq=True)
        tm.that(hasattr(FlextPluginTypes.Execution, "ExecutionResult"), eq=True)
        tm.that(hasattr(FlextPluginTypes.Execution, "ExecutionError"), eq=True)
        tm.that(hasattr(FlextPluginTypes.Execution, "ResourceLimits"), eq=True)

    def test_registry_type_aliases(self) -> None:
        """Test Registry type aliases exist."""
        tm.that(hasattr(FlextPluginTypes.Registry, "RegistryConfig"), eq=True)
        tm.that(hasattr(FlextPluginTypes.Registry, "RegistryEntry"), eq=True)
