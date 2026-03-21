"""Unit tests for FlextPluginTypes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import u

from flext_plugin import FlextPluginTypes, t


class TestFlextPluginTypes:
    """Test cases for FlextPluginTypes."""

    def test_types_initialization(self) -> None:
        """Test that types can be initialized."""
        types = FlextPluginTypes()
        u.Tests.Matchers.that(types is not None, eq=True)

    def test_types_alias_exists(self) -> None:
        """Test that t alias exists."""
        u.Tests.Matchers.that(t is FlextPluginTypes, eq=True)

    def test_plugin_class_exists(self) -> None:
        """Test that Plugin nested class exists."""
        u.Tests.Matchers.that(hasattr(FlextPluginTypes, "Plugin"), eq=True)
        u.Tests.Matchers.that(FlextPluginTypes.Plugin is not None, eq=True)

    def test_discovery_class_exists(self) -> None:
        """Test that Discovery nested class exists."""
        u.Tests.Matchers.that(hasattr(FlextPluginTypes, "Discovery"), eq=True)
        u.Tests.Matchers.that(FlextPluginTypes.Discovery is not None, eq=True)

    def test_execution_class_exists(self) -> None:
        """Test that Execution nested class exists."""
        u.Tests.Matchers.that(hasattr(FlextPluginTypes, "Execution"), eq=True)
        u.Tests.Matchers.that(FlextPluginTypes.Execution is not None, eq=True)

    def test_registry_class_exists(self) -> None:
        """Test that Registry nested class exists."""
        u.Tests.Matchers.that(hasattr(FlextPluginTypes, "Registry"), eq=True)
        u.Tests.Matchers.that(FlextPluginTypes.Registry is not None, eq=True)

    def test_discovery_type_aliases(self) -> None:
        """Test Discovery type aliases exist."""
        u.Tests.Matchers.that(
            hasattr(FlextPluginTypes.Discovery, "DiscoveryPath"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextPluginTypes.Discovery, "DiscoveryResult"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextPluginTypes.Discovery, "PluginLoader"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextPluginTypes.Discovery, "EntryPoint"), eq=True
        )

    def test_execution_type_aliases(self) -> None:
        """Test Execution type aliases exist."""
        u.Tests.Matchers.that(
            hasattr(FlextPluginTypes.Execution, "ExecutionContext"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextPluginTypes.Execution, "ExecutionResult"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextPluginTypes.Execution, "ExecutionError"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextPluginTypes.Execution, "ResourceLimits"), eq=True
        )

    def test_registry_type_aliases(self) -> None:
        """Test Registry type aliases exist."""
        u.Tests.Matchers.that(
            hasattr(FlextPluginTypes.Registry, "RegistryConfig"), eq=True
        )
        u.Tests.Matchers.that(
            hasattr(FlextPluginTypes.Registry, "RegistryEntry"), eq=True
        )
