"""
BLS (Bureau of Labor Statistics) API Client
"""

import pandas as pd
from .base_client import BaseAPIClient


class BLSClient(BaseAPIClient):
    """BLS API client for labor statistics"""
    
    def __init__(self):
        super().__init__(
            base_url='https://api.bls.gov/publicAPI/v2',
            api_key=None
        )


def get_bls_client() -> BLSClient:
    return BLSClient()
