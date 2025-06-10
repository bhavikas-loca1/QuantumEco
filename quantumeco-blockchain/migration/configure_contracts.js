/**
 * QuantumEco Intelligence - Contract Configuration
 * 
 * This migration handles post-deployment configuration including:
 * - Setting up initial parameters
 * - Configuring contract interactions
 * - Creating demo data
 * - Setting up access controls
 * - Initializing system parameters
 */

const DeliveryVerification = artifacts.require("DeliveryVerification");
const EnvironmentalTrustToken = artifacts.require("EnvironmentalTrustToken");
const CarbonCreditToken = artifacts.require("CarbonCreditToken");

// Configuration constants
const CONFIGURATION = {
  // Initial system parameters
  systemParams: {
    maxRouteDistance: 1000000, // 1000 km in meters
    maxOptimizationScore: 100,
    minCarbonSaved: 0,
    defaultValidityPeriod: 365 * 24 * 60 * 60, // 1 year in seconds
  },
  
  // Demo data configuration
  demoData: {
    enabled: true,
    routeCount: 10,
    vehicleTypes: ['diesel_truck', 'electric_van', 'hybrid_delivery'],
  },
  
  // Access control settings
  accessControl: {
    setupMultipleVerifiers: true,
    verifierCount: 3
  },
  
  // Environmental Trust Token settings
  ettConfig: {
    defaultValidityPeriod: 365 * 24 * 60 * 60, // 1 year
    baseURI: "https://api.quantumeco.io/ett/metadata/",
    maxTrustScore: 100,
    maxSustainabilityRating: 100
  },
  
    // Carbon Credit Token settings
    carbonCreditConfig: {
      gramsPerTon: 1000000,
      maxExpirationYears: 10,
      minCarbonAmount: 1000, // 1 kg minimum
      defaultStandard: "QUANTUMECO"
    }
  };

module.exports = async function (deployer, network, accounts) {
  console.log("\n⚙️  QuantumEco Intelligence - Contract Configuration");
  console.log("=" .repeat(80));
  console.log(`📡 Network: ${network}`);
  console.log(`👤 Configuration Account: ${accounts[0]}`);
  console.log(`💰 Balance: ${web3.utils.fromWei(await web3.eth.getBalance(accounts[0]), 'ether')} ETH`);
  console.log("=" .repeat(80));

  try {
    // Get deployed contract instances
    const deliveryVerification = await DeliveryVerification.deployed();
    const environmentalTrustToken = await EnvironmentalTrustToken.deployed();
    const carbonCreditToken = await CarbonCreditToken.deployed();
    
    console.log("\n📋 Contract Instances Retrieved:");
    console.log(`   • DeliveryVerification: ${deliveryVerification.address}`);
    console.log(`   • EnvironmentalTrustToken: ${environmentalTrustToken.address}`);
    console.log(`   • CarbonCreditToken: ${carbonCreditToken.address}`);
    
    // Step 1: Configure Access Controls
    console.log("\n🔐 Step 1: Configuring Access Controls...");
    console.log("-" .repeat(50));
    
    if (CONFIGURATION.accessControl.setupMultipleVerifiers) {
      for (let i = 1; i < Math.min(CONFIGURATION.accessControl.verifierCount, accounts.length); i++) {
        try {
          const tx = await deliveryVerification.authorizeVerifier(accounts[i], {
            from: accounts[0],
            gas: 100000
          });
          
          console.log(`✅ Authorized verifier ${i}: ${accounts[i]}`);
          console.log(`   Transaction: ${tx.tx}`);
        } catch (error) {
          console.log(`⚠️  Failed to authorize verifier ${i}: ${error.message}`);
        }
      }
    }
    
    // Verify authorized verifiers
    try {
      const authorizedVerifiers = await deliveryVerification.getAuthorizedVerifiers();
      console.log(`🔍 Total Authorized Verifiers: ${authorizedVerifiers.length}`);
    } catch (error) {
      console.log("⚠️  Could not retrieve authorized verifiers");
    }
    
    // Step 2: Configure Environmental Trust Token
    console.log("\n🌱 Step 2: Configuring Environmental Trust Token...");
    console.log("-" .repeat(50));
    
    try {
      // Set base URI for metadata
      const setBaseURITx = await environmentalTrustToken.setBaseURI(
        CONFIGURATION.ettConfig.baseURI,
        {
          from: accounts[0],
          gas: 100000
        }
      );
      
      console.log("✅ ETT Base URI configured");
      console.log(`   URI: ${CONFIGURATION.ettConfig.baseURI}`);
      console.log(`   Transaction: ${setBaseURITx.tx}`);
    } catch (error) {
      console.log(`⚠️  ETT Base URI configuration failed: ${error.message}`);
    }
    
    // Step 3: Configure Carbon Credit Token
    console.log("\n💚 Step 3: Configuring Carbon Credit Token...");
    console.log("-" .repeat(50));
    
    try {
      // Set metadata URI template
      const setURITx = await carbonCreditToken.setURI(
        "https://api.quantumeco.io/carbon-credits/metadata/{id}.json",
        {
          from: accounts[0],
          gas: 100000
        }
      );
      
      console.log("✅ Carbon Credit URI template configured");
      console.log(`   Transaction: ${setURITx.tx}`);
    } catch (error) {
      console.log(`⚠️  Carbon Credit URI configuration failed: ${error.message}`);
    }
    
    // Step 4: Create Demo Data (if enabled)
    if (CONFIGURATION.demoData.enabled) {
      console.log("\n🎯 Step 4: Creating Demo Data...");
      console.log("-" .repeat(50));
      
      const demoTransactions = [];
      
      for (let i = 0; i < CONFIGURATION.demoData.routeCount; i++) {
        try {
          const routeId = `demo_route_${String(i + 1).padStart(3, '0')}`;
          const vehicleId = `demo_vehicle_${String(i + 1).padStart(3, '0')}`;
          const vehicleType = CONFIGURATION.demoData.vehicleTypes[i % CONFIGURATION.demoData.vehicleTypes.length];
          
          // Generate realistic demo data
          const carbonSaved = Math.floor(Math.random() * 50000) + 10000; // 10-60 kg in grams
          const costSaved = Math.floor(Math.random() * 15000) + 5000;    // $50-200 in cents
          const distanceKm = Math.floor(Math.random() * 200000) + 50000; // 50-250 km in meters
          const optimizationScore = Math.floor(Math.random() * 20) + 80; // 80-100
          
          // Generate verification hash
          const verificationData = JSON.stringify({
            routeId,
            vehicleId,
            carbonSaved,
            costSaved,
            timestamp: Date.now()
          });
          const verificationHash = web3.utils.keccak256(verificationData);
          
          // Create delivery record
          const deliveryTx = await deliveryVerification.addDeliveryRecord(
            routeId,
            vehicleId,
            carbonSaved,
            costSaved,
            distanceKm,
            optimizationScore,
            1, // delivery count
            verificationHash,
            `ipfs://demo_metadata_${i + 1}`, // metadata hash
            {
              from: accounts[0],
              gas: 500000
            }
          );
          
          demoTransactions.push({
            type: 'delivery',
            routeId,
            transaction: deliveryTx.tx,
            gasUsed: deliveryTx.receipt.gasUsed
          });
          
          console.log(`✅ Demo delivery ${i + 1}: ${routeId}`);
          
          // Create ETT for every other route
          if (i % 2 === 0) {
            const trustScore = Math.floor(Math.random() * 30) + 70; // 70-100
            const sustainabilityRating = Math.floor(Math.random() * 30) + 70; // 70-100
            
            const ettTx = await environmentalTrustToken.createETT(
              routeId,
              accounts[0], // recipient
              trustScore,
              carbonSaved,
              sustainabilityRating,
              0, // use default validity period
              {
                from: accounts[0],
                gas: 400000
              }
            );
            
            demoTransactions.push({
              type: 'ett',
              routeId,
              transaction: ettTx.tx,
              gasUsed: ettTx.receipt.gasUsed
            });
            
            console.log(`   🌱 ETT created for ${routeId}`);
          }
          
          // Create carbon credit for every third route
          if (i % 3 === 0) {
            const carbonAmount = Math.floor(carbonSaved * 0.8); // 80% of saved carbon
            const pricePerTon = Math.floor(Math.random() * 3000) + 2000; // $20-50 per ton in cents
            
            const carbonCreditTx = await carbonCreditToken.issueCarbonCredit(
              routeId,
              carbonAmount,
              pricePerTon,
              5, // 5 years expiration
              CONFIGURATION.carbonCreditConfig.defaultStandard,
              3, // PLATINUM quality
              {
                from: accounts[0],
                gas: 500000
              }
            );
            
            demoTransactions.push({
              type: 'carbon_credit',
              routeId,
              transaction: carbonCreditTx.tx,
              gasUsed: carbonCreditTx.receipt.gasUsed
            });
            
            console.log(`   💚 Carbon Credit issued for ${routeId}`);
          }
          
          // Small delay to avoid nonce issues
          await new Promise(resolve => setTimeout(resolve, 100));
          
        } catch (error) {
          console.log(`⚠️  Demo data creation failed for route ${i + 1}: ${error.message}`);
        }
      }
      
      // Demo data statistics
      const totalGasUsed = demoTransactions.reduce((total, tx) => total + tx.gasUsed, 0);
      console.log(`\n📊 Demo Data Summary:`);
      console.log(`   • Total Transactions: ${demoTransactions.length}`);
      console.log(`   • Delivery Records: ${demoTransactions.filter(tx => tx.type === 'delivery').length}`);
      console.log(`   • ETT Tokens: ${demoTransactions.filter(tx => tx.type === 'ett').length}`);
      console.log(`   • Carbon Credits: ${demoTransactions.filter(tx => tx.type === 'carbon_credit').length}`);
      console.log(`   • Total Gas Used: ${totalGasUsed.toLocaleString()}`);
    }
    
    // Step 5: System Verification and Statistics
    console.log("\n📊 Step 5: System Verification and Statistics...");
    console.log("-" .repeat(50));
    
    try {
      // Get network statistics
      const networkStats = await deliveryVerification.getNetworkStatistics();
      console.log("✅ Network Statistics Retrieved:");
      console.log(`   • Total Carbon Saved: ${(networkStats[0] / 1000).toFixed(2)} kg`);
      console.log(`   • Total Cost Saved: $${(networkStats[1] / 100).toFixed(2)}`);
      console.log(`   • Total Deliveries: ${networkStats[2]}`);
      console.log(`   • Total Distance: ${(networkStats[3] / 1000).toFixed(2)} km`);
      console.log(`   • Average Optimization Score: ${networkStats[4]}`);
      console.log(`   • Total Verifiers: ${networkStats[5]}`);
    } catch (error) {
      console.log(`⚠️  Network statistics retrieval failed: ${error.message}`);
    }
    
    try {
      // Get ETT statistics
      const totalETTs = await environmentalTrustToken.getTotalETTs();
      const levelDistribution = await environmentalTrustToken.getLevelDistribution();
      
      console.log("✅ ETT Statistics:");
      console.log(`   • Total ETTs: ${totalETTs}`);
      console.log(`   • Bronze: ${levelDistribution[0]}`);
      console.log(`   • Silver: ${levelDistribution[1]}`);
      console.log(`   • Gold: ${levelDistribution[2]}`);
      console.log(`   • Platinum: ${levelDistribution[3]}`);
    } catch (error) {
      console.log(`⚠️  ETT statistics retrieval failed: ${error.message}`);
    }
    
    try {
      // Get Carbon Credit statistics
      const totalCredits = await carbonCreditToken.getTotalCredits();
      const marketStats = await carbonCreditToken.getMarketStatistics();
      
      console.log("✅ Carbon Credit Statistics:");
      console.log(`   • Total Credits: ${totalCredits}`);
      console.log(`   • Total Carbon Credits: ${(marketStats[0] / 1000).toFixed(2)} kg`);
      console.log(`   • Total Retired: ${(marketStats[1] / 1000).toFixed(2)} kg`);
      console.log(`   • Total Trading Volume: ${(marketStats[2] / 1000).toFixed(2)} kg`);
      if (marketStats[3] > 0) {
        console.log(`   • Average Price: $${(marketStats[3] / 100).toFixed(2)} per ton`);
      }
    } catch (error) {
      console.log(`⚠️  Carbon Credit statistics retrieval failed: ${error.message}`);
    }
    
    // Step 6: Create Integration Documentation
    console.log("\n📚 Step 6: Creating Integration Documentation...");
    console.log("-" .repeat(50));
    
    const fs = require('fs');
    const path = require('path');
    
    // Create comprehensive integration guide
    const integrationGuide = {
      title: "QuantumEco Intelligence Blockchain Integration Guide",
      version: "1.0.0",
      timestamp: new Date().toISOString(),
      network: network,
      
      contracts: {
        DeliveryVerification: {
          address: deliveryVerification.address,
          description: "Main contract for delivery verification and tracking",
          keyFunctions: [
            "addDeliveryRecord(routeId, vehicleId, carbonSaved, costSaved, distanceKm, optimizationScore, deliveryCount, verificationHash, metadataHash)",
            "verifyDeliveryRecord(routeId) -> bool",
            "getDeliveryRecord(routeId) -> (details...)",
            "getNetworkStatistics() -> (totalCarbon, totalCost, totalDeliveries, totalDistance, avgScore, totalVerifiers)"
          ]
        },
        
        EnvironmentalTrustToken: {
          address: environmentalTrustToken.address,
          description: "NFT-based Environmental Trust Tokens",
          keyFunctions: [
            "createETT(routeId, recipient, trustScore, carbonImpact, sustainabilityRating, validityPeriod) -> tokenId",
            "getETTData(tokenId) -> (tokenData...)",
            "isValidETT(tokenId) -> bool",
            "getTotalETTs() -> uint256"
          ]
        },
        
        CarbonCreditToken: {
          address: carbonCreditToken.address,
          description: "ERC1155-based tradeable carbon credits",
          keyFunctions: [
            "issueCarbonCredit(routeId, carbonAmount, pricePerTon, expirationYears, standard, quality) -> creditId",
            "getCarbonCredit(creditId) -> (creditData...)",
            "retireCarbonCredit(creditId, amount, reason)",
            "getMarketStatistics() -> (totalCredits, totalRetired, totalVolume, avgPrice)"
          ]
        }
      },
      
      configuration: CONFIGURATION,
      
      quickStart: {
        python: {
          install: "pip install web3 eth-account",
          connect: `
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
contract = w3.eth.contract(address='${deliveryVerification.address}', abi=abi)
`,
          example: `
# Create delivery certificate
tx_hash = contract.functions.addDeliveryRecord(
    'route_001', 'vehicle_001', 25000, 7500, 125000, 92, 1, 
    verification_hash, metadata_hash
).transact({'from': account})
`
        },
        
        javascript: {
          install: "npm install web3",
          connect: `
const Web3 = require('web3');
const web3 = new Web3('http://127.0.0.1:8545');
const contract = new web3.eth.Contract(abi, '${deliveryVerification.address}');
`,
          example: `
// Verify delivery record
const isVerified = await contract.methods.verifyDeliveryRecord('route_001').call();
`
        }
      },
      
      testing: {
        healthCheck: `curl -X GET "http://localhost:8000/api/blockchain/explorer"`,
        createCertificate: `curl -X POST "http://localhost:8000/api/blockchain/certificate" -H "Content-Type: application/json" -d '{"route_id": "test_001", "vehicle_id": "truck_001", "carbon_saved": 25.5, "cost_saved": 150.0, "distance_km": 100.0, "optimization_score": 95}'`,
        verifyCertificate: `curl -X GET "http://localhost:8000/api/blockchain/certificate/test_001"`
      }
    };
    
    // Write integration guide
    const artifactsDir = path.join(__dirname, '..', 'artifacts');
    fs.writeFileSync(
      path.join(artifactsDir, 'integration_guide.json'),
      JSON.stringify(integrationGuide, null, 2)
    );
    
    // Create environment configuration file
    const envConfig = `# QuantumEco Intelligence Blockchain Configuration
# Generated on ${new Date().toISOString()}

# Network Configuration
BLOCKCHAIN_URL=http://127.0.0.1:8545
NETWORK_ID=${await web3.eth.net.getId()}

# Contract Addresses
DELIVERY_VERIFICATION_ADDRESS=${deliveryVerification.address}
ENVIRONMENTAL_TRUST_TOKEN_ADDRESS=${environmentalTrustToken.address}
CARBON_CREDIT_TOKEN_ADDRESS=${carbonCreditToken.address}

# Default Account (for development only)
DEFAULT_ACCOUNT=${accounts[0]}
PRIVATE_KEY=0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d

# Gas Settings
DEFAULT_GAS_LIMIT=500000
DEFAULT_GAS_PRICE=20000000000

# Demo Configuration
DEMO_MODE_ENABLED=true
DEMO_DATA_CREATED=${CONFIGURATION.demoData.enabled}
`;
    
    fs.writeFileSync(
      path.join(artifactsDir, 'blockchain.env'),
      envConfig
    );
    
    console.log("✅ Integration documentation created:");
    console.log("   • integration_guide.json - Comprehensive integration guide");
    console.log("   • blockchain.env - Environment configuration file");
    
    // Final Configuration Summary
    console.log("\n🎉 CONFIGURATION COMPLETE!");
    console.log("=" .repeat(80));
    console.log("🚀 QuantumEco Intelligence Blockchain Platform Ready!");
    console.log("\n📋 Configuration Summary:");
    console.log(`   • Network: ${network}`);
    console.log(`   • Total Contracts: 3`);
    console.log(`   • Demo Data: ${CONFIGURATION.demoData.enabled ? 'Created' : 'Disabled'}`);
    console.log(`   • Authorized Verifiers: ${CONFIGURATION.accessControl.setupMultipleVerifiers ? CONFIGURATION.accessControl.verifierCount : 1}`);
    
    try {
      const finalNetworkStats = await deliveryVerification.getNetworkStatistics();
      console.log("\n📊 Final Network State:");
      console.log(`   • Total Deliveries: ${finalNetworkStats[2]}`);
      console.log(`   • Total Carbon Saved: ${(finalNetworkStats[0] / 1000).toFixed(2)} kg`);
      console.log(`   • Total Cost Saved: $${(finalNetworkStats[1] / 100).toFixed(2)}`);
    } catch (error) {
      console.log("   • Network stats: Unable to retrieve");
    }
    
    console.log("\n🔗 Next Steps:");
    console.log("   1. Update backend with new contract addresses");
    console.log("   2. Test integration with: python test_blockchain_integration.py");
    console.log("   3. Start demo data generation");
    console.log("   4. Begin frontend integration");
    console.log("=" .repeat(80));
    
  } catch (error) {
    console.error("\n❌ CONFIGURATION FAILED!");
    console.error("=" .repeat(80));
    console.error("Error Details:", error);
    console.error("=" .repeat(80));
    throw error;
  }
};
