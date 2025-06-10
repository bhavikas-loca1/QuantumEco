"""
QuantumEco Intelligence Blockchain Interface Package

This package provides blockchain functionality for the QuantumEco Intelligence platform,
handling smart contract interactions, certificate creation, and Environmental Trust Tokens.

Compatible with Python 3.7-3.11 for Web3.py and solcx compatibility.
"""

__version__ = "1.0.0"
__author__ = "QuantumEco Intelligence Team"

# Import main components for easy access
from .blockchain_service import BlockchainService
from .contract_interface import ContractInterface
from .web3_utils import Web3Utils
from .api_server import app as blockchain_api

# Package-level configuration
DEFAULT_CONFIG = {
    "ganache_url": "http://127.0.0.1:8545",
    "api_port": 8546,
    "gas_limit": 300000,
    "gas_price": 20000000000,  # 20 Gwei
    "chain_id": 1337,  # Ganache default
    "confirmation_blocks": 1,
    "timeout": 60
}

# Contract addresses (will be updated after deployment)
CONTRACT_ADDRESSES = {
    "delivery_verification": None,
    "environmental_trust_token": None,
    "carbon_credit_token": None
}

# ABI cache for contract interfaces
ABI_CACHE = {}

def initialize_blockchain_interface(config=None):
    """Initialize the blockchain interface with custom configuration"""
    global DEFAULT_CONFIG
    if config:
        DEFAULT_CONFIG.update(config)
    
    print(f"🚀 QuantumEco Blockchain Interface v{__version__} initialized")
    print(f"📡 Ganache URL: {DEFAULT_CONFIG['ganache_url']}")
    print(f"🔌 API Port: {DEFAULT_CONFIG['api_port']}")
    
    return DEFAULT_CONFIG

def get_health_status():
    """Get overall health status of blockchain interface"""
    try:
        service = BlockchainService()
        return {
            "status": "healthy",
            "version": __version__,
            "ganache_connected": service.is_connected(),
            "contracts_loaded": len(ABI_CACHE) > 0,
            "api_running": True
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "version": __version__,
            "error": str(e)
        }

# Export all main components
__all__ = [
    "BlockchainService",
    "ContractInterface", 
    "Web3Utils",
    "blockchain_api",
    "initialize_blockchain_interface",
    "get_health_status",
    "DEFAULT_CONFIG",
    "CONTRACT_ADDRESSES"
]
