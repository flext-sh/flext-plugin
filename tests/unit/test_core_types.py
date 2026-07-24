"""Behavioral test suite for flext-plugin core type definitions.

Validates the OBSERVABLE PUBLIC CONTRACT of the plugin constant enums and the
exception family: enum membership, string round-trips, membership frozensets,
status-classification behavior, and error construction. All assertions target
public behavior only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_tests import e, tm
from tests import c

_Type = c.Plugin.Type
_Status = c.Plugin.PluginStatus


class TestsFlextPluginCoreTypes:
    """Behavioral contract of c.Plugin.Type / PluginStatus enums and errors."""

    @pytest.mark.parametrize(
        ("member", "value"),
        [
            (_Type.TAP, "tap"),
            (_Type.TARGET, "target"),
            (_Type.TRANSFORM, "transform"),
            (_Type.UTILITY, "utility"),
            (_Type.SERVICE, "service"),
            (_Type.CORE, "core"),
        ],
    )
    def test_plugin_type_member_carries_its_string_value(
        self, member: c.Plugin.Type, value: str
    ) -> None:
        """Each plugin-type member exposes its canonical lowercase string."""
        tm.that(member.value, eq=value)
        tm.that(member, eq=value)  # StrEnum equality with the raw string

    @pytest.mark.parametrize(
        "value", ["tap", "target", "transform", "utility", "service", "core"]
    )
    def test_plugin_type_round_trips_from_string(self, value: str) -> None:
        """Constructing from a valid string yields the matching member back."""
        tm.that(c.Plugin.Type(value).value, eq=value)

    def test_plugin_type_invalid_string_raises_value_error(self) -> None:
        """An unknown string is rejected with ValueError naming the input."""
        with pytest.raises(ValueError, match=r"invalid_type"):
            c.Plugin.Type("invalid_type")

    def test_plugin_type_membership_frozensets_partition_all_types(self) -> None:
        """The category frozensets are disjoint and union to ALL_PLUGIN_TYPES."""
        p = c.Plugin
        groups = [
            p.SINGER_PLUGIN_TYPES,
            p.ARCHITECTURE_PLUGIN_TYPES,
            p.INTEGRATION_PLUGIN_TYPES,
            p.UTILITY_PLUGIN_TYPES,
        ]
        union: frozenset[str] = frozenset().union(*groups)
        tm.that(union, eq=p.ALL_PLUGIN_TYPES)
        total = sum(len(g) for g in groups)
        tm.that(total, eq=len(union))  # disjoint: no type in two categories

    @pytest.mark.parametrize("member", [_Type.TAP, _Type.TARGET, _Type.TRANSFORM])
    def test_singer_types_belong_to_singer_group(self, member: c.Plugin.Type) -> None:
        """Singer plugin types are classified in the Singer frozenset."""
        tm.that(c.Plugin.SINGER_PLUGIN_TYPES, has=member)
        tm.that(c.Plugin.ALL_PLUGIN_TYPES, has=member)

    @pytest.mark.parametrize(
        ("member", "value"),
        [
            (_Status.UNKNOWN, "unknown"),
            (_Status.DISCOVERED, "discovered"),
            (_Status.LOADED, "loaded"),
            (_Status.ACTIVE, "active"),
            (_Status.ERROR, "error"),
            (_Status.HEALTHY, "healthy"),
            (_Status.UNHEALTHY, "unhealthy"),
            (_Status.DISABLED, "disabled"),
        ],
    )
    def test_plugin_status_member_carries_its_string_value(
        self, member: c.Plugin.PluginStatus, value: str
    ) -> None:
        """Each status member exposes its canonical lowercase string."""
        tm.that(member.value, eq=value)
        assert c.Plugin.PluginStatus(value) is member

    @pytest.mark.parametrize(
        "member", [_Status.ERROR, _Status.UNHEALTHY, _Status.DISABLED]
    )
    def test_error_states_report_as_error_and_not_operational(
        self, member: c.Plugin.PluginStatus
    ) -> None:
        """Error-class statuses classify as error and never operational."""
        tm.that(member.is_error_state(), eq=True)
        tm.that(member.is_operational(), eq=False)
        tm.that(c.Plugin.PluginStatus.get_error_statuses(), has=member)

    @pytest.mark.parametrize(
        "member", [_Status.ACTIVE, _Status.HEALTHY, _Status.LOADED]
    )
    def test_operational_states_report_as_operational_and_not_error(
        self, member: c.Plugin.PluginStatus
    ) -> None:
        """Operational statuses classify as operational and never error."""
        tm.that(member.is_operational(), eq=True)
        tm.that(member.is_error_state(), eq=False)
        tm.that(c.Plugin.PluginStatus.get_operational_statuses(), has=member)

    def test_error_and_operational_status_sets_are_disjoint(self) -> None:
        """No status is simultaneously an error state and operational."""
        errors = c.Plugin.PluginStatus.get_error_statuses()
        operational = c.Plugin.PluginStatus.get_operational_statuses()
        assert errors.isdisjoint(operational)

    def test_plugin_status_invalid_string_raises_value_error(self) -> None:
        """An unknown status string is rejected with ValueError."""
        with pytest.raises(ValueError, match=r"not_a_status"):
            c.Plugin.PluginStatus("not_a_status")

    @pytest.mark.parametrize(
        ("member", "value"),
        [
            (c.Plugin.DiscoveryTypeLiteral.FILE, "file"),
            (c.Plugin.DiscoveryTypeLiteral.DIRECTORY, "directory"),
            (c.Plugin.DiscoveryTypeLiteral.ENTRY_POINT, "entry_point"),
        ],
    )
    def test_discovery_type_literal_values(
        self, member: c.Plugin.DiscoveryTypeLiteral, value: str
    ) -> None:
        """Discovery-type literals expose their canonical string values."""
        tm.that(member.value, eq=value)

    def test_base_error_preserves_message_and_is_exception(self) -> None:
        """BaseError is raisable, carries its message, and is an Exception."""
        message = "plugin failed to load"
        with pytest.raises(e.BaseError, match=r"plugin failed to load") as excinfo:
            raise e.BaseError(message)
        tm.that(str(excinfo.value), has=message)
        tm.that(excinfo.value, is_=Exception)
