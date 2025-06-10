// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
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
 * @title CarbonCreditToken
 * @dev ERC1155-based Carbon Credit tokens for QuantumEco Intelligence
 * @author QuantumEco Intelligence Team
 */
contract CarbonCreditToken is ERC1155, Ownable, ReentrancyGuard, Pausable {
    using Counters for Counters.Counter;
    
    // ===== STRUCTS =====
    
    struct CarbonCredit {
        uint256 creditId;
        string routeId;
        uint256 carbonAmount;         // in grams
        uint256 pricePerTon;          // in wei per ton
        address issuer;
        uint256 issuanceDate;
        uint256 expirationDate;
        bool isRetired;
        string standard;              // e.g., "VCS", "CDM", "QUANTUMECO"
        string metadataURI;
        CreditQuality quality;
    }
    
    enum CreditQuality {
        STANDARD,    // Basic carbon credits
        PREMIUM,     // High-quality verified credits
        GOLD,        // Gold standard credits
        PLATINUM     // Highest quality quantum-verified credits
    }
    
    struct TradingInfo {
        uint256 totalVolume;          // Total traded volume
        uint256 currentPrice;         // Current market price
        uint256 lastTradePrice;       // Last transaction price
        uint256 lastTradeTimestamp;   // When last trade occurred
        bool isTradeable;            // Whether credit can be traded
    }
    
    struct RetirementInfo {
        uint256 retiredAmount;
        address retiredBy;
        uint256 retirementDate;
        string retirementReason;
        string retirementCertificate;
    }
    
    // ===== STATE VARIABLES =====
    
    Counters.Counter private _creditIdCounter;
    IDeliveryVerification public deliveryVerification;
    
    mapping(uint256 => CarbonCredit) public carbonCredits;
    mapping(uint256 => TradingInfo) public tradingInfo;
    mapping(uint256 => RetirementInfo[]) public retirements;
    mapping(string => uint256) public routeToCredit;
    mapping(address => uint256[]) public issuerCredits;
    mapping(CreditQuality => uint256) public qualitySupply;
    
    uint256 public constant GRAMS_PER_TON = 1000000;
    uint256 public constant MAX_EXPIRATION_YEARS = 10;
    uint256 public constant MIN_CARBON_AMOUNT = 1000; // 1 kg minimum
    
    uint256 public totalCarbonCredits;
    uint256 public totalRetiredCredits;
    uint256 public totalTradingVolume;
    
    string public constant VERSION = "1.0.0";
    
    // ===== EVENTS =====
    
    event CarbonCreditIssued(
        uint256 indexed creditId,
        string indexed routeId,
        address indexed issuer,
        uint256 carbonAmount,
        uint256 pricePerTon,
        CreditQuality quality
    );
    
    event CarbonCreditTraded(
        uint256 indexed creditId,
        address indexed from,
        address indexed to,
        uint256 amount,
        uint256 pricePerTon
    );
    
    event CarbonCreditRetired(
        uint256 indexed creditId,
        address indexed retiredBy,
        uint256 amount,
        string reason
    );
    
    event CreditQualityUpgraded(
        uint256 indexed creditId,
        CreditQuality oldQuality,
        CreditQuality newQuality
    );
    
    event TradingStatusChanged(
        uint256 indexed creditId,
        bool isTradeable
    );
    
    // ===== MODIFIERS =====
    
    modifier validCreditId(uint256 creditId) {
        require(creditId > 0 && creditId <= _creditIdCounter.current(), "Invalid credit ID");
        _;
    }
    
    modifier creditExists(uint256 creditId) {
        require(carbonCredits[creditId].creditId != 0, "Credit does not exist");
        _;
    }
    
    modifier notExpired(uint256 creditId) {
        require(block.timestamp <= carbonCredits[creditId].expirationDate, "Credit has expired");
        _;
    }
    
    modifier notRetired(uint256 creditId) {
        require(!carbonCredits[creditId].isRetired, "Credit has been retired");
        _;
    }
    
    modifier onlyIssuer(uint256 creditId) {
        require(carbonCredits[creditId].issuer == msg.sender, "Not the issuer");
        _;
    }
    
    // ===== CONSTRUCTOR =====
    
    constructor(address _deliveryVerification) 
        ERC1155("https://api.quantumeco.io/carbon-credits/metadata/{id}.json") 
    {
        require(_deliveryVerification != address(0), "Invalid delivery verification address");
        deliveryVerification = IDeliveryVerification(_deliveryVerification);
    }
    
    // ===== MAIN FUNCTIONS =====
    
    /**
     * @dev Issue new carbon credits based on verified delivery records
     * @param routeId Route identifier from verified delivery
     * @param carbonAmount Amount of carbon credits in grams
     * @param pricePerTon Price per ton in wei
     * @param expirationYears Years until expiration (max 10)
     * @param standard Credit standard (e.g., "VCS", "CDM", "QUANTUMECO")
     * @param quality Quality level of the credit
     * @return creditId The created credit ID
     */
    function issueCarbonCredit(
        string memory routeId,
        uint256 carbonAmount,
        uint256 pricePerTon,
        uint256 expirationYears,
        string memory standard,
        CreditQuality quality
    )
        external
        onlyOwner
        nonReentrant
        whenNotPaused
        returns (uint256)
    {
        require(bytes(routeId).length > 0, "Route ID cannot be empty");
        require(carbonAmount >= MIN_CARBON_AMOUNT, "Carbon amount too small");
        require(pricePerTon > 0, "Price must be positive");
        require(expirationYears > 0 && expirationYears <= MAX_EXPIRATION_YEARS, "Invalid expiration years");
        require(bytes(standard).length > 0, "Standard cannot be empty");
        require(routeToCredit[routeId] == 0, "Credit already exists for this route");
        
        // Verify the delivery record exists and get carbon savings
        require(deliveryVerification.verifyDeliveryRecord(routeId), "Delivery record not verified");
        
        (, , uint256 carbonSaved, , , , , , , , , ) = 
            deliveryVerification.getDeliveryRecord(routeId);
        
        require(carbonSaved >= carbonAmount, "Credit amount exceeds verified savings");
        
        _creditIdCounter.increment();
        uint256 creditId = _creditIdCounter.current();
        
        uint256 expirationDate = block.timestamp + (expirationYears * 365 days);
        
        // Create carbon credit
        carbonCredits[creditId] = CarbonCredit({
            creditId: creditId,
            routeId: routeId,
            carbonAmount: carbonAmount,
            pricePerTon: pricePerTon,
            issuer: msg.sender,
            issuanceDate: block.timestamp,
            expirationDate: expirationDate,
            isRetired: false,
            standard: standard,
            metadataURI: string(abi.encodePacked("https://api.quantumeco.io/carbon-credits/metadata/", _toString(creditId), ".json")),
            quality: quality
        });
        
        // Initialize trading info
        tradingInfo[creditId] = TradingInfo({
            totalVolume: 0,
            currentPrice: pricePerTon,
            lastTradePrice: pricePerTon,
            lastTradeTimestamp: block.timestamp,
            isTradeable: true
        });
        
        // Update mappings and counters
        routeToCredit[routeId] = creditId;
        issuerCredits[msg.sender].push(creditId);
        qualitySupply[quality] += carbonAmount;
        totalCarbonCredits += carbonAmount;
        
        // Mint the credits as fungible tokens (amount = carbon amount in grams)
        _mint(msg.sender, creditId, carbonAmount, "");
        
        emit CarbonCreditIssued(
            creditId,
            routeId,
            msg.sender,
            carbonAmount,
            pricePerTon,
            quality
        );
        
        return creditId;
    }
    
    /**
     * @dev Trade carbon credits between addresses
     * @param creditId Credit ID to trade
     * @param to Recipient address
     * @param amount Amount to trade in grams
     * @param pricePerTon Agreed price per ton
     */
    function tradeCarbonCredit(
        uint256 creditId,
        address to,
        uint256 amount,
        uint256 pricePerTon
    )
        external
        payable
        nonReentrant
        whenNotPaused
        creditExists(creditId)
        notExpired(creditId)
        notRetired(creditId)
    {
        require(to != address(0), "Invalid recipient address");
        require(amount > 0, "Amount must be positive");
        require(balanceOf(msg.sender, creditId) >= amount, "Insufficient balance");
        require(tradingInfo[creditId].isTradeable, "Credit is not tradeable");
        
        uint256 totalPrice = (amount * pricePerTon) / GRAMS_PER_TON;
        require(msg.value >= totalPrice, "Insufficient payment");
        
        // Transfer credits
        safeTransferFrom(msg.sender, to, creditId, amount, "");
        
        // Update trading info
        TradingInfo storage trading = tradingInfo[creditId];
        trading.totalVolume += amount;
        trading.lastTradePrice = pricePerTon;
        trading.lastTradeTimestamp = block.timestamp;
        trading.currentPrice = pricePerTon; // Simple price update, could be more sophisticated
        
        totalTradingVolume += amount;
        
        // Refund excess payment
        if (msg.value > totalPrice) {
            payable(msg.sender).transfer(msg.value - totalPrice);
        }
        
        emit CarbonCreditTraded(creditId, msg.sender, to, amount, pricePerTon);
    }
    
    /**
     * @dev Retire carbon credits (permanent removal from circulation)
     * @param creditId Credit ID to retire
     * @param amount Amount to retire in grams
     * @param reason Reason for retirement
     */
    function retireCarbonCredit(
        uint256 creditId,
        uint256 amount,
        string memory reason
    )
        external
        nonReentrant
        whenNotPaused
        creditExists(creditId)
        notExpired(creditId)
    {
        require(amount > 0, "Amount must be positive");
        require(balanceOf(msg.sender, creditId) >= amount, "Insufficient balance");
        require(bytes(reason).length > 0, "Reason cannot be empty");
        
        // Burn the retired credits
        _burn(msg.sender, creditId, amount);
        
        // Record retirement
        retirements[creditId].push(RetirementInfo({
            retiredAmount: amount,
            retiredBy: msg.sender,
            retirementDate: block.timestamp,
            retirementReason: reason,
            retirementCertificate: string(abi.encodePacked("RET-", _toString(creditId), "-", _toString(block.timestamp)))
        }));
        
        // Update counters
        totalRetiredCredits += amount;
        qualitySupply[carbonCredits[creditId].quality] -= amount;
        
        // If all credits are retired, mark as retired
        if (totalSupply(creditId) == 0) {
            carbonCredits[creditId].isRetired = true;
        }
        
        emit CarbonCreditRetired(creditId, msg.sender, amount, reason);
    }
    
    /**
     * @dev Upgrade credit quality (only issuer)
     * @param creditId Credit ID to upgrade
     * @param newQuality New quality level
     */
    function upgradeCreditQuality(uint256 creditId, CreditQuality newQuality)
        external
        creditExists(creditId)
        onlyIssuer(creditId)
        notRetired(creditId)
    {
        CreditQuality oldQuality = carbonCredits[creditId].quality;
        require(newQuality > oldQuality, "Can only upgrade quality");
        
        uint256 creditAmount = carbonCredits[creditId].carbonAmount;
        
        // Update quality supply tracking
        qualitySupply[oldQuality] -= creditAmount;
        qualitySupply[newQuality] += creditAmount;
        
        carbonCredits[creditId].quality = newQuality;
        
        emit CreditQualityUpgraded(creditId, oldQuality, newQuality);
    }
    
    /**
     * @dev Set trading status for a credit
     * @param creditId Credit ID
     * @param isTradeable Whether credit can be traded
     */
    function setTradingStatus(uint256 creditId, bool isTradeable)
        external
        creditExists(creditId)
        onlyIssuer(creditId)
    {
        require(tradingInfo[creditId].isTradeable != isTradeable, "Already in requested state");
        
        tradingInfo[creditId].isTradeable = isTradeable;
        
        emit TradingStatusChanged(creditId, isTradeable);
    }
    
    // ===== VIEW FUNCTIONS =====
    
    /**
     * @dev Get complete carbon credit data
     * @param creditId Credit ID
     * @return Complete carbon credit struct
     */
    function getCarbonCredit(uint256 creditId)
        external
        view
        creditExists(creditId)
        returns (CarbonCredit memory)
    {
        return carbonCredits[creditId];
    }
    
    /**
     * @dev Get trading information for a credit
     * @param creditId Credit ID
     * @return Trading info struct
     */
    function getTradingInfo(uint256 creditId)
        external
        view
        creditExists(creditId)
        returns (TradingInfo memory)
    {
        return tradingInfo[creditId];
    }
    
    /**
     * @dev Get retirement history for a credit
     * @param creditId Credit ID
     * @return Array of retirement info
     */
    function getRetirementHistory(uint256 creditId)
        external
        view
        creditExists(creditId)
        returns (RetirementInfo[] memory)
    {
        return retirements[creditId];
    }
    
    /**
     * @dev Get credits issued by an address
     * @param issuer Issuer address
     * @return Array of credit IDs
     */
    function getCreditsByIssuer(address issuer)
        external
        view
        returns (uint256[] memory)
    {
        return issuerCredits[issuer];
    }
    
    /**
     * @dev Get quality distribution of all credits
     * @return Array of supply amounts for each quality level
     */
    function getQualityDistribution()
        external
        view
        returns (uint256[] memory)
    {
        uint256[] memory distribution = new uint256[](4);
        distribution[0] = qualitySupply[CreditQuality.STANDARD];
        distribution[1] = qualitySupply[CreditQuality.PREMIUM];
        distribution[2] = qualitySupply[CreditQuality.GOLD];
        distribution[3] = qualitySupply[CreditQuality.PLATINUM];
        return distribution;
    }
    
    /**
     * @dev Get market statistics
     * @return totalCredits, totalRetired, totalVolume, averagePrice
     */
    function getMarketStatistics()
        external
        view
        returns (uint256, uint256, uint256, uint256)
    {
        uint256 averagePrice = 0;
        uint256 activeCreditCount = 0;
        
        // Calculate average price from active credits
        for (uint256 i = 1; i <= _creditIdCounter.current(); i++) {
            if (!carbonCredits[i].isRetired && block.timestamp <= carbonCredits[i].expirationDate) {
                averagePrice += tradingInfo[i].currentPrice;
                activeCreditCount++;
            }
        }
        
        if (activeCreditCount > 0) {
            averagePrice = averagePrice / activeCreditCount;
        }
        
        return (totalCarbonCredits, totalRetiredCredits, totalTradingVolume, averagePrice);
    }
    
    /**
     * @dev Check if credit is valid (not expired, not retired)
     * @param creditId Credit ID
     * @return True if valid
     */
    function isValidCredit(uint256 creditId)
        external
        view
        creditExists(creditId)
        returns (bool)
    {
        CarbonCredit memory credit = carbonCredits[creditId];
        return !credit.isRetired && block.timestamp <= credit.expirationDate;
    }
    
    /**
     * @dev Get total supply of a specific credit
     * @param creditId Credit ID
     * @return Total supply (remaining after retirements)
     */
    function totalSupply(uint256 creditId) public view returns (uint256) {
        return carbonCredits[creditId].carbonAmount - _getTotalRetired(creditId);
    }
    
    /**
     * @dev Get total number of credits created
     * @return Total count
     */
    function getTotalCredits() external view returns (uint256) {
        return _creditIdCounter.current();
    }
    
    // ===== ADMIN FUNCTIONS =====
    
    /**
     * @dev Update delivery verification contract
     * @param newDeliveryVerification New contract address
     */
    function updateDeliveryVerification(address newDeliveryVerification) external onlyOwner {
        require(newDeliveryVerification != address(0), "Invalid address");
        deliveryVerification = IDeliveryVerification(newDeliveryVerification);
    }
    
    /**
     * @dev Set URI for token metadata
     * @param newURI New URI template
     */
    function setURI(string memory newURI) external onlyOwner {
        _setURI(newURI);
    }
    
    /**
     * @dev Withdraw contract balance (from trading fees)
     */
    function withdraw() external onlyOwner {
        uint256 balance = address(this).balance;
        require(balance > 0, "No balance to withdraw");
        
        payable(owner()).transfer(balance);
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
    
    function _getTotalRetired(uint256 creditId) internal view returns (uint256) {
        uint256 totalRetired = 0;
        RetirementInfo[] memory creditRetirements = retirements[creditId];
        
        for (uint256 i = 0; i < creditRetirements.length; i++) {
            totalRetired += creditRetirements[i].retiredAmount;
        }
        
        return totalRetired;
    }
    
    function _beforeTokenTransfer(
        address operator,
        address from,
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) internal virtual override whenNotPaused {
        super._beforeTokenTransfer(operator, from, to, ids, amounts, data);
        
        // Additional validation for transfers
        for (uint256 i = 0; i < ids.length; i++) {
            require(!carbonCredits[ids[i]].isRetired, "Cannot transfer retired credits");
            require(block.timestamp <= carbonCredits[ids[i]].expirationDate, "Cannot transfer expired credits");
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
}
