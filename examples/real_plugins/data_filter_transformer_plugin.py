"""Data Filter Transformer Plugin - Real Data Processing Implementation.

This plugin demonstrates a working transformer that filters data based on
configurable conditions. It supports multiple filter types and operators
for flexible data processing pipelines.
"""

import re
from collections.abc import Callable
from datetime import datetime
from typing import Any

from flext_plugin.base import BaseTransformerPlugin, PluginMetadata
from flext_plugin.types import PluginError, PluginType


class DataFilterTransformerPlugin(BaseTransformerPlugin):
    """Data filter transformer plugin with real data processing capabilities.

    This plugin can filter data with:
    - Multiple condition types (equals, contains, range, regex)
    - Logical operators (AND, OR, NOT)
    - Data type-aware comparisons
    - Configurable filter rules
    - Statistics tracking for filtered vs passed records
    """

    METADATA = PluginMetadata(
        id="data-filter-transformer",
        name="Data Filter Transformer",
        version="1.0.0",
        description="Filter data records based on configurable conditions and rules",
        plugin_type=PluginType.TRANSFORMER,
        author="FLEXT Team",
        license="MIT",
        entry_point="data_filter_transformer_plugin.DataFilterTransformerPlugin",
        capabilities=[
            "data_filtering",
            "condition_evaluation",
            "logical_operators",
            "type_aware_comparison",
            "statistics_tracking",
        ],
        configuration_schema={
            "type": "object",
            "properties": {
                "filter_rules": {
                    "type": "array",
                    "description": "List of filter rules to apply",
                    "items": {
                        "type": "object",
                        "properties": {
                            "field": {
                                "type": "string",
                                "description": "Field name to filter on",
                            },
                            "operator": {
                                "type": "string",
                                "enum": [
                                    "equals",
                                    "not_equals",
                                    "contains",
                                    "not_contains",
                                    "starts_with",
                                    "ends_with",
                                    "regex",
                                    "greater_than",
                                    "less_than",
                                    "between",
                                    "in",
                                    "not_in",
                                    "is_null",
                                    "is_not_null",
                                ],
                                "description": "Filter operator",
                            },
                            "value": {"description": "Value to compare against"},
                            "case_sensitive": {
                                "type": "boolean",
                                "default": True,
                                "description": "Case sensitive comparison for string operations",
                            },
                        },
                        "required": ["field", "operator"],
                    },
                },
                "logic_operator": {
                    "type": "string",
                    "enum": ["AND", "OR"],
                    "default": "AND",
                    "description": "Logical operator to combine multiple rules",
                },
                "include_statistics": {
                    "type": "boolean",
                    "default": True,
                    "description": "Include filtering statistics in output metadata",
                },
                "fail_on_missing_field": {
                    "type": "boolean",
                    "default": False,
                    "description": "Fail transformation if filter field is missing from record",
                },
            },
            "required": ["filter_rules"],
        },
        default_configuration={
            "logic_operator": "AND",
            "include_statistics": True,
            "fail_on_missing_field": False,
        },
    )

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize data filter transformer plugin."""
        super().__init__(config)
        self._filter_rules: list[dict[str, Any]] = []
        self._logic_operator: str = "AND"
        self._include_statistics: bool = True
        self._fail_on_missing_field: bool = False
        self._statistics: dict[str, Any] = {}

    async def initialize(self) -> None:
        """Initialize plugin with filter configuration."""
        self._filter_rules = self._config.get("filter_rules", [])
        self._logic_operator = self._config.get("logic_operator", "AND")
        self._include_statistics = self._config.get("include_statistics", True)
        self._fail_on_missing_field = self._config.get("fail_on_missing_field", False)

        if not self._filter_rules:
            msg = "At least one filter rule must be specified"
            raise PluginError(
                msg,
                plugin_id=self.metadata.id,
                error_code="MISSING_CONFIG",
            )

        # Validate filter rules
        for i, rule in enumerate(self._filter_rules):
            if not all(key in rule for key in ["field", "operator"]):
                msg = f"Filter rule {i} missing required fields (field, operator)"
                raise PluginError(
                    msg,
                    plugin_id=self.metadata.id,
                    error_code="INVALID_FILTER_RULE",
                )

            # Validate operator
            valid_operators = {
                "equals",
                "not_equals",
                "contains",
                "not_contains",
                "starts_with",
                "ends_with",
                "regex",
                "greater_than",
                "less_than",
                "between",
                "in",
                "not_in",
                "is_null",
                "is_not_null",
            }
            if rule["operator"] not in valid_operators:
                msg = f"Invalid operator '{rule['operator']}' in filter rule {i}"
                raise PluginError(
                    msg,
                    plugin_id=self.metadata.id,
                    error_code="INVALID_OPERATOR",
                )

        # Reset statistics
        self._reset_statistics()
        self._initialized = True

    async def transform(
        self, data: Any, transform_config: dict[str, Any]
    ) -> dict[str, Any]:
        """Transform data by applying filter rules.

        Args:
        ----
            data: Input data (list of records or single record)
            transform_config: Additional transformation configuration

        Returns:
        -------
            Dictionary containing filtered data and metadata

        """
        if not self._initialized:
            msg = "Plugin not initialized"
            raise PluginError(
                msg,
                plugin_id=self.metadata.id,
                error_code="NOT_INITIALIZED",
            )

        # Override config with transform_config
        filter_rules = transform_config.get("filter_rules", self._filter_rules)
        logic_operator = transform_config.get("logic_operator", self._logic_operator)

        try:
            # Reset statistics for this transformation
            self._reset_statistics()

            # Handle different input data formats
            if isinstance(data, dict):
                if "data" in data:
                    # Input is a plugin result with data field
                    records = data["data"]
                    input_metadata = data.get("metadata", {})
                else:
                    # Input is a single record
                    records = [data]
                    input_metadata = {}
            elif isinstance(data, list):
                # Input is a list of records
                records = data
                input_metadata = {}
            else:
                msg = f"Unsupported input data type: {type(data)}"
                raise PluginError(
                    msg,
                    plugin_id=self.metadata.id,
                    error_code="INVALID_INPUT_TYPE",
                )

            # Apply filters
            filtered_records = []
            for record in records:
                self._statistics["total_records"] += 1

                if self._evaluate_record(record, filter_rules, logic_operator):
                    filtered_records.append(record)
                    self._statistics["passed_records"] += 1
                else:
                    self._statistics["filtered_records"] += 1

            # Calculate statistics
            self._statistics["filter_rate"] = (
                self._statistics["filtered_records"] / self._statistics["total_records"]
                if self._statistics["total_records"] > 0
                else 0
            )

            # Build result metadata
            output_metadata = {
                "transformation_timestamp": datetime.now().isoformat(),
                "transformer": self.metadata.name,
                "filter_rules_applied": len(filter_rules),
                "logic_operator": logic_operator,
                "input_metadata": input_metadata,
            }

            if self._include_statistics:
                output_metadata["filter_statistics"] = self._statistics.copy()

            return {
                "data": filtered_records,
                "metadata": output_metadata,
                "success": True,
            }

        except Exception as e:
            msg = f"Failed to apply data filters: {e}"
            raise PluginError(
                msg,
                plugin_id=self.metadata.id,
                error_code="TRANSFORMATION_FAILED",
                cause=e,
            )

    async def health_check(self) -> dict[str, Any]:
        """Perform health check."""
        health = {
            "status": "healthy",
            "plugin_id": self.metadata.id,
            "initialized": self._initialized,
            "filter_rules_count": len(self._filter_rules),
            "logic_operator": self._logic_operator,
            "checks": [],
        }

        # Check filter rules
        if not self._filter_rules:
            health["checks"].append("No filter rules configured")
            health["status"] = "degraded"
        else:
            health["checks"].append(
                f"Filter rules configured: {len(self._filter_rules)}"
            )

        # Validate each filter rule
        invalid_rules = 0
        for i, rule in enumerate(self._filter_rules):
            try:
                self._validate_filter_rule(rule)
            except Exception as e:
                invalid_rules += 1
                health["checks"].append(f"Invalid filter rule {i}: {e}")

        if invalid_rules > 0:
            health["status"] = "unhealthy"

        return health

    async def cleanup(self) -> None:
        """Clean up plugin resources."""
        self._filter_rules.clear()
        self._reset_statistics()
        self._initialized = False

    def _evaluate_record(
        self,
        record: dict[str, Any],
        filter_rules: list[dict[str, Any]],
        logic_operator: str,
    ) -> bool:
        """Evaluate if a record passes the filter rules."""
        if not filter_rules:
            return True

        results = []
        for rule in filter_rules:
            try:
                result = self._evaluate_filter_rule(record, rule)
                results.append(result)
            except Exception as e:
                if self._fail_on_missing_field:
                    msg = f"Filter evaluation failed: {e}"
                    raise PluginError(
                        msg,
                        plugin_id=self.metadata.id,
                        error_code="FILTER_EVALUATION_FAILED",
                        cause=e,
                    )
                # If not failing on missing fields, treat as False
                results.append(False)

        # Apply logic operator
        if logic_operator == "AND":
            return all(results)
        if logic_operator == "OR":
            return any(results)
        msg = f"Invalid logic operator: {logic_operator}"
        raise PluginError(
            msg,
            plugin_id=self.metadata.id,
            error_code="INVALID_LOGIC_OPERATOR",
        )

    def _evaluate_filter_rule(
        self, record: dict[str, Any], rule: dict[str, Any]
    ) -> bool:
        """Evaluate a single filter rule against a record."""
        field = rule["field"]
        operator = rule["operator"]
        expected_value = rule.get("value")
        case_sensitive = rule.get("case_sensitive", True)

        # Get field value from record
        if field not in record:
            if self._fail_on_missing_field:
                msg = f"Field '{field}' not found in record"
                raise ValueError(msg)
            return False

        actual_value = record[field]

        # Handle null checks first
        if operator == "is_null":
            return actual_value is None
        if operator == "is_not_null":
            return actual_value is not None

        # For other operators, if actual value is None, return False
        if actual_value is None:
            return False

        # Get comparison function
        comparison_func = self._get_comparison_function(operator, case_sensitive)

        try:
            return comparison_func(actual_value, expected_value)
        except Exception as e:
            msg = f"Filter comparison failed: {e}"
            raise ValueError(msg)

    def _get_comparison_function(
        self, operator: str, case_sensitive: bool
    ) -> Callable[[Any, Any], bool]:
        """Get the appropriate comparison function for an operator."""

        def prepare_string_values(actual, expected):
            """Prepare string values for comparison based on case sensitivity."""
            if not case_sensitive:
                if isinstance(actual, str):
                    actual = actual.lower()
                if isinstance(expected, str):
                    expected = expected.lower()
            return actual, expected

        def equals(actual, expected):
            actual, expected = prepare_string_values(actual, expected)
            return actual == expected

        def not_equals(actual, expected):
            actual, expected = prepare_string_values(actual, expected)
            return actual != expected

        def contains(actual, expected):
            actual, expected = prepare_string_values(actual, expected)
            return str(expected) in str(actual)

        def not_contains(actual, expected):
            actual, expected = prepare_string_values(actual, expected)
            return str(expected) not in str(actual)

        def starts_with(actual, expected):
            actual, expected = prepare_string_values(actual, expected)
            return str(actual).startswith(str(expected))

        def ends_with(actual, expected):
            actual, expected = prepare_string_values(actual, expected)
            return str(actual).endswith(str(expected))

        def regex_match(actual, expected):
            flags = 0 if case_sensitive else re.IGNORECASE
            pattern = re.compile(str(expected), flags)
            return bool(pattern.search(str(actual)))

        def greater_than(actual, expected):
            return self._convert_for_comparison(actual) > self._convert_for_comparison(
                expected
            )

        def less_than(actual, expected):
            return self._convert_for_comparison(actual) < self._convert_for_comparison(
                expected
            )

        def between(actual, expected):
            if not isinstance(expected, list | tuple) or len(expected) != 2:
                msg = "'between' operator requires a list/tuple of 2 values"
                raise ValueError(msg)
            min_val, max_val = expected
            actual_val = self._convert_for_comparison(actual)
            min_val = self._convert_for_comparison(min_val)
            max_val = self._convert_for_comparison(max_val)
            return min_val <= actual_val <= max_val

        def in_values(actual, expected):
            if not isinstance(expected, list | tuple):
                msg = "'in' operator requires a list/tuple of values"
                raise ValueError(msg)
            if not case_sensitive and isinstance(actual, str):
                expected = [
                    str(v).lower() if isinstance(v, str) else v for v in expected
                ]
                actual = actual.lower()
            return actual in expected

        def not_in_values(actual, expected) -> bool:
            return not in_values(actual, expected)

        # Operator mapping
        operators = {
            "equals": equals,
            "not_equals": not_equals,
            "contains": contains,
            "not_contains": not_contains,
            "starts_with": starts_with,
            "ends_with": ends_with,
            "regex": regex_match,
            "greater_than": greater_than,
            "less_than": less_than,
            "between": between,
            "in": in_values,
            "not_in": not_in_values,
        }

        if operator not in operators:
            msg = f"Unsupported operator: {operator}"
            raise ValueError(msg)

        return operators[operator]

    def _convert_for_comparison(self, value: Any) -> Any:
        """Convert value for numeric/date comparisons."""
        if isinstance(value, str):
            # Try to convert to number
            try:
                if "." in value:
                    return float(value)
                return int(value)
            except ValueError:
                # Try to parse as date
                try:
                    return datetime.fromisoformat(value.replace("Z", "+00:00"))
                except ValueError:
                    return value
        return value

    def _validate_filter_rule(self, rule: dict[str, Any]) -> None:
        """Validate a single filter rule."""
        required_fields = ["field", "operator"]
        for field in required_fields:
            if field not in rule:
                msg = f"Missing required field: {field}"
                raise ValueError(msg)

        operator = rule["operator"]
        value = rule.get("value")

        # Operators that require a value
        operators_requiring_value = {
            "equals",
            "not_equals",
            "contains",
            "not_contains",
            "starts_with",
            "ends_with",
            "regex",
            "greater_than",
            "less_than",
            "between",
            "in",
            "not_in",
        }

        if operator in operators_requiring_value and value is None:
            msg = f"Operator '{operator}' requires a value"
            raise ValueError(msg)

        # Special validation for specific operators
        if operator == "between":
            if not isinstance(value, list | tuple) or len(value) != 2:
                msg = "'between' operator requires a list/tuple of 2 values"
                raise ValueError(msg)

        if operator in {"in", "not_in"} and not isinstance(value, list | tuple):
            msg = f"'{operator}' operator requires a list/tuple of values"
            raise ValueError(
                msg
            )

    def _reset_statistics(self) -> None:
        """Reset filtering statistics."""
        self._statistics = {
            "total_records": 0,
            "passed_records": 0,
            "filtered_records": 0,
            "filter_rate": 0.0,
        }


# Entry point for plugin discovery
plugin_class = DataFilterTransformerPlugin
