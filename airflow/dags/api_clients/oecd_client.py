"""
OECD API Client
"""

import pandas as pd
from .base_client import BaseAPIClient


class OECDClient(BaseAPIClient):
    """OECD API client for economic data"""
    
    def __init__(self):
        super().__init__(
            base_url='https://sdmx.oecd.org/public/rest/data',
            api_key=None
        )


def get_oecd_client() -> OECDClient:
    return OECDClient()
