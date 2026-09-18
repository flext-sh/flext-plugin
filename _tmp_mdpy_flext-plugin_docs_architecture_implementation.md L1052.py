# from flext-plugin/docs/architecture/implementation.md:1052
# flext_plugin/cache.py
from __future__ import annotations

import asyncio
from datetime import datetime, timedelta


class FlextPluginCache:
    """Multi-level caching for plugin system performance."""

    def __init__(self, max_memory_items: int = 1000, ttl_seconds: int = 3600):
        self.memory_cache: dict[str, dict[str, t.JsonValue]] = {}
        self.max_memory_items = max_memory_items
        self.ttl_seconds = ttl_seconds
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> t.JsonValue | None:
        """Get item from cache with TTL check."""
        async with self._lock:
            if key in self.memory_cache:
                entry = self.memory_cache[key]
                if not self._is_expired(entry):
                    return entry["value"]
                # Remove expired entry
                del self.memory_cache[key]

        return None

    async def set(self, key: str, value) -> None:
        """Set item in cache with TTL."""
        async with self._lock:
            # Implement LRU eviction if needed
            if len(self.memory_cache) >= self.max_memory_items:
                self._evict_lru()

            self.memory_cache[key] = {
                "value": value,
                "timestamp": datetime.now(UTC),
                "ttl": timedelta(seconds=self.ttl_seconds),
            }

    def _is_expired(self, entry: dict[str, t.JsonValue]) -> bool:
        """Check if cache entry is expired."""
        return datetime.now(UTC) > entry["timestamp"] + entry["ttl"]

    def _evict_lru(self) -> None:
        """Evict least recently used items."""
        # Simple FIFO eviction for demonstration
        oldest_key = next(iter(self.memory_cache))
        del self.memory_cache[oldest_key]```
### Asynchronous Processing

#### **Concurrent Plugin Operations**

