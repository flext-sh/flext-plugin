"""Version metadata for flext plugin."""

from __future__ import annotations

from typing import Final

from importlib.metadata import metadata

_metadata = metadata("flext-plugin")

__version__: Final[str] = _metadata["Version"]
__version_info__: Final[tuple[int | str, ...]] = tuple(
    int(part) if part.isdigit() else part for part in __version__.split(".")
)

__all__ = ["__version__", "__version_info__"]
