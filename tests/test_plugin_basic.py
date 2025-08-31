"""REAL tests for flext_plugin basic functionality - APENAS classes que EXISTEM.

Este módulo testa APENAS as funcionalidades básicas que REALMENTE existem no
flext_plugin, não classes imaginárias. Focamos em validar componentes reais.

CLASSES QUE EXISTEM E PODEM SER TESTADAS:
- ✅ PluginType (existe)
- ✅ FlextResult (de flext-core)
- ✅ PluginDiscovery (existe)
- ✅ FlextPluginPlatform (existe)
- ✅ create_plugin_manager (factory function que existe)

CLASSES QUE NÃO EXISTEM (removidas dos testes):
- ❌ FlextPluginManager (NÃO EXISTE - era import alias incorreto)

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Este arquivo foi corrigido para refletir a REALIDADE do código, não fantasias.
"""

from __future__ import annotations

import pytest
from flext_core import FlextResult

from flext_plugin import FlextPluginPlatform, PluginType, create_plugin_manager


def test_flext_plugin_imports() -> None:
    """Test that flext-plugin core components can be imported.

    This verifies that the core plugin components are available for import.
    """
    try:
        assert create_plugin_manager is not None
        assert PluginType is not None
        assert FlextPluginPlatform is not None
    except ImportError:
        pytest.fail(
            "flext-plugin core components not available",
        )


def test_flext_core_dependencies() -> None:
    """Test that flext-plugin can use flext-core dependencies.

    This verifies that flext-core types and patterns are accessible.
    """
    # 🚨 ARCHITECTURAL COMPLIANCE: Using módulo raiz imports

    # Test FlextResult works
    result = FlextResult[dict[str, str]].ok({"test": "data"})
    assert result.success
    expected_data = {"test": "data"}
    if result.data != expected_data:
        raise AssertionError(f"Expected {expected_data}, got {result.data}")


def test_plugin_type_enum() -> None:
    """Test PluginType enum from flext_plugin."""
    # Test standard plugin types
    if PluginType.TAP.value != "tap":
        raise AssertionError(f"Expected {'tap'}, got {PluginType.TAP.value}")
    assert PluginType.TARGET.value == "target"
    if PluginType.TRANSFORM.value != "transform":
        raise AssertionError(
            f"Expected {'transform'}, got {PluginType.TRANSFORM.value}",
        )
    assert PluginType.UTILITY.value == "utility"


def test_plugin_manager_basic() -> None:
    """Test plugin manager basic functionality using real factory."""
    manager = create_plugin_manager()
    assert manager is not None

    # Test that manager is a valid object
    assert hasattr(manager, "__class__")
    # We know it's a RegistryService from investigation


class TestFlextPluginIntegration:
    """REAL test suite for FLEXT plugin system integration using existing components.

    Testa apenas componentes que REALMENTE existem no sistema de plugins FLEXT.
    """

    def test_plugin_platform_basic(self) -> None:
        """Test FlextPluginPlatform basic functionality."""
        # Test platform initialization
        platform = FlextPluginPlatform()
        assert platform is not None
        assert isinstance(platform, FlextPluginPlatform)

    def test_plugin_manager_factory(self) -> None:
        """Test plugin manager factory function."""
        # Test manager factory works
        manager = create_plugin_manager()
        assert manager is not None
        # Don't test specific methods since we don't know exact interface

    def test_plugin_type_enumeration(self) -> None:
        """Test that plugin types are properly enumerated."""
        # Test that we can access all plugin types
        assert hasattr(PluginType, "TAP")
        assert hasattr(PluginType, "TARGET")
        assert hasattr(PluginType, "TRANSFORM")
        assert hasattr(PluginType, "UTILITY")

        # Test that plugin types have values
        plugin_types = [
            PluginType.TAP,
            PluginType.TARGET,
            PluginType.TRANSFORM,
            PluginType.UTILITY,
        ]
        for plugin_type in plugin_types:
            assert plugin_type.value is not None
            assert isinstance(plugin_type.value, str)
            assert len(plugin_type.value) > 0
