/**
 * QuantumEco Intelligence - Initial Migration
 * 
 * This migration handles the initial setup and deployment of the Migrations contract
 * which is required by Truffle for tracking deployment state.
 */

const Migrations = artifacts.require("Migrations");

module.exports = async function (deployer, network, accounts) {
  console.log("\n🚀 QuantumEco Intelligence - Initial Migration");
  console.log("=" .repeat(60));
  console.log(`📡 Network: ${network}`);
  console.log(`👤 Deployer: ${accounts[0]}`);
  console.log(`💰 Balance: ${web3.utils.fromWei(await web3.eth.getBalance(accounts[0]), 'ether')} ETH`);
  console.log("=" .repeat(60));

  // Deploy Migrations contract
  try {
    await deployer.deploy(Migrations, {
      from: accounts[0],
      gas: 500000,
      gasPrice: network === 'development' ? 20000000000 : undefined // 20 Gwei for local
    });
    console.log("✅ Migrations contract deployed successfully");
    console.log(`📍 Address: ${Migrations.address}`);
    console.log("=" .repeat(60));
  } catch (error) {
    console.error("❌ Initial migration failed:", error);
    throw error;
  }
};
