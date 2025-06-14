from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, Any

# Import all controllers
from app.controllers.route_controller import router as route_router
from app.controllers.carbon_controller import router as carbon_router
from app.controllers.blockchain_controller import router as blockchain_router
from app.controllers.analytics_controller import router as analytics_router
from app.controllers.demo_controller import router as demo_router

# Import configuration and database
from app.config import settings
from app.database import init_database, check_database_health, engine

# Import services for health checks
from app.services.route_optimizer import RouteOptimizer
from app.services.carbon_calculator import CarbonCalculator
from app.services.blockchain_service import BlockchainService
from app.services.analytics_service import AnalyticsService
from app.services.demo_data_service import DemoDataService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global service instances
route_optimizer = RouteOptimizer()
carbon_calculator = CarbonCalculator()
blockchain_service = BlockchainService()
analytics_service = AnalyticsService()
demo_service = DemoDataService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events"""
    # Startup
    logger.info("🚀 Starting QuantumEco Intelligence Backend...")
    
    try:
        # Initialize database
        logger.info("📊 Initializing database...")
        if init_database():
            logger.info("✅ Database initialized successfully")
        else:
            logger.warning("⚠️ Database initialization had issues")
        
        # Test service connections
        logger.info("🔧 Testing service connections...")
        
        # Test route optimizer
        optimizer_health = await route_optimizer.health_check()
        logger.info(f"🛣️ Route Optimizer: {optimizer_health}")
        
        # Test carbon calculator
        carbon_health = await carbon_calculator.health_check()
        logger.info(f"🌱 Carbon Calculator: {carbon_health}")
        
        # Test blockchain service
        blockchain_health = await blockchain_service.test_connection()
        logger.info(f"⛓️ Blockchain Service: {blockchain_health}")
        
        # Test analytics service
        analytics_health = await analytics_service.health_check()
        logger.info(f"📈 Analytics Service: {analytics_health}")
        
        logger.info("✅ All services initialized successfully!")
        logger.info(f"🌐 Server running on http://{settings.HOST}:{settings.PORT}")
        logger.info("📚 API Documentation: http://localhost:8000/docs")
        logger.info("🔍 Alternative docs: http://localhost:8000/redoc")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down QuantumEco Intelligence Backend...")
    try:
        # Close database connections
        engine.dispose()
        logger.info("✅ Database connections closed")
    except Exception as e:
        logger.error(f"❌ Shutdown error: {str(e)}")

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://your-app-name.netlify.app",  # Add your Netlify domain
        "https://*.netlify.app"  # Allow all Netlify subdomains
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(route_router, prefix="/api/routes", tags=["🛣️ Route Optimization"])
app.include_router(carbon_router, prefix="/api/carbon", tags=["🌱 Carbon Tracking"])
app.include_router(blockchain_router, prefix="/api/blockchain", tags=["⛓️ Blockchain Verification"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["📈 Analytics & Dashboard"])
app.include_router(demo_router, prefix="/api/demo", tags=["🎯 Demo Data"])


"""
# Test health check
curl http://localhost:8000/health

# Test quick demo
curl http://localhost:8000/demo/quick-start

# Test route optimization (POST request)
curl -X POST "http://localhost:8000/api/routes/optimize" \
  -H "Content-Type: application/json" \
  -d '{
    "locations": [
      {"id": "depot", "latitude": 40.7128, "longitude": -74.0060, "demand_kg": 0},
      {"id": "loc1", "latitude": 40.7589, "longitude": -73.9851, "demand_kg": 50}
    ],
    "vehicles": [
      {"id": "truck1", "type": "diesel_truck", "capacity_kg": 1000, "cost_per_km": 0.85, "emission_factor": 0.27}
    ]
  }'
"""

# Root endpoint
@app.get("/", tags=["System"])
async def root():
    """Root endpoint with system information"""
    return {
        "message": "🚀 QuantumEco Intelligence API",
        "version": settings.PROJECT_VERSION,
        "status": "operational",
        "description": "Quantum-inspired logistics optimization with blockchain verification",
        "endpoints": {
            "documentation": "/docs",
            "alternative_docs": "/redoc",
            "health": "/health",
            "system_info": "/system-info"
        },
        "timestamp": datetime.utcnow().isoformat()
    }

# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """Comprehensive health check for all services"""
    logger.info("🔍 Starting comprehensive health check...")
    try:
        # Check database
        logger.info("📊 Checking database health...")
        db_health = check_database_health()
        logger.info(f"Database health status: {db_health['status']}")
        if db_health['status'] != 'healthy':
            logger.warning(f"Database health issues detected: {db_health.get('details', 'No details provided')}")
        
        # Check all services
        logger.info("🔧 Checking service health...")
        
        # Route optimizer check
        logger.info("Checking route optimizer...")
        route_health = await route_optimizer.health_check()
        logger.info(f"Route optimizer status: {route_health}")
        
        # Carbon calculator check
        logger.info("Checking carbon calculator...")
        carbon_health = await carbon_calculator.health_check()
        logger.info(f"Carbon calculator status: {carbon_health}")
        
        # Analytics service check
        logger.info("Checking analytics service...")
        analytics_health = await analytics_service.health_check()
        logger.info(f"Analytics service status: {analytics_health}")
        
        services_health = {
            "route_optimizer": route_health,
            "carbon_calculator": carbon_health,
            "analytics_service": analytics_health,
        }
        
        # Blockchain service check
        logger.info("⛓️ Checking blockchain connection...")
        blockchain_health = await blockchain_service.test_connection()
        logger.info(f"Blockchain service status: {blockchain_health}")
        
        # Determine overall health
        logger.info("📊 Evaluating overall system health...")
        all_healthy = (
            db_health["status"] == "healthy" and
            all("healthy" in str(status) for status in services_health.values()) and 
            ("connected" in str(blockchain_health) or "healthy" in str(blockchain_health))
        )
        
        status = "healthy" if all_healthy else "degraded"
        logger.info(f"Overall system status: {status}")
        
        response_data = {
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "database": db_health,
            "services": services_health,
            "blockchain": blockchain_health,
            "uptime": "operational",
            "version": settings.PROJECT_VERSION
        }
        
        logger.info("✅ Health check completed successfully")
        logger.debug(f"Detailed health check response: {response_data}")
        return response_data
         
    except Exception as e:
        error_msg = f"Health check failed: {str(e)}"
        logger.error(error_msg)
        logger.exception("Detailed error traceback:")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
                "details": {
                    "error_type": type(e).__name__,
                    "error_location": "health_check endpoint",
                    "stack_trace": str(e.__traceback__)
                }
            }
        )

# System information endpoint
@app.get("/system-info", tags=["System"])
async def system_info():
    """Get detailed system information"""
    try:
        return {
            "project": {
                "name": settings.PROJECT_NAME,
                "version": settings.PROJECT_VERSION,
                "description": settings.PROJECT_DESCRIPTION,
                "environment": settings.ENVIRONMENT
            },
            "configuration": {
                "debug": settings.DEBUG,
                "database_url": settings.database_url_to_use.split("@")[-1] if "@" in settings.database_url_to_use else settings.database_url_to_use,
                "blockchain_url": settings.BLOCKCHAIN_URL,
                "api_keys_configured": settings.validate_api_keys()
            },
            "optimization": {
                "quantum_population_size": settings.QUANTUM_POPULATION_SIZE,
                "quantum_max_iterations": settings.QUANTUM_MAX_ITERATIONS,
                "optimization_weights": settings.get_optimization_weights()
            },
            "limits": {
                "max_locations_per_request": settings.MAX_LOCATIONS_PER_REQUEST,
                "max_vehicles_per_request": settings.MAX_VEHICLES_PER_REQUEST,
                "optimization_timeout": settings.OPTIMIZATION_TIMEOUT
            },
            "demo": {
                "demo_mode_enabled": settings.ENABLE_DEMO_MODE,
                "walmart_stores": settings.WALMART_STORES_COUNT,
                "daily_deliveries": settings.walmart_total_daily_deliveries
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"System info failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Demo quick-start endpoint
@app.get("/demo/quick-start", tags=["🎯 Demo Data"])
async def demo_quick_start():
    """Quick demo endpoint to showcase the system
    
        Expected Output:
        
        {
        "demo_title": "🚀 QuantumEco Intelligence - Live Demo",
        "scenario": "Walmart NYC Delivery Optimization",
        "locations": 20,
        "vehicles": 3,
        "results": {
            "traditional": {
                "total_cost": 372.8,
                "total_carbon": 91.4,
                "total_time": 1373.5
            },
            "quantum_inspired": {
                "total_cost": 264.73,
                "total_carbon": 63.44,
                "total_time": 1074.3
            },
            "improvements": {
                "cost_saved": "$108.07 (29.0%)",
                "carbon_reduced": "27.96 kg CO₂ (30.6%)",
                "time_saved": "299.2 min (21.8%)"
            }
        },
        "walmart_scale_projection": {
            "annual_cost_savings": "$103,544,568,750",
            "annual_carbon_reduction": "26,789,175 tons CO₂",
            "stores_impacted": "10,500"
        },
        "blockchain_certificates": 3,
        "environmental_impact": {
            "trees_planted_equivalent": 1.3,
            "cars_off_road_days": 2.2,
            "homes_powered_hours": 33.7,
            "miles_not_driven": 69.2,
            "gallons_fuel_saved": 3.1
        },
        "generated_at": "2025-06-09T05:11:16.648551"
        }
    
    
    """
    try:
        logger.info("🎯 Generating quick demo scenario...")
        
        # Generate a quick NYC demo scenario
        from app.utils.demo_data import demo_generator
        scenario = demo_generator.generate_walmart_nyc_scenario(20, 3)  # Smaller for quick demo
        
        # Extract key metrics for impressive display
        quantum_result = scenario["quantum_optimization"]
        traditional_result = scenario["traditional_optimization"]
        savings = scenario["savings_analysis"]
        
        return {
            "demo_title": "🚀 QuantumEco Intelligence - Live Demo",
            "scenario": "Walmart NYC Delivery Optimization",
            "locations": 20,
            "vehicles": 3,
            "results": {
                "traditional": {
                    "total_cost": traditional_result["total_cost"],
                    "total_carbon": traditional_result["total_carbon"],
                    "total_time": traditional_result["total_time"]
                },
                "quantum_inspired": {
                    "total_cost": quantum_result["total_cost"],
                    "total_carbon": quantum_result["total_carbon"],
                    "total_time": quantum_result["total_time"]
                },
                "improvements": {
                    "cost_saved": f"${savings['cost_saved_usd']:.2f} ({savings['cost_improvement_percent']:.1f}%)",
                    "carbon_reduced": f"{savings['carbon_saved_kg']:.2f} kg CO₂ ({savings['carbon_improvement_percent']:.1f}%)",
                    "time_saved": f"{savings['time_saved_minutes']:.1f} min ({savings['time_improvement_percent']:.1f}%)"
                }
            },
            "walmart_scale_projection": {
                "annual_cost_savings": f"${scenario['walmart_scale_projection']['annual_cost_savings_usd']:,.0f}",
                "annual_carbon_reduction": f"{scenario['walmart_scale_projection']['annual_carbon_reduction_tons']:,.0f} tons CO₂",
                "stores_impacted": f"{scenario['walmart_scale_projection']['stores_impacted']:,}"
            },
            "blockchain_certificates": len(scenario["blockchain_certificates"]),
            "environmental_impact": scenario["environmental_impact"],
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Demo quick-start failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Demo generation failed: {str(e)}")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "log": str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level="info"
    )
