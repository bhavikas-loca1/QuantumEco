from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Dict, Any, Optional
import asyncio
import time
import uuid
from datetime import datetime

from app.schemas.route_schemas import (
    RouteOptimizationRequest,
    RouteOptimizationResponse,
    BatchOptimizationRequest,
    BatchOptimizationResponse,
    RouteComparisonRequest,
    RouteComparisonResponse,
    RouteRecalculationRequest,
    RouteDetailsResponse,
    VehicleProfileResponse,
    Location,
    Vehicle
)
from app.services.route_optimizer import RouteOptimizer
from app.services.carbon_calculator import CarbonCalculator
from app.services.blockchain_service import BlockchainService
from app.utils.helpers import generate_route_id, validate_coordinates
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# Initialize services
route_optimizer = RouteOptimizer()
carbon_calculator = CarbonCalculator()
blockchain_service = BlockchainService()

# In-memory cache for optimization results (for demo purposes)
optimization_cache: Dict[str, Dict[str, Any]] = {}

@router.post("/optimize", response_model=RouteOptimizationResponse)
async def optimize_routes(
    request: RouteOptimizationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Quantum-inspired multi-objective route optimization
    Optimizes delivery routes considering cost, carbon emissions, and time
    """
    try:
        # Validate input data
        if len(request.locations) < 2:
            raise HTTPException(status_code=400, detail="At least 2 locations required")
        
        if len(request.vehicles) < 1:
            raise HTTPException(status_code=400, detail="At least 1 vehicle required")
        
        # Validate coordinates
        for location in request.locations:
            if not validate_coordinates(location.latitude, location.longitude):
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid coordinates for location {location.id}"
                )
        
        # Generate unique optimization ID
        optimization_id = generate_route_id()
        start_time = time.time()
        
        # Prepare optimization data
        optimization_data = {
            "locations": [loc.dict() for loc in request.locations],
            "vehicles": [veh.dict() for veh in request.vehicles],
            "optimization_goals": request.optimization_goals,
            "constraints": {
                "max_distance_per_vehicle": request.max_distance_per_vehicle,
                "max_time_per_vehicle": request.max_time_per_vehicle,
                "traffic_enabled": request.traffic_enabled,
                "weather_enabled": request.weather_enabled
            }
        }
        
        # Run quantum-inspired optimization
        optimization_result = await route_optimizer.optimize_multi_objective(
            locations=request.locations,
            vehicles=request.vehicles,
            optimization_goals=request.optimization_goals,
            constraints=optimization_data["constraints"]
        )
        
        # Calculate carbon emissions for optimized routes
        carbon_results = []
        total_carbon_emissions = 0
        total_carbon_saved = 0
        
        for route in optimization_result["optimized_routes"]:
            carbon_data = await carbon_calculator.calculate_route_emissions(
                route=route,
                vehicle_type=route["vehicle_type"],
                weather_enabled=request.weather_enabled
            )
            carbon_results.append(carbon_data)
            total_carbon_emissions += carbon_data["total_emissions"]
            total_carbon_saved += carbon_data.get("carbon_saved", 0)
        
        # Calculate traditional routing for comparison
        traditional_result = await route_optimizer.calculate_traditional_routing(
            locations=request.locations,
            vehicles=request.vehicles
        )
        
        # Calculate savings
        savings_analysis = {
            "cost_saved": traditional_result["total_cost"] - optimization_result["total_cost"],
            "time_saved": traditional_result["total_time"] - optimization_result["total_time"],
            "distance_saved": traditional_result["total_distance"] - optimization_result["total_distance"],
            "carbon_saved": total_carbon_saved,
            "cost_improvement_percent": round(
                ((traditional_result["total_cost"] - optimization_result["total_cost"]) / traditional_result["total_cost"]) * 100, 2
            ),
            "time_improvement_percent": round(
                ((traditional_result["total_time"] - optimization_result["total_time"]) / traditional_result["total_time"]) * 100, 2
            ),
            "carbon_improvement_percent": round(
                (total_carbon_saved / traditional_result.get("total_carbon", 1)) * 100, 2
            )
        }
        
        # Prepare response
        response_data = RouteOptimizationResponse(
            optimization_id=optimization_id,
            status="completed",
            optimized_routes=optimization_result["optimized_routes"],
            total_distance=optimization_result["total_distance"],
            total_time=optimization_result["total_time"],
            total_cost=optimization_result["total_cost"],
            total_carbon_emissions=total_carbon_emissions,
            savings_analysis=savings_analysis,
            optimization_method="quantum_inspired",
            optimization_time=round(time.time() - start_time, 2),
            quantum_improvement_score=optimization_result.get("quantum_score", 85),
            created_at=datetime.utcnow()
        )
        
        # Cache the result
        optimization_cache[optimization_id] = response_data.dict()
        
        # Create blockchain certificate in background
        if request.create_certificate:
            background_tasks.add_task(
                create_optimization_certificate,
                optimization_id,
                response_data.dict()
            )
        
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")


@router.post("/batch-optimize", response_model=BatchOptimizationResponse)
async def batch_optimize_routes(request: BatchOptimizationRequest):
    """
    Optimize multiple delivery scenarios simultaneously
    Useful for comparing different vehicle configurations or time windows
    """
    try:
        if len(request.scenarios) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 scenarios allowed")
        
        batch_id = generate_route_id("batch")
        start_time = time.time()
        
        # Process scenarios concurrently
        tasks = []
        for i, scenario in enumerate(request.scenarios):
            task = route_optimizer.optimize_multi_objective(
                locations=scenario.locations,
                vehicles=scenario.vehicles,
                optimization_goals=scenario.optimization_goals,
                constraints=scenario.constraints or {}
            )
            tasks.append(task)
        
        # Wait for all optimizations to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        optimized_scenarios = []
        total_processing_time = time.time() - start_time
        
        for i, (scenario, result) in enumerate(zip(request.scenarios, results)):
            if isinstance(result, Exception):
                scenario_result = {
                    "scenario_id": f"scenario_{i+1}",
                    "status": "failed",
                    "error": str(result),
                    "optimized_routes": [],
                    "savings_analysis": {}
                }
            else:
                # Calculate carbon emissions
                carbon_data = await carbon_calculator.calculate_batch_emissions(
                    routes=result["optimized_routes"]
                )
                
                scenario_result = {
                    "scenario_id": f"scenario_{i+1}",
                    "status": "completed",
                    "optimized_routes": result["optimized_routes"],
                    "total_distance": result["total_distance"],
                    "total_time": result["total_time"],
                    "total_cost": result["total_cost"],
                    "total_carbon_emissions": carbon_data["total_emissions"],
                    "savings_analysis": result.get("savings_analysis", {}),
                    "quantum_improvement_score": result.get("quantum_score", 85)
                }
            
            optimized_scenarios.append(scenario_result)
        
        # Find best scenario
        best_scenario = max(
            [s for s in optimized_scenarios if s["status"] == "completed"],
            key=lambda x: x.get("quantum_improvement_score", 0),
            default=None
        )
        
        response = BatchOptimizationResponse(
            batch_id=batch_id,
            status="completed",
            scenarios=optimized_scenarios,
            best_scenario_id=best_scenario["scenario_id"] if best_scenario else None,
            total_processing_time=round(total_processing_time, 2),
            successful_optimizations=len([s for s in optimized_scenarios if s["status"] == "completed"]),
            created_at=datetime.utcnow()
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch optimization failed: {str(e)}")


@router.get("/route/{route_id}", response_model=RouteDetailsResponse)
async def get_route_details(route_id: str):
    """
    Get detailed information about a specific optimized route
    """
    try:
        # Check cache first
        if route_id in optimization_cache:
            cached_data = optimization_cache[route_id]
            
            # Get additional details
            route_details = await route_optimizer.get_route_analytics(route_id)
            carbon_details = await carbon_calculator.get_detailed_emissions(route_id)
            
            response = RouteDetailsResponse(
                route_id=route_id,
                optimization_data=cached_data,
                route_analytics=route_details,
                carbon_analysis=carbon_details,
                blockchain_certificate=cached_data.get("certificate_id"),
                last_updated=datetime.utcnow()
            )
            
            return response
        else:
            raise HTTPException(status_code=404, detail="Route not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get route details: {str(e)}")


@router.post("/compare", response_model=RouteComparisonResponse)
async def compare_routes(request: RouteComparisonRequest):
    """
    Compare quantum-inspired vs traditional route optimization
    Shows the benefits of using quantum-inspired algorithms
    """
    try:
        start_time = time.time()
        
        # Run both optimizations concurrently
        quantum_task = route_optimizer.optimize_multi_objective(
            locations=request.locations,
            vehicles=request.vehicles,
            optimization_goals=request.optimization_goals
        )
        
        traditional_task = route_optimizer.calculate_traditional_routing(
            locations=request.locations,
            vehicles=request.vehicles
        )
        
        quantum_result, traditional_result = await asyncio.gather(
            quantum_task, traditional_task
        )
        
        # Calculate carbon emissions for both
        quantum_carbon = await carbon_calculator.calculate_batch_emissions(
            routes=quantum_result["optimized_routes"]
        )
        
        traditional_carbon = await carbon_calculator.calculate_batch_emissions(
            routes=traditional_result["routes"]
        )
        
        # Calculate improvements
        improvements = {
            "cost_improvement": round(
                ((traditional_result["total_cost"] - quantum_result["total_cost"]) / traditional_result["total_cost"]) * 100, 2
            ),
            "time_improvement": round(
                ((traditional_result["total_time"] - quantum_result["total_time"]) / traditional_result["total_time"]) * 100, 2
            ),
            "distance_improvement": round(
                ((traditional_result["total_distance"] - quantum_result["total_distance"]) / traditional_result["total_distance"]) * 100, 2
            ),
            "carbon_improvement": round(
                ((traditional_carbon["total_emissions"] - quantum_carbon["total_emissions"]) / traditional_carbon["total_emissions"]) * 100, 2
            )
        }
        
        response = RouteComparisonResponse(
            comparison_id=generate_route_id("comp"),
            quantum_inspired_result={
                "method": "quantum_inspired",
                "total_cost": quantum_result["total_cost"],
                "total_time": quantum_result["total_time"],
                "total_distance": quantum_result["total_distance"],
                "total_carbon": quantum_carbon["total_emissions"],
                "routes": quantum_result["optimized_routes"],
                "optimization_time": quantum_result.get("processing_time", 0)
            },
            traditional_result={
                "method": "traditional",
                "total_cost": traditional_result["total_cost"],
                "total_time": traditional_result["total_time"],
                "total_distance": traditional_result["total_distance"],
                "total_carbon": traditional_carbon["total_emissions"],
                "routes": traditional_result["routes"],
                "optimization_time": traditional_result.get("processing_time", 0)
            },
            improvements=improvements,
            winner="quantum_inspired" if sum(improvements.values()) > 0 else "traditional",
            total_comparison_time=round(time.time() - start_time, 2),
            created_at=datetime.utcnow()
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Route comparison failed: {str(e)}")


@router.post("/recalculate")
async def recalculate_route(request: RouteRecalculationRequest):
    """
    Real-time route recalculation based on traffic/weather updates
    """
    try:
        if request.route_id not in optimization_cache:
            raise HTTPException(status_code=404, detail="Original route not found")
        
        original_data = optimization_cache[request.route_id]
        
        # Get current traffic and weather data
        current_conditions = await route_optimizer.get_current_conditions(
            locations=request.affected_locations,
            include_traffic=True,
            include_weather=True
        )
        
        # Recalculate affected routes
        recalculated_routes = await route_optimizer.recalculate_with_conditions(
            original_routes=original_data["optimized_routes"],
            current_conditions=current_conditions,
            optimization_goals=original_data.get("optimization_goals", {})
        )
        
        # Calculate impact
        impact_analysis = {
            "routes_affected": len(request.affected_locations),
            "time_change": recalculated_routes["total_time"] - original_data["total_time"],
            "cost_change": recalculated_routes["total_cost"] - original_data["total_cost"],
            "distance_change": recalculated_routes["total_distance"] - original_data["total_distance"],
            "recalculation_reason": request.reason
        }
        
        # Update cache
        updated_data = original_data.copy()
        updated_data.update({
            "optimized_routes": recalculated_routes["optimized_routes"],
            "total_time": recalculated_routes["total_time"],
            "total_cost": recalculated_routes["total_cost"],
            "total_distance": recalculated_routes["total_distance"],
            "last_recalculation": datetime.utcnow().isoformat(),
            "recalculation_count": updated_data.get("recalculation_count", 0) + 1
        })
        
        optimization_cache[request.route_id] = updated_data
        
        return {
            "route_id": request.route_id,
            "status": "recalculated",
            "updated_routes": recalculated_routes["optimized_routes"],
            "impact_analysis": impact_analysis,
            "recalculation_time": datetime.utcnow(),
            "conditions_considered": current_conditions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Route recalculation failed: {str(e)}")


@router.get("/vehicles", response_model=List[VehicleProfileResponse])
async def get_vehicle_profiles():
    """
    Get available vehicle types and their capabilities
    """
    try:
        vehicle_profiles = [
            VehicleProfileResponse(
                vehicle_type="diesel_truck",
                display_name="Diesel Truck",
                capacity_kg=1000,
                max_range_km=800,
                cost_per_km=0.85,
                emission_factor=0.27,
                fuel_type="diesel",
                description="Heavy-duty delivery truck for large loads",
                environmental_impact="high",
                recommended_use="Long distance, high capacity deliveries"
            ),
            VehicleProfileResponse(
                vehicle_type="electric_van",
                display_name="Electric Van",
                capacity_kg=500,
                max_range_km=300,
                cost_per_km=0.65,
                emission_factor=0.05,
                fuel_type="electric",
                description="Eco-friendly electric delivery van",
                environmental_impact="low",
                recommended_use="Urban deliveries, short to medium distance"
            ),
            VehicleProfileResponse(
                vehicle_type="hybrid_delivery",
                display_name="Hybrid Delivery Vehicle",
                capacity_kg=750,
                max_range_km=600,
                cost_per_km=0.75,
                emission_factor=0.12,
                fuel_type="hybrid",
                description="Fuel-efficient hybrid delivery vehicle",
                environmental_impact="medium",
                recommended_use="Mixed urban and suburban deliveries"
            ),
            VehicleProfileResponse(
                vehicle_type="gas_truck",
                display_name="Gas Truck",
                capacity_kg=800,
                max_range_km=700,
                cost_per_km=0.80,
                emission_factor=0.23,
                fuel_type="gasoline",
                description="Standard gasoline delivery truck",
                environmental_impact="medium-high",
                recommended_use="General purpose deliveries"
            ),
            VehicleProfileResponse(
                vehicle_type="cargo_bike",
                display_name="Electric Cargo Bike",
                capacity_kg=50,
                max_range_km=80,
                cost_per_km=0.25,
                emission_factor=0.01,
                fuel_type="electric",
                description="Ultra-low emission cargo bike for small deliveries",
                environmental_impact="very_low",
                recommended_use="Last-mile urban deliveries, small packages"
            )
        ]
        
        return vehicle_profiles
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get vehicle profiles: {str(e)}")


# Background task for certificate creation
async def create_optimization_certificate(optimization_id: str, optimization_data: Dict[str, Any]):
    """
    Create blockchain certificate for optimization result
    """
    try:
        certificate_data = {
            "route_id": optimization_id,
            "vehicle_count": len(optimization_data.get("optimized_routes", [])),
            "carbon_saved": optimization_data.get("savings_analysis", {}).get("carbon_saved", 0),
            "cost_saved": optimization_data.get("savings_analysis", {}).get("cost_saved", 0),
            "distance_km": optimization_data.get("total_distance", 0),
            "optimization_score": optimization_data.get("quantum_improvement_score", 85)
        }
        
        certificate = await blockchain_service.create_delivery_certificate(certificate_data)
        
        # Update cache with certificate ID
        if optimization_id in optimization_cache:
            optimization_cache[optimization_id]["certificate_id"] = certificate.get("certificate_id")
            optimization_cache[optimization_id]["transaction_hash"] = certificate.get("transaction_hash")
        
    except Exception as e:
        print(f"Failed to create certificate for {optimization_id}: {str(e)}")


# Health check endpoint for route optimization service
@router.get("/health")
async def route_service_health():
    """
    Health check for route optimization service
    """
    try:
        # Test route optimizer
        optimizer_status = await route_optimizer.health_check()
        
        # Test carbon calculator
        carbon_status = await carbon_calculator.health_check()
        
        # Test blockchain service
        blockchain_status = blockchain_service.is_connected()
        
        return {
            "status": "healthy",
            "services": {
                "route_optimizer": optimizer_status,
                "carbon_calculator": carbon_status,
                "blockchain_service": blockchain_status
            },
            "cache_size": len(optimization_cache),
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")
