# from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, JSON, Text, Index, text
# from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session
# from sqlalchemy.sql import func
# from sqlalchemy.pool import StaticPool
# from typing import Generator
# import os
# from pathlib import Path

# from app.config import settings

# # Create declarative base
# Base = declarative_base()

# # ===== Database Models =====

# class DeliveryRecord(Base):
#     """Optimized delivery information with performance metrics"""
#     __tablename__ = 'delivery_records'
    
#     id = Column(Integer, primary_key=True, index=True)
#     route_id = Column(String(255), unique=True, index=True, nullable=False)
#     vehicle_id = Column(String(255), nullable=False, index=True)
#     optimization_id = Column(String(255), nullable=True, index=True)
    
#     # Performance metrics
#     total_distance = Column(Float, nullable=False)
#     total_time = Column(Float, nullable=False)
#     total_cost_usd = Column(Float, nullable=False)
#     total_emissions_kg = Column(Float, nullable=False)
#     optimization_score = Column(Float, nullable=True)
    
#     # Route details
#     optimization_method = Column(String(100), nullable=False, default="quantum_inspired")
#     vehicle_utilization_percent = Column(Float, nullable=True)
#     load_factor = Column(Float, nullable=True, default=1.0)
    
#     # Metadata
#     route_data = Column(JSON, nullable=True)  # Store complete route information
#     created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
#     # Relationships
#     blockchain_certificate_id = Column(String(255), ForeignKey('blockchain_certificates.certificate_id'), nullable=True)
#     blockchain_certificate = relationship('BlockchainCertificate', back_populates='delivery_record')
    
#     # Indexes for performance
#     __table_args__ = (
#         Index('idx_delivery_vehicle_date', 'vehicle_id', 'created_at'),
#         Index('idx_delivery_optimization', 'optimization_method', 'optimization_score'),
#     )

# class RouteOptimization(Base):
#     """Route optimization requests and results"""
#     __tablename__ = 'route_optimizations'
    
#     id = Column(Integer, primary_key=True, index=True)
#     request_id = Column(String(255), unique=True, index=True, nullable=False)
#     optimization_id = Column(String(255), unique=True, index=True, nullable=False)
    
#     # Request details
#     status = Column(String(50), nullable=False, default="pending", index=True)
#     optimization_goals = Column(JSON, nullable=True)  # Cost, carbon, time weights
#     constraints = Column(JSON, nullable=True)  # Max distance, time, etc.
    
#     # Input data
#     locations_count = Column(Integer, nullable=False)
#     vehicles_count = Column(Integer, nullable=False)
#     input_data = Column(JSON, nullable=False)  # Complete request data
    
#     # Results
#     optimization_data = Column(JSON, nullable=True)  # Complete optimization result
#     processing_time_seconds = Column(Float, nullable=True)
#     quantum_improvement_score = Column(Float, nullable=True)
    
#     # Metadata
#     algorithm_used = Column(String(100), nullable=True)
#     error_message = Column(Text, nullable=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())
#     completed_at = Column(DateTime(timezone=True), nullable=True)
    
#     # Indexes for performance
#     __table_args__ = (
#         Index('idx_optimization_status_date', 'status', 'created_at'),
#         Index('idx_optimization_algorithm', 'algorithm_used', 'quantum_improvement_score'),
#     )

# class CarbonCalculation(Base):
#     """Carbon emission calculations with factors"""
#     __tablename__ = 'carbon_calculations'
    
#     id = Column(Integer, primary_key=True, index=True)
#     calculation_id = Column(String(255), unique=True, index=True, nullable=False)
#     route_id = Column(String(255), nullable=False, index=True)
    
#     # Basic calculation data
#     total_emissions_kg = Column(Float, nullable=False)
#     emissions_per_km = Column(Float, nullable=False)
#     distance_km = Column(Float, nullable=False)
#     vehicle_type = Column(String(100), nullable=False, index=True)
    
#     # Impact factors
#     weather_impact_factor = Column(Float, nullable=True, default=1.0)
#     load_impact_factor = Column(Float, nullable=True, default=1.0)
#     traffic_impact_factor = Column(Float, nullable=True, default=1.0)
#     efficiency_factor = Column(Float, nullable=True, default=1.0)
    
#     # Economic data
#     carbon_cost_usd = Column(Float, nullable=True)
#     carbon_price_per_ton = Column(Float, nullable=True, default=50.0)
    
#     # Environmental impact
#     environmental_impact = Column(String(50), nullable=True)
#     carbon_saved_kg = Column(Float, nullable=True, default=0.0)
    
#     # Calculation metadata
#     methodology = Column(String(100), nullable=True, default="IPCC 2021 Guidelines")
#     confidence_level = Column(Float, nullable=True, default=0.95)
#     weather_conditions = Column(JSON, nullable=True)
#     calculation_timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
#     # Indexes for performance
#     __table_args__ = (
#         Index('idx_carbon_vehicle_date', 'vehicle_type', 'calculation_timestamp'),
#         Index('idx_carbon_route_emissions', 'route_id', 'total_emissions_kg'),
#     )

# class BlockchainCertificate(Base):
#     """Certificate references and verification status"""
#     __tablename__ = 'blockchain_certificates'
    
#     certificate_id = Column(String(255), primary_key=True, index=True)
#     route_id = Column(String(255), nullable=False, index=True)
#     vehicle_id = Column(String(255), nullable=False)
    
#     # Certificate data
#     carbon_saved_kg = Column(Float, nullable=False)
#     cost_saved_usd = Column(Float, nullable=False)
#     distance_km = Column(Float, nullable=False)
#     optimization_score = Column(Integer, nullable=False)
    
#     # Blockchain data
#     verification_hash = Column(String(255), nullable=False)
#     transaction_hash = Column(String(255), nullable=False, unique=True, index=True)
#     block_number = Column(Integer, nullable=False, index=True)
#     gas_used = Column(Integer, nullable=True)
    
#     # Status and metadata
#     verified = Column(Boolean, default=False, index=True)
#     certificate_status = Column(String(50), nullable=False, default="pending")
#     blockchain_network = Column(String(100), nullable=False, default="ganache_local")
#     issuer = Column(String(255), nullable=True)
    
#     # Timestamps
#     created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
#     verified_at = Column(DateTime(timezone=True), nullable=True)
#     expires_at = Column(DateTime(timezone=True), nullable=True)
    
#     # Relationships
#     delivery_record = relationship('DeliveryRecord', back_populates='blockchain_certificate')
    
#     # Indexes for performance
#     __table_args__ = (
#         Index('idx_certificate_status_date', 'certificate_status', 'created_at'),
#         Index('idx_certificate_blockchain', 'blockchain_network', 'verified'),
#     )

# class VehicleProfile(Base):
#     """Vehicle type configurations and emission factors"""
#     __tablename__ = 'vehicle_profiles'
    
#     id = Column(Integer, primary_key=True, index=True)
#     vehicle_type = Column(String(100), unique=True, nullable=False, index=True)
#     display_name = Column(String(255), nullable=False)
    
#     # Physical specifications
#     capacity_kg = Column(Float, nullable=False)
#     max_range_km = Column(Float, nullable=True, default=500.0)
#     fuel_type = Column(String(50), nullable=True)
    
#     # Cost factors
#     cost_per_km = Column(Float, nullable=False)
#     maintenance_factor = Column(Float, nullable=True, default=1.0)
    
#     # Emission factors
#     emission_factor = Column(Float, nullable=False)  # kg CO2 per km
#     lifecycle_emissions_kg_per_km = Column(Float, nullable=True)
    
#     # Efficiency ratings
#     efficiency_rating = Column(String(10), nullable=True)  # A+, A, B, C, D
#     weather_sensitivity = Column(Float, nullable=True, default=1.0)
#     load_sensitivity = Column(Float, nullable=True, default=1.0)
    
#     # Descriptive information
#     description = Column(Text, nullable=True)
#     environmental_impact = Column(String(50), nullable=True)
#     recommended_use = Column(Text, nullable=True)
    
#     # Metadata
#     is_active = Column(Boolean, default=True, index=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
#     # Indexes for performance
#     __table_args__ = (
#         Index('idx_vehicle_type_active', 'vehicle_type', 'is_active'),
#         Index('idx_vehicle_emission_factor', 'emission_factor'),
#     )

# # ===== Database Engine and Session Setup =====

# def create_database_engine():
#     """Create database engine with appropriate configuration"""
#     database_url = settings.database_url_to_use
    
#     if database_url.startswith("sqlite"):
#         # SQLite configuration for development
#         engine = create_engine(
#             database_url,
#             connect_args={
#                 "check_same_thread": False,
#                 "timeout": 20
#             },
#             poolclass=StaticPool,
#             pool_pre_ping=True,
#             echo=settings.DATABASE_ECHO
#         )
#     else:
#         # PostgreSQL configuration for production
#         engine = create_engine(
#             database_url,
#             pool_size=10,
#             max_overflow=20,
#             pool_pre_ping=True,
#             pool_recycle=3600,
#             echo=settings.DATABASE_ECHO
#         )
    
#     return engine

# # Create engine instance
# engine = create_database_engine()

# # Create session factory
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # ===== Database Dependencies =====

# def get_db() -> Generator[Session, None, None]:
#     """
#     Dependency function to get database session
#     Used with FastAPI Depends() for automatic session management
#     """
#     db = SessionLocal()
#     try:
#         yield db
#     except Exception as e:
#         db.rollback()
#         raise e
#     finally:
#         db.close()

# def get_db_session() -> Session:
#     """
#     Get database session for direct use
#     Remember to close the session manually
#     """
#     return SessionLocal()

# # ===== Database Initialization =====

# def create_tables():
#     """Create all database tables"""
#     try:
#         Base.metadata.create_all(bind=engine)
#         print("✅ Database tables created successfully")
#         return True
#     except Exception as e:
#         print(f"❌ Error creating database tables: {str(e)}")
#         return False

# def drop_tables():
#     """Drop all database tables (use with caution)"""
#     try:
#         Base.metadata.drop_all(bind=engine)
#         print("✅ Database tables dropped successfully")
#         return True
#     except Exception as e:
#         print(f"❌ Error dropping database tables: {str(e)}")
#         return False

# def init_database():
#     """Initialize database with tables and seed data"""
#     try:
#         # Ensure database directory exists
#         if settings.DATABASE_URL.startswith("sqlite"):
#             db_path = Path(settings.DATABASE_URL.replace("sqlite:///", ""))
#             db_path.parent.mkdir(parents=True, exist_ok=True)
        
#         # Create tables
#         create_tables()
        
#         # Seed vehicle profiles
#         seed_vehicle_profiles()
        
#         print("✅ Database initialized successfully")
#         return True
        
#     except Exception as e:
#         print(f"❌ Error initializing database: {str(e)}")
#         return False

# def seed_vehicle_profiles():
#     """Seed database with default vehicle profiles"""
#     try:
#         db = get_db_session()
        
#         # Check if vehicle profiles already exist
#         existing_count = db.query(VehicleProfile).count()
#         if existing_count > 0:
#             print(f"Vehicle profiles already exist ({existing_count} profiles)")
#             db.close()
#             return
        
#         # Default vehicle profiles
#         vehicle_profiles = [
#             {
#                 "vehicle_type": "diesel_truck",
#                 "display_name": "Diesel Truck",
#                 "capacity_kg": 1000.0,
#                 "max_range_km": 800.0,
#                 "fuel_type": "diesel",
#                 "cost_per_km": 0.85,
#                 "emission_factor": 0.27,
#                 "efficiency_rating": "C",
#                 "weather_sensitivity": 1.15,
#                 "load_sensitivity": 1.20,
#                 "description": "Heavy-duty diesel truck for large deliveries",
#                 "environmental_impact": "high",
#                 "recommended_use": "Long distance, high capacity deliveries"
#             },
#             {
#                 "vehicle_type": "electric_van",
#                 "display_name": "Electric Van",
#                 "capacity_kg": 500.0,
#                 "max_range_km": 300.0,
#                 "fuel_type": "electric",
#                 "cost_per_km": 0.65,
#                 "emission_factor": 0.05,
#                 "efficiency_rating": "A+",
#                 "weather_sensitivity": 1.05,
#                 "load_sensitivity": 1.08,
#                 "description": "Zero-emission electric delivery van",
#                 "environmental_impact": "very_low",
#                 "recommended_use": "Urban deliveries, short to medium distance"
#             },
#             {
#                 "vehicle_type": "hybrid_delivery",
#                 "display_name": "Hybrid Delivery Vehicle",
#                 "capacity_kg": 750.0,
#                 "max_range_km": 600.0,
#                 "fuel_type": "hybrid",
#                 "cost_per_km": 0.75,
#                 "emission_factor": 0.12,
#                 "efficiency_rating": "B+",
#                 "weather_sensitivity": 1.08,
#                 "load_sensitivity": 1.12,
#                 "description": "Fuel-efficient hybrid delivery vehicle",
#                 "environmental_impact": "medium",
#                 "recommended_use": "Mixed urban and suburban deliveries"
#             },
#             {
#                 "vehicle_type": "gas_truck",
#                 "display_name": "Gas Truck",
#                 "capacity_kg": 800.0,
#                 "max_range_km": 700.0,
#                 "fuel_type": "gasoline",
#                 "cost_per_km": 0.80,
#                 "emission_factor": 0.23,
#                 "efficiency_rating": "C+",
#                 "weather_sensitivity": 1.12,
#                 "load_sensitivity": 1.18,
#                 "description": "Standard gasoline delivery truck",
#                 "environmental_impact": "medium_high",
#                 "recommended_use": "General purpose deliveries"
#             },
#             {
#                 "vehicle_type": "cargo_bike",
#                 "display_name": "Electric Cargo Bike",
#                 "capacity_kg": 50.0,
#                 "max_range_km": 80.0,
#                 "fuel_type": "electric",
#                 "cost_per_km": 0.25,
#                 "emission_factor": 0.01,
#                 "efficiency_rating": "A++",
#                 "weather_sensitivity": 1.02,
#                 "load_sensitivity": 1.05,
#                 "description": "Ultra-low emission cargo bike for small deliveries",
#                 "environmental_impact": "minimal",
#                 "recommended_use": "Last-mile urban deliveries, small packages"
#             }
#         ]
        
#         # Insert vehicle profiles
#         for profile_data in vehicle_profiles:
#             profile = VehicleProfile(**profile_data)
#             db.add(profile)
        
#         db.commit()
#         print(f"✅ Seeded {len(vehicle_profiles)} vehicle profiles")
        
#     except Exception as e:
#         print(f"❌ Error seeding vehicle profiles: {str(e)}")
#         if db:
#             db.rollback()
#     finally:
#         if db:
#             db.close()

# # ===== Database Health Check =====

# def check_database_health() -> dict:
#     """Check database connectivity and health"""
#     print("\n=== Starting Database Health Check ===")
#     try:
#         print("🔄 Establishing database connection...")
#         db = get_db_session()
        
#         # Test basic connectivity
#         print("🔄 Testing database connectivity...")
#         db.execute(text('SELECT 1'))
#         print("✅ Database connection successful")
        
#         # Get table counts
#         print("\n🔄 Collecting table statistics...")
#         table_counts = {}
        
#         print("   📊 Counting delivery_records...")
#         table_counts["delivery_records"] = db.query(DeliveryRecord).count()
        
#         print("   📊 Counting route_optimizations...")
#         table_counts["route_optimizations"] = db.query(RouteOptimization).count()
        
#         print("   📊 Counting carbon_calculations...")
#         table_counts["carbon_calculations"] = db.query(CarbonCalculation).count()
        
#         print("   📊 Counting blockchain_certificates...")
#         table_counts["blockchain_certificates"] = db.query(BlockchainCertificate).count()
        
#         print("   📊 Counting vehicle_profiles...")
#         table_counts["vehicle_profiles"] = db.query(VehicleProfile).count()
        
#         total_records = sum(table_counts.values())
#         print(f"\n✅ Health check complete - Found {total_records} total records")
        
#         db.close()
#         print("✅ Database connection closed properly")
        
#         database_url = settings.database_url_to_use.split("@")[-1] if "@" in settings.database_url_to_use else settings.database_url_to_use
#         print(f"📍 Database URL: {database_url}")
        
#         result = {
#             "status": "healthy",
#             "database_url": database_url,
#             "table_counts": table_counts,
#             "total_records": total_records
#         }
#         print("\n=== Health Check Results ===")
#         print(f"Status: {result['status']}")
#         print("Table counts:")
#         for table, count in table_counts.items():
#             print(f"   {table}: {count}")
        
#         return result
        
#     except Exception as e:
#         print(f"\n❌ Database health check failed!")
#         print(f"❌ Error: {str(e)}")
#         database_url = settings.database_url_to_use.split("@")[-1] if "@" in settings.database_url_to_use else settings.database_url_to_use
#         print(f"📍 Database URL: {database_url}")
        
#         return {
#             "status": "unhealthy",
#             "error": str(e),
#             "database_url": database_url
#         }

# # ===== Utility Functions =====

# def get_vehicle_profile_by_type(vehicle_type: str) -> VehicleProfile:
#     """Get vehicle profile by type"""
#     db = get_db_session()
#     try:
#         profile = db.query(VehicleProfile).filter(
#             VehicleProfile.vehicle_type == vehicle_type,
#             VehicleProfile.is_active == True
#         ).first()
#         return profile
#     finally:
#         db.close()

# def get_all_vehicle_profiles() -> list:
#     """Get all active vehicle profiles"""
#     db = get_db_session()
#     try:
#         profiles = db.query(VehicleProfile).filter(
#             VehicleProfile.is_active == True
#         ).all()
#         return profiles
#     finally:
#         db.close()
        
# # Add this function to the existing database.py file

# from sqlalchemy.orm import Session
# from typing import Generator

# def get_db() -> Generator[Session, None, None]:
#     """
#     Dependency function to get database session
#     Used with FastAPI Depends() for automatic session management
#     """
#     db = SessionLocal()
#     try:
#         yield db
#     except Exception as e:
#         db.rollback()
#         raise e
#     finally:
#         db.close()


# def cleanup_old_records(days: int = 30):
#     """Clean up old records older than specified days"""
#     try:
#         db = get_db_session()
#         cutoff_date = func.now() - func.interval(f'{days} days')
        
#         # Clean up old route optimizations
#         old_optimizations = db.query(RouteOptimization).filter(
#             RouteOptimization.created_at < cutoff_date,
#             RouteOptimization.status.in_(["completed", "failed"])
#         ).count()
        
#         if old_optimizations > 0:
#             db.query(RouteOptimization).filter(
#                 RouteOptimization.created_at < cutoff_date,
#                 RouteOptimization.status.in_(["completed", "failed"])
#             ).delete()
            
#         db.commit()
#         print(f"✅ Cleaned up {old_optimizations} old optimization records")
        
#     except Exception as e:
#         print(f"❌ Error cleaning up old records: {str(e)}")
#         if db:
#             db.rollback()
#     finally:
#         if db:
#             db.close()

# # Initialize database on import
# if __name__ == "__main__":
#     init_database()
# else:
#     # Auto-initialize for production
#     try:
#         create_tables()
#     except Exception as e:
#         print(f"Warning: Could not auto-initialize database: {str(e)}")

# # Export commonly used items
# __all__ = [
#     "Base",
#     "engine",
#     "SessionLocal",
#     "get_db",
#     "get_db_session",
#     "DeliveryRecord",
#     "RouteOptimization", 
#     "CarbonCalculation",
#     "BlockchainCertificate",
#     "VehicleProfile",
#     "init_database",
#     "create_tables",
#     "check_database_health",
#     "get_vehicle_profile_by_type",
#     "get_all_vehicle_profiles"
# ]

# """# After adding models, create and run migration:
# alembic revision --autogenerate -m "Add certificate, delivery, route, vehicle models"
# alembic upgrade head
# """
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, JSON, Text, Index, text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session
from sqlalchemy.sql import func
from sqlalchemy.pool import StaticPool
from typing import Generator
import os
from pathlib import Path

from app.config import settings

# Create declarative base
Base = declarative_base()

# ===== Database Models =====

class DeliveryRecord(Base):
    """Optimized delivery information with performance metrics"""
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
    
    # Metadata
    route_data = Column(JSON, nullable=True)  # Store complete route information
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    blockchain_certificate_id = Column(String(255), ForeignKey('blockchain_certificates.certificate_id'), nullable=True)
    blockchain_certificate = relationship('BlockchainCertificate', back_populates='delivery_record')
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_delivery_vehicle_date', 'vehicle_id', 'created_at'),
        Index('idx_delivery_optimization', 'optimization_method', 'optimization_score'),
    )

class RouteOptimization(Base):
    """Route optimization requests and results"""
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
    
    # Metadata
    algorithm_used = Column(String(100), nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_optimization_status_date', 'status', 'created_at'),
        Index('idx_optimization_algorithm', 'algorithm_used', 'quantum_improvement_score'),
    )

class CarbonCalculation(Base):
    """Carbon emission calculations with factors"""
    __tablename__ = 'carbon_calculations'
    
    id = Column(Integer, primary_key=True, index=True)
    calculation_id = Column(String(255), unique=True, index=True, nullable=False)
    route_id = Column(String(255), nullable=False, index=True)
    
    # Basic calculation data
    total_emissions_kg = Column(Float, nullable=False)
    emissions_per_km = Column(Float, nullable=False)
    distance_km = Column(Float, nullable=False)
    vehicle_type = Column(String(100), nullable=False, index=True)
    
    # Impact factors
    weather_impact_factor = Column(Float, nullable=True, default=1.0)
    load_impact_factor = Column(Float, nullable=True, default=1.0)
    traffic_impact_factor = Column(Float, nullable=True, default=1.0)
    efficiency_factor = Column(Float, nullable=True, default=1.0)
    
    # Economic data
    carbon_cost_usd = Column(Float, nullable=True)
    carbon_price_per_ton = Column(Float, nullable=True, default=50.0)
    
    # Environmental impact
    environmental_impact = Column(String(50), nullable=True)
    carbon_saved_kg = Column(Float, nullable=True, default=0.0)
    
    # Calculation metadata
    methodology = Column(String(100), nullable=True, default="IPCC 2021 Guidelines")
    confidence_level = Column(Float, nullable=True, default=0.95)
    weather_conditions = Column(JSON, nullable=True)
    calculation_timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_carbon_vehicle_date', 'vehicle_type', 'calculation_timestamp'),
        Index('idx_carbon_route_emissions', 'route_id', 'total_emissions_kg'),
    )

class BlockchainCertificate(Base):
    """Certificate references and verification status"""
    __tablename__ = 'blockchain_certificates'
    
    certificate_id = Column(String(255), primary_key=True, index=True)
    route_id = Column(String(255), nullable=False, index=True)
    vehicle_id = Column(String(255), nullable=False)
    
    # Certificate data
    carbon_saved_kg = Column(Float, nullable=False)
    cost_saved_usd = Column(Float, nullable=False)
    distance_km = Column(Float, nullable=False)
    optimization_score = Column(Integer, nullable=False)
    
    # Blockchain data
    verification_hash = Column(String(255), nullable=False)
    transaction_hash = Column(String(255), nullable=False, unique=True, index=True)
    block_number = Column(Integer, nullable=False, index=True)
    gas_used = Column(Integer, nullable=True)
    
    # Status and metadata
    verified = Column(Boolean, default=False, index=True)
    certificate_status = Column(String(50), nullable=False, default="pending")
    blockchain_network = Column(String(100), nullable=False, default="ganache_local")
    issuer = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    delivery_record = relationship('DeliveryRecord', back_populates='blockchain_certificate')
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_certificate_status_date', 'certificate_status', 'created_at'),
        Index('idx_certificate_blockchain', 'blockchain_network', 'verified'),
    )

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
    )

# ===== Database Engine and Session Setup =====

def create_database_engine():
    """Create database engine with appropriate configuration"""
    database_url = settings.database_url_to_use
    
    if database_url.startswith("sqlite"):
        # SQLite configuration for development
        engine = create_engine(
            database_url,
            connect_args={
                "check_same_thread": False,
                "timeout": 20
            },
            poolclass=StaticPool,
            pool_pre_ping=True,
            echo=settings.DATABASE_ECHO
        )
    else:
        # PostgreSQL configuration for production
        engine = create_engine(
            database_url,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=settings.DATABASE_ECHO
        )
    
    return engine

# Create engine instance
engine = create_database_engine()

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ===== Database Dependencies =====

def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session
    Used with FastAPI Depends() for automatic session management
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def get_db_session() -> Session:
    """
    Get database session for direct use
    Remember to close the session manually
    """
    return SessionLocal()

# ===== Database Initialization =====

def create_tables():
    """Create all database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating database tables: {str(e)}")
        return False

def drop_tables():
    """Drop all database tables (use with caution)"""
    try:
        Base.metadata.drop_all(bind=engine)
        print("✅ Database tables dropped successfully")
        return True
    except Exception as e:
        print(f"❌ Error dropping database tables: {str(e)}")
        return False

def init_database():
    """Initialize database with tables and seed data"""
    try:
        # Ensure database directory exists
        if settings.DATABASE_URL.startswith("sqlite"):
            db_path = Path(settings.DATABASE_URL.replace("sqlite:///", ""))
            db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create tables
        create_tables()
        
        # Seed vehicle profiles
        seed_vehicle_profiles()
        
        print("✅ Database initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        return False

def seed_vehicle_profiles():
    """Seed database with default vehicle profiles"""
    try:
        db = get_db_session()
        
        # Check if vehicle profiles already exist
        existing_count = db.query(VehicleProfile).count()
        if existing_count > 0:
            print(f"Vehicle profiles already exist ({existing_count} profiles)")
            db.close()
            return
        
        # Default vehicle profiles
        vehicle_profiles = [
            {
                "vehicle_type": "diesel_truck",
                "display_name": "Diesel Truck",
                "capacity_kg": 1000.0,
                "max_range_km": 800.0,
                "fuel_type": "diesel",
                "cost_per_km": 0.85,
                "emission_factor": 0.27,
                "efficiency_rating": "C",
                "weather_sensitivity": 1.15,
                "load_sensitivity": 1.20,
                "description": "Heavy-duty diesel truck for large deliveries",
                "environmental_impact": "high",
                "recommended_use": "Long distance, high capacity deliveries"
            },
            {
                "vehicle_type": "electric_van",
                "display_name": "Electric Van",
                "capacity_kg": 500.0,
                "max_range_km": 300.0,
                "fuel_type": "electric",
                "cost_per_km": 0.65,
                "emission_factor": 0.05,
                "efficiency_rating": "A+",
                "weather_sensitivity": 1.05,
                "load_sensitivity": 1.08,
                "description": "Zero-emission electric delivery van",
                "environmental_impact": "very_low",
                "recommended_use": "Urban deliveries, short to medium distance"
            },
            {
                "vehicle_type": "hybrid_delivery",
                "display_name": "Hybrid Delivery Vehicle",
                "capacity_kg": 750.0,
                "max_range_km": 600.0,
                "fuel_type": "hybrid",
                "cost_per_km": 0.75,
                "emission_factor": 0.12,
                "efficiency_rating": "B+",
                "weather_sensitivity": 1.08,
                "load_sensitivity": 1.12,
                "description": "Fuel-efficient hybrid delivery vehicle",
                "environmental_impact": "medium",
                "recommended_use": "Mixed urban and suburban deliveries"
            },
            {
                "vehicle_type": "gas_truck",
                "display_name": "Gas Truck",
                "capacity_kg": 800.0,
                "max_range_km": 700.0,
                "fuel_type": "gasoline",
                "cost_per_km": 0.80,
                "emission_factor": 0.23,
                "efficiency_rating": "C+",
                "weather_sensitivity": 1.12,
                "load_sensitivity": 1.18,
                "description": "Standard gasoline delivery truck",
                "environmental_impact": "medium_high",
                "recommended_use": "General purpose deliveries"
            },
            {
                "vehicle_type": "cargo_bike",
                "display_name": "Electric Cargo Bike",
                "capacity_kg": 50.0,
                "max_range_km": 80.0,
                "fuel_type": "electric",
                "cost_per_km": 0.25,
                "emission_factor": 0.01,
                "efficiency_rating": "A++",
                "weather_sensitivity": 1.02,
                "load_sensitivity": 1.05,
                "description": "Ultra-low emission cargo bike for small deliveries",
                "environmental_impact": "minimal",
                "recommended_use": "Last-mile urban deliveries, small packages"
            }
        ]
        
        # Insert vehicle profiles
        for profile_data in vehicle_profiles:
            profile = VehicleProfile(**profile_data)
            db.add(profile)
        
        db.commit()
        print(f"✅ Seeded {len(vehicle_profiles)} vehicle profiles")
        
    except Exception as e:
        print(f"❌ Error seeding vehicle profiles: {str(e)}")
        if db:
            db.rollback()
    finally:
        if db:
            db.close()

# ===== Database Health Check with Auto-Fix =====

def check_database_health() -> dict:
    """Check database connectivity and health with auto-fix for missing columns"""
    print("\n=== Starting Database Health Check ===")
    try:
        print("🔄 Establishing database connection...")
        db = get_db_session()
        
        # Test basic connectivity
        print("🔄 Testing database connectivity...")
        db.execute(text('SELECT 1'))
        print("✅ Database connection successful")
        
        # ✅ NEW: Auto-fix missing columns in delivery_records table
        print("\n🔄 Checking and fixing delivery_records table schema...")
        try:
            # Check delivery_records table schema
            result = db.execute(text("PRAGMA table_info(delivery_records)"))
            existing_columns = [row[1] for row in result.fetchall()]
            
            # Required columns that might be missing
            required_columns = {
                'total_distance': 'REAL',
                'total_time': 'REAL', 
                'total_cost_usd': 'REAL',
                'total_emissions_kg': 'REAL',
                'optimization_score': 'REAL',
                'vehicle_utilization_percent': 'REAL',
                'load_factor': 'REAL'
            }
            
            # Add missing columns
            columns_added = 0
            for col_name, col_type in required_columns.items():
                if col_name not in existing_columns:
                    print(f"➕ Adding missing column: {col_name} ({col_type})")
                    db.execute(text(f"ALTER TABLE delivery_records ADD COLUMN {col_name} {col_type}"))
                    columns_added += 1
                    
            if columns_added > 0:
                db.commit()
                print(f"✅ Fixed schema - added {columns_added} missing columns")
            else:
                print("✅ Schema check completed - no missing columns")
            
        except Exception as schema_error:
            print(f"⚠️ Schema check failed: {str(schema_error)}")
            db.rollback()
            # Continue with health check even if schema fix fails
        
        # Get table counts
        print("\n🔄 Collecting table statistics...")
        table_counts = {}
        
        print("   📊 Counting delivery_records...")
        table_counts["delivery_records"] = db.query(DeliveryRecord).count()
        
        print("   📊 Counting route_optimizations...")
        table_counts["route_optimizations"] = db.query(RouteOptimization).count()
        
        print("   📊 Counting carbon_calculations...")
        table_counts["carbon_calculations"] = db.query(CarbonCalculation).count()
        
        print("   📊 Counting blockchain_certificates...")
        table_counts["blockchain_certificates"] = db.query(BlockchainCertificate).count()
        
        print("   📊 Counting vehicle_profiles...")
        table_counts["vehicle_profiles"] = db.query(VehicleProfile).count()
        
        total_records = sum(table_counts.values())
        print(f"\n✅ Health check complete - Found {total_records} total records")
        
        db.close()
        print("✅ Database connection closed properly")
        
        database_url = settings.database_url_to_use.split("@")[-1] if "@" in settings.database_url_to_use else settings.database_url_to_use
        print(f"📍 Database URL: {database_url}")
        
        result = {
            "status": "healthy",
            "database_url": database_url,
            "table_counts": table_counts,
            "total_records": total_records
        }
        print("\n=== Health Check Results ===")
        print(f"Status: {result['status']}")
        print("Table counts:")
        for table, count in table_counts.items():
            print(f"   {table}: {count}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Database health check failed!")
        print(f"❌ Error: {str(e)}")
        database_url = settings.database_url_to_use.split("@")[-1] if "@" in settings.database_url_to_use else settings.database_url_to_use
        print(f"📍 Database URL: {database_url}")
        
        return {
            "status": "unhealthy",
            "error": str(e),
            "database_url": database_url
        }

# ===== Utility Functions =====

def get_vehicle_profile_by_type(vehicle_type: str) -> VehicleProfile:
    """Get vehicle profile by type"""
    db = get_db_session()
    try:
        profile = db.query(VehicleProfile).filter(
            VehicleProfile.vehicle_type == vehicle_type,
            VehicleProfile.is_active == True
        ).first()
        return profile
    finally:
        db.close()

def get_all_vehicle_profiles() -> list:
    """Get all active vehicle profiles"""
    db = get_db_session()
    try:
        profiles = db.query(VehicleProfile).filter(
            VehicleProfile.is_active == True
        ).all()
        return profiles
    finally:
        db.close()

def cleanup_old_records(days: int = 30):
    """Clean up old records older than specified days"""
    try:
        db = get_db_session()
        cutoff_date = func.now() - func.interval(f'{days} days')
        
        # Clean up old route optimizations
        old_optimizations = db.query(RouteOptimization).filter(
            RouteOptimization.created_at < cutoff_date,
            RouteOptimization.status.in_(["completed", "failed"])
        ).count()
        
        if old_optimizations > 0:
            db.query(RouteOptimization).filter(
                RouteOptimization.created_at < cutoff_date,
                RouteOptimization.status.in_(["completed", "failed"])
            ).delete()
            
        db.commit()
        print(f"✅ Cleaned up {old_optimizations} old optimization records")
        
    except Exception as e:
        print(f"❌ Error cleaning up old records: {str(e)}")
        if db:
            db.rollback()
    finally:
        if db:
            db.close()

# Initialize database on import
if __name__ == "__main__":
    init_database()
else:
    # Auto-initialize for production
    try:
        create_tables()
    except Exception as e:
        print(f"Warning: Could not auto-initialize database: {str(e)}")

# Export commonly used items
__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "get_db",
    "get_db_session",
    "DeliveryRecord",
    "RouteOptimization", 
    "CarbonCalculation",
    "BlockchainCertificate",
    "VehicleProfile",
    "init_database",
    "create_tables",
    "check_database_health",
    "get_vehicle_profile_by_type",
    "get_all_vehicle_profiles"
]
