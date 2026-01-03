"""FLEXT Plugin System - plugin management for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Version - acceptable exception for __init__.py (foundation module importing version)
from flext_plugin.__version__ import __version__, __version_info__

# Layer 0: Constants & Types (Foundation only - no services/api imports)
from flext_plugin.constants import FlextPluginConstants

# Layer 1: Domain Models
from flext_plugin.models import FlextPluginModels
from flext_plugin.protocols import FlextPluginProtocols
from flext_plugin.typings import FlextPluginTypes, t

__all__ = [
    # Layer 0
    "FlextPluginConstants",
    # Layer 1
    "FlextPluginModels",
    "FlextPluginProtocols",
    "FlextPluginTypes",
    # Version
    "__version__",
    "__version_info__",
    # Domain-specific aliases
    "t",
]
