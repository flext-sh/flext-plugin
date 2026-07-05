"""Behavioral contract for :class:`FlextPluginSettings`.

Exercises only the public settings contract inherited from
``FlextSettingsBase``: singleton retrieval, snapshot cloning, global update
with typo-guarding, dependency-injection cloning, override merging, and the
env-prefix isolation from the root ``FLEXT_`` namespace (rule 3). No private
attributes, internal collaborators, or line-coverage pokes are touched.
"""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_plugin import FlextPluginSettings

# Root-level concrete fields that FlextPluginSettings must NOT inherit as its
# own declared fields — isolation contract (rule 3).
_ROOT_FIELDS: tuple[str, ...] = (
    "app_name",
    "debug",
    "trace",
    "enable_caching",
    "cache_ttl",
    "max_workers",
    "timeout_seconds",
    "api_key",
    "log_level",
    "database_url",
)


class TestsFlextPluginConfig:
    """Public settings contract of the isolated plugin settings facade."""

    def setup_method(self) -> None:
        """Drop the per-class singleton between tests (Pydantic-2 native)."""
        FlextPluginSettings.reset_for_testing()

    def test_fetch_global_returns_stable_singleton(self) -> None:
        """``fetch_global`` returns the same instance on repeated calls."""
        first = FlextPluginSettings.fetch_global()
        second = FlextPluginSettings.fetch_global()
        tm.that(first is second, eq=True)

    def test_reset_for_testing_replaces_singleton(self) -> None:
        """``reset_for_testing`` forces a fresh singleton on next fetch."""
        original = FlextPluginSettings.fetch_global()
        FlextPluginSettings.reset_for_testing()
        replacement = FlextPluginSettings.fetch_global()
        tm.that(replacement is original, eq=False)

    def test_env_prefix_is_isolated_from_root(self) -> None:
        """``env_prefix`` is the plugin namespace, never the root ``FLEXT_``."""
        prefix = FlextPluginSettings.model_config.get("env_prefix")
        tm.that(prefix, eq="FLEXT_PLUGIN_")

    @pytest.mark.parametrize("root_field", _ROOT_FIELDS)
    def test_root_concrete_fields_are_not_declared(self, root_field: str) -> None:
        """No root concrete field leaks into the plugin field contract."""
        tm.that(root_field in FlextPluginSettings.model_fields, eq=False)

    def test_clone_returns_independent_snapshot(self) -> None:
        """``clone`` yields a distinct instance with equal public state."""
        global_settings = FlextPluginSettings.fetch_global()
        snapshot = global_settings.clone()
        tm.that(snapshot is global_settings, eq=False)
        tm.that(snapshot.model_dump(), eq=global_settings.model_dump())

    def test_clone_does_not_replace_global_singleton(self) -> None:
        """Cloning must not mutate or swap the shared global instance."""
        global_settings = FlextPluginSettings.fetch_global()
        global_settings.clone()
        tm.that(FlextPluginSettings.fetch_global() is global_settings, eq=True)

    def test_update_global_installs_returned_instance(self) -> None:
        """``update_global`` returns the instance that becomes the new global."""
        updated = FlextPluginSettings.update_global()
        tm.that(isinstance(updated, FlextPluginSettings), eq=True)
        tm.that(FlextPluginSettings.fetch_global() is updated, eq=True)

    def test_update_global_rejects_unknown_field(self) -> None:
        """``update_global`` raises ``ValueError`` naming the settings class."""
        with pytest.raises(ValueError, match="FlextPluginSettings"):
            FlextPluginSettings.update_global(nonexistent_field=42)

    def test_clone_for_injection_passes_through_none(self) -> None:
        """``clone_for_injection(None)`` yields ``None`` (optional contract)."""
        tm.that(FlextPluginSettings.clone_for_injection(None), eq=None)

    def test_clone_for_injection_returns_independent_clone(self) -> None:
        """``clone_for_injection`` deep-copies a provided settings instance."""
        global_settings = FlextPluginSettings.fetch_global()
        injected = FlextPluginSettings.clone_for_injection(global_settings)
        tm.that(isinstance(injected, FlextPluginSettings), eq=True)
        tm.that(injected is global_settings, eq=False)

    def test_merge_overrides_returns_mapping(self) -> None:
        """``merge_overrides`` yields a dict of the effective override state."""
        global_settings = FlextPluginSettings.fetch_global()
        merged = FlextPluginSettings.merge_overrides(global_settings)
        tm.that(isinstance(merged, dict), eq=True)


__all__: list[str] = ["TestsFlextPluginConfig"]
