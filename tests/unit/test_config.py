"""Behavioral contract for :class:`FlextPluginSettings`.

Exercises only the public settings contract inherited from
``FlextSettings``: singleton retrieval, snapshot cloning with field
overrides, global update with typo-guarding, override-isolated retrieval
for dependency injection, and the env-prefix isolation from the root
``FLEXT_`` namespace (rule 3). No private attributes, internal
collaborators, or line-coverage pokes are touched.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from flext_core import FlextSettings

from flext_plugin import FlextPluginConfig, FlextPluginSettings, config
from tests import tm, u

if TYPE_CHECKING:
    from tests import t

# NOTE (multi-agent): no-mock/SSOT rewrite — the old _ROOT_FIELDS list asserted the
# absence of 7 fields (app_name, enable_caching, cache_ttl, max_workers,
# timeout_seconds, api_key, database_url) that the real FlextSettings root no
# longer declares, so the test was vacuous. The live contract is checked against
# the runtime SSOT instead: FlextSettings.model_fields is the single source of
# truth for the universal operational fields (debug/trace/log_level/timezone/
# async_logging), and FlextPluginSettings must neither add nor drop fields.
_UNIVERSAL_FIELDS: t.VariadicTuple[str] = (
    "debug",
    "trace",
    "log_level",
    "timezone",
    "async_logging",
)


class TestsFlextPluginConfig:
    """Public settings contract of the isolated plugin settings facade."""

    @staticmethod
    def test_business_namespace_validates_and_round_trips() -> None:
        """Typed YAML rules survive construction and JSON validation unchanged."""
        original = config.Plugin
        replacement_version = original.version.model_copy(
            update={"default": f"{original.version.default}-candidate"},
        )
        replacement = original.model_copy(update={"version": replacement_version})
        candidate = FlextPluginConfig(Plugin=replacement)
        restored = FlextPluginConfig.model_validate_json(candidate.model_dump_json())
        tm.that(restored.Plugin.model_dump(), eq=replacement.model_dump())
        tm.that(config.Plugin.model_dump(), eq=original.model_dump())

    @staticmethod
    def setup_method() -> None:
        """Drop the per-class singleton between tests (Pydantic-2 native)."""
        FlextPluginSettings.reset_for_testing()

    @staticmethod
    def test_fetch_global_returns_stable_singleton() -> None:
        """``fetch_global`` returns the same instance on repeated calls."""
        first = FlextPluginSettings.fetch_global()
        second = FlextPluginSettings.fetch_global()
        tm.ok(first is second)

    @staticmethod
    def test_reset_for_testing_reloads_the_imported_singleton() -> None:
        """Reset reloads environment values without invalidating imported handles."""
        original = FlextPluginSettings.fetch_global()
        debug = original.debug
        prefix = tm.not_none(FlextPluginSettings.model_config.get("env_prefix"))
        with u.Tests.env_vars_context(
            env_vars={f"{prefix}DEBUG": str(not debug).lower()},
        ):
            FlextPluginSettings.reset_for_testing()
            replacement = FlextPluginSettings.fetch_global()
            tm.ok(replacement is original)
            tm.that(original.debug, eq=not debug)
        FlextPluginSettings.reset_for_testing()
        tm.that(original.debug, eq=debug)

    @staticmethod
    def test_env_prefix_is_isolated_from_root() -> None:
        """``env_prefix`` is the plugin namespace, never the root ``FLEXT_``."""
        prefix = FlextPluginSettings.model_config.get("env_prefix")
        tm.that(prefix, eq="FLEXT_PLUGIN_")

    @staticmethod
    def test_plugin_settings_match_root_field_contract() -> None:
        """Plugin settings declare exactly the FlextSettings SSOT root fields."""
        tm.that(
            set(FlextPluginSettings.model_fields),
            eq=frozenset(FlextSettings.model_fields),
        )

    @staticmethod
    @pytest.mark.parametrize("universal_field", _UNIVERSAL_FIELDS)
    def test_universal_fields_are_inherited(universal_field: str) -> None:
        """Every universal operational flag is inherited from the SSOT root."""
        tm.ok(universal_field in FlextPluginSettings.model_fields)

    @staticmethod
    def test_clone_returns_independent_snapshot() -> None:
        """``clone`` yields a distinct instance with equal public state."""
        global_settings = FlextPluginSettings.fetch_global()
        snapshot = global_settings.clone()
        tm.fail(snapshot is global_settings)
        tm.that(snapshot.model_dump(), eq=global_settings.model_dump())

    @staticmethod
    def test_clone_applies_field_overrides() -> None:
        """``clone(**overrides)`` merges overrides without touching the source."""
        global_settings = FlextPluginSettings.fetch_global()
        overridden = global_settings.clone(debug=True)
        tm.ok(overridden.debug)
        tm.fail(overridden is global_settings)
        tm.fail(global_settings.debug)

    @staticmethod
    def test_clone_does_not_replace_global_singleton() -> None:
        """Cloning must not mutate or swap the shared global instance."""
        global_settings = FlextPluginSettings.fetch_global()
        global_settings.clone()
        tm.ok(FlextPluginSettings.fetch_global() is global_settings)

    @staticmethod
    def test_update_global_installs_returned_instance() -> None:
        """``update_global`` returns the instance that becomes the new global."""
        updated = FlextPluginSettings.update_global(debug=True)
        tm.ok(updated.debug)
        tm.ok(FlextPluginSettings.fetch_global() is updated)

    @staticmethod
    def test_update_global_rejects_unknown_field() -> None:
        """``update_global`` raises ``ValueError`` naming the settings class."""
        with pytest.raises(ValueError, match="FlextPluginSettings"):
            FlextPluginSettings.update_global(nonexistent_field=42)

    @staticmethod
    def test_fetch_global_overrides_returns_isolated_clone() -> None:
        """``fetch_global(overrides=...)`` yields an isolated instance for DI."""
        global_settings = FlextPluginSettings.fetch_global()
        injected = FlextPluginSettings.fetch_global(overrides={"debug": True})
        tm.fail(injected is global_settings)
        tm.ok(injected.debug)

    @staticmethod
    def test_fetch_global_overrides_does_not_mutate_singleton() -> None:
        """Override-isolated retrieval must not touch the shared singleton."""
        global_settings = FlextPluginSettings.fetch_global()
        FlextPluginSettings.fetch_global(overrides={"debug": True})
        tm.ok(FlextPluginSettings.fetch_global() is global_settings)
        tm.fail(global_settings.debug)
