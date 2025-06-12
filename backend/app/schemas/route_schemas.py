from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime, time
from enum import Enum

class DeliveryType(str, Enum):
    """Enumeration for delivery types"""
    STANDARD = "standard"
    EXPRESS = "express"
    SAME_DAY = "same_day"
    SCHEDULED = "scheduled"

class VehicleType(str, Enum):
    """Enumeration for vehicle types"""
    DIESEL_TRUCK = "diesel_truck"
    ELECTRIC_VAN = "electric_van"
    HYBRID_DELIVERY = "hybrid_delivery"
    GAS_TRUCK = "gas_truck"
    CARGO_BIKE = "cargo_bike"

class OptimizationStatus(str, Enum):
    """Enumeration for optimization status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class Location(BaseModel):
    """Delivery location with coordinates, time windows, and priority"""
    id: str = Field(..., description="Unique identifier for the location")
    name: Optional[str] = Field(None, description="Human-readable name for the location")
    address: str = Field(..., description="Full address of the location")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate (-90 to 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate (-180 to 180)")
    demand_kg: float = Field(default=0, ge=0, le=2000, description="Delivery demand in kilograms")
    priority: int = Field(default=1, ge=1, le=5, description="Delivery priority (1=lowest, 5=highest)")
    time_window_start: Optional[str] = Field(None, description="Delivery window start time (HH:MM format)")
    time_window_end: Optional[str] = Field(None, description="Delivery window end time (HH:MM format)")
    delivery_type: DeliveryType = Field(default=DeliveryType.STANDARD, description="Type of delivery")
    special_requirements: Optional[List[str]] = Field(default=[], description="Special delivery requirements")
    contact_info: Optional[str] = Field(None, description="Contact information for delivery")
    
    @validator('time_window_start', 'time_window_end')
    def validate_time_format(cls, v):
        """Validate time format is HH:MM"""
        if v is not None:
            try:
                time.fromisoformat(v)
            except ValueError:
                raise ValueError('Time must be in HH:MM format')
        return v
    
    @validator('longitude')
    def validate_longitude(cls, v):
        """Additional longitude validation"""
        if not -180 <= v <= 180:
            raise ValueError('Longitude must be between -180 and 180 degrees')
        return v
    
    @validator('latitude')
    def validate_latitude(cls, v):
        """Additional latitude validation"""
        if not -90 <= v <= 90:
            raise ValueError('Latitude must be between -90 and 90 degrees')
        return v

class Vehicle(BaseModel):
    """Vehicle profile with capacity, emission factor, and cost parameters"""
    id: str = Field(..., description="Unique identifier for the vehicle")
    type: VehicleType = Field(..., description="Type of vehicle")
    capacity_kg: float = Field(..., gt=0, le=5000, description="Vehicle capacity in kilograms")
    cost_per_km: float = Field(..., gt=0, le=10, description="Operating cost per kilometer")
    emission_factor: float = Field(..., ge=0, le=1, description="CO2 emission factor (kg per km)")
    max_range_km: Optional[float] = Field(default=500, gt=0, description="Maximum range in kilometers")
    driver_id: Optional[str] = Field(None, description="Assigned driver identifier")
    current_location: Optional[Location] = Field(None, description="Current vehicle location")
    availability_start: Optional[str] = Field(default="08:00", description="Vehicle availability start time")
    availability_end: Optional[str] = Field(default="18:00", description="Vehicle availability end time")
    fuel_level: Optional[float] = Field(default=1.0, ge=0, le=1, description="Current fuel level (0-1)")
    maintenance_due: Optional[datetime] = Field(None, description="Next maintenance due date")
    
    @validator('availability_start', 'availability_end')
    def validate_availability_time(cls, v):
        """Validate availability time format"""
        if v is not None:
            try:
                time.fromisoformat(v)
            except ValueError:
                raise ValueError('Availability time must be in HH:MM format')
        return v

class OptimizationGoals(BaseModel):
    """Optimization goals and weights"""
    cost: float = Field(default=0.4, ge=0, le=1, description="Cost optimization weight")
    carbon: float = Field(default=0.4, ge=0, le=1, description="Carbon emission optimization weight")
    time: float = Field(default=0.2, ge=0, le=1, description="Time optimization weight")
    
    @validator('cost', 'carbon', 'time')
    def validate_weights_sum(cls, v, values):
        """Ensure weights sum to approximately 1.0"""
        if 'cost' in values and 'carbon' in values:
            total = values['cost'] + values['carbon'] + v
            if abs(total - 1.0) > 0.01:  # Allow small floating point errors
                raise ValueError('Optimization weights must sum to 1.0')
        return v

class RouteConstraints(BaseModel):
    """Route optimization constraints"""
    max_distance_per_vehicle: Optional[float] = Field(default=500, gt=0, description="Maximum distance per vehicle (km)")
    max_time_per_vehicle: Optional[float] = Field(default=480, gt=0, description="Maximum time per vehicle (minutes)")
    max_locations_per_vehicle: Optional[int] = Field(default=50, gt=0, description="Maximum locations per vehicle")
    require_return_to_depot: bool = Field(default=True, description="Vehicles must return to starting depot")
    allow_split_deliveries: bool = Field(default=False, description="Allow splitting deliveries across vehicles")
    respect_time_windows: bool = Field(default=True, description="Respect delivery time windows")

class RouteOptimizationRequest(BaseModel):
    """Complete optimization request with goals and constraints"""
    request_id: Optional[str] = Field(None, description="Unique request identifier")
    locations: List[Location] = Field(..., min_items=2, max_items=100, description="List of delivery locations")
    vehicles: List[Vehicle] = Field(..., min_items=1, max_items=20, description="List of available vehicles")
    optimization_goals: OptimizationGoals = Field(default_factory=OptimizationGoals, description="Optimization objectives")
    constraints: Optional[RouteConstraints] = Field(default_factory=RouteConstraints, description="Route constraints")
    traffic_enabled: bool = Field(default=True, description="Consider real-time traffic data")
    weather_enabled: bool = Field(default=True, description="Consider weather impact on routes")
    create_certificate: bool = Field(default=True, description="Create blockchain certificate for results")
    optimization_timeout: int = Field(default=30, ge=5, le=300, description="Optimization timeout in seconds")
    algorithm_preference: Optional[str] = Field(default="quantum_inspired", description="Preferred optimization algorithm")
    
    @validator('locations')
    def validate_locations_count(cls, v):
        """Validate locations count is within limits"""
        if len(v) < 2:
            raise ValueError('At least 2 locations are required for optimization')
        if len(v) > 100:
            raise ValueError('Maximum 100 locations allowed per request')
        return v
    
    @validator('vehicles')
    def validate_vehicles_count(cls, v):
        """Validate vehicles count is within limits"""
        if len(v) < 1:
            raise ValueError('At least 1 vehicle is required for optimization')
        if len(v) > 20:
            raise ValueError('Maximum 20 vehicles allowed per request')
        return v

class RouteSegment(BaseModel):
    """Individual route segment between two locations"""
    from_location_id: str = Field(..., description="Starting location ID")
    to_location_id: str = Field(..., description="Destination location ID")
    distance_km: float = Field(..., ge=0, description="Segment distance in kilometers")
    travel_time_minutes: float = Field(..., ge=0, description="Travel time in minutes")
    carbon_emissions_kg: float = Field(..., ge=0, description="Carbon emissions for this segment")
    estimated_arrival: Optional[str] = Field(None, description="Estimated arrival time")
    traffic_factor: Optional[float] = Field(default=1.0, description="Traffic impact factor")
    weather_factor: Optional[float] = Field(default=1.0, description="Weather impact factor")

class OptimizedRoute(BaseModel):
    """Optimized route with performance metrics and geometry"""
    route_id: str = Field(..., description="Unique route identifier")
    vehicle_id: str = Field(..., description="Assigned vehicle ID")
    vehicle_type: VehicleType = Field(..., description="Type of assigned vehicle")
    locations: List[Location] = Field(..., description="Ordered list of locations in route")
    route_segments: List[RouteSegment] = Field(..., description="Detailed route segments")
    total_distance_km: float = Field(..., ge=0, description="Total route distance")
    total_time_minutes: float = Field(..., ge=0, description="Total route time")
    total_cost: float = Field(..., ge=0, description="Total route cost")
    total_carbon_kg: float = Field(..., ge=0, description="Total carbon emissions")
    load_utilization_percent: float = Field(..., ge=0, le=100, description="Vehicle load utilization percentage")
    route_geometry: Optional[List[List[float]]] = Field(None, description="Route polyline coordinates [[lat, lng], ...]")
    optimization_score: float = Field(..., ge=0, le=100, description="Route optimization quality score")
    estimated_start_time: Optional[str] = Field(None, description="Estimated route start time")
    estimated_end_time: Optional[str] = Field(None, description="Estimated route completion time")
    special_instructions: Optional[List[str]] = Field(default=[], description="Special route instructions")

class SavingsAnalysis(BaseModel):
    """Analysis of savings compared to baseline/traditional routing"""
    cost_saved_usd: float = Field(..., description="Cost savings in USD")
    cost_improvement_percent: float = Field(..., description="Cost improvement percentage")
    carbon_saved_kg: float = Field(..., description="Carbon emissions saved in kg")
    carbon_improvement_percent: float = Field(..., description="Carbon improvement percentage")
    time_saved_minutes: float = Field(..., description="Time savings in minutes")
    time_improvement_percent: float = Field(..., description="Time improvement percentage")
    distance_saved_km: float = Field(..., description="Distance savings in kilometers")
    distance_improvement_percent: float = Field(..., description="Distance improvement percentage")
    efficiency_score: float = Field(..., ge=0, le=100, description="Overall efficiency improvement score")

class RouteOptimizationResponse(BaseModel):
    """Full optimization results with savings analysis"""
    optimization_id: str = Field(..., description="Unique optimization identifier")
    request_id: Optional[str] = Field(None, description="Original request identifier")
    status: OptimizationStatus = Field(..., description="Optimization status")
    optimized_routes: List[OptimizedRoute] = Field(..., description="List of optimized routes")
    total_distance_km: float = Field(..., ge=0, description="Total distance across all routes")
    total_time_minutes: float = Field(..., ge=0, description="Total time across all routes")
    total_cost: float = Field(..., ge=0, description="Total cost across all routes")
    total_carbon_kg: float = Field(..., ge=0, description="Total carbon emissions across all routes")
    savings_analysis: Optional[SavingsAnalysis] = Field(None, description="Savings compared to baseline")
    method: str = Field(default="quantum_inspired", description="Optimization method used")
    processing_time: float = Field(..., ge=0, description="Time taken for optimization")
    quantum_improvement_score: Optional[float] = Field(None, ge=0, le=100, description="Quantum algorithm improvement score")
    certificates: Optional[List[str]] = Field(default=[], description="Generated blockchain certificate IDs")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Optimization completion timestamp")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Additional optimization metadata")
    
    @validator('optimized_routes')
    def validate_routes_not_empty(cls, v):
        """Ensure at least one route is returned for successful optimization"""
        if not v:
            raise ValueError('At least one optimized route must be provided')
        return v

class BatchOptimizationRequest(BaseModel):
    """Request for optimizing multiple scenarios simultaneously"""
    batch_id: Optional[str] = Field(None, description="Unique batch identifier")
    scenarios: List[RouteOptimizationRequest] = Field(..., min_items=1, max_items=10, description="List of optimization scenarios")
    parallel_processing: bool = Field(default=True, description="Enable parallel processing of scenarios")
    compare_results: bool = Field(default=True, description="Compare results across scenarios")
    
    @validator('scenarios')
    def validate_scenarios_count(cls, v):
        """Validate scenarios count is within limits"""
        if len(v) > 10:
            raise ValueError('Maximum 10 scenarios allowed per batch request')
        return v

class BatchOptimizationResponse(BaseModel):
    """Response for batch optimization with multiple scenario results"""
    batch_id: str = Field(..., description="Unique batch identifier")
    status: OptimizationStatus = Field(..., description="Overall batch status")
    scenarios: List[RouteOptimizationResponse] = Field(..., description="Results for each scenario")
    best_scenario_id: Optional[str] = Field(None, description="ID of the best performing scenario")
    total_processing_time: float = Field(..., ge=0, description="Total processing time for batch")
    successful_optimizations: int = Field(..., ge=0, description="Number of successful optimizations")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Batch completion timestamp")

class RouteComparisonRequest(BaseModel):
    """Request for comparing different optimization methods"""
    locations: List[Location] = Field(..., min_items=2, max_items=100, description="Locations for comparison")
    vehicles: List[Vehicle] = Field(..., min_items=1, max_items=20, description="Vehicles for comparison")
    optimization_goals: OptimizationGoals = Field(default_factory=OptimizationGoals, description="Optimization goals")
    methods_to_compare: List[str] = Field(default=["traditional", "quantum_inspired"], description="Methods to compare")

class MethodResult(BaseModel):
    """Results for a specific optimization method"""
    method: str = Field(..., description="Optimization method name")
    total_cost: float = Field(..., ge=0, description="Total cost")
    total_time_minutes: float = Field(..., ge=0, description="Total time")
    total_distance_km: float = Field(..., ge=0, description="Total distance")
    total_carbon_kg: float = Field(..., ge=0, description="Total carbon emissions")
    routes: List[OptimizedRoute] = Field(..., description="Optimized routes")
    processing_time: float = Field(..., ge=0, description="Processing time")
    quality_score: float = Field(..., ge=0, le=100, description="Solution quality score")

class RouteComparisonResponse(BaseModel):
    """Response comparing different optimization methods"""
    comparison_id: str = Field(..., description="Unique comparison identifier")
    quantum_inspired_result: MethodResult = Field(..., description="Quantum-inspired optimization results")
    traditional_result: MethodResult = Field(..., description="Traditional optimization results")
    improvements: Dict[str, float] = Field(..., description="Improvement percentages")
    winner: str = Field(..., description="Best performing method")
    total_comparison_time_seconds: float = Field(..., ge=0, description="Total comparison time")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Comparison completion timestamp")

class RouteRecalculationRequest(BaseModel):
    """Request for real-time route recalculation"""
    route_id: str = Field(..., description="Route ID to recalculate")
    affected_locations: List[str] = Field(..., description="Location IDs affected by changes")
    reason: str = Field(..., description="Reason for recalculation (traffic, weather, etc.)")
    current_conditions: Optional[Dict[str, Any]] = Field(default={}, description="Current traffic/weather conditions")
    priority: int = Field(default=1, ge=1, le=5, description="Recalculation priority")

class RouteDetailsResponse(BaseModel):
    """Detailed information about a specific route"""
    route_id: str = Field(..., description="Route identifier")
    optimization_data: Dict[str, Any] = Field(..., description="Complete optimization data")
    route_analytics: Dict[str, Any] = Field(..., description="Route performance analytics")
    carbon_analysis: Dict[str, Any] = Field(..., description="Detailed carbon emission analysis")
    blockchain_certificate: Optional[str] = Field(None, description="Associated blockchain certificate ID")
    last_updated: datetime = Field(..., description="Last update timestamp")

class VehicleProfileResponse(BaseModel):
    """Vehicle profile information for selection"""
    vehicle_type: VehicleType = Field(..., description="Vehicle type")
    display_name: str = Field(..., description="Human-readable vehicle name")
    capacity_kg: float = Field(..., gt=0, description="Vehicle capacity")
    max_range_km: float = Field(..., gt=0, description="Maximum range")
    cost_per_km: float = Field(..., gt=0, description="Operating cost per km")
    emission_factor: float = Field(..., ge=0, description="Emission factor")
    fuel_type: str = Field(..., description="Fuel type")
    description: str = Field(..., description="Vehicle description")
    environmental_impact: str = Field(..., description="Environmental impact level")
    recommended_use: str = Field(..., description="Recommended use cases")

class DeliveryType(str, Enum):
    """Enumeration for delivery types"""
    STANDARD = "standard"
    EXPRESS = "express"
    SAME_DAY = "same_day"
    SCHEDULED = "scheduled"

class VehicleType(str, Enum):
    """Enumeration for vehicle types"""
    DIESEL_TRUCK = "diesel_truck"
    ELECTRIC_VAN = "electric_van"
    HYBRID_DELIVERY = "hybrid_delivery"
    GAS_TRUCK = "gas_truck"
    CARGO_BIKE = "cargo_bike"

class OptimizationStatus(str, Enum):
    """Enumeration for optimization status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class Location(BaseModel):
    """Delivery location with coordinates, time windows, and priority"""
    id: str = Field(..., description="Unique identifier for the location")
    name: Optional[str] = Field(None, description="Human-readable name for the location")
    address: str = Field(..., description="Full address of the location")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate (-90 to 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate (-180 to 180)")
    demand_kg: float = Field(default=0, ge=0, le=2000, description="Delivery demand in kilograms")
    priority: int = Field(default=1, ge=1, le=5, description="Delivery priority (1=lowest, 5=highest)")
    time_window_start: Optional[str] = Field(None, description="Delivery window start time (HH:MM format)")
    time_window_end: Optional[str] = Field(None, description="Delivery window end time (HH:MM format)")
    delivery_type: DeliveryType = Field(default=DeliveryType.STANDARD, description="Type of delivery")
    special_requirements: Optional[List[str]] = Field(default=[], description="Special delivery requirements")
    contact_info: Optional[str] = Field(None, description="Contact information for delivery")
    
    @validator('time_window_start', 'time_window_end')
    def validate_time_format(cls, v):
        """Validate time format is HH:MM"""
        if v is not None:
            try:
                time.fromisoformat(v)
            except ValueError:
                raise ValueError('Time must be in HH:MM format')
        return v

class Vehicle(BaseModel):
    """Vehicle profile with capacity, emission factor, and cost parameters"""
    id: str = Field(..., description="Unique identifier for the vehicle")
    type: VehicleType = Field(..., description="Type of vehicle")
    capacity_kg: float = Field(..., gt=0, le=5000, description="Vehicle capacity in kilograms")
    cost_per_km: float = Field(..., gt=0, le=10, description="Operating cost per kilometer")
    emission_factor: float = Field(..., ge=0, le=1, description="CO2 emission factor (kg per km)")
    max_range_km: Optional[float] = Field(default=500, gt=0, description="Maximum range in kilometers")
    driver_id: Optional[str] = Field(None, description="Assigned driver identifier")
    current_location: Optional[Location] = Field(None, description="Current vehicle location")
    availability_start: Optional[str] = Field(default="08:00", description="Vehicle availability start time")
    availability_end: Optional[str] = Field(default="18:00", description="Vehicle availability end time")
    fuel_level: Optional[float] = Field(default=1.0, ge=0, le=1, description="Current fuel level (0-1)")
    maintenance_due: Optional[datetime] = Field(None, description="Next maintenance due date")

class OptimizationGoals(BaseModel):
    """Optimization goals and weights"""
    cost: float = Field(default=0.4, ge=0, le=1, description="Cost optimization weight")
    carbon: float = Field(default=0.4, ge=0, le=1, description="Carbon emission optimization weight")
    time: float = Field(default=0.2, ge=0, le=1, description="Time optimization weight")
    
    @validator('cost', 'carbon', 'time')
    def validate_weights_sum(cls, v, values):
        """Ensure weights sum to approximately 1.0"""
        if 'cost' in values and 'carbon' in values:
            total = values['cost'] + values['carbon'] + v
            if abs(total - 1.0) > 0.01:
                raise ValueError('Optimization weights must sum to 1.0')
        return v

class RouteConstraints(BaseModel):
    """Route optimization constraints"""
    max_distance_per_vehicle: Optional[float] = Field(default=500, gt=0, description="Maximum distance per vehicle (km)")
    max_time_per_vehicle: Optional[float] = Field(default=480, gt=0, description="Maximum time per vehicle (minutes)")
    max_locations_per_vehicle: Optional[int] = Field(default=50, gt=0, description="Maximum locations per vehicle")
    require_return_to_depot: bool = Field(default=True, description="Vehicles must return to starting depot")
    allow_split_deliveries: bool = Field(default=False, description="Allow splitting deliveries across vehicles")
    respect_time_windows: bool = Field(default=True, description="Respect delivery time windows")

class RouteOptimizationRequest(BaseModel):
    """Complete optimization request with goals and constraints"""
    request_id: Optional[str] = Field(None, description="Unique request identifier")
    locations: List[Location] = Field(..., min_items=2, max_items=100, description="List of delivery locations")
    vehicles: List[Vehicle] = Field(..., min_items=1, max_items=20, description="List of available vehicles")
    optimization_goals: OptimizationGoals = Field(default_factory=OptimizationGoals, description="Optimization objectives")
    constraints: Optional[RouteConstraints] = Field(default_factory=RouteConstraints, description="Route constraints")
    traffic_enabled: bool = Field(default=True, description="Consider real-time traffic data")
    weather_enabled: bool = Field(default=True, description="Consider weather impact on routes")
    create_certificate: bool = Field(default=True, description="Create blockchain certificate for results")
    optimization_timeout: int = Field(default=30, ge=5, le=300, description="Optimization timeout in seconds")
    algorithm_preference: Optional[str] = Field(default="quantum_inspired", description="Preferred optimization algorithm")

class RouteSegment(BaseModel):
    """Individual route segment between two locations"""
    from_location_id: str = Field(..., description="Starting location ID")
    to_location_id: str = Field(..., description="Destination location ID")
    distance_km: float = Field(..., ge=0, description="Segment distance in kilometers")
    travel_time_minutes: float = Field(..., ge=0, description="Travel time in minutes")
    carbon_emissions_kg: float = Field(..., ge=0, description="Carbon emissions for this segment")
    estimated_arrival: Optional[str] = Field(None, description="Estimated arrival time")
    traffic_factor: Optional[float] = Field(default=1.0, description="Traffic impact factor")
    weather_factor: Optional[float] = Field(default=1.0, description="Weather impact factor")

class OptimizedRoute(BaseModel):
    """Optimized route with performance metrics and geometry"""
    route_id: str = Field(..., description="Unique route identifier")
    vehicle_id: str = Field(..., description="Assigned vehicle ID")
    vehicle_type: VehicleType = Field(..., description="Type of assigned vehicle")
    locations: List[Location] = Field(..., description="Ordered list of locations in route")
    route_segments: List[RouteSegment] = Field(..., description="Detailed route segments")
    total_distance_km: float = Field(..., ge=0, description="Total route distance")
    total_time_minutes: float = Field(..., ge=0, description="Total route time")
    total_cost: float = Field(..., ge=0, description="Total route cost")
    total_carbon_kg: float = Field(..., ge=0, description="Total carbon emissions")
    load_utilization_percent: float = Field(..., ge=0, le=100, description="Vehicle load utilization percentage")
    route_geometry: Optional[List[List[float]]] = Field(None, description="Route polyline coordinates [[lat, lng], ...]")
    optimization_score: float = Field(..., ge=0, le=100, description="Route optimization quality score")
    estimated_start_time: Optional[str] = Field(None, description="Estimated route start time")
    estimated_end_time: Optional[str] = Field(None, description="Estimated route completion time")
    special_instructions: Optional[List[str]] = Field(default=[], description="Special route instructions")

class SavingsAnalysis(BaseModel):
    """Analysis of savings compared to baseline/traditional routing"""
    cost_saved_usd: float = Field(..., description="Cost savings in USD")
    cost_improvement_percent: float = Field(..., description="Cost improvement percentage")
    carbon_saved_kg: float = Field(..., description="Carbon emissions saved in kg")
    carbon_improvement_percent: float = Field(..., description="Carbon improvement percentage")
    time_saved_minutes: float = Field(..., description="Time savings in minutes")
    time_improvement_percent: float = Field(..., description="Time improvement percentage")
    distance_saved_km: float = Field(..., description="Distance savings in kilometers")
    distance_improvement_percent: float = Field(..., description="Distance improvement percentage")
    efficiency_score: float = Field(..., ge=0, le=100, description="Overall efficiency improvement score")

class RouteOptimizationResponse(BaseModel):
    """Full optimization results with savings analysis"""
    optimization_id: str = Field(..., description="Unique optimization identifier")
    request_id: Optional[str] = Field(None, description="Original request identifier")
    status: OptimizationStatus = Field(..., description="Optimization status")
    optimized_routes: List[OptimizedRoute] = Field(..., description="List of optimized routes")
    total_distance_km: float = Field(..., ge=0, description="Total distance across all routes")
    total_time_minutes: float = Field(..., ge=0, description="Total time across all routes")
    total_cost: float = Field(..., ge=0, description="Total cost across all routes")
    total_carbon_kg: float = Field(..., ge=0, description="Total carbon emissions across all routes")
    savings_analysis: Optional[SavingsAnalysis] = Field(None, description="Savings compared to baseline")
    method: str = Field(default="quantum_inspired", description="Optimization method used")
    processing_time: float = Field(..., ge=0, description="Time taken for optimization")
    quantum_improvement_score: Optional[float] = Field(None, ge=0, le=100, description="Quantum algorithm improvement score")
    certificates: Optional[List[str]] = Field(default=[], description="Generated blockchain certificate IDs")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Optimization completion timestamp")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Additional optimization metadata")

class BatchOptimizationRequest(BaseModel):
    """Request for optimizing multiple scenarios simultaneously"""
    batch_id: Optional[str] = Field(None, description="Unique batch identifier")
    scenarios: List[RouteOptimizationRequest] = Field(..., min_items=1, max_items=10, description="List of optimization scenarios")
    parallel_processing: bool = Field(default=True, description="Enable parallel processing of scenarios")
    compare_results: bool = Field(default=True, description="Compare results across scenarios")
    
class RouteOptimizationResponse(BaseModel):
    optimization_id: str
    status: str = "completed"
    optimized_routes: List[OptimizedRoute]
    total_distance_km: float = Field(alias="total_distance")
    total_time_minutes: float = Field(alias="total_time") 
    total_cost: float
    total_carbon_kg: float = Field(alias="total_carbon")
    savings_analysis: Optional[Dict[str, Any]] = None
    method: str = "quantum_inspired"
    processing_time: float
    quantum_improvement_score: Optional[float] = None
    created_at: datetime
    
    class Config:
        allow_population_by_field_name = True
        
class RouteComparisonRequest(BaseModel):
    """Request for comparing different optimization methods"""
    locations: List[Location] = Field(..., min_items=2, max_items=100, description="Locations for comparison")
    vehicles: List[Vehicle] = Field(..., min_items=1, max_items=20, description="Vehicles for comparison")
    optimization_goals: OptimizationGoals = Field(default_factory=OptimizationGoals, description="Optimization goals")
    methods_to_compare: List[str] = Field(default=["traditional", "quantum_inspired"], description="Methods to compare")

class MethodResult(BaseModel):
    """Results for a specific optimization method"""
    method: str = Field(..., description="Optimization method name")
    total_cost: float = Field(..., ge=0, description="Total cost")
    total_time_minutes: float = Field(..., ge=0, description="Total time")
    total_distance_km: float = Field(..., ge=0, description="Total distance")
    total_carbon_kg: float = Field(..., ge=0, description="Total carbon emissions")
    routes: List[OptimizedRoute] = Field(..., description="Optimized routes")
    processing_time: float = Field(..., ge=0, description="Processing time")
    quality_score: float = Field(..., ge=0, le=100, description="Solution quality score")

class RouteComparisonResponse(BaseModel):
    """Response comparing different optimization methods"""
    comparison_id: str = Field(..., description="Unique comparison identifier")
    quantum_inspired_result: MethodResult = Field(..., description="Quantum-inspired optimization results")
    traditional_result: MethodResult = Field(..., description="Traditional optimization results")
    improvements: Dict[str, float] = Field(..., description="Improvement percentages")
    winner: str = Field(..., description="Best performing method")
    total_comparison_time_seconds: float = Field(..., ge=0, description="Total comparison time")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Comparison completion timestamp")

class RouteRecalculationRequest(BaseModel):
    """Request for real-time route recalculation"""
    route_id: str = Field(..., description="Route ID to recalculate")
    affected_locations: List[str] = Field(..., description="Location IDs affected by changes")
    reason: str = Field(..., description="Reason for recalculation (traffic, weather, etc.)")
    current_conditions: Optional[Dict[str, Any]] = Field(default={}, description="Current traffic/weather conditions")
    priority: int = Field(default=1, ge=1, le=5, description="Recalculation priority")

class RouteDetailsResponse(BaseModel):
    """Detailed information about a specific route"""
    route_id: str = Field(..., description="Route identifier")
    optimization_data: Dict[str, Any] = Field(..., description="Complete optimization data")
    route_analytics: Dict[str, Any] = Field(..., description="Route performance analytics")
    carbon_analysis: Dict[str, Any] = Field(..., description="Detailed carbon emission analysis")
    blockchain_certificate: Optional[str] = Field(None, description="Associated blockchain certificate ID")
    last_updated: datetime = Field(..., description="Last update timestamp")

class VehicleProfileResponse(BaseModel):
    """Vehicle profile information for selection"""
    vehicle_type: VehicleType = Field(..., description="Vehicle type")
    display_name: str = Field(..., description="Human-readable vehicle name")
    capacity_kg: float = Field(..., gt=0, description="Vehicle capacity")
    max_range_km: float = Field(..., gt=0, description="Maximum range")
    cost_per_km: float = Field(..., gt=0, description="Operating cost per km")
    emission_factor: float = Field(..., ge=0, description="Emission factor")
    fuel_type: str = Field(..., description="Fuel type")
    description: str = Field(..., description="Vehicle description")
    environmental_impact: str = Field(..., description="Environmental impact level")
    recommended_use: str = Field(..., description="Recommended use cases")

