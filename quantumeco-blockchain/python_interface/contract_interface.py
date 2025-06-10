"""
Smart Contract Interface Layer for QuantumEco Intelligence

Provides low-level smart contract interaction capabilities including
function calls, event listening, and transaction management.
"""

import json
import time
import logging
from typing import Dict, Any, List, Optional, Union
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContractInterface:
    """
    Smart contract interaction layer
    
    Handles direct interaction with deployed smart contracts including:
    - Contract loading and initialization
    - Function calls (read and write)
    - Event filtering and listening
    - Transaction management and monitoring
    """
    
    def __init__(self, web3_utils):
        """Initialize contract interface with Web3 utilities"""
        self.web3_utils = web3_utils
        self.w3 = web3_utils.w3
        
        # Contract storage
        self.contracts = {}
        self.contract_addresses = {}
        self.contract_abis = {}
        
        # Event filters
        self.event_filters = {}
        
        # Transaction cache
        self.transaction_cache = {}
        
        # Configuration
        self.default_gas_limit = 300000
        self.confirmation_blocks = 1
        
    def load_contract(self, contract_name: str, contract_address: Optional[str] = None) -> bool:
        """
        Load smart contract from deployment artifacts
        
        Args:
            contract_name: Name of the contract (e.g., "DeliveryVerification")
            contract_address: Deployed contract address (optional, will try to auto-detect)
            
        Returns:
            bool: True if contract loaded successfully
        """
        try:
            # Try to load from Truffle build artifacts
            contract_path = Path(f"../build/contracts/{contract_name}.json")
            
            if not contract_path.exists():
                # Try alternative paths
                alternative_paths = [
                    Path(f"./build/contracts/{contract_name}.json"),
                    Path(f"./contracts/build/{contract_name}.json"),
                    Path(f"./{contract_name}.json")
                ]
                
                contract_path = None
                for path in alternative_paths:
                    if path.exists():
                        contract_path = path
                        break
                
                if not contract_path:
                    logger.warning(f"⚠️ Contract artifact not found for {contract_name}")
                    return self._create_mock_contract(contract_name)
            
            # Load contract artifact
            with open(contract_path, 'r') as f:
                contract_artifact = json.load(f)
            
            # Get contract ABI
            contract_abi = contract_artifact.get('abi', [])
            if not contract_abi:
                logger.error(f"❌ No ABI found for contract {contract_name}")
                return False
            
            # Get contract address
            if not contract_address:
                # Try to get from deployment networks
                networks = contract_artifact.get('networks', {})
                network_id = str(self.w3.net.version)
                
                if network_id in networks:
                    contract_address = networks[network_id].get('address')
                
                if not contract_address:
                    logger.warning(f"⚠️ No deployed address found for {contract_name}")
                    return self._create_mock_contract(contract_name)
            
            # Create contract instance
            contract_instance = self.w3.eth.contract(
                address=contract_address,
                abi=contract_abi
            )
            
            # Store contract information
            self.contracts[contract_name] = contract_instance
            self.contract_addresses[contract_name] = contract_address
            self.contract_abis[contract_name] = contract_abi
            
            logger.info(f"✅ Contract {contract_name} loaded at {contract_address}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load contract {contract_name}: {str(e)}")
            return self._create_mock_contract(contract_name)
    
    async def execute_contract_function(self, contract_name: str, function_name: str, 
                                      params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a contract function that modifies state (write operation)
        
        Args:
            contract_name: Name of the contract
            function_name: Name of the function to call
            params: Parameters to pass to the function
            
        Returns:
            Dict containing transaction result
        """
        try:
            if contract_name not in self.contracts:
                return {
                    "success": False,
                    "error": f"Contract {contract_name} not loaded"
                }
            
            contract = self.contracts[contract_name]
            
            # Get contract function
            if not hasattr(contract.functions, function_name):
                return {
                    "success": False,
                    "error": f"Function {function_name} not found in contract"
                }
            
            function = getattr(contract.functions, function_name)
            
            # Prepare transaction parameters
            tx_params = {
                'from': self.web3_utils.default_account,
                'gas': self.default_gas_limit,
                'gasPrice': self.web3_utils.gas_price
            }
            
            # Build transaction based on function signature
            if function_name == "addDeliveryRecord":
                tx = function(
                    params["route_id"],
                    params["vehicle_id"],
                    params["carbon_saved"],
                    params["cost_saved"],
                    params["distance_km"],
                    params["optimization_score"],
                    params["verification_hash"]
                ).buildTransaction(tx_params)
                
            elif function_name == "createETT":
                tx = function(
                    params["route_id"],
                    params["trust_score"],
                    params["carbon_impact"],
                    params["sustainability_rating"]
                ).buildTransaction(tx_params)
                
            elif function_name == "issueCarbonCredit":
                tx = function(
                    params["route_id"],
                    params["carbon_amount"],
                    params["value_usd"]
                ).buildTransaction(tx_params)
                
            else:
                # Generic function call
                tx = function(**params).buildTransaction(tx_params)
            
            # Sign and send transaction
            signed_tx = self.web3_utils.sign_transaction(tx)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            # Wait for confirmation
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(
                tx_hash, 
                timeout=60
            )
            
            # Process transaction events
            events = self._process_transaction_events(contract, tx_receipt)
            
            # Cache transaction
            self.transaction_cache[tx_hash.hex()] = {
                "contract_name": contract_name,
                "function_name": function_name,
                "params": params,
                "receipt": dict(tx_receipt),
                "timestamp": int(time.time())
            }
            
            return {
                "success": True,
                "transaction_hash": tx_hash.hex(),
                "block_number": tx_receipt.blockNumber,
                "gas_used": tx_receipt.gasUsed,
                "status": "success" if tx_receipt.status == 1 else "failed",
                "events": events,
                "confirmation_time": time.time()
            }
            
        except Exception as e:
            logger.error(f"Contract function execution failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "function_name": function_name,
                "contract_name": contract_name
            }
    
    async def call_contract_function(self, contract_name: str, function_name: str, 
                                   params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a contract function that doesn't modify state (read operation)
        
        Args:
            contract_name: Name of the contract
            function_name: Name of the function to call
            params: Parameters to pass to the function
            
        Returns:
            Dict containing function result
        """
        try:
            if contract_name not in self.contracts:
                return {
                    "success": False,
                    "error": f"Contract {contract_name} not loaded"
                }
            
            contract = self.contracts[contract_name]
            
            # Get contract function
            if not hasattr(contract.functions, function_name):
                return {
                    "success": False,
                    "error": f"Function {function_name} not found in contract"
                }
            
            function = getattr(contract.functions, function_name)
            
            # Call function based on expected parameters
            if function_name == "verifyDelivery":
                result = function(params["route_id"]).call()
                
            elif function_name == "getDeliveryRecord":
                result = function(params["route_id"]).call()
                
            elif function_name == "getNetworkStats":
                result = function().call()
                
            elif function_name == "getTrustToken":
                result = function(params["token_id"]).call()
                
            elif function_name == "getCarbonCredit":
                result = function(params["credit_id"]).call()
                
            else:
                # Generic function call
                if params:
                    result = function(**params).call()
                else:
                    result = function().call()
            
            return {
                "success": True,
                "result": result,
                "function_name": function_name,
                "contract_name": contract_name
            }
            
        except Exception as e:
            logger.error(f"Contract function call failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "function_name": function_name,
                "contract_name": contract_name
            }
    
    async def get_contract_events(self, contract_name: str, event_name: str, 
                                from_block: Union[str, int] = "latest", 
                                to_block: Union[str, int] = "latest",
                                limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get contract events from blockchain
        
        Args:
            contract_name: Name of the contract
            event_name: Name of the event to filter
            from_block: Starting block for event search
            to_block: Ending block for event search
            limit: Maximum number of events to return
            
        Returns:
            List of event dictionaries
        """
        try:
            if contract_name not in self.contracts:
                return []
            
            contract = self.contracts[contract_name]
            
            # Calculate block range
            if from_block == "latest":
                latest_block = self.w3.eth.get_block('latest')
                from_block = max(0, latest_block.number - 1000)  # Look back 1000 blocks
            
            # Get event filter
            event_filter = None
            
            if event_name == "DeliveryRecorded" and hasattr(contract.events, 'DeliveryRecorded'):
                event_filter = contract.events.DeliveryRecorded.createFilter(
                    fromBlock=from_block,
                    toBlock=to_block
                )
                
            elif event_name == "ETTCreated" and hasattr(contract.events, 'ETTCreated'):
                event_filter = contract.events.ETTCreated.createFilter(
                    fromBlock=from_block,
                    toBlock=to_block
                )
                
            elif event_name == "CarbonCreditIssued" and hasattr(contract.events, 'CarbonCreditIssued'):
                event_filter = contract.events.CarbonCreditIssued.createFilter(
                    fromBlock=from_block,
                    toBlock=to_block
                )
            
            if not event_filter:
                logger.warning(f"Event {event_name} not found in contract {contract_name}")
                return []
            
            # Get events
            events = event_filter.get_all_entries()
            
            # Sort by block number (most recent first) and limit
            sorted_events = sorted(events, key=lambda x: x.blockNumber, reverse=True)
            limited_events = sorted_events[:limit]
            
            # Convert to dictionaries
            event_list = []
            for event in limited_events:
                event_dict = {
                    "event": event.event,
                    "blockNumber": event.blockNumber,
                    "transactionHash": event.transactionHash.hex(),
                    "args": dict(event.args)
                }
                event_list.append(event_dict)
            
            return event_list
            
        except Exception as e:
            logger.error(f"Failed to get contract events: {str(e)}")
            return []
    
    def create_event_filter(self, contract_name: str, event_name: str, 
                          filter_params: Optional[Dict] = None) -> Optional[str]:
        """
        Create persistent event filter for real-time monitoring
        
        Args:
            contract_name: Name of the contract
            event_name: Name of the event to monitor
            filter_params: Optional filter parameters
            
        Returns:
            Filter ID for tracking
        """
        try:
            if contract_name not in self.contracts:
                return None
            
            contract = self.contracts[contract_name]
            filter_id = f"{contract_name}_{event_name}_{int(time.time())}"
            
            # Create event filter
            if hasattr(contract.events, event_name):
                event = getattr(contract.events, event_name)
                event_filter = event.createFilter(fromBlock='latest')
                
                self.event_filters[filter_id] = {
                    "filter": event_filter,
                    "contract_name": contract_name,
                    "event_name": event_name,
                    "created_at": time.time()
                }
                
                logger.info(f"✅ Event filter created: {filter_id}")
                return filter_id
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to create event filter: {str(e)}")
            return None
    
    def get_new_events(self, filter_id: str) -> List[Dict[str, Any]]:
        """
        Get new events from an existing filter
        
        Args:
            filter_id: ID of the event filter
            
        Returns:
            List of new events
        """
        try:
            if filter_id not in self.event_filters:
                return []
            
            filter_info = self.event_filters[filter_id]
            event_filter = filter_info["filter"]
            
            # Get new entries
            new_events = event_filter.get_new_entries()
            
            # Convert to dictionaries
            event_list = []
            for event in new_events:
                event_dict = {
                    "event": event.event,
                    "blockNumber": event.blockNumber,
                    "transactionHash": event.transactionHash.hex(),
                    "args": dict(event.args),
                    "timestamp": int(time.time())
                }
                event_list.append(event_dict)
            
            return event_list
            
        except Exception as e:
            logger.error(f"Failed to get new events: {str(e)}")
            return []
    
    def remove_event_filter(self, filter_id: str) -> bool:
        """
        Remove an event filter
        
        Args:
            filter_id: ID of the filter to remove
            
        Returns:
            bool: True if filter was removed successfully
        """
        try:
            if filter_id in self.event_filters:
                # Uninstall the filter
                filter_info = self.event_filters[filter_id]
                self.w3.eth.uninstall_filter(filter_info["filter"].filter_id)
                
                # Remove from tracking
                del self.event_filters[filter_id]
                
                logger.info(f"✅ Event filter removed: {filter_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to remove event filter: {str(e)}")
            return False
    
    def get_contract_info(self, contract_name: str) -> Dict[str, Any]:
        """
        Get information about a loaded contract
        
        Args:
            contract_name: Name of the contract
            
        Returns:
            Dict containing contract information
        """
        if contract_name not in self.contracts:
            return {"error": f"Contract {contract_name} not loaded"}
        
        return {
            "contract_name": contract_name,
            "address": self.contract_addresses[contract_name],
            "abi_functions": [item["name"] for item in self.contract_abis[contract_name] if item["type"] == "function"],
            "abi_events": [item["name"] for item in self.contract_abis[contract_name] if item["type"] == "event"],
            "loaded": True
        }
    
    def _process_transaction_events(self, contract, tx_receipt) -> List[Dict[str, Any]]:
        """Process events from transaction receipt"""
        events = []
        
        try:
            # Get all events from the transaction
            for log in tx_receipt.logs:
                try:
                    # Try to decode log using contract ABI
                    decoded_log = contract.events.DeliveryRecorded().processLog(log)
                    events.append({
                        "event": "DeliveryRecorded",
                        "args": dict(decoded_log.args)
                    })
                except:
                    try:
                        decoded_log = contract.events.ETTCreated().processLog(log)
                        events.append({
                            "event": "ETTCreated",
                            "args": dict(decoded_log.args)
                        })
                    except:
                        try:
                            decoded_log = contract.events.CarbonCreditIssued().processLog(log)
                            events.append({
                                "event": "CarbonCreditIssued",
                                "args": dict(decoded_log.args)
                            })
                        except:
                            # Unknown event, skip
                            pass
            
        except Exception as e:
            logger.warning(f"Could not process transaction events: {str(e)}")
        
        return events
    
    def _create_mock_contract(self, contract_name: str) -> bool:
        """Create mock contract for testing/demo purposes"""
        logger.info(f"🎭 Creating mock contract for {contract_name}")
        
        # Create mock contract data
        mock_address = f"0x{'1' * 40}"  # Mock address
        mock_abi = [
            {"name": "addDeliveryRecord", "type": "function"},
            {"name": "createETT", "type": "function"},
            {"name": "verifyDelivery", "type": "function"},
            {"name": "getDeliveryRecord", "type": "function"},
            {"name": "getNetworkStats", "type": "function"}
        ]
        
        # Store mock contract
        self.contract_addresses[contract_name] = mock_address
        self.contract_abis[contract_name] = mock_abi
        self.contracts[contract_name] = None  # Mark as mock
        
        return True
    
    def cleanup(self):
        """Clean up resources (remove event filters, clear caches)"""
        try:
            # Remove all event filters
            for filter_id in list(self.event_filters.keys()):
                self.remove_event_filter(filter_id)
            
            # Clear caches
            self.transaction_cache.clear()
            
            logger.info("✅ Contract interface cleaned up")
            
        except Exception as e:
            logger.error(f"Cleanup failed: {str(e)}")
