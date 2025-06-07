from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, JSON, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class RouteOptimization(Base):
    """Route optimization request and results model"""
    __tablename__ = 'route_optimizations'
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String(255), unique=True, index=True, nullable=False)
    optimization_id = Column(String(255), unique=True, index=True, nullable=False)
    
    # Request details
    status = Column(String(50), nullable=False, default="pending", index=True)
    optimization_goals = Column(JSON, nullable=True)  # Cost, carbon, time weights
    constraints = Column(JSON, nullable=True)  # Max distance, time, etc.
    
    # Input data
    locations_count = Column(Integer, nullable=False)
    vehicles_count = Column(Integer, nullable=False)
    input_data = Column(JSON, nullable=False)  # Complete request data
    
    # Results
    optimization_data = Column(JSON, nullable=True)  # Complete optimization result
    processing_time_seconds = Column(Float, nullable=True)
    quantum_improvement_score = Column(Float, nullable=True)
    
    # Performance metrics
    total_distance_km = Column(Float, nullable=True)
    total_time_minutes = Column(Float, nullable=True)
    total_cost_usd = Column(Float, nullable=True)
    total_carbon_kg = Column(Float, nullable=True)
    
    # Savings analysis
    cost_saved_usd = Column(Float, nullable=True, default=0)
    carbon_saved_kg = Column(Float, nullable=True, default=0)
    time_saved_minutes = Column(Float, nullable=True, default=0)
    distance_saved_km = Column(Float, nullable=True, default=0)
    
    # Algorithm details
    algorithm_used = Column(String(100), nullable=True)
    iterations_count = Column(Integer, nullable=True)
    convergence_score = Column(Float, nullable=True)
    
    # Error handling
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    delivery_records = relationship("DeliveryRecord", foreign_keys="DeliveryRecord.optimization_id", 
                                  primaryjoin="RouteOptimization.optimization_id == DeliveryRecord.optimization_id")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_optimization_status_date', 'status', 'created_at'),
        Index('idx_optimization_algorithm', 'algorithm_used', 'quantum_improvement_score'),
        Index('idx_optimization_performance', 'total_cost_usd', 'total_carbon_kg'),
    )

class RouteSegment(Base):
    """Individual route segment model"""
    __tablename__ = 'route_segments'
    
    id = Column(Integer, primary_key=True, index=True)
    route_optimization_id = Column(Integer, ForeignKey('route_optimizations.id'), nullable=False)
    vehicle_id = Column(String(255), nullable=False)
    
    # Segment details
    from_location_id = Column(String(255), nullable=False)
    to_location_id = Column(String(255), nullable=False)
    segment_sequence = Column(Integer, nullable=False)
    
    # Metrics
    distance_km = Column(Float, nullable=False)
    travel_time_minutes = Column(Float, nullable=False)
    carbon_emissions_kg = Column(Float, nullable=False)
    fuel_cost_usd = Column(Float, nullable=False)
    
    # Conditions
    traffic_factor = Column(Float, nullable=True, default=1.0)
    weather_factor = Column(Float, nullable=True, default=1.0)
    estimated_arrival = Column(String(10), nullable=True)  # HH:MM format
    
    # Relationships
    route_optimization = relationship("RouteOptimization")
    
    # Indexes
    __table_args__ = (
        Index('idx_segment_route_sequence', 'route_optimization_id', 'segment_sequence'),
        Index('idx_segment_vehicle', 'vehicle_id', 'segment_sequence'),
    )

class BatchOptimization(Base):
    """Batch optimization for multiple scenarios"""
    __tablename__ = 'batch_optimizations'
    
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(String(255), unique=True, index=True, nullable=False)
    
    # Batch details
    status = Column(String(50), nullable=False, default="pending")
    scenarios_count = Column(Integer, nullable=False)
    successful_optimizations = Column(Integer, nullable=False, default=0)
    
    # Processing
    parallel_processing = Column(Boolean, nullable=False, default=True)
    total_processing_time_seconds = Column(Float, nullable=True)
    
    # Results
    best_scenario_id = Column(String(255), nullable=True)
    batch_results = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_batch_status_date', 'status', 'created_at'),
    )
