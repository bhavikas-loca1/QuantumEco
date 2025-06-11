"""
QuantumEco Intelligence Blockchain Interface Package

This package provides blockchain functionality for the QuantumEco Intelligence platform,
handling smart contract interactions, certificate creation, and Environmental Trust Tokens.

Compatible with Python 3.7-3.11 for Web3.py and solcx compatibility.
"""

__version__ = "1.0.0"
__author__ = "QuantumEco Intelligence Team"

# Import main components for easy access
from .blockchain_service import BlockchainService, DEFAULT_CONFIG, CONTRACT_ADDRESSES, ABI_CACHE
from .contract_interface import ContractInterface
from .web3_utils import Web3Utils
from .api_server import app as blockchain_api


