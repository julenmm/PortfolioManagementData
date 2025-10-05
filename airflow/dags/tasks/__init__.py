"""
Economic Data Update Tasks
"""

from .china_tasks import (
    update_china_manufacturing_pmi,
    update_china_interest_rates,
    update_china_consumer_price_index,
)

from .us_tasks import (
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

from .utils import (
    get_db_hook,
    get_last_date,
    log_update
)

__all__ = [
    # China tasks
    'update_china_manufacturing_pmi',
    'update_china_interest_rates', 
    'update_china_consumer_price_index',
    
    # US tasks
    'update_durable_goods',
    'update_employment_data',
    'update_industrial_production',
    'update_jobless_claims',
    'update_commodities_data',
    'update_eia_data',
    'update_cot_data',
    'update_yields_data',
    'update_inflation_data',
    'update_building_permits',
    'update_m2_money_supply',
    'update_usd_index',
    'update_ism_manufacturing',
    'update_ism_non_manufacturing',
    'update_nfib_small_business',
    'update_umcsi_consumer_sentiment',
    
    # Utils
    'get_db_hook',
    'get_last_date',
    'log_update'
]
