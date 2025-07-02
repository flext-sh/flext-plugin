"""PostgreSQL Database Loader Plugin - Real Data Processing Implementation.

This plugin demonstrates a working database loader that connects to PostgreSQL
and loads data with batch processing, upsert capabilities, and transaction management.
"""

from datetime import datetime
from typing import Any

from flext_plugin.base import BaseLoaderPlugin, PluginMetadata
from flext_plugin.types import PluginError, PluginType

try:
    import asyncpg

    ASYNCPG_AVAILABLE = True
except ImportError:
    ASYNCPG_AVAILABLE = False

    # Create mock asyncpg for type hints
    class MockAsyncpg:
        class Connection:
            pass

        class Pool:
            pass

    asyncpg = MockAsyncpg()


class PostgreSQLLoaderPlugin(BaseLoaderPlugin):
    """PostgreSQL database loader plugin with real data processing capabilities.

    This plugin can load data to PostgreSQL databases with:
    - Connection pooling and management
    - Batch processing for large datasets
    - Insert, update, and upsert operations
    - Transaction management and rollback
    - Schema validation and creation
    - Data type mapping and conversion
    """

    METADATA = PluginMetadata(
        id="postgres-loader",
        name="PostgreSQL Database Loader",
        version="1.0.0",
        description="Load data to PostgreSQL databases with batch processing and transaction management",
        plugin_type=PluginType.LOADER,
        author="FLEXT Team",
        license="MIT",
        entry_point="postgres_loader_plugin.PostgreSQLLoaderPlugin",
        dependencies=["asyncpg>=0.28.0"],
        capabilities=[
            "database_loading",
            "batch_processing",
            "upsert_operations",
            "transaction_management",
            "schema_validation",
            "connection_pooling",
        ],
        configuration_schema={
            "type": "object",
            "properties": {
                "host": {"type": "string", "description": "PostgreSQL host"},
                "port": {
                    "type": "integer",
                    "default": 5432,
                    "description": "PostgreSQL port",
                },
                "database": {"type": "string", "description": "Database name"},
                "username": {"type": "string", "description": "Database username"},
                "password": {"type": "string", "description": "Database password"},
                "table_name": {"type": "string", "description": "Target table name"},
                "schema_name": {
                    "type": "string",
                    "default": "public",
                    "description": "Database schema name",
                },
                "batch_size": {
                    "type": "integer",
                    "default": 1000,
                    "description": "Number of rows per batch",
                },
                "max_connections": {
                    "type": "integer",
                    "default": 10,
                    "description": "Maximum database connections in pool",
                },
                "operation": {
                    "type": "string",
                    "enum": ["insert", "upsert", "update"],
                    "default": "insert",
                    "description": "Load operation type",
                },
                "conflict_columns": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Columns for conflict resolution in upsert operations",
                },
                "create_table": {
                    "type": "boolean",
                    "default": False,
                    "description": "Create table if it doesn't exist",
                },
                "truncate_before_load": {
                    "type": "boolean",
                    "default": False,
                    "description": "Truncate table before loading data",
                },
                "transaction_timeout": {
                    "type": "integer",
                    "default": 300,
                    "description": "Transaction timeout in seconds",
                },
            },
            "required": ["host", "database", "username", "password", "table_name"],
        },
        default_configuration={
            "port": 5432,
            "schema_name": "public",
            "batch_size": 1000,
            "max_connections": 10,
            "operation": "insert",
            "create_table": False,
            "truncate_before_load": False,
            "transaction_timeout": 300,
        },
    )

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize PostgreSQL loader plugin."""
        super().__init__(config)
        self._connection_pool: asyncpg.Pool | None = None
        self._host: str = ""
        self._port: int = 5432
        self._database: str = ""
        self._username: str = ""
        self._password: str = ""
        self._table_name: str = ""
        self._schema_name: str = "public"
        self._batch_size: int = 1000
        self._max_connections: int = 10
        self._operation: str = "insert"
        self._conflict_columns: list[str] = []
        self._create_table: bool = False
        self._truncate_before_load: bool = False
        self._transaction_timeout: int = 300
        self._load_statistics: dict[str, Any] = {}

    async def initialize(self) -> None:
        """Initialize plugin with database connection."""
        if not ASYNCPG_AVAILABLE:
            msg = "asyncpg library is required but not installed"
            raise PluginError(
                msg,
                plugin_id=self.metadata.id,
                error_code="MISSING_DEPENDENCY",
            )

        # Load configuration
        self._host = self._config.get("host", "")
        self._port = self._config.get("port", 5432)
        self._database = self._config.get("database", "")
        self._username = self._config.get("username", "")
        self._password = self._config.get("password", "")
        self._table_name = self._config.get("table_name", "")
        self._schema_name = self._config.get("schema_name", "public")
        self._batch_size = self._config.get("batch_size", 1000)
        self._max_connections = self._config.get("max_connections", 10)
        self._operation = self._config.get("operation", "insert")
        self._conflict_columns = self._config.get("conflict_columns", [])
        self._create_table = self._config.get("create_table", False)
        self._truncate_before_load = self._config.get("truncate_before_load", False)
        self._transaction_timeout = self._config.get("transaction_timeout", 300)

        # Validate required configuration
        if not all(
            [
                self._host,
                self._database,
                self._username,
                self._password,
                self._table_name,
            ]
        ):
            msg = "Missing required database connection parameters"
            raise PluginError(
                msg,
                plugin_id=self.metadata.id,
                error_code="MISSING_CONFIG",
            )

        # Validate operation
        if self._operation not in {"insert", "upsert", "update"}:
            msg = f"Invalid operation: {self._operation}"
            raise PluginError(
                msg,
                plugin_id=self.metadata.id,
                error_code="INVALID_CONFIG",
            )

        # Validate upsert configuration
        if self._operation == "upsert" and not self._conflict_columns:
            msg = "conflict_columns must be specified for upsert operations"
            raise PluginError(
                msg,
                plugin_id=self.metadata.id,
                error_code="MISSING_CONFIG",
            )

        # Create connection pool
        try:
            self._connection_pool = await asyncpg.create_pool(
                host=self._host,
                port=self._port,
                database=self._database,
                user=self._username,
                password=self._password,
                min_size=1,
                max_size=self._max_connections,
                command_timeout=self._transaction_timeout,
            )
        except Exception as e:
            msg = f"Failed to create database connection pool: {e}"
            raise PluginError(
                msg,
                plugin_id=self.metadata.id,
                error_code="CONNECTION_FAILED",
                cause=e,
            )

        # Test connection
        try:
            async with self._connection_pool.acquire() as connection:
                await connection.execute("SELECT 1")
        except Exception as e:
            msg = f"Database connection test failed: {e}"
            raise PluginError(
                msg,
                plugin_id=self.metadata.id,
                error_code="CONNECTION_TEST_FAILED",
                cause=e,
            )

        self._reset_statistics()
        self._initialized = True

    async def load(
        self, data: Any, destination_config: dict[str, Any]
    ) -> dict[str, Any]:
        """Load data to PostgreSQL database.

        Args:
        ----
            data: Data to load (list of records or plugin result)
            destination_config: Additional destination configuration

        Returns:
        -------
        Dictionary containing load results and metrics

        """
        if not self._initialized or not self._connection_pool:
            msg = "Plugin not initialized"
            raise PluginError(
                msg,
                plugin_id=self.metadata.id,
                error_code="NOT_INITIALIZED",
            )

        # Override config with destination_config
        table_name = destination_config.get("table_name", self._table_name)
        schema_name = destination_config.get("schema_name", self._schema_name)
        operation = destination_config.get("operation", self._operation)
        batch_size = destination_config.get("batch_size", self._batch_size)
        truncate_before_load = destination_config.get(
            "truncate_before_load", self._truncate_before_load
        )

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
                msg = f"Unsupported input data type: {type(data)}"
                raise PluginError(
                    msg,
                    plugin_id=self.metadata.id,
                    error_code="INVALID_INPUT_TYPE",
                )

            if not records:
                return {
                    "success": True,
                    "message": "No data to load",
                    "records_loaded": 0,
                }

            self._load_statistics["total_input_records"] = len(records)

            # Get full table name
            full_table_name = f"{schema_name}.{table_name}"

            async with self._connection_pool.acquire() as connection:
                async with connection.transaction():
                    # Create table if requested
                    if self._create_table:
                        await self._create_table_if_not_exists(
                            connection, table_name, schema_name, records[0]
                        )

                    # Truncate table if requested
                    if truncate_before_load:
                        await connection.execute(f"TRUNCATE TABLE {full_table_name}")
                        self._load_statistics["table_truncated"] = True

                    # Load data in batches
                    total_loaded = 0
                    batch_count = 0

                    for i in range(0, len(records), batch_size):
                        batch = records[i : i + batch_size]

                        if operation == "insert":
                            loaded = await self._insert_batch(
                                connection, full_table_name, batch
                            )
                        elif operation == "upsert":
                            loaded = await self._upsert_batch(
                                connection,
                                full_table_name,
                                batch,
                                self._conflict_columns,
                            )
                        elif operation == "update":
                            loaded = await self._update_batch(
                                connection, full_table_name, batch
                            )
                        else:
                            msg = f"Unsupported operation: {operation}"
                            raise PluginError(
                                msg,
                                plugin_id=self.metadata.id,
                                error_code="INVALID_OPERATION",
                            )

                        total_loaded += loaded
                        batch_count += 1

                        self._load_statistics["batches_processed"] = batch_count
                        self._load_statistics["records_loaded"] = total_loaded

            # Build result
            return {
                "success": True,
                "records_loaded": total_loaded,
                "batches_processed": batch_count,
                "table_name": full_table_name,
                "operation": operation,
                "load_timestamp": datetime.now().isoformat(),
                "input_metadata": input_metadata,
                "load_statistics": self._load_statistics.copy(),
            }

        except Exception as e:
            msg = f"Failed to load data to PostgreSQL: {e}"
            raise PluginError(
                msg,
                plugin_id=self.metadata.id,
                error_code="LOAD_FAILED",
                cause=e,
            )

    async def health_check(self) -> dict[str, Any]:
        """Perform health check."""
        health = {
            "status": "healthy",
            "plugin_id": self.metadata.id,
            "initialized": self._initialized,
            "connection_pool_status": None,
            "database_accessible": False,
            "table_accessible": False,
            "checks": [],
        }

        # Check connection pool
        if self._connection_pool:
            try:
                pool_size = self._connection_pool.get_size()
                health["connection_pool_status"] = {
                    "size": pool_size,
                    "max_size": self._max_connections,
                }
                health["checks"].append(
                    f"Connection pool healthy ({pool_size}/{self._max_connections})"
                )
            except Exception as e:
                health["checks"].append(f"Connection pool check failed: {e}")
                health["status"] = "degraded"

        # Test database connectivity
        if self._connection_pool:
            try:
                async with self._connection_pool.acquire() as connection:
                    result = await connection.fetchval("SELECT 1")
                    if result == 1:
                        health["database_accessible"] = True
                        health["checks"].append("Database connection successful")
                    else:
                        health["checks"].append("Unexpected database response")
                        health["status"] = "degraded"
            except Exception as e:
                health["checks"].append(f"Database connection failed: {e}")
                health["status"] = "unhealthy"

        # Test table accessibility
        if self._connection_pool and health["database_accessible"]:
            try:
                full_table_name = f"{self._schema_name}.{self._table_name}"
                async with self._connection_pool.acquire() as connection:
                    await connection.execute(f"SELECT 1 FROM {full_table_name} LIMIT 1")
                    health["table_accessible"] = True
                    health["checks"].append(f"Table {full_table_name} accessible")
            except Exception as e:
                health["checks"].append(f"Table {full_table_name} not accessible: {e}")
                if not self._create_table:
                    health["status"] = "degraded"

        return health

    async def cleanup(self) -> None:
        """Clean up plugin resources."""
        if self._connection_pool:
            await self._connection_pool.close()
            self._connection_pool = None
        self._reset_statistics()
        self._initialized = False

    async def _create_table_if_not_exists(
        self,
        connection: asyncpg.Connection,
        table_name: str,
        schema_name: str,
        sample_record: dict[str, Any],
    ) -> None:
        """Create table if it doesn't exist based on sample record."""
        full_table_name = f"{schema_name}.{table_name}"

        # Check if table exists
        exists = await connection.fetchval(
            """
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = $1 AND table_name = $2
            )
        """,
            schema_name,
            table_name,
        )

        if not exists:
            # Infer column types from sample record
            columns = []
            for field, value in sample_record.items():
                postgres_type = self._infer_postgres_type(value)
                columns.append(f'"{field}" {postgres_type}')

            # Create table
            create_sql = f"""
                CREATE TABLE {full_table_name} (
                    {', '.join(columns)}
                )
            """

            await connection.execute(create_sql)
            self._load_statistics["table_created"] = True

    async def _insert_batch(
        self,
        connection: asyncpg.Connection,
        table_name: str,
        batch: list[dict[str, Any]],
    ) -> int:
        """Insert batch of records."""
        if not batch:
            return 0

        # Get field names from first record
        fields = list(batch[0].keys())
        placeholders = ", ".join(f"${i + 1}" for i in range(len(fields)))
        field_names = ", ".join(f'"{field}"' for field in fields)

        insert_sql = f"""
            INSERT INTO {table_name} ({field_names})
            VALUES ({placeholders})
        """

        # Prepare data for batch insert
        batch_data = []
        for record in batch:
            row = [record.get(field) for field in fields]
            batch_data.append(row)

        await connection.executemany(insert_sql, batch_data)
        return len(batch)

    async def _upsert_batch(
        self,
        connection: asyncpg.Connection,
        table_name: str,
        batch: list[dict[str, Any]],
        conflict_columns: list[str],
    ) -> int:
        """Upsert batch of records using ON CONFLICT."""
        if not batch:
            return 0

        fields = list(batch[0].keys())
        placeholders = ", ".join(f"${i + 1}" for i in range(len(fields)))
        field_names = ", ".join(f'"{field}"' for field in fields)

        # Build conflict columns
        conflict_cols = ", ".join(f'"{col}"' for col in conflict_columns)

        # Build update clause for non-conflict columns
        update_fields = [f for f in fields if f not in conflict_columns]
        update_clause = ", ".join(
            f'"{field}" = EXCLUDED."{field}"' for field in update_fields
        )

        upsert_sql = f"""
            INSERT INTO {table_name} ({field_names})
            VALUES ({placeholders})
            ON CONFLICT ({conflict_cols})
            DO UPDATE SET {update_clause}
        """

        # Prepare data for batch upsert
        batch_data = []
        for record in batch:
            row = [record.get(field) for field in fields]
            batch_data.append(row)

        await connection.executemany(upsert_sql, batch_data)
        return len(batch)

    async def _update_batch(
        self,
        connection: asyncpg.Connection,
        table_name: str,
        batch: list[dict[str, Any]],
    ) -> int:
        """Update batch of records (requires primary key)."""
        # This is a simplified update - in practice, you'd need to identify
        # which columns constitute the primary key for the WHERE clause
        msg = "Update operation not fully implemented - requires primary key configuration"
        raise PluginError(
            msg,
            plugin_id=self.metadata.id,
            error_code="NOT_IMPLEMENTED",
        )

    def _infer_postgres_type(self, value: Any) -> str:
        """Infer PostgreSQL data type from Python value."""
        if value is None:
            return "TEXT"
        if isinstance(value, bool):
            return "BOOLEAN"
        if isinstance(value, int):
            return "BIGINT"
        if isinstance(value, float):
            return "DOUBLE PRECISION"
        if isinstance(value, datetime):
            return "TIMESTAMP"
        if isinstance(value, list | dict):
            return "JSONB"
        return "TEXT"

    def _reset_statistics(self) -> None:
        """Reset load statistics."""
        self._load_statistics = {
            "total_input_records": 0,
            "records_loaded": 0,
            "batches_processed": 0,
            "table_created": False,
            "table_truncated": False,
        }


# Entry point for plugin discovery
plugin_class = PostgreSQLLoaderPlugin
