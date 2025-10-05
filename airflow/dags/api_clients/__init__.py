"""
API Clients for Economic Data Sources
"""

from .base_client import BaseAPIClient
from .fred_client import FREDClient, get_fred_client
from .yfinance_client import YFinanceClient, get_yfinance_client
from .bls_client import BLSClient, get_bls_client
from .oecd_client import OECDClient, get_oecd_client
from .imf_client import IMFClient, get_imf_client
from .eia_client import EIAClient, get_eia_client
from .nasdaq_client import NASDAQClient, get_nasdaq_client
from .ecb_client import ECBClient, get_ecb_client
from .world_bank_client import WorldBankClient, get_world_bank_client

__all__ = [
    'BaseAPIClient',
    'FREDClient', 'get_fred_client',
    'YFinanceClient', 'get_yfinance_client',
    'BLSClient', 'get_bls_client',
    'OECDClient', 'get_oecd_client',
    'IMFClient', 'get_imf_client',
    'EIAClient', 'get_eia_client',
    'NASDAQClient', 'get_nasdaq_client',
    'ECBClient', 'get_ecb_client',
    'WorldBankClient', 'get_world_bank_client',
]
