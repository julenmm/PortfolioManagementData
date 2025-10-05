-- Initialize TimescaleDB for Economic Data Warehouse
-- This script sets up the database with TimescaleDB extension and creates schemas for economic data

-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- =============================================================================
-- CREATE SCHEMAS FOR DIFFERENT DATA CATEGORIES
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS china;
CREATE SCHEMA IF NOT EXISTS coincident_indicators;
CREATE SCHEMA IF NOT EXISTS commodities;
CREATE SCHEMA IF NOT EXISTS europe;
CREATE SCHEMA IF NOT EXISTS fixed_income;
CREATE SCHEMA IF NOT EXISTS general_macro;
CREATE SCHEMA IF NOT EXISTS survey_data;
CREATE SCHEMA IF NOT EXISTS metadata;

-- =============================================================================
-- METADATA SCHEMA - Track data sources and updates
-- =============================================================================

CREATE TABLE IF NOT EXISTS metadata.data_sources (
    id SERIAL PRIMARY KEY,
    source_name VARCHAR(100) NOT NULL UNIQUE,
    api_name VARCHAR(50) NOT NULL,
    base_url TEXT,
    description TEXT,
    update_frequency VARCHAR(50),
    last_updated TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS metadata.data_updates (
    id SERIAL PRIMARY KEY,
    schema_name VARCHAR(50) NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    source_id INTEGER REFERENCES metadata.data_sources(id),
    records_added INTEGER DEFAULT 0,
    records_updated INTEGER DEFAULT 0,
    update_status VARCHAR(20),
    error_message TEXT,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

-- =============================================================================
-- CHINA SCHEMA
-- =============================================================================

-- China Manufacturing PMIs (FRED)
CREATE TABLE IF NOT EXISTS china.manufacturing_pmi (
    date DATE NOT NULL,
    pmi_value DECIMAL(10,4),
    source TEXT DEFAULT 'FRED',
    series_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, series_id)
);

SELECT create_hypertable('china.manufacturing_pmi', 'date', if_not_exists => TRUE);

-- China Real Rates (OECD)
CREATE TABLE IF NOT EXISTS china.real_rates (
    date DATE NOT NULL,
    real_rate DECIMAL(10,4),
    nominal_rate DECIMAL(10,4),
    inflation_rate DECIMAL(10,4),
    source TEXT DEFAULT 'OECD',
    series_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, series_id)
);

SELECT create_hypertable('china.real_rates', 'date', if_not_exists => TRUE);

-- China Consumer Price Index (FRED)
CREATE TABLE IF NOT EXISTS china.consumer_price_index (
    date DATE NOT NULL,
    cpi_value DECIMAL(10,4),
    cpi_yoy_change DECIMAL(10,4),
    source TEXT DEFAULT 'FRED',
    series_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, series_id)
);

SELECT create_hypertable('china.consumer_price_index', 'date', if_not_exists => TRUE);

-- =============================================================================
-- COINCIDENT INDICATORS SCHEMA
-- =============================================================================

-- Durable Goods Shipments (FRED)
CREATE TABLE IF NOT EXISTS coincident_indicators.durable_goods_shipments (
    date DATE NOT NULL,
    value DECIMAL(15,2),
    percent_change DECIMAL(10,4),
    series_id TEXT,
    seasonally_adjusted BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, series_id)
);

SELECT create_hypertable('coincident_indicators.durable_goods_shipments', 'date', if_not_exists => TRUE);

-- Employment Situation Report (BLS)
CREATE TABLE IF NOT EXISTS coincident_indicators.employment_situation (
    date DATE NOT NULL,
    total_nonfarm_payroll INTEGER,
    unemployment_rate DECIMAL(5,2),
    labor_force_participation_rate DECIMAL(5,2),
    average_hourly_earnings DECIMAL(10,2),
    average_weekly_hours DECIMAL(5,2),
    series_id TEXT,
    seasonally_adjusted BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, series_id)
);

SELECT create_hypertable('coincident_indicators.employment_situation', 'date', if_not_exists => TRUE);

-- Industrial Production (FRED)
CREATE TABLE IF NOT EXISTS coincident_indicators.industrial_production (
    date DATE NOT NULL,
    index_value DECIMAL(10,4),
    percent_change DECIMAL(10,4),
    series_id TEXT,
    industry_category TEXT,
    seasonally_adjusted BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, series_id, industry_category)
);

SELECT create_hypertable('coincident_indicators.industrial_production', 'date', if_not_exists => TRUE);

-- Jobless Claims (FRED)
CREATE TABLE IF NOT EXISTS coincident_indicators.jobless_claims (
    date DATE NOT NULL,
    initial_claims INTEGER,
    continuing_claims INTEGER,
    four_week_moving_avg INTEGER,
    series_id TEXT,
    seasonally_adjusted BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, series_id)
);

SELECT create_hypertable('coincident_indicators.jobless_claims', 'date', if_not_exists => TRUE);

-- =============================================================================
-- COMMODITIES SCHEMA
-- =============================================================================

-- Commitment of Traders (NASDAQ)
CREATE TABLE IF NOT EXISTS commodities.cot_metals_energy (
    date DATE NOT NULL,
    commodity TEXT NOT NULL,
    commercial_long INTEGER,
    commercial_short INTEGER,
    noncommercial_long INTEGER,
    noncommercial_short INTEGER,
    total_open_interest INTEGER,
    net_position INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, commodity)
);

SELECT create_hypertable('commodities.cot_metals_energy', 'date', if_not_exists => TRUE);

-- Commodity Prices (IMF)
CREATE TABLE IF NOT EXISTS commodities.commodity_prices (
    date DATE NOT NULL,
    commodity_name TEXT NOT NULL,
    price DECIMAL(15,4),
    unit TEXT,
    currency TEXT DEFAULT 'USD',
    price_type TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, commodity_name, price_type)
);

SELECT create_hypertable('commodities.commodity_prices', 'date', if_not_exists => TRUE);

-- Commodities Summary (EIA)
CREATE TABLE IF NOT EXISTS commodities.eia_summary (
    date DATE NOT NULL,
    series_id TEXT NOT NULL,
    product TEXT,
    value DECIMAL(15,4),
    unit TEXT,
    frequency TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, series_id)
);

SELECT create_hypertable('commodities.eia_summary', 'date', if_not_exists => TRUE);

-- Cyclical Commodities Demand Supply (EIA)
CREATE TABLE IF NOT EXISTS commodities.demand_supply_factors (
    date DATE NOT NULL,
    commodity TEXT NOT NULL,
    demand DECIMAL(15,4),
    supply DECIMAL(15,4),
    inventory DECIMAL(15,4),
    capacity_utilization DECIMAL(5,2),
    unit TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, commodity)
);

SELECT create_hypertable('commodities.demand_supply_factors', 'date', if_not_exists => TRUE);

-- =============================================================================
-- EUROPE SCHEMA
-- =============================================================================

-- Benchmark Yields EU (ECB)
CREATE TABLE IF NOT EXISTS europe.benchmark_yields_ecb (
    date DATE NOT NULL,
    country TEXT NOT NULL,
    maturity TEXT NOT NULL,
    yield DECIMAL(10,4),
    series_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, country, maturity)
);

SELECT create_hypertable('europe.benchmark_yields_ecb', 'date', if_not_exists => TRUE);

-- European Economic Sentiment Indicator (ECB)
CREATE TABLE IF NOT EXISTS europe.economic_sentiment (
    date DATE NOT NULL,
    country TEXT NOT NULL,
    esi_value DECIMAL(10,2),
    industrial_confidence DECIMAL(10,2),
    services_confidence DECIMAL(10,2),
    consumer_confidence DECIMAL(10,2),
    retail_confidence DECIMAL(10,2),
    construction_confidence DECIMAL(10,2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, country)
);

SELECT create_hypertable('europe.economic_sentiment', 'date', if_not_exists => TRUE);

-- Global GDP (WORLD BANK)
CREATE TABLE IF NOT EXISTS europe.global_gdp (
    date DATE NOT NULL,
    country TEXT NOT NULL,
    gdp_current_usd DECIMAL(20,2),
    gdp_growth_rate DECIMAL(10,4),
    gdp_per_capita DECIMAL(15,2),
    series_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, country, series_id)
);

SELECT create_hypertable('europe.global_gdp', 'date', if_not_exists => TRUE);

-- =============================================================================
-- FIXED INCOME SCHEMA
-- =============================================================================

-- Benchmark Yields (FRED) - Multiple Countries
CREATE TABLE IF NOT EXISTS fixed_income.benchmark_yields (
    date DATE NOT NULL,
    country TEXT NOT NULL,
    maturity TEXT NOT NULL,
    yield DECIMAL(10,4),
    series_id TEXT,
    source TEXT DEFAULT 'FRED',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, country, maturity, series_id)
);

SELECT create_hypertable('fixed_income.benchmark_yields', 'date', if_not_exists => TRUE);

-- Bond Market Basics (FRED)
CREATE TABLE IF NOT EXISTS fixed_income.bond_market_basics (
    date DATE NOT NULL,
    series_id TEXT NOT NULL,
    series_name TEXT,
    value DECIMAL(15,4),
    category TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, series_id)
);

SELECT create_hypertable('fixed_income.bond_market_basics', 'date', if_not_exists => TRUE);

-- Corporate Bond Indices (FRED)
CREATE TABLE IF NOT EXISTS fixed_income.corporate_bond_indices (
    date DATE NOT NULL,
    index_name TEXT NOT NULL,
    index_value DECIMAL(15,4),
    yield DECIMAL(10,4),
    spread DECIMAL(10,4),
    duration DECIMAL(10,4),
    rating TEXT,
    series_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, index_name, series_id)
);

SELECT create_hypertable('fixed_income.corporate_bond_indices', 'date', if_not_exists => TRUE);

-- =============================================================================
-- GENERAL MACRO SCHEMA
-- =============================================================================

-- Inflation CPI & PPI (BLS)
CREATE TABLE IF NOT EXISTS general_macro.inflation (
    date DATE NOT NULL,
    cpi_all_items DECIMAL(10,4),
    cpi_core DECIMAL(10,4),
    cpi_yoy_change DECIMAL(10,4),
    ppi_all_commodities DECIMAL(10,4),
    ppi_core DECIMAL(10,4),
    ppi_yoy_change DECIMAL(10,4),
    series_id TEXT,
    seasonally_adjusted BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, series_id)
);

SELECT create_hypertable('general_macro.inflation', 'date', if_not_exists => TRUE);

-- US Building Permits (FRED)
CREATE TABLE IF NOT EXISTS general_macro.building_permits (
    date DATE NOT NULL,
    total_permits INTEGER,
    single_family INTEGER,
    multi_family INTEGER,
    series_id TEXT,
    region TEXT,
    seasonally_adjusted BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, series_id, region)
);

SELECT create_hypertable('general_macro.building_permits', 'date', if_not_exists => TRUE);

-- US M2 Money Supply (FRED)
CREATE TABLE IF NOT EXISTS general_macro.m2_money_supply (
    date DATE NOT NULL,
    m2_value DECIMAL(20,2),
    m2_yoy_change DECIMAL(10,4),
    series_id TEXT,
    seasonally_adjusted BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, series_id)
);

SELECT create_hypertable('general_macro.m2_money_supply', 'date', if_not_exists => TRUE);

-- USD Trade Weighted Indices (FRED)
CREATE TABLE IF NOT EXISTS general_macro.usd_trade_weighted (
    date DATE NOT NULL,
    broad_index DECIMAL(10,4),
    major_currencies DECIMAL(10,4),
    other_important_trading_partners DECIMAL(10,4),
    series_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, series_id)
);

SELECT create_hypertable('general_macro.usd_trade_weighted', 'date', if_not_exists => TRUE);

-- =============================================================================
-- SURVEY DATA SCHEMA
-- =============================================================================

-- ISM Manufacturing Index (QUANDL/ISM)
CREATE TABLE IF NOT EXISTS survey_data.ism_manufacturing (
    date DATE NOT NULL PRIMARY KEY,
    pmi DECIMAL(10,2),
    new_orders DECIMAL(10,2),
    production DECIMAL(10,2),
    employment DECIMAL(10,2),
    supplier_deliveries DECIMAL(10,2),
    inventories DECIMAL(10,2),
    customers_inventories DECIMAL(10,2),
    prices DECIMAL(10,2),
    backlog_orders DECIMAL(10,2),
    new_export_orders DECIMAL(10,2),
    imports DECIMAL(10,2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

SELECT create_hypertable('survey_data.ism_manufacturing', 'date', if_not_exists => TRUE);

-- ISM Non-Manufacturing Index (QUANDL/ISM)
CREATE TABLE IF NOT EXISTS survey_data.ism_non_manufacturing (
    date DATE NOT NULL PRIMARY KEY,
    nmi DECIMAL(10,2),
    business_activity DECIMAL(10,2),
    new_orders DECIMAL(10,2),
    employment DECIMAL(10,2),
    supplier_deliveries DECIMAL(10,2),
    inventories DECIMAL(10,2),
    prices DECIMAL(10,2),
    backlog_orders DECIMAL(10,2),
    new_export_orders DECIMAL(10,2),
    imports DECIMAL(10,2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

SELECT create_hypertable('survey_data.ism_non_manufacturing', 'date', if_not_exists => TRUE);

-- NFIB Small Business Optimism Index (FRED)
CREATE TABLE IF NOT EXISTS survey_data.nfib_optimism (
    date DATE NOT NULL,
    optimism_index DECIMAL(10,2),
    region TEXT,
    industry TEXT,
    series_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, region, industry)
);

SELECT create_hypertable('survey_data.nfib_optimism', 'date', if_not_exists => TRUE);

-- NFIB Small Business Sentiment Components (FRED)
CREATE TABLE IF NOT EXISTS survey_data.nfib_sentiment_components (
    date DATE NOT NULL,
    earnings_trend DECIMAL(10,2),
    sales_expectations DECIMAL(10,2),
    expansion_plans DECIMAL(10,2),
    hiring_plans DECIMAL(10,2),
    inventory_plans DECIMAL(10,2),
    capital_spending DECIMAL(10,2),
    credit_conditions DECIMAL(10,2),
    series_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, series_id)
);

SELECT create_hypertable('survey_data.nfib_sentiment_components', 'date', if_not_exists => TRUE);

-- UMCSI - University of Michigan Consumer Sentiment Index (FRED)
CREATE TABLE IF NOT EXISTS survey_data.umcsi (
    date DATE NOT NULL,
    sentiment_index DECIMAL(10,2),
    current_conditions DECIMAL(10,2),
    expectations DECIMAL(10,2),
    series_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, series_id)
);

SELECT create_hypertable('survey_data.umcsi', 'date', if_not_exists => TRUE);

-- Correlation Analysis Tables
CREATE TABLE IF NOT EXISTS survey_data.correlation_ism_manufacturing (
    date DATE NOT NULL PRIMARY KEY,
    ism_manufacturing DECIMAL(10,2),
    sp500_return DECIMAL(10,4),
    gdp_growth DECIMAL(10,4),
    correlation_coefficient DECIMAL(10,6),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS survey_data.correlation_ism_non_manufacturing (
    date DATE NOT NULL PRIMARY KEY,
    ism_non_manufacturing DECIMAL(10,2),
    sp500_return DECIMAL(10,4),
    gdp_growth DECIMAL(10,4),
    correlation_coefficient DECIMAL(10,6),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS survey_data.nfib_regional_optimism (
    date DATE NOT NULL,
    region TEXT NOT NULL,
    optimism_index DECIMAL(10,2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (date, region)
);

-- =============================================================================
-- CREATE INDEXES FOR PERFORMANCE
-- =============================================================================

-- China schema indexes
CREATE INDEX IF NOT EXISTS idx_china_pmi_date ON china.manufacturing_pmi (date DESC);
CREATE INDEX IF NOT EXISTS idx_china_rates_date ON china.real_rates (date DESC);
CREATE INDEX IF NOT EXISTS idx_china_cpi_date ON china.consumer_price_index (date DESC);

-- Coincident indicators indexes
CREATE INDEX IF NOT EXISTS idx_durable_goods_date ON coincident_indicators.durable_goods_shipments (date DESC);
CREATE INDEX IF NOT EXISTS idx_employment_date ON coincident_indicators.employment_situation (date DESC);
CREATE INDEX IF NOT EXISTS idx_industrial_prod_date ON coincident_indicators.industrial_production (date DESC);
CREATE INDEX IF NOT EXISTS idx_jobless_claims_date ON coincident_indicators.jobless_claims (date DESC);

-- Commodities indexes
CREATE INDEX IF NOT EXISTS idx_cot_date_commodity ON commodities.cot_metals_energy (date DESC, commodity);
CREATE INDEX IF NOT EXISTS idx_commodity_prices_date ON commodities.commodity_prices (date DESC, commodity_name);

-- Fixed income indexes
CREATE INDEX IF NOT EXISTS idx_yields_date_country ON fixed_income.benchmark_yields (date DESC, country);
CREATE INDEX IF NOT EXISTS idx_corp_bonds_date ON fixed_income.corporate_bond_indices (date DESC);

-- General macro indexes
CREATE INDEX IF NOT EXISTS idx_inflation_date ON general_macro.inflation (date DESC);
CREATE INDEX IF NOT EXISTS idx_building_permits_date ON general_macro.building_permits (date DESC);

-- Survey data indexes
CREATE INDEX IF NOT EXISTS idx_ism_mfg_date ON survey_data.ism_manufacturing (date DESC);
CREATE INDEX IF NOT EXISTS idx_ism_nonmfg_date ON survey_data.ism_non_manufacturing (date DESC);
CREATE INDEX IF NOT EXISTS idx_nfib_date ON survey_data.nfib_optimism (date DESC);

-- =============================================================================
-- CREATE VIEWS FOR COMMON QUERIES
-- =============================================================================

-- Comprehensive Economic Dashboard View
CREATE OR REPLACE VIEW metadata.economic_dashboard AS
SELECT 
    CURRENT_DATE as snapshot_date,
    (SELECT COUNT(*) FROM metadata.data_sources) as total_data_sources,
    (SELECT COUNT(*) FROM metadata.data_updates WHERE update_status = 'success') as successful_updates,
    (SELECT MAX(completed_at) FROM metadata.data_updates) as last_update;

-- Latest ISM Manufacturing Data
CREATE OR REPLACE VIEW survey_data.latest_ism_manufacturing AS
SELECT * FROM survey_data.ism_manufacturing
WHERE date = (SELECT MAX(date) FROM survey_data.ism_manufacturing);

-- Latest Employment Data
CREATE OR REPLACE VIEW coincident_indicators.latest_employment AS
SELECT * FROM coincident_indicators.employment_situation
WHERE date = (SELECT MAX(date) FROM coincident_indicators.employment_situation);

-- =============================================================================
-- INSERT SAMPLE DATA SOURCES
-- =============================================================================

INSERT INTO metadata.data_sources (source_name, api_name, description, update_frequency) VALUES
('China Manufacturing PMI', 'FRED', 'China Manufacturing PMI from Federal Reserve Economic Data', 'Monthly'),
('China Real Rates', 'OECD', 'China Real Interest Rates from OECD', 'Quarterly'),
('Durable Goods Shipments', 'FRED', 'US Durable Goods Shipments', 'Monthly'),
('Employment Situation', 'BLS', 'US Employment Situation Report from Bureau of Labor Statistics', 'Monthly'),
('Industrial Production', 'FRED', 'US Industrial Production Index', 'Monthly'),
('Jobless Claims', 'FRED', 'US Initial and Continuing Jobless Claims', 'Weekly'),
('Commitment of Traders', 'NASDAQ', 'COT Report for Metals and Energy', 'Weekly'),
('Commodity Prices', 'IMF', 'Global Commodity Prices from IMF', 'Monthly'),
('EIA Summary', 'EIA', 'Energy Information Administration Summary', 'Weekly'),
('Benchmark Yields', 'FRED', 'Government Bond Yields Multiple Countries', 'Daily'),
('ISM Manufacturing', 'ISM', 'ISM Manufacturing Index', 'Monthly'),
('ISM Non-Manufacturing', 'ISM', 'ISM Non-Manufacturing Index', 'Monthly'),
('NFIB Optimism', 'FRED', 'NFIB Small Business Optimism Index', 'Monthly'),
('UMCSI', 'FRED', 'University of Michigan Consumer Sentiment Index', 'Monthly')
ON CONFLICT (source_name) DO NOTHING;

-- =============================================================================
-- CREATE FUNCTIONS FOR DATA MANAGEMENT
-- =============================================================================

-- Function to get latest data date for a table
CREATE OR REPLACE FUNCTION metadata.get_latest_date(schema_name TEXT, table_name TEXT)
RETURNS DATE AS $$
DECLARE
    latest_date DATE;
BEGIN
    EXECUTE format('SELECT MAX(date) FROM %I.%I', schema_name, table_name) INTO latest_date;
    RETURN latest_date;
END;
$$ LANGUAGE plpgsql;

-- Function to count records in a table
CREATE OR REPLACE FUNCTION metadata.count_records(schema_name TEXT, table_name TEXT)
RETURNS INTEGER AS $$
DECLARE
    record_count INTEGER;
BEGIN
    EXECUTE format('SELECT COUNT(*) FROM %I.%I', schema_name, table_name) INTO record_count;
    RETURN record_count;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- GRANT PERMISSIONS
-- =============================================================================

-- Create roles if they don't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'economic_data_app') THEN
        CREATE ROLE economic_data_app WITH LOGIN PASSWORD 'economic_app_password';
    END IF;
END
$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'economic_data_readonly') THEN
        CREATE ROLE economic_data_readonly WITH LOGIN PASSWORD 'economic_readonly_password';
    END IF;
END
$$;

-- Grant permissions to app role
GRANT USAGE ON SCHEMA china, coincident_indicators, commodities, europe, fixed_income, general_macro, survey_data, metadata TO economic_data_app;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA china, coincident_indicators, commodities, europe, fixed_income, general_macro, survey_data, metadata TO economic_data_app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA china, coincident_indicators, commodities, europe, fixed_income, general_macro, survey_data, metadata TO economic_data_app;

-- Grant permissions to readonly role
GRANT USAGE ON SCHEMA china, coincident_indicators, commodities, europe, fixed_income, general_macro, survey_data, metadata TO economic_data_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA china, coincident_indicators, commodities, europe, fixed_income, general_macro, survey_data, metadata TO economic_data_readonly;

COMMENT ON SCHEMA china IS 'Economic data related to China';
COMMENT ON SCHEMA coincident_indicators IS 'US economic coincident indicators';
COMMENT ON SCHEMA commodities IS 'Commodity prices and trading data';
COMMENT ON SCHEMA europe IS 'European economic data';
COMMENT ON SCHEMA fixed_income IS 'Fixed income and bond market data';
COMMENT ON SCHEMA general_macro IS 'General macroeconomic indicators';
COMMENT ON SCHEMA survey_data IS 'Economic survey and sentiment data';
COMMENT ON SCHEMA metadata IS 'Metadata about data sources and updates';