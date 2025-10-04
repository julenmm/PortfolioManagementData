# Economic Data Pipeline DAGs

## Overview

This folder contains Apache Airflow DAGs for automatically fetching and updating economic data from various APIs into the TimescaleDB warehouse.

## Main DAG: `economic_data_daily_update.py`

**Schedule**: Daily at 6:00 AM  
**Purpose**: Fetch and update all economic indicators from multiple data sources

### Data Sources Covered

#### 🇨🇳 China
- Manufacturing PMI (FRED)
- Real Interest Rates (OECD)

#### 📈 Coincident Indicators
- Durable Goods Shipments (FRED)
- Employment Situation Report (BLS)
- Industrial Production (FRED)
- Jobless Claims - Initial & Continuing (FRED)

#### 🛢️ Commodities
- Commitment of Traders - Metals & Energy (NASDAQ)
- Commodity Prices (IMF)
- EIA Energy Summary (EIA)

#### 💸 Fixed Income
- Benchmark Yields for: US, CA, DE, UK, JP, AU (FRED)
- Corporate Bond Indices (FRED)

#### 📊 General Macro
- Inflation - CPI & PPI (BLS)
- Building Permits (FRED)
- M2 Money Supply (FRED)
- USD Trade Weighted Indices (FRED)

#### 📋 Survey Data
- ISM Manufacturing Index (NASDAQ/ISM)
- ISM Non-Manufacturing Index (NASDAQ/ISM)
- NFIB Small Business Optimism (FRED)
- University of Michigan Consumer Sentiment (FRED)

## Configuration

### Required API Keys

Set the following in your `.env` file:

```env
# FRED
FRED_API_KEY=your_key_here

# BLS
BLS_API_KEY=your_key_here

# EIA
EIA_API_KEY=your_key_here

# NASDAQ Data Link
NASDAQ_API_KEY=your_key_here

# Alpha Vantage (optional backup)
ALPHA_VANTAGE_API_KEY=your_key_here
```

### Getting API Keys

1. **FRED**: https://fred.stlouisfed.org/docs/api/api_key.html
2. **BLS**: https://www.bls.gov/developers/home.htm
3. **EIA**: https://www.eia.gov/opendata/register.php
4. **NASDAQ Data Link**: https://data.nasdaq.com/sign-up
5. **OECD**: No key required for basic access
6. **IMF**: No key required
7. **ECB**: No key required
8. **World Bank**: No key required

## DAG Structure

```
start
  ├── China Tasks (parallel)
  │   ├── update_china_manufacturing_pmi
  │   └── update_china_real_rates
  │
  ├── Coincident Indicators (parallel)
  │   ├── update_durable_goods_shipments
  │   ├── update_employment_situation
  │   ├── update_industrial_production
  │   └── update_jobless_claims
  │
  ├── Commodities (parallel)
  │   ├── update_commodity_prices
  │   ├── update_eia_summary
  │   └── update_cot_metals_energy
  │
  ├── Fixed Income (parallel)
  │   └── update_benchmark_yields
  │
  ├── General Macro (parallel)
  │   ├── update_inflation_cpi_ppi
  │   ├── update_building_permits
  │   ├── update_m2_money_supply
  │   └── update_usd_trade_weighted
  │
  └── Survey Data (parallel)
      ├── update_ism_manufacturing
      ├── update_ism_non_manufacturing
      ├── update_nfib_optimism
      └── update_umcsi
end
```

## Monitoring

### View DAG Status

1. Access Airflow Web UI: http://localhost:8080
2. Navigate to the `economic_data_daily_update` DAG
3. Check task status and logs

### Check Data Updates

Query the metadata schema:

```sql
-- View recent updates
SELECT 
    schema_name,
    table_name,
    records_added,
    update_status,
    completed_at
FROM metadata.data_updates
ORDER BY completed_at DESC
LIMIT 20;

-- View data freshness
SELECT 
    'china.manufacturing_pmi' as table_name,
    MAX(date) as latest_date,
    COUNT(*) as total_records
FROM china.manufacturing_pmi
UNION ALL
SELECT 
    'coincident_indicators.employment_situation',
    MAX(date),
    COUNT(*)
FROM coincident_indicators.employment_situation;
```

## Customization

### Adding New Data Sources

1. Add API client to `utils/api_clients.py`
2. Create update function in the DAG
3. Add PythonOperator to the DAG
4. Add task to dependency chain

### Changing Schedule

Modify the `schedule_interval` in the DAG definition:

```python
dag = DAG(
    'economic_data_daily_update',
    schedule_interval='0 6 * * *',  # Change this
    ...
)
```

Common schedules:
- `'0 6 * * *'` - Daily at 6 AM
- `'0 6 * * 1'` - Weekly on Monday at 6 AM
- `'0 6 1 * *'` - Monthly on 1st at 6 AM
- `'@daily'` - Daily at midnight
- `'@weekly'` - Weekly on Sunday at midnight

## Troubleshooting

### Task Failures

1. **API Key Invalid**: Check `.env` file and verify API keys
2. **Rate Limiting**: Increase `API_RATE_LIMIT_DELAY` in `.env`
3. **Network Issues**: Check `API_TIMEOUT` setting
4. **Data Format Changes**: Review API client code in `utils/api_clients.py`

### Database Issues

1. **Connection Failed**: Verify `timescaledb_conn` in Airflow connections
2. **Permission Denied**: Check database user permissions
3. **Table Not Found**: Run init scripts to create schema

### Debug Mode

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Performance Optimization

### Parallel Execution

Tasks are designed to run in parallel. Adjust Airflow parallelism:

```python
# airflow.cfg
[core]
parallelism = 32
dag_concurrency = 16
max_active_runs_per_dag = 1
```

### Data Incremental Updates

The DAG only fetches new data since the last update by:
1. Querying last date in database
2. Using that as `start_date` for API calls
3. Inserting only new records

### Rate Limiting

Respect API rate limits by adjusting:

```env
API_RATE_LIMIT_DELAY=1  # seconds between API calls
API_MAX_RETRIES=3
```

## Data Quality

### Validation

Each task logs:
- Number of records added
- Update status (success/failure)
- Error messages if any

### Monitoring Data Freshness

Run this query to check data staleness:

```sql
SELECT 
    schema_name,
    table_name,
    metadata.get_latest_date(schema_name, table_name) as latest_date,
    CURRENT_DATE - metadata.get_latest_date(schema_name, table_name) as days_stale
FROM metadata.data_updates
WHERE update_status = 'success'
GROUP BY schema_name, table_name;
```

## Support

For issues or questions:
1. Check Airflow logs: `docker-compose logs -f airflow_webserver`
2. Review task logs in Airflow UI
3. Check database logs: `docker-compose logs -f timescaledb`

## References

- [FRED API Docs](https://fred.stlouisfed.org/docs/api/fred/)
- [BLS API Docs](https://www.bls.gov/developers/api_signature_v2.htm)
- [EIA API Docs](https://www.eia.gov/opendata/)
- [NASDAQ Data Link Docs](https://docs.data.nasdaq.com/)
- [Airflow Docs](https://airflow.apache.org/docs/)
