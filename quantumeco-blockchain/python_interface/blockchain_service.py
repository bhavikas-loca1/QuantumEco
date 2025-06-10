"""
Main Blockchain Service for QuantumEco Intelligence

Handles all blockchain operations including certificate creation,
Environmental Trust Token management, and smart contract interactions.
"""

import asyncio
import json
import time
import hashlib
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta

from .contract_interface import ContractInterface
from .web3_utils import Web3Utils
from . import DEFAULT_CONFIG, CONTRACT_ADDRESSES

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BlockchainService:
    """
    Main blockchain service for QuantumEco Intelligence platform
    
    Provides high-level blockchain operations for:
    - Delivery certificate creation and verification
    - Environmental Trust Token (ETT) management
    - Carbon credit tokenization
    - Network statistics and monitoring
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize blockchain service with configuration"""
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        
        # Initialize core components
        self.web3_utils = Web3Utils(
            provider_url=self.config["ganache_url"],
            gas_limit=self.config["gas_limit"],
            gas_price=self.config["gas_price"]
        )
        
        self.contract_interface = ContractInterface(self.web3_utils)
        
        # Service state
        self._connected = False
        self._contracts_loaded = False
        self.last_health_check = None
        
        # Performance metrics
        self.metrics = {
            "certificates_created": 0,
            "ett_tokens_created": 0,
            "carbon_credits_issued": 0,
            "transactions_processed": 0,
            "total_gas_used": 0,
            "average_confirmation_time": 0
        }
        
        # Initialize connection
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize connection to blockchain and load contracts"""
        try:
            # Test Web3 connection
            if self.web3_utils.is_connected():
                self._connected = True
                logger.info("✅ Connected to Ganache blockchain")
                
                # Load contract interfaces
                self._load_contracts()
                
                # Perform initial health check
                self.health_check()
                
            else:
                logger.warning("⚠️ Failed to connect to Ganache - using mock mode")
                self._connected = False
                
        except Exception as e:
            logger.error(f"❌ Blockchain initialization failed: {str(e)}")
            self._connected = False
    
    def _load_contracts(self):
        """Load smart contract interfaces from deployment artifacts"""
        try:
            # Load DeliveryVerification contract
            delivery_contract = self.contract_interface.load_contract(
                "DeliveryVerification",
                CONTRACT_ADDRESSES.get("delivery_verification")
            )
            
            if delivery_contract:
                self._contracts_loaded = True
                logger.info("✅ Smart contracts loaded successfully")
            else:
                logger.warning("⚠️ Contracts not deployed - using mock responses")
                
        except Exception as e:
            logger.error(f"❌ Contract loading failed: {str(e)}")
            self._contracts_loaded = False
    
    # ===== MAIN SERVICE METHODS =====
    
    async def create_delivery_certificate(self, certificate_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create blockchain-verified delivery certificate
        
        Args:
            certificate_data: Dict containing:
                - route_id: Unique route identifier
                - vehicle_id: Vehicle identifier
                - carbon_saved: Carbon savings in kg
                - cost_saved: Cost savings in USD
                - distance_km: Distance traveled in km
                - optimization_score: Optimization quality score (0-100)
                
        Returns:
            Dict containing certificate details and blockchain proof
        """
        start_time = time.time()
        
        try:
            # Validate input data
            validation_result = self._validate_certificate_data(certificate_data)
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "error": validation_result["error"],
                    "certificate_id": None
                }
            
            # Check if we're connected to blockchain
            if not self._connected or not self._contracts_loaded:
                return self._create_mock_certificate(certificate_data)
            
            # Generate verification hash
            verification_hash = self._generate_verification_hash(certificate_data)
            
            # Prepare contract transaction
            tx_data = {
                "route_id": certificate_data["route_id"],
                "vehicle_id": certificate_data["vehicle_id"],
                "carbon_saved": int(certificate_data["carbon_saved"] * 1000),  # Convert to grams
                "cost_saved": int(certificate_data["cost_saved"] * 100),       # Convert to cents
                "distance_km": int(certificate_data["distance_km"] * 1000),   # Convert to meters
                "optimization_score": int(certificate_data["optimization_score"]),
                "verification_hash": verification_hash
            }
            
            # Execute blockchain transaction
            tx_result = await self.contract_interface.execute_contract_function(
                "DeliveryVerification",
                "addDeliveryRecord",
                tx_data
            )
            
            if tx_result["success"]:
                # Update metrics
                self.metrics["certificates_created"] += 1
                self.metrics["transactions_processed"] += 1
                self.metrics["total_gas_used"] += tx_result.get("gas_used", 0)
                
                confirmation_time = time.time() - start_time
                self._update_average_confirmation_time(confirmation_time)
                
                # Return certificate details
                return {
                    "success": True,
                    "certificate_id": certificate_data["route_id"],
                    "transaction_hash": tx_result["transaction_hash"],
                    "block_number": tx_result["block_number"],
                    "verification_hash": verification_hash,
                    "gas_used": tx_result["gas_used"],
                    "confirmation_time": confirmation_time,
                    "timestamp": int(time.time()),
                    "verified": True,
                    "blockchain_network": "ganache_local"
                }
            else:
                return {
                    "success": False,
                    "error": tx_result.get("error", "Transaction failed"),
                    "certificate_id": certificate_data["route_id"]
                }
                
        except Exception as e:
            logger.error(f"Certificate creation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "certificate_id": certificate_data.get("route_id")
            }
    
    async def create_environmental_trust_token(self, ett_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create Environmental Trust Token (ETT)
        
        Args:
            ett_data: Dict containing:
                - route_id: Associated route identifier
                - trust_score: Trust score (0-100)
                - carbon_impact: Carbon impact in kg
                - sustainability_rating: Sustainability rating (0-100)
                
        Returns:
            Dict containing ETT details and blockchain proof
        """
        try:
            # Validate ETT data
            if not self._validate_ett_data(ett_data):
                return {
                    "success": False,
                    "error": "Invalid ETT data provided"
                }
            
            # Check blockchain connection
            if not self._connected or not self._contracts_loaded:
                return self._create_mock_ett(ett_data)
            
            # Verify prerequisite delivery record exists
            verification_result = await self.verify_certificate(ett_data["route_id"])
            if not verification_result.get("verified"):
                return {
                    "success": False,
                    "error": "Delivery record must be verified before creating ETT"
                }
            
            # Prepare ETT transaction
            tx_data = {
                "route_id": ett_data["route_id"],
                "trust_score": int(ett_data["trust_score"]),
                "carbon_impact": int(ett_data["carbon_impact"] * 1000),  # Convert to grams
                "sustainability_rating": int(ett_data["sustainability_rating"])
            }
            
            # Execute ETT creation on blockchain
            tx_result = await self.contract_interface.execute_contract_function(
                "DeliveryVerification",
                "createETT",
                tx_data
            )
            
            if tx_result["success"]:
                # Extract token ID from transaction events
                token_id = self._extract_token_id_from_events(tx_result.get("events", []))
                
                # Update metrics
                self.metrics["ett_tokens_created"] += 1
                self.metrics["transactions_processed"] += 1
                
                return {
                    "success": True,
                    "token_id": token_id,
                    "route_id": ett_data["route_id"],
                    "trust_score": ett_data["trust_score"],
                    "carbon_impact": ett_data["carbon_impact"],
                    "sustainability_rating": ett_data["sustainability_rating"],
                    "transaction_hash": tx_result["transaction_hash"],
                    "block_number": tx_result["block_number"],
                    "timestamp": int(time.time()),
                    "active": True
                }
            else:
                return {
                    "success": False,
                    "error": tx_result.get("error", "ETT creation failed")
                }
                
        except Exception as e:
            logger.error(f"ETT creation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def verify_certificate(self, certificate_id: str) -> Dict[str, Any]:
        """
        Verify certificate authenticity on blockchain
        
        Args:
            certificate_id: Certificate/route identifier to verify
            
        Returns:
            Dict containing verification status and certificate details
        """
        try:
            if not self._connected or not self._contracts_loaded:
                return self._verify_mock_certificate(certificate_id)
            
            # Query blockchain for certificate
            verification_result = await self.contract_interface.call_contract_function(
                "DeliveryVerification",
                "verifyDelivery",
                {"route_id": certificate_id}
            )
            
            if verification_result["success"] and verification_result["result"]:
                # Get full certificate details
                certificate_details = await self.contract_interface.call_contract_function(
                    "DeliveryVerification",
                    "getDeliveryRecord",
                    {"route_id": certificate_id}
                )
                
                if certificate_details["success"]:
                    record = certificate_details["result"]
                    return {
                        "verified": True,
                        "certificate_id": certificate_id,
                        "route_id": record[0],
                        "vehicle_id": record[1],
                        "carbon_saved": record[2] / 1000,  # Convert from grams
                        "cost_saved": record[3] / 100,    # Convert from cents
                        "distance_km": record[4] / 1000,  # Convert from meters
                        "optimization_score": record[5],
                        "timestamp": record[6],
                        "verifier": record[7],
                        "verification_hash": record[9],
                        "blockchain_verified": True
                    }
            
            return {
                "verified": False,
                "certificate_id": certificate_id,
                "message": "Certificate not found on blockchain"
            }
            
        except Exception as e:
            logger.error(f"Certificate verification failed: {str(e)}")
            return {
                "verified": False,
                "certificate_id": certificate_id,
                "error": str(e)
            }
    
    async def create_carbon_credit(self, credit_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create tradeable carbon credit tokens
        
        Args:
            credit_data: Dict containing:
                - route_id: Associated route identifier
                - carbon_amount: Amount of carbon credits in kg
                - value_usd: USD value of credits
                - issuer: Credit issuer information
                
        Returns:
            Dict containing carbon credit details and blockchain proof
        """
        try:
            # Validate carbon credit data
            if not self._validate_carbon_credit_data(credit_data):
                return {
                    "success": False,
                    "error": "Invalid carbon credit data"
                }
            
            if not self._connected or not self._contracts_loaded:
                return self._create_mock_carbon_credit(credit_data)
            
            # Verify prerequisite delivery record
            verification_result = await self.verify_certificate(credit_data["route_id"])
            if not verification_result.get("verified"):
                return {
                    "success": False,
                    "error": "Delivery record must be verified before issuing carbon credits"
                }
            
            # Prepare carbon credit transaction
            tx_data = {
                "route_id": credit_data["route_id"],
                "carbon_amount": int(credit_data["carbon_amount"] * 1000),  # Convert to grams
                "value_usd": int(credit_data["value_usd"] * 100),           # Convert to cents
                "issuer": credit_data.get("issuer", "QuantumEco Intelligence")
            }
            
            # Execute carbon credit creation
            tx_result = await self.contract_interface.execute_contract_function(
                "CarbonCreditToken",
                "issueCarbonCredit",
                tx_data
            )
            
            if tx_result["success"]:
                # Extract credit ID from events
                credit_id = self._extract_credit_id_from_events(tx_result.get("events", []))
                
                # Update metrics
                self.metrics["carbon_credits_issued"] += 1
                self.metrics["transactions_processed"] += 1
                
                return {
                    "success": True,
                    "credit_id": credit_id,
                    "route_id": credit_data["route_id"],
                    "carbon_amount": credit_data["carbon_amount"],
                    "value_usd": credit_data["value_usd"],
                    "transaction_hash": tx_result["transaction_hash"],
                    "block_number": tx_result["block_number"],
                    "timestamp": int(time.time()),
                    "tradeable": True
                }
            else:
                return {
                    "success": False,
                    "error": tx_result.get("error", "Carbon credit creation failed")
                }
                
        except Exception as e:
            logger.error(f"Carbon credit creation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_network_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive blockchain network statistics
        
        Returns:
            Dict containing network statistics and metrics
        """
        try:
            if not self._connected:
                return self._get_mock_network_stats()
            
            # Get blockchain network info
            latest_block = self.web3_utils.get_latest_block()
            network_info = self.web3_utils.get_network_info()
            
            # Get contract statistics
            contract_stats = {}
            if self._contracts_loaded:
                stats_result = await self.contract_interface.call_contract_function(
                    "DeliveryVerification",
                    "getNetworkStats",
                    {}
                )
                
                if stats_result["success"]:
                    contract_stats = {
                        "total_carbon_saved": stats_result["result"][0] / 1000,  # Convert to kg
                        "total_cost_saved": stats_result["result"][1] / 100,    # Convert to USD
                        "total_deliveries": stats_result["result"][2]
                    }
            
            # Get recent transactions
            recent_certificates = await self.get_recent_certificates(limit=10)
            
            return {
                "network_name": "Ganache Local Development",
                "latest_block": latest_block.get("number", 0),
                "gas_price": network_info.get("gas_price", 0),
                "network_id": network_info.get("network_id", 1337),
                "connected_accounts": len(network_info.get("accounts", [])),
                "contract_statistics": contract_stats,
                "service_metrics": self.metrics,
                "recent_certificates": recent_certificates,
                "health_status": "healthy" if self._connected else "disconnected",
                "last_updated": int(time.time())
            }
            
        except Exception as e:
            logger.error(f"Failed to get network statistics: {str(e)}")
            return {
                "error": str(e),
                "health_status": "error",
                "last_updated": int(time.time())
            }
    
    async def get_recent_certificates(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recently created certificates
        
        Args:
            limit: Maximum number of certificates to return
            
        Returns:
            List of recent certificate summaries
        """
        try:
            if not self._connected or not self._contracts_loaded:
                return self._get_mock_recent_certificates(limit)
            
            # Get recent DeliveryRecorded events
            events = await self.contract_interface.get_contract_events(
                "DeliveryVerification",
                "DeliveryRecorded",
                from_block="latest",
                limit=limit
            )
            
            certificates = []
            for event in events:
                certificates.append({
                    "certificate_id": event["args"]["routeId"],
                    "carbon_saved": event["args"]["carbonSaved"] / 1000,  # Convert to kg
                    "cost_saved": event["args"]["costSaved"] / 100,      # Convert to USD
                    "block_number": event["blockNumber"],
                    "transaction_hash": event["transactionHash"],
                    "timestamp": int(time.time())  # Approximate timestamp
                })
            
            return certificates[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get recent certificates: {str(e)}")
            return []
    
    def get_transaction_details(self, tx_hash: str) -> Dict[str, Any]:
        """
        Get detailed information about a blockchain transaction
        
        Args:
            tx_hash: Transaction hash to query
            
        Returns:
            Dict containing transaction details
        """
        try:
            if not self._connected:
                return self._get_mock_transaction_details(tx_hash)
            
            tx_details = self.web3_utils.get_transaction_details(tx_hash)
            tx_receipt = self.web3_utils.get_transaction_receipt(tx_hash)
            
            return {
                "transaction_hash": tx_hash,
                "block_number": tx_receipt.get("blockNumber"),
                "gas_used": tx_receipt.get("gasUsed"),
                "gas_price": tx_details.get("gasPrice"),
                "status": "success" if tx_receipt.get("status") == 1 else "failed",
                "from_address": tx_details.get("from"),
                "to_address": tx_details.get("to"),
                "value": tx_details.get("value", 0),
                "timestamp": int(time.time())  # Approximate
            }
            
        except Exception as e:
            logger.error(f"Failed to get transaction details: {str(e)}")
            return {
                "transaction_hash": tx_hash,
                "error": str(e),
                "status": "error"
            }
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform comprehensive health check of blockchain service
        
        Returns:
            Dict containing health status and diagnostic information
        """
        try:
            health_status = {
                "timestamp": datetime.utcnow().isoformat(),
                "service_version": "1.0.0",
                "overall_status": "healthy"
            }
            
            # Check Web3 connection
            if self.web3_utils.is_connected():
                health_status["web3_connection"] = "connected"
                health_status["ganache_url"] = self.config["ganache_url"]
            else:
                health_status["web3_connection"] = "disconnected"
                health_status["overall_status"] = "degraded"
            
            # Check contract loading
            if self._contracts_loaded:
                health_status["contracts_loaded"] = "success"
                health_status["available_contracts"] = list(self.contract_interface.contracts.keys())
            else:
                health_status["contracts_loaded"] = "failed"
                health_status["overall_status"] = "degraded"
            
            # Check recent activity
            if self.metrics["transactions_processed"] > 0:
                health_status["recent_activity"] = "active"
                health_status["total_transactions"] = self.metrics["transactions_processed"]
            else:
                health_status["recent_activity"] = "idle"
            
            # Performance metrics
            health_status["performance_metrics"] = {
                "certificates_created": self.metrics["certificates_created"],
                "ett_tokens_created": self.metrics["ett_tokens_created"],
                "carbon_credits_issued": self.metrics["carbon_credits_issued"],
                "average_confirmation_time": round(self.metrics["average_confirmation_time"], 2)
            }
            
            self.last_health_check = time.time()
            return health_status
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "overall_status": "unhealthy",
                "error": str(e)
            }
    
    def is_connected(self) -> bool:
        """Check if service is connected to blockchain"""
        return self._connected and self.web3_utils.is_connected()
    
    # ===== PRIVATE HELPER METHODS =====
    
    def _validate_certificate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate certificate data structure and values"""
        required_fields = ["route_id", "vehicle_id", "carbon_saved", "cost_saved", "distance_km", "optimization_score"]
        
        for field in required_fields:
            if field not in data:
                return {"valid": False, "error": f"Missing required field: {field}"}
        
        # Validate data types and ranges
        try:
            if not isinstance(data["route_id"], str) or len(data["route_id"]) == 0:
                return {"valid": False, "error": "route_id must be non-empty string"}
            
            if not isinstance(data["vehicle_id"], str) or len(data["vehicle_id"]) == 0:
                return {"valid": False, "error": "vehicle_id must be non-empty string"}
            
            if not (0 <= float(data["carbon_saved"]) <= 10000):
                return {"valid": False, "error": "carbon_saved must be between 0 and 10000 kg"}
            
            if not (0 <= float(data["cost_saved"]) <= 100000):
                return {"valid": False, "error": "cost_saved must be between 0 and 100000 USD"}
            
            if not (0 <= float(data["distance_km"]) <= 10000):
                return {"valid": False, "error": "distance_km must be between 0 and 10000 km"}
            
            if not (0 <= int(data["optimization_score"]) <= 100):
                return {"valid": False, "error": "optimization_score must be between 0 and 100"}
            
            return {"valid": True}
            
        except (ValueError, TypeError) as e:
            return {"valid": False, "error": f"Invalid data type: {str(e)}"}
    
    def _validate_ett_data(self, data: Dict[str, Any]) -> bool:
        """Validate Environmental Trust Token data"""
        required_fields = ["route_id", "trust_score", "carbon_impact", "sustainability_rating"]
        
        for field in required_fields:
            if field not in data:
                return False
        
        try:
            return (
                isinstance(data["route_id"], str) and len(data["route_id"]) > 0 and
                0 <= int(data["trust_score"]) <= 100 and
                0 <= float(data["carbon_impact"]) <= 10000 and
                0 <= int(data["sustainability_rating"]) <= 100
            )
        except (ValueError, TypeError):
            return False
    
    def _validate_carbon_credit_data(self, data: Dict[str, Any]) -> bool:
        """Validate carbon credit data"""
        required_fields = ["route_id", "carbon_amount", "value_usd"]
        
        for field in required_fields:
            if field not in data:
                return False
        
        try:
            return (
                isinstance(data["route_id"], str) and len(data["route_id"]) > 0 and
                0 <= float(data["carbon_amount"]) <= 10000 and
                0 <= float(data["value_usd"]) <= 1000000
            )
        except (ValueError, TypeError):
            return False
    
    def _generate_verification_hash(self, data: Dict[str, Any]) -> str:
        """Generate secure verification hash for data integrity"""
        # Create deterministic hash from certificate data
        hash_data = {
            "route_id": data["route_id"],
            "vehicle_id": data["vehicle_id"],
            "carbon_saved": data["carbon_saved"],
            "cost_saved": data["cost_saved"],
            "distance_km": data["distance_km"],
            "optimization_score": data["optimization_score"],
            "timestamp": int(time.time())
        }
        
        hash_string = json.dumps(hash_data, sort_keys=True)
        return hashlib.sha256(hash_string.encode()).hexdigest()
    
    def _extract_token_id_from_events(self, events: List[Dict]) -> Optional[int]:
        """Extract token ID from ETT creation events"""
        for event in events:
            if event.get("event") == "ETTCreated":
                return event.get("args", {}).get("tokenId")
        return None
    
    def _extract_credit_id_from_events(self, events: List[Dict]) -> Optional[int]:
        """Extract credit ID from carbon credit creation events"""
        for event in events:
            if event.get("event") == "CarbonCreditIssued":
                return event.get("args", {}).get("creditId")
        return None
    
    def _update_average_confirmation_time(self, new_time: float):
        """Update rolling average confirmation time"""
        current_avg = self.metrics["average_confirmation_time"]
        transaction_count = self.metrics["transactions_processed"]
        
        if transaction_count <= 1:
            self.metrics["average_confirmation_time"] = new_time
        else:
            # Calculate rolling average
            self.metrics["average_confirmation_time"] = (
                (current_avg * (transaction_count - 1) + new_time) / transaction_count
            )
    
    # ===== MOCK METHODS FOR DEMO/TESTING =====
    
    def _create_mock_certificate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create mock certificate when blockchain unavailable"""
        import random
        route_time = f"{data['route_id']}{time.time()}"
        return {
            "success": True,
            "certificate_id": data["route_id"],
            "transaction_hash": f"0x{hashlib.sha256(route_time.encode()).hexdigest()}",
            "block_number": random.randint(1000000, 2000000),
            "verification_hash": self._generate_verification_hash(data),
            "gas_used": random.randint(50000, 150000),
            "confirmation_time": random.uniform(1, 5),
            "timestamp": int(time.time()),
            "verified": True,
            "blockchain_network": "mock_mode"
        }
    
    def _create_mock_ett(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create mock ETT when blockchain unavailable"""
        import random
        ett_time = f"ett_{data['route_id']}{time.time()}"
        return {
            "success": True,
            "token_id": random.randint(1, 10000),
            "route_id": data["route_id"],
            "trust_score": data["trust_score"],
            "carbon_impact": data["carbon_impact"],
            "sustainability_rating": data["sustainability_rating"],
            "transaction_hash": f"0x{hashlib.sha256(ett_time.encode()).hexdigest()}",
            "block_number": random.randint(1000000, 2000000),
            "timestamp": int(time.time()),
            "active": True,
            "blockchain_network": "mock_mode"
        }
    
    def _create_mock_carbon_credit(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create mock carbon credit when blockchain unavailable"""
        import random
        credit_time = f"credit_{data['route_id']}{time.time()}"
        return {
            "success": True,
            "credit_id": random.randint(1, 10000),
            "route_id": data["route_id"],
            "carbon_amount": data["carbon_amount"],
            "value_usd": data["value_usd"],
            "transaction_hash": f"0x{hashlib.sha256(credit_time.encode()).hexdigest()}",
            "block_number": random.randint(1000000, 2000000),
            "timestamp": int(time.time()),
            "tradeable": True,
            "blockchain_network": "mock_mode"
        }
    
    def _verify_mock_certificate(self, certificate_id: str) -> Dict[str, Any]:
        """Verify mock certificate"""
        import random
        return {
            "verified": True,
            "certificate_id": certificate_id,
            "route_id": certificate_id,
            "vehicle_id": f"vehicle_{random.randint(1, 10)}",
            "carbon_saved": random.uniform(10, 100),
            "cost_saved": random.uniform(50, 500),
            "distance_km": random.uniform(50, 300),
            "optimization_score": random.randint(80, 99),
            "timestamp": int(time.time()),
            "verifier": "0x1234...5678",
            "verification_hash": hashlib.sha256(f"{certificate_id}{time.time()}".encode()).hexdigest(),
            "blockchain_verified": False,
            "mock_mode": True
        }
    
    def _get_mock_network_stats(self) -> Dict[str, Any]:
        """Get mock network statistics"""
        import random
        return {
            "network_name": "Mock Blockchain Network",
            "latest_block": random.randint(1000000, 2000000),
            "gas_price": 20000000000,
            "network_id": 1337,
            "connected_accounts": 10,
            "contract_statistics": {
                "total_carbon_saved": random.uniform(1000, 10000),
                "total_cost_saved": random.uniform(5000, 50000),
                "total_deliveries": random.randint(100, 1000)
            },
            "service_metrics": self.metrics,
            "recent_certificates": self._get_mock_recent_certificates(5),
            "health_status": "mock_mode",
            "last_updated": int(time.time())
        }
    
    def _get_mock_recent_certificates(self, limit: int) -> List[Dict[str, Any]]:
        """Get mock recent certificates"""
        import random
        certificates = []
        
        for i in range(min(limit, 10)):
            certificates.append({
                "certificate_id": f"mock_route_{i+1:03d}",
                "carbon_saved": random.uniform(10, 100),
                "cost_saved": random.uniform(50, 500),
                "block_number": random.randint(1000000, 2000000),
                "transaction_hash": f"0x{hashlib.sha256(f'mock_{i}{time.time()}'.encode()).hexdigest()}",
                "timestamp": int(time.time()) - random.randint(60, 3600)
            })
        
        return certificates
    
    def _get_mock_transaction_details(self, tx_hash: str) -> Dict[str, Any]:
        """Get mock transaction details"""
        import random
        return {
            "transaction_hash": tx_hash,
            "block_number": random.randint(1000000, 2000000),
            "gas_used": random.randint(50000, 150000),
            "gas_price": 20000000000,
            "status": "success",
            "from_address": "0x1234567890123456789012345678901234567890",
            "to_address": "0x0987654321098765432109876543210987654321",
            "value": 0,
            "timestamp": int(time.time()),
            "mock_mode": True
        }
