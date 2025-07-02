"""CSV File Loader Plugin - Real Data Processing Implementation.

This plugin demonstrates a working loader that writes data to CSV files
with configurable formats, encoding, and output options.
"""

import csv
from datetime import datetime
from pathlib import Path
from typing import Any

from flext_plugin.base import BaseLoaderPlugin, PluginMetadata
from flext_plugin.types import PluginError, PluginType


class CSVLoaderPlugin(BaseLoaderPlugin):
    """CSV file loader plugin with real data processing capabilities.

    This plugin can load data to CSV files with:
    - Configurable output paths and filenames
    - Custom delimiters and encoding
    - Header row management
    - Data type formatting
    - File append or overwrite modes
    - Error handling and validation
    """

    METADATA = PluginMetadata(
        id="csv-loader",
        name="CSV File Loader",
        version="1.0.0",
        description="Load data to CSV files with configurable format and output options",
        plugin_type=PluginType.LOADER,
        author="FLEXT Team",
        license="MIT",
        entry_point="csv_loader_plugin.CSVLoaderPlugin",
        capabilities=[
            "file_loading",
            "csv_formatting",
            "custom_delimiters",
            "append_mode",
            "data_validation"
        ],
        configuration_schema={
            "type": "object",
            "properties": {
                "output_path": {
                    "type": "string",
                    "description": "Output file path for CSV"
                },
                "output_directory": {
                    "type": "string",
                    "description": "Output directory (alternative to output_path)"
                },
                "filename_template": {
                    "type": "string",
                    "default": "output_{timestamp}.csv",
                    "description": "Filename template with placeholders"
                },
                "delimiter": {
                    "type": "string",
                    "default": ",",
                    "description": "CSV delimiter character"
                },
                "encoding": {
                    "type": "string",
                    "default": "utf-8",
                    "description": "File encoding"
                },
                "include_header": {
                    "type": "boolean",
                    "default": True,
                    "description": "Include header row in CSV"
                },
                "append_mode": {
                    "type": "boolean",
                    "default": False,
                    "description": "Append to existing file instead of overwriting"
                },
                "create_directories": {
                    "type": "boolean",
                    "default": True,
                    "description": "Create output directories if they don't exist"
                },
                "date_format": {
                    "type": "string",
                    "default": "%Y-%m-%d %H:%M:%S",
                    "description": "Date format for timestamp formatting"
                },
                "null_value": {
                    "type": "string",
                    "default": "",
                    "description": "String representation for null values"
                },
                "quoting": {
                    "type": "string",
                    "enum": ["minimal", "all", "non_numeric", "none"],
                    "default": "minimal",
                    "description": "CSV quoting behavior"
                }
            },
            "required": []
        },
        default_configuration={
            "delimiter": ",",
            "encoding": "utf-8",
            "include_header": True,
            "append_mode": False,
            "create_directories": True,
            "filename_template": "output_{timestamp}.csv",
            "date_format": "%Y-%m-%d %H:%M:%S",
            "null_value": "",
            "quoting": "minimal"
        }
    )

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize CSV loader plugin."""
        super().__init__(config)
        self._output_path: str | None = None
        self._output_directory: str | None = None
        self._filename_template: str = "output_{timestamp}.csv"
        self._delimiter: str = ","
        self._encoding: str = "utf-8"
        self._include_header: bool = True
        self._append_mode: bool = False
        self._create_directories: bool = True
        self._date_format: str = "%Y-%m-%d %H:%M:%S"
        self._null_value: str = ""
        self._quoting: str = "minimal"
        self._load_statistics: dict[str, Any] = {}

    async def initialize(self) -> None:
        """Initialize plugin with configuration."""
        self._output_path = self._config.get("output_path")
        self._output_directory = self._config.get("output_directory")
        self._filename_template = self._config.get("filename_template", "output_{timestamp}.csv")
        self._delimiter = self._config.get("delimiter", ",")
        self._encoding = self._config.get("encoding", "utf-8")
        self._include_header = self._config.get("include_header", True)
        self._append_mode = self._config.get("append_mode", False)
        self._create_directories = self._config.get("create_directories", True)
        self._date_format = self._config.get("date_format", "%Y-%m-%d %H:%M:%S")
        self._null_value = self._config.get("null_value", "")
        self._quoting = self._config.get("quoting", "minimal")

        # Validate configuration
        if not self._output_path and not self._output_directory:
            raise PluginError(
                "Either output_path or output_directory must be specified",
                plugin_id=self.metadata.id,
                error_code="MISSING_CONFIG"
            )

        # Validate quoting parameter
        valid_quoting = {"minimal", "all", "non_numeric", "none"}
        if self._quoting not in valid_quoting:
            raise PluginError(
                f"Invalid quoting option: {self._quoting}",
                plugin_id=self.metadata.id,
                error_code="INVALID_CONFIG"
            )

        self._reset_statistics()
        self._initialized = True

    async def load(self, data: Any, destination_config: dict[str, Any]) -> dict[str, Any]:
        """Load data to CSV file.

        Args:
        ----
            data: Data to load (list of records or plugin result)
            destination_config: Additional destination configuration

        Returns:
        -------
            Dictionary containing load results and metrics

        """
        if not self._initialized:
            raise PluginError(
                "Plugin not initialized",
                plugin_id=self.metadata.id,
                error_code="NOT_INITIALIZED"
            )

        # Override config with destination_config
        output_path = destination_config.get("output_path", self._output_path)
        output_directory = destination_config.get("output_directory", self._output_directory)
        filename_template = destination_config.get("filename_template", self._filename_template)
        append_mode = destination_config.get("append_mode", self._append_mode)

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

            if not records:
                return {
                    "success": True,
                    "message": "No data to load",
                    "records_loaded": 0,
                    "output_path": None
                }

            # Determine final output path
            final_output_path = self._determine_output_path(
                output_path, output_directory, filename_template
            )

            # Create output directory if needed
            if self._create_directories:
                output_dir = Path(final_output_path).parent
                output_dir.mkdir(parents=True, exist_ok=True)

            # Load data to CSV
            loaded_records = await self._write_csv_file(
                records, final_output_path, append_mode
            )

            self._load_statistics["records_loaded"] = loaded_records
            self._load_statistics["output_path"] = str(final_output_path)
            self._load_statistics["file_size_bytes"] = Path(final_output_path).stat().st_size

            # Build result
            result = {
                "success": True,
                "records_loaded": loaded_records,
                "output_path": str(final_output_path),
                "file_size_bytes": self._load_statistics["file_size_bytes"],
                "load_timestamp": datetime.now().isoformat(),
                "input_metadata": input_metadata,
                "load_statistics": self._load_statistics.copy()
            }

            return result

        except Exception as e:
            raise PluginError(
                f"Failed to load data to CSV: {e}",
                plugin_id=self.metadata.id,
                error_code="LOAD_FAILED",
                cause=e
            )

    async def health_check(self) -> dict[str, Any]:
        """Perform health check."""
        health = {
            "status": "healthy",
            "plugin_id": self.metadata.id,
            "initialized": self._initialized,
            "output_writable": False,
            "checks": []
        }

        # Check output path configuration
        output_path = self._output_path or self._output_directory
        if not output_path:
            health["checks"].append("No output path configured")
            health["status"] = "degraded"
        else:
            health["checks"].append(f"Output path configured: {output_path}")

        # Test write permissions
        if output_path:
            try:
                test_path = self._determine_output_path(
                    self._output_path, self._output_directory, "test.csv"
                )
                test_dir = Path(test_path).parent

                # Check if directory exists or can be created
                if test_dir.exists() or self._create_directories:
                    if self._create_directories:
                        test_dir.mkdir(parents=True, exist_ok=True)

                    # Test write permission by creating a temporary file
                    test_file = test_dir / ".write_test"
                    test_file.touch()
                    test_file.unlink()

                    health["output_writable"] = True
                    health["checks"].append("Output directory is writable")
                else:
                    health["checks"].append("Output directory does not exist and create_directories is False")
                    health["status"] = "degraded"

            except Exception as e:
                health["checks"].append(f"Output directory not writable: {e}")
                health["status"] = "unhealthy"

        return health

    async def cleanup(self) -> None:
        """Clean up plugin resources."""
        self._reset_statistics()
        self._initialized = False

    def _determine_output_path(
        self,
        output_path: str | None,
        output_directory: str | None,
        filename_template: str
    ) -> Path:
        """Determine the final output file path."""
        if output_path:
            return Path(output_path)

        if output_directory:
            # Generate filename from template
            filename = self._format_filename_template(filename_template)
            return Path(output_directory) / filename

        raise PluginError(
            "No output path could be determined",
            plugin_id=self.metadata.id,
            error_code="INVALID_OUTPUT_PATH"
        )

    def _format_filename_template(self, template: str) -> str:
        """Format filename template with placeholders."""
        now = datetime.now()

        # Available placeholders
        placeholders = {
            "timestamp": now.strftime("%Y%m%d_%H%M%S"),
            "date": now.strftime("%Y%m%d"),
            "time": now.strftime("%H%M%S"),
            "year": now.strftime("%Y"),
            "month": now.strftime("%m"),
            "day": now.strftime("%d"),
            "hour": now.strftime("%H"),
            "minute": now.strftime("%M"),
            "second": now.strftime("%S")
        }

        # Replace placeholders
        formatted = template
        for placeholder, value in placeholders.items():
            formatted = formatted.replace(f"{{{placeholder}}}", value)

        return formatted

    async def _write_csv_file(
        self,
        records: list[dict[str, Any]],
        output_path: Path,
        append_mode: bool
    ) -> int:
        """Write records to CSV file."""
        if not records:
            return 0

        # Get CSV quoting constant
        quoting_map = {
            "minimal": csv.QUOTE_MINIMAL,
            "all": csv.QUOTE_ALL,
            "non_numeric": csv.QUOTE_NONNUMERIC,
            "none": csv.QUOTE_NONE
        }
        quoting = quoting_map.get(self._quoting, csv.QUOTE_MINIMAL)

        # Determine if file exists for append mode
        file_exists = output_path.exists()
        write_header = self._include_header and (not append_mode or not file_exists)

        # Get field names from first record
        fieldnames = list(records[0].keys()) if records else []

        # Open file and write data
        mode = 'a' if append_mode else 'w'
        with open(output_path, mode, newline='', encoding=self._encoding) as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=fieldnames,
                delimiter=self._delimiter,
                quoting=quoting
            )

            # Write header if needed
            if write_header and fieldnames:
                writer.writeheader()

            # Write records
            records_written = 0
            for record in records:
                # Format record values
                formatted_record = self._format_record(record)
                writer.writerow(formatted_record)
                records_written += 1

            return records_written

    def _format_record(self, record: dict[str, Any]) -> dict[str, str]:
        """Format record values for CSV output."""
        formatted = {}

        for field, value in record.items():
            if value is None:
                formatted[field] = self._null_value
            elif isinstance(value, datetime):
                formatted[field] = value.strftime(self._date_format)
            elif isinstance(value, (list, dict)):
                # Convert complex types to JSON string
                import json
                formatted[field] = json.dumps(value)
            else:
                formatted[field] = str(value)

        return formatted

    def _reset_statistics(self) -> None:
        """Reset load statistics."""
        self._load_statistics = {
            "records_loaded": 0,
            "output_path": None,
            "file_size_bytes": 0
        }


# Entry point for plugin discovery
plugin_class = CSVLoaderPlugin
