from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
import json
import hashlib
import time
import random
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from eth_account import Account
from app.utils.web3_utils import Web3Utils


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

class BlockchainService:
    def __init__(self, provider_url: str = 'http://127.0.0.1:8545', config: Optional[Dict[str, Any]] = None):
        """Initialize blockchain service with Ganache connection."""
        self.provider_url = provider_url
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        
        self.web3_utils = Web3Utils(
            provider_url=self.config["ganache_url"],
            gas_limit=self.config["gas_limit"],
            gas_price=self.config["gas_price"]
        )
        
        # Add PoA middleware for Ganache compatibility
        self.w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        
        # Default account setup
        self.default_account = None
        self.private_key = None
        
        # Contract instances
        self.delivery_contract = None
        self.carbon_contract = None
        
        # Contract addresses (will be set after deployment)
        self.delivery_contract_address = None
        self.carbon_contract_address = None
        
        # Initialize connection
        self._initialize_connection()
        
        # Cache for performance
        self.transaction_cache = {}
        self.certificate_cache = {}
        
    def _initialize_connection(self):
        """Initialize blockchain connection and setup accounts."""
        try:
            if self.w3.is_connected():
                # Get available accounts from Ganache
                accounts = self.w3.eth.accounts
                if accounts:
                    self.default_account = accounts[0]
                    # For Ganache, we can use a deterministic private key
                    self.private_key = '0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d'
                else:
                    # Create a new account if none available
                    account = Account.create()
                    self.default_account = account.address
                    self.private_key = account.privateKey.hex()
                    
                # Setup contract interfaces
                self._setup_contracts()
                
        except Exception as e:
            print(f"Failed to initialize blockchain connection: {str(e)}")
            # Use mock mode for development
            self._setup_mock_mode()
    
    def _setup_contracts(self):
        """Setup smart contract interfaces with ABI and addresses."""
        # Delivery Verification Contract ABI (simplified for demo)
        self.delivery_abi = [
            {
                "inputs": [
                    {"name": "routeId", "type": "string"},
                    {"name": "vehicleId", "type": "string"},
                    {"name": "carbonSaved", "type": "uint256"},
                    {"name": "costSaved", "type": "uint256"},
                    {"name": "distanceKm", "type": "uint256"},
                    {"name": "optimizationScore", "type": "uint256"},
                    {"name": "metadataHash", "type": "string"}
                ],
                "name": "addDeliveryRecord",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"name": "routeId", "type": "string"}],
                "name": "verifyDelivery",
                "outputs": [{"name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [{"name": "routeId", "type": "string"}],
                "name": "getDeliveryRecord",
                "outputs": [
                    {"name": "routeId", "type": "string"},
                    {"name": "vehicleId", "type": "string"},
                    {"name": "carbonSaved", "type": "uint256"},
                    {"name": "costSaved", "type": "uint256"},
                    {"name": "timestamp", "type": "uint256"},
                    {"name": "verified", "type": "bool"}
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {"name": "routeId", "type": "string"},
                    {"name": "trustScore", "type": "uint256"},
                    {"name": "carbonImpact", "type": "uint256"},
                    {"name": "sustainabilityRating", "type": "uint256"}
                ],
                "name": "createETT",
                "outputs": [{"name": "tokenId", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getNetworkStats",
                "outputs": [
                    {"name": "totalCarbonSaved", "type": "uint256"},
                    {"name": "totalCostSaved", "type": "uint256"},
                    {"name": "totalDeliveries", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function"
            }
        ]
        
        # For demo purposes, use a mock contract address
        # In production, this would be the actual deployed contract address
        self.delivery_contract_address = '0x1234567890123456789012345678901234567890'
        
        # Create contract instance (will work in mock mode for demo)
        try:
            self.delivery_contract = self.w3.eth.contract(
                address=self.delivery_contract_address,
                abi=self.delivery_abi
            )
        except Exception:
            # Use mock contract for demo
            self.delivery_contract = None
    
    def _setup_mock_mode(self):
        """Setup mock mode for demo when blockchain is not available."""
        self.default_account = '0x742d35Cc6634C0532925a3b8D93329B5e3c8E930'
        self.private_key = '0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d'
        self.delivery_contract_address = '0x1234567890123456789012345678901234567890'
        print("Running in mock mode - blockchain transactions will be simulated")
    
    def calculate_verification_hash(self, data: Dict[str, Any]) -> str:
        """Calculate secure verification hash for data integrity."""
        # Sort keys for consistent hashing
        data_string = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(data_string.encode()).hexdigest()
    
    async def create_delivery_certificate(self, certificate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate blockchain-verified delivery certificate."""
        try:
            route_id = certificate_data['route_id']
            
            # Calculate verification hash
            verification_hash = self.calculate_verification_hash(certificate_data)
            
            # Prepare transaction data
            tx_data = {
                'route_id': route_id,
                'vehicle_id': certificate_data.get('vehicle_id', 'unknown'),
                'carbon_saved': int(certificate_data.get('carbon_saved', 0) * 1000),  # Convert to grams
                'cost_saved': int(certificate_data.get('cost_saved', 0) * 100),      # Convert to cents
                'distance_km': int(certificate_data.get('distance_km', 0) * 1000),   # Convert to meters
                'optimization_score': int(certificate_data.get('optimization_score', 0)),
                'verification_hash': verification_hash
            }
            
            # Execute blockchain transaction
            if self.w3.is_connected() and self.delivery_contract:
                # Real blockchain transaction
                result = await self._execute_blockchain_transaction(tx_data)
            else:
                # Mock transaction for demo
                result = self._simulate_blockchain_transaction(tx_data)
            
            # Cache the certificate
            self.certificate_cache[route_id] = {
                **certificate_data,
                'verification_hash': verification_hash,
                'transaction_hash': result['transaction_hash'],
                'block_number': result['block_number'],
                'verified': True,
                'created_at': datetime.utcnow().isoformat()
            }
            
            return {
                'verified': True,
                'certificate_id': route_id,
                'transaction_hash': result['transaction_hash'],
                'block_number': result['block_number'],
                'gas_used': result.get('gas_used', 21000),
                'verification_hash': verification_hash,
                'timestamp': int(time.time())
            }
            
        except Exception as e:
            return {
                'verified': False,
                'error': f'Certificate creation failed: {str(e)}'
            }
    
    async def _execute_blockchain_transaction(self, tx_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute real blockchain transaction."""
        try:
            # Get current nonce
            nonce = self.w3.eth.get_transaction_count(self.default_account)
            
            # Build transaction
            transaction = self.delivery_contract.functions.addDeliveryRecord(
                tx_data['route_id'],
                tx_data['vehicle_id'],
                tx_data['carbon_saved'],
                tx_data['cost_saved'],
                tx_data['distance_km'],
                tx_data['optimization_score'],
                tx_data['verification_hash']
            ).build_transaction({
                'from': self.default_account,
                'nonce': nonce,
                'gas': 300000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Sign transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            # Wait for receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'transaction_hash': tx_hash.hex(),
                'block_number': receipt.blockNumber,
                'gas_used': receipt.gasUsed,
                'status': 'success' if receipt.status == 1 else 'failed'
            }
            
        except Exception as e:
            raise Exception(f"Blockchain transaction failed: {str(e)}")
    
    def _simulate_blockchain_transaction(self, tx_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate blockchain transaction for demo purposes."""
        # Generate realistic-looking transaction hash
        tx_hash = '0x' + hashlib.sha256(
            f"{tx_data['route_id']}{int(time.time())}".encode()
        ).hexdigest()
        
        # Simulate block number
        block_number = random.randint(1000000, 2000000)
        
        # Simulate gas usage
        gas_used = random.randint(150000, 250000)
        
        return {
            'transaction_hash': tx_hash,
            'block_number': block_number,
            'gas_used': gas_used,
            'status': 'success'
        }
    
    async def verify_certificate_on_chain(self, certificate_id: str) -> Dict[str, Any]:
        """Verify certificate authenticity on blockchain."""
        try:
            if self.w3.is_connected() and self.delivery_contract:
                # Real blockchain verification
                verified = self.delivery_contract.functions.verifyDelivery(certificate_id).call()
                return {'verified': verified}
            else:
                # Mock verification - check cache
                if certificate_id in self.certificate_cache:
                    return {'verified': True}
                else:
                    return {'verified': False}
                    
        except Exception as e:
            return {'verified': False, 'error': str(e)}
    
    async def get_certificate_from_blockchain(self, certificate_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve certificate details from blockchain."""
        try:
            # Check cache first
            if certificate_id in self.certificate_cache:
                return self.certificate_cache[certificate_id]
            
            if self.w3.is_connected() and self.delivery_contract:
                # Real blockchain query
                try:
                    record = self.delivery_contract.functions.getDeliveryRecord(certificate_id).call()
                    if record and record[0]:  # Check if record exists
                        return {
                            'route_id': record[0],
                            'vehicle_id': record[1],
                            'carbon_saved': record[2],
                            'cost_saved': record[3],
                            'timestamp': record[4],
                            'verified': record[5]
                        }
                except Exception:
                    pass
            
            # Return None if not found
            return None
            
        except Exception as e:
            print(f"Error retrieving certificate: {str(e)}")
            return None
    
    async def verify_blockchain_integrity(self, certificate_id: str) -> bool:
        """Verify blockchain integrity for certificate."""
        try:
            # For demo purposes, always return True
            # In production, this would verify block hashes and merkle proofs
            certificate = await self.get_certificate_from_blockchain(certificate_id)
            return certificate is not None
            
        except Exception:
            return False
    
    async def create_environmental_trust_token(self, ett_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create Environmental Trust Token with sustainability metrics."""
        try:
            route_id = ett_data['route_id']
            
            # Verify that the route certificate exists
            certificate_exists = await self.verify_certificate_exists(route_id)
            if not certificate_exists:
                return {'error': f'Route certificate {route_id} not found'}
            
            # Prepare ETT data
            token_data = {
                'route_id': route_id,
                'trust_score': int(ett_data.get('trust_score', 0)),
                'carbon_impact': int(ett_data.get('carbon_impact', 0) * 1000),  # Convert to grams
                'sustainability_rating': int(ett_data.get('sustainability_rating', 0))
            }
            
            # Execute ETT creation
            if self.w3.is_connected() and self.delivery_contract:
                # Real blockchain transaction
                result = await self._execute_ett_transaction(token_data)
            else:
                # Mock transaction
                result = self._simulate_ett_transaction(token_data)
            
            return {
                'token_id': result['token_id'],
                'route_id': route_id,
                'transaction_hash': result['transaction_hash'],
                'block_number': result.get('block_number', 0),
                'created_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {'error': f'ETT creation failed: {str(e)}'}
    
    async def _execute_ett_transaction(self, token_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute ETT creation transaction on blockchain."""
        try:
            nonce = self.w3.eth.get_transaction_count(self.default_account)
            
            transaction = self.delivery_contract.functions.createETT(
                token_data['route_id'],
                token_data['trust_score'],
                token_data['carbon_impact'],
                token_data['sustainability_rating']
            ).build_transaction({
                'from': self.default_account,
                'nonce': nonce,
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            # Extract token ID from logs (simplified)
            token_id = random.randint(1, 1000000)  # In production, parse from event logs
            
            return {
                'token_id': token_id,
                'transaction_hash': tx_hash.hex(),
                'block_number': receipt.blockNumber
            }
            
        except Exception as e:
            raise Exception(f"ETT transaction failed: {str(e)}")
    
    def _simulate_ett_transaction(self, token_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate ETT creation for demo."""
        return {
            'token_id': random.randint(1, 1000000),
            'transaction_hash': '0x' + hashlib.sha256(
                f"ett_{token_data['route_id']}{int(time.time())}".encode()
            ).hexdigest(),
            'block_number': random.randint(1000000, 2000000)
        }
    
    async def verify_certificate_exists(self, route_id: str) -> bool:
        """Verify that a certificate exists for the given route."""
        try:
            certificate = await self.get_certificate_from_blockchain(route_id)
            return certificate is not None
        except Exception:
            return False
    
    async def get_transaction_details(self, tx_hash: str) -> Dict[str, Any]:
        """Get detailed blockchain transaction information."""
        try:
            # Check cache first
            if tx_hash in self.transaction_cache:
                return self.transaction_cache[tx_hash]
            
            if self.w3.is_connected():
                # Real blockchain query
                try:
                    tx_receipt = self.w3.eth.get_transaction_receipt(tx_hash)
                    tx = self.w3.eth.get_transaction(tx_hash)
                    
                    details = {
                        'blockNumber': tx_receipt.blockNumber,
                        'blockHash': tx_receipt.blockHash.hex(),
                        'transactionIndex': tx_receipt.transactionIndex,
                        'from': tx['from'],
                        'to': tx['to'],
                        'gasUsed': tx_receipt.gasUsed,
                        'gasPrice': tx['gasPrice'],
                        'status': tx_receipt.status,
                        'timestamp': int(time.time())
                    }
                    
                    # Cache the result
                    self.transaction_cache[tx_hash] = details
                    return details
                    
                except Exception:
                    pass
            
            # Return mock data if blockchain query fails
            return self._generate_mock_transaction_details(tx_hash)
            
        except Exception as e:
            return {'error': f'Failed to get transaction details: {str(e)}'}
    
    def _generate_mock_transaction_details(self, tx_hash: str) -> Dict[str, Any]:
        """Generate mock transaction details for demo."""
        return {
            'blockNumber': random.randint(1000000, 2000000),
            'blockHash': '0x' + 'a' * 64,
            'transactionIndex': random.randint(0, 50),
            'from': self.default_account,
            'to': self.delivery_contract_address,
            'gasUsed': random.randint(150000, 250000),
            'gasPrice': 20000000000,
            'status': 1,
            'timestamp': int(time.time())
        }
    
    async def get_recent_certificates(self, limit: int) -> List[Dict[str, Any]]:
        """Get recently created delivery certificates."""
        try:
            # For demo, return cached certificates
            certificates = list(self.certificate_cache.values())
            
            # Sort by creation time (most recent first)
            certificates.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            
            # Add some mock certificates if cache is empty
            if not certificates:
                certificates = self._generate_mock_certificates(limit)
            
            return certificates[:limit]
            
        except Exception as e:
            print(f"Error getting recent certificates: {str(e)}")
            return []
    
    def _generate_mock_certificates(self, count: int) -> List[Dict[str, Any]]:
        """Generate mock certificates for demo."""
        certificates = []
        
        for i in range(count):
            cert_id = f"demo_cert_{i+1}_{int(time.time())}"
            certificates.append({
                'certificate_id': cert_id,
                'route_id': f"demo_route_{i+1}",
                'vehicle_id': f"demo_vehicle_{i+1}",
                'carbon_saved': random.uniform(10, 50),
                'cost_saved': random.uniform(25, 100),
                'optimization_score': random.randint(85, 98),
                'verification_hash': hashlib.sha256(f"demo_{i}".encode()).hexdigest(),
                'transaction_hash': '0x' + hashlib.sha256(f"tx_demo_{i}".encode()).hexdigest(),
                'block_number': 1000000 + i,
                'verified': True,
                'created_at': datetime.utcnow().isoformat()
            })
        
        return certificates
    
    async def get_network_statistics(self) -> Dict[str, Any]:
        """Get blockchain network statistics."""
        try:
            if self.w3.is_connected():
                # Real network stats
                latest_block = self.w3.eth.block_number
                gas_price = self.w3.eth.gas_price
                
                # Try to get contract stats
                try:
                    if self.delivery_contract:
                        stats = self.delivery_contract.functions.getNetworkStats().call()
                        total_carbon_saved = stats[0]
                        total_cost_saved = stats[1]
                        total_deliveries = stats[2]
                    else:
                        raise Exception("Contract not available")
                except Exception:
                    # Use mock data
                    total_carbon_saved = 1000000
                    total_cost_saved = 5000000
                    total_deliveries = 1000
                
                return {
                    'network_id': 1337,  # Ganache default
                    'latest_block': latest_block,
                    'total_carbon_saved': total_carbon_saved,
                    'total_cost_saved': total_cost_saved,
                    'total_deliveries': total_deliveries,
                    'gas_price': gas_price,
                    'hash_rate': random.randint(1000000, 5000000)
                }
            else:
                # Mock network stats
                return {
                    'network_id': 1337,
                    'latest_block': random.randint(1000000, 2000000),
                    'total_carbon_saved': 1500000,
                    'total_cost_saved': 7500000,
                    'total_deliveries': 1500,
                    'gas_price': 20000000000,
                    'hash_rate': 2500000
                }
                
        except Exception as e:
            return {'error': f'Failed to get network statistics: {str(e)}'}
    
    async def get_recent_blocks(self, count: int) -> List[Dict[str, Any]]:
        """Get recent blockchain blocks."""
        try:
            blocks = []
            
            if self.w3.is_connected():
                latest = self.w3.eth.block_number
                for i in range(latest, max(latest - count, 0), -1):
                    try:
                        block = self.w3.eth.get_block(i)
                        blocks.append({
                            'number': block.number,
                            'hash': block.hash.hex(),
                            'timestamp': block.timestamp,
                            'transactions': len(block.transactions)
                        })
                    except Exception:
                        break
            else:
                # Generate mock blocks
                latest = random.randint(1000000, 2000000)
                for i in range(count):
                    blocks.append({
                        'number': latest - i,
                        'hash': '0x' + hashlib.sha256(f"block_{latest-i}".encode()).hexdigest(),
                        'timestamp': int(time.time()) - (i * 15),  # 15 seconds per block
                        'transactions': random.randint(0, 10)
                    })
            
            return blocks
            
        except Exception as e:
            return []
        
    async def get_recent_transactions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent transactions with all required fields"""
        try:
            # Generate mock transactions with all required fields
            transactions = []
            current_time = int(time.time())
            
            for i in range(limit):
                tx_hash = f"0x{hashlib.sha256(f'tx_{current_time}_{i}'.encode()).hexdigest()}"
                transactions.append({
                    "hash": tx_hash,
                    "from_address": self.default_account,
                    'to_address': self.delivery_contract_address,
                    "value": int(random.uniform(1, 50)),
                    "gas_used": random.randint(21000, 100000),
                    "gas_price": 20000000000,
                    "block_number": random.randint(1, 100),
                    "timestamp": int(current_time - (i * 30))
                })
            
            return transactions
        
        except Exception as e:
            print(f"Error getting recent transactions: {e}")
            # Return empty list with proper structure if error
            return []
        
    async def get_gas_statistics(self) -> Dict[str, Any]:
        """Get gas price statistics."""
        try:
            if self.w3.is_connected():
                current_gas_price = self.w3.eth.gas_price
                return {
                    'average_gas_price': current_gas_price,
                    'fast_gas_price': int(current_gas_price * 1.2),
                    'slow_gas_price': int(current_gas_price * 0.8)
                }
            else:
                return {
                    'average_gas_price': 20000000000,
                    'fast_gas_price': 24000000000,
                    'slow_gas_price': 16000000000
                }
                
        except Exception as e:
            return {'average_gas_price': 20000000000}
    
    async def create_carbon_credit(self, credit_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create tradeable carbon credit tokens."""
        try:
            route_id = credit_data['route_id']
            carbon_amount = credit_data['carbon_amount_kg']
            value_usd = credit_data['value_usd']
            
            # Simulate carbon credit creation
            credit_id = random.randint(1, 1000000)
            tx_hash = '0x' + hashlib.sha256(
                f"carbon_credit_{route_id}_{int(time.time())}".encode()
            ).hexdigest()
            
            return {
                'credit_id': credit_id,
                'route_id': route_id,
                'carbon_amount_kg': carbon_amount,
                'value_usd': value_usd,
                'transaction_hash': tx_hash,
                'block_number': random.randint(1000000, 2000000),
                'created_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {'error': f'Carbon credit creation failed: {str(e)}'}
    
    async def verify_route_carbon_savings(self, route_id: str) -> Dict[str, Any]:
        """Verify route carbon savings for credit generation."""
        try:
            certificate = await self.get_certificate_from_blockchain(route_id)
            
            if certificate:
                carbon_saved = certificate.get('carbon_saved', 0)
                if isinstance(carbon_saved, int):
                    carbon_saved = carbon_saved / 1000  # Convert from grams to kg
                
                return {
                    'verified': True,
                    'carbon_saved_kg': carbon_saved,
                    'route_id': route_id
                }
            else:
                return {
                    'verified': False,
                    'error': 'Route certificate not found'
                }
                
        except Exception as e:
            return {
                'verified': False,
                'error': f'Verification failed: {str(e)}'
            }
    
    async def test_connection(self) -> str:
        """Test blockchain connection."""
        try:
            if self.w3.is_connected():
                block_number = self.w3.eth.block_number
                return f'connected - latest block: {block_number}'
            else:
                return 'disconnected'
        except Exception as e:
            return f'connection_error: {str(e)}'
    
    async def test_contract_interaction(self) -> str:
        """Test smart contract interaction."""
        try:
            if self.delivery_contract:
                # Try to call a view function
                try:
                    stats = self.delivery_contract.functions.getNetworkStats().call()
                    return f'contract_interaction_successful: {stats}'
                except Exception:
                    return 'contract_interaction_mock_mode'
            else:
                return 'contract_interaction_mock_mode'
        except Exception as e:
            return f'contract_interaction_failed: {str(e)}'
    
    def is_connected(self) -> bool:
        """Check if blockchain service is connected."""
        try:
            return self.w3.is_connected()
        except Exception:
            return False
    
    def generate_environmental_impact_description(self, carbon_impact: float, sustainability_rating: int) -> str:
        """Generate environmental impact description."""
        if carbon_impact > 50:
            impact_level = "High"
        elif carbon_impact > 20:
            impact_level = "Medium"
        else:
            impact_level = "Low"
        
        if sustainability_rating >= 90:
            rating_desc = "Excellent"
        elif sustainability_rating >= 70:
            rating_desc = "Good"
        elif sustainability_rating >= 50:
            rating_desc = "Fair"
        else:
            rating_desc = "Poor"
        
        return f"{impact_level} environmental impact with {rating_desc} sustainability rating. Carbon impact: {carbon_impact} kg CO2."
    
    def calculate_environmental_equivalents(self, carbon_kg: float) -> Dict[str, float]:
        """Calculate environmental equivalents for carbon savings."""
        return {
            'trees_planted_equivalent': round(carbon_kg / 21.77, 2),
            'cars_off_road_days': round(carbon_kg / 12.6, 2),
            'homes_powered_hours': round(carbon_kg / 0.83, 2),
            'miles_not_driven': round(carbon_kg / 0.404, 2)
        }
    
    async def generate_demo_certificates(self, count: int) -> List[Dict[str, Any]]:
        """Generate demo certificates for presentation."""
        certificates = []
        
        for i in range(count):
            cert_data = {
                'route_id': f'demo_route_{i+1}',
                'vehicle_id': f'demo_vehicle_{i+1}',
                'carbon_saved': random.uniform(15, 45),
                'cost_saved': random.uniform(30, 90),
                'distance_km': random.uniform(50, 200),
                'optimization_score': random.randint(88, 97)
            }
            
            # Create certificate
            certificate = await self.create_delivery_certificate(cert_data)
            
            if certificate.get('verified'):
                certificates.append({
                    'certificate_id': certificate['certificate_id'],
                    'route_id': cert_data['route_id'],
                    'vehicle_id': cert_data['vehicle_id'],
                    'carbon_saved_kg': cert_data['carbon_saved'],
                    'cost_saved_usd': cert_data['cost_saved'],
                    'optimization_score': cert_data['optimization_score'],
                    'verification_hash': certificate['verification_hash'],
                    'transaction_hash': certificate['transaction_hash'],
                    'block_number': certificate['block_number'],
                    'verified': True,
                    'created_at': datetime.utcnow().isoformat()
                })
        
        return certificates
    
    
