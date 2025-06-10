// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract DeliveryVerification is Ownable, ReentrancyGuard {
    struct DeliveryRecord {
        string routeId;
        string vehicleId;
        uint256 carbonSaved;
        uint256 costSaved;
        uint256 distance;
        uint256 optimizationScore;
        uint256 timestamp;
        address verifier;
        string verificationHash;
    }
    
    struct NetworkStats {
        uint256 totalCarbonSaved;
        uint256 totalCostSaved;
        uint256 totalDeliveries;
        uint256 totalDistance;
    }

    mapping(string => DeliveryRecord) public records;
    mapping(address => bool) public authorizedVerifiers;
    NetworkStats public stats;
    
    event DeliveryRecordAdded(
        string indexed routeId,
        address indexed verifier,
        uint256 carbonSaved,
        uint256 costSaved,
        uint256 timestamp
    );
    
    event VerifierAuthorized(address verifier);
    event VerifierRevoked(address verifier);

    modifier onlyVerifier() {
        require(authorizedVerifiers[msg.sender], "Unauthorized verifier");
        _;
    }

    constructor() {
        authorizedVerifiers[msg.sender] = true;
    }

    function addDeliveryRecord(
        string memory routeId,
        string memory vehicleId,
        uint256 carbonSaved,
        uint256 costSaved,
        uint256 distance,
        uint256 optimizationScore,
        string memory verificationHash
    ) external onlyVerifier nonReentrant {
        require(bytes(routeId).length > 0, "Invalid route ID");
        require(bytes(vehicleId).length > 0, "Invalid vehicle ID");
        require(optimizationScore <= 100, "Invalid score");
        
        records[routeId] = DeliveryRecord({
            routeId: routeId,
            vehicleId: vehicleId,
            carbonSaved: carbonSaved,
            costSaved: costSaved,
            distance: distance,
            optimizationScore: optimizationScore,
            timestamp: block.timestamp,
            verifier: msg.sender,
            verificationHash: verificationHash
        });

        stats.totalCarbonSaved += carbonSaved;
        stats.totalCostSaved += costSaved;
        stats.totalDeliveries++;
        stats.totalDistance += distance;

        emit DeliveryRecordAdded(routeId, msg.sender, carbonSaved, costSaved, block.timestamp);
    }

    function verifyDelivery(string memory routeId) external view returns (bool) {
        return bytes(records[routeId].routeId).length > 0;
    }

    function authorizeVerifier(address verifier) external onlyOwner {
        authorizedVerifiers[verifier] = true;
        emit VerifierAuthorized(verifier);
    }

    function revokeVerifier(address verifier) external onlyOwner {
        authorizedVerifiers[verifier] = false;
        emit VerifierRevoked(verifier);
    }
}
