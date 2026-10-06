"""Test utilities for flext-plugin.

Provides TestsFlextPluginUtilities, combining TestsFlextUtilities with
FlextPluginUtilities for test-specific utility definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_tests import FlextTestsUtilities

from flext_plugin import FlextPluginUtilities, m, p, r, t


class TestsFlextPluginUtilities(FlextTestsUtilities, FlextPluginUtilities):
    """Test utilities combining TestsFlextUtilities with flext-plugin utilities."""

    class Plugin(FlextPluginUtilities.Plugin):
        """Plugin test utilities namespace."""

        class Tests:
            """Internal tests declarations.

            Real protocol-conforming collaborators injected into the platform
            service seams (``_discovery`` / ``_loader`` / ``_executor``) so tests
            exercise the real delegation and payload-mapping code paths — no
            patching or test doubles anywhere (workspace no-mock rule).
            """

            class FilePluginLoader:
                """Real file-backed loader implementing ``p.Plugin.Loader``.

                Loads a plugin from a real ``.py`` file on disk and returns its
                metadata as a mapping — the payload shape the platform maps and
                registers for real.
                """

                def __init__(self) -> None:
                    """Initialize with empty loaded-plugin tracking."""
                    self._loaded: list[str] = []

                def get_loaded_plugins(self) -> t.StrSequence:
                    """Return the names of plugins loaded through this loader."""
                    return list(self._loaded)

                def plugin_loaded(self, plugin_name: str) -> bool:
                    """Check whether a plugin was loaded through this loader.

                    Returns:
                        The resulting ``bool``.
                    """
                    return plugin_name in self._loaded

                def load_plugin(self, plugin_path: str) -> p.Result[t.JsonMapping]:
                    """Load a real plugin file, failing when it does not exist.

                    Returns:
                        The resulting ``p.Result[t.JsonMapping]``.
                    """
                    path = Path(plugin_path)
                    if not path.is_file():
                        return r[t.JsonMapping].fail(
                            f"Plugin file not found: {plugin_path}",
                        )
                    self._loaded.append(path.stem)
                    return r[t.JsonMapping].ok({
                        "name": path.stem,
                        "version": "1.0.0",
                        "path": str(path),
                        "load_type": "file",
                        "loaded_at": "",
                    })

                def unload_plugin(self, plugin_name: str) -> p.Result[bool]:
                    """Unload a previously loaded plugin.

                    Returns:
                        The resulting ``p.Result[bool]``.
                    """
                    if plugin_name in self._loaded:
                        self._loaded.remove(plugin_name)
                    return r[bool].ok(value=True)

            class EchoExecutor:
                """Real executor implementing ``p.Plugin.Execution``.

                Echoes the execution context back as the result so tests can
                assert the real execution-record bookkeeping of the platform.
                """

                def __init__(self) -> None:
                    """Initialize with empty execution tracking."""
                    self._executed: list[str] = []

                def execute_plugin(
                    self,
                    plugin_name: str,
                    context: t.JsonMapping,
                ) -> p.Result[t.JsonMapping]:
                    """Record the execution and echo the context as result.

                    Returns:
                        The resulting ``p.Result[t.JsonMapping]``.
                    """
                    self._executed.append(plugin_name)
                    # NOTE (multi-agent): pyrefly fix — heterogeneous literals go
                    # through the canonical json_mapping_adapter (same pattern as
                    # plugin_platform.py) so the r[t.JsonMapping] return type holds.
                    payload = t.json_mapping_adapter().validate_python({
                        "plugin": plugin_name,
                        "echo": context,
                    })
                    return r[t.JsonMapping].ok(payload)

                @staticmethod
                def get_execution_status(execution_id: str) -> p.Result[str]:
                    """Every execution through this executor completes.

                    Returns:
                        The resulting ``p.Result[str]``.
                    """
                    _ = execution_id
                    return r[str].ok("completed")

                @staticmethod
                def list_running_executions() -> t.StrSequence:
                    """No execution stays running after execute_plugin returns.

                    Returns:
                        The resulting ``t.StrSequence``.
                    """
                    running: t.StrSequence = []
                    return running

                @staticmethod
                def stop_execution(execution_id: str) -> p.Result[bool]:
                    """Stop is always a no-op success for completed executions.

                    Returns:
                        The resulting ``p.Result[bool]``.
                    """
                    _ = execution_id
                    return r[bool].ok(value=True)

            class FailingExecutor:
                """Real executor whose executions always fail deterministically."""

                @staticmethod
                def execute_plugin(
                    plugin_name: str,
                    context: t.JsonMapping,
                ) -> p.Result[t.JsonMapping]:
                    """Report a real execution failure.

                    Returns:
                        The resulting ``p.Result[t.JsonMapping]``.
                    """
                    _ = plugin_name
                    _ = context
                    return r[t.JsonMapping].fail("exec error")

                @staticmethod
                def get_execution_status(execution_id: str) -> p.Result[str]:
                    """Every execution through this executor fails.

                    Returns:
                        The resulting ``p.Result[str]``.
                    """
                    _ = execution_id
                    return r[str].ok("failed")

                @staticmethod
                def list_running_executions() -> t.StrSequence:
                    """No execution stays running after a failure.

                    Returns:
                        The resulting ``t.StrSequence``.
                    """
                    running: t.StrSequence = []
                    return running

                @staticmethod
                def stop_execution(execution_id: str) -> p.Result[bool]:
                    """Stop is always a no-op success for failed executions.

                    Returns:
                        The resulting ``p.Result[bool]``.
                    """
                    _ = execution_id
                    return r[bool].ok(value=True)

            class FailingDiscovery:
                """Real discovery whose operations always fail deterministically."""

                @staticmethod
                def discover_plugin(
                    plugin_path: str,
                ) -> p.Result[m.Plugin.DiscoveryData]:
                    """Report a real discovery failure for one plugin.

                    Returns:
                        The resulting ``p.Result[m.Plugin.DiscoveryData]``.
                    """
                    _ = plugin_path
                    return r[m.Plugin.DiscoveryData].fail("discovery failed")

                @staticmethod
                def discover_plugins(
                    paths: t.StrSequence,
                ) -> p.Result[t.SequenceOf[m.Plugin.DiscoveryData]]:
                    """Report a real discovery failure for the given paths.

                    Returns:
                        The resulting
                            ``p.Result[t.SequenceOf[m.Plugin.DiscoveryData]]``.
                    """
                    _ = paths
                    return r[t.SequenceOf[m.Plugin.DiscoveryData]].fail(
                        "discovery failed",
                    )

                @staticmethod
                def validate_plugin(
                    plugin_data: m.Plugin.DiscoveryData,
                ) -> p.Result[bool]:
                    """Report a real validation failure.

                    Returns:
                        The resulting ``p.Result[bool]``.
                    """
                    _ = plugin_data
                    return r[bool].fail("discovery failed")


u = TestsFlextPluginUtilities
__all__: list[str] = ["TestsFlextPluginUtilities", "u"]
