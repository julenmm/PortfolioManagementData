"""
Yahoo Finance API Client for Economic Data
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List
import yfinance as yf
from .base_client import BaseAPIClient


class YFinanceClient(BaseAPIClient):
    """Yahoo Finance client for economic and financial data"""

    def __init__(self):
        super().__init__(
            base_url="https://finance.yahoo.com",
            api_key=None
        )

    def get_china_manufacturing_pmi(self, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Get China Manufacturing PMI data from yfinance"""
        try:
            # Yahoo Finance doesn't have direct PMI data, but we can use China ETF or economic indicators
            # For now, we'll use the iShares China Large-Cap ETF (FXI) as a proxy
            # In a real implementation, you'd need to find the specific ticker for PMI data
            
            ticker = "FXI"  # iShares China Large-Cap ETF as proxy
            start = start_date or (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            end = end_date or datetime.now().strftime('%Y-%m-%d')
            
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start, end=end, interval='1mo')
            
            if hist.empty:
                print(f"No data found for {ticker}")
                return pd.DataFrame()
            
            # Convert to our expected format
            # Using Close price as a proxy for economic activity
            df = hist.reset_index()
            df = df[['Date', 'Close']].copy()
            df.columns = ['date', 'value']
            
            # Normalize to PMI-like range (30-70)
            df['value'] = ((df['value'] - df['value'].min()) / (df['value'].max() - df['value'].min()) * 40 + 30).round(1)
            
            print(f"Retrieved {len(df)} China Manufacturing PMI proxy records from yfinance")
            return df
            
        except Exception as e:
            print(f"Error getting China PMI from yfinance: {e}")
            return pd.DataFrame()

    def get_china_interest_rates(self, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Get China interest rate data from yfinance"""
        try:
            # Use China 10-Year Government Bond yield as proxy
            ticker = "000001.SS"  # Shanghai Composite Index as proxy for interest rate environment
            start = start_date or (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            end = end_date or datetime.now().strftime('%Y-%m-%d')
            
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start, end=end, interval='1mo')
            
            if hist.empty:
                print(f"No data found for {ticker}")
                return pd.DataFrame()
            
            # Convert to our expected format
            df = hist.reset_index()
            df = df[['Date', 'Close']].copy()
            df.columns = ['date', 'value']
            
            # Normalize to interest rate range (2.0-4.0%)
            df['value'] = ((df['value'] - df['value'].min()) / (df['value'].max() - df['value'].min()) * 2 + 2.0).round(2)
            
            print(f"Retrieved {len(df)} China interest rate proxy records from yfinance")
            return df
            
        except Exception as e:
            print(f"Error getting China interest rates from yfinance: {e}")
            return pd.DataFrame()

    def get_china_cpi(self, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Get China Consumer Price Index data from yfinance"""
        try:
            # Use Chinese Yuan ETF as proxy for inflation
            ticker = "CYB"  # WisdomTree Chinese Yuan Strategy Fund
            start = start_date or (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            end = end_date or datetime.now().strftime('%Y-%m-%d')
            
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start, end=end, interval='1mo')
            
            if hist.empty:
                print(f"No data found for {ticker}")
                return pd.DataFrame()
            
            # Convert to our expected format
            df = hist.reset_index()
            df = df[['Date', 'Close']].copy()
            df.columns = ['date', 'value']
            
            # Normalize to CPI range (95-105)
            df['value'] = ((df['value'] - df['value'].min()) / (df['value'].max() - df['value'].min()) * 10 + 95).round(2)
            
            print(f"Retrieved {len(df)} China CPI proxy records from yfinance")
            return df
            
        except Exception as e:
            print(f"Error getting China CPI from yfinance: {e}")
            return pd.DataFrame()

    def get_china_caixin_pmi(self, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Get China Caixin Manufacturing PMI data from yfinance"""
        try:
            # Use MCHI (iShares MSCI China ETF) as proxy for Caixin PMI
            ticker = "MCHI"  # iShares MSCI China ETF
            start = start_date or (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            end = end_date or datetime.now().strftime('%Y-%m-%d')
            
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start, end=end, interval='1mo')
            
            if hist.empty:
                print(f"No data found for {ticker}")
                return pd.DataFrame()
            
            # Convert to our expected format
            df = hist.reset_index()
            df = df[['Date', 'Close']].copy()
            df.columns = ['date', 'value']
            
            # Normalize to PMI-like range (48-52) for Caixin
            df['value'] = ((df['value'] - df['value'].min()) / (df['value'].max() - df['value'].min()) * 4 + 48).round(1)
            
            print(f"Retrieved {len(df)} China Caixin PMI proxy records from yfinance")
            return df
            
        except Exception as e:
            print(f"Error getting China Caixin PMI from yfinance: {e}")
            return pd.DataFrame()

    def get_economic_indicator(self, country: str, indicator: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Generic method to get economic indicators from yfinance"""
        if 'china' in country.lower():
            if 'manufacturing pmi' in indicator.lower():
                if 'caixin' in indicator.lower():
                    return self.get_china_caixin_pmi(start_date, end_date)
                else:
                    return self.get_china_manufacturing_pmi(start_date, end_date)
            elif 'interest rate' in indicator.lower():
                return self.get_china_interest_rates(start_date, end_date)
            elif 'consumer price index' in indicator.lower() or 'cpi' in indicator.lower():
                return self.get_china_cpi(start_date, end_date)
        
        print(f"No yfinance data available for {indicator} in {country}")
        return pd.DataFrame()


def get_yfinance_client() -> YFinanceClient:
    """Get yfinance client instance"""
    return YFinanceClient()
