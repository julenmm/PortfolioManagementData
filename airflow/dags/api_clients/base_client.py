"""
Base API Client for all economic data sources
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
        

        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        time.sleep(self.rate_limit_delay)
        return response.json()
