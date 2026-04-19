"""Test suite for flext_plugin.handlers module.

Tests the actual FlextPluginHandlers class that exists in the codebase.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping

import pytest

from flext_plugin import FlextPluginHandlers
from tests import t


class TestFlextPluginHandlersHandlers:
    """Tests for FlextPluginHandlers class."""

    @pytest.fixture
    def handlers(self) -> FlextPluginHandlers:
        """Create handlers instance for testing."""
        return FlextPluginHandlers()

    def test_initialization(self, handlers: FlextPluginHandlers) -> None:
        """Test handlers initialization."""
        assert handlers is not None
        assert isinstance(handlers._handlers, dict)
        assert isinstance(handlers._event_history, list)

    def test_register_handler_success(self, handlers: FlextPluginHandlers) -> None:
        """Test successful handler registration."""

        async def sample_handler(
            event: Mapping[str, t.Container],
        ) -> Mapping[str, t.Container]:
            return {"value": event.get("key", "default")}

        result = handlers.register_handler("test_event", sample_handler)
        assert result.success
        assert result.value is True
        assert "test_event" in handlers._handlers
        assert len(handlers._handlers["test_event"]) == 1

    def test_register_handler_with_priority(
        self,
        handlers: FlextPluginHandlers,
    ) -> None:
        """Test handler registration with priority."""

        async def handler1(
            event: Mapping[str, t.Container],
        ) -> Mapping[str, t.Container]:
            _ = event
            return {"handler": "handler1"}

        async def handler2(
            event: Mapping[str, t.Container],
        ) -> Mapping[str, t.Container]:
            _ = event
            return {"handler": "handler2"}

        handlers.register_handler("priority_event", handler1, priority=1)
        handlers.register_handler("priority_event", handler2, priority=10)
        assert len(handlers._handlers["priority_event"]) == 2
        first_handler = handlers._handlers["priority_event"][0]
        assert first_handler.priority == 10

    def test_register_multiple_handlers(self, handlers: FlextPluginHandlers) -> None:
        """Test registering multiple handlers for different events."""

        async def handler_a(
            event: Mapping[str, t.Container],
        ) -> Mapping[str, t.Container]:
            _ = event
            return {"handler": "a"}

        async def handler_b(
            event: Mapping[str, t.Container],
        ) -> Mapping[str, t.Container]:
            _ = event
            return {"handler": "b"}

        handlers.register_handler("event_a", handler_a)
        handlers.register_handler("event_b", handler_b)
        assert "event_a" in handlers._handlers
        assert "event_b" in handlers._handlers
        assert len(handlers._handlers["event_a"]) == 1
        assert len(handlers._handlers["event_b"]) == 1

    def test_handlers_exist(self) -> None:
        """Test that FlextPluginHandlers class exists and is callable."""
        assert FlextPluginHandlers is not None
        assert callable(FlextPluginHandlers)

    def test_handlers_has_expected_methods(self, handlers: FlextPluginHandlers) -> None:
        """Test that handlers has expected methods."""
        assert callable(handlers.register_handler)
