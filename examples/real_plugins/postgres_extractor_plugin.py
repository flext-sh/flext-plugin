"""PostgreSQL Database Extractor Plugin - Real Data Processing Implementation.

This plugin demonstrates a working database extractor that connects to PostgreSQL
and extracts data with SQL queries. It includes connection management,
query optimization, and batch processing capabilities.
"""

from collections.abc import AsyncIterator
from datetime import UTC, datetime
from typing import Any, Optional

from flext_plugin.base import BaseExtractorPlugin, PluginMetadata
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


class PostgreSQLExtractorPlugin(BaseExtractorPlugin):
    """PostgreSQL database extractor plugin with real data processing capabilities.

    This plugin can extract data from PostgreSQL databases with:
    - Connection pooling and management
    - Custom SQL queries or table extraction
    - Batch processing for large datasets
    - Schema introspection
    - Incremental extraction support
    - Query optimization and timeout handling
    """

    METADATA = PluginMetadata(
        id="postgres-extractor",
        name="PostgreSQL Database Extractor",
        version="1.0.0",
        description="Extract data from PostgreSQL databases with SQL queries and batch processing",
        plugin_type=PluginType.EXTRACTOR,
        author="FLEXT Team",
        license="MIT",
        entry_point="postgres_extractor_plugin.PostgreSQLExtractorPlugin",
        dependencies=["asyncpg>=0.28.0"],
        capabilities=[
            "database_extraction",
            "custom_queries",
            "batch_processing",
            "schema_introspection",
            "incremental_extraction",
            "connection_pooling"
        ],
        configuration_schema={
            "type": "object",
            "properties": {
                "host": {
                    "type": "string",
                    "description": "PostgreSQL host"
                },
                "port": {
                    "type": "integer",
                    "default": 5432,
                    "description": "PostgreSQL port"
                },
                "database": {
                    "type": "string",
                    "description": "Database name"
                },
                "username": {
                    "type": "string",
                    "description": "Database username"
                },
                "password": {
                    "type": "string",
                    "description": "Database password"
                },
                "table_name": {
                    "type": "string",
                    "description": "Table to extract (if not using custom query)"
                },
                "query": {
                    "type": "string",
                    "description": "Custom SQL query to execute"
                },
                "batch_size": {
                    "type": "integer",
                    "default": 1000,
                    "description": "Number of rows per batch"
                },
                "max_connections": {
                    "type": "integer",
                    "default": 10,
                    "description": "Maximum database connections in pool"
                },
                "query_timeout": {
                    "type": "integer",
                    "default": 300,
                    "description": "Query timeout in seconds"
                },
                "incremental_column": {
                    "type": "string",
                    "description": "Column for incremental extraction (e.g., updated_at)"
                },
                "incremental_value": {
                    "type": "string",
                    "description": "Last extracted value for incremental extraction"
                }
            },
            "required": ["host", "database", "username", "password"]
        },
        default_configuration={
            "port": 5432,
            "batch_size": 1000,
            "max_connections": 10,
            "query_timeout": 300
        }
    )

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize PostgreSQL extractor plugin."""
        super().__init__(config)
        self._connection_pool: Optional[asyncpg.Pool] = None
        self._host: str = ""
        self._port: int = 5432
        self._database: str = ""
        self._username: str = ""
        self._password: str = ""
        self._table_name: Optional[str] = None
        self._query: Optional[str] = None
        self._batch_size: int = 1000
        self._max_connections: int = 10
        self._query_timeout: int = 300
        self._incremental_column: Optional[str] = None
        self._incremental_value: Optional[str] = None

    async def initialize(self) -> None:
        """Initialize plugin with database connection."""
        if not ASYNCPG_AVAILABLE:
            raise PluginError(
                "asyncpg library is required but not installed",
                plugin_id=self.metadata.id,
                error_code="MISSING_DEPENDENCY"
            )

        # Load configuration
        self._host = self._config.get("host", "")
        self._port = self._config.get("port", 5432)
        self._database = self._config.get("database", "")
        self._username = self._config.get("username", "")
        self._password = self._config.get("password", "")
        self._table_name = self._config.get("table_name")
        self._query = self._config.get("query")
        self._batch_size = self._config.get("batch_size", 1000)
        self._max_connections = self._config.get("max_connections", 10)
        self._query_timeout = self._config.get("query_timeout", 300)
        self._incremental_column = self._config.get("incremental_column")
        self._incremental_value = self._config.get("incremental_value")

        # Validate required configuration
        if not all([self._host, self._database, self._username, self._password]):
            raise PluginError(
                "Missing required database connection parameters",
                plugin_id=self.metadata.id,
                error_code="MISSING_CONFIG"
            )

        if not self._table_name and not self._query:
            raise PluginError(
                "Either table_name or query must be specified",
                plugin_id=self.metadata.id,
                error_code="MISSING_CONFIG"
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
                command_timeout=self._query_timeout
            )
        except Exception as e:
            raise PluginError(
                f"Failed to create database connection pool: {e}",
                plugin_id=self.metadata.id,
                error_code="CONNECTION_FAILED",
                cause=e
            )

        # Test connection
        try:
            async with self._connection_pool.acquire() as connection:
                await connection.execute("SELECT 1")
        except Exception as e:
            raise PluginError(
                f"Database connection test failed: {e}",
                plugin_id=self.metadata.id,
                error_code="CONNECTION_TEST_FAILED",
                cause=e
            )

        self._initialized = True

    async def extract(self, source_config: dict[str, Any]) -> dict[str, Any]:
        """Extract data from PostgreSQL database.

        Args:
        ----
            source_config: Additional source configuration

        Returns:
        -------
            Dictionary containing extracted data and metadata

        """
        if not self._initialized or not self._connection_pool:
            raise PluginError(
                "Plugin not initialized",
                plugin_id=self.metadata.id,
                error_code="NOT_INITIALIZED"
            )

        # Override config with source_config
        query = source_config.get("query", self._query)
        table_name = source_config.get("table_name", self._table_name)
        batch_size = source_config.get("batch_size", self._batch_size)
        incremental_column = source_config.get("incremental_column", self._incremental_column)
        incremental_value = source_config.get("incremental_value", self._incremental_value)

        try:
            # Build final query
            final_query = await self._build_query(
                query=query,
                table_name=table_name,
                incremental_column=incremental_column,
                incremental_value=incremental_value
            )

            # Execute query and collect results
            records = []
            total_rows = 0

            async with self._connection_pool.acquire() as connection:
                # Get query plan for optimization info
                explain_query = f"EXPLAIN (FORMAT JSON) {final_query}"
                try:
                    plan_result = await connection.fetch(explain_query)
                    query_plan = plan_result[0][0] if plan_result else {}
                except:
                    query_plan = {}

                # Execute main query
                async with connection.transaction():
                    cursor = await connection.cursor(final_query)

                    while True:
                        batch = await cursor.fetch(batch_size)
                        if not batch:
                            break

                        # Convert records to dictionaries
                        for record in batch:
                            record_dict = dict(record)
                            records.append(record_dict)
                            total_rows += 1

            # Get table schema information
            schema_info = await self._get_table_schema(table_name) if table_name else {}

            metadata = {
                "extraction_timestamp": datetime.now(UTC).isoformat(),
                "total_rows_extracted": total_rows,
                "query_executed": final_query,
                "query_plan": query_plan,
                "batch_size": batch_size,
                "table_name": table_name,
                "schema_info": schema_info,
                "incremental_extraction": bool(incremental_column),
                "database_info": {
                    "host": self._host,
                    "port": self._port,
                    "database": self._database
                }
            }

            return {
                "data": records,
                "metadata": metadata,
                "schema": schema_info.get("columns", {}),
                "success": True
            }

        except Exception as e:
            raise PluginError(
                f"Failed to extract data from PostgreSQL: {e}",
                plugin_id=self.metadata.id,
                error_code="EXTRACTION_FAILED",
                cause=e
            )

    async def extract_stream(self, source_config: dict[str, Any]) -> AsyncIterator[dict[str, Any]]:
        """Extract data as a stream for large datasets.

        Args:
        ----
            source_config: Source configuration

        Yields:
        ------
            Individual records as dictionaries

        """
        if not self._initialized or not self._connection_pool:
            raise PluginError(
                "Plugin not initialized",
                plugin_id=self.metadata.id,
                error_code="NOT_INITIALIZED"
            )

        query = source_config.get("query", self._query)
        table_name = source_config.get("table_name", self._table_name)
        batch_size = source_config.get("batch_size", self._batch_size)
        incremental_column = source_config.get("incremental_column", self._incremental_column)
        incremental_value = source_config.get("incremental_value", self._incremental_value)

        try:
            final_query = await self._build_query(
                query=query,
                table_name=table_name,
                incremental_column=incremental_column,
                incremental_value=incremental_value
            )

            async with self._connection_pool.acquire() as connection:
                async with connection.transaction():
                    cursor = await connection.cursor(final_query)

                    while True:
                        batch = await cursor.fetch(batch_size)
                        if not batch:
                            break

                        for record in batch:
                            yield dict(record)

        except Exception as e:
            raise PluginError(
                f"Failed to stream data from PostgreSQL: {e}",
                plugin_id=self.metadata.id,
                error_code="STREAM_FAILED",
                cause=e
            )

    async def health_check(self) -> dict[str, Any]:
        """Perform health check."""
        health = {
            "status": "healthy",
            "plugin_id": self.metadata.id,
            "initialized": self._initialized,
            "connection_pool_status": None,
            "database_accessible": False,
            "checks": []
        }

        # Check connection pool
        if self._connection_pool:
            try:
                pool_size = self._connection_pool.get_size()
                health["connection_pool_status"] = {
                    "size": pool_size,
                    "max_size": self._max_connections
                }
                health["checks"].append(f"Connection pool healthy ({pool_size}/{self._max_connections})")
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

        return health

    async def cleanup(self) -> None:
        """Clean up plugin resources."""
        if self._connection_pool:
            await self._connection_pool.close()
            self._connection_pool = None
        self._initialized = False

    async def _build_query(
        self,
        query: Optional[str] = None,
        table_name: Optional[str] = None,
        incremental_column: Optional[str] = None,
        incremental_value: Optional[str] = None
    ) -> str:
        """Build final SQL query with incremental logic."""
        if query:
            # Use custom query
            final_query = query
        elif table_name:
            # Build query from table name
            final_query = f"SELECT * FROM {table_name}"
        else:
            raise PluginError(
                "No query or table_name specified",
                plugin_id=self.metadata.id,
                error_code="MISSING_QUERY"
            )

        # Add incremental extraction logic
        if incremental_column and incremental_value:
            if " WHERE " in final_query.upper():
                final_query += f" AND {incremental_column} > '{incremental_value}'"
            else:
                final_query += f" WHERE {incremental_column} > '{incremental_value}'"

            # Add ORDER BY for consistent incremental extraction
            if " ORDER BY " not in final_query.upper():
                final_query += f" ORDER BY {incremental_column}"

        return final_query

    async def _get_table_schema(self, table_name: str) -> dict[str, Any]:
        """Get table schema information."""
        if not self._connection_pool or not table_name:
            return {}

        try:
            async with self._connection_pool.acquire() as connection:
                # Get column information
                column_query = """
                    SELECT
                        column_name,
                        data_type,
                        is_nullable,
                        column_default,
                        character_maximum_length,
                        numeric_precision,
                        numeric_scale
                    FROM information_schema.columns
                    WHERE table_name = $1
                    ORDER BY ordinal_position
                """

                columns = await connection.fetch(column_query, table_name)

                schema_info = {
                    "table_name": table_name,
                    "columns": {}
                }

                for column in columns:
                    column_name = column["column_name"]
                    schema_info["columns"][column_name] = {
                        "data_type": column["data_type"],
                        "nullable": column["is_nullable"] == "YES",
                        "default": column["column_default"],
                        "max_length": column["character_maximum_length"],
                        "precision": column["numeric_precision"],
                        "scale": column["numeric_scale"]
                    }

                return schema_info

        except Exception as e:
            # Schema introspection is optional
            return {"error": str(e)}


# Entry point for plugin discovery
plugin_class = PostgreSQLExtractorPlugin
