"""Compose the layer-zero plugin schemas into the public model family.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_plugin/_models/config
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from flext_plugin.config_models import FlextPluginModelsConfig as _ConfigModels


class FlextPluginModelsConfig(_ConfigModels):
    """Public model holder sharing the canonical configuration declarations."""


__all__: list[str] = ["FlextPluginModelsConfig"]
