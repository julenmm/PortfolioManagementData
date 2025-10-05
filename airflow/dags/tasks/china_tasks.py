"""
China Economic Data Update Tasks
"""

from api_clients import get_fred_client
from .utils import get_db_hook, get_last_date, log_update


def update_china_manufacturing_pmi(**context):
    """Update China Manufacturing PMI from FRED"""
    fred_client = get_fred_client()
    hook = get_db_hook()
    
    # FRED series ID for China Manufacturing PMI
    series_id = 'CHNPMI'
    start_date = '1900-01-01'
    
    df = fred_client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO china.manufacturing_pmi (date, pmi_value, series_id, source)
            VALUES (%s, %s, %s, 'FRED')
            ON CONFLICT (date, series_id) DO UPDATE SET pmi_value = EXCLUDED.pmi_value
            """
            hook.run(insert_sql, parameters=(row['date'], row['value'], series_id))
        
        log_update('china', 'manufacturing_pmi', len(df), 'success')
        print(f"Updated {len(df)} records for China Manufacturing PMI from FRED")
    else:
        log_update('china', 'manufacturing_pmi', 0, 'no_data')
        print("No data available for China Manufacturing PMI from FRED")

""" china non manufacturing pmi FRED CHNNSAMN
"""


def update_china_interest_rates(**context):
    """Update China real rates from FRED"""
    """The overnight rate for banks lending to each other, reflecting short-term market liquidity.
    """
    fred_client = get_fred_client()
    hook = get_db_hook()
    
    # FRED series ID for China Interest Rate
    series_id = 'IRSTCI01CNM156N'
    start_date = '1900-01-01'
    
    df = fred_client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO china.real_rates (date, real_rate, series_id, source)
            VALUES (%s, %s, %s, 'FRED')
            ON CONFLICT (date, series_id) DO UPDATE SET real_rate = EXCLUDED.real_rate
            """
            hook.run(insert_sql, parameters=(row['date'], row['value'], series_id))
        
        log_update('china', 'real_rates', len(df), 'success')
        print(f"Updated {len(df)} records for China Real Rates from FRED")
    else:
        log_update('china', 'real_rates', 0, 'no_data')
        print("No data available for China Real Rates from FRED")
    

def update_china_consumer_price_index(**context):
    """Update China Consumer Price Index from FRED"""
    fred_client = get_fred_client()
    hook = get_db_hook()
    
    # FRED series ID for China Consumer Price Index
    series_id = 'CHNCPALTT01IXOBM'
    start_date = '1900-01-01'
    
    df = fred_client.get_series(series_id, start_date=start_date)
    
    if not df.empty:
        for _, row in df.iterrows():
            insert_sql = """
            INSERT INTO china.consumer_price_index (date, cpi_value, series_id, source)
            VALUES (%s, %s, %s, 'FRED')
            ON CONFLICT (date, series_id) DO UPDATE SET cpi_value = EXCLUDED.cpi_value
            """
            hook.run(insert_sql, parameters=(row['date'], row['value'], series_id))
        
        log_update('china', 'consumer_price_index', len(df), 'success')
        print(f"Updated {len(df)} records for China Consumer Price Index from FRED")
    else:
        log_update('china', 'consumer_price_index', 0, 'no_data')
        print("No data available for China Consumer Price Index from FRED")