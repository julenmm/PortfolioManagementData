"""
Utility functions for economic data tasks
"""

from airflow.providers.postgres.hooks.postgres import PostgresHook
from typing import Optional


def get_db_hook() -> PostgresHook:
    """Get database hook for TimescaleDB connection"""
    return PostgresHook(postgres_conn_id='timescaledb_conn')


def get_last_date(schema: str, table: str, series_id: str) -> Optional[str]:
    """Get the last date for a specific series in a table"""
    hook = get_db_hook()
    
    query = f"SELECT MAX(date) FROM {schema}.{table} WHERE series_id = %s"
    result = hook.get_first(query, parameters=(series_id,))
    
    if result and result[0]:
        return result[0].strftime('%Y-%m-%d')
    
    return None


def log_update(schema: str, table: str, records_count: int, status: str):
    """Log update results"""
    print(f"Update {schema}.{table}: {records_count} records, status: {status}")
