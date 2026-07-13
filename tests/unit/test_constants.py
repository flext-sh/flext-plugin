"""Unit tests for FlextPluginConstants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from tests.constants import c

__all__: list[str] = ["TestsFlextPluginConstantsUnit"]


class TestsFlextPluginConstantsUnit:
    """Behavioral contract tests for FlextPluginConstants."""

    def test_category_types_are_nonempty_frozensets(self) -> None:
        """Each plugin-type category exposes a non-empty immutable frozenset."""
        categories = (
            c.Plugin.SINGER_PLUGIN_TYPES,
            c.Plugin.ARCHITECTURE_PLUGIN_TYPES,
            c.Plugin.INTEGRATION_PLUGIN_TYPES,
            c.Plugin.UTILITY_PLUGIN_TYPES,
            c.Plugin.ALL_PLUGIN_TYPES,
        )
        for category in categories:
            assert isinstance(category, frozenset)
            assert len(category) > 0

    @pytest.mark.parametrize(
        ("category", "expected_values"),
        [
            (c.Plugin.SINGER_PLUGIN_TYPES, {"tap", "target", "transform"}),
            (
                c.Plugin.ARCHITECTURE_PLUGIN_TYPES,
                {"addon", "core", "language", "theme"},
            ),
            (
                c.Plugin.INTEGRATION_PLUGIN_TYPES,
                {
                    "api",
                    "authentication",
                    "authorization",
                    "database",
                    "middleware",
                    "notification",
                    "service",
                },
            ),
            (
                c.Plugin.UTILITY_PLUGIN_TYPES,
                {
                    "extension",
                    "handler",
                    "processor",
                    "tool",
                    "transformer",
                    "utility",
                },
            ),
        ],
    )
    def test_category_exact_membership(
        self,
        category: frozenset[c.Plugin.Type],
        expected_values: set[str],
    ) -> None:
        """Each category contains exactly its documented plugin type values."""
        assert {member.value for member in category} == expected_values

    def test_all_types_is_disjoint_union_of_categories(self) -> None:
        """ALL_PLUGIN_TYPES equals the exact union of the four disjoint categories."""
        singer = c.Plugin.SINGER_PLUGIN_TYPES
        arch = c.Plugin.ARCHITECTURE_PLUGIN_TYPES
        integration = c.Plugin.INTEGRATION_PLUGIN_TYPES
        utility = c.Plugin.UTILITY_PLUGIN_TYPES

        union = singer | arch | integration | utility
        assert union == c.Plugin.ALL_PLUGIN_TYPES
        # A disjoint union preserves total cardinality (no overlap, no loss).
        assert len(union) == len(singer) + len(arch) + len(integration) + len(utility)

    @pytest.mark.parametrize(
        ("left", "right"),
        [
            (c.Plugin.SINGER_PLUGIN_TYPES, c.Plugin.ARCHITECTURE_PLUGIN_TYPES),
            (c.Plugin.SINGER_PLUGIN_TYPES, c.Plugin.INTEGRATION_PLUGIN_TYPES),
            (c.Plugin.SINGER_PLUGIN_TYPES, c.Plugin.UTILITY_PLUGIN_TYPES),
            (c.Plugin.ARCHITECTURE_PLUGIN_TYPES, c.Plugin.INTEGRATION_PLUGIN_TYPES),
            (c.Plugin.ARCHITECTURE_PLUGIN_TYPES, c.Plugin.UTILITY_PLUGIN_TYPES),
            (c.Plugin.INTEGRATION_PLUGIN_TYPES, c.Plugin.UTILITY_PLUGIN_TYPES),
        ],
    )
    def test_categories_are_pairwise_disjoint(
        self,
        left: frozenset[c.Plugin.Type],
        right: frozenset[c.Plugin.Type],
    ) -> None:
        """No plugin type belongs to more than one category."""
        assert left.isdisjoint(right)
        assert left.issubset(c.Plugin.ALL_PLUGIN_TYPES)
        assert right.issubset(c.Plugin.ALL_PLUGIN_TYPES)

    @pytest.mark.parametrize(
        ("attribute", "expected"),
        [
            ("PYTHON_EXTENSION", ".py"),
            ("YAML_CONFIG_EXTENSION", ".yaml"),
            ("JSON_CONFIG_EXTENSION", ".json"),
            ("TOML_CONFIG_EXTENSION", ".toml"),
            ("DEFAULT_PLUGIN_DIR", "plugins"),
            ("DEFAULT_CACHE_DIR", ".plugin_cache"),
            ("DEFAULT_CONFIG_DIR", "settings"),
        ],
    )
    def test_file_constants_exact_values(
        self,
        attribute: str,
        expected: str,
    ) -> None:
        """File-related constants expose their exact documented string values."""
        assert getattr(c.Plugin.Files, attribute) == expected

    def test_config_extensions_are_distinct(self) -> None:
        """Each configuration format maps to a unique file extension."""
        extensions = {
            c.Plugin.Files.YAML_CONFIG_EXTENSION,
            c.Plugin.Files.JSON_CONFIG_EXTENSION,
            c.Plugin.Files.TOML_CONFIG_EXTENSION,
        }
        assert len(extensions) == 3

    def test_extensions_start_with_dot(self) -> None:
        """Every declared file extension is dot-prefixed."""
        for extension in (
            c.Plugin.Files.PYTHON_EXTENSION,
            c.Plugin.Files.YAML_CONFIG_EXTENSION,
            c.Plugin.Files.JSON_CONFIG_EXTENSION,
            c.Plugin.Files.TOML_CONFIG_EXTENSION,
        ):
            assert extension.startswith(".")
