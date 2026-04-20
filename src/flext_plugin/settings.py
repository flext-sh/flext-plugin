"""FLEXT Plugin Settings - Plugin system settings management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import ClassVar

from flext_core import FlextSettings

from flext_plugin import m


@FlextSettings.auto_register("plugin")
class FlextPluginSettings(FlextSettings):
    """Plugin system runtime settings."""

    model_config: ClassVar[m.SettingsConfigDict] = m.SettingsConfigDict(
        env_prefix="FLEXT_PLUGIN_", extra="ignore"
    )


__all__: list[str] = ["FlextPluginSettings"]
