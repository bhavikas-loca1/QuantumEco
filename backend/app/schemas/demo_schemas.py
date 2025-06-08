
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator

from app.schemas.route_schemas import OptimizationGoals


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


class DemoComplexity(str, Enum):
    """Enumeration for demo complexity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class OptimizationType(str, Enum):
    """Enumeration for optimization types"""
    TRADITIONAL = "traditional"
    QUANTUM_INSPIRED = "quantum_inspired"
    HYBRID = "hybrid"

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
    special_requirements: Optional[List[str]] = Field(default=[], description="Special requirements")

class VehicleAssignment(BaseModel):
    """Vehicle assignment for demo scenarios"""
    vehicle_id: str = Field(..., description="Vehicle identifier")
    vehicle_type: str = Field(..., description="Vehicle type")
    capacity_kg: float = Field(..., description="Vehicle capacity")
    cost_per_km: float = Field(..., description="Cost per kilometer")
    emission_factor: float = Field(..., description="Emission factor")
    assigned_locations: List[str] = Field(..., description="Assigned location IDs")
    route_distance_km: Optional[float] = Field(None, description="Total route distance")
    route_time_minutes: Optional[float] = Field(None, description="Total route time")
    utilization_percent: Optional[float] = Field(None, description="Vehicle utilization")

class OptimizationResult(BaseModel):
    """Optimization result for demo scenarios"""
    method: OptimizationType = Field(..., description="Optimization method")
    total_cost: float = Field(..., description="Total cost")
    total_carbon: float = Field(..., description="Total carbon emissions")
    total_time: float = Field(..., description="Total time")
    total_distance: float = Field(..., description="Total distance")
    routes: List[Dict[str, Any]] = Field(..., description="Route details")
    processing_time: float = Field(..., description="Processing time")
    optimization_score: Optional[float] = Field(None, description="Optimization quality score")
    convergence_iterations: Optional[int] = Field(None, description="Iterations to convergence")

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
    complexity_level: DemoComplexity = Field(..., description="Scenario complexity")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Generation timestamp")

class DemoGenerationRequest(BaseModel):
    """Request for generating custom demo data"""
    num_locations: int = Field(..., ge=5, le=200, description="Number of locations")
    num_vehicles: int = Field(..., ge=1, le=20, description="Number of vehicles")
    area: str = Field(..., description="Geographic area")
    location_density: str = Field(default="urban", description="Location density")
    vehicle_types: List[str] = Field(..., description="Vehicle types to include")
    capacity_range: Dict[str, int] = Field(..., description="Vehicle capacity range")
    optimization_goals: Dict[str, float] = Field(..., description="Optimization goals")
    include_weather_factors: bool = Field(default=True, description="Include weather factors")
    include_traffic_factors: bool = Field(default=True, description="Include traffic factors")
    complexity_level: DemoComplexity = Field(default=DemoComplexity.MEDIUM, description="Desired complexity")
    
    @validator('num_locations')
    def validate_locations_vehicles_ratio(cls, v, values):
        """Validate locations to vehicles ratio is reasonable"""
        if 'num_vehicles' in values and v < values['num_vehicles']:
            raise ValueError('Number of locations must be >= number of vehicles')
        return v

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
    competitive_advantages: Dict[str, float] = Field(..., description="Competitive advantages")
    environmental_impact: Dict[str, float] = Field(..., description="Environmental impact metrics")
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
    real_time_factors: Dict[str, Any] = Field(..., description="Real-time factors considered")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Generation timestamp")

class ScenarioSummary(BaseModel):
    """Summary of a demo scenario"""
    scenario_id: str = Field(..., description="Scenario identifier")
    name: str = Field(..., description="Scenario name")
    description: str = Field(..., description="Brief description")
    complexity: DemoComplexity = Field(..., description="Complexity level")
    estimated_savings: Dict[str, float] = Field(..., description="Estimated savings percentages")
    locations_count: int = Field(..., description="Number of locations")
    vehicles_count: int = Field(..., description="Number of vehicles")
    optimization_type: OptimizationType = Field(..., description="Optimization type")
    featured: bool = Field(default=False, description="Whether scenario is featured")

class ScenarioListResponse(BaseModel):
    """List of available demo scenarios"""
    scenarios: List[ScenarioSummary] = Field(..., description="Available scenarios")
    total_scenarios: int = Field(..., description="Total number of scenarios")
    featured_scenario: str = Field(..., description="Featured scenario ID")
    categories: List[str] = Field(..., description="Available scenario categories")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
