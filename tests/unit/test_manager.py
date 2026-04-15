"""Test suite for flext_plugin manager components.

Tests the actual plugin service and manager functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import asyncio
from collections.abc import Mapping, MutableSequence, Sequence
from types import ModuleType
from typing import override

import pytest

from flext_core import r
from flext_plugin import FlextPluginAdapters, FlextPluginService
from tests import m, p, t


class TestFlextPluginService:
    """Tests for FlextPluginService class."""

    @pytest.fixture
    def service(self) -> FlextPluginService:
        """Create service instance for testing."""
        return FlextPluginService()

    def test_initialization(self, service: FlextPluginService) -> None:
        """Test service initialization."""
        assert service is not None

    def test_class_exists(self) -> None:
        """Test that FlextPluginService class exists and is callable."""
        assert FlextPluginService is not None
        assert callable(FlextPluginService)


class TestFlextPluginServiceStubBridges:
    """Tests for FlextPluginService stub bridges."""

    def test_discovery_calls_security_registry_and_monitoring(self) -> None:

        class Discovery(FlextPluginAdapters.FileSystemDiscoveryAdapter):
            @override
            def discover_plugins(
                self,
                paths: t.StrSequence,
            ) -> p.Result[Sequence[t.RecursiveContainerMapping]]:
                _ = paths
                return r[Sequence[t.RecursiveContainerMapping]].ok([
                    {
                        "name": "stub_plugin",
                        "version": "1.0.0",
                        "metadata": {"plugin_type": "utility"},
                    },
                ])

        class Security(FlextPluginAdapters.PluginSecurityAdapter):
            def __init__(self) -> None:
                super().__init__()
                self.calls = 0

            @override
            def validate_plugin_security(
                self, _plugin: t.RecursiveContainer
            ) -> p.Result[bool]:
                self.calls += 1
                return r[bool].ok(True)

        class Registry(FlextPluginAdapters.MemoryRegistryAdapter):
            def __init__(self) -> None:
                super().__init__()
                self.registered: MutableSequence[str] = []

            @override
            def register_plugin(
                self,
                _plugin: m.Plugin.Plugin | t.RecursiveContainer,
            ) -> p.Result[bool]:
                if isinstance(_plugin, Mapping):
                    self.registered.append(str(_plugin.get("name", "")))
                else:
                    self.registered.append("")
                return r[bool].ok(True)

        class Monitoring(FlextPluginAdapters.PluginMonitoringAdapter):
            def __init__(self) -> None:
                super().__init__()
                self.started: MutableSequence[str] = []

            @override
            def start_monitoring(self, _plugin_name: str) -> p.Result[bool]:
                self.started.append(_plugin_name)
                return r[bool].ok(True)

        security = Security()
        registry = Registry()
        monitoring = Monitoring()
        service = FlextPluginService(
            discovery=Discovery(),
            security=security,
            registry=registry,
            monitoring=monitoring,
        )
        result = service.discover_and_register_plugins(["/tmp"])
        assert result.success
        assert len(result.unwrap()) == 1
        assert security.calls == 1
        assert registry.registered == ["stub_plugin"]
        assert monitoring.started == ["stub_plugin"]

    def test_load_plugin_calls_security_registry_and_monitoring(self) -> None:

        class Loader(FlextPluginAdapters.DynamicLoaderAdapter):
            @override
            def load_plugin(
                self,
                plugin_path: str,
            ) -> p.Result[t.RecursiveContainerMapping]:
                _ = plugin_path
                return r[t.RecursiveContainerMapping].ok({
                    "name": "stub_plugin",
                    "version": "1.0.0",
                    "metadata": {"plugin_type": "utility"},
                })

        class Security(FlextPluginAdapters.PluginSecurityAdapter):
            def __init__(self) -> None:
                super().__init__()
                self.calls = 0

            @override
            def validate_plugin_security(
                self, _plugin: t.RecursiveContainer
            ) -> p.Result[bool]:
                self.calls += 1
                return r[bool].ok(True)

        class Registry(FlextPluginAdapters.MemoryRegistryAdapter):
            def __init__(self) -> None:
                super().__init__()
                self.registered: MutableSequence[str] = []

            @override
            def register_plugin(
                self,
                _plugin: m.Plugin.Plugin | t.RecursiveContainer,
            ) -> p.Result[bool]:
                if isinstance(_plugin, Mapping):
                    self.registered.append(str(_plugin.get("name", "")))
                else:
                    self.registered.append("")
                return r[bool].ok(True)

        class Monitoring(FlextPluginAdapters.PluginMonitoringAdapter):
            def __init__(self) -> None:
                super().__init__()
                self.started: MutableSequence[str] = []

            @override
            def start_monitoring(self, _plugin_name: str) -> p.Result[bool]:
                self.started.append(_plugin_name)
                return r[bool].ok(True)

        security = Security()
        registry = Registry()
        monitoring = Monitoring()
        service = FlextPluginService(
            loader=Loader(),
            security=security,
            registry=registry,
            monitoring=monitoring,
        )
        result = service.load_plugin("/tmp/stub_plugin.py")
        assert result.success
        assert security.calls == 1
        assert registry.registered == ["stub_plugin"]
        assert monitoring.started == ["stub_plugin"]

    def test_execute_plugin_uses_executor_adapter_result(self) -> None:

        class Loader(FlextPluginAdapters.DynamicLoaderAdapter):
            @override
            def load_plugin(
                self,
                plugin_path: str,
            ) -> p.Result[t.RecursiveContainerMapping]:
                _ = plugin_path
                return r[t.RecursiveContainerMapping].ok({
                    "name": "stub_plugin",
                    "version": "1.0.0",
                    "metadata": {"plugin_type": "utility"},
                })

        class Executor(FlextPluginAdapters.PluginExecutorAdapter):
            def __init__(self) -> None:
                super().__init__()
                self.calls: MutableSequence[str] = []

            @override
            def execute_plugin(
                self,
                _plugin_name: str,
                _context: t.RecursiveContainerMapping,
            ) -> p.Result[t.RecursiveContainerMapping]:
                self.calls.append(_plugin_name)
                return r[t.RecursiveContainerMapping].ok({
                    "status": "executed",
                    "plugin": _plugin_name,
                })

        executor = Executor()
        service = FlextPluginService(loader=Loader(), executor=executor)
        load_result = service.load_plugin("/tmp/stub_plugin.py")
        assert load_result.success
        result = service.execute_plugin("stub_plugin", {})
        assert result.success
        execution = result.unwrap()
        assert execution.result == {"status": "executed", "plugin": "stub_plugin"}
        assert executor.calls == ["stub_plugin"]

    def test_unload_plugin_calls_monitoring_registry_and_loader(self) -> None:

        class Loader(FlextPluginAdapters.DynamicLoaderAdapter):
            def __init__(self) -> None:
                super().__init__()
                self.unloaded: MutableSequence[str] = []

            @override
            def load_plugin(
                self,
                plugin_path: str,
            ) -> p.Result[t.RecursiveContainerMapping]:
                _ = plugin_path
                self._loaded_plugins["stub_plugin"] = ModuleType("stub_plugin")
                return r[t.RecursiveContainerMapping].ok({
                    "name": "stub_plugin",
                    "version": "1.0.0",
                    "metadata": {"plugin_type": "utility"},
                })

            @override
            def unload_plugin(self, plugin_name: str) -> p.Result[bool]:
                self.unloaded.append(plugin_name)
                return super().unload_plugin(plugin_name)

        class Registry(FlextPluginAdapters.MemoryRegistryAdapter):
            def __init__(self) -> None:
                super().__init__()
                self.unregistered: MutableSequence[str] = []

            @override
            def unregister_plugin(self, plugin_name: str) -> p.Result[bool]:
                self.unregistered.append(plugin_name)
                return r[bool].ok(True)

        class Monitoring(FlextPluginAdapters.PluginMonitoringAdapter):
            def __init__(self) -> None:
                super().__init__()
                self.stopped: MutableSequence[str] = []

            @override
            def stop_monitoring(self, _plugin_name: str) -> p.Result[bool]:
                self.stopped.append(_plugin_name)
                return r[bool].ok(True)

        loader = Loader()
        registry = Registry()
        monitoring = Monitoring()
        service = FlextPluginService(
            loader=loader,
            registry=registry,
            monitoring=monitoring,
        )
        load_result = service.load_plugin("/tmp/stub_plugin.py")
        assert load_result.success
        unload_result = asyncio.run(service.unload_plugin("stub_plugin"))
        assert unload_result.success
        assert monitoring.stopped == ["stub_plugin"]
        assert registry.unregistered == ["stub_plugin"]
        assert loader.unloaded == ["stub_plugin"]
        assert service.plugin_loaded("stub_plugin") is False
