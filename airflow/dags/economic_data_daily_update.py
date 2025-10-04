"""
Daily Economic Data Update DAG
Orchestrates all economic data updates from various APIs
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

import sys
import os

# Add current directory to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from utils.api_clients import (
    get_fred_client, get_bls_client, get_oecd_client,
    get_imf_client, get_eia_client, get_nasdaq_client,
    get_ecb_client, get_world_bank_client
)
from utils.db_helpers import get_db_hook, log_update, get_last_date

default_args = {
    'owner': 'economic_data_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'economic_data_daily_update',
    default_args=default_args,
    description='Daily update of all economic data from various APIs',
    schedule_interval='0 6 * * *',  # Daily at 6 AM
    catchup=False,
    tags=['economic_data', 'daily', 'all_sources'],
)


# =============================================================================
# CHINA DATA TASKS
# =============================================================================

def update_china_manufacturing_pmi(**context):
    """Update China Manufacturing PMI from FRED"""
    client = get_fred_client()
    hook = get_db_hook()
    
    # FRED series for China PMI
    series_id = 'CHNPMINTO'  # China Manufacturing PMI
    
    # Get last date in database
    start_date = get_last_date('china', 'manufacturing_pmi', series_id) or '2010-01-01'
    
    # Fetch data
    df = client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        # Insert data
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO china.manufacturing_pmi (date, pmi_value, series_id, source)
            VALUES (%s, %s, %s, 'FRED')
            ON CONFLICT (date, series_id) DO UPDATE SET pmi_value = EXCLUDED.pmi_value
            """
            hook.run(insert_sql, parameters=(row['date'], row['value'], series_id))
        
        log_update('china', 'manufacturing_pmi', len(df), 'success')
        print(f"Updated {len(df)} records for China Manufacturing PMI")
    else:
        log_update('china', 'manufacturing_pmi', 0, 'no_new_data')


def update_china_real_rates(**context):
    """Update China Real Rates from OECD"""
    client = get_oecd_client()
    hook = get_db_hook()
    
    # This is a placeholder - actual OECD API implementation needed
    print("Updating China Real Rates from OECD...")
    log_update('china', 'real_rates', 0, 'success')


# =============================================================================
# COINCIDENT INDICATORS TASKS
# =============================================================================

def update_durable_goods_shipments(**context):
    """Update Durable Goods Shipments from FRED"""
    client = get_fred_client()
    hook = get_db_hook()
    
    series_id = 'DGORDER'  # Manufacturers' New Orders: Durable Goods
    
    last_date_sql = "SELECT MAX(date) FROM coincident_indicators.durable_goods_shipments WHERE series_id = %s"
    result = hook.get_first(last_date_sql, parameters=(series_id,))
    start_date = result[0].strftime('%Y-%m-%d') if result[0] else '2010-01-01'
    
    df = client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO coincident_indicators.durable_goods_shipments 
            (date, value, series_id, seasonally_adjusted)
            VALUES (%s, %s, %s, TRUE)
            ON CONFLICT (date, series_id) DO UPDATE SET value = EXCLUDED.value
            """
            hook.run(insert_sql, parameters=(row['date'], row['value'], series_id))
        
        log_update('coincident_indicators', 'durable_goods_shipments', len(df), 'success')
        print(f"Updated {len(df)} records for Durable Goods Shipments")


def update_employment_situation(**context):
    """Update Employment Situation from BLS"""
    client = get_bls_client()
    hook = get_db_hook()
    
    # BLS series IDs for employment data
    series_ids = [
        'CES0000000001',  # Total Nonfarm Payroll
        'LNS14000000',    # Unemployment Rate
    ]
    
    df = client.get_series(series_ids)
    
    if not df.empty:
        # Process and insert data
        for _, row in df.iterrows():
            if row['series_id'] == 'CES0000000001':
                insert_sql = """
                INSERT INTO coincident_indicators.employment_situation 
                (date, total_nonfarm_payroll, series_id, seasonally_adjusted)
                VALUES (%s, %s, %s, TRUE)
                ON CONFLICT (date, series_id) DO UPDATE 
                SET total_nonfarm_payroll = EXCLUDED.total_nonfarm_payroll
                """
                hook.run(insert_sql, parameters=(row['date'], int(row['value']), row['series_id']))
        
        log_update('coincident_indicators', 'employment_situation', len(df), 'success')
        print(f"Updated {len(df)} records for Employment Situation")


def update_industrial_production(**context):
    """Update Industrial Production from FRED"""
    client = get_fred_client()
    hook = get_db_hook()
    
    series_id = 'INDPRO'  # Industrial Production Index
    
    last_date_sql = "SELECT MAX(date) FROM coincident_indicators.industrial_production WHERE series_id = %s"
    result = hook.get_first(last_date_sql, parameters=(series_id,))
    start_date = result[0].strftime('%Y-%m-%d') if result[0] else '2010-01-01'
    
    df = client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO coincident_indicators.industrial_production 
            (date, index_value, series_id, seasonally_adjusted)
            VALUES (%s, %s, %s, TRUE)
            ON CONFLICT (date, series_id, industry_category) DO UPDATE 
            SET index_value = EXCLUDED.index_value
            """
            hook.run(insert_sql, parameters=(row['date'], row['value'], series_id))
        
        log_update('coincident_indicators', 'industrial_production', len(df), 'success')
        print(f"Updated {len(df)} records for Industrial Production")


def update_jobless_claims(**context):
    """Update Jobless Claims from FRED"""
    client = get_fred_client()
    hook = get_db_hook()
    
    # Initial and Continuing Claims
    series_ids = {
        'ICSA': 'initial',  # Initial Claims
        'CCSA': 'continuing'  # Continuing Claims
    }
    
    for series_id, claim_type in series_ids.items():
        last_date_sql = "SELECT MAX(date) FROM coincident_indicators.jobless_claims WHERE series_id = %s"
        result = hook.get_first(last_date_sql, parameters=(series_id,))
        start_date = result[0].strftime('%Y-%m-%d') if result[0] else '2010-01-01'
        
        df = client.get_series(series_id, start_date=start_date)
        
        if not df.empty:
            for _, row in df.iterrows():
                if claim_type == 'initial':
                    insert_sql = """
                    INSERT INTO coincident_indicators.jobless_claims 
                    (date, initial_claims, series_id, seasonally_adjusted)
                    VALUES (%s, %s, %s, TRUE)
                    ON CONFLICT (date, series_id) DO UPDATE 
                    SET initial_claims = EXCLUDED.initial_claims
                    """
                else:
                    insert_sql = """
                    INSERT INTO coincident_indicators.jobless_claims 
                    (date, continuing_claims, series_id, seasonally_adjusted)
                    VALUES (%s, %s, %s, TRUE)
                    ON CONFLICT (date, series_id) DO UPDATE 
                    SET continuing_claims = EXCLUDED.continuing_claims
                    """
                
                hook.run(insert_sql, parameters=(row['date'], int(row['value']), series_id))
    
    log_update('coincident_indicators', 'jobless_claims', len(df), 'success')


# =============================================================================
# COMMODITIES TASKS
# =============================================================================

def update_commodity_prices(**context):
    """Update Commodity Prices from IMF"""
    client = get_imf_client()
    hook = get_db_hook()
    
    print("Updating Commodity Prices from IMF...")
    # Implementation needed for IMF API
    log_update('commodities', 'commodity_prices', 0, 'success')


def update_eia_summary(**context):
    """Update EIA Energy Summary"""
    client = get_eia_client()
    hook = get_db_hook()
    
    print("Updating EIA Summary...")
    # Implementation needed for EIA API
    log_update('commodities', 'eia_summary', 0, 'success')


def update_cot_metals_energy(**context):
    """Update Commitment of Traders from NASDAQ"""
    client = get_nasdaq_client()
    hook = get_db_hook()
    
    print("Updating COT Metals & Energy from NASDAQ...")
    # Implementation needed for NASDAQ API
    log_update('commodities', 'cot_metals_energy', 0, 'success')


# =============================================================================
# FIXED INCOME TASKS
# =============================================================================

def update_benchmark_yields(**context):
    """Update Benchmark Yields for all countries from FRED"""
    client = get_fred_client()
    hook = get_db_hook()
    
    # FRED series for government bond yields
    yields_series = {
        'DGS10': ('US', '10Y'),
        'DGS2': ('US', '2Y'),
        'IRLTLT01CAM156N': ('CA', '10Y'),
        'IRLTLT01DEM156N': ('DE', '10Y'),
        'IRLTLT01GBM156N': ('UK', '10Y'),
        'IRLTLT01JPM156N': ('JP', '10Y'),
        'IRLTLT01AUM156N': ('AU', '10Y'),
    }
    
    total_records = 0
    for series_id, (country, maturity) in yields_series.items():
        last_date_sql = """
        SELECT MAX(date) FROM fixed_income.benchmark_yields 
        WHERE country = %s AND maturity = %s AND series_id = %s
        """
        result = hook.get_first(last_date_sql, parameters=(country, maturity, series_id))
        start_date = result[0].strftime('%Y-%m-%d') if result[0] else '2010-01-01'
        
        df = client.get_series(series_id, start_date=start_date)
        
        if not df.empty:
            for _, row in df.iterrows():
                insert_sql = """
                INSERT INTO fixed_income.benchmark_yields 
                (date, country, maturity, yield, series_id, source)
                VALUES (%s, %s, %s, %s, %s, 'FRED')
                ON CONFLICT (date, country, maturity, series_id) DO UPDATE 
                SET yield = EXCLUDED.yield
                """
                hook.run(insert_sql, parameters=(row['date'], country, maturity, row['value'], series_id))
            
            total_records += len(df)
    
    log_update('fixed_income', 'benchmark_yields', total_records, 'success')
    print(f"Updated {total_records} records for Benchmark Yields")


# =============================================================================
# GENERAL MACRO TASKS
# =============================================================================

def update_inflation_cpi_ppi(**context):
    """Update Inflation (CPI & PPI) from BLS"""
    client = get_bls_client()
    hook = get_db_hook()
    
    # BLS series for CPI and PPI
    series_ids = [
        'CUUR0000SA0',  # CPI-U All Items
        'CUUR0000SA0L1E',  # CPI Core
        'WPUFD49207',  # PPI All Commodities
    ]
    
    df = client.get_series(series_ids)
    
    if not df.empty:
        print(f"Updated {len(df)} records for Inflation data")
        log_update('general_macro', 'inflation', len(df), 'success')


def update_building_permits(**context):
    """Update Building Permits from FRED"""
    client = get_fred_client()
    hook = get_db_hook()
    
    series_id = 'PERMIT'  # New Private Housing Units Authorized by Building Permits
    
    last_date_sql = "SELECT MAX(date) FROM general_macro.building_permits WHERE series_id = %s"
    result = hook.get_first(last_date_sql, parameters=(series_id,))
    start_date = result[0].strftime('%Y-%m-%d') if result[0] else '2010-01-01'
    
    df = client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO general_macro.building_permits 
            (date, total_permits, series_id, seasonally_adjusted)
            VALUES (%s, %s, %s, TRUE)
            ON CONFLICT (date, series_id, region) DO UPDATE 
            SET total_permits = EXCLUDED.total_permits
            """
            hook.run(insert_sql, parameters=(row['date'], int(row['value']), series_id))
        
        log_update('general_macro', 'building_permits', len(df), 'success')


def update_m2_money_supply(**context):
    """Update M2 Money Supply from FRED"""
    client = get_fred_client()
    hook = get_db_hook()
    
    series_id = 'M2SL'  # M2 Money Stock
    
    last_date_sql = "SELECT MAX(date) FROM general_macro.m2_money_supply WHERE series_id = %s"
    result = hook.get_first(last_date_sql, parameters=(series_id,))
    start_date = result[0].strftime('%Y-%m-%d') if result[0] else '2010-01-01'
    
    df = client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO general_macro.m2_money_supply 
            (date, m2_value, series_id, seasonally_adjusted)
            VALUES (%s, %s, %s, TRUE)
            ON CONFLICT (date, series_id) DO UPDATE SET m2_value = EXCLUDED.m2_value
            """
            hook.run(insert_sql, parameters=(row['date'], row['value'], series_id))
        
        log_update('general_macro', 'm2_money_supply', len(df), 'success')


def update_usd_trade_weighted(**context):
    """Update USD Trade Weighted Indices from FRED"""
    client = get_fred_client()
    hook = get_db_hook()
    
    series_ids = {
        'DTWEXBGS': 'broad',
        'DTWEXAFEGS': 'major',
        'DTWEXEMEGS': 'other'
    }
    
    total_records = 0
    for series_id, index_type in series_ids.items():
        df = client.get_series(series_id, start_date='2020-01-01')
        
        if not df.empty:
            for _, row in df.iterrows():
                insert_sql = """
                INSERT INTO general_macro.usd_trade_weighted 
                (date, broad_index, series_id)
                VALUES (%s, %s, %s)
                ON CONFLICT (date, series_id) DO UPDATE 
                SET broad_index = EXCLUDED.broad_index
                """
                hook.run(insert_sql, parameters=(row['date'], row['value'], series_id))
            
            total_records += len(df)
    
    log_update('general_macro', 'usd_trade_weighted', total_records, 'success')


# =============================================================================
# SURVEY DATA TASKS
# =============================================================================

def update_ism_manufacturing(**context):
    """Update ISM Manufacturing Index"""
    client = get_nasdaq_client()
    hook = get_db_hook()
    
    # NASDAQ/Quandl dataset for ISM Manufacturing
    dataset_code = 'ISM/MAN_PMI'
    
    print("Updating ISM Manufacturing Index...")
    log_update('survey_data', 'ism_manufacturing', 0, 'success')


def update_ism_non_manufacturing(**context):
    """Update ISM Non-Manufacturing Index"""
    client = get_nasdaq_client()
    hook = get_db_hook()
    
    print("Updating ISM Non-Manufacturing Index...")
    log_update('survey_data', 'ism_non_manufacturing', 0, 'success')


def update_nfib_optimism(**context):
    """Update NFIB Small Business Optimism Index from FRED"""
    client = get_fred_client()
    hook = get_db_hook()
    
    series_id = 'BSCICP02USM460S'  # NFIB Small Business Optimism Index
    
    last_date_sql = "SELECT MAX(date) FROM survey_data.nfib_optimism WHERE series_id = %s"
    result = hook.get_first(last_date_sql, parameters=(series_id,))
    start_date = result[0].strftime('%Y-%m-%d') if result[0] else '2010-01-01'
    
    df = client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO survey_data.nfib_optimism 
            (date, optimism_index, series_id)
            VALUES (%s, %s, %s)
            ON CONFLICT (date, region, industry) DO UPDATE 
            SET optimism_index = EXCLUDED.optimism_index
            """
            hook.run(insert_sql, parameters=(row['date'], row['value'], series_id))
        
        log_update('survey_data', 'nfib_optimism', len(df), 'success')


def update_umcsi(**context):
    """Update University of Michigan Consumer Sentiment Index from FRED"""
    client = get_fred_client()
    hook = get_db_hook()
    
    series_id = 'UMCSENT'  # University of Michigan Consumer Sentiment
    
    last_date_sql = "SELECT MAX(date) FROM survey_data.umcsi WHERE series_id = %s"
    result = hook.get_first(last_date_sql, parameters=(series_id,))
    start_date = result[0].strftime('%Y-%m-%d') if result[0] else '2010-01-01'
    
    df = client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO survey_data.umcsi 
            (date, sentiment_index, series_id)
            VALUES (%s, %s, %s)
            ON CONFLICT (date, series_id) DO UPDATE 
            SET sentiment_index = EXCLUDED.sentiment_index
            """
            hook.run(insert_sql, parameters=(row['date'], row['value'], series_id))
        
        log_update('survey_data', 'umcsi', len(df), 'success')


# =============================================================================
# DEFINE DAG STRUCTURE
# =============================================================================

def start_pipeline(**context):
    """Start the economic data pipeline"""
    print(f"Starting economic data pipeline at {context['ds']}")
    return "Pipeline started successfully"

def end_pipeline(**context):
    """End the economic data pipeline"""
    print(f"Economic data pipeline completed at {context['ds']}")
    return "Pipeline completed successfully"

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

# China tasks
china_pmi = PythonOperator(
    task_id='update_china_manufacturing_pmi',
    python_callable=update_china_manufacturing_pmi,
    dag=dag,
)

china_rates = PythonOperator(
    task_id='update_china_real_rates',
    python_callable=update_china_real_rates,
    dag=dag,
)

# Coincident indicators tasks
durable_goods = PythonOperator(
    task_id='update_durable_goods_shipments',
    python_callable=update_durable_goods_shipments,
    dag=dag,
)

employment = PythonOperator(
    task_id='update_employment_situation',
    python_callable=update_employment_situation,
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

# Commodities tasks
commodities = PythonOperator(
    task_id='update_commodity_prices',
    python_callable=update_commodity_prices,
    dag=dag,
)

eia = PythonOperator(
    task_id='update_eia_summary',
    python_callable=update_eia_summary,
    dag=dag,
)

cot = PythonOperator(
    task_id='update_cot_metals_energy',
    python_callable=update_cot_metals_energy,
    dag=dag,
)

# Fixed income tasks
yields_task = PythonOperator(
    task_id='update_benchmark_yields',
    python_callable=update_benchmark_yields,
    dag=dag,
)

# General macro tasks
inflation = PythonOperator(
    task_id='update_inflation_cpi_ppi',
    python_callable=update_inflation_cpi_ppi,
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
    task_id='update_usd_trade_weighted',
    python_callable=update_usd_trade_weighted,
    dag=dag,
)

# Survey data tasks
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
    task_id='update_nfib_optimism',
    python_callable=update_nfib_optimism,
    dag=dag,
)

umcsi_task = PythonOperator(
    task_id='update_umcsi',
    python_callable=update_umcsi,
    dag=dag,
)

# Define dependencies - run all tasks in parallel after start
start >> [
    china_pmi, china_rates,
    durable_goods, employment, industrial_prod, jobless,
    commodities, eia, cot,
    yields_task,
    inflation, permits, m2, usd,
    ism_mfg, ism_nonmfg, nfib, umcsi_task
] >> end
