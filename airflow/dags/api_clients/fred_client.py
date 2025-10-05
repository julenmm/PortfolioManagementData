"""
FRED (Federal Reserve Economic Data) API Client
"""

import os
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
from .base_client import BaseAPIClient


class FREDClient(BaseAPIClient):
    """FRED API client for economic data"""
    
    def __init__(self):
        api_key = os.getenv('FRED_API_KEY')
        if not api_key:
            raise ValueError("FRED_API_KEY environment variable is required")
        
        super().__init__(
            base_url='https://api.stlouisfed.org/fred',
            api_key=api_key
        )
    
    def get_series(self, series_id: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Get economic series data from FRED"""
        try:
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
                if not df.empty:
                    # Convert date and value columns
                    df['date'] = pd.to_datetime(df['date'])
                    df['value'] = pd.to_numeric(df['value'], errors='coerce')
                    # Remove rows with missing values
                    df = df.dropna(subset=['value'])
                    df = df[['date', 'value']]
                    
                    print(f"Retrieved {len(df)} records for series {series_id}")
                    return df
            
            print(f"No data found for series {series_id}")
            return pd.DataFrame()
            
        except Exception as e:
            print(f"Error retrieving FRED series {series_id}: {e}")
            return pd.DataFrame()
    
    def get_series_info(self, series_id: str) -> dict:
        """Get series information from FRED"""
        try:
            params = {
                'series_id': series_id,
                'api_key': self.api_key,
                'file_type': 'json'
            }
            
            data = self._make_request('series', params)
            
            if 'seriess' in data and data['seriess']:
                return data['seriess'][0]
            
            return {}
            
        except Exception as e:
            print(f"Error retrieving FRED series info for {series_id}: {e}")
            return {}


def get_fred_client() -> FREDClient:
    return FREDClient()
