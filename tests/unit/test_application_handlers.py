"""Test suite for flext_plugin.handlers - Event handling functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import asyncio

from flext_plugin import FlextPluginHandlers
from tests import t


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

        async def test_handler(
            event_data: t.JsonMapping,
        ) -> t.JsonMapping:
            return {"status": "processed", "event": dict(event_data.items())}

        result = handlers.register_handler("test_event", test_handler)
        assert result.success
        assert "test_event" in handlers._handlers
        assert len(handlers._handlers["test_event"]) == 1

    def test_event_triggering(self) -> None:
        """Test triggering events."""

        async def _inner() -> None:
            handlers = FlextPluginHandlers()
            results: list[t.JsonMapping] = []

            async def test_handler(
                event_data: t.JsonMapping,
            ) -> t.JsonMapping:
                results.append(event_data)
                return {"status": "handled"}

            handlers.register_handler("test_event", test_handler)
            result = await handlers.trigger_event("test_event", {"key": "value"})
            assert result.success
            assert len(results) == 1
            assert results[0] == {"key": "value"}

        asyncio.run(_inner())

    def test_event_history(self) -> None:
        """Test event history tracking."""

        async def _inner() -> None:
            handlers = FlextPluginHandlers()
            await handlers.trigger_event("event1", {"data": "test1"})
            await handlers.trigger_event("event2", {"data": "test2"})
            history = handlers.get_event_history()
            assert len(history) == 2
            assert history[0]["event_type"] == "event1"
            assert history[1]["event_type"] == "event2"

        asyncio.run(_inner())

    def test_handler_priorities(self) -> None:
        """Test handler priority ordering."""

        async def _inner() -> None:
            handlers = FlextPluginHandlers()
            results: list[str] = []

            async def handler_low(
                event_data: t.JsonMapping,
            ) -> t.JsonMapping:
                _ = event_data
                results.append("low")
                return {"handler": "low"}

            async def handler_high(
                event_data: t.JsonMapping,
            ) -> t.JsonMapping:
                _ = event_data
                results.append("high")
                return {"handler": "high"}

            handlers.register_handler("test", handler_low, priority=1)
            handlers.register_handler("test", handler_high, priority=10)
            await handlers.trigger_event("test", {})
            assert results == ["high", "low"]

        asyncio.run(_inner())

    def test_multiple_handlers_same_event(self) -> None:
        """Test multiple handlers for the same event."""

        async def _inner() -> None:
            handlers = FlextPluginHandlers()
            results: list[str] = []

            async def handler1(
                event_data: t.JsonMapping,
            ) -> t.JsonMapping:
                _ = event_data
                results.append("handler1")
                return {"handler": "handler1"}

            async def handler2(
                event_data: t.JsonMapping,
            ) -> t.JsonMapping:
                _ = event_data
                results.append("handler2")
                return {"handler": "handler2"}

            handlers.register_handler("test_event", handler1)
            handlers.register_handler("test_event", handler2)
            await handlers.trigger_event("test_event", {})
            assert len(results) == 2
            assert "handler1" in results
            assert "handler2" in results

        asyncio.run(_inner())

    def test_event_filtering(self) -> None:
        """Test filtering event history."""

        async def _inner() -> None:
            handlers = FlextPluginHandlers()
            await handlers.trigger_event("plugin_loaded", {"plugin": "test1"})
            await handlers.trigger_event("plugin_executed", {"plugin": "test1"})
            await handlers.trigger_event("plugin_loaded", {"plugin": "test2"})
            all_events = handlers.get_event_history()
            assert len(all_events) == 3
            loaded_events = handlers.get_event_history("plugin_loaded")
            assert len(loaded_events) == 2
            assert all(
                event["event_type"] == "plugin_loaded" for event in loaded_events
            )

        asyncio.run(_inner())

    def test_handler_error_handling(self) -> None:
        """Test error handling in event handlers."""

        async def _inner() -> None:
            handlers = FlextPluginHandlers()

            async def failing_handler(
                event_data: t.JsonMapping,
            ) -> t.JsonMapping:
                _ = event_data
                msg = "Handler failed"
                raise ValueError(msg)

            async def working_handler(
                event_data: t.JsonMapping,
            ) -> t.JsonMapping:
                _ = event_data
                return {"status": "success"}

            handlers.register_handler("test", failing_handler)
            handlers.register_handler("test", working_handler)
            result = await handlers.trigger_event("test", {})
            assert result.success

        asyncio.run(_inner())
