"""Shared service foundation for flext-plugin components.

Provides typed access to the registered ``plugin`` settings namespace while
preserving flext-plugin service runtime behavior.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextService


class FlextPluginServiceBase[TDomainResult](FlextService[TDomainResult]):
    """Base class for flext-plugin services with typed plugin settings access."""


s = FlextPluginServiceBase

__all__: list[str] = ["FlextPluginServiceBase", "s"]
