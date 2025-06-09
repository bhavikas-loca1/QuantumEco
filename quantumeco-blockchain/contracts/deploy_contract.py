# contracts/deploy_contract.py
from web3 import Web3
from solcx import compile_source
import json

def deploy_contract():
    # Connect to Ganache
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    
    if not w3.is_connected():
        print("❌ Failed to connect to Ganache")
        return None
    
    print("✅ Connected to Ganache")
    
    # Read contract source
    with open('DeliveryVerification.sol', 'r') as file:
        contract_source = file.read()
    
    # Compile contract
    print("🔨 Compiling contract...")
    compiled_sol = compile_source(contract_source)
    contract_interface = compiled_sol['<stdin>:DeliveryVerification']
    
    # Deploy contract
    print("🚀 Deploying contract...")
    contract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']
    )
    
    # Get default account
    default_account = w3.eth.accounts[0]
    
    # Deploy transaction
    tx_hash = contract.constructor().transact({
        'from': default_account,
        'gas': 3000000
    })
    
    # Wait for deployment
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt.contractAddress
    
    print(f"✅ Contract deployed at: {contract_address}")
    print(f"📝 Transaction hash: {tx_hash.hex()}")
    print(f"🧱 Block number: {tx_receipt.blockNumber}")
    
    # Save deployment info
    deployment_info = {
        'contract_address': contract_address,
        'abi': contract_interface['abi'],
        'transaction_hash': tx_hash.hex(),
        'block_number': tx_receipt.blockNumber
    }
    
    with open('deployment_info.json', 'w') as f:
        json.dump(deployment_info, f, indent=2, default=str)
    
    print("💾 Deployment info saved to deployment_info.json")
    return deployment_info

if __name__ == "__main__":
    # Install solcx if not installed
    try:
        from solcx import install_solc
        install_solc('0.8.20')
    except:
        pass
    
    deploy_contract()
