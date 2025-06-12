
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator


class KPIMetric(BaseModel):
    """Key Performance Indicator metric"""
    name: str = Field(..., description="Metric name")
    value: Union[int, float, str] = Field(..., description="Metric value")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    change_percent: Optional[float] = Field(None, description="Percentage change from previous period")
    trend: Optional[str] = Field(None, description="Trend direction (up, down, stable)")
    description: str = Field(..., description="Metric description")

class ChartDataPoint(BaseModel):
    """Data point for charts and visualizations"""
    timestamp: datetime = Field(..., description="Data point timestamp")
    cost_savings: float = Field(..., description="Cost savings value")
    carbon_savings: float = Field(..., description="Carbon savings value")
    efficiency_score: float = Field(..., description="Efficiency score")
    routes_count: int = Field(..., description="Number of routes")

class RecentActivity(BaseModel):
    """Recent system activity item"""
    timestamp: datetime = Field(..., description="Activity timestamp")
    activity_type: str = Field(..., description="Type of activity")
    description: str = Field(..., description="Activity description")
    impact_value: Optional[float] = Field(None, description="Impact value")
    status: str = Field(..., description="Activity status")

class EfficiencyTrendsResponse(BaseModel):
    """Efficiency trends analysis response"""
    days: int = Field(..., description="Number of days analyzed")
    metric_type: str = Field(..., description="Type of metric analyzed")
    daily_efficiency_scores: List[float] = Field(..., description="Daily efficiency scores")
    moving_average_7d: List[float] = Field(..., description="7-day moving average")
    moving_average_30d: List[float] = Field(..., description="30-day moving average")
    trend_direction: str = Field(..., description="Overall trend direction")
    trend_strength: float = Field(..., description="Trend strength")
    best_day_score: float = Field(..., description="Best day score")
    worst_day_score: float = Field(..., description="Worst day score")
    average_score: float = Field(..., description="Average score")
    improvement_rate_percent: float = Field(..., description="Rate of improvement")
    volatility_index: float = Field(..., description="Volatility index")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")

class MethodComparisonResponse(BaseModel):
    """Method comparison analysis response"""
    sample_size: int = Field(..., description="Sample size used for comparison")
    quantum_inspired_score: float = Field(..., description="Quantum-inspired method score")
    traditional_score: float = Field(..., description="Traditional method score")
    improvement_percent: float = Field(..., description="Improvement percentage")
    performance_breakdown: Dict[str, Dict[str, float]] = Field(..., description="Detailed performance breakdown")
    category_winners: Dict[str, str] = Field(..., description="Winner for each category")
    statistical_significance: Dict[str, Any] = Field(..., description="Statistical significance analysis")
    confidence_level: float = Field(..., description="Confidence level")
    recommendation: str = Field(..., description="Recommended method")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")

class MetricTrend(str, Enum):
    """Enumeration for metric trends"""
    UP = "up"
    DOWN = "down"
    STABLE = "stable"

class SimulationType(str, Enum):
    """Enumeration for simulation types"""
    STANDARD = "standard"
    STRESS_TEST = "stress_test"
    SCALE_TEST = "scale_test"
    PERFORMANCE = "performance"

class KPIMetric(BaseModel):
    """Key Performance Indicator metric"""
    name: str = Field(..., description="Metric name")
    value: Union[int, float, str] = Field(..., description="Metric value")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    change_percent: Optional[float] = Field(None, description="Percentage change from previous period")
    trend: Optional[MetricTrend] = Field(None, description="Trend direction")
    description: str = Field(..., description="Metric description")
    target_value: Optional[Union[int, float]] = Field(None, description="Target value for this metric")
    achievement_percent: Optional[float] = Field(None, description="Achievement percentage vs target")

class ChartDataPoint(BaseModel):
    """Data point for charts and visualizations"""
    timestamp: datetime = Field(..., description="Data point timestamp")
    cost_savings: float = Field(..., description="Cost savings value")
    carbon_savings: float = Field(..., description="Carbon savings value")
    efficiency_score: float = Field(..., description="Efficiency score")
    routes_count: int = Field(..., description="Number of routes")
    optimization_time: Optional[float] = Field(None, description="Optimization processing time")

class RecentActivity(BaseModel):
    """Recent system activity item"""
    timestamp: datetime = Field(..., description="Activity timestamp")
    activity_type: str = Field(..., description="Type of activity")
    description: str = Field(..., description="Activity description")
    impact_value: Optional[float] = Field(None, description="Impact value")
    status: str = Field(..., description="Activity status")
    route_id: Optional[str] = Field(None, description="Associated route ID")
    user_id: Optional[str] = Field(None, description="User who triggered activity")

class SystemHealth(BaseModel):
    """System health metrics"""
    overall_score: float = Field(..., ge=0, le=100, description="Overall system health score")
    api_health: float = Field(..., ge=0, le=100, description="API health score")
    database_health: float = Field(..., ge=0, le=100, description="Database health score")
    optimization_engine_health: float = Field(..., ge=0, le=100, description="Optimization engine health")
    blockchain_health: float = Field(..., ge=0, le=100, description="Blockchain service health")
    last_check: datetime = Field(default_factory=datetime.utcnow, description="Last health check timestamp")

class DashboardDataResponse(BaseModel):
    """Main dashboard analytics with KPIs and charts"""
    kpi_metrics: List[KPIMetric] = Field(..., description="Key performance indicators")
    chart_data: List[ChartDataPoint] = Field(..., description="Chart data points")
    recent_activities: List[RecentActivity] = Field(..., description="Recent system activities")
    system_health: SystemHealth = Field(..., description="System health metrics")
    time_range: str = Field(..., description="Time range for data")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    data_freshness_seconds: int = Field(default=0, description="Data freshness in seconds")
    total_optimizations_today: int = Field(default=0, description="Total optimizations today")
    active_routes: int = Field(default=0, description="Currently active routes")

class SavingsSummaryResponse(BaseModel):
    """Cost and carbon savings summary with trends"""
    period: str = Field(..., description="Analysis period")
    total_cost_saved_usd: float = Field(..., ge=0, description="Total cost savings")
    total_carbon_saved_kg: float = Field(..., ge=0, description="Total carbon savings")
    total_time_saved_hours: float = Field(..., ge=0, description="Total time savings")
    total_distance_saved_km: float = Field(..., ge=0, description="Total distance savings")
    cost_trend_percent: float = Field(..., description="Cost savings trend percentage")
    carbon_trend_percent: float = Field(..., description="Carbon savings trend percentage")
    deliveries_optimized: int = Field(..., ge=0, description="Number of deliveries optimized")
    average_savings_per_delivery: Dict[str, float] = Field(..., description="Average savings per delivery")
    environmental_impact: Dict[str, float] = Field(..., description="Environmental impact equivalents")
    projections: Optional[Dict[str, float]] = Field(None, description="Future projections")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Generation timestamp")

class PerformanceMetricsResponse(BaseModel):
    """Route optimization performance metrics and benchmarks"""
    average_response_time_ms: float = Field(..., ge=0, description="Average API response time")
    throughput_requests_per_second: float = Field(..., ge=0, description="Request throughput")
    error_rate_percent: float = Field(..., ge=0, le=100, description="Error rate percentage")
    optimization_success_rate_percent: float = Field(..., ge=0, le=100, description="Optimization success rate")
    average_optimization_time_seconds: float = Field(..., ge=0, description="Average optimization time")
    quantum_improvement_factor: float = Field(..., ge=1, description="Quantum vs traditional improvement factor")
    system_cpu_usage_percent: float = Field(..., ge=0, le=100, description="System CPU usage")
    system_memory_usage_percent: float = Field(..., ge=0, le=100, description="System memory usage")
    cache_hit_rate_percent: float = Field(..., ge=0, le=100, description="Cache hit rate")
    database_query_time_ms: float = Field(..., ge=0, description="Average database query time")
    concurrent_optimizations: int = Field(..., ge=0, description="Current concurrent optimizations")
    uptime_hours: float = Field(..., ge=0, description="System uptime in hours")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

class MarketImpact(BaseModel):
    """Market impact analysis"""
    industry_leadership_value: float = Field(..., description="Industry leadership value in USD")
    competitive_advantage_duration_years: int = Field(..., description="Competitive advantage duration")
    market_share_increase_percent: float = Field(..., description="Market share increase percentage")
    customer_satisfaction_increase_percent: float = Field(..., description="Customer satisfaction increase")
    brand_value_increase_usd: float = Field(..., description="Brand value increase")

class WalmartImpactResponse(BaseModel):
    """Walmart-specific impact report with projections"""
    annual_cost_savings_usd: float = Field(..., ge=0, description="Annual cost savings")
    annual_carbon_reduction_kg: float = Field(..., ge=0, description="Annual carbon reduction")
    annual_time_savings_hours: float = Field(..., ge=0, description="Annual time savings")
    roi_percent: float = Field(..., description="Return on investment percentage")
    payback_period_months: float = Field(..., gt=0, description="Payback period in months")
    implementation_cost_usd: float = Field(..., gt=0, description="Implementation cost")
    stores_impacted: int = Field(..., gt=0, description="Number of stores impacted")
    daily_deliveries_optimized: int = Field(..., gt=0, description="Daily deliveries optimized")
    environmental_equivalents: Dict[str, float] = Field(..., description="Environmental impact equivalents")
    market_impact: MarketImpact = Field(..., description="Market impact analysis")
    confidence_level: float = Field(..., ge=0, le=1, description="Confidence level of projections")
    projection_basis: str = Field(..., description="Basis for projections")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Generation timestamp")

class SimulationRequest(BaseModel):
    """Large-scale optimization simulation parameters"""
    simulation_id: Optional[str] = Field(None, description="Unique simulation identifier")
    num_deliveries: int = Field(..., ge=1, le=100000, description="Number of deliveries to simulate")
    num_vehicles: int = Field(..., ge=1, le=1000, description="Number of vehicles to simulate")
    optimization_goals: Dict[str, float] = Field(..., description="Optimization goals weights")
    simulation_type: SimulationType = Field(default=SimulationType.STANDARD, description="Type of simulation")
    include_weather: bool = Field(default=True, description="Include weather factors")
    include_traffic: bool = Field(default=True, description="Include traffic factors")
    geographic_area: Optional[str] = Field(default="urban", description="Geographic area type")
    time_constraints: Optional[Dict[str, Any]] = Field(default={}, description="Time constraints")
    
    @validator('optimization_goals')
    def validate_optimization_goals(cls, v):
        """Validate optimization goals sum to approximately 1.0"""
        total = sum(v.values())
        if abs(total - 1.0) > 0.01:
            raise ValueError('Optimization goals must sum to 1.0')
        return v

class SimulationResults(BaseModel):
    """Large-scale simulation results"""
    simulation_id: str = Field(..., description="Simulation identifier")
    total_cost_usd: float = Field(..., ge=0, description="Total simulation cost")
    total_carbon: float = Field(..., ge=0, description="Total carbon emissions")
    total_time_hours: float = Field(..., ge=0, description="Total time in hours")
    total_distance: float = Field(..., ge=0, description="Total distance")
    optimization_score: float = Field(..., ge=0, le=100, description="Overall optimization score")
    cost_per_delivery: float = Field(..., ge=0, description="Average cost per delivery")
    carbon_per_delivery: float = Field(..., ge=0, description="Average carbon per delivery")
    vehicle_utilization_percent: float = Field(..., ge=0, le=100, description="Vehicle utilization percentage")
    processing_time_seconds: float = Field(..., ge=0, description="Simulation processing time")
    quantum_improvement_percent: float = Field(..., description="Quantum vs traditional improvement")
    recommendations: List[str] = Field(..., description="Optimization recommendations")
    simulation_parameters: Dict[str, Any] = Field(..., description="Original simulation parameters")
    scalability_metrics: Optional[Dict[str, float]] = Field(None, description="Scalability analysis")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
