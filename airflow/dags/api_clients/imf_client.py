"""
IMF API Client
"""

import pandas as pd
from .base_client import BaseAPIClient


class IMFClient(BaseAPIClient):
    """IMF API client for economic data"""
    
    def __init__(self):
        super().__init__(
            base_url='https://dataservices.imf.org/REST/SDMX_JSON.svc',
            api_key=None
        )


def get_imf_client() -> IMFClient:
    return IMFClient()
