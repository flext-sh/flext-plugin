"""FLEXT Plugin Settings - Plugin system settings management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import ClassVar

from flext_core import FlextSettingsBase
from flext_plugin import m


class FlextPluginSettings(FlextSettingsBase):
    """Plugin system runtime settings."""

    model_config: ClassVar[m.SettingsConfigDict] = m.SettingsConfigDict(
        env_prefix="FLEXT_PLUGIN_", extra="ignore"
    )


__all__: list[str] = ["FlextPluginSettings"]
