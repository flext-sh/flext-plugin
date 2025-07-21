"""Plugin domain value objects.

REFACTORED: PluginMetadata moved to domain.entities to eliminate duplication.
Use: from flext_plugin.domain.entities import PluginMetadata
"""

from __future__ import annotations

# Re-export from canonical location to maintain backwards compatibility
from flext_plugin.domain.entities import PluginMetadata

__all__ = ["PluginMetadata"]
