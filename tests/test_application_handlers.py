"""Test suite for flext_plugin.handlers - Event handling functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations
from flext_core import FlextTypes as t

from typing import Never

import pytest

from flext_plugin import FlextPluginHandlers


class TestFlextPluginHandlers:
    """Test suite for FlextPluginHandlers functionality."""

    def test_handlers_initialization(self) -> None:
        """Test that handlers can be initialized."""
        handlers = FlextPluginHandlers()
        assert handlers is not None
        assert isinstance(handlers._handlers, dict)
        assert isinstance(handlers._event_history, list)

    def test_handler_registration(self) -> None:
        """Test registering event handlers."""
        handlers = FlextPluginHandlers()

        def test_handler(event_data: dict[str, t.GeneralValueType]) -> str:
            return f"processed: {event_data}"

        result = handlers.register_handler("test_event", test_handler)
        assert result.is_success

        # Check that handler was registered
        assert "test_event" in handlers._handlers
        assert len(handlers._handlers["test_event"]) == 1

    @pytest.mark.asyncio
    async def test_event_triggering(self) -> None:
        """Test triggering events."""
        handlers = FlextPluginHandlers()

        results = []

        def test_handler(event_data: dict[str, t.GeneralValueType]) -> str:
            results.append(event_data)
            return "handled"

        handlers.register_handler("test_event", test_handler)

        # Trigger event
        result = await handlers.trigger_event("test_event", {"key": "value"})

        # Check that handler was called
        assert result.is_success
        assert len(results) == 1
        assert results[0] == {"key": "value"}

    @pytest.mark.asyncio
    async def test_event_history(self) -> None:
        """Test event history tracking."""
        handlers = FlextPluginHandlers()

        # Trigger some events
        await handlers.trigger_event("event1", {"data": "test1"})
        await handlers.trigger_event("event2", {"data": "test2"})

        # Check history
        history = handlers.get_event_history()
        assert len(history) == 2
        assert history[0]["event_type"] == "event1"
        assert history[1]["event_type"] == "event2"

    @pytest.mark.asyncio
    async def test_handler_priorities(self) -> None:
        """Test handler priority ordering."""
        handlers = FlextPluginHandlers()

        results = []

        def handler_low(event_data: dict[str, t.GeneralValueType]) -> None:
            results.append("low")

        def handler_high(event_data: dict[str, t.GeneralValueType]) -> None:
            results.append("high")

        # Register with different priorities (higher number = higher priority)
        handlers.register_handler("test", handler_low, priority=1)
        handlers.register_handler("test", handler_high, priority=10)

        await handlers.trigger_event("test", {})

        # High priority handler should be called first
        assert results == ["high", "low"]

    @pytest.mark.asyncio
    async def test_multiple_handlers_same_event(self) -> None:
        """Test multiple handlers for the same event."""
        handlers = FlextPluginHandlers()

        results = []

        def handler1(event_data: dict[str, t.GeneralValueType]) -> None:
            results.append("handler1")

        def handler2(event_data: dict[str, t.GeneralValueType]) -> None:
            results.append("handler2")

        handlers.register_handler("test_event", handler1)
        handlers.register_handler("test_event", handler2)

        await handlers.trigger_event("test_event", {})

        # Both handlers should be called
        assert len(results) == 2
        assert "handler1" in results
        assert "handler2" in results

    @pytest.mark.asyncio
    async def test_event_filtering(self) -> None:
        """Test filtering event history."""
        handlers = FlextPluginHandlers()

        # Trigger events of different types
        await handlers.trigger_event("plugin_loaded", {"plugin": "test1"})
        await handlers.trigger_event("plugin_executed", {"plugin": "test1"})
        await handlers.trigger_event("plugin_loaded", {"plugin": "test2"})

        # Get all events
        all_events = handlers.get_event_history()
        assert len(all_events) == 3

        # Filter by event type
        loaded_events = handlers.get_event_history("plugin_loaded")
        assert len(loaded_events) == 2
        assert all(event["event_type"] == "plugin_loaded" for event in loaded_events)

    @pytest.mark.asyncio
    async def test_handler_error_handling(self) -> None:
        """Test error handling in event handlers."""
        handlers = FlextPluginHandlers()

        def failing_handler(event_data: dict[str, t.GeneralValueType]) -> Never:
            msg = "Handler failed"
            raise ValueError(msg)

        def working_handler(event_data: dict[str, t.GeneralValueType]) -> str:
            return "success"

        handlers.register_handler("test", failing_handler)
        handlers.register_handler("test", working_handler)

        # Trigger event - should not crash despite failing handler
        result = await handlers.trigger_event("test", {})
        assert result.is_success

        # Check that working handler still executed
        # (This would need to be verified by checking results if handlers returned values)
