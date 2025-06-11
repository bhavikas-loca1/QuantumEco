// src/services/types.ts
// Complete TypeScript interfaces matching your backend Pydantic schemas

// ===== Core Enums =====
export type DeliveryType = 'standard' | 'express' | 'same_day' | 'scheduled';
export type VehicleType = 'diesel_truck' | 'electric_van' | 'hybrid_delivery' | 'gas_truck' | 'cargo_bike';
export type OptimizationStatus = 'pending' | 'in_progress' | 'completed' | 'failed';
export type MetricTrend = 'up' | 'down' | 'stable';
export type DemoComplexity = 'low' | 'medium' | 'high';
export type OptimizationType = 'traditional' | 'quantum_inspired' | 'hybrid';

// ===== Analytics & Dashboard Types =====
export interface KPIMetric {
  name: string;
  value: number | string;
  unit?: string;
  change_percent?: number;
  trend?: MetricTrend;
  description: string;
  target_value?: number;
  achievement_percent?: number;
}

export interface ChartDataPoint {
  timestamp: string; // ISO string
  cost_savings: number;
  carbon_savings: number;
  efficiency_score: number;
  routes_count: number;
  optimization_time?: number;
}

export interface RecentActivity {
  timestamp: string; // ISO string
  activity_type: string;
  description: string;
  impact_value?: number;
  status: string;
  route_id?: string;
  user_id?: string;
}

export interface SystemHealth {
  overall_score: number;
  api_health: number;
  database_health: number;
  optimization_engine_health: number;
  blockchain_health: number;
  last_check: string; // ISO string
}

export interface DashboardDataResponse {
  kpi_metrics: KPIMetric[];
  chart_data: ChartDataPoint[];
  recent_activities: RecentActivity[];
  system_health: SystemHealth;
  time_range: string;
  last_updated: string; // ISO string
  data_freshness_seconds: number;
  total_optimizations_today: number;
  active_routes: number;
}

// ===== Route Optimization Types =====
export interface Location {
  id: string;
  name?: string;
  address: string;
  latitude: number;
  longitude: number;
  demand_kg?: number;
  priority?: number;
  time_window_start?: string;
  time_window_end?: string;
  delivery_type?: DeliveryType;
  special_requirements?: string[];
  contact_info?: string;
}

export interface Vehicle {
  id: string;
  type: VehicleType;
  capacity_kg: number;
  cost_per_km: number;
  emission_factor: number;
  max_range_km?: number;
  driver_id?: string;
  availability_start?: string;
  availability_end?: string;
  fuel_level?: number;
  current_location?: {
    latitude: number;
    longitude: number;
    address?: string;
  };
}

export interface OptimizationGoals {
  cost: number;
  carbon: number;
  time: number;
}

export interface RouteConstraints {
  max_distance_per_vehicle?: number;
  max_time_per_vehicle?: number;
  max_locations_per_vehicle?: number;
  require_return_to_depot?: boolean;
  allow_split_deliveries?: boolean;
  respect_time_windows?: boolean;
}

// ===== MISSING TYPES - Added to fix API integration =====
export interface RouteOptimizationRequest {
  request_id?: string;
  locations: Location[];
  vehicles: Vehicle[];
  optimization_goals?: OptimizationGoals;
  constraints?: RouteConstraints;
  traffic_enabled?: boolean;
  weather_enabled?: boolean;
  create_certificate?: boolean;
  optimization_timeout?: number;
  algorithm_preference?: string;
}

export interface RouteSegment {
  from_location_id: string;
  to_location_id: string;
  distance_km: number;
  travel_time_minutes: number;
  carbon_emissions_kg: number;
  estimated_arrival?: string;
  traffic_factor?: number;
  weather_factor?: number;
}

export interface OptimizedRoute {
  distance_km: number; 
  time_minutes: number; 
  cost_usd: number;
   carbon_kg: number; 
   load_kg: number;
  route: number[]; 
  route_id: string;
  vehicle_id: string;
  vehicle_type: VehicleType;
  locations: Location[];
  route_segments?: RouteSegment[];
  total_distance: number;
  total_time: number;
  total_cost: number;
  total_carbon: number;
  load_utilization_percent: number;
  route_geometry?: number[][];
  optimization_score: number;
  estimated_start_time?: string;
  estimated_end_time?: string;
  special_instructions?: string[];
  utilization_percent: number;
}

export interface SavingsAnalysis {
  cost_saved_usd: number;
  cost_improvement_percent: number;
  carbon_saved_kg: number;
  carbon_improvement_percent: number;
  time_saved_minutes: number;
  time_improvement_percent: number;
  distance_saved_km: number;
  distance_improvement_percent: number;
  efficiency_score: number;
}

export interface RouteOptimizationResponse {
  optimization_id: string;
  request_id?: string;
  status: OptimizationStatus;
  optimized_routes: OptimizedRoute[];
  total_distance: number;
  total_time: number;
  total_cost: number;
  total_carbon: number;
  savings_analysis?: SavingsAnalysis;
  method: string;
  processing_time: number;
  quantum_improvement_score?: number;
  certificates?: string[];
  created_at: string; // ISO string
  metadata?: Record<string, any>;
}

// ===== Carbon Calculation Types =====
export interface CarbonCalculationRequest {
  route_id: string;
  distance_km: number;
  vehicle_type: VehicleType;
  load_factor?: number;
  weather_conditions?: any;
  traffic_factor?: number;
  driver_efficiency?: number;
  route_complexity?: number;
  calculation_precision?: number;
}

export interface EmissionBreakdown {
  base_emissions: number;
  weather_impact: number;
  load_impact: number;
  traffic_impact: number;
  efficiency_adjustment: number;
  total_emissions: number;
}

export interface CarbonCalculationResponse {
  calculation_id: string;
  route_id: string;
  total_emissions_kg: number;
  emissions_per_km: number;
  emission_breakdown: EmissionBreakdown;
  weather_impact_factor: number;
  load_impact_factor: number;
  traffic_impact_factor: number;
  carbon_cost_usd: number;
  vehicle_type: VehicleType;
  distance_km: number;
  environmental_impact: string;
  calculation_timestamp: string; // ISO string
  methodology: string;
  confidence_level: number;
}

// ===== Blockchain Types =====
export interface Certificate {
  certificate_id: string;
  route_id: string;
  vehicle_id: string;
  carbon_saved_kg: number;
  cost_saved_usd: number;
  distance_km: number;
  optimization_score: number;
  verification_hash: string;
  transaction_hash: string;
  block_number: number;
  verified: boolean;
  certificate_status: string;
  blockchain_network: string;
  created_at: string; // ISO string
  verified_at?: string;
}

export interface EnvironmentalTrustToken {
  token_id: number;
  route_id: string;
  trust_score: number;
  carbon_impact_kg: number;
  sustainability_rating: number;
  environmental_impact_description: string;
  transaction_hash: string;
  block_number: number;
  token_status: string;
  created_at: string; // ISO string
  expires_at?: string;
}

// ===== Demo Types =====
export interface LocationData {
  id: string;
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  demand_kg: number;
  priority: number;
  time_window_start: string;
  time_window_end: string;
  delivery_type: string;
  special_requirements?: string[];
}

export interface OptimizationResult {
  method: OptimizationType;
  total_cost: number;
  total_carbon: number;
  total_time: number;
  total_distance: number;
  routes: any[];
  processing_time: number;
  optimization_score?: number;
  convergence_iterations?: number;
}

export interface WalmartNYCResponse {
  scenario_id: string;
  scenario_name: string;
  description: string;
  locations: LocationData[];
  vehicles: any[];
  traditional_optimization: OptimizationResult;
  quantum_optimization: OptimizationResult;
  savings_analysis: SavingsAnalysis;
  blockchain_certificates: any[];
  environmental_impact: {
    trees_planted_equivalent: number;
    cars_off_road_days: number;
    homes_powered_hours: number;
    miles_not_driven: number;
    gallons_fuel_saved: number;
  };
  walmart_scale_projection: {
    daily_cost_savings_usd: number;
    annual_cost_savings_usd: number;
    daily_carbon_reduction_kg: number;
    annual_carbon_reduction_tons: number;
    stores_impacted: number;
    confidence_level: number;
  };
  generated_at: string; // ISO string
}

export interface WalmartImpactResponse {
  annual_cost_savings_usd: number;
  annual_carbon_reduction_kg: number;
  annual_time_savings_hours: number;
  roi_percent: number;
  payback_period_months: number;
  implementation_cost_usd: number;
  stores_impacted: number;
  daily_deliveries_optimized: number;
  environmental_equivalents: Record<string, number>;
  confidence_level: number;
  projection_basis: string;
  generated_at: string; // ISO string
}

// ===== Quick Demo Response =====
export interface QuickDemoResponse {
  demo_title: string;
  scenario: string;
  locations: number;
  vehicles: number;
  results: {
    traditional: {
      total_cost: number;
      total_carbon: number;
      total_time: number;
    };
    quantum_inspired: {
      total_cost: number;
      total_carbon: number;
      total_time: number;
    };
    improvements: {
      cost_saved: string;
      carbon_reduced: string;
      time_saved: string;
    };
  };
  walmart_scale_projection: {
    annual_cost_savings: string;
    annual_carbon_reduction: string;
    stores_impacted: string;
  };
  blockchain_certificates: number;
  environmental_impact: any;
  generated_at: string; // ISO string
}

// ===== Health Check Response =====
export interface HealthCheckResponse {
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  database: {
    status: string;
  };
  services: {
    route_optimizer: string;
    carbon_calculator: string;
    blockchain_service: string;
    analytics_service: string;
  };
  uptime: string;
  version: string;
}

// ===== API Response Wrapper =====
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
  timestamp?: string;
}

// ===== Additional Missing Types for Complete Coverage =====
export interface VehicleProfile {
  vehicle_type: VehicleType;
  display_name: string;
  capacity_kg: number;
  cost_per_km: number;
  emission_factor: number;
  efficiency_rating: string;
  environmental_impact: string;
  description?: string;
}

export interface TrafficData {
  traffic_level: 'light' | 'moderate' | 'heavy';
  traffic_factor: number;
  estimated_delay_minutes: number;
}

export interface WeatherData {
  condition: string;
  temperature: number;
  humidity: number;
  wind_speed: number;
  visibility: number;
  impact_factor: number;
}

// ===== Batch Operations =====
export interface BatchOptimizationRequest {
  scenarios: RouteOptimizationRequest[];
  parallel_processing?: boolean;
  compare_results?: boolean;
}

export interface BatchOptimizationResponse {
  batch_id: string;
  scenarios_processed: number;
  successful_optimizations: number;
  failed_optimizations: number;
  results: RouteOptimizationResponse[];
  processing_time: number;
  best_scenario_id?: string;
}

// ===== Real-time Tracking =====
export interface RealTimeTrackingRequest {
  tracking_session_id: string;
  delivery_ids: string[];
  tracking_interval_seconds?: number;
  include_predictions?: boolean;
}

export interface RealTimeTrackingResponse {
  session_id: string;
  active_deliveries: number;
  total_emissions_current: number;
  estimated_total_emissions: number;
  progress_percentage: number;
  eta_minutes: number;
}

// ===== Simulation Types =====
export interface SimulationRequest {
  num_deliveries: number;
  num_vehicles: number;
  optimization_goals: OptimizationGoals;
  simulation_type?: 'standard' | 'stress_test' | 'scale_test' | 'performance';
  include_weather?: boolean;
  include_traffic?: boolean;
  geographic_area?: string;
}

export interface SimulationResponse {
  simulation_id: string;
  total_cost: number;
  total_carbon: number;
  total_time_hours: number;
  total_distance: number;
  vehicle_utilization_percent: number;
  quantum_improvement_percent: number;
  processing_time: number;
  recommendations: string[];
}
// ===== Missing API Response Types Based on RouteOptimizer Implementation =====

// Route Comparison Response - matches RouteOptimizer comparison methods
export interface RouteComparisonResponse {
  comparison_id: string;
  quantum_inspired_result: {
    status: 'success' | 'error' | 'no_solution';
    optimized_routes: Array<{
      vehicle_id: string;
      route: number[]; // Array of location indices
      distance_km: number;
      time_minutes: number;
      cost_usd: number;
      carbon_kg: number;
      load_kg: number;
      utilization_percent: number;
    }>;
    total_distance: number;
    total_time: number;
    total_cost: number;
    total_carbon: number;
    processing_time: number;
    quantum_score: number;
    quantum_improvement?: number;
    method: 'quantum_inspired';
  };
  traditional_result: {
    status: 'success' | 'error' | 'no_solution';
    optimized_routes: Array<{
      vehicle_id: string;
      route: number[]; // Array of location indices
      distance_km: number;
      time_minutes: number;
      cost_usd: number;
      carbon_kg: number;
      load_kg: number;
      utilization_percent: number;
    }>;
    total_distance: number;
    total_time: number;
    total_cost: number;
    total_carbon: number;
    processing_time: number;
    quantum_score: number;
    method: 'traditional';
  };
  improvements: {
    cost_improvement_percent: number;
    carbon_improvement_percent: number;
    time_improvement_percent: number;
    distance_improvement_percent: number;
    overall_improvement_percent: number;
    cost_saved_usd: number;
    carbon_saved_kg: number;
    time_saved_minutes: number;
    distance_saved_km: number;
  };
  winner: 'quantum_inspired' | 'traditional' | 'tie';
  comparison_timestamp: string;
  algorithm_details: {
    quantum_iterations: number;
    quantum_tunnel_probability: number;
    annealing_temperature: number;
    convergence_achieved: boolean;
  };
}

// Vehicle Profile Response - matches RouteOptimizer vehicle specifications
export interface VehicleProfileResponse {
  vehicle_profiles: {
    diesel_truck: {
      display_name: string;
      capacity_kg: number;
      cost_per_km: number;
      emission_factor: number;
      max_range_km: number;
      fuel_type: string;
      average_speed_kmh: number;
      efficiency_rating: string;
      environmental_impact: string;
      maintenance_cost_per_km: number;
    };
    electric_van: {
      display_name: string;
      capacity_kg: number;
      cost_per_km: number;
      emission_factor: number;
      max_range_km: number;
      fuel_type: string;
      average_speed_kmh: number;
      efficiency_rating: string;
      environmental_impact: string;
      maintenance_cost_per_km: number;
    };
    hybrid_delivery: {
      display_name: string;
      capacity_kg: number;
      cost_per_km: number;
      emission_factor: number;
      max_range_km: number;
      fuel_type: string;
      average_speed_kmh: number;
      efficiency_rating: string;
      environmental_impact: string;
      maintenance_cost_per_km: number;
    };
    gas_truck: {
      display_name: string;
      capacity_kg: number;
      cost_per_km: number;
      emission_factor: number;
      max_range_km: number;
      fuel_type: string;
      average_speed_kmh: number;
      efficiency_rating: string;
      environmental_impact: string;
      maintenance_cost_per_km: number;
    };
    cargo_bike: {
      display_name: string;
      capacity_kg: number;
      cost_per_km: number;
      emission_factor: number;
      max_range_km: number;
      fuel_type: string;
      average_speed_kmh: number;
      efficiency_rating: string;
      environmental_impact: string;
      maintenance_cost_per_km: number;
    };
  };
  available_types: VehicleType[];
  total_profiles: number;
  last_updated: string;
  default_recommendations: {
    urban_delivery: VehicleType;
    long_distance: VehicleType;
    eco_friendly: VehicleType;
    cost_effective: VehicleType;
  };
}

// Additional helper types for RouteOptimizer integration
export interface RouteAnalyticsResponse {
  route_id: string;
  method: 'quantum_inspired' | 'traditional';
  efficiency_score: number;
  cost_per_km: number;
  carbon_per_km: number;
  average_speed_kmh: number;
  fuel_efficiency: string;
  route_complexity: 'low' | 'medium' | 'high';
  performance_metrics: {
    distance_optimization: number;
    time_optimization: number;
    cost_optimization: number;
    carbon_optimization: number;
  };
}

export interface CurrentConditionsResponse {
  timestamp: string;
  traffic: 'light' | 'moderate' | 'heavy';
  weather: 'clear' | 'cloudy' | 'rain' | 'snow';
  temperature: number;
  visibility: 'good' | 'reduced';
  traffic_impact_factor: number;
  weather_impact_factor: number;
  recommendations: string[];
}

export interface RealTimeRecalculationResponse {
  status: 'success' | 'error';
  optimized_routes: Array<{
    vehicle_id: string;
    route: number[];
    distance_km: number;
    time_minutes: number;
    cost_usd: number;
    carbon_kg: number;
    load_kg: number;
    utilization_percent: number;
  }>;
  total_distance: number;
  total_time: number;
  total_cost: number;
  total_carbon: number;
  conditions_applied: CurrentConditionsResponse;
  adjustments: {
    traffic_impact: string;
    weather_impact: string;
  };
  recalculation_reason: string;
  processing_time: number;
}
