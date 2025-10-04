# API Keys Setup Guide

This guide will help you obtain all necessary API keys for the economic data pipeline.

## 🔑 Required API Keys

### 1. FRED (Federal Reserve Economic Data) ⭐ **REQUIRED**

**What it provides**: US economic indicators, international data, interest rates

**How to get**:
1. Go to https://fred.stlouisfed.org/
2. Create a free account
3. Go to https://fred.stlouisfed.org/docs/api/api_key.html
4. Click "Request API Key"
5. Copy your API key

**Add to .env**:
```env
FRED_API_KEY=your_actual_key_here
```

**Rate Limits**: 120 requests/minute

---

### 2. BLS (Bureau of Labor Statistics) ⭐ **REQUIRED**

**What it provides**: Employment data, inflation (CPI/PPI), labor statistics

**How to get**:
1. Go to https://www.bls.gov/developers/
2. Click "Registration"
3. Fill out the registration form
4. Check your email for API key

**Add to .env**:
```env
BLS_API_KEY=your_actual_key_here
```

**Rate Limits**: 500 requests/day (with key), 25 requests/day (without)

---

### 3. EIA (Energy Information Administration) ⭐ **REQUIRED**

**What it provides**: Energy data, oil prices, natural gas data

**How to get**:
1. Go to https://www.eia.gov/opendata/register.php
2. Fill out registration form
3. Verify email address
4. API key will be sent to your email

**Add to .env**:
```env
EIA_API_KEY=your_actual_key_here
```

**Rate Limits**: No strict limit

---

### 4. NASDAQ Data Link (formerly Quandl) ⭐ **REQUIRED**

**What it provides**: ISM data, COT reports, financial datasets

**How to get**:
1. Go to https://data.nasdaq.com/sign-up
2. Create free account
3. Go to Account Settings → API Key
4. Copy your API key

**Add to .env**:
```env
NASDAQ_API_KEY=your_actual_key_here
```

**Rate Limits**: 
- Free: 50 calls/day
- Premium: Unlimited

---

### 5. Alpha Vantage (Optional Backup)

**What it provides**: Backup for some financial indicators

**How to get**:
1. Go to https://www.alphavantage.co/support/#api-key
2. Enter your email
3. Receive API key instantly

**Add to .env**:
```env
ALPHA_VANTAGE_API_KEY=your_actual_key_here
```

**Rate Limits**: 5 API requests per minute, 500 per day (free)

---

## 🆓 No API Key Required

These sources don't require API keys:

### OECD (Organisation for Economic Co-operation and Development)
- **What it provides**: International economic data, OECD member statistics
- **Access**: Direct API access, no key required
- **URL**: https://stats.oecd.org/

### IMF (International Monetary Fund)
- **What it provides**: Global commodity prices, international financial data
- **Access**: Public API, no key required
- **URL**: http://dataservices.imf.org/

### ECB (European Central Bank)
- **What it provides**: European benchmark yields, economic sentiment
- **Access**: Open data portal, no key required
- **URL**: https://data.ecb.europa.eu/

### World Bank
- **What it provides**: Global GDP, development indicators
- **Access**: Open data API, no key required
- **URL**: https://api.worldbank.org/v2

---

## 📝 Complete .env Configuration

After obtaining all keys, your `.env` file should look like:

```env
# =============================================================================
# API KEYS - Economic Data Sources
# =============================================================================

# FRED (Federal Reserve Economic Data) - REQUIRED
FRED_API_KEY=1234567890abcdef1234567890abcdef
FRED_BASE_URL=https://api.stlouisfed.org/fred

# Bureau of Labor Statistics (BLS) - REQUIRED
BLS_API_KEY=1234567890abcdef1234567890abcdef1234567890abcdef
BLS_BASE_URL=https://api.bls.gov/publicAPI/v2

# OECD - No key required
OECD_BASE_URL=https://stats.oecd.org/restsdmx/sdmx.ashx/GetData

# IMF - No key required
IMF_BASE_URL=http://dataservices.imf.org/REST/SDMX_JSON.svc

# EIA (Energy Information Administration) - REQUIRED
EIA_API_KEY=1234567890abcdef1234567890abcdef
EIA_BASE_URL=https://api.eia.gov/v2

# NASDAQ Data Link (formerly Quandl) - REQUIRED
NASDAQ_API_KEY=abcdefghijklmnop
NASDAQ_BASE_URL=https://data.nasdaq.com/api/v3

# ECB - No key required
ECB_BASE_URL=https://data-api.ecb.europa.eu/service

# World Bank - No key required
WORLD_BANK_BASE_URL=https://api.worldbank.org/v2

# Alpha Vantage (backup) - Optional
ALPHA_VANTAGE_API_KEY=DEMO
ALPHA_VANTAGE_BASE_URL=https://www.alphavantage.co/query

# =============================================================================
# API RATE LIMITING
# =============================================================================
API_RATE_LIMIT_DELAY=1
API_MAX_RETRIES=3
API_TIMEOUT=30
```

---

## ✅ Testing Your API Keys

After adding keys, test them:

### Test FRED
```bash
curl "https://api.stlouisfed.org/fred/series/observations?series_id=GNPCA&api_key=YOUR_KEY&file_type=json"
```

### Test BLS
```bash
curl -X POST "https://api.bls.gov/publicAPI/v2/timeseries/data/" \
  -H "Content-Type: application/json" \
  -d '{"seriesid":["CUUR0000SA0"],"startyear":"2023","endyear":"2024","registrationkey":"YOUR_KEY"}'
```

### Test EIA
```bash
curl "https://api.eia.gov/v2/petroleum/pri/spt/data/?api_key=YOUR_KEY"
```

### Test NASDAQ
```bash
curl "https://data.nasdaq.com/api/v3/datasets/FRED/GDP.json?api_key=YOUR_KEY"
```

---

## 🚦 Rate Limit Management

The pipeline automatically handles rate limits:

```env
# Adjust these based on your API tier
API_RATE_LIMIT_DELAY=1  # Wait 1 second between calls
API_MAX_RETRIES=3        # Retry failed calls 3 times
API_TIMEOUT=30           # Timeout after 30 seconds
```

### For Premium/Paid Accounts

If you have premium accounts with higher rate limits:

```env
API_RATE_LIMIT_DELAY=0.1  # 10 calls per second
```

---

## 🆙 Upgrading to Premium

### When to Upgrade

Consider upgrading if you:
- Need more frequent updates (hourly instead of daily)
- Want historical data beyond free limits
- Require real-time data feeds
- Hit rate limits regularly

### Costs (Approximate)

- **FRED**: Free (no premium tier)
- **BLS**: Free (no premium tier)
- **NASDAQ Data Link**: $49+/month for unlimited calls
- **EIA**: Free (no premium tier)
- **Alpha Vantage**: $49.99+/month for higher limits

---

## 🔒 Security Best Practices

1. **Never commit .env to git**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Use separate keys for dev/prod**
   ```env
   # Development
   FRED_API_KEY=dev_key_here
   
   # Production (separate .env file)
   FRED_API_KEY=prod_key_here
   ```

3. **Rotate keys periodically**
   - Regenerate keys every 6-12 months
   - Update immediately if compromised

4. **Monitor usage**
   - Check API dashboard for usage
   - Set up alerts for unusual activity

---

## 📊 Data Coverage Summary

| Data Category | Primary Source | Backup Source | API Key Required |
|--------------|---------------|---------------|------------------|
| US Economic Indicators | FRED | - | ✅ Yes |
| Employment Data | BLS | FRED | ✅ Yes |
| Energy Data | EIA | - | ✅ Yes |
| ISM Surveys | NASDAQ | - | ✅ Yes |
| COT Reports | NASDAQ | - | ✅ Yes |
| Commodity Prices | IMF | NASDAQ | ❌ No |
| International Yields | FRED | ECB | ✅ Yes |
| European Data | ECB | OECD | ❌ No |
| Global GDP | World Bank | - | ❌ No |

---

## 🆘 Troubleshooting

### "Invalid API Key" Error
1. Check for typos in .env file
2. Verify key hasn't expired
3. Check if key is activated (some require email verification)

### "Rate Limit Exceeded"
1. Increase `API_RATE_LIMIT_DELAY` in .env
2. Upgrade to premium tier
3. Reduce update frequency

### "No Data Returned"
1. Verify series ID is correct
2. Check date range is valid
3. Ensure data exists for requested period

---

## 📞 Support Contacts

- **FRED**: https://fred.stlouisfed.org/contactus
- **BLS**: https://www.bls.gov/bls/contact.htm
- **EIA**: InfoCtr@eia.gov
- **NASDAQ**: support@data.nasdaq.com

---

## ✨ Quick Start Checklist

- [ ] Register for FRED API key
- [ ] Register for BLS API key
- [ ] Register for EIA API key
- [ ] Register for NASDAQ Data Link API key
- [ ] (Optional) Register for Alpha Vantage
- [ ] Add all keys to .env file
- [ ] Test each API key
- [ ] Run `./start.sh` to start the pipeline
- [ ] Check Airflow UI for successful DAG runs
- [ ] Verify data in database

---

**Need Help?** Check the main README.md or the airflow/dags/README_DAGS.md for more information.
