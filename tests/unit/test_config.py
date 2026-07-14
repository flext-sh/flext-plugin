"""Behavioral contract for :class:`FlextPluginSettings`.

Exercises only the public settings contract inherited from
``FlextSettings``: singleton retrieval, snapshot cloning with field
overrides, global update with typo-guarding, override-isolated retrieval
for dependency injection, and the env-prefix isolation from the root
``FLEXT_`` namespace (rule 3). No private attributes, internal
collaborators, or line-coverage pokes are touched.
"""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_core import FlextSettings
from flext_plugin import FlextPluginSettings

# NOTE (multi-agent): no-mock/SSOT rewrite — the old _ROOT_FIELDS list asserted the
# absence of 7 fields (app_name, enable_caching, cache_ttl, max_workers,
# timeout_seconds, api_key, database_url) that the real FlextSettings root no
# longer declares, so the test was vacuous. The live contract is checked against
# the runtime SSOT instead: FlextSettings.model_fields is the single source of
# truth for the universal operational fields (debug/trace/log_level/timezone/
# async_logging), and FlextPluginSettings must neither add nor drop fields.
_UNIVERSAL_FIELDS: tuple[str, ...] = (
    "debug",
    "trace",
    "log_level",
    "timezone",
    "async_logging",
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

    def test_plugin_settings_match_root_field_contract(self) -> None:
        """Plugin settings declare exactly the FlextSettings SSOT root fields."""
        tm.that(
            set(FlextPluginSettings.model_fields),
            eq=set(FlextSettings.model_fields),
        )

    @pytest.mark.parametrize("universal_field", _UNIVERSAL_FIELDS)
    def test_universal_fields_are_inherited(self, universal_field: str) -> None:
        """Every universal operational flag is inherited from the SSOT root."""
        tm.that(universal_field in FlextPluginSettings.model_fields, eq=True)

    def test_clone_returns_independent_snapshot(self) -> None:
        """``clone`` yields a distinct instance with equal public state."""
        global_settings = FlextPluginSettings.fetch_global()
        snapshot = global_settings.clone()
        tm.that(snapshot is global_settings, eq=False)
        tm.that(snapshot.model_dump(), eq=global_settings.model_dump())

    def test_clone_applies_field_overrides(self) -> None:
        """``clone(**overrides)`` merges overrides without touching the source."""
        global_settings = FlextPluginSettings.fetch_global()
        overridden = global_settings.clone(debug=True)
        tm.that(overridden.debug, eq=True)
        tm.that(overridden is global_settings, eq=False)
        tm.that(global_settings.debug, eq=False)

    def test_clone_does_not_replace_global_singleton(self) -> None:
        """Cloning must not mutate or swap the shared global instance."""
        global_settings = FlextPluginSettings.fetch_global()
        global_settings.clone()
        tm.that(FlextPluginSettings.fetch_global() is global_settings, eq=True)

    def test_update_global_installs_returned_instance(self) -> None:
        """``update_global`` returns the instance that becomes the new global."""
        updated = FlextPluginSettings.update_global(debug=True)
        tm.that(updated.debug, eq=True)
        tm.that(FlextPluginSettings.fetch_global() is updated, eq=True)

    def test_update_global_rejects_unknown_field(self) -> None:
        """``update_global`` raises ``ValueError`` naming the settings class."""
        with pytest.raises(ValueError, match="FlextPluginSettings"):
            FlextPluginSettings.update_global(nonexistent_field=42)

    def test_fetch_global_overrides_returns_isolated_clone(self) -> None:
        """``fetch_global(overrides=...)`` yields an isolated instance for DI."""
        global_settings = FlextPluginSettings.fetch_global()
        injected = FlextPluginSettings.fetch_global(overrides={"debug": True})
        tm.that(isinstance(injected, FlextPluginSettings), eq=True)
        tm.that(injected is global_settings, eq=False)
        tm.that(injected.debug, eq=True)

    def test_fetch_global_overrides_does_not_mutate_singleton(self) -> None:
        """Override-isolated retrieval must not touch the shared singleton."""
        global_settings = FlextPluginSettings.fetch_global()
        FlextPluginSettings.fetch_global(overrides={"debug": True})
        tm.that(FlextPluginSettings.fetch_global() is global_settings, eq=True)
        tm.that(global_settings.debug, eq=False)


__all__: list[str] = ["TestsFlextPluginConfig"]
