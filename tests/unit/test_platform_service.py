"""Behavioral tests for the plugin platform service.

Exercises the public contract of ``FlextPluginPlatform.PluginPlatformService``
and its nested ``PluginExecution`` entity: lifecycle, registry operations,
discovery/loading/execution delegation, and status reporting.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""
# mypy: warn-unused-ignores=False

from __future__ import annotations

from pathlib import Path

import pytest

from flext_plugin import c
from flext_plugin._utilities.discovery import FlextPluginDiscovery
from flext_plugin._utilities.plugin_platform import FlextPluginPlatform
from tests.utilities import u

Platform = FlextPluginPlatform


@pytest.mark.usefixtures("reset_platform_state")
class TestsFlextPluginPlatformExecution:
    """Behavioral tests for plugin execution entity lifecycle."""

    @pytest.fixture
    def reset_platform_state(self) -> None:
        """Reset the platform service singleton state before each test."""
        Platform.PluginPlatformService.fetch_global().reset_for_testing()

    def test_execution_create_generates_uuid_when_id_omitted(self) -> None:
        """create() assigns a UUID execution_id when none is supplied."""
        execution = Platform.PluginExecution.create(
            plugin_name="demo",
            execution_config={"input_data": {"x": 1}},
        )

        assert execution.plugin_name == "demo"
        assert execution.execution_id
        assert execution.input_data == {"x": 1}
        assert execution.is_running is False
        assert execution.is_completed is False

    def test_execution_create_honors_explicit_id(self) -> None:
        """create() uses the supplied execution_id verbatim."""
        execution = Platform.PluginExecution.create(
            plugin_name="demo",
            execution_config={},
            execution_id="exec-123",
        )

        assert execution.execution_id == "exec-123"

    def test_execution_mark_started_sets_running_and_timestamp(self) -> None:
        """mark_started() transitions the execution to running."""
        execution = Platform.PluginExecution.create("demo", {})

        execution.mark_started()

        assert execution.is_running is True
        assert execution.started_at is not None

    def test_execution_mark_completed_sets_success(self) -> None:
        """mark_completed(success=True) records success and timestamp."""
        execution = Platform.PluginExecution.create("demo", {})

        execution.mark_completed(success=True)

        assert execution.is_completed is True
        assert execution.is_running is False
        assert execution.success is True
        assert execution.completed_at is not None

    def test_execution_mark_completed_sets_failure_and_message(self) -> None:
        """mark_completed(success=False) records failure and message."""
        execution = Platform.PluginExecution.create("demo", {})

        execution.mark_completed(success=False, error_message="boom")

        assert execution.is_completed is True
        assert execution.success is False
        assert execution.error_message == "boom"


@pytest.mark.usefixtures("reset_registry")
class TestsFlextPluginPlatformRegistry:
    """Behavioral tests for registry edge cases not covered elsewhere."""

    @pytest.fixture
    def reset_registry(self) -> None:
        """Clear class-level registry storage before each test."""
        registry = Platform.PluginRegistry.create()
        listed = registry.list_plugins()
        if listed.success:
            for name in listed.value:
                registry.unregister(name)

    def test_registry_fetch_plugin_fails_for_unknown(self) -> None:
        """fetch_plugin() fails when the name is not registered."""
        registry = Platform.PluginRegistry.create()

        result = registry.fetch_plugin("plugins", "missing")

        assert result.failure is True
        assert "not found" in (result.error or "").lower()

    def test_registry_list_plugins_honors_scope(self) -> None:
        """list_plugins() succeeds with an empty class-level registry."""
        registry = Platform.PluginRegistry.create()

        result = registry.list_plugins()

        assert result.success is True
        assert result.value == []

    def test_registry_get_invalid_payload_fails(self) -> None:
        """get() fails gracefully when registry payload is not a plugin."""
        registry = Platform.PluginRegistry.create()
        registry.register("bad", "not a plugin")

        result = registry.get("bad")

        assert result.failure is True
        assert "valid Plugin" in (result.error or "")


@pytest.mark.usefixtures("reset_service")
class TestsFlextPluginPlatformService:
    """Behavioral tests for the plugin platform service."""

    @pytest.fixture
    def reset_service(self) -> None:
        """Reset platform service singleton state before each test."""
        Platform.PluginPlatformService.fetch_global().reset_for_testing()

    @staticmethod
    def _make_plugin(
        *,
        name: str = "demo-plugin",
        is_enabled: bool = True,
    ) -> Platform.Plugin:
        """Build a platform plugin entity."""
        plugin: Platform.Plugin = Platform.Plugin.create(
            name=name,
            plugin_version="1.0.0",
            is_enabled=is_enabled,
        )
        return plugin

    def test_service_execute_returns_ok(self) -> None:
        """execute() on the platform service succeeds."""
        service = Platform.PluginPlatformService()

        result = service.execute()

        assert result.success is True

    def test_service_register_and_fetch_plugin(self) -> None:
        """register_plugin() then fetch_plugin() round-trips the plugin."""
        service = Platform.PluginPlatformService()
        plugin = self._make_plugin()

        result = service.register_plugin(plugin)

        assert result.success is True
        assert service.fetch_plugin("demo-plugin") is not None
        assert service.fetch_plugin_status("demo-plugin") == "active"
        assert service.resolve_plugin_active("demo-plugin") is True

    def test_service_fetch_unknown_plugin_returns_none(self) -> None:
        """fetch_plugin(), fetch_plugin_status() and resolve_plugin_active() handle unknowns."""
        service = Platform.PluginPlatformService()

        assert service.fetch_plugin("missing") is None
        assert service.fetch_plugin_status("missing") is None
        assert service.resolve_plugin_active("missing") is False

    def test_service_unregister_plugin_removes_it(self) -> None:
        """unregister_plugin() drops the plugin from internal storage."""
        service = Platform.PluginPlatformService()
        plugin = self._make_plugin()
        service.register_plugin(plugin)

        result = service.unregister_plugin("demo-plugin")

        assert result.success is True
        assert service.fetch_plugin("demo-plugin") is None

    def test_service_list_plugins_after_registration(self) -> None:
        """list_plugins() returns registered plugins."""
        service = Platform.PluginPlatformService()
        service.register_plugin(self._make_plugin(name="alpha"))
        service.register_plugin(self._make_plugin(name="beta"))

        plugins = service.list_plugins()

        assert len(plugins) == 2
        assert {plugin.name for plugin in plugins} == {"alpha", "beta"}

    def test_service_platform_status_reflects_state(self) -> None:
        """platform_status reports plugin and execution counts."""
        service = Platform.PluginPlatformService()
        service.register_plugin(self._make_plugin(name="active"))
        service.register_plugin(self._make_plugin(name="inactive", is_enabled=False))
        execution = Platform.PluginExecution.create("active", {})
        execution.mark_started()
        service._executions["e1"] = execution

        status = service.platform_status

        assert status["total_plugins"] == 2
        assert status["active_plugins"] == 1
        assert status["total_executions"] == 1
        assert status["running_executions"] == 1

    def test_service_cleanup_executions_removes_completed(self) -> None:
        """cleanup_executions() removes completed executions and returns count."""
        service = Platform.PluginPlatformService()
        completed = Platform.PluginExecution.create("demo", {})
        completed.mark_completed(success=True)
        running = Platform.PluginExecution.create("demo", {})
        running.mark_started()
        service._executions["done"] = completed
        service._executions["run"] = running

        removed = service.cleanup_executions()

        assert removed == 1
        assert "done" not in service.executions
        assert "run" in service.executions

    def test_service_list_executions_and_running(self) -> None:
        """list_executions() and list_running_executions() filter correctly."""
        service = Platform.PluginPlatformService()
        running = Platform.PluginExecution.create("demo", {})
        running.mark_started()
        completed = Platform.PluginExecution.create("demo", {})
        completed.mark_completed(success=True)
        service._executions["r"] = running
        service._executions["c"] = completed

        assert len(service.list_executions()) == 2
        assert len(service.list_running_executions()) == 1
        assert service.fetch_execution("r") is running
        assert service.fetch_execution("missing") is None

    def test_service_discover_plugins_without_discovery_fails(self) -> None:
        """discover_plugins() fails when no discovery protocol is configured."""
        service = Platform.PluginPlatformService()

        result = service.discover_plugins(["/tmp"])

        assert result.failure is True
        assert "Discovery" in (result.error or "")

    def test_service_load_plugin_without_loader_fails(self) -> None:
        """load_plugin() fails when no loader protocol is configured."""
        service = Platform.PluginPlatformService()

        result = service.load_plugin("/tmp/demo.py")

        assert result.failure is True
        assert "Loader" in (result.error or "")

    def test_service_execute_plugin_without_executor_fails(self) -> None:
        """execute_plugin() fails when no executor protocol is configured."""
        service = Platform.PluginPlatformService()
        plugin = self._make_plugin()
        service.register_plugin(plugin)

        result = service.execute_plugin("demo-plugin", {})

        assert result.failure is True
        assert "Executor" in (result.error or "")

    def test_service_execute_plugin_unknown_fails(self) -> None:
        """execute_plugin() fails when plugin name is unknown."""
        service = Platform.PluginPlatformService()

        result = service.execute_plugin("missing", {})

        assert result.failure is True

    def test_service_discover_plugins_with_real_discovery(
        self,
        tmp_path: Path,
    ) -> None:
        """discover_plugins() registers plugins found by real file-system discovery."""
        service = Platform.PluginPlatformService()
        (tmp_path / "found.py").write_text(
            '"""Real plugin module."""\n',
            encoding="utf-8",
        )
        service._discovery = FlextPluginDiscovery()

        result = service.discover_plugins([str(tmp_path)])

        assert result.success is True
        assert service.fetch_plugin("found") is not None

    def test_service_load_plugin_with_real_loader(self, tmp_path: Path) -> None:
        """load_plugin() maps a real loader payload and registers the plugin."""
        service = Platform.PluginPlatformService()
        plugin_file = tmp_path / "loaded.py"
        plugin_file.write_text('"""Real loadable plugin."""\n', encoding="utf-8")
        loader = u.Plugin.Tests.FilePluginLoader()
        service._loader = loader

        result = service.load_plugin(str(plugin_file))

        assert result.success is True
        assert service.fetch_plugin("loaded") is not None
        assert loader.plugin_loaded("loaded")

    def test_service_load_plugin_propagates_loader_failure(
        self,
        tmp_path: Path,
    ) -> None:
        """load_plugin() fails when the real loader cannot find the file."""
        service = Platform.PluginPlatformService()
        service._loader = u.Plugin.Tests.FilePluginLoader()

        result = service.load_plugin(str(tmp_path / "missing.py"))

        assert result.failure is True

    def test_service_execute_plugin_with_real_executor_success(self) -> None:
        """execute_plugin() records a real completed execution with the result."""
        service = Platform.PluginPlatformService()
        plugin = self._make_plugin()
        service.register_plugin(plugin)
        service._executor = u.Plugin.Tests.EchoExecutor()

        result = service.execute_plugin("demo-plugin", {"x": 1}, execution_id="e1")

        assert result.success is True
        execution = service.fetch_execution("e1")
        assert execution is not None
        assert execution.success is True
        assert execution.result is not None
        assert execution.result["plugin"] == "demo-plugin"

    def test_service_execute_plugin_with_real_executor_failure(self) -> None:
        """execute_plugin() fails when the real executor reports a failure."""
        service = Platform.PluginPlatformService()
        plugin = self._make_plugin()
        service.register_plugin(plugin)
        service._executor = u.Plugin.Tests.FailingExecutor()

        result = service.execute_plugin("demo-plugin", {})

        assert result.failure is True

    def test_plugin_with_invalid_version_is_rejected_at_construction(self) -> None:
        """Invalid semver is rejected by the real model validator at construction.

        NOTE (multi-agent): no-mock rewrite — the old test patched
        ``Plugin.validate_business_rules`` because every rule it checks (name,
        semver, type) is already enforced by Pydantic at construction; an
        invalid plugin can never reach ``register_plugin``. The real guarantee
        is that construction itself rejects the invalid version.
        """
        with pytest.raises(c.ValidationError, match="semantic"):
            Platform.Plugin.create(
                name="valid-plugin",
                plugin_version="not-semver",
            )

    def test_service_hot_reload_methods(self) -> None:
        """Hot reload methods return success without side effects."""
        service = Platform.PluginPlatformService()

        assert service.start_hot_reload(["/tmp"]).success is True
        assert service.stop_hot_reload().success is True

    def test_service_registry_property_creates_default(self) -> None:
        """Registry property lazily creates a registry if unset."""
        service = Platform.PluginPlatformService()
        service._registry = None

        registry = service.registry

        assert registry is not None


__all__: list[str] = [
    "TestsFlextPluginPlatformExecution",
    "TestsFlextPluginPlatformRegistry",
    "TestsFlextPluginPlatformService",
]
