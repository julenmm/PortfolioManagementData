"""
US Economic Data Update Tasks
"""

from api_clients import get_fred_client
from .utils import get_db_hook, get_last_date, log_update


def update_durable_goods(**context):
    """Update US Durable Goods Shipments from FRED"""
    fred_client = get_fred_client()
    hook = get_db_hook()
    
    series_id = 'DGORDER'  # Manufacturers' New Orders: Durable Goods
    
    start_date = get_last_date('coincident_indicators', 'durable_goods_shipments', series_id) or '2010-01-01'
    
    df = fred_client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO coincident_indicators.durable_goods_shipments (date, shipment_value, series_id, source)
            VALUES (%s, %s, %s, 'FRED')
            ON CONFLICT (date, series_id) DO UPDATE SET shipment_value = EXCLUDED.shipment_value
            """
            hook.run(insert_sql, parameters=(row['date'], row['value'], series_id))
        
        log_update('coincident_indicators', 'durable_goods_shipments', len(df), 'success')
        print(f"Updated {len(df)} records for Durable Goods Shipments")
    else:
        log_update('coincident_indicators', 'durable_goods_shipments', 0, 'no_data')
        print("No data available for Durable Goods Shipments")


def update_employment_data(**context):
    """Update US Employment Data from FRED"""
    fred_client = get_fred_client()
    hook = get_db_hook()
    
    series_id = 'PAYEMS'  # All Employees, Total Nonfarm
    
    start_date = get_last_date('coincident_indicators', 'employment_situation', series_id) or '2010-01-01'
    
    df = fred_client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO coincident_indicators.employment_situation (date, employment_value, series_id, source)
            VALUES (%s, %s, %s, 'FRED')
            ON CONFLICT (date, series_id) DO UPDATE SET employment_value = EXCLUDED.employment_value
            """
            hook.run(insert_sql, parameters=(row['date'], row['value'], series_id))
        
        log_update('coincident_indicators', 'employment_situation', len(df), 'success')
        print(f"Updated {len(df)} records for Employment Data")
    else:
        log_update('coincident_indicators', 'employment_situation', 0, 'no_data')
        print("No data available for Employment Data")


def update_industrial_production(**context):
    """Update US Industrial Production from FRED"""
    fred_client = get_fred_client()
    hook = get_db_hook()
    
    series_id = 'INDPRO'  # Industrial Production Index
    
    start_date = get_last_date('coincident_indicators', 'industrial_production', series_id) or '2010-01-01'
    
    df = fred_client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO coincident_indicators.industrial_production
            (date, index_value, series_id, industry_category, seasonally_adjusted)
            VALUES (%s, %s, %s, %s, TRUE)
            ON CONFLICT (date, series_id, industry_category) DO UPDATE
            SET index_value = EXCLUDED.index_value
            """
            hook.run(insert_sql, parameters=(row['date'], row['value'], series_id, 'Total'))
        
        log_update('coincident_indicators', 'industrial_production', len(df), 'success')
        print(f"Updated {len(df)} records for Industrial Production")
    else:
        log_update('coincident_indicators', 'industrial_production', 0, 'no_data')
        print("No data available for Industrial Production")


def update_jobless_claims(**context):
    """Update US Jobless Claims from FRED"""
    fred_client = get_fred_client()
    hook = get_db_hook()
    
    series_id = 'ICSA'  # Initial Claims
    
    start_date = get_last_date('coincident_indicators', 'jobless_claims', series_id) or '2010-01-01'
    
    df = fred_client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO coincident_indicators.jobless_claims (date, initial_claims, series_id, seasonally_adjusted)
            VALUES (%s, %s, %s, TRUE)
            ON CONFLICT (date, series_id) DO UPDATE SET initial_claims = EXCLUDED.initial_claims
            """
            hook.run(insert_sql, parameters=(row['date'], row['value'], series_id))
        
        log_update('coincident_indicators', 'jobless_claims', len(df), 'success')
        print(f"Updated {len(df)} records for Jobless Claims")
    else:
        log_update('coincident_indicators', 'jobless_claims', 0, 'no_data')
        print("No data available for Jobless Claims")


def update_commodities_data(**context):
    """Update Commodities Data from FRED"""
    fred_client = get_fred_client()
    hook = get_db_hook()
    
    series_id = 'GOLDAMGBD228NLBM'  # Gold Price
    
    start_date = get_last_date('commodities', 'commodity_prices', series_id) or '2010-01-01'
    
    df = fred_client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO commodities.commodity_prices (date, commodity_name, price, series_id, source)
            VALUES (%s, %s, %s, %s, 'FRED')
            ON CONFLICT (date, commodity_name, series_id) DO UPDATE SET price = EXCLUDED.price
            """
            hook.run(insert_sql, parameters=(row['date'], 'Gold', row['value'], series_id))
        
        log_update('commodities', 'commodity_prices', len(df), 'success')
        print(f"Updated {len(df)} records for Gold Price")
    else:
        log_update('commodities', 'commodity_prices', 0, 'no_data')
        print("No data available for Gold Price")


def update_eia_data(**context):
    """Update EIA Energy Data"""
    # Placeholder for EIA data updates
    print("EIA data update not implemented yet")


def update_cot_data(**context):
    """Update COT (Commitment of Traders) Data"""
    # Placeholder for COT data updates
    print("COT data update not implemented yet")


def update_yields_data(**context):
    """Update US Treasury Yields from FRED"""
    fred_client = get_fred_client()
    hook = get_db_hook()
    
    series_id = 'DGS10'  # 10-Year Treasury Constant Maturity Rate
    
    start_date = get_last_date('fixed_income', 'benchmark_yields', series_id) or '2010-01-01'
    
    df = fred_client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO fixed_income.benchmark_yields (date, country, maturity, yield, series_id, source)
            VALUES (%s, %s, %s, %s, %s, 'FRED')
            ON CONFLICT (date, country, maturity, series_id) DO UPDATE SET yield = EXCLUDED.yield
            """
            hook.run(insert_sql, parameters=(row['date'], 'US', '10Y', row['value'], series_id))
        
        log_update('fixed_income', 'benchmark_yields', len(df), 'success')
        print(f"Updated {len(df)} records for 10-Year Treasury Yield")
    else:
        log_update('fixed_income', 'benchmark_yields', 0, 'no_data')
        print("No data available for 10-Year Treasury Yield")


def update_inflation_data(**context):
    """Update US Inflation Data from FRED"""
    fred_client = get_fred_client()
    hook = get_db_hook()
    
    series_id = 'CPIAUCSL'  # Consumer Price Index for All Urban Consumers
    
    start_date = get_last_date('general_macro', 'inflation', series_id) or '2010-01-01'
    
    df = fred_client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO general_macro.inflation (date, cpi_all_items, series_id, source)
            VALUES (%s, %s, %s, 'FRED')
            ON CONFLICT (date, series_id) DO UPDATE SET cpi_all_items = EXCLUDED.cpi_all_items
            """
            hook.run(insert_sql, parameters=(row['date'], row['value'], series_id))
        
        log_update('general_macro', 'inflation', len(df), 'success')
        print(f"Updated {len(df)} records for CPI")
    else:
        log_update('general_macro', 'inflation', 0, 'no_data')
        print("No data available for CPI")


def update_building_permits(**context):
    """Update US Building Permits from FRED"""
    fred_client = get_fred_client()
    hook = get_db_hook()
    
    series_id = 'PERMIT'  # New Private Housing Units Authorized by Building Permits
    
    start_date = get_last_date('general_macro', 'building_permits', series_id) or '2010-01-01'
    
    df = fred_client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO general_macro.building_permits (date, total_permits, series_id, source)
            VALUES (%s, %s, %s, 'FRED')
            ON CONFLICT (date, series_id) DO UPDATE SET total_permits = EXCLUDED.total_permits
            """
            hook.run(insert_sql, parameters=(row['date'], row['value'], series_id))
        
        log_update('general_macro', 'building_permits', len(df), 'success')
        print(f"Updated {len(df)} records for Building Permits")
    else:
        log_update('general_macro', 'building_permits', 0, 'no_data')
        print("No data available for Building Permits")


def update_m2_money_supply(**context):
    """Update US M2 Money Supply from FRED"""
    fred_client = get_fred_client()
    hook = get_db_hook()
    
    series_id = 'M2SL'  # M2 Money Stock
    
    start_date = get_last_date('general_macro', 'm2_money_supply', series_id) or '2010-01-01'
    
    df = fred_client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO general_macro.m2_money_supply (date, m2_value, series_id, seasonally_adjusted)
            VALUES (%s, %s, %s, TRUE)
            ON CONFLICT (date, series_id) DO UPDATE SET m2_value = EXCLUDED.m2_value
            """
            hook.run(insert_sql, parameters=(row['date'], row['value'], series_id))
        
        log_update('general_macro', 'm2_money_supply', len(df), 'success')
        print(f"Updated {len(df)} records for M2 Money Supply")
    else:
        log_update('general_macro', 'm2_money_supply', 0, 'no_data')
        print("No data available for M2 Money Supply")


def update_usd_index(**context):
    """Update US Dollar Index from FRED"""
    fred_client = get_fred_client()
    hook = get_db_hook()
    
    series_id = 'DTWEXBGS'  # Trade Weighted U.S. Dollar Index
    
    start_date = get_last_date('general_macro', 'usd_trade_weighted', series_id) or '2010-01-01'
    
    df = fred_client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO general_macro.usd_trade_weighted (date, broad_index, series_id, source)
            VALUES (%s, %s, %s, 'FRED')
            ON CONFLICT (date, series_id) DO UPDATE SET broad_index = EXCLUDED.broad_index
            """
            hook.run(insert_sql, parameters=(row['date'], row['value'], series_id))
        
        log_update('general_macro', 'usd_trade_weighted', len(df), 'success')
        print(f"Updated {len(df)} records for USD Index")
    else:
        log_update('general_macro', 'usd_trade_weighted', 0, 'no_data')
        print("No data available for USD Index")


def update_ism_manufacturing(**context):
    """Update ISM Manufacturing PMI from FRED"""
    fred_client = get_fred_client()
    hook = get_db_hook()
    
    series_id = 'NAPM'  # ISM Manufacturing PMI
    
    start_date = get_last_date('survey_data', 'ism_manufacturing', series_id) or '2010-01-01'
    
    df = fred_client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO survey_data.ism_manufacturing (date, pmi, series_id, source)
            VALUES (%s, %s, %s, 'FRED')
            ON CONFLICT (date) DO UPDATE SET pmi = EXCLUDED.pmi
            """
            hook.run(insert_sql, parameters=(row['date'], row['value'], series_id))
        
        log_update('survey_data', 'ism_manufacturing', len(df), 'success')
        print(f"Updated {len(df)} records for ISM Manufacturing PMI")
    else:
        log_update('survey_data', 'ism_manufacturing', 0, 'no_data')
        print("No data available for ISM Manufacturing PMI")


def update_ism_non_manufacturing(**context):
    """Update ISM Non-Manufacturing PMI from FRED"""
    fred_client = get_fred_client()
    hook = get_db_hook()
    
    series_id = 'NONREVSL'  # ISM Non-Manufacturing PMI
    
    start_date = get_last_date('survey_data', 'ism_non_manufacturing', series_id) or '2010-01-01'
    
    df = fred_client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO survey_data.ism_non_manufacturing (date, nmi, series_id, source)
            VALUES (%s, %s, %s, 'FRED')
            ON CONFLICT (date) DO UPDATE SET nmi = EXCLUDED.nmi
            """
            hook.run(insert_sql, parameters=(row['date'], row['value'], series_id))
        
        log_update('survey_data', 'ism_non_manufacturing', len(df), 'success')
        print(f"Updated {len(df)} records for ISM Non-Manufacturing PMI")
    else:
        log_update('survey_data', 'ism_non_manufacturing', 0, 'no_data')
        print("No data available for ISM Non-Manufacturing PMI")


def update_nfib_small_business(**context):
    """Update NFIB Small Business Optimism Index from FRED"""
    fred_client = get_fred_client()
    hook = get_db_hook()
    
    series_id = 'NFIB'  # NFIB Small Business Optimism Index
    
    start_date = get_last_date('survey_data', 'nfib_optimism', series_id) or '2010-01-01'
    
    df = fred_client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO survey_data.nfib_optimism (date, optimism_index, series_id, source)
            VALUES (%s, %s, %s, 'FRED')
            ON CONFLICT (date, series_id) DO UPDATE SET optimism_index = EXCLUDED.optimism_index
            """
            hook.run(insert_sql, parameters=(row['date'], row['value'], series_id))
        
        log_update('survey_data', 'nfib_optimism', len(df), 'success')
        print(f"Updated {len(df)} records for NFIB Small Business Optimism")
    else:
        log_update('survey_data', 'nfib_optimism', 0, 'no_data')
        print("No data available for NFIB Small Business Optimism")


def update_umcsi_consumer_sentiment(**context):
    """Update University of Michigan Consumer Sentiment Index from FRED"""
    fred_client = get_fred_client()
    hook = get_db_hook()
    
    series_id = 'UMCSENT'  # University of Michigan: Consumer Sentiment
    
    start_date = get_last_date('survey_data', 'umcsi', series_id) or '2010-01-01'
    
    df = fred_client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO survey_data.umcsi (date, sentiment_index, series_id, source)
            VALUES (%s, %s, %s, 'FRED')
            ON CONFLICT (date, series_id) DO UPDATE SET sentiment_index = EXCLUDED.sentiment_index
            """
            hook.run(insert_sql, parameters=(row['date'], row['value'], series_id))
        
        log_update('survey_data', 'umcsi', len(df), 'success')
        print(f"Updated {len(df)} records for UMCSI Consumer Sentiment")
    else:
        log_update('survey_data', 'umcsi', 0, 'no_data')
        print("No data available for UMCSI Consumer Sentiment")
