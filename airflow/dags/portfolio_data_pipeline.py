"""
Portfolio Management Data Pipeline
This DAG handles the complete data pipeline for portfolio management.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Default arguments
default_args = {
    'owner': 'portfolio_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
dag = DAG(
    'portfolio_data_pipeline',
    default_args=default_args,
    description='Complete portfolio management data pipeline',
    schedule_interval='0 6 * * *',  # Daily at 6 AM
    catchup=False,
    tags=['portfolio', 'data', 'pipeline'],
)

def extract_market_data(**context):
    """Extract market data from various sources"""
    import requests
    import pandas as pd
    from datetime import datetime
    
    # Example: Extract data from a financial API
    # In a real implementation, you would connect to actual APIs
    print("Extracting market data...")
    
    # Simulate data extraction
    data = {
        'symbol': ['AAPL', 'GOOGL', 'MSFT', 'TSLA'],
        'price': [150.0, 2800.0, 300.0, 800.0],
        'volume': [1000000, 500000, 800000, 600000],
        'timestamp': [datetime.now()] * 4
    }
    
    df = pd.DataFrame(data)
    print(f"Extracted {len(df)} records")
    
    return df.to_json()

def transform_data(**context):
    """Transform and clean the extracted data"""
    import pandas as pd
    import json
    
    # Get data from previous task
    ti = context['ti']
    data_json = ti.xcom_pull(task_ids='extract_market_data')
    
    df = pd.read_json(data_json)
    
    # Data transformation logic
    df['price_change'] = df['price'].pct_change()
    df['volume_weighted_price'] = df['price'] * df['volume']
    
    print("Data transformation completed")
    return df.to_json()

def load_data_to_timescaledb(**context):
    """Load transformed data to TimescaleDB"""
    import pandas as pd
    import json
    
    # Get data from previous task
    ti = context['ti']
    data_json = ti.xcom_pull(task_ids='transform_data')
    
    df = pd.read_json(data_json)
    
    # Connect to TimescaleDB
    postgres_hook = PostgresHook(postgres_conn_id='timescaledb_conn')
    
    # Create table if not exists
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS market_data (
        id SERIAL PRIMARY KEY,
        symbol VARCHAR(10) NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        volume BIGINT NOT NULL,
        price_change DECIMAL(10,4),
        volume_weighted_price DECIMAL(15,2),
        timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    
    -- Create hypertable for time-series data
    SELECT create_hypertable('market_data', 'timestamp', if_not_exists => TRUE);
    """
    
    postgres_hook.run(create_table_sql)
    
    # Insert data
    for _, row in df.iterrows():
        insert_sql = """
        INSERT INTO market_data (symbol, price, volume, price_change, volume_weighted_price, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        postgres_hook.run(insert_sql, parameters=(
            row['symbol'], row['price'], row['volume'], 
            row['price_change'], row['volume_weighted_price'], row['timestamp']
        ))
    
    print(f"Loaded {len(df)} records to TimescaleDB")

def calculate_portfolio_metrics(**context):
    """Calculate portfolio performance metrics"""
    postgres_hook = PostgresHook(postgres_conn_id='timescaledb_conn')
    
    # Calculate portfolio metrics
    metrics_sql = """
    WITH portfolio_metrics AS (
        SELECT 
            symbol,
            AVG(price) as avg_price,
            STDDEV(price) as price_volatility,
            MAX(price) as max_price,
            MIN(price) as min_price,
            SUM(volume) as total_volume
        FROM market_data 
        WHERE timestamp >= NOW() - INTERVAL '1 day'
        GROUP BY symbol
    )
    SELECT * FROM portfolio_metrics;
    """
    
    results = postgres_hook.get_records(metrics_sql)
    print(f"Calculated metrics for {len(results)} symbols")
    
    return results

# Task definitions
extract_task = PythonOperator(
    task_id='extract_market_data',
    python_callable=extract_market_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data_to_timescaledb',
    python_callable=load_data_to_timescaledb,
    dag=dag,
)

calculate_metrics_task = PythonOperator(
    task_id='calculate_portfolio_metrics',
    python_callable=calculate_portfolio_metrics,
    dag=dag,
)

# Data quality check
data_quality_check = PostgresOperator(
    task_id='data_quality_check',
    postgres_conn_id='timescaledb_conn',
    sql="""
    SELECT COUNT(*) as record_count 
    FROM market_data 
    WHERE timestamp >= NOW() - INTERVAL '1 day';
    """,
    dag=dag,
)

# Task dependencies
extract_task >> transform_task >> load_task >> calculate_metrics_task >> data_quality_check
