#!/usr/bin/env python3
"""Test Real Plugin Integration with End-to-End Data Processing.

This script demonstrates the complete plugin integration by:
1. Creating sample data files
2. Loading and configuring real plugins
3. Running a complete ETL pipeline with actual data processing
4. Validating the results

This serves as both a test and a demonstration of the real plugin system.
"""

import asyncio
import tempfile
from pathlib import Path
from typing import Any

# Import sample plugins
from real_plugins.csv_extractor_plugin import CSVExtractorPlugin
from real_plugins.csv_loader_plugin import CSVLoaderPlugin
from real_plugins.data_aggregator_transformer_plugin import (
    DataAggregatorTransformerPlugin,
)
from real_plugins.data_filter_transformer_plugin import DataFilterTransformerPlugin

# Import the plugin system components
from flext_plugin.manager import PluginManager, create_plugin_manager
from flext_plugin.pipeline_executor import (
    Pipeline,
    PipelineStep,
    create_pipeline_executor,
)
from flext_plugin.types import PluginType


class PluginIntegrationTest:
    """Test suite for real plugin integration."""

    def __init__(self) -> None:
        """Initialize test environment."""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="flext_plugin_test_"))
        self.input_file = self.temp_dir / "sample_data.csv"
        self.output_file = self.temp_dir / "processed_data.csv"

        # Create a mock container for the plugin manager
        self.mock_container = None  # In a real scenario, this would be the DI container


    def create_sample_data(self) -> None:
        """Create sample CSV data for testing."""
        sample_data = [
            "id,name,age,department,salary,active",
            "1,Alice Johnson,28,Engineering,75000,true",
            "2,Bob Smith,34,Marketing,62000,true",
            "3,Charlie Brown,29,Engineering,68000,false",
            "4,Diana Prince,31,HR,58000,true",
            "5,Eve Wilson,27,Engineering,72000,true",
            "6,Frank Miller,35,Marketing,65000,true",
            "7,Grace Lee,26,HR,55000,false",
            "8,Henry Davis,33,Engineering,78000,true",
            "9,Iris Taylor,30,Marketing,60000,true",
            "10,Jack Anderson,32,Engineering,76000,true"
        ]

        with open(self.input_file, 'w') as f:
            f.write('\n'.join(sample_data))


    async def setup_plugin_manager(self) -> PluginManager:
        """Set up plugin manager with real plugins."""
        # Create plugin manager (without actual container for this test)
        plugin_manager = create_plugin_manager(
            container=self.mock_container,
            auto_discover=False,  # We'll manually register plugins
            security_enabled=False  # Disable for testing
        )

        # Initialize plugin manager
        await plugin_manager.initialize()

        # Manually register our test plugins
        await self._register_test_plugins(plugin_manager)

        return plugin_manager

    async def _register_test_plugins(self, plugin_manager: PluginManager) -> None:
        """Register test plugins manually."""
        # Create plugin instances with test configurations

        # CSV Extractor
        csv_extractor = CSVExtractorPlugin({
            "file_path": str(self.input_file),
            "delimiter": ",",
            "has_header": True,
            "infer_schema": True
        })
        await csv_extractor.initialize()

        # Data Filter Transformer
        filter_transformer = DataFilterTransformerPlugin({
            "filter_rules": [
                {
                    "field": "active",
                    "operator": "equals",
                    "value": "true"
                },
                {
                    "field": "age",
                    "operator": "greater_than",
                    "value": "25"
                }
            ],
            "logic_operator": "AND"
        })
        await filter_transformer.initialize()

        # Data Aggregator Transformer
        aggregator_transformer = DataAggregatorTransformerPlugin({
            "group_by": ["department"],
            "aggregations": [
                {
                    "field": "salary",
                    "function": "avg",
                    "alias": "avg_salary"
                },
                {
                    "field": "salary",
                    "function": "count",
                    "alias": "employee_count"
                },
                {
                    "field": "age",
                    "function": "avg",
                    "alias": "avg_age"
                }
            ]
        })
        await aggregator_transformer.initialize()

        # CSV Loader
        csv_loader = CSVLoaderPlugin({
            "output_path": str(self.output_file),
            "delimiter": ",",
            "include_header": True
        })
        await csv_loader.initialize()

        # Register plugins in the manager's registry
        plugin_manager.registry._plugins = {
            "csv-extractor": csv_extractor,
            "data-filter": filter_transformer,
            "data-aggregator": aggregator_transformer,
            "csv-loader": csv_loader
        }


    def create_test_pipeline(self) -> Pipeline:
        """Create a test pipeline with real plugin steps."""
        steps = [
            # Step 1: Extract data from CSV
            PipelineStep(
                step_id="extract_csv",
                plugin_id="csv-extractor",
                step_type=PluginType.EXTRACTOR,
                configuration={
                    "file_path": str(self.input_file)
                }
            ),

            # Step 2: Filter active employees over 25
            PipelineStep(
                step_id="filter_active_employees",
                plugin_id="data-filter",
                step_type=PluginType.TRANSFORMER,
                configuration={
                    "filter_rules": [
                        {
                            "field": "active",
                            "operator": "equals",
                            "value": "true"
                        }
                    ]
                },
                dependencies=["extract_csv"]
            ),

            # Step 3: Aggregate by department
            PipelineStep(
                step_id="aggregate_by_department",
                plugin_id="data-aggregator",
                step_type=PluginType.TRANSFORMER,
                configuration={
                    "group_by": ["department"],
                    "aggregations": [
                        {
                            "field": "salary",
                            "function": "avg",
                            "alias": "avg_salary"
                        },
                        {
                            "field": "id",
                            "function": "count",
                            "alias": "employee_count"
                        }
                    ]
                },
                dependencies=["filter_active_employees"]
            ),

            # Step 4: Load aggregated data to CSV
            PipelineStep(
                step_id="load_to_csv",
                plugin_id="csv-loader",
                step_type=PluginType.LOADER,
                configuration={
                    "output_path": str(self.output_file)
                },
                dependencies=["aggregate_by_department"]
            )
        ]

        pipeline = Pipeline(
            pipeline_id="test_etl_pipeline",
            name="Test ETL Pipeline with Real Plugins",
            steps=steps,
            configuration={
                "description": "End-to-end test of plugin integration",
                "version": "1.0.0"
            }
        )

        return pipeline

    async def run_pipeline_test(self) -> dict[str, Any]:
        """Run the complete pipeline test."""
        # Set up plugin manager
        plugin_manager = await self.setup_plugin_manager()

        # Create pipeline executor
        pipeline_executor = create_pipeline_executor(plugin_manager)

        # Create test pipeline
        pipeline = self.create_test_pipeline()

        # Execute pipeline

        result = await pipeline_executor.execute_pipeline(
            pipeline=pipeline,
            user_id="test_user",
            environment="test",
            global_variables={"test_mode": True}
        )

        return result

    def validate_results(self, execution_result: dict[str, Any]) -> bool:
        """Validate the pipeline execution results."""
        success = True

        # Check execution success
        if not execution_result.get("success", False):
            success = False
        else:
            pass

        # Check output file exists
        if self.output_file.exists():

            # Read and validate output data
            with open(self.output_file) as f:
                output_content = f.read()
                lines = output_content.strip().split('\n')


                if len(lines) > 1:  # Header + data rows

                    # Print sample of output data
                    for _i, _line in enumerate(lines[:5]):  # Show first 5 lines
                        pass

                    if len(lines) > 5:
                        pass
                else:
                    success = False
        else:
            success = False

        # Check execution summary
        execution_result.get("execution_summary", {})

        return success

    def cleanup(self) -> None:
        """Clean up test environment."""
        try:
            # Remove test files
            import shutil
            shutil.rmtree(self.temp_dir)
        except Exception:
            pass

    def print_test_summary(self, success: bool, execution_result: dict[str, Any]) -> None:
        """Print test summary."""
        if success:

            # Print what was demonstrated
            pass

        else:
            pass


        final_data = execution_result.get("final_data")
        if final_data:
            pass


async def main():
    """Main test function."""
    test = PluginIntegrationTest()

    try:
        # Create sample data
        test.create_sample_data()

        # Run the pipeline test
        execution_result = await test.run_pipeline_test()

        # Validate results
        success = test.validate_results(execution_result)

        # Print summary
        test.print_test_summary(success, execution_result)

        return success

    except Exception:
        import traceback
        traceback.print_exc()
        return False

    finally:
        # Always cleanup
        test.cleanup()


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
