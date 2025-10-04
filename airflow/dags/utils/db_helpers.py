"""
Database helper functions for economic data pipeline
"""

from airflow.providers.postgres.hooks.postgres import PostgresHook
from typing import Optional, Tuple
from datetime import datetime


def get_db_hook(conn_id: str = 'timescaledb_conn') -> PostgresHook:
    """Get PostgreSQL hook with connection to TimescaleDB"""
    return PostgresHook(postgres_conn_id=conn_id)


def log_update(
    schema: str, 
    table: str, 
    records_added: int, 
    status: str,
    error_message: Optional[str] = None,
    source_id: Optional[int] = None
):
    """
    Log data update to metadata.data_updates table
    
    Args:
        schema: Database schema name
        table: Table name
        records_added: Number of records added/updated
        status: Update status (success, failed, no_new_data)
        error_message: Error message if status is failed
        source_id: Reference to data source ID
    """
    hook = get_db_hook()
    
    sql = """
    INSERT INTO metadata.data_updates 
    (schema_name, table_name, source_id, records_added, update_status, error_message, completed_at)
    VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """
    
    hook.run(sql, parameters=(schema, table, source_id, records_added, status, error_message))


def get_last_date(schema: str, table: str, series_id: Optional[str] = None) -> Optional[str]:
    """
    Get the last date of data in a table
    
    Args:
        schema: Database schema name
        table: Table name
        series_id: Optional series ID to filter by
        
    Returns:
        Last date as string in YYYY-MM-DD format, or None if no data
    """
    hook = get_db_hook()
    
    if series_id:
        sql = f"SELECT MAX(date) FROM {schema}.{table} WHERE series_id = %s"
        result = hook.get_first(sql, parameters=(series_id,))
    else:
        sql = f"SELECT MAX(date) FROM {schema}.{table}"
        result = hook.get_first(sql)
    
    if result and result[0]:
        return result[0].strftime('%Y-%m-%d')
    
    return None


def insert_or_update(
    schema: str,
    table: str,
    data: dict,
    conflict_columns: list,
    update_columns: list = None
):
    """
    Insert data or update on conflict
    
    Args:
        schema: Database schema name
        table: Table name
        data: Dictionary of column_name: value
        conflict_columns: Columns that define uniqueness
        update_columns: Columns to update on conflict (if None, updates all)
    """
    hook = get_db_hook()
    
    columns = list(data.keys())
    values = list(data.values())
    placeholders = ', '.join(['%s'] * len(values))
    
    # Build conflict clause
    conflict_cols = ', '.join(conflict_columns)
    
    # Build update clause
    if update_columns is None:
        update_columns = [col for col in columns if col not in conflict_columns]
    
    update_clause = ', '.join([f"{col} = EXCLUDED.{col}" for col in update_columns])
    
    sql = f"""
    INSERT INTO {schema}.{table} ({', '.join(columns)})
    VALUES ({placeholders})
    ON CONFLICT ({conflict_cols}) DO UPDATE SET {update_clause}
    """
    
    hook.run(sql, parameters=tuple(values))


def get_source_id(source_name: str) -> Optional[int]:
    """
    Get source ID from metadata.data_sources
    
    Args:
        source_name: Name of the data source
        
    Returns:
        Source ID or None if not found
    """
    hook = get_db_hook()
    
    sql = "SELECT id FROM metadata.data_sources WHERE source_name = %s"
    result = hook.get_first(sql, parameters=(source_name,))
    
    if result:
        return result[0]
    
    return None


def execute_query(query: str, params: tuple = None) -> list:
    """
    Execute a query and return results
    
    Args:
        query: SQL query to execute
        params: Query parameters
        
    Returns:
        List of result rows
    """
    hook = get_db_hook()
    return hook.get_records(query, parameters=params)
