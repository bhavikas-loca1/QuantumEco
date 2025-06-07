
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


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
