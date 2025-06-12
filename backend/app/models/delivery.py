from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, JSON, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class DeliveryRecord(Base):
    """Delivery record model with optimization metrics"""
    __tablename__ = 'delivery_records'
    
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(String(255), unique=True, index=True, nullable=False)
    vehicle_id = Column(String(255), nullable=False, index=True)
    optimization_id = Column(String(255), nullable=True, index=True)
    
    # Performance metrics
    total_distance = Column(Float, nullable=False)
    total_time = Column(Float, nullable=False)
    total_cost_usd = Column(Float, nullable=False)
    total_emissions_kg = Column(Float, nullable=False)
    optimization_score = Column(Float, nullable=True)
    
    # Route details
    optimization_method = Column(String(100), nullable=False, default="quantum_inspired")
    vehicle_utilization_percent = Column(Float, nullable=True)
    load_factor = Column(Float, nullable=True, default=1.0)
    delivery_count = Column(Integer, nullable=False, default=1)
    
    # Savings analysis
    cost_saved_usd = Column(Float, nullable=True, default=0)
    carbon_saved_kg = Column(Float, nullable=True, default=0)
    time_saved_minutes = Column(Float, nullable=True, default=0)
    distance_saved_km = Column(Float, nullable=True, default=0)
    
    # Status and metadata
    status = Column(String(50), nullable=False, default="completed")
    route_data = Column(JSON, nullable=True)  # Store complete route information
    weather_conditions = Column(JSON, nullable=True)
    traffic_conditions = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    certificate_id = Column(String(255), ForeignKey('blockchain_certificates.certificate_id'), nullable=True)
    certificate = relationship('BlockchainCertificate', back_populates='delivery_records')
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_delivery_vehicle_date', 'vehicle_id', 'created_at'),
        Index('idx_delivery_optimization', 'optimization_method', 'optimization_score'),
        Index('idx_delivery_status', 'status', 'created_at'),
    )

class DeliveryLocation(Base):
    """Individual delivery location model"""
    __tablename__ = 'delivery_locations'
    
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(String(255), index=True, nullable=False)
    delivery_record_id = Column(Integer, ForeignKey('delivery_records.id'), nullable=False)
    
    # Location data
    name = Column(String(255), nullable=True)
    address = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Delivery details
    demand_kg = Column(Float, nullable=False, default=0)
    priority = Column(Integer, nullable=False, default=1)
    time_window_start = Column(String(10), nullable=True)  # HH:MM format
    time_window_end = Column(String(10), nullable=True)
    delivery_type = Column(String(50), nullable=False, default="standard")
    
    # Status
    delivery_status = Column(String(50), nullable=False, default="pending")
    estimated_arrival = Column(DateTime(timezone=True), nullable=True)
    actual_arrival = Column(DateTime(timezone=True), nullable=True)
    
    # Sequence in route
    route_sequence = Column(Integer, nullable=True)
    
    # Relationships
    delivery_record = relationship("DeliveryRecord")
    
    # Indexes
    __table_args__ = (
        Index('idx_location_coordinates', 'latitude', 'longitude'),
        Index('idx_location_delivery', 'delivery_record_id', 'route_sequence'),
    )

class DeliveryTracking(Base):
    """Real-time delivery tracking model"""
    __tablename__ = 'delivery_tracking'
    
    id = Column(Integer, primary_key=True, index=True)
    delivery_record_id = Column(Integer, ForeignKey('delivery_records.id'), nullable=False)
    tracking_id = Column(String(255), unique=True, index=True, nullable=False)
    
    # Current status
    current_location_lat = Column(Float, nullable=True)
    current_location_lng = Column(Float, nullable=True)
    distance_covered_km = Column(Float, nullable=False, default=0)
    progress_percentage = Column(Float, nullable=False, default=0)
    
    # Real-time metrics
    current_emissions_kg = Column(Float, nullable=False, default=0)
    estimated_total_emissions_kg = Column(Float, nullable=True)
    current_speed_kmh = Column(Float, nullable=True)
    
    # Status
    tracking_status = Column(String(50), nullable=False, default="active")
    last_update = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    delivery_record = relationship("DeliveryRecord")
    
    # Indexes
    __table_args__ = (
        Index('idx_tracking_status', 'tracking_status', 'last_update'),
        Index('idx_tracking_location', 'current_location_lat', 'current_location_lng'),
    )
