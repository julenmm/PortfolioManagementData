"""
API clients for various economic data sources
"""

import os
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd


class BaseAPIClient:
    """Base class for API clients"""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        self.rate_limit_delay = float(os.getenv('API_RATE_LIMIT_DELAY', 1))
        self.max_retries = int(os.getenv('API_MAX_RETRIES', 3))
        self.timeout = int(os.getenv('API_TIMEOUT', 30))
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make API request with retry logic"""
        url = f"{self.base_url}/{endpoint}"
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                time.sleep(self.rate_limit_delay)
                return response.json()
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return {}


class FREDClient(BaseAPIClient):
    """FRED API Client"""
    
    def __init__(self):
        super().__init__(
            base_url=os.getenv('FRED_BASE_URL', 'https://api.stlouisfed.org/fred'),
            api_key=os.getenv('FRED_API_KEY')
        )
    
    def get_series(self, series_id: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Get FRED time series data"""
        params = {
            'series_id': series_id,
            'api_key': self.api_key,
            'file_type': 'json'
        }
        
        if start_date:
            params['observation_start'] = start_date
        if end_date:
            params['observation_end'] = end_date
        
        data = self._make_request('series/observations', params)
        
        if 'observations' in data:
            df = pd.DataFrame(data['observations'])
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            return df
        
        return pd.DataFrame()


class BLSClient(BaseAPIClient):
    """BLS API Client"""
    
    def __init__(self):
        super().__init__(
            base_url=os.getenv('BLS_BASE_URL', 'https://api.bls.gov/publicAPI/v2'),
            api_key=os.getenv('BLS_API_KEY')
        )
    
    def get_series(self, series_ids: List[str], start_year: int = None, end_year: int = None) -> pd.DataFrame:
        """Get BLS time series data"""
        if not start_year:
            start_year = (datetime.now() - timedelta(days=365*5)).year
        if not end_year:
            end_year = datetime.now().year
        
        payload = {
            'seriesid': series_ids,
            'startyear': str(start_year),
            'endyear': str(end_year),
            'registrationkey': self.api_key
        }
        
        response = self.session.post(
            f"{self.base_url}/timeseries/data/",
            json=payload,
            timeout=self.timeout
        )
        
        data = response.json()
        
        if data['status'] == 'REQUEST_SUCCEEDED':
            all_data = []
            for series in data['Results']['series']:
                series_id = series['seriesID']
                for item in series['data']:
                    all_data.append({
                        'series_id': series_id,
                        'year': item['year'],
                        'period': item['period'],
                        'value': float(item['value']),
                        'date': self._parse_bls_date(item['year'], item['period'])
                    })
            
            return pd.DataFrame(all_data)
        
        return pd.DataFrame()
    
    @staticmethod
    def _parse_bls_date(year: str, period: str) -> datetime:
        """Parse BLS date format"""
        if period.startswith('M'):
            month = int(period[1:])
            return datetime(int(year), month, 1)
        elif period.startswith('Q'):
            quarter = int(period[1:])
            month = (quarter - 1) * 3 + 1
            return datetime(int(year), month, 1)
        else:
            return datetime(int(year), 1, 1)


class OECDClient(BaseAPIClient):
    """OECD API Client"""
    
    def __init__(self):
        super().__init__(
            base_url=os.getenv('OECD_BASE_URL', 'https://stats.oecd.org/restsdmx/sdmx.ashx/GetData')
        )
    
    def get_data(self, dataset: str, filter_expression: str = '') -> pd.DataFrame:
        """Get OECD data"""
        url = f"{self.base_url}/{dataset}/{filter_expression}/all"
        params = {'format': 'json'}
        
        data = self._make_request('', params)
        # Parse SDMX-JSON format (implementation depends on specific dataset structure)
        return pd.DataFrame()


class IMFClient(BaseAPIClient):
    """IMF API Client"""
    
    def __init__(self):
        super().__init__(
            base_url=os.getenv('IMF_BASE_URL', 'http://dataservices.imf.org/REST/SDMX_JSON.svc')
        )
    
    def get_commodity_prices(self, commodity_code: str = 'PCPS_IX') -> pd.DataFrame:
        """Get IMF commodity price data"""
        endpoint = f"CompactData/PCPS/{commodity_code}"
        data = self._make_request(endpoint)
        
        # Parse IMF SDMX-JSON format
        return pd.DataFrame()


class EIAClient(BaseAPIClient):
    """EIA API Client"""
    
    def __init__(self):
        super().__init__(
            base_url=os.getenv('EIA_BASE_URL', 'https://api.eia.gov/v2'),
            api_key=os.getenv('EIA_API_KEY')
        )
    
    def get_series(self, series_id: str, start_date: str = None) -> pd.DataFrame:
        """Get EIA time series data"""
        params = {
            'api_key': self.api_key,
            'frequency': 'daily',
            'data[0]': 'value'
        }
        
        if start_date:
            params['start'] = start_date
        
        data = self._make_request(f"seriesid/{series_id}", params)
        return pd.DataFrame(data.get('response', {}).get('data', []))


class NASDAQClient(BaseAPIClient):
    """NASDAQ Data Link (Quandl) API Client"""
    
    def __init__(self):
        super().__init__(
            base_url=os.getenv('NASDAQ_BASE_URL', 'https://data.nasdaq.com/api/v3'),
            api_key=os.getenv('NASDAQ_API_KEY')
        )
    
    def get_dataset(self, dataset_code: str, start_date: str = None) -> pd.DataFrame:
        """Get NASDAQ dataset"""
        params = {
            'api_key': self.api_key
        }
        
        if start_date:
            params['start_date'] = start_date
        
        data = self._make_request(f"datasets/{dataset_code}/data.json", params)
        
        if 'dataset_data' in data:
            df = pd.DataFrame(
                data['dataset_data']['data'],
                columns=data['dataset_data']['column_names']
            )
            df['Date'] = pd.to_datetime(df['Date'])
            return df
        
        return pd.DataFrame()


class ECBClient(BaseAPIClient):
    """ECB API Client"""
    
    def __init__(self):
        super().__init__(
            base_url=os.getenv('ECB_BASE_URL', 'https://data-api.ecb.europa.eu/service')
        )
    
    def get_data(self, flow: str, key: str = '') -> pd.DataFrame:
        """Get ECB data"""
        endpoint = f"data/{flow}/{key}"
        params = {'format': 'jsondata'}
        
        data = self._make_request(endpoint, params)
        return pd.DataFrame()


class WorldBankClient(BaseAPIClient):
    """World Bank API Client"""
    
    def __init__(self):
        super().__init__(
            base_url=os.getenv('WORLD_BANK_BASE_URL', 'https://api.worldbank.org/v2')
        )
    
    def get_indicator(self, country: str, indicator: str, start_year: int = None) -> pd.DataFrame:
        """Get World Bank indicator data"""
        endpoint = f"country/{country}/indicator/{indicator}"
        params = {
            'format': 'json',
            'per_page': 500
        }
        
        if start_year:
            params['date'] = f"{start_year}:{datetime.now().year}"
        
        data = self._make_request(endpoint, params)
        
        if isinstance(data, list) and len(data) > 1:
            df = pd.DataFrame(data[1])
            return df
        
        return pd.DataFrame()


# Helper function to get client instances
def get_fred_client() -> FREDClient:
    return FREDClient()

def get_bls_client() -> BLSClient:
    return BLSClient()

def get_oecd_client() -> OECDClient:
    return OECDClient()

def get_imf_client() -> IMFClient:
    return IMFClient()

def get_eia_client() -> EIAClient:
    return EIAClient()

def get_nasdaq_client() -> NASDAQClient:
    return NASDAQClient()

def get_ecb_client() -> ECBClient:
    return ECBClient()

def get_world_bank_client() -> WorldBankClient:
    return WorldBankClient()
