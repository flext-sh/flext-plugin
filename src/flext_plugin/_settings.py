"""FLEXT Plugin Settings - Plugin system settings management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextSettings
from flext_plugin import m


class FlextPluginSettings(FlextSettings):
    """Plugin system runtime settings."""

    # Why: pydantic_settings is owned by flext-core; route SettingsConfigDict
    # through the m facade instead of importing the third-party package
    # directly (ENFORCE-070).
    model_config = m.SettingsConfigDict(env_prefix="FLEXT_PLUGIN_", extra="ignore")


settings: FlextPluginSettings = FlextPluginSettings.fetch_global()
"""Pre-instantiated project settings singleton — ``from flext_plugin import settings``."""

__all__: list[str] = ["FlextPluginSettings", "settings"]
