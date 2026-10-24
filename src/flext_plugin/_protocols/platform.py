"""Public plugin platform capabilities.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from flext_plugin import p, t


class FlextPluginProtocolsPlatform:
    """Structural public service boundary."""

    @runtime_checkable
    class PlatformService(Protocol):
        """Operations exposed directly by the MRO API."""

        @property
        def registry(self) -> p.Registry: ...

        def register_plugin(self, plugin: p.Plugin.Instance) -> p.Result[bool]: ...

        def unregister_plugin(self, plugin_name: str) -> p.Result[bool]: ...

        def fetch_plugin(self, plugin_name: str) -> p.Result[p.Plugin.Instance]: ...

        def fetch_plugin_status(self, plugin_name: str) -> p.Result[str]: ...

        def resolve_plugin_active(self, plugin_name: str) -> p.Result[bool]: ...

        def list_plugins(self) -> p.Result[t.SequenceOf[p.Plugin.Instance]]: ...

        def discover_plugins(
            self, paths: t.StrSequence
        ) -> p.Result[t.SequenceOf[p.Plugin.Instance]]: ...

        def load_plugin(self, plugin_path: str) -> p.Result[p.Plugin.Instance]: ...

        def execute_plugin(
            self,
            plugin_name: str,
            context: t.JsonMapping,
            execution_id: str | None = None,
        ) -> p.Result[p.Plugin.Run]: ...

        def execute(self) -> p.Result[p.Plugin.Snapshot]: ...

        def fetch_execution(self, eid: str) -> p.Plugin.Run | None: ...

        def list_executions(self) -> t.SequenceOf[p.Plugin.Run]: ...

        def list_running_executions(self) -> t.SequenceOf[p.Plugin.Run]: ...

        def cleanup_executions(self) -> int: ...

        @property
        def platform_status(self) -> t.JsonMapping: ...

        def start_hot_reload(self, paths: t.StrSequence) -> p.Result[bool]: ...

        def stop_hot_reload(self) -> p.Result[bool]: ...


__all__: list[str] = ["FlextPluginProtocolsPlatform"]
