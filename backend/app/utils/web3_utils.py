"""
Web3 Utility Functions for QuantumEco Intelligence

Provides low-level Web3.py utilities for blockchain interaction including
transaction management, account handling, and network operations.
"""

import time
import logging
from typing import Dict, Any, List, Optional, Union
from web3 import Web3
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from eth_account import Account

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Web3Utils:
    """
    Web3 utility class for blockchain operations
    
    Provides low-level Web3 functionality including:
    - Connection management
    - Transaction signing and sending
    - Gas estimation and optimization
    - Account management
    - Network monitoring
    """
    
    def __init__(self, provider_url: str = "http://127.0.0.1:8545", 
                 gas_limit: int = 300000, gas_price: int = 20000000000):
        """Initialize Web3 utilities"""
        self.provider_url = provider_url
        self.gas_limit = gas_limit
        self.gas_price = gas_price
        
        # Initialize Web3 connection
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        
        # Add PoA middleware for Ganache compatibility
        self.w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        
        # Account management
        self.default_account = None
        self.private_key = None
        self.accounts = []
        
        # Connection state
        self._connected = False
        
        # Performance metrics
        self.metrics = {
            "transactions_sent": 0,
            "total_gas_used": 0,
            "average_gas_price": gas_price,
            "connection_uptime": 0,
            "last_block_time": 0
        }
        
        # Initialize connection
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize Web3 connection and account setup"""
        try:
            # Test connection
            if self.w3:
                self._connected = True
                logger.info(f"✅ Connected to blockchain at {self.provider_url}")
                
                # Get available accounts
                self.accounts = self.w3.eth.accounts
                if self.accounts:
                    self.default_account = self.accounts[0]
                    logger.info(f"🔑 Default account: {self.default_account}")
                else:
                    logger.warning("⚠️ No accounts available")
                
                # Set default private key for Ganache
                self._set_default_private_key()
                
                # Initialize metrics
                self.metrics["connection_uptime"] = time.time()
                
            else:
                self._connected = False
                logger.error("❌ Failed to connect to blockchain")
                
        except Exception as e:
            logger.error(f"Connection initialization failed: {str(e)}")
            self._connected = False
    
    def _set_default_private_key(self):
        """Set default private key for Ganache deterministic accounts"""
        # Ganache deterministic private key for account[0]
        ganache_private_keys = [
            "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d",
            "0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1",
            "0x6370fd033278c143179d81c5526140625662b8daa446c22ee2d73db3707e620c"
        ]
        
        if self.accounts:
            try:
                # Use first available private key
                self.private_key = ganache_private_keys[0]
                
                # Verify the private key matches the account
                account = Account.from_key(self.private_key)
                if account.address.lower() == self.default_account.lower():
                    logger.info("✅ Private key verified for default account")
                else:
                    logger.warning("⚠️ Private key mismatch - transactions may fail")
                    
            except Exception as e:
                logger.warning(f"Private key setup failed: {str(e)}")
    
    # ===== CONNECTION MANAGEMENT =====
    
    def is_connected(self) -> bool:
        """Check if Web3 is connected to blockchain"""
        try:
            return bool(self._connected and self.w3)
        except:
            return False
    
    def reconnect(self) -> bool:
        """Attempt to reconnect to blockchain"""
        try:
            self.w3 = Web3(Web3.HTTPProvider(self.provider_url))
            self.w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
            
            if self.w3:
                self._connected = True
                logger.info("✅ Reconnected to blockchain")
                return True
            else:
                self._connected = False
                return False
                
        except Exception as e:
            logger.error(f"Reconnection failed: {str(e)}")
            self._connected = False
            return False
    
    def get_connection_status(self) -> Dict[str, Any]:
        """Get detailed connection status"""
        try:
            if not self.is_connected():
                return {
                    "connected": False,
                    "provider_url": self.provider_url,
                    "error": "Not connected to blockchain"
                }
            
            latest_block = self.w3.eth.get_block('latest')
            
            return {
                "connected": True,
                "provider_url": self.provider_url,
                "network_id": self.w3.net.version,
                "chain_id": self.w3.eth.chain_id,
                "latest_block": latest_block.number,
                "gas_price": self.w3.eth.gas_price,
                "account_count": len(self.accounts),
                "default_account": self.default_account,
                "uptime": time.time() - self.metrics["connection_uptime"]
            }
            
        except Exception as e:
            return {
                "connected": False,
                "provider_url": self.provider_url,
                "error": str(e)
            }
    
    # ===== ACCOUNT MANAGEMENT =====
    
    def create_account(self) -> Dict[str, str]:
        """Create a new Ethereum account"""
        try:
            account = Account.create()
            return {
                "address": account.address,
                "private_key": account.privateKey.hex(),
                "created_at": int(time.time())
            }
        except Exception as e:
            logger.error(f"Account creation failed: {str(e)}")
            return {"error": str(e)}
    
    def get_account_balance(self, account: Optional[str] = None) -> int:
        """Get account balance in wei"""
        try:
            if not self.is_connected():
                return 0
            
            account_address = account or self.default_account
            if not account_address:
                return 0
            
            return self.w3.eth.get_balance(account_address)
            
        except Exception as e:
            logger.error(f"Failed to get balance: {str(e)}")
            return 0
    
    def get_account_nonce(self, account: Optional[str] = None) -> int:
        """Get account nonce (transaction count)"""
        try:
            if not self.is_connected():
                return 0
            
            account_address = account or self.default_account
            if not account_address:
                return 0
            
            return self.w3.eth.get_transaction_count(account_address)
            
        except Exception as e:
            logger.error(f"Failed to get nonce: {str(e)}")
            return 0
    
    # ===== TRANSACTION MANAGEMENT =====
    
    def estimate_gas(self, transaction: Dict[str, Any]) -> int:
        """Estimate gas required for transaction"""
        try:
            if not self.is_connected():
                return self.gas_limit
            
            estimated_gas = self.w3.eth.estimate_gas(transaction)
            
            # Add 20% buffer for safety
            return int(estimated_gas * 1.2)
            
        except Exception as e:
            logger.warning(f"Gas estimation failed: {str(e)}")
            return self.gas_limit
    
    def get_optimal_gas_price(self) -> int:
        """Get optimal gas price for current network conditions"""
        try:
            if not self.is_connected():
                return self.gas_price
            
            current_gas_price = self.w3.eth.gas_price
            
            # For Ganache, use fixed price
            # For mainnet, could implement more sophisticated logic
            return current_gas_price
            
        except Exception as e:
            logger.warning(f"Gas price optimization failed: {str(e)}")
            return self.gas_price
    
    def build_transaction(self, to_address: str, data: str = "", 
                         value: int = 0, gas_limit: Optional[int] = None) -> Dict[str, Any]:
        """Build transaction dictionary"""
        try:
            if not self.default_account:
                raise ValueError("No default account available")
            
            # Get current nonce
            nonce = self.get_account_nonce()
            
            # Build transaction
            transaction = {
                'from': self.default_account,
                'to': to_address,
                'value': value,
                'nonce': nonce,
                'gas': gas_limit or self.gas_limit,
                'gasPrice': self.get_optimal_gas_price(),
                'data': data
            }
            
            # Estimate gas if not provided
            if not gas_limit:
                transaction['gas'] = self.estimate_gas(transaction)
            
            return transaction
            
        except Exception as e:
            logger.error(f"Transaction building failed: {str(e)}")
            raise
    
    def sign_transaction(self, transaction: Dict[str, Any]) -> Any:
        """Sign transaction with private key"""
        try:
            if not self.private_key:
                raise ValueError("No private key available for signing")
            
            # Sign transaction
            signed_tx = self.w3.eth.account.sign_transaction(
                transaction, 
                private_key=self.private_key
            )
            
            return signed_tx
            
        except Exception as e:
            logger.error(f"Transaction signing failed: {str(e)}")
            raise
    
    def send_transaction(self, transaction: Dict[str, Any]) -> str:
        """Sign and send transaction"""
        try:
            if not self.is_connected():
                raise ValueError("Not connected to blockchain")
            
            # Sign transaction
            signed_tx = self.sign_transaction(transaction)
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            # Update metrics
            self.metrics["transactions_sent"] += 1
            
            logger.info(f"✅ Transaction sent: {tx_hash.hex()}")
            return tx_hash.hex()
            
        except Exception as e:
            logger.error(f"Transaction sending failed: {str(e)}")
            raise
    
    def wait_for_transaction_receipt(self, tx_hash: str, timeout: int = 60) -> Dict[str, Any]:
        """Wait for transaction confirmation"""
        try:
            if not self.is_connected():
                raise ValueError("Not connected to blockchain")
            
            # Wait for receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(
                tx_hash, 
                timeout=timeout
            )
            
            # Update metrics
            self.metrics["total_gas_used"] += receipt.gasUsed
            
            return dict(receipt)
            
        except Exception as e:
            logger.error(f"Transaction receipt failed: {str(e)}")
            raise
    
    def get_transaction_details(self, tx_hash: str) -> Dict[str, Any]:
        """Get transaction details"""
        try:
            if not self.is_connected():
                return {"error": "Not connected to blockchain"}
            
            tx = self.w3.eth.get_transaction(tx_hash)
            return dict(tx)
            
        except Exception as e:
            logger.error(f"Failed to get transaction details: {str(e)}")
            return {"error": str(e)}
    
    def get_transaction_receipt(self, tx_hash: str) -> Dict[str, Any]:
        """Get transaction receipt"""
        try:
            if not self.is_connected():
                return {"error": "Not connected to blockchain"}
            
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            return dict(receipt)
            
        except Exception as e:
            logger.error(f"Failed to get transaction receipt: {str(e)}")
            return {"error": str(e)}
    
    # ===== BLOCK AND NETWORK OPERATIONS =====
    
    def get_latest_block(self) -> Dict[str, Any]:
        """Get latest block information"""
        try:
            if not self.is_connected():
                return {"error": "Not connected to blockchain"}
            
            block = self.w3.eth.get_block('latest')
            self.metrics["last_block_time"] = block.timestamp
            
            return {
                "number": block.number,
                "hash": block.hash.hex(),
                "timestamp": block.timestamp,
                "transactions": len(block.transactions),
                "gas_used": block.gasUsed,
                "gas_limit": block.gasLimit,
                "difficulty": block.difficulty
            }
            
        except Exception as e:
            logger.error(f"Failed to get latest block: {str(e)}")
            return {"error": str(e)}
    
    def get_block_by_number(self, block_number: int) -> Dict[str, Any]:
        """Get block by number"""
        try:
            if not self.is_connected():
                return {"error": "Not connected to blockchain"}
            
            block = self.w3.eth.get_block(block_number)
            
            return {
                "number": block.number,
                "hash": block.hash.hex(),
                "timestamp": block.timestamp,
                "transactions": [tx.hex() for tx in block.transactions],
                "gas_used": block.gasUsed,
                "gas_limit": block.gasLimit
            }
            
        except Exception as e:
            logger.error(f"Failed to get block {block_number}: {str(e)}")
            return {"error": str(e)}
    
    def get_network_info(self) -> Dict[str, Any]:
        """Get comprehensive network information"""
        try:
            if not self.is_connected():
                return {"error": "Not connected to blockchain"}
            
            latest_block = self.get_latest_block()
            
            return {
                "network_id": self.w3.net.version,
                "chain_id": self.w3.eth.chain_id,
                "client_version": self.w3.clientVersion,
                "protocol_version": self.w3.eth.protocol_version,
                "syncing": self.w3.eth.syncing,
                "gas_price": self.w3.eth.gas_price,
                "accounts": self.accounts,
                "latest_block": latest_block,
                "coinbase": getattr(self.w3.eth, 'coinbase', None)
            }
            
        except Exception as e:
            logger.error(f"Failed to get network info: {str(e)}")
            return {"error": str(e)}
    
    # ===== UTILITY METHODS =====
    
    def wei_to_ether(self, wei_amount: int) -> float:
        """Convert wei to ether"""
        return self.w3.fromWei(wei_amount, 'ether')
    
    def ether_to_wei(self, ether_amount: float) -> int:
        """Convert ether to wei"""
        return self.w3.toWei(ether_amount, 'ether')
    
    def is_address(self, address: str) -> bool:
        """Check if string is valid Ethereum address"""
        return self.w3.isAddress(address)
    
    def to_checksum_address(self, address: str) -> str:
        """Convert address to checksum format"""
        try:
            return self.w3.toChecksumAddress(address)
        except:
            return address
    
    def keccak(self, data: str) -> str:
        """Calculate Keccak-256 hash"""
        return self.w3.keccak(text=data).hex()
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get Web3 performance metrics"""
        current_time = time.time()
        uptime = current_time - self.metrics["connection_uptime"]
        
        return {
            "transactions_sent": self.metrics["transactions_sent"],
            "total_gas_used": self.metrics["total_gas_used"],
            "average_gas_price": self.metrics["average_gas_price"],
            "connection_uptime": uptime,
            "transactions_per_minute": self.metrics["transactions_sent"] / max(uptime / 60, 1),
            "last_block_time": self.metrics["last_block_time"],
            "connected": self.is_connected()
        }
    
    def reset_metrics(self):
        """Reset performance metrics"""
        self.metrics = {
            "transactions_sent": 0,
            "total_gas_used": 0,
            "average_gas_price": self.gas_price,
            "connection_uptime": time.time(),
            "last_block_time": 0
        }
        logger.info("✅ Performance metrics reset")
    
    def cleanup(self):
        """Clean up Web3 connection and resources"""
        try:
            # Close provider if possible
            if hasattr(self.w3.provider, 'close'):
                self.w3.provider.close()
            
            self._connected = False
            logger.info("✅ Web3 utilities cleaned up")
            
        except Exception as e:
            logger.error(f"Cleanup failed: {str(e)}")
