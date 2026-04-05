"""Unit tests for FlextPluginTypes.

Tests type namespace organization and type alias accessibility
via canonical t.Plugin namespace.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import tm

from flext_plugin import FlextPluginTypes
from tests import t


class TestFlextPluginTypes:
    """Test cases for FlextPluginTypes."""

    def test_types_alias_matches_facade(self) -> None:
        """T alias inherits from FlextPluginTypes facade."""
        tm.that(FlextPluginTypes in t.__mro__, eq=True)

    def test_plugin_namespace_exposes_sub_namespaces(self) -> None:
        """Plugin namespace contains Discovery, Execution, Registry sub-namespaces."""
        plugin = t.Plugin
        tm.that(str(plugin.Discovery.__name__), eq="Discovery")
        tm.that(str(plugin.Execution.__name__), eq="Execution")
        tm.that(str(plugin.Registry.__name__), eq="Registry")

    def test_discovery_type_aliases_accessible(self) -> None:
        """Discovery sub-namespace exposes expected type aliases."""
        discovery = t.Plugin.Discovery
        tm.that(str(discovery.DiscoveryPath), none=False)
        tm.that(str(discovery.DiscoveryResult), none=False)
        tm.that(str(discovery.PluginLoader), none=False)
        tm.that(str(discovery.EntryPoint), none=False)

    def test_execution_type_aliases_accessible(self) -> None:
        """Execution sub-namespace exposes expected type aliases."""
        execution = t.Plugin.Execution
        tm.that(str(execution.ExecutionContext), none=False)
        tm.that(str(execution.ExecutionResult), none=False)
        tm.that(str(execution.ExecutionError), none=False)
        tm.that(str(execution.ResourceLimits), none=False)

    def test_registry_type_aliases_accessible(self) -> None:
        """Registry sub-namespace exposes expected type aliases."""
        registry = t.Plugin.Registry
        tm.that(str(registry.RegistryConfig), none=False)
        tm.that(str(registry.RegistryEntry), none=False)

    def test_plugin_container_types_accessible(self) -> None:
        """Plugin namespace exposes container type aliases."""
        plugin = t.Plugin
        tm.that(str(plugin.PluginDict), none=False)
        tm.that(str(plugin.PluginList), none=False)
        tm.that(str(plugin.StringDict), none=False)
        tm.that(str(plugin.StringList), none=False)
        tm.that(str(plugin.StringSet), none=False)
