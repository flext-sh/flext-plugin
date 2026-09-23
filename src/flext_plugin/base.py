"""Shared service foundation for flext-plugin components.

Provides typed access to the registered ``plugin`` settings namespace while
preserving flext-plugin service runtime behavior.
"""

from __future__ import annotations

from abc import ABC

from flext_core import s

from . import FlextPluginSettings, m, p, t


class FlextPluginServiceBase[
    TDomainResult: t.JsonPayload | t.SequenceOf[t.JsonPayload] = t.JsonPayload
](s[TDomainResult], ABC):
    """Base class for flext-plugin services with typed plugin settings access."""

    def __init__(
        self,
        *,
        settings_type: type | None = None,
        runtime_settings: p.Settings | None = None,
        settings_overrides: t.ScalarMapping | None = None,
        initial_context: p.Context | None = None,
    ) -> None:
        """Bootstrap plugin services with one concrete runtime settings contract."""
        super().__init__(
            settings_type=settings_type or FlextPluginSettings,
            runtime_settings=runtime_settings,
            settings_overrides=settings_overrides,
            initial_context=initial_context,
        )

    @classmethod
    def runtime_bootstrap_options(cls) -> m.RuntimeBootstrapOptions:
        """Return runtime bootstrap options for plugin services."""
        return m.RuntimeBootstrapOptions(settings_type=FlextPluginSettings)


s = FlextPluginServiceBase

__all__: t.MutableSequenceOf[str] = ["FlextPluginServiceBase", "s"]
