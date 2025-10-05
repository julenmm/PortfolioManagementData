"""
Economic Data Daily Update DAG
Fetches and updates economic indicators from various sources
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Import all tasks
from tasks import (
    # China tasks
    update_china_manufacturing_pmi,
    update_china_interest_rates,
    update_china_consumer_price_index,
    
    # US tasks
    update_durable_goods,
    update_employment_data,
    update_industrial_production,
    update_jobless_claims,
    update_commodities_data,
    update_eia_data,
    update_cot_data,
    update_yields_data,
    update_inflation_data,
    update_building_permits,
    update_m2_money_supply,
    update_usd_index,
    update_ism_manufacturing,
    update_ism_non_manufacturing,
    update_nfib_small_business,
    update_umcsi_consumer_sentiment
)


# Default arguments
default_args = {
    'owner': 'economic_data_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
dag = DAG(
    'economic_data_daily_update',
    default_args=default_args,
    description='Daily update of economic indicators from various sources',
    schedule_interval='0 6 * * *',  # Run daily at 6 AM UTC
    catchup=False,
    tags=['economic_data', 'daily', 'indicators'],
)


def start_pipeline(**context):
    """Start the economic data pipeline"""
    print(f"Starting economic data pipeline at {context['ds']}")
    return "Pipeline started successfully"


def end_pipeline(**context):
    """End the economic data pipeline"""
    print(f"Economic data pipeline completed at {context['ds']}")
    return "Pipeline completed successfully"


# Pipeline start and end tasks
start = PythonOperator(
    task_id='start',
    python_callable=start_pipeline,
    dag=dag,
)

end = PythonOperator(
    task_id='end',
    python_callable=end_pipeline,
    dag=dag,
)

# China economic data tasks
china_pmi = PythonOperator(
    task_id='update_china_manufacturing_pmi',
    python_callable=update_china_manufacturing_pmi,
    dag=dag,
)

china_rates = PythonOperator(
    task_id='update_china_interest_rates',
    python_callable=update_china_interest_rates,
    dag=dag,
)

china_cpi = PythonOperator(
    task_id='update_china_consumer_price_index',
    python_callable=update_china_consumer_price_index,
    dag=dag,
)
# US economic data tasks
durable_goods = PythonOperator(
    task_id='update_durable_goods',
    python_callable=update_durable_goods,
    dag=dag,
)

employment = PythonOperator(
    task_id='update_employment_data',
    python_callable=update_employment_data,
    dag=dag,
)

industrial_prod = PythonOperator(
    task_id='update_industrial_production',
    python_callable=update_industrial_production,
    dag=dag,
)

jobless = PythonOperator(
    task_id='update_jobless_claims',
    python_callable=update_jobless_claims,
    dag=dag,
)

commodities = PythonOperator(
    task_id='update_commodities_data',
    python_callable=update_commodities_data,
    dag=dag,
)

eia = PythonOperator(
    task_id='update_eia_data',
    python_callable=update_eia_data,
    dag=dag,
)

cot = PythonOperator(
    task_id='update_cot_data',
    python_callable=update_cot_data,
    dag=dag,
)

yields_task = PythonOperator(
    task_id='update_yields_data',
    python_callable=update_yields_data,
    dag=dag,
)

inflation = PythonOperator(
    task_id='update_inflation_data',
    python_callable=update_inflation_data,
    dag=dag,
)

permits = PythonOperator(
    task_id='update_building_permits',
    python_callable=update_building_permits,
    dag=dag,
)

m2 = PythonOperator(
    task_id='update_m2_money_supply',
    python_callable=update_m2_money_supply,
    dag=dag,
)

usd = PythonOperator(
    task_id='update_usd_index',
    python_callable=update_usd_index,
    dag=dag,
)

ism_mfg = PythonOperator(
    task_id='update_ism_manufacturing',
    python_callable=update_ism_manufacturing,
    dag=dag,
)

ism_nonmfg = PythonOperator(
    task_id='update_ism_non_manufacturing',
    python_callable=update_ism_non_manufacturing,
    dag=dag,
)

nfib = PythonOperator(
    task_id='update_nfib_small_business',
    python_callable=update_nfib_small_business,
    dag=dag,
)

umcsi_task = PythonOperator(
    task_id='update_umcsi_consumer_sentiment',
    python_callable=update_umcsi_consumer_sentiment,
    dag=dag,
)

# Task dependencies
start >> [
    china_pmi, china_rates, china_cpi,
    durable_goods, employment, industrial_prod, jobless,
    commodities, eia, cot,
    yields_task,
    inflation, permits, m2, usd,
    ism_mfg, ism_nonmfg, nfib, umcsi_task
] >> end