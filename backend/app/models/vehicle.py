from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, Index
from sqlalchemy.sql import func
from app.database import Base

class VehicleProfile(Base):
    """Vehicle type configurations and emission factors"""
    __tablename__ = 'vehicle_profiles'
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_type = Column(String(100), unique=True, nullable=False, index=True)
    display_name = Column(String(255), nullable=False)
    
    # Physical specifications
    capacity_kg = Column(Float, nullable=False)
    max_range_km = Column(Float, nullable=True, default=500.0)
    fuel_type = Column(String(50), nullable=True)
    
    # Cost factors
    cost_per_km = Column(Float, nullable=False)
    maintenance_factor = Column(Float, nullable=True, default=1.0)
    
    # Emission factors
    emission_factor = Column(Float, nullable=False)  # kg CO2 per km
    lifecycle_emissions_kg_per_km = Column(Float, nullable=True)
    
    # Efficiency ratings
    efficiency_rating = Column(String(10), nullable=True)  # A+, A, B, C, D
    weather_sensitivity = Column(Float, nullable=True, default=1.0)
    load_sensitivity = Column(Float, nullable=True, default=1.0)
    
    # Descriptive information
    description = Column(Text, nullable=True)
    environmental_impact = Column(String(50), nullable=True)
    recommended_use = Column(Text, nullable=True)
    
    # Metadata
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_vehicle_type_active', 'vehicle_type', 'is_active'),
        Index('idx_vehicle_emission_factor', 'emission_factor'),
        Index('idx_vehicle_efficiency', 'efficiency_rating', 'environmental_impact'),
    )

class VehicleInstance(Base):
    """Individual vehicle instances"""
    __tablename__ = 'vehicle_instances'
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(String(255), unique=True, index=True, nullable=False)
    vehicle_type = Column(String(100), nullable=False, index=True)
    
    # Vehicle details
    license_plate = Column(String(50), nullable=True)
    driver_id = Column(String(255), nullable=True)
    current_location_lat = Column(Float, nullable=True)
    current_location_lng = Column(Float, nullable=True)
    
    # Status
    availability_status = Column(String(50), nullable=False, default="available")
    fuel_level = Column(Float, nullable=True, default=1.0)  # 0-1
    maintenance_due = Column(DateTime(timezone=True), nullable=True)
    
    # Schedule
    availability_start = Column(String(10), nullable=True, default="08:00")  # HH:MM
    availability_end = Column(String(10), nullable=True, default="18:00")
    
    # Performance tracking
    total_distance = Column(Float, nullable=False, default=0)
    total_deliveries = Column(Integer, nullable=False, default=0)
    total_emissions_kg = Column(Float, nullable=False, default=0)
    efficiency_score = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_maintenance = Column(DateTime(timezone=True), nullable=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_vehicle_status', 'availability_status', 'vehicle_type'),
        Index('idx_vehicle_location', 'current_location_lat', 'current_location_lng'),
        Index('idx_vehicle_performance', 'efficiency_score', 'total_deliveries'),
    )

class VehicleAssignment(Base):
    """Vehicle assignments to routes"""
    __tablename__ = 'vehicle_assignments'
    
    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(String(255), unique=True, index=True, nullable=False)
    vehicle_id = Column(String(255), nullable=False, index=True)
    route_optimization_id = Column(Integer, nullable=False, index=True)
    
    # Assignment details
    assigned_locations = Column(Integer, nullable=False)
    total_load_kg = Column(Float, nullable=False)
    utilization_percent = Column(Float, nullable=False)
    
    # Route metrics
    route_distance_km = Column(Float, nullable=False)
    route_time_minutes = Column(Float, nullable=False)
    route_cost_usd = Column(Float, nullable=False)
    route_emissions_kg = Column(Float, nullable=False)
    
    # Status
    assignment_status = Column(String(50), nullable=False, default="assigned")
    
    # Timestamps
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_assignment_vehicle_status', 'vehicle_id', 'assignment_status'),
        Index('idx_assignment_route', 'route_optimization_id'),
    )
