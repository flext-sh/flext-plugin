"""FLEXT Plugin Implementations - Consolidated Class Following FLEXT Patterns.

Single class containing ALL plugin implementation definitions as nested classes.
Maintains backward compatibility through property re-exports and follows
FLEXT architectural standards.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from flext_core import u
from flext_plugin import c, m, r, t

if TYPE_CHECKING:
    from flext_plugin import p


class FlextPluginImplementations:
    """Consolidated plugin implementations as nested classes."""

    class PluginDiscovery:
        """Real file-backed discovery implementing p.Plugin.Discovery.

        Discovers plugins from real files on disk and returns their
        metadata as DiscoveryData — the payload shape the platform maps
        and registers for real.

        """

        def __init__(self) -> None:
            """Initialize with empty discovered-plugin tracking."""
            self._discovered: list[str] = []

        def discover_plugin(self, plugin_path: str) -> p.Result[m.Plugin.DiscoveryData]:
            """Discover a single plugin from a real file.

            Args:
                plugin_path: Filesystem path of the plugin file.

            Returns:
                Ok with the discovery data, or Fail when the path is not
                a file.

            """
            path = Path(plugin_path)
            if not path.is_file():
                return r[m.Plugin.DiscoveryData].fail(
                    f"Plugin file not found: {plugin_path}",
                )
            self._discovered.append(path.stem)
            return r[m.Plugin.DiscoveryData].ok(
                m.Plugin.DiscoveryData(
                    name=path.stem,
                    version=c.Plugin.DEFAULT_PLUGIN_VERSION,
                    path=path,
                    discovery_type=c.Plugin.DiscoveryTypeLiteral.FILE,
                    discovery_method=c.Plugin.DiscoveryMethodLiteral.FILE_SYSTEM,
                    metadata={},
                ),
            )

        def discover_plugins(
            self,
            paths: t.StrSequence,
        ) -> p.Result[t.SequenceOf[m.Plugin.DiscoveryData]]:
            """Discover plugins from multiple paths.

            Args:
                paths: File paths and directories to scan for ``.py``
                    plugin modules.

            Returns:
                Ok with the discovery data of the discovered plugins.

            """
            results: list[m.Plugin.DiscoveryData] = []
            for path_str in paths:
                path = Path(path_str)
                if path.is_file() and path.suffix == ".py":
                    result = self.discover_plugin(path_str)
                    if result.success:
                        results.append(result.value)
                elif path.is_dir():
                    for py_file in path.rglob("*.py"):
                        if not py_file.name.startswith("_"):
                            result = self.discover_plugin(str(py_file))
                            if result.success:
                                results.append(result.value)
            return r[t.SequenceOf[m.Plugin.DiscoveryData]].ok(results)

        @staticmethod
        def validate_plugin(
            plugin_data: m.Plugin.DiscoveryData,
        ) -> p.Result[bool]:
            """Validate discovered plugin data.

            Args:
                plugin_data: Plugin data to validate; accepted and
                    treated as valid.

            Returns:
                Ok with ``True``.

            """
            _ = plugin_data
            return r[bool].ok(value=True)

    class FilePluginLoader:
        """Real file-backed loader implementing p.Plugin.Loader.

        Loads a plugin from a real .py file on disk and returns its
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

            Args:
                plugin_name: Name of the plugin to check.

            Returns:
                ``True`` when the plugin was loaded here, ``False``
                otherwise.

            """
            return plugin_name in self._loaded

        def load_plugin(self, plugin_path: str) -> p.Result[t.JsonMapping]:
            """Load a real plugin file, failing when it does not exist.

            Args:
                plugin_path: Filesystem path of the plugin file.

            Returns:
                Ok with the plugin metadata mapping, or Fail when the
                path is not a file.

            """
            path = Path(plugin_path)
            if not path.is_file():
                return r[t.JsonMapping].fail(f"Plugin file not found: {plugin_path}")
            self._loaded.append(path.stem)
            return r[t.JsonMapping].ok({
                "name": path.stem,
                "version": c.Plugin.DEFAULT_PLUGIN_VERSION,
                "path": str(path),
                "load_type": "file",
                "loaded_at": "",
            })

        def unload_plugin(self, plugin_name: str) -> p.Result[bool]:
            """Unload a previously loaded plugin.

            Args:
                plugin_name: Name of the plugin to unload.

            Returns:
                Ok with ``True`` whether or not the plugin was loaded
                here.

            """
            if plugin_name in self._loaded:
                self._loaded.remove(plugin_name)
            return r[bool].ok(value=True)

    class EchoExecutor:
        """Real executor implementing p.Plugin.Execution.

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

            Args:
                plugin_name: Name of the executed plugin.
                context: Input payload echoed back in the result.

            Returns:
                Ok with the echo payload.

            """
            self._executed.append(plugin_name)
            payload = u.json_mapping_adapter().validate_python({
                "plugin": plugin_name,
                "echo": context,
            })
            return r[t.JsonMapping].ok(payload)

        @staticmethod
        def get_execution_status(_execution_id: str) -> p.Result[str]:
            """Every execution through this executor completes.

            Args:
                _execution_id: Identifier of the execution to inspect;
                    unused because every execution completes.

            Returns:
                Ok with the ``completed`` status.

            """
            return r[str].ok("completed")

        @staticmethod
        def list_running_executions() -> t.StrSequence:
            """No execution stays running after execute_plugin returns.

            Returns:
                Empty sequence; no execution stays running.

            """
            return []

        @staticmethod
        def stop_execution(_execution_id: str) -> p.Result[bool]:
            """Stop is always a no-op success for completed executions.

            Args:
                _execution_id: Identifier of the execution to stop;
                    unused because executions complete immediately.

            Returns:
                Ok with ``True``.

            """
            return r[bool].ok(value=True)

    class FailingExecutor:
        """Real executor whose executions always fail deterministically."""

        @staticmethod
        def execute_plugin(
            plugin_name: str,
            context: t.JsonMapping,
        ) -> p.Result[t.JsonMapping]:
            """Report a real execution failure.

            Args:
                plugin_name: Name of the plugin; unused, every run fails.
                context: Input payload; unused, every run fails.

            Returns:
                Fail with the execution error.

            """
            _ = plugin_name
            _ = context
            return r[t.JsonMapping].fail("exec error")

        @staticmethod
        def get_execution_status(_execution_id: str) -> p.Result[str]:
            """Every execution through this executor fails.

            Args:
                _execution_id: Identifier of the execution to inspect;
                    unused because every execution fails.

            Returns:
                Ok with the ``failed`` status.

            """
            return r[str].ok("failed")

        @staticmethod
        def list_running_executions() -> t.StrSequence:
            """No execution stays running after a failure.

            Returns:
                Empty sequence; no execution stays running.

            """
            return []

        @staticmethod
        def stop_execution(_execution_id: str) -> p.Result[bool]:
            """Stop is always a no-op success for failed executions.

            Args:
                _execution_id: Identifier of the execution to stop;
                    unused because executions fail immediately.

            Returns:
                Ok with ``True``.

            """
            return r[bool].ok(value=True)

    class FailingDiscovery:
        """Real discovery whose operations always fail deterministically."""

        @staticmethod
        def discover_plugin(plugin_path: str) -> p.Result[m.Plugin.DiscoveryData]:
            """Report a real discovery failure for one plugin.

            Args:
                plugin_path: Path of the plugin; unused, discovery always
                    fails.

            Returns:
                Fail with the discovery error.

            """
            _ = plugin_path
            return r[m.Plugin.DiscoveryData].fail("discovery failed")

        @staticmethod
        def discover_plugins(
            paths: t.StrSequence,
        ) -> p.Result[t.SequenceOf[m.Plugin.DiscoveryData]]:
            """Report a real discovery failure for the given paths.

            Args:
                paths: Paths to scan; unused, discovery always fails.

            Returns:
                Fail with the discovery error.

            """
            _ = paths
            return r[t.SequenceOf[m.Plugin.DiscoveryData]].fail("discovery failed")

        @staticmethod
        def validate_plugin(
            plugin_data: m.Plugin.DiscoveryData,
        ) -> p.Result[bool]:
            """Report a real validation failure.

            Args:
                plugin_data: Plugin data to validate; unused, validation
                    always fails.

            Returns:
                Fail with the validation error.

            """
            _ = plugin_data
            return r[bool].fail("discovery failed")


__all__: list[str] = ["FlextPluginImplementations"]
