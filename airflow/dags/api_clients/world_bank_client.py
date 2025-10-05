"""
World Bank API Client
"""

import pandas as pd
from .base_client import BaseAPIClient


class WorldBankClient(BaseAPIClient):
    """World Bank API client for development data"""
    
    def __init__(self):
        super().__init__(
            base_url='https://api.worldbank.org/v2',
            api_key=None
        )


def get_world_bank_client() -> WorldBankClient:
    return WorldBankClient()
