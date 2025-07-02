"""CSV File Extractor Plugin - Real Data Processing Implementation.

This plugin demonstrates a working extractor that reads CSV files and outputs
structured data for pipeline processing. It includes schema inference,
data validation, and error handling.
"""

import csv
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from flext_plugin.base import BaseExtractorPlugin, PluginMetadata
from flext_plugin.types import PluginError, PluginType


class CSVExtractorPlugin(BaseExtractorPlugin):
    """CSV file extractor plugin with real data processing capabilities.

    This plugin can extract data from CSV files with:
    - Automatic schema inference
    - Data type conversion
    - Error handling and validation
    - Streaming data output for large files
    - Configurable delimiters and encoding
    """

    METADATA = PluginMetadata(
        id="csv-extractor",
        name="CSV File Extractor",
        version="1.0.0",
        description="Extract data from CSV files with schema inference and validation",
        plugin_type=PluginType.EXTRACTOR,
        author="FLEXT Team",
        license="MIT",
        entry_point="csv_extractor_plugin.CSVExtractorPlugin",
        capabilities=[
            "file_extraction",
            "schema_inference",
            "data_validation",
            "streaming_output",
            "configurable_parsing",
        ],
        configuration_schema={
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the CSV file to extract",
                },
                "delimiter": {
                    "type": "string",
                    "default": ",",
                    "description": "CSV delimiter character",
                },
                "encoding": {
                    "type": "string",
                    "default": "utf-8",
                    "description": "File encoding",
                },
                "has_header": {
                    "type": "boolean",
                    "default": True,
                    "description": "Whether CSV has header row",
                },
                "skip_rows": {
                    "type": "integer",
                    "default": 0,
                    "description": "Number of rows to skip at start",
                },
                "max_rows": {
                    "type": "integer",
                    "description": "Maximum number of rows to extract (optional)",
                },
                "infer_schema": {
                    "type": "boolean",
                    "default": True,
                    "description": "Automatically infer data types",
                },
            },
            "required": ["file_path"],
        },
        default_configuration={
            "delimiter": ",",
            "encoding": "utf-8",
            "has_header": True,
            "skip_rows": 0,
            "infer_schema": True,
        },
    )

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize CSV extractor plugin."""
        super().__init__(config)
        self._file_path: str | None = None
        self._delimiter: str = ","
        self._encoding: str = "utf-8"
        self._has_header: bool = True
        self._skip_rows: int = 0
        self._max_rows: int | None = None
        self._infer_schema: bool = True
        self._schema: dict[str, str] = {}
        self._total_rows: int = 0

    async def initialize(self) -> None:
        """Initialize plugin with configuration."""
        self._file_path = self._config.get("file_path")
        self._delimiter = self._config.get("delimiter", ",")
        self._encoding = self._config.get("encoding", "utf-8")
        self._has_header = self._config.get("has_header", True)
        self._skip_rows = self._config.get("skip_rows", 0)
        self._max_rows = self._config.get("max_rows")
        self._infer_schema = self._config.get("infer_schema", True)

        if not self._file_path:
            raise PluginError(
                "file_path configuration is required",
                plugin_id=self.metadata.id,
                error_code="MISSING_CONFIG",
            )

        # Validate file exists and is readable
        file_path = Path(self._file_path)
        if not file_path.exists():
            raise PluginError(
                f"File not found: {self._file_path}",
                plugin_id=self.metadata.id,
                error_code="FILE_NOT_FOUND",
            )

        if not file_path.is_file():
            raise PluginError(
                f"Path is not a file: {self._file_path}",
                plugin_id=self.metadata.id,
                error_code="INVALID_FILE",
            )

        # Try to open file to validate access
        try:
            with open(file_path, encoding=self._encoding) as f:
                f.read(1)  # Read one character to test access
        except (OSError, UnicodeDecodeError) as e:
            raise PluginError(
                f"Cannot read file: {e}",
                plugin_id=self.metadata.id,
                error_code="FILE_ACCESS_ERROR",
                cause=e,
            )

        # Infer schema if enabled
        if self._infer_schema:
            await self._infer_file_schema()

        self._update_lifecycle_state(self.metadata.METADATA.lifecycle_state)
        self._initialized = True

    async def extract(self, source_config: dict[str, Any]) -> dict[str, Any]:
        """Extract data from CSV file.

        Args:
        ----
            source_config: Additional source configuration (can override instance config)

        Returns:
        -------
            Dictionary containing extracted data and metadata

        """
        if not self._initialized:
            raise PluginError(
                "Plugin not initialized",
                plugin_id=self.metadata.id,
                error_code="NOT_INITIALIZED",
            )

        # Override config with source_config if provided
        file_path = source_config.get("file_path", self._file_path)
        max_rows = source_config.get("max_rows", self._max_rows)

        try:
            # Extract data
            records = []
            metadata = {
                "file_path": file_path,
                "schema": self._schema.copy(),
                "extraction_timestamp": datetime.now(UTC).isoformat(),
                "total_rows_extracted": 0,
                "has_header": self._has_header,
                "delimiter": self._delimiter,
                "encoding": self._encoding,
            }

            with open(file_path, encoding=self._encoding, newline="") as csvfile:
                reader = (
                    csv.DictReader(csvfile, delimiter=self._delimiter)
                    if self._has_header
                    else csv.reader(csvfile, delimiter=self._delimiter)
                )

                # Skip initial rows if configured
                for _ in range(self._skip_rows):
                    try:
                        next(reader)
                    except StopIteration:
                        break

                row_count = 0
                for row in reader:
                    # Apply max rows limit
                    if max_rows and row_count >= max_rows:
                        break

                    # Process row data
                    if self._has_header:
                        processed_row = self._process_row_with_schema(row)
                    else:
                        processed_row = self._process_row_without_header(row, row_count)

                    records.append(processed_row)
                    row_count += 1

                metadata["total_rows_extracted"] = row_count

            result = {
                "data": records,
                "metadata": metadata,
                "schema": self._schema,
                "success": True,
            }

            return result

        except Exception as e:
            raise PluginError(
                f"Failed to extract data from CSV: {e}",
                plugin_id=self.metadata.id,
                error_code="EXTRACTION_FAILED",
                cause=e,
            )

    async def extract_stream(
        self, source_config: dict[str, Any]
    ) -> Iterator[dict[str, Any]]:
        """Extract data as a stream for large files.

        Args:
        ----
            source_config: Source configuration

        Yields:
        ------
            Individual records as dictionaries

        """
        if not self._initialized:
            raise PluginError(
                "Plugin not initialized",
                plugin_id=self.metadata.id,
                error_code="NOT_INITIALIZED",
            )

        file_path = source_config.get("file_path", self._file_path)
        max_rows = source_config.get("max_rows", self._max_rows)

        try:
            with open(file_path, encoding=self._encoding, newline="") as csvfile:
                reader = (
                    csv.DictReader(csvfile, delimiter=self._delimiter)
                    if self._has_header
                    else csv.reader(csvfile, delimiter=self._delimiter)
                )

                # Skip initial rows
                for _ in range(self._skip_rows):
                    try:
                        next(reader)
                    except StopIteration:
                        break

                row_count = 0
                for row in reader:
                    if max_rows and row_count >= max_rows:
                        break

                    if self._has_header:
                        processed_row = self._process_row_with_schema(row)
                    else:
                        processed_row = self._process_row_without_header(row, row_count)

                    yield processed_row
                    row_count += 1

        except Exception as e:
            raise PluginError(
                f"Failed to stream data from CSV: {e}",
                plugin_id=self.metadata.id,
                error_code="STREAM_FAILED",
                cause=e,
            )

    async def health_check(self) -> dict[str, Any]:
        """Perform health check."""
        health = {
            "status": "healthy",
            "plugin_id": self.metadata.id,
            "initialized": self._initialized,
            "file_accessible": False,
            "schema_inferred": bool(self._schema),
            "checks": [],
        }

        # Check file accessibility
        if self._file_path:
            try:
                file_path = Path(self._file_path)
                if file_path.exists() and file_path.is_file():
                    health["file_accessible"] = True
                    health["checks"].append("File exists and is accessible")
                else:
                    health["checks"].append("File not found or inaccessible")
                    health["status"] = "degraded"
            except Exception as e:
                health["checks"].append(f"File check failed: {e}")
                health["status"] = "unhealthy"

        # Check configuration
        if not self._file_path:
            health["checks"].append("Missing file_path configuration")
            health["status"] = "unhealthy"

        return health

    async def cleanup(self) -> None:
        """Clean up plugin resources."""
        self._schema.clear()
        self._initialized = False

    async def _infer_file_schema(self) -> None:
        """Infer schema from CSV file by sampling data."""
        if not self._file_path:
            return

        try:
            with open(self._file_path, encoding=self._encoding, newline="") as csvfile:
                reader = (
                    csv.DictReader(csvfile, delimiter=self._delimiter)
                    if self._has_header
                    else csv.reader(csvfile, delimiter=self._delimiter)
                )

                # Skip initial rows
                for _ in range(self._skip_rows):
                    try:
                        next(reader)
                    except StopIteration:
                        break

                # Sample first few rows to infer types
                sample_rows = []
                for i, row in enumerate(reader):
                    sample_rows.append(row)
                    if i >= 10:  # Sample 10 rows max
                        break

                if self._has_header and sample_rows:
                    # Get field names from first row
                    field_names = list(sample_rows[0].keys())

                    # Infer types for each field
                    for field_name in field_names:
                        self._schema[field_name] = self._infer_field_type(
                            [row.get(field_name, "") for row in sample_rows]
                        )
                elif sample_rows:
                    # No header, create generic field names
                    first_row = sample_rows[0]
                    for i in range(len(first_row)):
                        field_name = f"column_{i}"
                        self._schema[field_name] = self._infer_field_type(
                            [row[i] if i < len(row) else "" for row in sample_rows]
                        )

        except Exception:
            # Schema inference is optional, don't fail initialization
            self._schema = {}

    def _infer_field_type(self, values: list[str]) -> str:
        """Infer data type from sample values."""
        non_empty_values = [v.strip() for v in values if v.strip()]

        if not non_empty_values:
            return "string"

        # Check if all values are integers
        try:
            for value in non_empty_values:
                int(value)
            return "integer"
        except ValueError:
            pass

        # Check if all values are floats
        try:
            for value in non_empty_values:
                float(value)
            return "number"
        except ValueError:
            pass

        # Check if all values are booleans
        boolean_values = {"true", "false", "1", "0", "yes", "no", "y", "n"}
        if all(v.lower() in boolean_values for v in non_empty_values):
            return "boolean"

        # Check if values look like dates (basic check)
        if any(self._looks_like_date(v) for v in non_empty_values[:3]):
            return "date"

        return "string"

    def _looks_like_date(self, value: str) -> bool:
        """Basic check if string looks like a date."""
        date_indicators = ["-", "/", ":", "T", "Z"]
        return (
            any(indicator in value for indicator in date_indicators) and len(value) >= 8
        )

    def _process_row_with_schema(self, row: dict[str, str]) -> dict[str, Any]:
        """Process row data using inferred schema."""
        processed = {}

        for field_name, value in row.items():
            field_type = self._schema.get(field_name, "string")
            processed[field_name] = self._convert_value(value, field_type)

        return processed

    def _process_row_without_header(
        self, row: list[str], row_index: int
    ) -> dict[str, Any]:
        """Process row data without header."""
        processed = {}

        for i, value in enumerate(row):
            field_name = f"column_{i}"
            field_type = self._schema.get(field_name, "string")
            processed[field_name] = self._convert_value(value, field_type)

        processed["_row_index"] = row_index
        return processed

    def _convert_value(self, value: str, field_type: str) -> Any:
        """Convert string value to appropriate type."""
        if not value.strip():
            return None

        try:
            if field_type == "integer":
                return int(value)
            elif field_type == "number":
                return float(value)
            elif field_type == "boolean":
                return value.lower() in {"true", "1", "yes", "y"}
            elif field_type == "date":
                # Basic date parsing - could be enhanced
                return value  # Keep as string for now
            else:
                return value.strip()
        except (ValueError, TypeError):
            # If conversion fails, return as string
            return value.strip()


# Entry point for plugin discovery
plugin_class = CSVExtractorPlugin
