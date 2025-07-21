"""Plugin validation system for comprehensive plugin verification.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

import inspect
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flext_plugin.core.base import Plugin


class ValidationRule:
    """Base class for plugin validation rules."""

    def __init__(self, rule_id: str, description: str) -> None:
        """Initialize validation rule.

        Args:
            rule_id: Unique identifier for the validation rule.
            description: Human-readable description of what the rule validates.

        """
        self.rule_id = rule_id
        self.description = description

    def validate(self, plugin: type[Plugin] | Plugin) -> tuple[bool, str | None]:
        """Validate a plugin against this rule.

        Args:
            plugin: Plugin class or instance to validate.

        Returns:
            Tuple of (is_valid, error_message).

        """
        # Default implementation passes validation
        return True, None


class MetadataValidationRule(ValidationRule):
    """Validates plugin metadata completeness and correctness."""

    def __init__(self) -> None:
        """Initialize metadata validation rule."""
        super().__init__(
            "metadata_validation",
            "Validates plugin metadata is complete and valid",
        )

    def validate(self, plugin: type[Plugin] | Plugin) -> tuple[bool, str | None]:
        """Validate plugin metadata completeness and correctness.

        Args:
            plugin: Plugin class or instance to validate.

        Returns:
            Tuple of (is_valid, error_message).

        """
        # Get metadata from class or instance
        if inspect.isclass(plugin):
            if not hasattr(plugin, "METADATA"):
                return False, "Plugin class missing METADATA attribute"
            # For class validation, we need to access the class attribute directly
            metadata = plugin.METADATA
        else:
            # Get metadata from instance
            metadata = plugin.metadata

        # Metadata should be a PluginMetadata object, not callable
        if metadata is None:
            return False, "Plugin metadata is None"

        # If metadata is callable (shouldn't happen with proper Plugin implementation)
        if callable(metadata):
            return False, "Plugin metadata should not be callable"

        # Validate required fields
        required_fields = ["name", "version", "plugin_type"]

        missing_fields = [
            field for field in required_fields if not getattr(metadata, field, None)
        ]

        if missing_fields:
            return (
                False,
                f"Missing required metadata fields: {', '.join(missing_fields)}",
            )

        # Validate version format (semantic versioning)
        version_pattern = re.compile(r"^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$")
        if not version_pattern.match(metadata.version):
            return (
                False,
                f"Invalid version format: {metadata.version} "
                f"(expected semantic versioning)",
            )

        # Validate plugin name format (used as identifier)
        name_pattern = re.compile(r"^[a-zA-Z0-9]+([_-][a-zA-Z0-9]+)*$")
        if not name_pattern.match(metadata.name):
            return (
                False,
                f"Invalid plugin name format: {metadata.name} "
                f"(expected alphanumeric with underscores/hyphens)",
            )

        return True, None


class InterfaceValidationRule(ValidationRule):
    """Validates plugin implements required interfaces."""

    def __init__(self) -> None:
        """Initialize interface validation rule."""
        super().__init__(
            "interface_validation",
            "Validates plugin implements required interfaces",
        )

    def validate(self, plugin: type[Plugin] | Plugin) -> tuple[bool, str | None]:
        """Validate plugin implements required interfaces.

        Args:
            plugin: Plugin class or instance to validate.

        Returns:
            Tuple of (is_valid, error_message).

        """
        plugin_class = plugin if inspect.isclass(plugin) else type(plugin)

        # Check if plugin has required methods
        required_methods = ["execute", "initialize", "cleanup", "health_check"]

        missing_methods = [
            method for method in required_methods if not hasattr(plugin_class, method)
        ]

        if missing_methods:
            return (
                False,
                f"Plugin missing required methods: {', '.join(missing_methods)}",
            )

        return True, None


class PluginValidator:
    """Comprehensive plugin validator using validation rules."""

    def __init__(self) -> None:
        """Initialize plugin validator with default rules."""
        self.rules = [
            MetadataValidationRule(),
            InterfaceValidationRule(),
        ]

    def validate_plugin(self, plugin: type[Plugin] | Plugin) -> tuple[bool, list[str]]:
        """Validate a plugin against all rules.

        Args:
            plugin: Plugin class or instance to validate.

        Returns:
            Tuple of (is_valid, list_of_errors).

        """
        errors = []

        for rule in self.rules:
            is_valid, error_msg = rule.validate(plugin)
            if not is_valid and error_msg:
                errors.append(f"{rule.rule_id}: {error_msg}")

        return len(errors) == 0, errors

    def add_rule(self, rule: ValidationRule) -> None:
        """Add a custom validation rule.

        Args:
            rule: The validation rule to add.

        """
        self.rules.append(rule)

    def remove_rule(self, rule_id: str) -> bool:
        """Remove a validation rule by ID.

        Args:
            rule_id: The ID of the rule to remove.

        Returns:
            True if rule was found and removed, False otherwise.

        """
        for i, rule in enumerate(self.rules):
            if rule.rule_id == rule_id:
                del self.rules[i]
                return True
        return False
