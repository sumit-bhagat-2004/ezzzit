"""
Snowflake connection module.
Provides persistent connection management with auto-reconnect capabilities.
"""

import snowflake.connector
from snowflake.connector import SnowflakeConnection
from snowflake.connector.cursor import SnowflakeCursor
import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global connection instance
_connection: SnowflakeConnection = None


def get_connection() -> SnowflakeConnection:
    """
    Get or create a persistent Snowflake connection.
    Auto-reconnects if connection is closed or invalid.
    
    Returns:
        SnowflakeConnection: Active Snowflake connection
    """
    global _connection
    
    if _connection is None or _connection.is_closed():
        logger.info("Creating new Snowflake connection...")
        _connection = snowflake.connector.connect(
            user=config.SNOWFLAKE_USER,
            password=config.SNOWFLAKE_PASSWORD,
            account=config.SNOWFLAKE_ACCOUNT,
            warehouse=config.SNOWFLAKE_WAREHOUSE,
            database=config.SNOWFLAKE_DATABASE,
            schema=config.SNOWFLAKE_SCHEMA
        )
        logger.info("Snowflake connection established successfully")
    
    return _connection


def get_cursor() -> SnowflakeCursor:
    """
    Get a cursor from the active connection.
    Ensures connection is valid before returning cursor.
    
    Returns:
        SnowflakeCursor: Cursor for executing queries
    """
    conn = get_connection()
    return conn.cursor()


def close_connection():
    """
    Close the Snowflake connection if it exists.
    """
    global _connection
    if _connection and not _connection.is_closed():
        _connection.close()
        logger.info("Snowflake connection closed")
        _connection = None


def execute_query(query: str, params: dict = None):
    """
    Execute a query and return results.
    
    Args:
        query: SQL query string
        params: Optional query parameters
    
    Returns:
        Query results
    """
    cursor = get_cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()


def initialize_schema():
    """
    Initialize the Snowflake schema and knowledge base table.
    Creates table if it doesn't exist.
    """
    cursor = get_cursor()
    try:
        # Ensure we're using the correct database and schema
        cursor.execute(f"USE DATABASE {config.SNOWFLAKE_DATABASE}")
        cursor.execute(f"USE SCHEMA {config.SNOWFLAKE_SCHEMA}")
        
        # Create knowledge base table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS KNOWLEDGE_BASE (
            ID STRING,
            CONCEPT STRING,
            CONTENT STRING,
            EMBEDDING VECTOR(FLOAT, 768)
        )
        """
        cursor.execute(create_table_query)
        logger.info("Knowledge base table initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing schema: {e}")
        raise
    finally:
        cursor.close()