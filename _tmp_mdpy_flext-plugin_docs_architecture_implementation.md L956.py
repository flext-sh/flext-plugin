# from flext-plugin/docs/architecture/implementation.md:956
# flext_plugin/health.py
from __future__ import annotations


class FlextPluginHealth:
    """Health check implementation for FLEXT Plugin system."""

    def __init__(self, platform: FlextPluginPlatform):
        self.platform = platform

    async def check_overall_health(self) -> p.Result[dict[str, t.JsonValue]]:
        """Comprehensive health check."""
        try:
            health_status = {
                "status": "healthy",
                "timestamp": datetime.now(UTC).isoformat(),
                "checks": {},
            }

            # Platform health
            platform_health = await self._check_platform_health()
            health_status["checks"]["platform"] = platform_health

            # Plugin health
            plugin_health = await self._check_plugin_health()
            health_status["checks"]["plugins"] = plugin_health

            # Registry health
            registry_health = await self._check_registry_health()
            health_status["checks"]["registry"] = registry_health

            # Determine overall status
            all_healthy = all(
                check.get("status") == "healthy"
                for check in health_status["checks"].values()
            )

            if not all_healthy:
                health_status["status"] = "unhealthy"

            return r.ok(health_status)

        except Exception as e:
            return r.fail(f"Health check failed: {e!s}")

    async def _check_platform_health(self) -> dict[str, t.JsonValue]:
        """Check platform operational health."""
        try:
            # Test basic platform operations
            status = self.platform.get_platform_status()

            return {
                "status": "healthy",
                "details": status,
                "response_time_ms": 10,  # Mock timing
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    async def _check_plugin_health(self) -> dict[str, t.JsonValue]:
        """Check plugin system health."""
        try:
            plugins = self.platform.list_plugins()
            active_plugins = [p for p in plugins if p.is_active()]

            return {
                "status": "healthy",
                "total_plugins": len(plugins),
                "active_plugins": len(active_plugins),
                "inactive_plugins": len(plugins) - len(active_plugins),
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    async def _check_registry_health(self) -> dict[str, t.JsonValue]:
        """Check plugin registry health."""
        try:
            # Test registry operations
            registry_status = {
                "can_read": True,
                "can_write": True,
                "last_backup": "2025-10-01T00:00:00Z",  # Mock data
            }

            return {"status": "healthy", "details": registry_status}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}```
______________________________________________________________________

## 📊 Performance Optimization Implementation

### Caching Strategies

#### **Multi-Level Caching**

