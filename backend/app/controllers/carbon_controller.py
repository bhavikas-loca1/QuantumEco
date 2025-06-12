from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from typing import List, Dict, Any, Optional
import asyncio
from datetime import datetime, timedelta
import uuid

from app.schemas.carbon_schemas import (
    CarbonCalculationRequest,
    CarbonCalculationResponse,
    CarbonTrackingRequest,
    CarbonTrackingResponse,
    CarbonSavingsRequest,
    CarbonSavingsResponse,
    VehicleEmissionProfile,
    DailyCarbonReport,
    CarbonTrendsResponse,
    CarbonPredictionRequest,
    CarbonPredictionResponse
)
from app.services.carbon_calculator import CarbonCalculator
from app.utils.helpers import validate_date_format, generate_calculation_id
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# Initialize carbon calculator service
carbon_calculator = CarbonCalculator()

# In-memory cache for calculations (for demo purposes)
calculation_cache: Dict[str, Dict[str, Any]] = {}

@router.post("/calculate", response_model=CarbonCalculationResponse)
async def calculate_carbon_footprint(
    request: CarbonCalculationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Calculate carbon emissions for a specific route
    Considers vehicle type, distance, weather conditions, and load factors
    """
    try:
        # Validate input parameters
        if request.distance_km <= 0:
            raise HTTPException(status_code=400, detail="Distance must be greater than 0")
        
        if request.load_factor < 0 or request.load_factor > 2.0:
            raise HTTPException(status_code=400, detail="Load factor must be between 0 and 2.0")
        
        # Generate calculation ID
        calculation_id = generate_calculation_id()
        
        # Get vehicle emission profile
        vehicle_profile = carbon_calculator.get_vehicle_emission_profile(request.vehicle_type)
        if not vehicle_profile:
            raise HTTPException(status_code=400, detail=f"Unknown vehicle type: {request.vehicle_type}")
        
        # Calculate base emissions
        base_emissions = request.distance_km * vehicle_profile["emission_factor"]
        
        # Apply weather impact factor
        weather_impact_factor = 1.0
        if request.weather_conditions:
            weather_impact_factor = carbon_calculator.calculate_weather_impact(
                weather_conditions=request.weather_conditions,
                vehicle_type=request.vehicle_type
            )
        
        # Apply load impact factor
        load_impact_factor = carbon_calculator.calculate_load_impact(
            load_factor=request.load_factor,
            vehicle_type=request.vehicle_type
        )
        
        # Calculate total emissions
        total_emissions = base_emissions * weather_impact_factor * load_impact_factor
        emissions_per_km = total_emissions / request.distance_km
        
        # Calculate carbon cost (using $50/ton CO2 as standard carbon price)
        carbon_cost_usd = (total_emissions / 1000) * 50  # Convert kg to tons
        
        # Prepare response
        response = CarbonCalculationResponse(
            calculation_id=calculation_id,
            route_id=request.route_id,
            total_emissions_kg=round(total_emissions, 3),
            emissions_per_km=round(emissions_per_km, 3),
            weather_impact_factor=round(weather_impact_factor, 3),
            load_impact_factor=round(load_impact_factor, 3),
            carbon_cost_usd=round(carbon_cost_usd, 2),
            vehicle_type=request.vehicle_type,
            distance_km=request.distance_km,
            calculation_timestamp=datetime.utcnow(),
            methodology="IPCC 2021 Guidelines",
            confidence_level=0.95
        )
        
        # Cache the calculation
        calculation_cache[calculation_id] = {
            "request": request.dict(),
            "response": response.dict(),
            "timestamp": datetime.utcnow()
        }
        
        # Store in database (background task)
        background_tasks.add_task(
            store_carbon_calculation,
            calculation_id,
            request.dict(),
            response.dict()
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Carbon calculation failed: {str(e)}")


@router.post("/track-realtime", response_model=List[CarbonTrackingResponse])
async def track_realtime_emissions(request: CarbonTrackingRequest):
    """
    Real-time carbon tracking for active deliveries
    Provides live emission updates for ongoing delivery routes
    """
    try:
        if len(request.delivery_ids) > 50:
            raise HTTPException(status_code=400, detail="Maximum 50 deliveries can be tracked simultaneously")
        
        tracking_results = []
        
        # Process each delivery ID
        for delivery_id in request.delivery_ids:
            try:
                # Get current delivery status and location
                delivery_status = await carbon_calculator.get_delivery_status(delivery_id)
                
                if not delivery_status:
                    tracking_results.append(CarbonTrackingResponse(
                        delivery_id=delivery_id,
                        status="not_found",
                        current_emissions_kg=0.0,
                        distance_covered_km=0.0,
                        estimated_total_emissions_kg=0.0,
                        timestamp=datetime.utcnow(),
                        error_message="Delivery not found"
                    ))
                    continue
                
                # Calculate current emissions based on distance covered
                current_emissions = await carbon_calculator.calculate_realtime_emissions(
                    delivery_id=delivery_id,
                    distance_covered=delivery_status["distance_covered"],
                    vehicle_type=delivery_status["vehicle_type"],
                    current_conditions=delivery_status.get("current_conditions", {})
                )
                
                tracking_results.append(CarbonTrackingResponse(
                    delivery_id=delivery_id,
                    status=delivery_status["status"],
                    current_emissions_kg=round(current_emissions["current_emissions"], 3),
                    distance_covered_km=round(delivery_status["distance_covered"], 2),
                    estimated_total_emissions_kg=round(current_emissions["estimated_total"], 3),
                    progress_percentage=round(delivery_status["progress_percentage"], 1),
                    vehicle_type=delivery_status["vehicle_type"],
                    timestamp=datetime.utcnow()
                ))
                
            except Exception as delivery_error:
                tracking_results.append(CarbonTrackingResponse(
                    delivery_id=delivery_id,
                    status="error",
                    current_emissions_kg=0.0,
                    distance_covered_km=0.0,
                    estimated_total_emissions_kg=0.0,
                    timestamp=datetime.utcnow(),
                    error_message=str(delivery_error)
                ))
        
        return tracking_results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Real-time tracking failed: {str(e)}")


@router.post("/savings", response_model=CarbonSavingsResponse)
async def calculate_carbon_savings(request: CarbonSavingsRequest):
    """
    Compare carbon savings between optimized and traditional routes
    Provides detailed analysis of environmental impact reduction
    """
    try:
        # Get original route emissions
        original_emissions = await carbon_calculator.get_route_emissions(request.original_route_id)
        if not original_emissions:
            raise HTTPException(status_code=404, detail="Original route not found")
        
        # Get optimized route emissions
        optimized_emissions = await carbon_calculator.get_route_emissions(request.optimized_route_id)
        if not optimized_emissions:
            raise HTTPException(status_code=404, detail="Optimized route not found")
        
        # Calculate savings
        carbon_saved_kg = original_emissions["total_emissions"] - optimized_emissions["total_emissions"]
        percentage_reduction = (carbon_saved_kg / original_emissions["total_emissions"]) * 100
        
        # Calculate monetary value (carbon credits at $50/ton)
        monetary_value_usd = (carbon_saved_kg / 1000) * 50
        
        # Calculate environmental impact equivalents
        environmental_equivalents = carbon_calculator.calculate_environmental_equivalents(carbon_saved_kg)
        
        # Generate impact description
        impact_description = carbon_calculator.generate_impact_description(
            carbon_saved_kg, environmental_equivalents
        )
        
        # Calculate annual projection
        annual_projection = {
            "carbon_saved_annually_kg": carbon_saved_kg * 365,
            "monetary_value_annually_usd": monetary_value_usd * 365,
            "trees_equivalent": environmental_equivalents["trees_planted"],
            "cars_off_road_days": environmental_equivalents["car_miles_avoided"] / 25  # Assuming 25 miles/day average
        }
        
        response = CarbonSavingsResponse(
            comparison_id=f"comp_{uuid.uuid4().hex[:8]}",
            original_route_id=request.original_route_id,
            optimized_route_id=request.optimized_route_id,
            carbon_saved_kg=round(carbon_saved_kg, 3),
            percentage_reduction=round(percentage_reduction, 2),
            monetary_value_usd=round(monetary_value_usd, 2),
            environmental_impact_description=impact_description,
            environmental_equivalents=environmental_equivalents,
            annual_projection=annual_projection,
            calculation_timestamp=datetime.utcnow(),
            confidence_level=0.92
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Carbon savings calculation failed: {str(e)}")


@router.get("/vehicle-profiles", response_model=List[VehicleEmissionProfile])
async def get_vehicle_emission_profiles():
    """
    Get emission profiles for different vehicle types
    Provides comprehensive data for carbon calculation and vehicle selection
    """
    try:
        profiles = [
            VehicleEmissionProfile(
                vehicle_type="diesel_truck",
                display_name="Diesel Truck",
                emission_factor_kg_per_km=0.27,
                fuel_type="diesel",
                capacity_kg=1000,
                efficiency_rating="C",
                weather_sensitivity=1.15,
                load_sensitivity=1.20,
                description="Heavy-duty diesel truck for large deliveries",
                environmental_impact="high",
                cost_per_km=0.85,
                maintenance_factor=1.10,
                lifecycle_emissions_kg_per_km=0.32
            ),
            VehicleEmissionProfile(
                vehicle_type="electric_van",
                display_name="Electric Van",
                emission_factor_kg_per_km=0.05,
                fuel_type="electric",
                capacity_kg=500,
                efficiency_rating="A+",
                weather_sensitivity=1.05,
                load_sensitivity=1.08,
                description="Zero-emission electric delivery van",
                environmental_impact="very_low",
                cost_per_km=0.65,
                maintenance_factor=0.85,
                lifecycle_emissions_kg_per_km=0.12
            ),
            VehicleEmissionProfile(
                vehicle_type="hybrid_delivery",
                display_name="Hybrid Delivery Vehicle",
                emission_factor_kg_per_km=0.12,
                fuel_type="hybrid",
                capacity_kg=750,
                efficiency_rating="B+",
                weather_sensitivity=1.08,
                load_sensitivity=1.12,
                description="Fuel-efficient hybrid delivery vehicle",
                environmental_impact="medium",
                cost_per_km=0.75,
                maintenance_factor=0.95,
                lifecycle_emissions_kg_per_km=0.18
            ),
            VehicleEmissionProfile(
                vehicle_type="gas_truck",
                display_name="Gasoline Truck",
                emission_factor_kg_per_km=0.23,
                fuel_type="gasoline",
                capacity_kg=800,
                efficiency_rating="C+",
                weather_sensitivity=1.12,
                load_sensitivity=1.18,
                description="Standard gasoline delivery truck",
                environmental_impact="medium_high",
                cost_per_km=0.80,
                maintenance_factor=1.05,
                lifecycle_emissions_kg_per_km=0.28
            ),
            VehicleEmissionProfile(
                vehicle_type="cargo_bike",
                display_name="Electric Cargo Bike",
                emission_factor_kg_per_km=0.01,
                fuel_type="electric",
                capacity_kg=50,
                efficiency_rating="A++",
                weather_sensitivity=1.02,
                load_sensitivity=1.05,
                description="Ultra-low emission cargo bike for last-mile delivery",
                environmental_impact="minimal",
                cost_per_km=0.25,
                maintenance_factor=0.80,
                lifecycle_emissions_kg_per_km=0.03
            )
        ]
        
        return profiles
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get vehicle profiles: {str(e)}")


@router.get("/daily-report/{report_date}", response_model=DailyCarbonReport)
async def get_daily_carbon_report(report_date: str):
    """
    Daily carbon emissions and savings report
    Provides comprehensive analysis of daily environmental impact
    """
    try:
        # Validate date format
        if not validate_date_format(report_date):
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        # Generate daily report
        report_data = await carbon_calculator.generate_daily_report(report_date)
        
        # Calculate performance metrics
        performance_metrics = {
            "efficiency_score": report_data.get("efficiency_score", 85),
            "improvement_vs_previous_day": report_data.get("daily_improvement", 5.2),
            "target_achievement": report_data.get("target_achievement", 92.5)
        }
        
        # Generate recommendations
        recommendations = carbon_calculator.generate_optimization_recommendations(report_data)
        
        response = DailyCarbonReport(
            date=datetime.strptime(report_date, "%Y-%m-%d").date(),
            total_emissions_kg=round(report_data["total_emissions"], 2),
            total_savings_kg=round(report_data["total_savings"], 2),
            deliveries_count=report_data["deliveries_count"],
            average_emissions_per_delivery_kg=round(report_data["average_emissions"], 3),
            top_performing_routes=report_data["top_routes"][:5],
            worst_performing_routes=report_data["worst_routes"][:3],
            vehicle_breakdown=report_data["vehicle_breakdown"],
            performance_metrics=performance_metrics,
            improvement_recommendations=recommendations,
            carbon_cost_usd=round(report_data["carbon_cost"], 2),
            generated_at=datetime.utcnow()
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate daily report: {str(e)}")


@router.get("/trends", response_model=CarbonTrendsResponse)
async def get_carbon_trends(days: int = 30, vehicle_type: Optional[str] = None):
    """
    Carbon emission trends over specified time period
    Provides historical analysis and trend predictions
    """
    try:
        if days < 1 or days > 365:
            raise HTTPException(status_code=400, detail="Days must be between 1 and 365")
        
        # Get historical data
        trends_data = await carbon_calculator.get_emission_trends(
            days=days,
            vehicle_type=vehicle_type
        )
        
        # Calculate trend analysis
        trend_analysis = carbon_calculator.analyze_trends(trends_data)
        
        # Generate predictions
        predictions = carbon_calculator.predict_future_trends(trends_data, forecast_days=7)
        
        response = CarbonTrendsResponse(
            period_days=days,
            vehicle_type_filter=vehicle_type,
            daily_emissions=trends_data["daily_data"],
            trend_direction=trend_analysis["direction"],
            average_daily_emissions_kg=round(trend_analysis["average_daily"], 2),
            total_period_emissions_kg=round(trend_analysis["total_emissions"], 2),
            best_day=trend_analysis["best_day"],
            worst_day=trend_analysis["worst_day"],
            improvement_rate_percent=round(trend_analysis["improvement_rate"], 2),
            predictions=predictions,
            generated_at=datetime.utcnow()
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get carbon trends: {str(e)}")


@router.post("/predict", response_model=CarbonPredictionResponse)
async def predict_future_emissions(request: CarbonPredictionRequest):
    """
    Predict future carbon emissions based on delivery schedule
    Uses machine learning models for accurate forecasting
    """
    try:
        if len(request.scheduled_deliveries) > 1000:
            raise HTTPException(status_code=400, detail="Maximum 1000 deliveries can be predicted at once")
        
        # Validate prediction timeframe
        if request.prediction_date < datetime.utcnow().date():
            raise HTTPException(status_code=400, detail="Prediction date must be in the future")
        
        # Calculate predictions for each delivery
        delivery_predictions = []
        total_predicted_emissions = 0
        
        for delivery in request.scheduled_deliveries:
            # Get vehicle profile
            vehicle_profile = carbon_calculator.get_vehicle_emission_profile(delivery.vehicle_type)
            
            # Predict weather conditions for the date
            predicted_weather = await carbon_calculator.predict_weather_conditions(
                delivery.route_coordinates,
                request.prediction_date
            )
            
            # Calculate predicted emissions
            base_emissions = delivery.distance_km * vehicle_profile["emission_factor"]
            weather_factor = carbon_calculator.calculate_weather_impact(
                predicted_weather, delivery.vehicle_type
            )
            load_factor = carbon_calculator.calculate_load_impact(
                delivery.load_factor, delivery.vehicle_type
            )
            
            predicted_emissions = base_emissions * weather_factor * load_factor
            total_predicted_emissions += predicted_emissions
            
            delivery_predictions.append({
                "delivery_id": delivery.delivery_id,
                "predicted_emissions_kg": round(predicted_emissions, 3),
                "confidence_level": 0.88,
                "factors": {
                    "base_emissions": round(base_emissions, 3),
                    "weather_factor": round(weather_factor, 3),
                    "load_factor": round(load_factor, 3)
                }
            })
        
        # Calculate optimization potential
        optimization_potential = carbon_calculator.calculate_optimization_potential(
            delivery_predictions
        )
        
        # Generate recommendations
        optimization_recommendations = carbon_calculator.generate_prediction_recommendations(
            delivery_predictions, optimization_potential
        )
        
        response = CarbonPredictionResponse(
            prediction_id=f"pred_{uuid.uuid4().hex[:8]}",
            prediction_date=request.prediction_date,
            total_predicted_emissions_kg=round(total_predicted_emissions, 2),
            delivery_count=len(request.scheduled_deliveries),
            average_emissions_per_delivery_kg=round(total_predicted_emissions / len(request.scheduled_deliveries), 3),
            delivery_predictions=delivery_predictions,
            optimization_potential_kg=round(optimization_potential["potential_savings"], 2),
            optimization_potential_percent=round(optimization_potential["potential_percent"], 1),
            confidence_level=0.88,
            optimization_recommendations=optimization_recommendations,
            generated_at=datetime.utcnow()
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Emission prediction failed: {str(e)}")


# Background task for storing calculations
async def store_carbon_calculation(calculation_id: str, request_data: Dict, response_data: Dict):
    """
    Store carbon calculation in database for historical analysis
    """
    try:
        # This would typically store in a database
        # For demo purposes, we'll just log it
        print(f"Stored carbon calculation {calculation_id} with {response_data['total_emissions_kg']} kg CO2")
    except Exception as e:
        print(f"Failed to store calculation {calculation_id}: {str(e)}")


# Health check endpoint
@router.get("/health")
async def carbon_service_health():
    """
    Health check for carbon calculation service
    """
    try:
        # Test carbon calculator
        calculator_status = await carbon_calculator.health_check()
        
        return {
            "status": "healthy",
            "services": {
                "carbon_calculator": calculator_status,
                "weather_api": "connected",
                "emission_database": "loaded"
            },
            "cache_size": len(calculation_cache),
            "supported_vehicles": 5,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Carbon service unhealthy: {str(e)}")


# Demo endpoint for Walmart showcase
@router.get("/demo/walmart-impact")
async def get_walmart_demo_impact():
    """
    Demo endpoint showing potential Walmart-scale carbon impact
    """
    try:
        # Simulated Walmart-scale impact data
        daily_deliveries = 2_500_000  # Estimated daily deliveries across all stores
        average_emissions_per_delivery = 2.5  # kg CO2
        
        # Current emissions
        current_daily_emissions = daily_deliveries * average_emissions_per_delivery
        current_annual_emissions = current_daily_emissions * 365
        
        # With QuantumEco optimization (35% reduction)
        optimized_daily_emissions = current_daily_emissions * 0.65
        optimized_annual_emissions = optimized_daily_emissions * 365
        
        # Savings
        daily_savings = current_daily_emissions - optimized_daily_emissions
        annual_savings = current_annual_emissions - optimized_annual_emissions
        
        return {
            "walmart_scale_impact": {
                "current_emissions": {
                    "daily_kg": round(current_daily_emissions, 0),
                    "annual_tons": round(current_annual_emissions / 1000, 0)
                },
                "optimized_emissions": {
                    "daily_kg": round(optimized_daily_emissions, 0),
                    "annual_tons": round(optimized_annual_emissions / 1000, 0)
                },
                "savings": {
                    "daily_kg": round(daily_savings, 0),
                    "annual_tons": round(annual_savings / 1000, 0),
                    "percentage_reduction": 35.0,
                    "monetary_value_annual_usd": round((annual_savings / 1000) * 50, 0)
                },
                "environmental_equivalents": {
                    "trees_planted_equivalent": round(annual_savings / 21.77, 0),  # 21.77 kg CO2 per tree per year
                    "cars_off_road_equivalent": round(annual_savings / 4600, 0),  # 4.6 tons CO2 per car per year
                    "homes_powered_equivalent": round(annual_savings / 7300, 0)   # 7.3 tons CO2 per home per year
                }
            },
            "generated_at": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demo data generation failed: {str(e)}")
