"""Behavioral tests for the plugin platform service.

Exercises the public contract of ``FlextPluginPlatform.PluginPlatformService``
and its nested ``PluginExecution`` entity: lifecycle, registry operations,
discovery/loading/execution delegation, and status reporting.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""
# mypy: warn-unused-ignores=False

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from flext_tests import tm

from flext_plugin import c
from flext_plugin.utilities import FlextPluginDiscovery, FlextPluginPlatform
from tests import u

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.usefixtures("reset_platform_state")
class TestsFlextPluginPlatformExecution:
    """Behavioral tests for plugin execution entity lifecycle."""

    @staticmethod
    @pytest.fixture
    def reset_platform_state() -> None:
        """Reset the platform service singleton state before each test."""
        FlextPluginPlatform.PluginPlatformService.fetch_global().reset_for_testing()

    @staticmethod
    def test_execution_create_generates_uuid_when_id_omitted() -> None:
        """create() assigns a UUID execution_id when none is supplied."""
        execution = FlextPluginPlatform.PluginExecution(
            plugin_name="demo",
            execution_config={"input_data": {"x": 1}},
        )

        tm.that(execution.plugin_name, eq="demo")
        assert execution.execution_id
        tm.that(execution.input_data, eq={"x": 1})
        tm.that(execution.is_running, eq=False)
        tm.that(execution.is_completed, eq=False)

    @staticmethod
    def test_execution_create_honors_explicit_id() -> None:
        """create() uses the supplied execution_id verbatim."""
        execution = FlextPluginPlatform.PluginExecution(
            plugin_name="demo",
            execution_config={},
            execution_id="exec-123",
        )

        tm.that(execution.execution_id, eq="exec-123")

    @staticmethod
    def test_execution_mark_started_sets_running_and_timestamp() -> None:
        """mark_started() transitions the execution to running."""
        execution = FlextPluginPlatform.PluginExecution(
            plugin_name="demo",
            input_data={},
        )

        execution.mark_started()

        tm.that(execution.is_running, eq=True)
        tm.that(execution.started_at, none=False)

    @staticmethod
    def test_execution_mark_completed_sets_success() -> None:
        """mark_completed(success=True) records success and timestamp."""
        execution = FlextPluginPlatform.PluginExecution(
            plugin_name="demo",
            input_data={},
        )

        execution.mark_completed(success=True)

        tm.that(execution.is_completed, eq=True)
        tm.that(execution.is_running, eq=False)
        tm.that(execution.success, eq=True)
        tm.that(execution.completed_at, none=False)

    @staticmethod
    def test_execution_mark_completed_sets_failure_and_message() -> None:
        """mark_completed(success=False) records failure and message."""
        execution = FlextPluginPlatform.PluginExecution(
            plugin_name="demo",
            input_data={},
        )

        execution.mark_completed(success=False, error_message="boom")

        tm.that(execution.is_completed, eq=True)
        tm.that(execution.success, eq=False)
        tm.that(execution.error_message, eq="boom")


@pytest.mark.usefixtures("reset_registry")
class TestsFlextPluginPlatformRegistry:
    """Behavioral tests for registry edge cases not covered elsewhere."""

    @staticmethod
    @pytest.fixture
    def reset_registry() -> None:
        """Clear class-level registry storage before each test."""
        registry = FlextPluginPlatform.PluginRegistry()
        listed = registry.list_plugins()
        if listed.success:
            for name in listed.value:
                registry.unregister(name)

    @staticmethod
    def test_registry_fetch_plugin_fails_for_unknown() -> None:
        """fetch_plugin() fails when the name is not registered."""
        registry = FlextPluginPlatform.PluginRegistry()

        result = registry.fetch_plugin("plugins", "missing")

        tm.that(result.failure, eq=True)
        tm.that((result.error or "").lower(), has="not found")

    @staticmethod
    def test_registry_list_plugins_honors_scope() -> None:
        """list_plugins() succeeds with an empty class-level registry."""
        registry = FlextPluginPlatform.PluginRegistry()

        result = registry.list_plugins()

        tm.that(result.success, eq=True)
        tm.that(result.value, eq=[])

    @staticmethod
    def test_registry_get_invalid_payload_fails() -> None:
        """get() fails gracefully when registry payload is not a plugin."""
        registry = FlextPluginPlatform.PluginRegistry()
        registry.register("bad", "not a plugin")

        result = registry.get("bad")

        tm.that(result.failure, eq=True)
        tm.that((result.error or ""), has="valid Plugin")


@pytest.mark.usefixtures("reset_service")
def _make_plugin(
    *,
    name: str = "demo-plugin",
    is_enabled: bool = True,
) -> FlextPluginPlatform.Plugin:
    """Build a platform plugin entity.

    Returns:
        The resulting ``FlextPluginPlatform.Plugin``.
    """
    plugin: FlextPluginPlatform.Plugin = FlextPluginPlatform.Plugin(
        name=name,
        plugin_version="1.0.0",
        is_enabled=is_enabled,
    )
    return plugin


class TestsFlextPluginPlatformService:
    """Behavioral tests for the plugin platform service."""

    @staticmethod
    @pytest.fixture
    def reset_service() -> None:
        """Reset platform service singleton state before each test."""
        FlextPluginPlatform.PluginPlatformService.fetch_global().reset_for_testing()

    @staticmethod
    def test_service_execute_returns_ok() -> None:
        """execute() on the platform service succeeds."""
        service = FlextPluginPlatform.PluginPlatformService()

        result = service.execute()

        tm.that(result.success, eq=True)

    @staticmethod
    def test_service_register_and_fetch_plugin() -> None:
        """register_plugin() then fetch_plugin() round-trips the plugin."""
        service = FlextPluginPlatform.PluginPlatformService()
        plugin = _make_plugin()

        result = service.register_plugin(plugin)

        tm.that(result.success, eq=True)
        tm.that(service.fetch_plugin("demo-plugin"), none=False)
        tm.that(service.fetch_plugin_status("demo-plugin"), eq="active")
        tm.that(service.resolve_plugin_active("demo-plugin"), eq=True)

    @staticmethod
    def test_service_fetch_unknown_plugin_returns_none() -> None:
        """fetch_plugin()/fetch_plugin_status()/resolve_plugin_active() on unknowns."""
        service = FlextPluginPlatform.PluginPlatformService()

        tm.that(service.fetch_plugin("missing"), none=True)
        tm.that(service.fetch_plugin_status("missing"), none=True)
        tm.that(service.resolve_plugin_active("missing"), eq=False)

    @staticmethod
    def test_service_unregister_plugin_removes_it() -> None:
        """unregister_plugin() drops the plugin from internal storage."""
        service = FlextPluginPlatform.PluginPlatformService()
        plugin = _make_plugin()
        service.register_plugin(plugin)

        result = service.unregister_plugin("demo-plugin")

        tm.that(result.success, eq=True)
        tm.that(service.fetch_plugin("demo-plugin"), none=True)

    def test_service_list_plugins_after_registration(self) -> None:
        """list_plugins() returns registered plugins."""
        service = FlextPluginPlatform.PluginPlatformService()
        service.register_plugin(self._make_plugin(name="alpha"))
        service.register_plugin(self._make_plugin(name="beta"))

        plugins = service.list_plugins()

        tm.that(len(plugins), eq=2)
        tm.that({plugin.name for plugin in plugins}, eq=frozenset({"alpha", "beta"}))

    def test_service_platform_status_reflects_state(self) -> None:
        """platform_status reports plugin and execution counts."""
        service = FlextPluginPlatform.PluginPlatformService()
        service.register_plugin(self._make_plugin(name="active"))
        service.register_plugin(self._make_plugin(name="inactive", is_enabled=False))
        execution = FlextPluginPlatform.PluginExecution(
            plugin_name="active",
            input_data={},
        )
        execution.mark_started()
        service.inject_execution("e1", execution)

        status = service.platform_status

        tm.that(status["total_plugins"], eq=2)
        tm.that(status["active_plugins"], eq=1)
        tm.that(status["total_executions"], eq=1)
        tm.that(status["running_executions"], eq=1)

    @staticmethod
    def test_service_cleanup_executions_removes_completed() -> None:
        """cleanup_executions() removes completed executions and returns count."""
        service = FlextPluginPlatform.PluginPlatformService()
        completed = FlextPluginPlatform.PluginExecution(
            plugin_name="demo",
            input_data={},
        )
        completed.mark_completed(success=True)
        running = FlextPluginPlatform.PluginExecution(plugin_name="demo", input_data={})
        running.mark_started()
        service.inject_execution("done", completed)
        service.inject_execution("run", running)

        removed = service.cleanup_executions()

        tm.that(removed, eq=1)
        tm.that(service.executions, lacks="done")
        tm.that(service.executions, has="run")

    @staticmethod
    def test_service_list_executions_and_running() -> None:
        """list_executions() and list_running_executions() filter correctly."""
        service = FlextPluginPlatform.PluginPlatformService()
        running = FlextPluginPlatform.PluginExecution(plugin_name="demo", input_data={})
        running.mark_started()
        completed = FlextPluginPlatform.PluginExecution(
            plugin_name="demo",
            input_data={},
        )
        completed.mark_completed(success=True)
        service.inject_execution("r", running)
        service.inject_execution("c", completed)

        tm.that(len(service.list_executions()), eq=2)
        tm.that(len(service.list_running_executions()), eq=1)
        assert service.fetch_execution("r") is running
        tm.that(service.fetch_execution("missing"), none=True)

    @staticmethod
    def test_service_discover_plugins_without_discovery_fails(
        tmp_path: Path,
    ) -> None:
        """discover_plugins() fails when no discovery protocol is configured."""
        service = FlextPluginPlatform.PluginPlatformService()

        result = service.discover_plugins([str(tmp_path / "nonexistent")])

        tm.that(result.failure, eq=True)
        tm.that((result.error or ""), has="Discovery")

    @staticmethod
    def test_service_load_plugin_without_loader_fails(tmp_path: Path) -> None:
        """load_plugin() fails when no loader protocol is configured."""
        service = FlextPluginPlatform.PluginPlatformService()

        result = service.load_plugin(str(tmp_path / "demo.py"))

        tm.that(result.failure, eq=True)
        tm.that((result.error or ""), has="Loader")

    @staticmethod
    def test_service_execute_plugin_without_executor_fails() -> None:
        """execute_plugin() fails when no executor protocol is configured."""
        service = FlextPluginPlatform.PluginPlatformService()
        plugin = _make_plugin()
        service.register_plugin(plugin)

        result = service.execute_plugin("demo-plugin", {})

        tm.that(result.failure, eq=True)
        tm.that((result.error or ""), has="Executor")

    @staticmethod
    def test_service_execute_plugin_unknown_fails() -> None:
        """execute_plugin() fails when plugin name is unknown."""
        service = FlextPluginPlatform.PluginPlatformService()

        result = service.execute_plugin("missing", {})

        tm.that(result.failure, eq=True)

    @staticmethod
    def test_plugin_with_invalid_version_is_rejected_at_construction() -> None:
        """Invalid semver is rejected by the real model validator at construction.

        NOTE (multi-agent): no-mock rewrite — the old test patched
        ``Plugin.validate_business_rules`` because every rule it checks (name,
        semver, type) is already enforced by Pydantic at construction; an
        invalid plugin can never reach ``register_plugin``. The real guarantee
        is that construction itself rejects the invalid version.
        """
        with pytest.raises(c.ValidationError, match="semantic"):
            FlextPluginPlatform.Plugin(name="valid-plugin", plugin_version="not-semver")

    @staticmethod
    def test_service_hot_reload_methods(tmp_path: Path) -> None:
        """Hot reload methods return success without side effects."""
        service = FlextPluginPlatform.PluginPlatformService()

        tm.that(service.start_hot_reload([str(tmp_path)]).success, eq=True)
        tm.that(service.stop_hot_reload().success, eq=True)

    @staticmethod
    def test_service_registry_property_creates_default() -> None:
        """Registry property lazily creates a registry if unset."""
        service = FlextPluginPlatform.PluginPlatformService()
        service.reset_registry()

        registry = service.registry

        tm.that(registry, none=False)


class TestsFlextPluginPlatformServiceRealComponents:
    """Service tests against real discovery, loader, and executor components."""

    @staticmethod
    def test_service_discover_plugins_with_real_discovery(tmp_path: Path) -> None:
        """discover_plugins() registers plugins found by real file-system discovery."""
        service = FlextPluginPlatform.PluginPlatformService()
        (tmp_path / "found.py").write_text(
            '"""Real plugin module."""\n',
            encoding="utf-8",
        )
        service.discovery = FlextPluginDiscovery()

        result = service.discover_plugins([str(tmp_path)])

        tm.that(result.success, eq=True)
        tm.that(service.fetch_plugin("found"), none=False)

    @staticmethod
    def test_service_load_plugin_with_real_loader(tmp_path: Path) -> None:
        """load_plugin() maps a real loader payload and registers the plugin."""
        service = FlextPluginPlatform.PluginPlatformService()
        plugin_file = tmp_path / "loaded.py"
        plugin_file.write_text('"""Real loadable plugin."""\n', encoding="utf-8")
        loader = u.Plugin.Tests.FilePluginLoader()
        service.loader = loader

        result = service.load_plugin(str(plugin_file))

        tm.that(result.success, eq=True)
        tm.that(service.fetch_plugin("loaded"), none=False)
        assert loader.plugin_loaded("loaded")

    @staticmethod
    def test_service_load_plugin_propagates_loader_failure(
        tmp_path: Path,
    ) -> None:
        """load_plugin() fails when the real loader cannot find the file."""
        service = FlextPluginPlatform.PluginPlatformService()
        service.loader = u.Plugin.Tests.FilePluginLoader()

        result = service.load_plugin(str(tmp_path / "missing.py"))

        tm.that(result.failure, eq=True)

    def test_service_execute_plugin_with_real_executor_success(self) -> None:
        """execute_plugin() records a real completed execution with the result."""
        service = FlextPluginPlatform.PluginPlatformService()
        plugin = self._make_plugin()
        service.register_plugin(plugin)
        service.executor = u.Plugin.Tests.EchoExecutor()

        result = service.execute_plugin("demo-plugin", {"x": 1}, execution_id="e1")

        tm.that(result.success, eq=True)
        execution = service.fetch_execution("e1")
        assert execution is not None
        tm.that(execution.success, eq=True)
        execution_result = execution.result
        assert isinstance(execution_result, dict)
        tm.that(execution_result["plugin"], eq="demo-plugin")

    def test_service_execute_plugin_with_real_executor_failure(self) -> None:
        """execute_plugin() fails when the real executor reports a failure."""
        service = FlextPluginPlatform.PluginPlatformService()
        plugin = self._make_plugin()
        service.register_plugin(plugin)
        service.executor = u.Plugin.Tests.FailingExecutor()

        result = service.execute_plugin("demo-plugin", {})

        tm.that(result.failure, eq=True)
