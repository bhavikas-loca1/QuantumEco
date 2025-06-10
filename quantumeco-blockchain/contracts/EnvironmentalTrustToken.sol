// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

interface IDeliveryVerification {
    function verifyDeliveryRecord(string memory routeId) external view returns (bool);
    function getDeliveryRecord(string memory routeId) external view returns (
        string memory, string memory, uint256, uint256, uint256, 
        uint256, uint256, uint256, address, bool, string memory, string memory
    );
}

/**
 * @title EnvironmentalTrustToken (ETT)
 * @dev NFT-based Environmental Trust Tokens for QuantumEco Intelligence
 * @author QuantumEco Intelligence Team
 */
contract EnvironmentalTrustToken is ERC721, ERC721Enumerable, Ownable, ReentrancyGuard, Pausable {
    using Counters for Counters.Counter;
    
    // ===== STRUCTS =====
    
    struct ETTData {
        uint256 tokenId;
        string routeId;
        uint256 trustScore;           // 0-100
        uint256 carbonImpact;         // in grams (positive = saved, negative = excess)
        uint256 sustainabilityRating; // 0-100
        uint256 validityPeriod;       // timestamp until which token is valid
        address issuer;
        uint256 createdAt;
        bool isActive;
        string metadataURI;
        ETTLevel level;
    }
    
    enum ETTLevel {
        BRONZE,    // 0-69 trust score
        SILVER,    // 70-84 trust score
        GOLD,      // 85-94 trust score
        PLATINUM   // 95-100 trust score
    }
    
    struct TrustMetrics {
        uint256 routeOptimizationScore;
        uint256 carbonEfficiency;
        uint256 costEfficiency;
        uint256 consistencyScore;
        uint256 innovationFactor;
    }
    
    // ===== STATE VARIABLES =====
    
    Counters.Counter private _tokenIdCounter;
    IDeliveryVerification public deliveryVerification;
    
    mapping(uint256 => ETTData) public ettTokens;
    mapping(string => uint256) public routeToToken;
    mapping(address => uint256[]) public ownerTokens;
    mapping(ETTLevel => uint256) public levelCounts;
    mapping(uint256 => TrustMetrics) public tokenMetrics;
    
    uint256 public constant MAX_TRUST_SCORE = 100;
    uint256 public constant MAX_SUSTAINABILITY_RATING = 100;
    uint256 public constant DEFAULT_VALIDITY_PERIOD = 365 days;
    
    string private _baseTokenURI;
    
    // ===== EVENTS =====
    
    event ETTCreated(
        uint256 indexed tokenId,
        string indexed routeId,
        address indexed recipient,
        uint256 trustScore,
        uint256 carbonImpact,
        uint256 sustainabilityRating,
        ETTLevel level
    );
    
    event ETTLevelUpgraded(
        uint256 indexed tokenId,
        ETTLevel oldLevel,
        ETTLevel newLevel
    );
    
    event ETTActivationChanged(
        uint256 indexed tokenId,
        bool isActive
    );
    
    event TrustScoreUpdated(
        uint256 indexed tokenId,
        uint256 oldScore,
        uint256 newScore
    );
    
    // ===== MODIFIERS =====
    
    modifier validTrustScore(uint256 score) {
        require(score <= MAX_TRUST_SCORE, "Invalid trust score");
        _;
    }
    
    modifier validSustainabilityRating(uint256 rating) {
        require(rating <= MAX_SUSTAINABILITY_RATING, "Invalid sustainability rating");
        _;
    }
    
    modifier tokenExists(uint256 tokenId) {
        require(_exists(tokenId), "Token does not exist");
        _;
    }
    
    modifier onlyTokenOwner(uint256 tokenId) {
        require(ownerOf(tokenId) == msg.sender, "Not token owner");
        _;
    }
    
    // ===== CONSTRUCTOR =====
    
    constructor(address _deliveryVerification) ERC721("Environmental Trust Token", "ETT") {
        require(_deliveryVerification != address(0), "Invalid delivery verification address");
        deliveryVerification = IDeliveryVerification(_deliveryVerification);
        _baseTokenURI = "https://api.quantumeco.io/ett/metadata/";
    }
    
    // ===== MAIN FUNCTIONS =====
    
    /**
     * @dev Create a new Environmental Trust Token
     * @param routeId Route identifier from verified delivery
     * @param recipient Address to receive the token
     * @param trustScore Trust score (0-100)
     * @param carbonImpact Carbon impact in grams
     * @param sustainabilityRating Sustainability rating (0-100)
     * @param validityPeriod Custom validity period (0 for default)
     * @return tokenId The created token ID
     */
    function createETT(
        string memory routeId,
        address recipient,
        uint256 trustScore,
        uint256 carbonImpact,
        uint256 sustainabilityRating,
        uint256 validityPeriod
    )
        external
        onlyOwner
        nonReentrant
        whenNotPaused
        validTrustScore(trustScore)
        validSustainabilityRating(sustainabilityRating)
        returns (uint256)
    {
        require(bytes(routeId).length > 0, "Route ID cannot be empty");
        require(recipient != address(0), "Invalid recipient address");
        require(routeToToken[routeId] == 0, "ETT already exists for this route");
        
        // Verify the delivery record exists
        require(deliveryVerification.verifyDeliveryRecord(routeId), "Delivery record not verified");
        
        // Get delivery record details for validation
        (, , uint256 carbonSaved, uint256 costSaved, , uint256 optimizationScore, , , , , , ) = 
            deliveryVerification.getDeliveryRecord(routeId);
        
        require(carbonSaved > 0, "No carbon savings recorded");
        
        _tokenIdCounter.increment();
        uint256 tokenId = _tokenIdCounter.current();
        
        // Determine ETT level based on trust score
        ETTLevel level = _calculateETTLevel(trustScore);
        
        // Set validity period
        uint256 validity = validityPeriod > 0 ? 
            block.timestamp + validityPeriod : 
            block.timestamp + DEFAULT_VALIDITY_PERIOD;
        
        // Create ETT data
        ettTokens[tokenId] = ETTData({
            tokenId: tokenId,
            routeId: routeId,
            trustScore: trustScore,
            carbonImpact: carbonImpact,
            sustainabilityRating: sustainabilityRating,
            validityPeriod: validity,
            issuer: msg.sender,
            createdAt: block.timestamp,
            isActive: true,
            metadataURI: string(abi.encodePacked(_baseTokenURI, _toString(tokenId))),
            level: level
        });
        
        // Create trust metrics from delivery data
        tokenMetrics[tokenId] = TrustMetrics({
            routeOptimizationScore: optimizationScore,
            carbonEfficiency: _calculateCarbonEfficiency(carbonSaved, carbonImpact),
            costEfficiency: _calculateCostEfficiency(costSaved),
            consistencyScore: trustScore,
            innovationFactor: _calculateInnovationFactor(optimizationScore, trustScore)
        });
        
        // Update mappings
        routeToToken[routeId] = tokenId;
        ownerTokens[recipient].push(tokenId);
        levelCounts[level]++;
        
        // Mint the token
        _safeMint(recipient, tokenId);
        
        emit ETTCreated(
            tokenId,
            routeId,
            recipient,
            trustScore,
            carbonImpact,
            sustainabilityRating,
            level
        );
        
        return tokenId;
    }
    
    /**
     * @dev Update trust score for existing ETT
     * @param tokenId Token to update
     * @param newTrustScore New trust score
     */
    function updateTrustScore(uint256 tokenId, uint256 newTrustScore)
        external
        onlyOwner
        tokenExists(tokenId)
        validTrustScore(newTrustScore)
    {
        ETTData storage ettData = ettTokens[tokenId];
        require(ettData.isActive, "Token is not active");
        require(block.timestamp <= ettData.validityPeriod, "Token has expired");
        
        uint256 oldScore = ettData.trustScore;
        ETTLevel oldLevel = ettData.level;
        
        ettData.trustScore = newTrustScore;
        ETTLevel newLevel = _calculateETTLevel(newTrustScore);
        
        if (newLevel != oldLevel) {
            levelCounts[oldLevel]--;
            levelCounts[newLevel]++;
            ettData.level = newLevel;
            
            emit ETTLevelUpgraded(tokenId, oldLevel, newLevel);
        }
        
        // Update consistency score in metrics
        tokenMetrics[tokenId].consistencyScore = newTrustScore;
        
        emit TrustScoreUpdated(tokenId, oldScore, newTrustScore);
    }
    
    /**
     * @dev Activate or deactivate an ETT
     * @param tokenId Token to update
     * @param isActive New activation status
     */
    function setETTActivation(uint256 tokenId, bool isActive)
        external
        onlyOwner
        tokenExists(tokenId)
    {
        require(ettTokens[tokenId].isActive != isActive, "Already in requested state");
        
        ettTokens[tokenId].isActive = isActive;
        
        emit ETTActivationChanged(tokenId, isActive);
    }
    
    /**
     * @dev Extend validity period of an ETT
     * @param tokenId Token to extend
     * @param additionalTime Additional time in seconds
     */
    function extendValidity(uint256 tokenId, uint256 additionalTime)
        external
        onlyOwner
        tokenExists(tokenId)
    {
        require(additionalTime > 0, "Additional time must be positive");
        
        ettTokens[tokenId].validityPeriod += additionalTime;
    }
    
    /**
     * @dev Get complete ETT data
     * @param tokenId Token ID
     * @return Complete ETT data struct
     */
    function getETTData(uint256 tokenId)
        external
        view
        tokenExists(tokenId)
        returns (ETTData memory)
    {
        return ettTokens[tokenId];
    }
    
    /**
     * @dev Get trust metrics for a token
     * @param tokenId Token ID
     * @return Trust metrics struct
     */
    function getTrustMetrics(uint256 tokenId)
        external
        view
        tokenExists(tokenId)
        returns (TrustMetrics memory)
    {
        return tokenMetrics[tokenId];
    }
    
    /**
     * @dev Get ETT level distribution
     * @return Array of counts for each level
     */
    function getLevelDistribution()
        external
        view
        returns (uint256[] memory)
    {
        uint256[] memory distribution = new uint256[](4);
        distribution[0] = levelCounts[ETTLevel.BRONZE];
        distribution[1] = levelCounts[ETTLevel.SILVER];
        distribution[2] = levelCounts[ETTLevel.GOLD];
        distribution[3] = levelCounts[ETTLevel.PLATINUM];
        return distribution;
    }
    
    /**
     * @dev Get tokens owned by an address
     * @param owner Owner address
     * @return Array of token IDs
     */
    function getTokensByOwner(address owner)
        external
        view
        returns (uint256[] memory)
    {
        return ownerTokens[owner];
    }
    
    /**
     * @dev Check if ETT is valid and active
     * @param tokenId Token ID
     * @return True if valid and active
     */
    function isValidETT(uint256 tokenId)
        external
        view
        tokenExists(tokenId)
        returns (bool)
    {
        ETTData memory ettData = ettTokens[tokenId];
        return ettData.isActive && block.timestamp <= ettData.validityPeriod;
    }
    
    /**
     * @dev Get total number of ETTs created
     * @return Total count
     */
    function getTotalETTs() external view returns (uint256) {
        return _tokenIdCounter.current();
    }
    
    // ===== ADMIN FUNCTIONS =====
    
    /**
     * @dev Set base URI for token metadata
     * @param newBaseURI New base URI
     */
    function setBaseURI(string memory newBaseURI) external onlyOwner {
        _baseTokenURI = newBaseURI;
    }
    
    /**
     * @dev Update delivery verification contract
     * @param newDeliveryVerification New contract address
     */
    function updateDeliveryVerification(address newDeliveryVerification) external onlyOwner {
        require(newDeliveryVerification != address(0), "Invalid address");
        deliveryVerification = IDeliveryVerification(newDeliveryVerification);
    }
    
    /**
     * @dev Pause contract (emergency use)
     */
    function pause() external onlyOwner {
        _pause();
    }
    
    /**
     * @dev Unpause contract
     */
    function unpause() external onlyOwner {
        _unpause();
    }
    
    // ===== INTERNAL FUNCTIONS =====
    
    function _calculateETTLevel(uint256 trustScore) internal pure returns (ETTLevel) {
        if (trustScore >= 95) return ETTLevel.PLATINUM;
        if (trustScore >= 85) return ETTLevel.GOLD;
        if (trustScore >= 70) return ETTLevel.SILVER;
        return ETTLevel.BRONZE;
    }
    
    function _calculateCarbonEfficiency(uint256 carbonSaved, uint256 carbonImpact) 
        internal 
        pure 
        returns (uint256) 
    {
        if (carbonSaved == 0) return 0;
        return (carbonImpact * 100) / carbonSaved;
    }
    
    function _calculateCostEfficiency(uint256 costSaved) internal pure returns (uint256) {
        // Simplified cost efficiency calculation
        return costSaved > 0 ? (costSaved / 100) : 0; // Convert cents to dollars
    }
    
    function _calculateInnovationFactor(uint256 optimizationScore, uint256 trustScore) 
        internal 
        pure 
        returns (uint256) 
    {
        return (optimizationScore + trustScore) / 2;
    }
    
    function _baseURI() internal view virtual override returns (string memory) {
        return _baseTokenURI;
    }
    
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId,
        uint256 batchSize
    ) internal virtual override(ERC721, ERC721Enumerable) whenNotPaused {
        super._beforeTokenTransfer(from, to, tokenId, batchSize);
        
        // Update owner tokens mapping
        if (from != address(0) && to != address(0)) {
            _removeTokenFromOwnerArray(from, tokenId);
            ownerTokens[to].push(tokenId);
        }
    }
    
    function _removeTokenFromOwnerArray(address owner, uint256 tokenId) internal {
        uint256[] storage tokens = ownerTokens[owner];
        for (uint256 i = 0; i < tokens.length; i++) {
            if (tokens[i] == tokenId) {
                tokens[i] = tokens[tokens.length - 1];
                tokens.pop();
                break;
            }
        }
    }
    
    function _toString(uint256 value) internal pure returns (string memory) {
        if (value == 0) {
            return "0";
        }
        uint256 temp = value;
        uint256 digits;
        while (temp != 0) {
            digits++;
            temp /= 10;
        }
        bytes memory buffer = new bytes(digits);
        while (value != 0) {
            digits -= 1;
            buffer[digits] = bytes1(uint8(48 + uint256(value % 10)));
            value /= 10;
        }
        return string(buffer);
    }
    
    function supportsInterface(bytes4 interfaceId)
        public
        view
        virtual
        override(ERC721, ERC721Enumerable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
