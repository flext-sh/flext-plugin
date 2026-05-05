"""Behavior contract for FlextPluginSettings post-isolation (rule 3)."""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_plugin import FlextPluginSettings


class TestsFlextPluginConfig:
    """FlextPluginSettings is fully isolated from root FlextSettings.

    No root concrete fields (``app_name``, ``debug``, ``trace``,
    ``enable_caching``, ``cache_ttl``, ``max_workers``, ``timeout_seconds``,
    ``api_key``, ``log_level``, ``database_url``) — only its own env-prefixed
    fields. These tests cover the singleton + clone + update_global contract
    inherited from FlextSettingsBase.
    """

    def setup_method(self) -> None:
        """Drop the per-class singleton between tests (Pydantic-2 native)."""
        FlextPluginSettings.reset_for_testing()

    def test_fetch_global_returns_singleton(self) -> None:
        """``fetch_global`` returns the same instance on subsequent calls."""
        first = FlextPluginSettings.fetch_global()
        second = FlextPluginSettings.fetch_global()
        tm.that(first is second, eq=True)

    def test_env_prefix_is_isolated_from_root(self) -> None:
        """``env_prefix`` must NOT be the root ``FLEXT_`` (rule 3)."""
        prefix = FlextPluginSettings.model_config.get("env_prefix")
        tm.that(prefix, eq="FLEXT_PLUGIN_")

    def test_clone_returns_independent_snapshot(self) -> None:
        """``clone()`` deep-copies without mutating the global singleton."""
        global_settings = FlextPluginSettings.fetch_global()
        snapshot = global_settings.clone()
        tm.that(snapshot is global_settings, eq=False)

    def test_update_global_rejects_unknown_field(self) -> None:
        """``update_global`` raises ValueError on undeclared field (typo guard)."""
        with pytest.raises(ValueError, match="FlextPluginSettings"):
            FlextPluginSettings.update_global(nonexistent_field=42)
