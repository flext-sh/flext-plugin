"""Plugin payload validation and lifecycle projections through public owners.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest

from flext_plugin import FlextPluginApi, FlextPluginPlatform
from tests import c, m, tm


class TestsFlextPluginPlugin:
    """Owned payloads remain validated and are never reconstructed by registration."""

    @staticmethod
    def test_supplied_fields_and_default_version() -> None:
        """Configured version expectations come from the production constant owner."""
        payload = m.Plugin.Entity(name="payload-plugin", description="Caller metadata")
        tm.that(payload.name, eq="payload-plugin")
        tm.that(payload.description, eq="Caller metadata")
        tm.that(payload.plugin_version, eq=c.Plugin.DEFAULT_PLUGIN_VERSION)
        tm.that(
            payload.is_enabled,
            eq=m.Plugin.Entity.model_fields["is_enabled"].default,
        )

    @staticmethod
    @pytest.mark.parametrize("enabled", [True, False])
    def test_status_is_derived_from_supplied_enabled_state(*, enabled: bool) -> None:
        """Both entity and API projections observe the same stored payload."""
        payload = m.Plugin.Entity(name="status-plugin", is_enabled=enabled)
        api = FlextPluginApi()
        tm.ok(api.register_plugin(payload))
        expected = str(
            c.Plugin.PluginStatus.ACTIVE if enabled else c.Plugin.PluginStatus.INACTIVE
        )
        tm.that(api.fetch_plugin_status(payload.name).value, eq=expected)
        tm.that(api.resolve_plugin_active(payload.name).value, eq=enabled)
        tm.that(api.fetch_plugin(payload.name).value is payload, truth=True)

    @staticmethod
    @pytest.mark.parametrize(
        "bad_version", [c.ParserBooleanToken.ONE, "1.2.3.4", "1.x", "abc"]
    )
    def test_invalid_version_is_rejected_at_ingress(bad_version: str) -> None:
        """Invalid owned payloads never reach the registration operation."""
        with pytest.raises(c.ValidationError):
            m.Plugin.Entity(name="invalid-version-plugin", plugin_version=bad_version)

    @staticmethod
    def test_valid_owned_payload_passes_business_validation() -> None:
        """The business validator accepts a real validated domain payload."""
        payload = m.Plugin.Entity(name="valid-plugin")
        tm.ok(FlextPluginPlatform.Rules.validate_business_rules(payload))

    @staticmethod
    def test_multiple_plugins_preserve_registration_order_and_identity() -> None:
        """Listing resolves canonical entries instead of a second plugin cache."""
        api = FlextPluginApi()
        payloads = [
            m.Plugin.Entity(name=f"ordered-plugin-{index}") for index in range(3)
        ]
        for payload in payloads:
            tm.ok(api.register_plugin(payload))
        listed = api.list_plugins().value
        tm.that(len(listed), eq=len(payloads))
        for original, stored in zip(payloads, listed, strict=True):
            tm.that(stored is original, truth=True)
        for payload in payloads:
            tm.ok(api.unregister_plugin(payload.name))
        tm.that(api.list_plugins().value, eq=[])
