# from flext-plugin/docs/standards/python-module-organization.md:1062
from __future__ import annotations

from functools import wraps

import json


class PluginCache:
    """Plugin-aware caching system."""

    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.max_size = max_size
        self.ttl = ttl
        self._cache: dict[str, dict] = {}

    def cache_plugin_result(
        self,
        cache_key_func: collections.abc.Callable[..., str],
        invalidate_on_plugin_change: bool = True,
    ):
        """Decorator for caching plugin operation results."""

        def decorator(func: collections.abc.Callable[..., r[t.JsonValue]]):
            @wraps(func)
            def wrapper(*args, **kwargs) -> p.Result[t.JsonValue]:
                # Generate cache key
                cache_key = cache_key_func(*args, **kwargs)

                # Check cache first
                cached_result = self._get_cached_result(cache_key)
                if cached_result is not None:
                    return r[bool].ok(cached_result)

                # Execute function
                result = func(*args, **kwargs)

                # Cache successful results
                if result.success:
                    self._cache_result(
                        cache_key,
                        result.value,
                        {"invalidate_on_plugin_change": invalidate_on_plugin_change},
                    )

                return result

            return wrapper

        return decorator

    def invalidate_plugin_cache(self, plugin_id: str) -> None:
        """Invalidate cache entries related to specific plugin."""
        keys_to_remove = []

        for cache_key, cache_entry in self._cache.items():
            metadata = cache_entry.get("metadata", {})
            if metadata.get("invalidate_on_plugin_change") and plugin_id in cache_key:
                keys_to_remove.append(cache_key)

        for key in keys_to_remove:
            del self._cache[key]

    def _get_cached_result(self, cache_key: str) -> t.JsonValue | None:
        """Get cached result if still valid."""
        if cache_key not in self._cache:
            return None

        cache_entry = self._cache[cache_key]

        # Check TTL
        import time

        if time.time() - cache_entry["timestamp"] > self.ttl:
            del self._cache[cache_key]
            return None

        return cache_entry["data"]

    def _cache_result(self, cache_key: str, data, metadata: dict) -> None:
        """Cache result with metadata."""
        import time

        # Implement LRU eviction if needed
        if len(self._cache) >= self.max_size:
            oldest_key = min(
                self._cache.keys(), key=lambda k: self._cache[k]["timestamp"]
            )
            del self._cache[oldest_key]

        self._cache[cache_key] = {
            "data": data,
            "timestamp": time.time(),
            "metadata": metadata,
        }


# Usage example
plugin_cache = PluginCache()


@plugin_cache.cache_plugin_result(
    cache_key_func=lambda plugin_id, settings: (
        f"plugin_execution:{plugin_id}:{hash(json.dumps(settings, sort_keys=True))}"
    ),
    invalidate_on_plugin_change=True,
)
def execute_plugin_cached(plugin_id: str, settings: dict) -> p.Result[t.JsonValue]:
    """Execute plugin with caching."""
    # Actual plugin execution logic
    pass```
______________________________________________________________________

## 📏 **Code Quality Standards**

### **Type Annotation Requirements**

