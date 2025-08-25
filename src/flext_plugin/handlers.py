"""Legacy facade for flext_plugin_handlers - BACKWARD COMPATIBILITY ONLY.

This module provides backward compatibility for legacy imports.
All new code should import from flext_plugin_handlers directly.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings

# Backward compatibility facade - import all from consolidated handlers
from .flext_plugin_handlers import *  # noqa: F403

# Deprecation warning for legacy usage
warnings.warn(
    "flext_plugin.handlers is deprecated. Use flext_plugin.flext_plugin_handlers instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__: list[str] = []
