# from flext-plugin/docs/architecture/implementation.md:286
# flext_plugin/protocols.py - Structural typing protocols
from __future__ import annotations

import typing
from flext_plugin import FlextPluginModels


class FlextPluginProtocols:
    """typing.Protocol definitions for plugin system interfaces."""

    class PluginDiscovery(typing.Protocol):
        """typing.Protocol for plugin discovery mechanisms."""

        async def discover_plugins(
            self, paths: t.StringList
        ) -> p.Result[list[dict[str, t.JsonValue]]]:
            """Discover plugins from specified paths."""
            ...

    class PluginLoader(typing.Protocol):
        """typing.Protocol for plugin loading mechanisms."""

        async def load_plugin(
            self, plugin_path: str
        ) -> p.Result[FlextPluginModels.Plugin]:
            """Load plugin from specified path."""
            ...

    class PluginExecution(typing.Protocol):
        """typing.Protocol for plugin execution mechanisms."""

        async def execute_plugin(
            self, plugin: FlextPluginModels.Plugin, context: dict[str, t.JsonValue]
        ) -> p.Result[t.JsonValue]:
            """Execute plugin with given context."""
            ...

    class PluginSecurity(typing.Protocol):
        """typing.Protocol for plugin security validation."""

        async def validate_plugin(
            self, plugin: FlextPluginModels.Plugin
        ) -> p.Result[bool]:
            """Validate plugin security."""
            ...

    class PluginHotReload(typing.Protocol):
        """typing.Protocol for plugin hot reload functionality."""

        async def start_watching(self, paths: t.StringList) -> p.Result[bool]:
            """Start watching paths for plugin changes."""
            ...

        async def stop_watching(self) -> p.Result[bool]:
            """Stop watching for plugin changes."""
            ...```
#### **Protocol Implementation**

