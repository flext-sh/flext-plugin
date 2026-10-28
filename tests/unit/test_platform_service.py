"""Public plugin execution, state reporting, and failure lifecycle scenarios.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from typing import TYPE_CHECKING

from flext_plugin import FlextPluginApi
from tests import c, m, tm, u

if TYPE_CHECKING:
    from pathlib import Path


class TestsFlextPluginPlatformService:
    """The API executes the inherited service rather than a separate platform."""

    @staticmethod
    def test_execution_model_defaults_come_from_its_owner() -> None:
        """Execution state and generated identifiers belong to the existing model."""
        first = m.Plugin.Execution(plugin_name="execution-plugin", input_data={"x": 1})
        second = m.Plugin.Execution(plugin_name=first.plugin_name, input_data={})
        tm.that(first.execution_id, truth=True)
        tm.that(second.execution_id, truth=True)
        tm.that(first.execution_id != second.execution_id, truth=True)
        tm.that(first.input_data, eq={"x": 1})
        for field_name in ("is_running", "is_completed", "success"):
            tm.that(
                first.model_dump()[field_name],
                eq=m.Plugin.Execution.model_fields[field_name].default,
            )

    @staticmethod
    def test_execution_honors_explicit_id_and_records_completed_state() -> None:
        """A real executor run owns timestamps, result, identity, and cleanup."""
        api = FlextPluginApi(executor=u.Plugin.Tests.EchoExecutor())
        payload = m.Plugin.Entity(name="executed-plugin")
        tm.ok(api.register_plugin(payload))
        tm.that(api.list_executions(), eq=[])
        tm.that(api.list_running_executions(), eq=[])
        result = api.execute_plugin(payload.name, {"x": 1}, execution_id="caller-run")
        execution = tm.ok(result)
        tm.that(execution.execution_id, eq="caller-run")
        tm.that(execution.input_data, eq={"x": 1})
        tm.fail(execution.is_running)
        tm.ok(execution.is_completed)
        tm.ok(execution.success)
        tm.not_none(execution.started_at)
        tm.not_none(execution.completed_at)
        tm.that(execution.error_message is None, truth=True)
        output = tm.not_none(execution.result)
        tm.that(output["plugin"], eq=payload.name)
        tm.that(output["echo"], eq=execution.input_data)
        tm.that(api.fetch_execution(execution.execution_id) is execution, truth=True)
        tm.that(api.list_executions()[0] is execution, truth=True)
        tm.that(api.list_running_executions(), eq=[])
        tm.that(api.fetch_execution("absent-execution") is None, truth=True)
        tm.that(api.cleanup_executions(), eq=1)
        tm.that(api.list_executions(), eq=[])
        tm.that(api.cleanup_executions(), eq=0)

    @staticmethod
    def test_execution_without_explicit_id_uses_owned_generator() -> None:
        """The execution operation uses the canonical model's identifier factory."""
        api = FlextPluginApi(executor=u.Plugin.Tests.EchoExecutor())
        payload = m.Plugin.Entity(name="generated-run-plugin")
        tm.ok(api.register_plugin(payload))
        first = tm.ok(api.execute_plugin(payload.name, {}))
        second = tm.ok(api.execute_plugin(payload.name, {}))
        tm.that(first.execution_id, truth=True)
        tm.that(first.execution_id != second.execution_id, truth=True)
        tm.that(len(api.list_executions()), eq=2)
        tm.that(api.cleanup_executions(), eq=2)

    @staticmethod
    def test_failed_executor_run_is_recorded_without_false_success() -> None:
        """Failure and the tracked execution expose the same error."""
        api = FlextPluginApi(executor=u.Plugin.Tests.FailingExecutor())
        payload = m.Plugin.Entity(name="failed-run-plugin")
        tm.ok(api.register_plugin(payload))
        result = api.execute_plugin(payload.name, {}, execution_id="failed-run")
        tm.fail(result)
        execution = tm.not_none(api.fetch_execution("failed-run"))
        tm.ok(execution.is_completed)
        tm.fail(execution.is_running)
        tm.fail(execution.success)
        tm.that(execution.error_message, eq=result.error)
        tm.that(execution.result is None, truth=True)
        tm.not_none(execution.started_at)
        tm.not_none(execution.completed_at)
        tm.that(api.list_running_executions(), eq=[])
        tm.that(api.cleanup_executions(), eq=1)

    @staticmethod
    def test_unknown_plugin_and_absent_executor_do_not_create_executions() -> None:
        """Prerequisite failures cannot manufacture a completed execution."""
        api = FlextPluginApi()
        tm.fail(api.execute_plugin("missing-plugin", {}))
        payload = m.Plugin.Entity(name="no-executor-plugin")
        tm.ok(api.register_plugin(payload))
        tm.fail(api.execute_plugin(payload.name, {}))
        tm.that(api.list_executions(), eq=[])

    @staticmethod
    def test_status_and_transport_snapshot_observe_real_state() -> None:
        """Snapshot serialization preserves metadata without replacing payloads."""
        api = FlextPluginApi(executor=u.Plugin.Tests.EchoExecutor())
        active = m.Plugin.Entity(name="active-plugin", is_enabled=True, author="Caller")
        inactive = m.Plugin.Entity(
            name="inactive-plugin", is_enabled=False, metadata={"source": "caller"}
        )
        tm.ok(api.register_plugin(active))
        tm.ok(api.register_plugin(inactive))
        tm.ok(api.execute_plugin(active.name, {}))
        status = api.platform_status
        tm.that(status["total_plugins"], eq=len(api.list_plugins().value))
        tm.that(
            status["active_plugins"],
            eq=sum(payload.is_enabled for payload in api.list_plugins().value),
        )
        tm.that(status["total_executions"], eq=len(api.list_executions()))
        tm.that(status["running_executions"], eq=len(api.list_running_executions()))
        snapshot = tm.ok(api.execute())
        tm.that(snapshot.version, eq=c.Plugin.DEFAULT_PLUGIN_VERSION)
        serialized = u.json_mapping_adapter().validate_python(
            snapshot.plugins[active.name]
        )
        tm.that(serialized["author"], eq=active.author)
        serialized_inactive = u.json_mapping_adapter().validate_python(
            snapshot.plugins[inactive.name]
        )
        tm.that(serialized_inactive["metadata"], eq=inactive.metadata)
        tm.that(api.fetch_plugin(active.name).value is active, truth=True)
        tm.that(api.fetch_plugin(inactive.name).value is inactive, truth=True)

    @staticmethod
    def test_missing_discovery_and_loader_are_failed_prerequisites(
        tmp_path: Path,
    ) -> None:
        """Optional adapters do not cause hidden construction on first access."""
        api = FlextPluginApi()
        tm.fail(api.discover_plugins([str(tmp_path)]))
        tm.fail(api.load_plugin(str(tmp_path / "missing.py")))
        tm.that(api.list_plugins().value, eq=[])

    @staticmethod
    def test_hot_reload_preserves_existing_lifecycle_contract(tmp_path: Path) -> None:
        """The registry migration does not change the existing hot-reload behavior."""
        api = FlextPluginApi()
        tm.ok(api.start_hot_reload([str(tmp_path)]))
        tm.ok(api.stop_hot_reload())
        tm.that(api.list_plugins().value, eq=[])
        tm.that(api.list_executions(), eq=[])
