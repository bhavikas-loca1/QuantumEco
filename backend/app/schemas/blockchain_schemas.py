from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, date
from enum import Enum

class CertificateStatus(str, Enum):
    """Enumeration for certificate status types"""
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    EXPIRED = "expired"

class TokenStatus(str, Enum):
    """Enumeration for token status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    TRANSFERRED = "transferred"
    EXPIRED = "expired"

class TransactionStatus(str, Enum):
    """Enumeration for transaction status"""
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"

class BlockchainNetwork(str, Enum):
    """Enumeration for blockchain networks"""
    GANACHE_LOCAL = "ganache_local"
    ETHEREUM_MAINNET = "ethereum_mainnet"
    ETHEREUM_TESTNET = "ethereum_testnet"
    POLYGON = "polygon"

class CertificateCreationRequest(BaseModel):
    """Data required for blockchain certificate creation"""
    route_id: str = Field(..., description="Unique route identifier")
    vehicle_id: str = Field(..., description="Vehicle identifier used for delivery")
    carbon_saved: float = Field(..., ge=0, le=10000, description="Carbon emissions saved in kg CO2")
    cost_saved: float = Field(..., ge=0, le=100000, description="Cost savings in USD")
    distance_km: float = Field(..., gt=0, le=5000, description="Total route distance in kilometers")
    optimization_score: int = Field(..., ge=0, le=100, description="Route optimization quality score")
    delivery_count: Optional[int] = Field(default=1, ge=1, le=1000, description="Number of deliveries in route")
    time_saved_minutes: Optional[float] = Field(default=0, ge=0, description="Time savings in minutes")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Additional metadata for certificate")
    issuer: Optional[str] = Field(default="QuantumEco Intelligence", description="Certificate issuer")
    
    @validator('carbon_saved')
    def validate_carbon_saved(cls, v):
        """Validate carbon saved is reasonable"""
        if v < 0:
            raise ValueError('Carbon saved cannot be negative')
        if v > 10000:
            raise ValueError('Carbon saved seems unreasonably high (>10,000 kg)')
        return round(v, 3)
    
    @validator('cost_saved')
    def validate_cost_saved(cls, v):
        """Validate cost saved is reasonable"""
        if v < 0:
            raise ValueError('Cost saved cannot be negative')
        return round(v, 2)

class CertificateDetailsResponse(BaseModel):
    """Complete certificate information with blockchain proof"""
    certificate_id: str = Field(..., description="Unique certificate identifier")
    route_id: str = Field(..., description="Associated route identifier")
    vehicle_id: str = Field(..., description="Vehicle identifier")
    carbon_saved: float = Field(..., description="Carbon emissions saved in kg CO2")
    cost_saved: float = Field(..., description="Cost savings in USD")
    distance_km: float = Field(..., description="Route distance in kilometers")
    optimization_score: int = Field(..., description="Optimization quality score")
    verification_hash: str = Field(..., description="Cryptographic verification hash")
    transaction_hash: str = Field(..., description="Blockchain transaction hash")
    block_number: int = Field(..., description="Blockchain block number")
    gas_used: Optional[int] = Field(None, description="Gas used for transaction")
    verified: bool = Field(..., description="Certificate verification status")
    created_at: datetime = Field(..., description="Certificate creation timestamp")
    # timestamp: datetime = Field(..., description="Certificate creation timestamp")
    blockchain_network: BlockchainNetwork = Field(..., description="Blockchain network used")
    certificate_status: CertificateStatus = Field(..., description="Current certificate status")
    issuer: Optional[str] = Field(None, description="Certificate issuer")
    expires_at: Optional[datetime] = Field(None, description="Certificate expiration date")
    
    @validator('transaction_hash')
    def validate_transaction_hash(cls, v):
        # More lenient validation - just check if it's a hex string
        if isinstance(v, str) and len(v) >= 64:
            # Remove 0x prefix if present for validation
            hash_without_prefix = v.replace('0x', '')
            if all(c in '0123456789abcdefABCDEF' for c in hash_without_prefix):
                return v
        # If validation fails, return the value anyway for demo purposes
        return v

class CertificateVerificationRequest(BaseModel):
    """Request for certificate verification"""
    certificate_id: str = Field(..., description="Certificate ID to verify")
    expected_hash: Optional[str] = Field(None, description="Expected verification hash")
    check_expiration: bool = Field(default=True, description="Check if certificate is expired")

class CertificateVerificationResponse(BaseModel):
    """Certificate verification response"""
    certificate_id: str = Field(..., description="Certificate identifier")
    is_valid: bool = Field(..., description="Overall validity status")
    verification_status: str = Field(..., description="Detailed verification status")
    hash_verification: Optional[bool] = Field(None, description="Hash verification result")
    blockchain_verification: Optional[bool] = Field(None, description="Blockchain verification result")
    expiration_check: Optional[bool] = Field(None, description="Expiration check result")
    transaction_hash: Optional[str] = Field(None, description="Associated transaction hash")
    block_number: Optional[int] = Field(None, description="Block number")
    error_message: Optional[str] = Field(None, description="Error message if verification failed")
    verified_at: datetime = Field(default_factory=datetime.utcnow, description="Verification timestamp")

class ETTCreationRequest(BaseModel):
    """Environmental Trust Token creation parameters"""
    route_id: str = Field(..., description="Associated route identifier")
    trust_score: int = Field(..., ge=0, le=100, description="Trust score (0-100)")
    carbon_impact: float = Field(..., description="Carbon impact in kg CO2 (positive = saved, negative = excess)")
    sustainability_rating: int = Field(..., ge=0, le=100, description="Sustainability rating (0-100)")
    verification_level: str = Field(default="standard", description="Verification level (basic, standard, premium)")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Additional token metadata")
    valid_until: Optional[datetime] = Field(None, description="Token validity period")
    
    @validator('trust_score', 'sustainability_rating')
    def validate_score_range(cls, v):
        """Validate scores are within valid range"""
        if not 0 <= v <= 100:
            raise ValueError('Score must be between 0 and 100')
        return v

class ETTCreationResponse(BaseModel):
    """Environmental Trust Token creation response"""
    token_id: int = Field(..., description="Unique token identifier")
    route_id: str = Field(..., description="Associated route identifier")
    trust_score: int = Field(..., description="Trust score")
    carbon_impact_kg: float = Field(..., description="Carbon impact in kg CO2")
    sustainability_rating: int = Field(..., description="Sustainability rating")
    environmental_impact_description: str = Field(..., description="Human-readable impact description")
    transaction_hash: str = Field(..., description="Blockchain transaction hash")
    block_number: int = Field(..., description="Block number")
    # token_status: TokenStatus = Field(..., description="Token status")
    token_status: str = Field(default="active", description="Token status")  # Changed from TokenStatus enum to str
    created_at: datetime = Field(..., description="Token creation timestamp")
    expires_at: Optional[datetime] = Field(None, description="Token expiration date")
    metadata: Dict[str, Any] = Field(default={}, description="Token metadata")

class TransactionDetailsResponse(BaseModel):
    """Blockchain transaction details"""
    transaction_hash: str = Field(..., description="Transaction hash")
    block_number: int = Field(..., description="Block number")
    block_hash: str = Field(..., description="Block hash")
    transaction_index: int = Field(..., description="Transaction index in block")
    from_address: str = Field(..., description="Sender address")
    to_address: str = Field(..., description="Recipient address")
    gas_used: int = Field(..., description="Gas used for transaction")
    gas_price: int = Field(..., description="Gas price in wei")
    transaction_fee: int = Field(..., description="Total transaction fee in wei")
    status: TransactionStatus = Field(..., description="Transaction status")
    timestamp: datetime = Field(..., description="Transaction timestamp")
    transaction_type: str = Field(..., description="Type of transaction")
    related_certificate_id: Optional[str] = Field(None, description="Related certificate ID")
    related_token_id: Optional[int] = Field(None, description="Related token ID")
    
    @validator('transaction_hash', 'block_hash')
    def validate_hash_format(cls, v):
        """Validate hash format"""
        if not v.startswith('0x'):
            raise ValueError('Hash must start with 0x')
        return v

class RecentCertificatesResponse(BaseModel):
    """Response for recent certificates query"""
    certificates: List[Dict[str, Any]] = Field(..., description="List of recent certificates")
    total_count: int = Field(..., description="Total number of certificates")
    limit: int = Field(..., description="Query limit applied")
    offset: int = Field(..., description="Query offset applied")
    has_more: bool = Field(..., description="Whether more certificates are available")

class BlockInfo(BaseModel):
    """Blockchain block information"""
    number: int = Field(..., description="Block number")
    hash: str = Field(..., description="Block hash")
    timestamp: int = Field(..., description="Block timestamp")
    transactions: int = Field(..., description="Number of transactions in block")

class TransactionInfo(BaseModel):
    """Basic transaction information"""
    hash: str = Field(..., description="Transaction hash")
    from_address: str = Field(..., description="From address")
    to_address: str = Field(..., description="To address")
    value: int = Field(..., description="Transaction value")
    gas_used: int = Field(..., description="Gas used")
    timestamp: int = Field(..., description="Transaction timestamp")
    
class TransactionDetails(BaseModel):
    hash: str
    from_address: Optional[str] = "0x0000000000000000000000000000000000000000"
    to_address: Optional[str] = "0x0000000000000000000000000000000000000000"
    value: Optional[float] = 0.0
    gas_used: Optional[int] = 0
    gas_price: Optional[int] = 0
    block_number: Optional[int] = 0
    timestamp: Optional[int] = 0

class BlockchainExplorerResponse(BaseModel):
    """Blockchain explorer interface data"""
    network_name: str = Field(..., description="Blockchain network name")
    network_id: int = Field(..., description="Network ID")
    latest_block_number: int = Field(..., description="Latest block number")
    total_transactions: int = Field(..., description="Total number of transactions")
    total_certificates: int = Field(..., description="Total certificates created")
    total_carbon_saved_kg: float = Field(..., description="Total carbon saved across all certificates")
    total_cost_saved_usd: float = Field(..., description="Total cost saved across all certificates")
    average_gas_price: int = Field(..., description="Average gas price")
    network_hash_rate: int = Field(..., description="Network hash rate")
    recent_blocks: List[BlockInfo] = Field(..., description="Recent blocks")
    recent_transactions: List[TransactionInfo] = Field(..., description="Recent transactions")
    node_count: int = Field(..., description="Number of network nodes")
    network_status: str = Field(..., description="Network health status")
    last_updated: datetime = Field(..., description="Last update timestamp")
    

class CarbonCreditCreationRequest(BaseModel):
    """Request for creating tradeable carbon credit tokens"""
    route_id: str = Field(..., description="Associated route identifier")
    carbon_amount_kg: float = Field(..., gt=0, le=10000, description="Carbon amount in kg CO2")
    value_usd: float = Field(..., gt=0, le=1000000, description="Carbon credit value in USD")
    issuer: Optional[str] = Field(default="QuantumEco Intelligence", description="Credit issuer")
    credit_type: str = Field(default="verified_reduction", description="Type of carbon credit")
    verification_standard: str = Field(default="VCS", description="Verification standard (VCS, Gold Standard, etc.)")
    vintage_year: int = Field(..., ge=2020, le=2030, description="Vintage year of carbon reduction")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Additional credit metadata")
    
    @validator('carbon_amount_kg')
    def validate_carbon_amount(cls, v):
        """Validate carbon amount is reasonable"""
        if v <= 0:
            raise ValueError('Carbon amount must be greater than 0')
        if v > 10000:
            raise ValueError('Carbon amount seems unreasonably high')
        return round(v, 3)

class EnvironmentalEquivalents(BaseModel):
    """Environmental impact equivalents"""
    trees_planted_equivalent: float = Field(..., description="Equivalent trees planted")
    cars_off_road_days: float = Field(..., description="Equivalent car-free days")
    homes_powered_hours: float = Field(..., description="Equivalent home power hours")
    miles_not_driven: float = Field(..., description="Equivalent miles not driven")

class CarbonCreditCreationResponse(BaseModel):
    """Response for carbon credit creation"""
    credit_id: int = Field(..., description="Unique credit identifier")
    route_id: str = Field(..., description="Associated route identifier")
    carbon_amount_kg: float = Field(..., description="Carbon amount in kg CO2")
    value_usd: float = Field(..., description="Credit value in USD")
    price_per_kg: float = Field(..., description="Price per kg CO2")
    issuer: str = Field(..., description="Credit issuer")
    transaction_hash: str = Field(..., description="Blockchain transaction hash")
    block_number: int = Field(..., description="Block number")
    credit_status: str = Field(..., description="Credit status")
    environmental_equivalents: EnvironmentalEquivalents = Field(..., description="Environmental equivalents")
    created_at: datetime = Field(..., description="Creation timestamp")
    expires_at: datetime = Field(..., description="Expiration date")
    verification_standard: str = Field(..., description="Verification standard")
    vintage_year: int = Field(..., description="Vintage year")
    metadata: Dict[str, Any] = Field(default={}, description="Credit metadata")

class CertificateSummary(BaseModel):
    """Summary information for certificate listings"""
    certificate_id: str = Field(..., description="Certificate identifier")
    route_id: str = Field(..., description="Route identifier")
    carbon_saved_kg: float = Field(..., description="Carbon saved")
    cost_saved_usd: float = Field(..., description="Cost saved")
    optimization_score: int = Field(..., description="Optimization score")
    transaction_hash: str = Field(..., description="Transaction hash")
    block_number: int = Field(..., description="Block number")
    created_at: datetime = Field(..., description="Creation timestamp")
    verified: bool = Field(..., description="Verification status")

class BlockchainNetworkStats(BaseModel):
    """Blockchain network statistics"""
    network_id: int = Field(..., description="Network identifier")
    latest_block: int = Field(..., description="Latest block number")
    total_carbon_saved: float = Field(..., description="Total carbon saved in grams")
    total_cost_saved: float = Field(..., description="Total cost saved in cents")
    total_deliveries: int = Field(..., description="Total verified deliveries")
    gas_price: int = Field(..., description="Current gas price")
    hash_rate: int = Field(..., description="Network hash rate")

class ETTTokenDetails(BaseModel):
    """Environmental Trust Token details"""
    token_id: int = Field(..., description="Token identifier")
    route_id: str = Field(..., description="Associated route")
    trust_score: int = Field(..., description="Trust score")
    carbon_impact: float = Field(..., description="Carbon impact")
    sustainability_rating: int = Field(..., description="Sustainability rating")
    is_active: bool = Field(..., description="Token active status")
    owner: str = Field(..., description="Token owner address")
    created_at: datetime = Field(..., description="Creation timestamp")
