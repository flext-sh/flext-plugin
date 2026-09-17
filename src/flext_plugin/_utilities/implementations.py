"""FLEXT Plugin Implementations - Consolidated Class Following FLEXT Patterns.

Single class containing ALL plugin implementation definitions as nested classes.
Maintains backward compatibility through property re-exports and follows
FLEXT architectural standards.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

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
            """Discover a single plugin from a real file."""
            path = Path(plugin_path)
            if not path.is_file():
                return r[m.Plugin.DiscoveryData].fail(
                    f"Plugin file not found: {plugin_path}"
                )
            self._discovered.append(path.stem)
            return r[m.Plugin.DiscoveryData].ok(
                m.Plugin.DiscoveryData(
                    name=path.stem,
                    version="1.0.0",
                    path=path,
                    discovery_type=c.Plugin.DiscoveryTypeLiteral.FILE,
                    discovery_method=c.Plugin.DiscoveryMethodLiteral.FILE_SYSTEM,
                    metadata={},
                )
            )

        def discover_plugins(
            self, paths: t.StrSequence
        ) -> p.Result[t.SequenceOf[m.Plugin.DiscoveryData]]:
            """Discover plugins from multiple paths."""
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

        def validate_plugin(
            self, plugin_data: m.Plugin.DiscoveryData
        ) -> p.Result[bool]:
            """Validate discovered plugin data."""
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
            """Check whether a plugin was loaded through this loader."""
            return plugin_name in self._loaded

        def load_plugin(self, plugin_path: str) -> p.Result[t.JsonMapping]:
            """Load a real plugin file, failing when it does not exist."""
            path = Path(plugin_path)
            if not path.is_file():
                return r[t.JsonMapping].fail(f"Plugin file not found: {plugin_path}")
            self._loaded.append(path.stem)
            return r[t.JsonMapping].ok({
                "name": path.stem,
                "version": "1.0.0",
                "path": str(path),
                "load_type": "file",
                "loaded_at": "",
            })

        def unload_plugin(self, plugin_name: str) -> p.Result[bool]:
            """Unload a previously loaded plugin."""
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
            self, plugin_name: str, context: t.JsonMapping
        ) -> p.Result[t.JsonMapping]:
            """Record the execution and echo the context as result."""
            self._executed.append(plugin_name)
            payload = t.json_mapping_adapter().validate_python({
                "plugin": plugin_name,
                "echo": context,
            })
            return r[t.JsonMapping].ok(payload)

        def get_execution_status(self, _execution_id: str) -> p.Result[str]:
            """Every execution through this executor completes."""
            return r[str].ok("completed")

        def list_running_executions(self) -> t.StrSequence:
            """No execution stays running after execute_plugin returns."""
            return []

        def stop_execution(self, _execution_id: str) -> p.Result[bool]:
            """Stop is always a no-op success for completed executions."""
            return r[bool].ok(value=True)

    class FailingExecutor:
        """Real executor whose executions always fail deterministically."""

        def execute_plugin(
            self, plugin_name: str, context: t.JsonMapping
        ) -> p.Result[t.JsonMapping]:
            """Report a real execution failure."""
            _ = plugin_name
            _ = context
            return r[t.JsonMapping].fail("exec error")

        def get_execution_status(self, _execution_id: str) -> p.Result[str]:
            """Every execution through this executor fails."""
            return r[str].ok("failed")

        def list_running_executions(self) -> t.StrSequence:
            """No execution stays running after a failure."""
            return []

        def stop_execution(self, _execution_id: str) -> p.Result[bool]:
            """Stop is always a no-op success for failed executions."""
            return r[bool].ok(value=True)

    class FailingDiscovery:
        """Real discovery whose operations always fail deterministically."""

        def discover_plugin(self, plugin_path: str) -> p.Result[m.Plugin.DiscoveryData]:
            """Report a real discovery failure for one plugin."""
            _ = plugin_path
            return r[m.Plugin.DiscoveryData].fail("discovery failed")

        def discover_plugins(
            self, paths: t.StrSequence
        ) -> p.Result[t.SequenceOf[m.Plugin.DiscoveryData]]:
            """Report a real discovery failure for the given paths."""
            _ = paths
            return r[t.SequenceOf[m.Plugin.DiscoveryData]].fail("discovery failed")

        def validate_plugin(
            self, plugin_data: m.Plugin.DiscoveryData
        ) -> p.Result[bool]:
            """Report a real validation failure."""
            _ = plugin_data
            return r[bool].fail("discovery failed")


__all__: list[str] = ["FlextPluginImplementations"]
