# from flext-plugin_docs/standards/python-module-organization.md:666
from __future__ import annotations

from flext_plugin import FlextPlugin
from flext_plugin import PluginStatus, PluginType
from datetime import datetime


class FlextPlugin(FlextModels.Entity):
    """Rich plugin entity with comprehensive business logic.

    Represents a plugin in the FLEXT ecosystem with full lifecycle management,
    dependency tracking, and event sourcing capabilities.
    """

    # Core plugin attributes
    name: str
    plugin_version: str
    plugin_type: PluginType
    status: PluginStatus = PluginStatus.DISCOVERED

    # Metadata and configuration
    description: str = ""
    author: str = ""
    homepage_url: str = ""
    repository_url: str = ""
    license: str = "MIT"
    tags: t.StringList = field(default_factory=list)

    # Dependencies and compatibility
    dependencies: t.StringList = field(default_factory=list)
    flext_core_version: str = ">=0.9.9"
    python_version: str = ">=3.13"

    # Runtime state
    last_activated: datetime | None = None
    last_executed: datetime | None = None
    execution_count: int = 0
    error_count: int = 0

    # Business logic methods
    def can_activate(self) -> p.Result[bool]:
        """Check if plugin can be activated with business rules."""
        if self.status == PluginStatus.ACTIVE:
            return r[bool].fail("Plugin already active")

        if self.status not in [PluginStatus.LOADED, PluginStatus.INACTIVE]:
            return r[bool].fail(f"Cannot activate plugin in {self.status} state")

        # Check dependencies
        if not self._validate_dependencies():
            return r[bool].fail("Plugin dependencies not satisfied")

        return r[bool].ok(True)

    def activate(self) -> p.Result[bool]:
        """Activate plugin with business validation and event generation."""
        validation = self.can_activate()
        if validation.failure:
            return validation

        # Perform activation
        self.status = PluginStatus.ACTIVE
        self.last_activated = datetime.utcnow()

        # Generate domain event
        self.add_domain_event({
            "type": "PluginActivated",
            "plugin_id": str(self.id),
            "plugin_name": self.name,
            "timestamp": self.last_activated.isoformat(),
            "plugin_type": self.plugin_type.value,
        })

        return r[bool].ok(True)

    def record_execution(self, success: bool, execution_time: float) -> None:
        """Record plugin execution with metrics."""
        self.execution_count += 1
        self.last_executed = datetime.utcnow()

        if not success:
            self.error_count += 1

        # Generate execution event
        self.add_domain_event({
            "type": "PluginExecuted",
            "plugin_id": str(self.id),
            "success": success,
            "execution_time": execution_time,
            "timestamp": self.last_executed.isoformat(),
        })

    def get_health_status(self) -> dict:
        """Get plugin health metrics."""
        if self.execution_count == 0:
            success_rate = 0.0
        else:
            success_rate = (
                self.execution_count - self.error_count
            ) / self.execution_count

        return {
            "status": self.status.value,
            "execution_count": self.execution_count,
            "error_count": self.error_count,
            "success_rate": success_rate,
            "last_executed": self.last_executed.isoformat()
            if self.last_executed
            else None,
            "health": "healthy"
            if success_rate > 0.9
            else "degraded"
            if success_rate > 0.5
            else "unhealthy",
        }

    def _validate_dependencies(self) -> bool:
        """Validate plugin dependencies are satisfied."""
        # Implementation for dependency validation
        return True```
### **Plugin Aggregate Patterns**

