// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title DeliveryVerification - Blockchain storage and verification of delivery certificates
/// @author QuantumEco Intelligence
/// @notice Stores delivery optimization results, issues Environmental Trust Tokens, and tracks network stats

contract DeliveryVerification {
    // --- Data Structures ---

    struct DeliveryRecord {
        string routeId;
        string vehicleId;
        uint256 carbonSaved;      // in grams (for precision)
        uint256 costSaved;        // in cents (for precision)
        uint256 distanceKm;       // in meters (for precision)
        uint256 optimizationScore;
        uint256 timestamp;
        bool verified;
        string verificationHash;
    }

    struct EnvironmentalTrustToken {
        uint256 tokenId;
        string routeId;
        uint256 trustScore;
        uint256 carbonImpact;         // in grams
        uint256 sustainabilityRating; // 0-100
        uint256 timestamp;
        bool active;
    }

    // --- State Variables ---

    mapping(string => DeliveryRecord) public deliveries; // routeId => record
    mapping(uint256 => EnvironmentalTrustToken) public ettTokens; // tokenId => ETT
    uint256 public ettTokenCounter = 1;

    // Network statistics
    uint256 public totalCarbonSaved; // in grams
    uint256 public totalCostSaved;   // in cents
    uint256 public totalDeliveries;

    // Events
    event DeliveryRecordAdded(string indexed routeId, string vehicleId, uint256 carbonSaved, uint256 costSaved, uint256 timestamp, string verificationHash);
    event EnvironmentalTrustTokenCreated(uint256 indexed tokenId, string routeId, uint256 trustScore, uint256 carbonImpact, uint256 sustainabilityRating, uint256 timestamp);
    event DeliveryVerified(string indexed routeId, bool verified);

    // --- Core Functions ---

    /// @notice Store delivery certificate on blockchain
    function addDeliveryRecord(
        string memory routeId,
        string memory vehicleId,
        uint256 carbonSaved,
        uint256 costSaved,
        uint256 distanceKm,
        uint256 optimizationScore,
        string memory verificationHash
    ) public {
        require(bytes(routeId).length > 0, "Route ID required");
        require(bytes(vehicleId).length > 0, "Vehicle ID required");
        require(carbonSaved < 100000000, "Carbon saved too large");
        require(costSaved < 100000000, "Cost saved too large");
        require(distanceKm > 0, "Distance must be positive");
        require(deliveries[routeId].timestamp == 0, "Record already exists");

        deliveries[routeId] = DeliveryRecord({
            routeId: routeId,
            vehicleId: vehicleId,
            carbonSaved: carbonSaved,
            costSaved: costSaved,
            distanceKm: distanceKm,
            optimizationScore: optimizationScore,
            timestamp: block.timestamp,
            verified: true,
            verificationHash: verificationHash
        });

        // Update network stats
        totalCarbonSaved += carbonSaved;
        totalCostSaved += costSaved;
        totalDeliveries += 1;

        emit DeliveryRecordAdded(routeId, vehicleId, carbonSaved, costSaved, block.timestamp, verificationHash);
    }

    /// @notice Generate Environmental Trust Token (ETT)
    function createTrustToken(
        string memory routeId,
        uint256 trustScore,
        uint256 carbonImpact,
        uint256 sustainabilityRating
    ) public returns (uint256) {
        require(bytes(routeId).length > 0, "Route ID required");
        require(trustScore <= 100, "Trust score out of range");
        require(sustainabilityRating <= 100, "Sustainability rating out of range");

        uint256 tokenId = ettTokenCounter;
        ettTokens[tokenId] = EnvironmentalTrustToken({
            tokenId: tokenId,
            routeId: routeId,
            trustScore: trustScore,
            carbonImpact: carbonImpact,
            sustainabilityRating: sustainabilityRating,
            timestamp: block.timestamp,
            active: true
        });
        ettTokenCounter += 1;

        emit EnvironmentalTrustTokenCreated(tokenId, routeId, trustScore, carbonImpact, sustainabilityRating, block.timestamp);
        return tokenId;
    }

    /// @notice Verify certificate authenticity
    function verifyDeliveryRecord(string memory routeId) public view returns (bool) {
        DeliveryRecord memory record = deliveries[routeId];
        if (record.timestamp == 0) {
            return false;
        }
        return record.verified;
    }

    /// @notice Retrieve delivery record details
    function getDeliveryRecord(string memory routeId) public view returns (
        string memory, string memory, uint256, uint256, uint256, uint256, bool, string memory
    ) {
        DeliveryRecord memory record = deliveries[routeId];
        require(record.timestamp != 0, "Record not found");
        return (
            record.routeId,
            record.vehicleId,
            record.carbonSaved,
            record.costSaved,
            record.distanceKm,
            record.optimizationScore,
            record.verified,
            record.verificationHash
        );
    }

    /// @notice Retrieve blockchain network statistics
    function getNetworkStats() public view returns (
        uint256, uint256, uint256
    ) {
        return (totalCarbonSaved, totalCostSaved, totalDeliveries);
    }

    /// @notice Retrieve ETT details
    function getTrustToken(uint256 tokenId) public view returns (
        uint256, string memory, uint256, uint256, uint256, uint256, bool
    ) {
        EnvironmentalTrustToken memory token = ettTokens[tokenId];
        require(token.tokenId != 0, "Token not found");
        return (
            token.tokenId,
            token.routeId,
            token.trustScore,
            token.carbonImpact,
            token.sustainabilityRating,
            token.timestamp,
            token.active
        );
    }
}
