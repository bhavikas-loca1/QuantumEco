
from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel, Field

from backend.app.schemas.route_schemas import OptimizationGoals


class LocationData(BaseModel):
    """Location data for demo scenarios"""
    id: str = Field(..., description="Location identifier")
    name: str = Field(..., description="Location name")
    address: str = Field(..., description="Location address")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    demand_kg: float = Field(..., ge=0, description="Demand in kg")
    priority: int = Field(..., ge=1, le=5, description="Priority level")
    time_window_start: str = Field(..., description="Time window start")
    time_window_end: str = Field(..., description="Time window end")
    delivery_type: str = Field(..., description="Delivery type")

class VehicleAssignment(BaseModel):
    """Vehicle assignment for demo scenarios"""
    vehicle_id: str = Field(..., description="Vehicle identifier")
    vehicle_type: str = Field(..., description="Vehicle type")
    capacity_kg: float = Field(..., description="Vehicle capacity")
    cost_per_km: float = Field(..., description="Cost per kilometer")
    emission_factor: float = Field(..., description="Emission factor")
    assigned_locations: List[str] = Field(..., description="Assigned location IDs")

class OptimizationResult(BaseModel):
    """Optimization result for demo scenarios"""
    method: str = Field(..., description="Optimization method")
    total_cost: float = Field(..., description="Total cost")
    total_carbon: float = Field(..., description="Total carbon emissions")
    total_time: float = Field(..., description="Total time")
    total_distance: float = Field(..., description="Total distance")
    routes: List[Dict[str, Any]] = Field(..., description="Route details")
    processing_time: float = Field(..., description="Processing time")

class DemoScenarioResponse(BaseModel):
    """Demo scenario response"""
    scenario_id: str = Field(..., description="Scenario identifier")
    scenario_name: str = Field(..., description="Scenario name")
    description: str = Field(..., description="Scenario description")
    locations: List[LocationData] = Field(..., description="Scenario locations")
    vehicles: List[Dict[str, Any]] = Field(..., description="Scenario vehicles")
    optimization_result: OptimizationResult = Field(..., description="Optimization result")
    performance_metrics: Dict[str, Any] = Field(..., description="Performance metrics")
    recommendations: List[str] = Field(..., description="Optimization recommendations")
    generation_parameters: Dict[str, Any] = Field(..., description="Generation parameters")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Generation timestamp")

class DemoGenerationRequest(BaseModel):
    """Request for generating custom demo data"""
    num_locations: int = Field(..., ge=5, le=200, description="Number of locations")
    num_vehicles: int = Field(..., ge=1, le=20, description="Number of vehicles")
    area: str = Field(..., description="Geographic area")
    location_density: str = Field(default="urban", description="Location density")
    vehicle_types: List[str] = Field(..., description="Vehicle types to include")
    capacity_range: Dict[str, int] = Field(..., description="Vehicle capacity range")
    optimization_goals: OptimizationGoals = Field(default_factory=OptimizationGoals, description="Optimization goals")
    include_weather_factors: bool = Field(default=True, description="Include weather factors")
    include_traffic_factors: bool = Field(default=True, description="Include traffic factors")

class PerformanceShowcaseResponse(BaseModel):
    """Performance showcase for demo presentation"""
    showcase_title: str = Field(..., description="Showcase title")
    key_achievements: Dict[str, Any] = Field(..., description="Key achievements")
    roi_analysis: Dict[str, Any] = Field(..., description="ROI analysis")
    market_impact: Dict[str, Any] = Field(..., description="Market impact")
    technology_highlights: List[str] = Field(..., description="Technology highlights")
    demo_scenarios_available: int = Field(..., description="Number of demo scenarios")
    total_optimizations_simulated: int = Field(..., description="Total optimizations simulated")
    blockchain_certificates_generated: int = Field(..., description="Blockchain certificates generated")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Generation timestamp")

class WalmartNYCResponse(BaseModel):
    """Walmart NYC demo scenario response"""
    scenario_id: str = Field(..., description="Scenario identifier")
    scenario_name: str = Field(..., description="Scenario name")
    description: str = Field(..., description="Scenario description")
    locations: List[LocationData] = Field(..., description="NYC delivery locations")
    vehicles: List[Dict[str, Any]] = Field(..., description="Vehicle fleet")
    traditional_optimization: OptimizationResult = Field(..., description="Traditional optimization results")
    quantum_optimization: OptimizationResult = Field(..., description="Quantum optimization results")
    savings_analysis: Dict[str, Any] = Field(..., description="Savings analysis")
    blockchain_certificates: List[Dict[str, Any]] = Field(..., description="Blockchain certificates")
    environmental_impact: Dict[str, Any] = Field(..., description="Environmental impact")
    walmart_scale_projection: Dict[str, Any] = Field(..., description="Walmart scale projection")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Generation timestamp")

class ScenarioListResponse(BaseModel):
    """List of available demo scenarios"""
    scenarios: List[Dict[str, Any]] = Field(..., description="Available scenarios")
    total_scenarios: int = Field(..., description="Total number of scenarios")
    featured_scenario: str = Field(..., description="Featured scenario ID")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
