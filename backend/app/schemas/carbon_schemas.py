from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, date
from datetime import date as DateType
from enum import Enum

class EmissionUnit(str, Enum):
    """Enumeration for emission units"""
    KG_CO2 = "kg_co2"
    TONS_CO2 = "tons_co2"
    LBS_CO2 = "lbs_co2"
    GRAMS_CO2 = "grams_co2"

class VehicleType(str, Enum):
    """Enumeration for vehicle types"""
    DIESEL_TRUCK = "diesel_truck"
    ELECTRIC_VAN = "electric_van"
    HYBRID_DELIVERY = "hybrid_delivery"
    GAS_TRUCK = "gas_truck"
    CARGO_BIKE = "cargo_bike"

class WeatherCondition(str, Enum):
    """Enumeration for weather conditions"""
    CLEAR = "clear"
    CLOUDY = "cloudy"
    RAIN = "rain"
    SNOW = "snow"
    FOG = "fog"
    STORM = "storm"

class EnvironmentalImpact(str, Enum):
    """Enumeration for environmental impact levels"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

class WeatherConditions(BaseModel):
    """Weather conditions affecting carbon emissions"""
    condition: WeatherCondition = Field(..., description="Primary weather condition")
    temperature: Optional[float] = Field(None, ge=-50, le=60, description="Temperature in Celsius")
    wind_speed: Optional[float] = Field(default=0, ge=0, le=200, description="Wind speed in km/h")
    humidity: Optional[float] = Field(default=50, ge=0, le=100, description="Humidity percentage")
    visibility: Optional[float] = Field(default=10, ge=0, le=50, description="Visibility in kilometers")

class CarbonCalculationRequest(BaseModel):
    """Route data for emission calculation"""
    route_id: str = Field(..., description="Unique route identifier")
    distance_km: float = Field(..., gt=0, le=2000, description="Route distance in kilometers")
    vehicle_type: VehicleType = Field(..., description="Type of vehicle used")
    load_factor: float = Field(default=1.0, ge=0, le=2.0, description="Load factor (1.0 = full capacity)")
    weather_conditions: Optional[WeatherConditions] = Field(None, description="Weather conditions during route")
    traffic_factor: Optional[float] = Field(default=1.0, ge=0.5, le=3.0, description="Traffic impact factor")
    driver_efficiency: Optional[float] = Field(default=1.0, ge=0.7, le=1.3, description="Driver efficiency factor")
    route_complexity: Optional[float] = Field(default=1.0, ge=0.8, le=1.5, description="Route complexity factor")
    calculation_precision: int = Field(default=3, ge=1, le=6, description="Decimal places for precision")
    
    @validator('distance_km')
    def validate_distance(cls, v):
        """Validate distance is reasonable"""
        if v <= 0:
            raise ValueError('Distance must be greater than 0')
        if v > 2000:
            raise ValueError('Distance cannot exceed 2000 km for single route')
        return v

class EmissionBreakdown(BaseModel):
    """Detailed breakdown of emission factors"""
    base_emissions: float = Field(..., description="Base emissions without factors")
    weather_impact: float = Field(..., description="Additional emissions due to weather")
    load_impact: float = Field(..., description="Additional emissions due to load")
    traffic_impact: float = Field(..., description="Additional emissions due to traffic")
    efficiency_adjustment: float = Field(..., description="Emissions adjustment for efficiency")
    total_emissions: float = Field(..., description="Total calculated emissions")

class CarbonCalculationResponse(BaseModel):
    """Detailed emission breakdown with impact factors"""
    calculation_id: str = Field(..., description="Unique calculation identifier")
    route_id: str = Field(..., description="Route identifier")
    total_emissions_kg: float = Field(..., ge=0, description="Total emissions in kg CO2")
    emissions_per_km: float = Field(..., ge=0, description="Emissions per kilometer")
    emission_breakdown: EmissionBreakdown = Field(..., description="Detailed emission breakdown")
    weather_impact_factor: float = Field(..., description="Weather impact multiplier")
    load_impact_factor: float = Field(..., description="Load impact multiplier")
    traffic_impact_factor: float = Field(..., description="Traffic impact multiplier")
    carbon_cost_usd: float = Field(..., ge=0, description="Carbon cost at $50/ton CO2")
    vehicle_type: VehicleType = Field(..., description="Vehicle type used")
    distance_km: float = Field(..., description="Route distance")
    environmental_impact: EnvironmentalImpact = Field(..., description="Environmental impact level")
    calculation_timestamp: datetime = Field(default_factory=datetime.utcnow, description="Calculation timestamp")
    methodology: str = Field(default="IPCC 2021 Guidelines", description="Calculation methodology")
    confidence_level: float = Field(default=0.95, ge=0, le=1, description="Calculation confidence level")
    
    @validator('total_emissions_kg')
    def validate_emissions(cls, v):
        """Validate emissions are reasonable"""
        if v < 0:
            raise ValueError('Emissions cannot be negative')
        return round(v, 3)

class CarbonTrackingRequest(BaseModel):
    """Real-time tracking session parameters"""
    tracking_session_id: str = Field(..., description="Unique tracking session identifier")
    delivery_ids: List[str] = Field(..., min_items=1, max_items=50, description="List of delivery IDs to track")
    tracking_interval_seconds: int = Field(default=60, ge=30, le=300, description="Tracking update interval")
    include_predictions: bool = Field(default=True, description="Include emission predictions")
    alert_thresholds: Optional[Dict[str, float]] = Field(default={}, description="Alert thresholds for emissions")
    
    @validator('delivery_ids')
    def validate_delivery_ids(cls, v):
        """Validate delivery IDs list"""
        if len(v) > 50:
            raise ValueError('Maximum 50 deliveries can be tracked simultaneously')
        return v

class CarbonTrackingResponse(BaseModel):
    """Real-time carbon tracking response"""
    delivery_id: str = Field(..., description="Delivery identifier")
    status: str = Field(..., description="Delivery status")
    current_emissions_kg: float = Field(..., ge=0, description="Current emissions")
    distance_covered_km: float = Field(..., ge=0, description="Distance covered so far")
    estimated_total_emissions_kg: float = Field(..., ge=0, description="Estimated total emissions")
    progress_percentage: float = Field(..., ge=0, le=100, description="Delivery progress percentage")
    vehicle_type: VehicleType = Field(..., description="Vehicle type")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Update timestamp")
    error_message: Optional[str] = Field(None, description="Error message if tracking failed")

class VehicleEmissionProfile(BaseModel):
    """Vehicle-specific emission characteristics"""
    vehicle_type: VehicleType = Field(..., description="Vehicle type")
    display_name: str = Field(..., description="Human-readable vehicle name")
    emission_factor_kg_per_km: float = Field(..., ge=0, le=1, description="Base emission factor")
    fuel_type: str = Field(..., description="Fuel type (diesel, electric, hybrid, gasoline)")
    capacity_kg: float = Field(..., gt=0, description="Vehicle capacity in kg")
    efficiency_rating: str = Field(..., description="Efficiency rating (A+, A, B, C, D)")
    weather_sensitivity: float = Field(..., ge=1.0, le=2.0, description="Weather sensitivity factor")
    load_sensitivity: float = Field(..., ge=1.0, le=2.0, description="Load sensitivity factor")
    description: str = Field(..., description="Vehicle description")
    environmental_impact: EnvironmentalImpact = Field(..., description="Environmental impact level")
    cost_per_km: float = Field(..., gt=0, description="Operating cost per kilometer")
    maintenance_factor: float = Field(..., ge=0.5, le=2.0, description="Maintenance impact factor")
    lifecycle_emissions_kg_per_km: float = Field(..., ge=0, description="Lifecycle emissions including manufacturing")

class CarbonSavingsRequest(BaseModel):
    """Request for carbon savings comparison"""
    original_route_id: str = Field(..., description="Original route identifier")
    optimized_route_id: str = Field(..., description="Optimized route identifier")
    comparison_method: str = Field(default="absolute", description="Comparison method (absolute, percentage)")
    include_monetary_value: bool = Field(default=True, description="Include monetary value of savings")
    carbon_price_per_ton: float = Field(default=50.0, gt=0, description="Carbon price per ton for valuation")

class EnvironmentalEquivalents(BaseModel):
    """Environmental impact equivalents"""
    trees_planted_equivalent: float = Field(..., description="Equivalent trees planted")
    cars_off_road_days: float = Field(..., description="Equivalent car-free days")
    homes_powered_hours: float = Field(..., description="Equivalent home power hours")
    miles_not_driven: float = Field(..., description="Equivalent miles not driven")
    gallons_fuel_saved: float = Field(..., description="Equivalent gallons of fuel saved")

class CarbonSavingsResponse(BaseModel):
    """Savings analysis with monetary value"""
    comparison_id: str = Field(..., description="Unique comparison identifier")
    original_route_id: str = Field(..., description="Original route ID")
    optimized_route_id: str = Field(..., description="Optimized route ID")
    carbon_saved_kg: float = Field(..., description="Carbon emissions saved")
    percentage_reduction: float = Field(..., description="Percentage reduction in emissions")
    monetary_value_usd: float = Field(..., description="Monetary value of carbon savings")
    environmental_impact_description: str = Field(..., description="Human-readable impact description")
    environmental_equivalents: EnvironmentalEquivalents = Field(..., description="Environmental equivalents")
    annual_projection: Dict[str, float] = Field(..., description="Annual savings projection")
    calculation_timestamp: datetime = Field(default_factory=datetime.utcnow, description="Calculation timestamp")
    confidence_level: float = Field(default=0.92, ge=0, le=1, description="Calculation confidence")

class VehicleBreakdown(BaseModel):
    """Vehicle type breakdown for reports"""
    vehicle_type: VehicleType = Field(..., description="Vehicle type")
    count: int = Field(..., ge=0, description="Number of vehicles")
    total_emissions: float = Field(..., ge=0, description="Total emissions for this vehicle type")
    total_distance: float = Field(..., ge=0, description="Total distance for this vehicle type")
    average_emissions_per_km: float = Field(..., ge=0, description="Average emissions per km")

class PerformanceMetrics(BaseModel):
    """Performance metrics for carbon reporting"""
    efficiency_score: float = Field(..., ge=0, le=100, description="Overall efficiency score")
    improvement_vs_previous_day: float = Field(..., description="Improvement percentage vs previous day")
    target_achievement: float = Field(..., ge=0, le=100, description="Target achievement percentage")
    carbon_intensity: float = Field(..., ge=0, description="Carbon intensity (kg CO2 per delivery)")

class DailyCarbonReport(BaseModel):
    date: DateType = Field(..., description="Report date")
    total_emissions_kg: float = Field(..., ge=0, description="Total daily emissions")
    total_savings_kg: float = Field(..., ge=0, description="Total daily carbon savings")
    deliveries_count: int = Field(..., ge=0, description="Number of deliveries")
    average_emissions_per_delivery_kg: float = Field(..., ge=0, description="Average emissions per delivery")
    top_performing_routes: List[str] = Field(..., description="Best performing route IDs")
    worst_performing_routes: List[str] = Field(..., description="Worst performing route IDs")
    vehicle_breakdown: Dict[str, VehicleBreakdown] = Field(..., description="Breakdown by vehicle type")
    performance_metrics: PerformanceMetrics = Field(..., description="Performance metrics")
    improvement_recommendations: List[str] = Field(..., description="Optimization recommendations")
    carbon_cost_usd: float = Field(..., ge=0, description="Total carbon cost")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Report generation timestamp")

class CarbonTrendData(BaseModel):
    """Carbon trend data point"""
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    total_emissions: float = Field(..., ge=0, description="Total emissions for the day")
    average_emissions_per_delivery: float = Field(..., ge=0, description="Average emissions per delivery")
    deliveries_count: int = Field(..., ge=0, description="Number of deliveries")
    efficiency_score: float = Field(..., ge=0, le=100, description="Daily efficiency score")

class CarbonTrendsResponse(BaseModel):
    """Carbon emission trends over specified time period"""
    period_days: int = Field(..., ge=1, description="Number of days in analysis period")
    vehicle_type_filter: Optional[VehicleType] = Field(None, description="Vehicle type filter applied")
    daily_emissions: List[CarbonTrendData] = Field(..., description="Daily emission data")
    trend_direction: str = Field(..., description="Trend direction (improving, declining, stable)")
    average_daily_emissions_kg: float = Field(..., ge=0, description="Average daily emissions")
    total_period_emissions_kg: float = Field(..., ge=0, description="Total emissions for period")
    best_day: CarbonTrendData = Field(..., description="Best performing day")
    worst_day: CarbonTrendData = Field(..., description="Worst performing day")
    improvement_rate_percent: float = Field(..., description="Rate of improvement percentage")
    predictions: List[Dict[str, Any]] = Field(default=[], description="Future trend predictions")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")

class DeliveryPrediction(BaseModel):
    """Individual delivery emission prediction"""
    delivery_id: str = Field(..., description="Delivery identifier")
    vehicle_type: VehicleType = Field(..., description="Vehicle type")
    distance_km: float = Field(..., gt=0, description="Planned distance")
    load_factor: float = Field(..., ge=0, le=2, description="Expected load factor")
    route_coordinates: List[List[float]] = Field(..., description="Route coordinates [[lat, lng], ...]")

class CarbonPredictionRequest(BaseModel):
    """Predict future carbon emissions based on delivery schedule"""
    prediction_id: Optional[str] = Field(None, description="Unique prediction identifier")
    prediction_date: date = Field(..., description="Date for prediction")
    scheduled_deliveries: List[DeliveryPrediction] = Field(..., min_items=1, max_items=1000, description="Scheduled deliveries")
    weather_forecast: Optional[WeatherConditions] = Field(None, description="Weather forecast for the date")
    include_optimization_potential: bool = Field(default=True, description="Include optimization potential analysis")
    
    @validator('prediction_date')
    def validate_future_date(cls, v):
        """Ensure prediction date is in the future"""
        if v <= date.today():
            raise ValueError('Prediction date must be in the future')
        return v

class OptimizationPotential(BaseModel):
    """Optimization potential analysis"""
    potential_savings_kg: float = Field(..., ge=0, description="Potential carbon savings")
    potential_percent: float = Field(..., ge=0, le=100, description="Potential savings percentage")
    total_baseline_emissions_kg: float = Field(..., ge=0, description="Baseline emissions without optimization")
    optimization_method: str = Field(..., description="Recommended optimization method")

class CarbonPredictionResponse(BaseModel):
    """Emission prediction results"""
    prediction_id: str = Field(..., description="Unique prediction identifier")
    prediction_date: date = Field(..., description="Prediction date")
    total_predicted_emissions_kg: float = Field(..., ge=0, description="Total predicted emissions")
    delivery_count: int = Field(..., ge=0, description="Number of deliveries")
    average_emissions_per_delivery_kg: float = Field(..., ge=0, description="Average emissions per delivery")
    delivery_predictions: List[Dict[str, Any]] = Field(..., description="Individual delivery predictions")
    optimization_potential: OptimizationPotential = Field(..., description="Optimization potential analysis")
    confidence_level: float = Field(..., ge=0, le=1, description="Prediction confidence level")
    optimization_recommendations: List[str] = Field(..., description="Optimization recommendations")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Prediction timestamp")

class CarbonAlertThreshold(BaseModel):
    """Carbon emission alert threshold"""
    threshold_type: str = Field(..., description="Type of threshold (daily, route, vehicle)")
    threshold_value: float = Field(..., gt=0, description="Threshold value")
    unit: EmissionUnit = Field(default=EmissionUnit.KG_CO2, description="Threshold unit")
    alert_level: str = Field(..., description="Alert level (warning, critical)")

class CarbonAlert(BaseModel):
    """Carbon emission alert"""
    alert_id: str = Field(..., description="Unique alert identifier")
    alert_type: str = Field(..., description="Type of alert")
    threshold: CarbonAlertThreshold = Field(..., description="Threshold that was exceeded")
    current_value: float = Field(..., description="Current emission value")
    excess_amount: float = Field(..., description="Amount by which threshold was exceeded")
    affected_routes: List[str] = Field(..., description="Affected route IDs")
    recommendations: List[str] = Field(..., description="Recommended actions")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Alert creation time")
