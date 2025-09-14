"""Legacy facade for discovery - BACKWARD COMPATIBILITY ONLY.

This module provides backward compatibility for legacy imports.
All new code should import from discovery directly.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings

from flext_core import FlextTypes

# Deprecation warning for legacy usage
warnings.warn(
    "flext_plugin.core.discovery is deprecated. Use flext_plugin.discovery instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__: FlextTypes.Core.StringList = []
