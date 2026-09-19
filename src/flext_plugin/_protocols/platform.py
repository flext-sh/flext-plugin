"""Platform service protocol for flext-plugin."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Sequence

    from flext_plugin import m, p, t

    from .._protocols.plugin import FlextPluginProtocolsPlugin
    from .._utilities.plugin_platform import FlextPluginPlatform


@runtime_checkable
class FlextPluginProtocolsPlatformService(Protocol):
    """Protocol for the public plugin platform facade surface."""

    @property
    def discovery(self) -> FlextPluginProtocolsPlugin.Discovery | None:
        """The configured discovery protocol implementation."""
        ...

    @discovery.setter
    def discovery(self, value: FlextPluginProtocolsPlugin.Discovery | None) -> None:
        ...

    @property
    def loader(self) -> FlextPluginProtocolsPlugin.Loader | None:
        """The configured loader protocol implementation."""
        ...

    @loader.setter
    def loader(self, value: FlextPluginProtocolsPlugin.Loader | None) -> None:
        ...

    @property
    def executor(self) -> FlextPluginProtocolsPlugin.Execution | None:
        """The configured executor protocol implementation."""
        ...

    @executor.setter
    def executor(self, value: FlextPluginProtocolsPlugin.Execution | None) -> None:
        ...

    def discover_plugins(
        self, paths: t.StrSequence
    ) -> p.Result[Sequence[FlextPluginPlatform.Plugin]]:
        """Discover plugins from the provided paths."""
        ...

    def execute_plugin(
        self, plugin_name: str, context: t.JsonMapping, execution_id: str | None = None
    ) -> p.Result[FlextPluginPlatform.PluginExecution]:
        """Execute a plugin with the provided context."""
        ...

    def fetch_plugin(self, name: str) -> FlextPluginPlatform.Plugin | None:
        """Fetch a plugin by name."""
        ...

    def fetch_plugin_status(self, name: str) -> str | None:
        """Fetch the status of a plugin by name."""
        ...

    def resolve_plugin_active(self, name: str) -> bool:
        """Resolve whether the named plugin is active."""
        ...

    def list_plugins(self) -> Sequence[FlextPluginPlatform.Plugin]:
        """List registered plugins."""
        ...

    def load_plugin(
        self, plugin_path: str
    ) -> p.Result[FlextPluginPlatform.Plugin]:
        """Load a plugin from disk."""
        ...

    def register_plugin(
        self, plugin: FlextPluginPlatform.Plugin | m.Plugin.Entity
    ) -> p.Result[bool]:
        """Register a plugin instance."""
        ...

    def start_hot_reload(self, paths: t.StrSequence) -> p.Result[bool]:
        """Start plugin hot reload monitoring."""
        ...

    def stop_hot_reload(self) -> p.Result[bool]:
        """Stop plugin hot reload monitoring."""
        ...

    def unregister_plugin(self, plugin_name: str) -> p.Result[bool]:
        """Unregister a plugin by name."""
        ...


__all__: list[str] = ["FlextPluginProtocolsPlatformService"]
