from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class BlockchainCertificate(Base):
    """Blockchain certificate model for delivery verification"""
    __tablename__ = 'blockchain_certificates'
    
    id = Column(Integer, primary_key=True, index=True)
    certificate_id = Column(String(255), unique=True, index=True, nullable=False)
    route_id = Column(String(255), nullable=False, index=True)
    vehicle_id = Column(String(255), nullable=False)
    
    # Certificate data
    carbon_saved_kg = Column(Float, nullable=False)
    cost_saved_usd = Column(Float, nullable=False)
    distance_km = Column(Float, nullable=False)
    optimization_score = Column(Integer, nullable=False)
    delivery_count = Column(Integer, nullable=True, default=1)
    time_saved_minutes = Column(Float, nullable=True, default=0)
    
    # Blockchain data
    verification_hash = Column(String(255), nullable=False)
    transaction_hash = Column(String(255), nullable=False, unique=True, index=True)
    block_number = Column(Integer, nullable=False, index=True)
    gas_used = Column(Integer, nullable=True)
    
    # Status and metadata
    verified = Column(Boolean, default=False, index=True)
    certificate_status = Column(String(50), nullable=False, default="pending")
    blockchain_network = Column(String(100), nullable=False, default="ganache_local")
    issuer = Column(String(255), nullable=True, default="QuantumEco Intelligence")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    delivery_records = relationship("DeliveryRecord", back_populates="certificate")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_certificate_status_date', 'certificate_status', 'created_at'),
        Index('idx_certificate_blockchain', 'blockchain_network', 'verified'),
        Index('idx_certificate_route_vehicle', 'route_id', 'vehicle_id'),
    )

class EnvironmentalTrustToken(Base):
    """Environmental Trust Token (ETT) model"""
    __tablename__ = 'environmental_trust_tokens'
    
    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(Integer, unique=True, index=True, nullable=False)
    certificate_id = Column(String(255), ForeignKey('blockchain_certificates.certificate_id'), nullable=False)
    route_id = Column(String(255), nullable=False, index=True)
    
    # ETT data
    trust_score = Column(Integer, nullable=False)  # 0-100
    carbon_impact_kg = Column(Float, nullable=False)
    sustainability_rating = Column(Integer, nullable=False)  # 0-100
    verification_level = Column(String(50), nullable=False, default="standard")
    
    # Blockchain data
    transaction_hash = Column(String(255), nullable=False, unique=True)
    block_number = Column(Integer, nullable=False)
    
    # Status
    token_status = Column(String(50), nullable=False, default="active")
    environmental_impact_description = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    certificate = relationship("BlockchainCertificate")
    
    # Indexes
    __table_args__ = (
        Index('idx_ett_token_status', 'token_status', 'created_at'),
        Index('idx_ett_trust_score', 'trust_score'),
    )

class CarbonCredit(Base):
    """Carbon credit token model"""
    __tablename__ = 'carbon_credits'
    
    id = Column(Integer, primary_key=True, index=True)
    credit_id = Column(Integer, unique=True, index=True, nullable=False)
    route_id = Column(String(255), nullable=False, index=True)
    certificate_id = Column(String(255), ForeignKey('blockchain_certificates.certificate_id'), nullable=True)
    
    # Credit data
    carbon_amount_kg = Column(Float, nullable=False)
    value_usd = Column(Float, nullable=False)
    price_per_kg = Column(Float, nullable=False)
    issuer = Column(String(255), nullable=False)
    credit_type = Column(String(100), nullable=False, default="verified_reduction")
    verification_standard = Column(String(100), nullable=False, default="VCS")
    vintage_year = Column(Integer, nullable=False)
    
    # Blockchain data
    transaction_hash = Column(String(255), nullable=False, unique=True)
    block_number = Column(Integer, nullable=False)
    
    # Status
    credit_status = Column(String(50), nullable=False, default="active")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    certificate = relationship("BlockchainCertificate")
    
    # Indexes
    __table_args__ = (
        Index('idx_carbon_credit_status', 'credit_status', 'created_at'),
        Index('idx_carbon_credit_value', 'value_usd'),
    )
