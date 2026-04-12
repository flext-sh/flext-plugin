"""FLEXT Plugin Handlers - Plugin system event handlers.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import inspect
from collections.abc import MutableMapping, MutableSequence, Sequence
from datetime import UTC, datetime

from flext_plugin import c, r, t, u


class FlextPluginHandlers:
    """Plugin system event handlers for managing plugin lifecycle events.

    This class provides complete event handling for plugin operations
    including discovery, loading, execution, and lifecycle management events.

    Usage:
        ```python
        from flext_plugin import FlextPluginHandlers

        # Initialize handlers
        handlers = FlextPluginHandlers()

        # Register event handlers
        handlers.register_handler("plugin_loaded", my_plugin_loaded_handler)
        handlers.register_handler("plugin_executed", my_plugin_executed_handler)

        # Trigger events
        await handlers.trigger_event("plugin_loaded", {"plugin_name": "my-plugin"})
        ```
    """

    def __init__(self) -> None:
        """Initialize the plugin handlers."""
        super().__init__()
        self.logger = u.fetch_logger(__name__)
        self._handlers: MutableMapping[
            str,
            MutableSequence[t.Plugin.Handlers.HandlerInfo],
        ] = {}
        self._event_history: MutableSequence[t.MutableRecursiveContainerMapping] = []

    def clear_event_history(self) -> int:
        """Clear event history.

        Returns:
        Number of events cleared

        """
        count = len(self._event_history)
        self._event_history.clear()
        self.logger.info("Cleared %s events from history", count)
        return count

    def get_event_history(
        self,
        event_type: str | None = None,
        limit: int = 100,
    ) -> Sequence[t.RecursiveContainerMapping]:
        """Get event history, optionally filtered by event type.

        Args:
        event_type: Optional event type to filter by
        limit: Maximum number of events to return

        Returns:
        List of event records

        """
        history = self._event_history
        if event_type:
            history = [e for e in history if e["event_type"] == event_type]
        return [e for e in history if limit <= 0 or e in history[-limit:]]

    def get_handler_count(self, event_type: str) -> int:
        """Get count of handlers for a specific event type.

        Args:
        event_type: Type of event

        Returns:
        Number of handlers registered for the event type

        """
        return len(self._handlers.get(event_type, []))

    def get_handler_status(self) -> t.RecursiveContainerMapping:
        """Get the current status of the event handlers.

        Returns:
        Dictionary containing handler status information

        """
        return {
            "total_event_types": len(self._handlers),
            "total_handlers": sum(
                len(handlers) for handlers in self._handlers.values()
            ),
            "event_history_size": len(self._event_history),
            "registered_handlers": self.get_registered_handlers(),
        }

    def get_registered_handlers(self) -> t.IntMapping:
        """Get count of registered handlers by event type.

        Returns:
        Dictionary mapping event types to handler counts

        """
        return {
            event_type: len(handlers) for event_type, handlers in self._handlers.items()
        }

    async def handle_plugin_discovered(
        self,
        event_data: t.RecursiveContainerMapping,
    ) -> t.RecursiveContainerMapping:
        """Handle plugin discovered event.

        Args:
        event_data: Event data containing plugin information

        Returns:
        Handler result

        """
        plugin_name = event_data.get("plugin_name", c.IDENTIFIER_UNKNOWN)
        name_str = str(plugin_name)
        self.logger.info("Plugin discovered: %s", name_str)
        return {"success": True, "plugin_name": plugin_name}

    async def handle_plugin_error(
        self,
        event_data: t.RecursiveContainerMapping,
    ) -> t.RecursiveContainerMapping:
        """Handle plugin error event.

        Args:
        event_data: Event data containing error information

        Returns:
        Handler result

        """
        plugin_name = event_data.get("plugin_name", c.IDENTIFIER_UNKNOWN)
        error_message = event_data.get("error_message", "Unknown error")
        name_str = str(plugin_name)
        error_str = str(error_message)
        self.logger.error("Plugin error: %s - %s", name_str, error_str)
        return {
            "success": True,
            "plugin_name": plugin_name,
            "error_message": error_message,
        }

    async def handle_plugin_executed(
        self,
        event_data: t.RecursiveContainerMapping,
    ) -> t.RecursiveContainerMapping:
        """Handle plugin executed event.

        Args:
        event_data: Event data containing execution information

        Returns:
        Handler result

        """
        plugin_name = event_data.get("plugin_name", c.IDENTIFIER_UNKNOWN)
        execution_id = event_data.get("execution_id", c.IDENTIFIER_UNKNOWN)
        success = event_data.get("success", False)
        name_str = str(plugin_name)
        exec_str = str(execution_id)
        success_str = str(success)
        self.logger.info(
            "Plugin executed: %s (execution: %s, success: %s)",
            name_str,
            exec_str,
            success_str,
        )
        return {
            "success": True,
            "plugin_name": plugin_name,
            "execution_id": execution_id,
            "execution_success": success,
        }

    async def handle_plugin_loaded(
        self,
        event_data: t.RecursiveContainerMapping,
    ) -> t.RecursiveContainerMapping:
        """Handle plugin loaded event.

        Args:
        event_data: Event data containing plugin information

        Returns:
        Handler result

        """
        plugin_name = event_data.get("plugin_name", c.IDENTIFIER_UNKNOWN)
        name_str = str(plugin_name)
        self.logger.info("Plugin loaded: %s", name_str)
        return {"success": True, "plugin_name": plugin_name}

    async def handle_plugin_unloaded(
        self,
        event_data: t.RecursiveContainerMapping,
    ) -> t.RecursiveContainerMapping:
        """Handle plugin unloaded event.

        Args:
        event_data: Event data containing plugin information

        Returns:
        Handler result

        """
        plugin_name = event_data.get("plugin_name", c.IDENTIFIER_UNKNOWN)
        name_str = str(plugin_name)
        self.logger.info("Plugin unloaded: %s", name_str)
        return {"success": True, "plugin_name": plugin_name}

    def register_default_handlers(self) -> r[bool]:
        """Register default event handlers for common plugin operations.

        Returns:
        r indicating success or failure

        """
        try:
            handlers_to_register = [
                ("plugin_discovered", self.handle_plugin_discovered),
                ("plugin_loaded", self.handle_plugin_loaded),
                ("plugin_executed", self.handle_plugin_executed),
                ("plugin_error", self.handle_plugin_error),
                ("plugin_unloaded", self.handle_plugin_unloaded),
            ]
            for event_type, handler in handlers_to_register:
                result = self.register_handler(event_type, handler)
                if result.failure:
                    return r[bool].fail(f"Failed to register {event_type} handler")
            self.logger.info("Registered default event handlers")
            return r[bool].ok(True)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to register default handlers")
            return r[bool].fail(f"Default handler registration error: {e!s}")

    def register_handler(
        self,
        event_type: str,
        handler: t.Plugin.Handlers.EventHandler,
        priority: int = 0,
    ) -> r[bool]:
        """Register an event handler for a specific event type.

        Args:
            event_type: Type of event to handle
            handler: Handler function to register
            priority: Handler priority (higher numbers execute first)

        Returns:
            r indicating success or failure

        """
        try:
            if event_type not in self._handlers:
                self._handlers[event_type] = list[t.Plugin.Handlers.HandlerInfo]()
            handler_info = t.Plugin.Handlers.HandlerInfo(
                handler=handler, priority=priority
            )
            self._handlers[event_type].append(handler_info)

            def get_priority(handler_info: t.Plugin.Handlers.HandlerInfo) -> int:
                return handler_info.priority

            self._handlers[event_type] = sorted(
                self._handlers[event_type],
                key=get_priority,
                reverse=True,
            )
            self.logger.debug("Registered handler for event type: %s", event_type)
            return r[bool].ok(True)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to register handler for %s", event_type)
            return r[bool].fail(f"Handler registration error: {e!s}")

    async def trigger_event(
        self,
        event_type: str,
        event_data: t.RecursiveContainerMapping,
    ) -> r[t.RecursiveContainerList]:
        """Trigger an event and execute all registered handlers.

        Args:
        event_type: Type of event to trigger
        event_data: Data to pass to handlers

        Returns:
        r containing list of handler results

        """
        try:
            event_record: t.MutableRecursiveContainerMapping = {
                "event_type": event_type,
                "event_data": event_data,
                "timestamp": self._get_current_timestamp(),
            }
            self._event_history.append(event_record)
            if event_type not in self._handlers:
                self.logger.debug(
                    "No handlers registered for event type: %s",
                    event_type,
                )
                return r[t.RecursiveContainerList].ok([])
            results: t.MutableRecursiveContainerList = []
            for handler_info in self._handlers[event_type]:
                try:
                    handler = handler_info.handler
                    result = await self._execute_handler(handler, event_data)
                    results.append(result)
                except (
                    ValueError,
                    TypeError,
                    KeyError,
                    AttributeError,
                    OSError,
                    RuntimeError,
                    ImportError,
                ) as e:
                    self.logger.exception("Handler execution failed for %s", event_type)
                    results.append({"error": str(e), "success": False})
            self.logger.debug(
                f"Triggered event {event_type} with {len(results)} handlers",
            )
            return r[t.RecursiveContainerList].ok(results)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to trigger event %s", event_type)
            return r[t.RecursiveContainerList].fail(f"Event triggering error: {e!s}")

    def unregister_handler(
        self,
        event_type: str,
        handler: t.Plugin.Handlers.EventHandler,
    ) -> r[bool]:
        """Unregister an event handler.

        Args:
        event_type: Type of event
        handler: Handler function to unregister

        Returns:
        r indicating success or failure

        """
        try:
            if event_type not in self._handlers:
                return r[bool].fail(
                    f"No handlers registered for event type: {event_type}",
                )
            original_count = len(self._handlers[event_type])
            self._handlers[event_type] = [
                h for h in self._handlers[event_type] if h.handler != handler
            ]
            if len(self._handlers[event_type]) == original_count:
                return r[bool].fail(f"Handler not found for event type: {event_type}")
            self.logger.debug("Unregistered handler for event type: %s", event_type)
            return r[bool].ok(True)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to unregister handler for %s", event_type)
            return r[bool].fail(f"Handler unregistration error: {e!s}")

    async def _execute_handler(
        self,
        handler: t.Plugin.Handlers.EventHandler,
        event_data: t.RecursiveContainerMapping,
    ) -> t.RecursiveContainerMapping:
        """Execute a single handler with proper error handling.

        Args:
        handler: Handler function to execute
        event_data: Event data to pass to handler

        Returns:
        Handler execution result

        """
        try:
            async_result = handler(event_data)
            return await async_result
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ):
            self.logger.exception("Handler execution failed")
            raise

    def _get_current_timestamp(self) -> str:
        """Get current timestamp as ISO string.

        Returns:
        Current timestamp as ISO string

        """
        return datetime.now(UTC).isoformat()

    def _is_async_function(self, func: t.RecursiveContainer) -> bool:
        """Check if a function is async.

        Args:
        func: Function to check

        Returns:
        True if function is async, False otherwise

        """
        return inspect.iscoroutinefunction(func)


__all__: list[str] = ["FlextPluginHandlers"]
