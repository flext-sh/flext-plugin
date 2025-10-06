"""FLEXT Plugin Version - Plugin system version information.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final, NamedTuple


class FlextPluginVersion(NamedTuple):
    """Plugin system version information."""

    version: str
    version_info: tuple[int | str, ...]
    major: int
    minor: int
    micro: int
    releaselevel: str
    serial: int

    @classmethod
    def parse_version(cls, version_string: str) -> FlextPluginVersion:
        """Parse version string into version components.

        Args:
            version_string: Version string to parse

        Returns:
            FlextPluginVersion instance
        """
        # Parse version string (e.g., "0.9.9")
        parts = version_string.split(".")
        major = int(parts[0]) if len(parts) > 0 else 0
        minor = int(parts[1]) if len(parts) > 1 else 0
        micro = int(parts[2]) if len(parts) > 2 else 0

        # Default release level and serial
        releaselevel = "final"
        serial = 0

        # Check for pre-release indicators
        if "-" in version_string:
            releaselevel = "alpha"
        elif "rc" in version_string.lower():
            releaselevel = "candidate"

        version_info = (major, minor, micro, releaselevel, serial)

        return cls(
            version=version_string,
            version_info=version_info,
            major=major,
            minor=minor,
            micro=micro,
            releaselevel=releaselevel,
            serial=serial,
        )

    def __str__(self) -> str:
        """Return version string."""
        return self.version

    def __repr__(self) -> str:
        """Return detailed version representation."""
        return f"FlextPluginVersion(version='{self.version}', major={self.major}, minor={self.minor}, micro={self.micro})"


# Current version
VERSION: Final[FlextPluginVersion] = FlextPluginVersion.parse_version("0.9.9")

__all__ = ["FlextPluginVersion", "VERSION"]
