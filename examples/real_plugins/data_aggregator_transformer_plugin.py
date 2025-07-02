"""Data Aggregator Transformer Plugin - Real Data Processing Implementation.

This plugin demonstrates a working transformer that aggregates data using
various aggregation functions like sum, count, average, min, max, and
custom aggregations with grouping capabilities.
"""

from collections import defaultdict
from datetime import datetime
from typing import Any

from flext_plugin.base import BaseTransformerPlugin, PluginMetadata
from flext_plugin.types import PluginError, PluginType


class DataAggregatorTransformerPlugin(BaseTransformerPlugin):
    """Data aggregator transformer plugin with real data processing capabilities.

    This plugin can aggregate data with:
    - Multiple aggregation functions (sum, count, avg, min, max, etc.)
    - Grouping by one or multiple fields
    - Custom aggregation expressions
    - Statistical calculations
    - Data type-aware aggregations
    """

    METADATA = PluginMetadata(
        id="data-aggregator-transformer",
        name="Data Aggregator Transformer",
        version="1.0.0",
        description="Aggregate data using various functions with grouping capabilities",
        plugin_type=PluginType.TRANSFORMER,
        author="FLEXT Team",
        license="MIT",
        entry_point="data_aggregator_transformer_plugin.DataAggregatorTransformerPlugin",
        capabilities=[
            "data_aggregation",
            "grouping",
            "statistical_functions",
            "custom_expressions",
            "type_aware_aggregation"
        ],
        configuration_schema={
            "type": "object",
            "properties": {
                "group_by": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Fields to group by"
                },
                "aggregations": {
                    "type": "array",
                    "description": "List of aggregation configurations",
                    "items": {
                        "type": "object",
                        "properties": {
                            "field": {
                                "type": "string",
                                "description": "Field to aggregate"
                            },
                            "function": {
                                "type": "string",
                                "enum": ["sum", "count", "avg", "min", "max", "median",
                                        "std", "var", "first", "last", "concat", "unique_count"],
                                "description": "Aggregation function"
                            },
                            "alias": {
                                "type": "string",
                                "description": "Alias for the aggregated field"
                            },
                            "filter": {
                                "type": "object",
                                "description": "Optional filter to apply before aggregation",
                                "properties": {
                                    "operator": {"type": "string"},
                                    "value": {}
                                }
                            }
                        },
                        "required": ["field", "function"]
                    }
                },
                "include_group_stats": {
                    "type": "boolean",
                    "default": True,
                    "description": "Include group statistics in output"
                },
                "sort_by": {
                    "type": "object",
                    "description": "Sort aggregated results",
                    "properties": {
                        "field": {"type": "string"},
                        "direction": {"type": "string", "enum": ["asc", "desc"]}
                    }
                }
            },
            "required": ["aggregations"]
        },
        default_configuration={
            "group_by": [],
            "include_group_stats": True
        }
    )

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize data aggregator transformer plugin."""
        super().__init__(config)
        self._group_by: list[str] = []
        self._aggregations: list[dict[str, Any]] = []
        self._include_group_stats: bool = True
        self._sort_by: dict[str, str] = {}
        self._statistics: dict[str, Any] = {}

    async def initialize(self) -> None:
        """Initialize plugin with aggregation configuration."""
        self._group_by = self._config.get("group_by", [])
        self._aggregations = self._config.get("aggregations", [])
        self._include_group_stats = self._config.get("include_group_stats", True)
        self._sort_by = self._config.get("sort_by", {})

        if not self._aggregations:
            raise PluginError(
                "At least one aggregation must be specified",
                plugin_id=self.metadata.id,
                error_code="MISSING_CONFIG"
            )

        # Validate aggregations
        for i, agg in enumerate(self._aggregations):
            if not all(key in agg for key in ["field", "function"]):
                raise PluginError(
                    f"Aggregation {i} missing required fields (field, function)",
                    plugin_id=self.metadata.id,
                    error_code="INVALID_AGGREGATION"
                )

            # Validate function
            valid_functions = {
                "sum", "count", "avg", "min", "max", "median",
                "std", "var", "first", "last", "concat", "unique_count"
            }
            if agg["function"] not in valid_functions:
                raise PluginError(
                    f"Invalid aggregation function '{agg['function']}' in aggregation {i}",
                    plugin_id=self.metadata.id,
                    error_code="INVALID_FUNCTION"
                )

        self._reset_statistics()
        self._initialized = True

    async def transform(self, data: Any, transform_config: dict[str, Any]) -> dict[str, Any]:
        """Transform data by applying aggregations.

        Args:
        ----
            data: Input data (list of records or single record)
            transform_config: Additional transformation configuration

        Returns:
        -------
            Dictionary containing aggregated data and metadata

        """
        if not self._initialized:
            raise PluginError(
                "Plugin not initialized",
                plugin_id=self.metadata.id,
                error_code="NOT_INITIALIZED"
            )

        # Override config with transform_config
        group_by = transform_config.get("group_by", self._group_by)
        aggregations = transform_config.get("aggregations", self._aggregations)
        sort_by = transform_config.get("sort_by", self._sort_by)

        try:
            # Reset statistics
            self._reset_statistics()

            # Handle different input data formats
            if isinstance(data, dict):
                if "data" in data:
                    records = data["data"]
                    input_metadata = data.get("metadata", {})
                else:
                    records = [data]
                    input_metadata = {}
            elif isinstance(data, list):
                records = data
                input_metadata = {}
            else:
                raise PluginError(
                    f"Unsupported input data type: {type(data)}",
                    plugin_id=self.metadata.id,
                    error_code="INVALID_INPUT_TYPE"
                )

            self._statistics["total_input_records"] = len(records)

            # Group records
            groups = self._group_records(records, group_by)
            self._statistics["groups_created"] = len(groups)

            # Apply aggregations to each group
            aggregated_results = []
            for group_key, group_records in groups.items():
                aggregated_record = {}

                # Add group by fields to result
                if group_by:
                    if len(group_by) == 1:
                        aggregated_record[group_by[0]] = group_key
                    else:
                        for i, field in enumerate(group_by):
                            aggregated_record[field] = group_key[i] if isinstance(group_key, tuple) else group_key

                # Apply each aggregation
                for agg_config in aggregations:
                    field = agg_config["field"]
                    function = agg_config["function"]
                    alias = agg_config.get("alias", f"{function}_{field}")
                    filter_config = agg_config.get("filter")

                    # Filter records if filter is specified
                    filtered_records = group_records
                    if filter_config:
                        filtered_records = self._filter_records(group_records, field, filter_config)

                    # Apply aggregation function
                    aggregated_value = self._apply_aggregation_function(
                        filtered_records, field, function
                    )
                    aggregated_record[alias] = aggregated_value

                # Add group statistics if enabled
                if self._include_group_stats:
                    aggregated_record["_group_size"] = len(group_records)
                    if group_by:
                        aggregated_record["_group_key"] = group_key

                aggregated_results.append(aggregated_record)

            # Sort results if specified
            if sort_by and "field" in sort_by:
                reverse = sort_by.get("direction", "asc") == "desc"
                aggregated_results.sort(
                    key=lambda x: x.get(sort_by["field"], 0),
                    reverse=reverse
                )

            self._statistics["total_output_records"] = len(aggregated_results)

            # Build result metadata
            output_metadata = {
                "transformation_timestamp": datetime.now().isoformat(),
                "transformer": self.metadata.name,
                "group_by_fields": group_by,
                "aggregations_applied": len(aggregations),
                "input_metadata": input_metadata,
                "aggregation_statistics": self._statistics.copy()
            }

            return {
                "data": aggregated_results,
                "metadata": output_metadata,
                "success": True
            }

        except Exception as e:
            raise PluginError(
                f"Failed to apply data aggregations: {e}",
                plugin_id=self.metadata.id,
                error_code="TRANSFORMATION_FAILED",
                cause=e
            )

    async def health_check(self) -> dict[str, Any]:
        """Perform health check."""
        health = {
            "status": "healthy",
            "plugin_id": self.metadata.id,
            "initialized": self._initialized,
            "group_by_fields": len(self._group_by),
            "aggregations_count": len(self._aggregations),
            "checks": []
        }

        # Check aggregations configuration
        if not self._aggregations:
            health["checks"].append("No aggregations configured")
            health["status"] = "degraded"
        else:
            health["checks"].append(f"Aggregations configured: {len(self._aggregations)}")

        # Validate each aggregation
        invalid_aggregations = 0
        for i, agg in enumerate(self._aggregations):
            try:
                self._validate_aggregation(agg)
            except Exception as e:
                invalid_aggregations += 1
                health["checks"].append(f"Invalid aggregation {i}: {e}")

        if invalid_aggregations > 0:
            health["status"] = "unhealthy"

        return health

    async def cleanup(self) -> None:
        """Clean up plugin resources."""
        self._group_by.clear()
        self._aggregations.clear()
        self._reset_statistics()
        self._initialized = False

    def _group_records(self, records: list[dict[str, Any]], group_by: list[str]) -> dict[Any, list[dict[str, Any]]]:
        """Group records by specified fields."""
        if not group_by:
            # No grouping, return all records in single group
            return {"_all": records}

        groups = defaultdict(list)

        for record in records:
            # Create group key
            if len(group_by) == 1:
                group_key = record.get(group_by[0])
            else:
                group_key = tuple(record.get(field) for field in group_by)

            groups[group_key].append(record)

        return dict(groups)

    def _filter_records(
        self,
        records: list[dict[str, Any]],
        field: str,
        filter_config: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Apply filter to records before aggregation."""
        operator = filter_config.get("operator", "equals")
        filter_value = filter_config.get("value")

        filtered = []
        for record in records:
            record_value = record.get(field)

            if self._evaluate_filter(record_value, operator, filter_value):
                filtered.append(record)

        return filtered

    def _evaluate_filter(self, actual_value: Any, operator: str, expected_value: Any) -> bool:
        """Evaluate filter condition."""
        if operator == "equals":
            return actual_value == expected_value
        elif operator == "not_equals":
            return actual_value != expected_value
        elif operator == "greater_than":
            return self._convert_for_comparison(actual_value) > self._convert_for_comparison(expected_value)
        elif operator == "less_than":
            return self._convert_for_comparison(actual_value) < self._convert_for_comparison(expected_value)
        elif operator == "is_null":
            return actual_value is None
        elif operator == "is_not_null":
            return actual_value is not None
        else:
            return True

    def _apply_aggregation_function(
        self,
        records: list[dict[str, Any]],
        field: str,
        function: str
    ) -> Any:
        """Apply aggregation function to field values."""
        if not records:
            return None

        # Get field values, excluding None values for most functions
        if function == "count":
            return len(records)

        values = [record.get(field) for record in records]

        # Filter None values for most functions (except count and first/last)
        if function not in ["first", "last", "concat"]:
            values = [v for v in values if v is not None]

        if not values and function not in ["count"]:
            return None

        # Apply aggregation function
        try:
            if function == "sum":
                return sum(self._convert_to_numeric(v) for v in values)

            elif function == "avg":
                numeric_values = [self._convert_to_numeric(v) for v in values]
                return sum(numeric_values) / len(numeric_values) if numeric_values else None

            elif function == "min":
                return min(values)

            elif function == "max":
                return max(values)

            elif function == "median":
                sorted_values = sorted(self._convert_to_numeric(v) for v in values)
                n = len(sorted_values)
                if n == 0:
                    return None
                elif n % 2 == 0:
                    return (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
                else:
                    return sorted_values[n//2]

            elif function == "std":
                numeric_values = [self._convert_to_numeric(v) for v in values]
                if len(numeric_values) < 2:
                    return None
                mean = sum(numeric_values) / len(numeric_values)
                variance = sum((x - mean) ** 2 for x in numeric_values) / len(numeric_values)
                return variance ** 0.5

            elif function == "var":
                numeric_values = [self._convert_to_numeric(v) for v in values]
                if len(numeric_values) < 2:
                    return None
                mean = sum(numeric_values) / len(numeric_values)
                return sum((x - mean) ** 2 for x in numeric_values) / len(numeric_values)

            elif function == "first":
                return values[0] if values else None

            elif function == "last":
                return values[-1] if values else None

            elif function == "concat":
                return ", ".join(str(v) for v in values if v is not None)

            elif function == "unique_count":
                return len(set(v for v in values if v is not None))

            else:
                raise ValueError(f"Unknown aggregation function: {function}")

        except Exception as e:
            raise ValueError(f"Aggregation function '{function}' failed: {e}")

    def _convert_to_numeric(self, value: Any) -> float:
        """Convert value to numeric for mathematical operations."""
        if value is None:
            return 0.0

        if isinstance(value, (int, float)):
            return float(value)

        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                return 0.0

        return 0.0

    def _convert_for_comparison(self, value: Any) -> Any:
        """Convert value for comparison operations."""
        if isinstance(value, str):
            try:
                if '.' in value:
                    return float(value)
                else:
                    return int(value)
            except ValueError:
                return value
        return value

    def _validate_aggregation(self, agg: dict[str, Any]) -> None:
        """Validate a single aggregation configuration."""
        required_fields = ["field", "function"]
        for field in required_fields:
            if field not in agg:
                raise ValueError(f"Missing required field: {field}")

        function = agg["function"]
        valid_functions = {
            "sum", "count", "avg", "min", "max", "median",
            "std", "var", "first", "last", "concat", "unique_count"
        }

        if function not in valid_functions:
            raise ValueError(f"Invalid aggregation function: {function}")

    def _reset_statistics(self) -> None:
        """Reset aggregation statistics."""
        self._statistics = {
            "total_input_records": 0,
            "total_output_records": 0,
            "groups_created": 0
        }


# Entry point for plugin discovery
plugin_class = DataAggregatorTransformerPlugin
