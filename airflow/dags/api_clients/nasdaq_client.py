"""
NASDAQ API Client
"""

import pandas as pd
from .base_client import BaseAPIClient


class NASDAQClient(BaseAPIClient):
    """NASDAQ API client for financial data"""
    
    def __init__(self):
        super().__init__(
            base_url='https://data.nasdaq.com/api/v3',
            api_key=None
        )


def get_nasdaq_client() -> NASDAQClient:
    return NASDAQClient()
