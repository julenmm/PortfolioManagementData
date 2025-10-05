"""
EIA (Energy Information Administration) API Client
"""

import pandas as pd
from .base_client import BaseAPIClient


class EIAClient(BaseAPIClient):
    """EIA API client for energy data"""
    
    def __init__(self):
        super().__init__(
            base_url='https://api.eia.gov/v2',
            api_key=None
        )


def get_eia_client() -> EIAClient:
    return EIAClient()
