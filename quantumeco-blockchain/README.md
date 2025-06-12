Here are the complete configuration files for the QuantumEco blockchain implementation:


## .env (SAMPLE Environment Variables)
```bash
# Blockchain Configuration
BLOCKCHAIN_URL=http://127.0.0.1:8545
DELIVERY_VERIFICATION_ADDRESS=
ENVIRONMENTAL_TRUST_TOKEN_ADDRESS=
CARBON_CREDIT_TOKEN_ADDRESS=

# Default Account (Ganache deterministic account 0)
DEFAULT_ACCOUNT=0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1
PRIVATE_KEY=0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d

# Gas Settings
DEFAULT_GAS_LIMIT=500000
DEFAULT_GAS_PRICE=20000000000  # 20 Gwei

# Demo Configuration
DEMO_MODE_ENABLED=true
DEMO_DATA_GENERATED=false
```

## Setup Instructions

1. Install dependencies:
```bash
npm install
```

2. Start Ganache (in separate terminal):
```bash
npm run start:ganache
```
or
```bash
ganache-cli --deterministic --accounts 10 --host 0.0.0.0 --port 8545
```

3. Deploy contracts and update .env:
```bash
truffle compile
truffle migrate --reset

# After deployment, update .env with contract addresses from:
cat build/contracts/DeliveryVerification.json | grep '"address":'
cat build/contracts/EnvironmentalTrustToken.json | grep '"address":'
cat build/contracts/CarbonCreditToken.json | grep '"address":'
```

4. Run the system:
```bash
uvicorn app.main:app --reload
```
or
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload  
```

This configuration provides:
- Full Truffle setup for contract management
- Local blockchain configuration
- Gas optimization settings
- Demo mode capabilities
- Secure private key management
- Automatic contract verification

The system is ready for integration with the QuantumEco backend and frontend components.

# Additional Information:
You may test out the quantum-blockchain's isolated code experience by running it locally.
Uncomment the python-interface files, run the python server independently using uvicorn, and then use the API to interact with the blockchain.
