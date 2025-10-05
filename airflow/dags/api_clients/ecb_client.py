"""
ECB (European Central Bank) API Client
"""

import pandas as pd
from .base_client import BaseAPIClient


class ECBClient(BaseAPIClient):
    """ECB API client for European economic data"""
    
    def __init__(self):
        super().__init__(
            base_url='https://sdw-wsrest.ecb.europa.eu/service',
            api_key=None
        )


def get_ecb_client() -> ECBClient:
    return ECBClient()
