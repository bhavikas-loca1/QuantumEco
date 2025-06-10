/**
 * QuantumEco Intelligence - Main Contract Deployment
 * 
 * This migration deploys all core smart contracts for the QuantumEco Intelligence platform:
 * - DeliveryVerification: Main delivery verification and tracking
 * - EnvironmentalTrustToken: NFT-based environmental trust tokens
 * - CarbonCreditToken: ERC1155-based carbon credit tokens
 */

const DeliveryVerification = artifacts.require("DeliveryVerification");
const EnvironmentalTrustToken = artifacts.require("EnvironmentalTrustToken");
const CarbonCreditToken = artifacts.require("CarbonCreditToken");

// Configuration constants
const DEPLOYMENT_CONFIG = {
  // Gas settings per network
  gasSettings: {
    development: {
      gas: 6721975,
      gasPrice: 20000000000, // 20 Gwei
    },
    mainnet: {
      gas: 8000000,
      gasPrice: undefined, // Let web3 decide
    },
    testnet: {
      gas: 8000000,
      gasPrice: 10000000000, // 10 Gwei
    }
  },
  
  // Initial contract parameters
  contracts: {
    deliveryVerification: {
      name: "QuantumEco Delivery Verification",
      version: "1.0.0"
    },
    environmentalTrustToken: {
      name: "Environmental Trust Token",
      symbol: "ETT",
      baseURI: "https://api.quantumeco.io/ett/metadata/"
    },
    carbonCreditToken: {
      baseURI: "https://api.quantumeco.io/carbon-credits/metadata/{id}.json"
    }
  }
};

module.exports = async function (deployer, network, accounts) {
  console.log("\n🌍 QuantumEco Intelligence - Main Contract Deployment");
  console.log("=" .repeat(80));
  console.log(`📡 Network: ${network}`);
  console.log(`👤 Deployer: ${accounts[0]}`);
  console.log(`💰 Balance: ${web3.utils.fromWei(await web3.eth.getBalance(accounts[0]), 'ether')} ETH`);
  console.log(`⛽ Gas Limit: ${DEPLOYMENT_CONFIG.gasSettings[network]?.gas || 'auto'}`);
  console.log(`💸 Gas Price: ${DEPLOYMENT_CONFIG.gasSettings[network]?.gasPrice || 'auto'}`);
  console.log("=" .repeat(80));

  try {
    // Get gas settings for current network
    const gasSettings = DEPLOYMENT_CONFIG.gasSettings[network] || DEPLOYMENT_CONFIG.gasSettings.development;
    
    // Deploy DeliveryVerification contract first (no dependencies)
    console.log("\n📦 Step 1: Deploying DeliveryVerification Contract...");
    console.log("-" .repeat(50));
    
    const deliveryVerificationStartTime = Date.now();
    
    await deployer.deploy(DeliveryVerification, {
      from: accounts[0],
      ...gasSettings
    });
    
    const deliveryVerificationInstance = await DeliveryVerification.deployed();
    const deliveryVerificationDeployTime = Date.now() - deliveryVerificationStartTime;
    
    console.log("✅ DeliveryVerification deployed successfully");
    console.log(`📍 Address: ${deliveryVerificationInstance.address}`);
    console.log(`⏱️  Deploy Time: ${deliveryVerificationDeployTime}ms`);
    console.log(`⛽ Gas Used: ${(await web3.eth.getTransactionReceipt(deliveryVerificationInstance.transactionHash)).gasUsed}`);
    
    // Verify deployment
    const totalDeliveries = await deliveryVerificationInstance.totalDeliveries();
    console.log(`🔍 Verification: Total Deliveries = ${totalDeliveries.toString()}`);
    
    // Deploy EnvironmentalTrustToken contract (depends on DeliveryVerification)
    console.log("\n🌱 Step 2: Deploying EnvironmentalTrustToken Contract...");
    console.log("-" .repeat(50));
    
    const ettStartTime = Date.now();
    
    await deployer.deploy(
      EnvironmentalTrustToken,
      deliveryVerificationInstance.address, // Constructor parameter
      {
        from: accounts[0],
        ...gasSettings
      }
    );
    
    const ettInstance = await EnvironmentalTrustToken.deployed();
    const ettDeployTime = Date.now() - ettStartTime;
    
    console.log("✅ EnvironmentalTrustToken deployed successfully");
    console.log(`📍 Address: ${ettInstance.address}`);
    console.log(`⏱️  Deploy Time: ${ettDeployTime}ms`);
    console.log(`⛽ Gas Used: ${(await web3.eth.getTransactionReceipt(ettInstance.transactionHash)).gasUsed}`);
    console.log(`🔗 Linked to DeliveryVerification: ${deliveryVerificationInstance.address}`);
    
    // Verify ETT deployment
    const ettName = await ettInstance.name();
    const ettSymbol = await ettInstance.symbol();
    const totalETTs = await ettInstance.getTotalETTs();
    console.log(`🔍 Verification: Name="${ettName}", Symbol="${ettSymbol}", Total ETTs=${totalETTs.toString()}`);
    
    // Deploy CarbonCreditToken contract (depends on DeliveryVerification)
    console.log("\n💚 Step 3: Deploying CarbonCreditToken Contract...");
    console.log("-" .repeat(50));
    
    const carbonCreditStartTime = Date.now();
    
    await deployer.deploy(
      CarbonCreditToken,
      deliveryVerificationInstance.address, // Constructor parameter
      {
        from: accounts[0],
        ...gasSettings
      }
    );
    
    const carbonCreditInstance = await CarbonCreditToken.deployed();
    const carbonCreditDeployTime = Date.now() - carbonCreditStartTime;
    
    console.log("✅ CarbonCreditToken deployed successfully");
    console.log(`📍 Address: ${carbonCreditInstance.address}`);
    console.log(`⏱️  Deploy Time: ${carbonCreditDeployTime}ms`);
    console.log(`⛽ Gas Used: ${(await web3.eth.getTransactionReceipt(carbonCreditInstance.transactionHash)).gasUsed}`);
    console.log(`🔗 Linked to DeliveryVerification: ${deliveryVerificationInstance.address}`);
    
    // Verify CarbonCreditToken deployment
    const totalCredits = await carbonCreditInstance.getTotalCredits();
    const marketStats = await carbonCreditInstance.getMarketStatistics();
    console.log(`🔍 Verification: Total Credits=${totalCredits.toString()}, Market Stats Available=true`);
    
    // Calculate total deployment statistics
    const totalDeployTime = deliveryVerificationDeployTime + ettDeployTime + carbonCreditDeployTime;
    const totalGasUsed = 
      (await web3.eth.getTransactionReceipt(deliveryVerificationInstance.transactionHash)).gasUsed +
      (await web3.eth.getTransactionReceipt(ettInstance.transactionHash)).gasUsed +
      (await web3.eth.getTransactionReceipt(carbonCreditInstance.transactionHash)).gasUsed;
    
    const totalCostEth = web3.utils.fromWei(
      web3.utils.toBN(totalGasUsed).mul(web3.utils.toBN(gasSettings.gasPrice || 20000000000)),
      'ether'
    );
    
    // Save deployment information for integration
    const deploymentInfo = {
      network: network,
      deployer: accounts[0],
      timestamp: new Date().toISOString(),
      contracts: {
        DeliveryVerification: {
          address: deliveryVerificationInstance.address,
          transactionHash: deliveryVerificationInstance.transactionHash,
          gasUsed: (await web3.eth.getTransactionReceipt(deliveryVerificationInstance.transactionHash)).gasUsed,
          deployTime: deliveryVerificationDeployTime
        },
        EnvironmentalTrustToken: {
          address: ettInstance.address,
          transactionHash: ettInstance.transactionHash,
          gasUsed: (await web3.eth.getTransactionReceipt(ettInstance.transactionHash)).gasUsed,
          deployTime: ettDeployTime,
          dependencies: {
            deliveryVerification: deliveryVerificationInstance.address
          }
        },
        CarbonCreditToken: {
          address: carbonCreditInstance.address,
          transactionHash: carbonCreditInstance.transactionHash,
          gasUsed: (await web3.eth.getTransactionReceipt(carbonCreditInstance.transactionHash)).gasUsed,
          deployTime: carbonCreditDeployTime,
          dependencies: {
            deliveryVerification: deliveryVerificationInstance.address
          }
        }
      },
      totalStats: {
        totalDeployTime: totalDeployTime,
        totalGasUsed: totalGasUsed,
        totalCostEth: totalCostEth,
        averageGasPrice: gasSettings.gasPrice || 'variable'
      }
    };
    
    // Write deployment info to file (for integration with Python backend)
    const fs = require('fs');
    const path = require('path');
    
    // Ensure artifacts directory exists
    const artifactsDir = path.join(__dirname, '..', 'artifacts');
    if (!fs.existsSync(artifactsDir)) {
      fs.mkdirSync(artifactsDir, { recursive: true });
    }
    
    // Write deployment info
    fs.writeFileSync(
      path.join(artifactsDir, 'deployment_info.json'),
      JSON.stringify(deploymentInfo, null, 2)
    );
    
    // Write contract addresses for easy integration
    const contractAddresses = {
      DeliveryVerification: deliveryVerificationInstance.address,
      EnvironmentalTrustToken: ettInstance.address,
      CarbonCreditToken: carbonCreditInstance.address
    };
    
    fs.writeFileSync(
      path.join(artifactsDir, 'contract_addresses.json'),
      JSON.stringify(contractAddresses, null, 2)
    );
    
    // Write contract ABIs for integration
    const contractABIs = {
      DeliveryVerification: DeliveryVerification.abi,
      EnvironmentalTrustToken: EnvironmentalTrustToken.abi,
      CarbonCreditToken: CarbonCreditToken.abi
    };
    
    fs.writeFileSync(
      path.join(artifactsDir, 'contract_abis.json'),
      JSON.stringify(contractABIs, null, 2)
    );
    
    // Final deployment summary
    console.log("\n🎉 DEPLOYMENT COMPLETE!");
    console.log("=" .repeat(80));
    console.log("📊 Deployment Summary:");
    console.log(`   • Total Contracts: 3`);
    console.log(`   • Total Deploy Time: ${totalDeployTime}ms`);
    console.log(`   • Total Gas Used: ${totalGasUsed.toLocaleString()}`);
    console.log(`   • Total Cost: ${totalCostEth} ETH`);
    console.log(`   • Network: ${network}`);
    console.log("\n📋 Contract Addresses:");
    console.log(`   • DeliveryVerification: ${deliveryVerificationInstance.address}`);
    console.log(`   • EnvironmentalTrustToken: ${ettInstance.address}`);
    console.log(`   • CarbonCreditToken: ${carbonCreditInstance.address}`);
    console.log("\n📁 Integration Files Created:");
    console.log(`   • deployment_info.json - Complete deployment details`);
    console.log(`   • contract_addresses.json - Contract addresses for backend`);
    console.log(`   • contract_abis.json - Contract ABIs for integration`);
    console.log("=" .repeat(80));
    
    // Deployment verification tests
    console.log("\n🔍 Running Deployment Verification Tests...");
    console.log("-" .repeat(50));
    
    // Test DeliveryVerification
    try {
      const networkStats = await deliveryVerificationInstance.getNetworkStatistics();
      console.log("✅ DeliveryVerification: getNetworkStatistics() - Working");
    } catch (error) {
      console.log("❌ DeliveryVerification: getNetworkStatistics() - Failed");
    }
    
    // Test EnvironmentalTrustToken
    try {
      const deliveryVerificationAddress = await ettInstance.deliveryVerification();
      if (deliveryVerificationAddress.toLowerCase() === deliveryVerificationInstance.address.toLowerCase()) {
        console.log("✅ EnvironmentalTrustToken: Linked to DeliveryVerification - Working");
      } else {
        console.log("❌ EnvironmentalTrustToken: Incorrect DeliveryVerification link");
      }
    } catch (error) {
      console.log("❌ EnvironmentalTrustToken: Link verification - Failed");
    }
    
    // Test CarbonCreditToken
    try {
      const deliveryVerificationAddress = await carbonCreditInstance.deliveryVerification();
      if (deliveryVerificationAddress.toLowerCase() === deliveryVerificationInstance.address.toLowerCase()) {
        console.log("✅ CarbonCreditToken: Linked to DeliveryVerification - Working");
      } else {
        console.log("❌ CarbonCreditToken: Incorrect DeliveryVerification link");
      }
    } catch (error) {
      console.log("❌ CarbonCreditToken: Link verification - Failed");
    }
    
    console.log("\n🚀 Ready for Phase 3: Contract Configuration");
    console.log("=" .repeat(80));
    
  } catch (error) {
    console.error("\n❌ DEPLOYMENT FAILED!");
    console.error("=" .repeat(80));
    console.error("Error Details:", error);
    console.error("=" .repeat(80));
    throw error;
  }
};
