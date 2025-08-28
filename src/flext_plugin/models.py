"""Legacy facade for flext_plugin_models - BACKWARD COMPATIBILITY ONLY.

This module provides backward compatibility for legacy imports.
All new code should import from flext_plugin_models directly.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings

# Backward compatibility facade - import all from consolidated models
from .flext_plugin_models import *

# Deprecation warning for legacy usage
warnings.warn(
    "flext_plugin.models is deprecated. Use flext_plugin.flext_plugin_models instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__: list[str] = []
