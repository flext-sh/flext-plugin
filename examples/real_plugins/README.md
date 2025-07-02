# Real Plugin Examples

This directory contains working implementations of FLEXT plugins that demonstrate real data processing capabilities.

## Available Plugins

### Extractors
- **CSV Extractor** (`csv_extractor_plugin.py`): Extracts data from CSV files with schema inference
- **PostgreSQL Extractor** (`postgres_extractor_plugin.py`): Extracts data from PostgreSQL databases

### Transformers
- **Data Filter** (`data_filter_transformer_plugin.py`): Filters data based on configurable conditions
- **Data Aggregator** (`data_aggregator_transformer_plugin.py`): Aggregates data with grouping functions

### Loaders
- **CSV Loader** (`csv_loader_plugin.py`): Loads data to CSV files with configurable format
- **PostgreSQL Loader** (`postgres_loader_plugin.py`): Loads data to PostgreSQL databases

## Key Features

### Real Data Processing
- Actual data extraction, transformation, and loading
- No simulation or mocked operations
- Production-ready implementations

### Plugin Architecture Integration
- Built on FLEXT plugin base classes
- Full metadata and configuration support
- Health checks and error handling
- Resource monitoring and cleanup

### Data Flow Management
- Structured data packets between steps
- Execution context and lineage tracking
- Validation and quality metrics
- Error propagation and handling

## Example Usage

```python
from flext_plugin.pipeline_executor import Pipeline, PipelineStep
from flext_plugin.types import PluginType

# Create a simple ETL pipeline
pipeline = Pipeline(
    pipeline_id="example_etl",
    name="CSV Processing Pipeline",
    steps=[
        PipelineStep(
            step_id="extract",
            plugin_id="csv-extractor",
            step_type=PluginType.EXTRACTOR,
            configuration={"file_path": "/path/to/input.csv"}
        ),
        PipelineStep(
            step_id="filter",
            plugin_id="data-filter",
            step_type=PluginType.TRANSFORMER,
            configuration={
                "filter_rules": [
                    {"field": "status", "operator": "equals", "value": "active"}
                ]
            }
        ),
        PipelineStep(
            step_id="load",
            plugin_id="csv-loader",
            step_type=PluginType.LOADER,
            configuration={"output_path": "/path/to/output.csv"}
        )
    ]
)

# Execute the pipeline
executor = create_pipeline_executor(plugin_manager)
result = await executor.execute_pipeline(pipeline)
```

## Testing

Run the integration test to see all plugins working together:

```bash
cd examples
python test_real_plugin_integration.py
```

This test demonstrates:
- CSV data extraction with schema inference
- Data filtering with multiple conditions
- Data aggregation by department
- CSV output with processed results
- Complete data flow tracking

## Dependencies

Some plugins require additional dependencies:
- PostgreSQL plugins: `asyncpg>=0.28.0`
- Schema validation: `jsonschema` (optional)

Install with:
```bash
pip install asyncpg jsonschema
```

## Configuration Examples

### CSV Extractor
```python
config = {
    "file_path": "/data/employees.csv",
    "delimiter": ",",
    "encoding": "utf-8",
    "has_header": True,
    "infer_schema": True,
    "max_rows": 10000
}
```

### Data Filter
```python
config = {
    "filter_rules": [
        {
            "field": "age",
            "operator": "between",
            "value": [25, 65]
        },
        {
            "field": "department", 
            "operator": "in",
            "value": ["Engineering", "Marketing"]
        }
    ],
    "logic_operator": "AND"
}
```

### Data Aggregator
```python
config = {
    "group_by": ["department", "location"],
    "aggregations": [
        {
            "field": "salary",
            "function": "avg",
            "alias": "avg_salary"
        },
        {
            "field": "employee_id",
            "function": "count",
            "alias": "employee_count"
        }
    ]
}
```

## Architecture Benefits

This real plugin implementation provides:

1. **Actual Data Processing**: No more simulated operations
2. **Production Readiness**: Robust error handling and validation
3. **Extensibility**: Easy to add new plugin types
4. **Monitoring**: Built-in metrics and health checks
5. **Flexibility**: Configurable behavior for different use cases
6. **Integration**: Works with existing FLEXT infrastructure