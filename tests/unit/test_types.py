"""Unit tests for FlextPluginTypes.

Tests type namespace organization and type alias accessibility
via canonical t.Plugin namespace.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import tm

from flext_plugin import FlextPluginTypes
from tests import t


class TestsFlextPluginTypes:
    """Test cases for FlextPluginTypes."""

    def test_types_alias_matches_facade(self) -> None:
        """T alias inherits from FlextPluginTypes facade."""
        tm.that(FlextPluginTypes in t.__mro__, eq=True)
