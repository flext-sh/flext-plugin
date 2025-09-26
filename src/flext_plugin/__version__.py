"""Module docstring."""

from __future__ import annotations

"""Version management for FLEXT Plugin System.

SPDX-License-Identifier: MIT


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from importlib.metadata import PackageNotFoundError, version as _pkg_version

from flext_core import FlextTypes

try:
    __version__: str = _pkg_version("flext-plugin")
except PackageNotFoundError:
    # Fallback for local development without installed distribution metadata
    __version__ = "0.0.0-dev"

# Version metadata for programmatic access
VERSION_MAJOR: int = 0
VERSION_MINOR: int = 9
VERSION_PATCH: int = 0

# Release information
RELEASE_NAME: str = "Plugin Foundation"
RELEASE_DATE: str = "2025-08-25"
BUILD_TYPE: str = "stable"

# Version info tuple for compatibility
__version_info__ = (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)

__all__: FlextTypes.Core.StringList = [
    "BUILD_TYPE",
    "RELEASE_DATE",
    "RELEASE_NAME",
    "VERSION_MAJOR",
    "VERSION_MINOR",
    "VERSION_PATCH",
    "__version__",
    "__version_info__",
]
