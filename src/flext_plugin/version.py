"""Version information for FLEXT Plugin.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import NamedTuple

# Constants for version parsing
MIN_VERSION_PARTS = 3  # major.minor.patch


class FlextPluginVersion(NamedTuple):
    """Version information for FLEXT Plugin."""

    major: int
    minor: int
    patch: int
    pre_release: str | None = None
    dev_release: int | None = None

    @property
    def version(self) -> str:
        """Get version string."""
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.pre_release:
            version += f"-{self.pre_release}"
        if self.dev_release is not None:
            version += f".dev{self.dev_release}"
        return version

    @property
    def version_info(self) -> tuple[int | str, ...]:
        """Get version info tuple."""
        info = (self.major, self.minor, self.patch)
        if self.pre_release:
            info += (self.pre_release,)
        if self.dev_release is not None:
            info += ("dev", self.dev_release)
        return info

    @classmethod
    def from_string(cls, version_str: str) -> FlextPluginVersion:
        """Create version from string."""
        # Simple parsing - in real implementation would be more robust
        parts = version_str.split(".")
        if len(parts) >= MIN_VERSION_PARTS:
            major = int(parts[0])
            minor = int(parts[1])
            patch_part = parts[2]

            # Handle pre-release and dev suffixes
            patch = 0
            pre_release = None
            dev_release = None

            if "-" in patch_part:
                patch_str, suffix = patch_part.split("-", 1)
                patch = int(patch_str)
                if ".dev" in suffix:
                    pre_release, dev_str = suffix.split(".dev", 1)
                    dev_release = int(dev_str)
                else:
                    pre_release = suffix
            else:
                patch = int(patch_part)

            return cls(major, minor, patch, pre_release, dev_release)

        msg = f"Invalid version string: {version_str}"
        raise ValueError(msg)


# Current version
VERSION = FlextPluginVersion.from_string("0.9.0")

__all__ = ["VERSION", "FlextPluginVersion"]
