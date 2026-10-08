"""Shared service foundation for flext-plugin components.

Provides typed access to the registered ``plugin`` settings namespace while
preserving flext-plugin service runtime behavior.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from abc import ABC

from flext_core import s
from flext_plugin import FlextPluginSettings, m, t


class FlextPluginServiceBase[
    TDomainResult: t.JsonPayload | t.SequenceOf[t.JsonPayload] = t.JsonPayload,
](s[TDomainResult], ABC):
    """Base class for flext-plugin services with typed plugin settings access."""

    @classmethod
    def runtime_bootstrap_options(cls) -> m.RuntimeBootstrapOptions:
        """Return runtime bootstrap options for plugin services."""
        return m.RuntimeBootstrapOptions(settings_type=FlextPluginSettings)


s = FlextPluginServiceBase

__all__: t.MutableSequenceOf[str] = ["FlextPluginServiceBase", "s"]
