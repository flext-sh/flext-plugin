"""Compose the layer-zero plugin schemas into the public model family.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_plugin/_models/config
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_plugin.config_models import FlextPluginConfigModels as _ConfigModels


class FlextPluginConfigModels(_ConfigModels):
    """Public model holder sharing the canonical configuration declarations."""


__all__: list[str] = ["FlextPluginConfigModels"]
