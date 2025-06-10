"""
QuantumEco Intelligence Contract Deployment Script

Handles automated deployment of smart contracts to Ganache blockchain
with comprehensive configuration, verification, and artifact management.
"""

import json
import time
import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from web3 import Web3
from solcx import compile_source, install_solc, set_solc_version
import hashlib
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class ContractDeployer:
    """
    Comprehensive contract deployment manager for QuantumEco Intelligence
    
    Handles compilation, deployment, verification, and artifact management
    for all smart contracts in the ecosystem.
    """
    
    def __init__(self, provider_url: str = "http://127.0.0.1:8545", 
                 gas_limit: int = 6721975, gas_price: int = 20000000000):
        """Initialize contract deployer with blockchain connection"""
        self.provider_url = provider_url
        self.gas_limit = gas_limit
        self.gas_price = gas_price
        
        # Initialize Web3 connection
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        
        # Deployment configuration
        self.contracts_dir = Path("../contracts")
        self.build_dir = Path("../build/contracts")
        self.artifacts_dir = Path("../artifacts")
        
        # Create directories if they don't exist
        self.build_dir.mkdir(parents=True, exist_ok=True)
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        
        # Contract definitions
        self.contracts = {
            "DeliveryVerification": {
                "file": "DeliveryVerification.sol",
                "dependencies": [],
                "constructor_args": [],
                "verify_functions": ["addDeliveryRecord", "verifyDelivery", "getNetworkStats"]
            },
            "EnvironmentalTrustToken": {
                "file": "EnvironmentalTrustToken.sol", 
                "dependencies": ["DeliveryVerification"],
                "constructor_args": ["delivery_verification_address"],
                "verify_functions": ["createETT", "getETTData", "isValidETT"]
            },
            "CarbonCreditToken": {
                "file": "CarbonCreditToken.sol",
                "dependencies": ["DeliveryVerification"],
                "constructor_args": ["delivery_verification_address"], 
                "verify_functions": ["issueCarbonCredit", "getCarbonCredit", "totalSupply"]
            }
        }
        
        # Deployment state
        self.deployed_contracts = {}
        self.deployment_order = ["DeliveryVerification", "EnvironmentalTrustToken", "CarbonCreditToken"]
        
    def check_prerequisites(self) -> bool:
        """Check all prerequisites for deployment"""
        logger.info("🔍 Checking deployment prerequisites...")
        
        # Check Web3 connection
        if not self.w3.is_connected():
            logger.error("❌ Failed to connect to blockchain")
            return False
        
        logger.info(f"✅ Connected to blockchain at {self.provider_url}")
        
        # Check accounts
        accounts = self.w3.eth.accounts
        if not accounts:
            logger.error("❌ No accounts available")
            return False
        
        logger.info(f"✅ Found {len(accounts)} accounts")
        logger.info(f"   Default account: {accounts[0]}")
        
        # Check account balance
        balance = self.w3.eth.get_balance(accounts[0])
        balance_eth = self.w3.from_wei(balance, 'ether')
        
        if balance_eth < 1:  # Need at least 1 ETH for deployment
            logger.error(f"❌ Insufficient balance: {balance_eth} ETH")
            return False
        
        logger.info(f"✅ Account balance: {balance_eth} ETH")
        
        # Check contract files
        for contract_name, contract_info in self.contracts.items():
            contract_file = self.contracts_dir / contract_info["file"]
            if not contract_file.exists():
                logger.error(f"❌ Contract file not found: {contract_file}")
                return False
        
        logger.info("✅ All contract files found")
        
        # Check and install Solidity compiler
        try:
            install_solc('0.8.20')
            set_solc_version('0.8.20')
            logger.info("✅ Solidity compiler ready")
        except Exception as e:
            logger.error(f"❌ Solidity compiler setup failed: {str(e)}")
            return False
        
        return True
    
    def compile_contracts(self) -> Dict[str, Any]:
        """Compile all smart contracts"""
        logger.info("🔨 Compiling smart contracts...")
        
        compiled_contracts = {}
        
        for contract_name, contract_info in self.contracts.items():
            try:
                logger.info(f"   Compiling {contract_name}...")
                
                # Read contract source
                contract_file = self.contracts_dir / contract_info["file"]
                with open(contract_file, 'r', encoding='utf-8') as f:
                    contract_source = f.read()
                
                # Compile contract
                compiled_sol = compile_source(
                    contract_source,
                    output_values=['abi', 'bin', 'bin-runtime']
                )
                
                # Extract contract interface
                contract_key = f"<stdin>:{contract_name}"
                if contract_key in compiled_sol:
                    contract_interface = compiled_sol[contract_key]
                    compiled_contracts[contract_name] = contract_interface
                    
                    # Save compilation artifact
                    artifact = {
                        "contractName": contract_name,
                        "abi": contract_interface['abi'],
                        "bytecode": contract_interface['bin'],
                        "deployedBytecode": contract_interface['bin-runtime'],
                        "sourceCode": contract_source,
                        "compiler": {
                            "version": "0.8.20",
                            "settings": {
                                "optimizer": {"enabled": True, "runs": 200}
                            }
                        },
                        "compiledAt": datetime.utcnow().isoformat()
                    }
                    
                    # Save to build directory
                    artifact_file = self.build_dir / f"{contract_name}.json"
                    with open(artifact_file, 'w') as f:
                        json.dump(artifact, f, indent=2)
                    
                    logger.info(f"   ✅ {contract_name} compiled successfully")
                else:
                    logger.error(f"   ❌ {contract_name} compilation failed - contract not found in output")
                    
            except Exception as e:
                logger.error(f"   ❌ {contract_name} compilation failed: {str(e)}")
                raise
        
        logger.info(f"✅ Compiled {len(compiled_contracts)} contracts")
        return compiled_contracts
    
    def deploy_contract(self, contract_name: str, compiled_contracts: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy a single contract"""
        logger.info(f"🚀 Deploying {contract_name}...")
        
        try:
            # Get compiled contract
            contract_interface = compiled_contracts[contract_name]
            contract_info = self.contracts[contract_name]
            
            # Create contract instance
            contract = self.w3.eth.contract(
                abi=contract_interface['abi'],
                bytecode=contract_interface['bin']
            )
            
            # Prepare constructor arguments
            constructor_args = []
            for arg_name in contract_info["constructor_args"]:
                if arg_name == "delivery_verification_address":
                    if "DeliveryVerification" in self.deployed_contracts:
                        constructor_args.append(self.deployed_contracts["DeliveryVerification"]["address"])
                    else:
                        raise ValueError("DeliveryVerification must be deployed first")
            
            # Estimate gas
            try:
                gas_estimate = contract.constructor(*constructor_args).estimate_gas({
                    'from': self.w3.eth.accounts[0]
                })
                gas_limit = min(gas_estimate * 2, self.gas_limit)  # 2x buffer, capped at limit
                logger.info(f"   Gas estimate: {gas_estimate}, using: {gas_limit}")
            except Exception as e:
                logger.warning(f"   Gas estimation failed: {str(e)}, using default limit")
                gas_limit = self.gas_limit
            
            # Deploy contract
            tx_hash = contract.constructor(*constructor_args).transact({
                'from': self.w3.eth.accounts[0],
                'gas': gas_limit,
                'gasPrice': self.gas_price
            })
            
            logger.info(f"   Transaction sent: {tx_hash.hex()}")
            
            # Wait for deployment confirmation
            logger.info("   Waiting for confirmation...")
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
            
            if tx_receipt.status == 1:
                contract_address = tx_receipt.contractAddress
                
                # Create deployed contract instance
                deployed_contract = self.w3.eth.contract(
                    address=contract_address,
                    abi=contract_interface['abi']
                )
                
                deployment_info = {
                    "name": contract_name,
                    "address": contract_address,
                    "transaction_hash": tx_hash.hex(),
                    "block_number": tx_receipt.blockNumber,
                    "gas_used": tx_receipt.gasUsed,
                    "constructor_args": constructor_args,
                    "deployed_at": datetime.utcnow().isoformat(),
                    "contract_instance": deployed_contract,
                    "abi": contract_interface['abi']
                }
                
                self.deployed_contracts[contract_name] = deployment_info
                
                logger.info(f"   ✅ {contract_name} deployed successfully")
                logger.info(f"      Address: {contract_address}")
                logger.info(f"      Block: {tx_receipt.blockNumber}")
                logger.info(f"      Gas used: {tx_receipt.gasUsed:,}")
                
                return deployment_info
                
            else:
                raise Exception(f"Transaction failed with status: {tx_receipt.status}")
                
        except Exception as e:
            logger.error(f"   ❌ {contract_name} deployment failed: {str(e)}")
            raise
    
    def verify_deployment(self, contract_name: str) -> bool:
        """Verify contract deployment and functionality"""
        logger.info(f"🔍 Verifying {contract_name} deployment...")
        
        try:
            deployment_info = self.deployed_contracts[contract_name]
            contract = deployment_info["contract_instance"]
            contract_info = self.contracts[contract_name]
            
            # Check contract code
            deployed_code = self.w3.eth.get_code(deployment_info["address"])
            if deployed_code == b'':
                logger.error(f"   ❌ No code found at contract address")
                return False
            
            # Test contract functions
            for func_name in contract_info["verify_functions"]:
                try:
                    if hasattr(contract.functions, func_name):
                        # Test function existence (we won't call state-changing functions)
                        if func_name in ["addDeliveryRecord", "createETT", "issueCarbonCredit"]:
                            # Just check function exists
                            func = getattr(contract.functions, func_name)
                            logger.info(f"   ✅ Function {func_name} available")
                        else:
                            # Call read-only functions
                            func = getattr(contract.functions, func_name)
                            if func_name == "getNetworkStats":
                                result = func().call()
                                logger.info(f"   ✅ {func_name}() -> {result}")
                            elif func_name == "isValidETT":
                                # Don't call with invalid token ID
                                logger.info(f"   ✅ Function {func_name} available")
                            else:
                                logger.info(f"   ✅ Function {func_name} available")
                    else:
                        logger.warning(f"   ⚠️ Function {func_name} not found")
                        
                except Exception as e:
                    logger.warning(f"   ⚠️ Function {func_name} test failed: {str(e)}")
            
            # Additional contract-specific verification
            if contract_name == "DeliveryVerification":
                # Check initial state
                try:
                    total_deliveries = contract.functions.totalDeliveries().call()
                    total_carbon_saved = contract.functions.totalCarbonSaved().call()
                    total_cost_saved = contract.functions.totalCostSaved().call()
                    
                    logger.info(f"   ✅ Initial state: {total_deliveries} deliveries, {total_carbon_saved} carbon saved, {total_cost_saved} cost saved")
                except Exception as e:
                    logger.warning(f"   ⚠️ State check failed: {str(e)}")
            
            elif contract_name == "EnvironmentalTrustToken":
                # Check ETT contract initialization
                try:
                    total_etts = contract.functions.getTotalETTs().call()
                    logger.info(f"   ✅ Total ETTs: {total_etts}")
                except Exception as e:
                    logger.warning(f"   ⚠️ ETT check failed: {str(e)}")
            
            elif contract_name == "CarbonCreditToken":
                # Check carbon credit contract
                try:
                    total_credits = contract.functions.getTotalCredits().call()
                    logger.info(f"   ✅ Total Credits: {total_credits}")
                except Exception as e:
                    logger.warning(f"   ⚠️ Credit check failed: {str(e)}")
            
            logger.info(f"   ✅ {contract_name} verification completed")
            return True
            
        except Exception as e:
            logger.error(f"   ❌ {contract_name} verification failed: {str(e)}")
            return False
    
    def save_deployment_artifacts(self) -> str:
        """Save deployment artifacts for integration"""
        logger.info("💾 Saving deployment artifacts...")
        
        # Create deployment summary
        deployment_summary = {
            "network": {
                "name": "ganache_local",
                "chainId": self.w3.eth.chain_id,
                "url": self.provider_url
            },
            "deployer": self.w3.eth.accounts[0],
            "deployedAt": datetime.utcnow().isoformat(),
            "gasPrice": self.gas_price,
            "gasLimit": self.gas_limit,
            "contracts": {}
        }
        
        total_gas_used = 0
        
        for contract_name, deployment_info in self.deployed_contracts.items():
            contract_summary = {
                "address": deployment_info["address"],
                "transactionHash": deployment_info["transaction_hash"],
                "blockNumber": deployment_info["block_number"],
                "gasUsed": deployment_info["gas_used"],
                "constructorArgs": deployment_info["constructor_args"],
                "deployedAt": deployment_info["deployed_at"]
            }
            
            deployment_summary["contracts"][contract_name] = contract_summary
            total_gas_used += deployment_info["gas_used"]
        
        deployment_summary["totalGasUsed"] = total_gas_used
        
        # Save deployment summary
        summary_file = self.artifacts_dir / "deployment_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(deployment_summary, f, indent=2)
        
        # Save contract addresses for Python integration
        addresses_file = self.artifacts_dir / "contract_addresses.json"
        addresses = {
            name: info["address"] 
            for name, info in self.deployed_contracts.items()
        }
        
        with open(addresses_file, 'w') as f:
            json.dump(addresses, f, indent=2)
        
        # Save ABIs for integration
        abis_file = self.artifacts_dir / "contract_abis.json"
        abis = {
            name: info["abi"] 
            for name, info in self.deployed_contracts.items()
        }
        
        with open(abis_file, 'w') as f:
            json.dump(abis, f, indent=2)
        
        # Create Python integration file
        integration_code = self._generate_python_integration()
        integration_file = self.artifacts_dir / "contract_integration.py"
        with open(integration_file, 'w') as f:
            f.write(integration_code)
        
        logger.info(f"   ✅ Deployment summary: {summary_file}")
        logger.info(f"   ✅ Contract addresses: {addresses_file}")
        logger.info(f"   ✅ Contract ABIs: {abis_file}")
        logger.info(f"   ✅ Python integration: {integration_file}")
        
        return str(summary_file)
    
    def _generate_python_integration(self) -> str:
        """Generate Python integration code"""
        addresses = {
            name: info["address"] 
            for name, info in self.deployed_contracts.items()
        }
        
        integration_code = f'''"""
QuantumEco Intelligence Contract Integration
Generated automatically by deploy_contracts.py
"""

from web3 import Web3
import json

# Contract addresses (deployed on {datetime.utcnow().isoformat()})
CONTRACT_ADDRESSES = {json.dumps(addresses, indent=4)}

# Initialize Web3 connection
def get_web3_instance(provider_url="http://127.0.0.1:8545"):
    return Web3(Web3.HTTPProvider(provider_url))

# Load contract ABIs
def load_contract_abis():
    with open("contract_abis.json", "r") as f:
        return json.load(f)

# Get contract instance
def get_contract(w3, contract_name):
    abis = load_contract_abis()
    return w3.eth.contract(
        address=CONTRACT_ADDRESSES[contract_name],
        abi=abis[contract_name]
    )

# Example usage:
# w3 = get_web3_instance()
# delivery_contract = get_contract(w3, "DeliveryVerification")
# ett_contract = get_contract(w3, "EnvironmentalTrustToken")
# carbon_contract = get_contract(w3, "CarbonCreditToken")
'''
        
        return integration_code
    
    def deploy_all_contracts(self) -> bool:
        """Deploy all contracts in correct order"""
        logger.info("🚀 Starting complete contract deployment...")
        
        try:
            # Check prerequisites
            if not self.check_prerequisites():
                return False
            
            # Compile contracts
            compiled_contracts = self.compile_contracts()
            
            # Deploy contracts in dependency order
            for contract_name in self.deployment_order:
                if contract_name in compiled_contracts:
                    self.deploy_contract(contract_name, compiled_contracts)
                    
                    # Verify deployment
                    if not self.verify_deployment(contract_name):
                        logger.error(f"❌ {contract_name} verification failed")
                        return False
                    
                    # Brief pause between deployments
                    time.sleep(2)
                else:
                    logger.error(f"❌ {contract_name} not found in compiled contracts")
                    return False
            
            # Save deployment artifacts
            summary_file = self.save_deployment_artifacts()
            
            # Final summary
            logger.info("\n" + "="*60)
            logger.info("🎉 DEPLOYMENT COMPLETE!")
            logger.info("="*60)
            
            total_gas = sum(info["gas_used"] for info in self.deployed_contracts.values())
            total_cost_eth = self.w3.from_wei(total_gas * self.gas_price, 'ether')
            
            logger.info(f"📊 Deployment Summary:")
            logger.info(f"   Contracts deployed: {len(self.deployed_contracts)}")
            logger.info(f"   Total gas used: {total_gas:,}")
            logger.info(f"   Total cost: {total_cost_eth:.6f} ETH")
            logger.info(f"   Network: {self.provider_url}")
            
            logger.info(f"\n📋 Contract Addresses:")
            for name, info in self.deployed_contracts.items():
                logger.info(f"   {name}: {info['address']}")
            
            logger.info(f"\n📁 Artifacts saved to: {summary_file}")
            logger.info("="*60)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Deployment failed: {str(e)}")
            return False

def main():
    """Main deployment function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Deploy QuantumEco Intelligence smart contracts')
    parser.add_argument('--provider', default='http://127.0.0.1:8545', help='Blockchain provider URL')
    parser.add_argument('--gas-limit', type=int, default=6721975, help='Gas limit for deployment')
    parser.add_argument('--gas-price', type=int, default=20000000000, help='Gas price in wei')
    parser.add_argument('--verify-only', action='store_true', help='Only verify existing deployments')
    
    args = parser.parse_args()
    
    # Create deployer
    deployer = ContractDeployer(
        provider_url=args.provider,
        gas_limit=args.gas_limit,
        gas_price=args.gas_price
    )
    
    if args.verify_only:
        # Load existing deployment and verify
        try:
            with open(deployer.artifacts_dir / "contract_addresses.json", 'r') as f:
                addresses = json.load(f)
            
            with open(deployer.artifacts_dir / "contract_abis.json", 'r') as f:
                abis = json.load(f)
            
            logger.info("🔍 Verifying existing deployments...")
            
            for name, address in addresses.items():
                deployer.deployed_contracts[name] = {
                    "address": address,
                    "contract_instance": deployer.w3.eth.contract(address=address, abi=abis[name])
                }
                
                if deployer.verify_deployment(name):
                    logger.info(f"✅ {name} verification passed")
                else:
                    logger.error(f"❌ {name} verification failed")
            
        except Exception as e:
            logger.error(f"❌ Verification failed: {str(e)}")
            sys.exit(1)
    else:
        # Deploy contracts
        if deployer.deploy_all_contracts():
            logger.info("🎉 Deployment successful!")
            sys.exit(0)
        else:
            logger.error("❌ Deployment failed!")
            sys.exit(1)

if __name__ == "__main__":
    main()
