// src/services/api.ts
// Complete API service optimized for QuantumEco FastAPI backend with RouteOptimizer integration

import axios, { type AxiosResponse, AxiosError } from 'axios';
import type {
  DashboardDataResponse,
  RouteOptimizationRequest,
  RouteOptimizationResponse,
  WalmartNYCResponse,
  WalmartImpactResponse,
  QuickDemoResponse,
  HealthCheckResponse,
  Certificate,
  CarbonCalculationResponse,
  Location,
  Vehicle,
  OptimizationGoals,
  RouteComparisonResponse,
  VehicleProfileResponse,
} from './types';

// API Configuration
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// Request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error: AxiosError) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for better error handling
api.interceptors.response.use(
  (response: AxiosResponse) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error: AxiosError) => {
    console.error('API Error:', {
      message: error.message,
      status: error.response?.status,
      url: error.config?.url,
      data: error.response?.data,
    });
    return Promise.reject(error);
  }
);

// ===== Core System APIs =====
export const getHealthCheck = async (): Promise<HealthCheckResponse> => {
  try {
    const response: AxiosResponse<HealthCheckResponse> = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

export const getQuickDemo = async (): Promise<QuickDemoResponse> => {
  try {
    const response: AxiosResponse<QuickDemoResponse> = await api.get('/demo/quick-start');
    return response.data;
  } catch (error) {
    console.error('Quick demo failed:', error);
    throw error;
  }
};

export const getSystemInfo = async (): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.get('/system-info');
    return response.data;
  } catch (error) {
    console.error('System info failed:', error);
    throw error;
  }
};

// ===== Analytics & Dashboard APIs =====
export const getDashboardData = async (timeRange = '24h'): Promise<DashboardDataResponse> => {
  try {
    const response: AxiosResponse<DashboardDataResponse> = await api.get(
      `/api/analytics/dashboard?time_range=${timeRange}`
    );
    return response.data;
  } catch (error) {
    console.error('Dashboard data failed:', error);
    throw error;
  }
};

export const getWalmartImpactReport = async (): Promise<WalmartImpactResponse> => {
  try {
    const response: AxiosResponse<WalmartImpactResponse> = await api.get('/api/analytics/walmart/impact');
    return response.data;
  } catch (error) {
    console.error('Walmart impact report failed:', error);
    throw error;
  }
};

export const getPerformanceMetrics = async (): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.get('/api/analytics/performance');
    return response.data;
  } catch (error) {
    console.error('Performance metrics failed:', error);
    throw error;
  }
};

export const getSavingsSummary = async (period = 'week'): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.get(`/api/analytics/savings/summary?period=${period}`);
    return response.data;
  } catch (error) {
    console.error('Savings summary failed:', error);
    throw error;
  }
};

// ===== Route Optimization APIs (Based on RouteOptimizer class) =====
export const optimizeRoutes = async (
  locations: Location[],
  vehicles: Vehicle[],
  optimizationGoals: OptimizationGoals = { cost: 0.4, carbon: 0.4, time: 0.2 }
): Promise<RouteOptimizationResponse> => {
  try {
    const request: RouteOptimizationRequest = {
      locations,
      vehicles,
      optimization_goals: optimizationGoals,
      constraints: {
        max_distance_per_vehicle: 500,
        max_time_per_vehicle: 480,
        require_return_to_depot: true,
        respect_time_windows: true,
      },
      traffic_enabled: true,
      weather_enabled: true,
      create_certificate: true,
      optimization_timeout: 30,
      algorithm_preference: 'quantum_inspired',
    };

    const response: AxiosResponse<RouteOptimizationResponse> = await api.post(
      '/api/routes/optimize', 
      request
    );
    return response.data;
  } catch (error) {
    console.error('Route optimization failed:', error);
    throw error;
  }
};

export const compareOptimizationMethods = async (
  locations: Location[],
  vehicles: Vehicle[]
): Promise<RouteComparisonResponse> => {
  try {
    const response: AxiosResponse<RouteComparisonResponse> = await api.post('/api/routes/compare', {
      locations,
      vehicles,
      optimization_goals: { cost: 0.4, carbon: 0.4, time: 0.2 },
      methods_to_compare: ['traditional', 'quantum_inspired'],
    });
    return response.data;
  } catch (error) {
    console.error('Route comparison failed:', error);
    throw error;
  }
};

export const getVehicleProfiles = async (): Promise<VehicleProfileResponse> => {
  try {
    const response: AxiosResponse<VehicleProfileResponse> = await api.get('/api/routes/vehicles');
    return response.data;
  } catch (error) {
    console.error('Get vehicle profiles failed:', error);
    throw error;
  }
};

export const getRouteDetails = async (routeId: string): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.get(`/api/routes/route/${routeId}`);
    return response.data;
  } catch (error) {
    console.error('Get route details failed:', error);
    throw error;
  }
};

export const recalculateRoute = async (
  routeId: string,
  affectedLocations: string[],
  reason: string,
  currentConditions = {}
): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.post('/api/routes/recalculate', {
      route_id: routeId,
      affected_locations: affectedLocations,
      reason,
      current_conditions: currentConditions,
      priority: 1,
    });
    return response.data;
  } catch (error) {
    console.error('Route recalculation failed:', error);
    throw error;
  }
};

export const batchOptimizeRoutes = async (scenarios: RouteOptimizationRequest[]): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.post('/api/routes/batch-optimize', {
      scenarios,
      parallel_processing: true,
      compare_results: true,
    });
    return response.data;
  } catch (error) {
    console.error('Batch optimization failed:', error);
    throw error;
  }
};

export const getRouteAnalytics = async (routeId: string): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.get(`/api/routes/analytics/${routeId}`);
    return response.data;
  } catch (error) {
    console.error('Route analytics failed:', error);
    throw error;
  }
};

export const getCurrentConditions = async (locations: Location[]): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.post('/api/routes/conditions', {
      locations,
      include_traffic: true,
      include_weather: true,
    });
    return response.data;
  } catch (error) {
    console.error('Get current conditions failed:', error);
    throw error;
  }
};

// ===== Carbon Calculation APIs =====
export const calculateCarbon = async (
  routeId: string,
  distanceKm: number,
  vehicleType: string
): Promise<CarbonCalculationResponse> => {
  try {
    const response: AxiosResponse<CarbonCalculationResponse> = await api.post('/api/carbon/calculate', {
      route_id: routeId,
      distance_km: distanceKm,
      vehicle_type: vehicleType,
      load_factor: 1.0,
      calculation_precision: 3,
    });
    return response.data;
  } catch (error) {
    console.error('Carbon calculation failed:', error);
    throw error;
  }
};

export const trackCarbonRealtime = async (trackingSessionId: string, deliveryIds: string[]): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.post('/api/carbon/track-realtime', {
      tracking_session_id: trackingSessionId,
      delivery_ids: deliveryIds,
      tracking_interval_seconds: 60,
      include_predictions: true,
    });
    return response.data;
  } catch (error) {
    console.error('Carbon tracking failed:', error);
    throw error;
  }
};

export const calculateCarbonSavings = async (
  originalRouteId: string,
  optimizedRouteId: string
): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.post('/api/carbon/savings', {
      original_route_id: originalRouteId,
      optimized_route_id: optimizedRouteId,
      comparison_method: 'absolute',
      include_monetary_value: true,
    });
    return response.data;
  } catch (error) {
    console.error('Carbon savings calculation failed:', error);
    throw error;
  }
};

export const getCarbonVehicleProfiles = async (): Promise<any[]> => {
  try {
    const response: AxiosResponse<any[]> = await api.get('/api/carbon/vehicle-profiles');
    return response.data;
  } catch (error) {
    console.error('Get carbon vehicle profiles failed:', error);
    throw error;
  }
};

export const getDailyCarbonReport = async (date: string): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.get(`/api/carbon/daily-report/${date}`);
    return response.data;
  } catch (error) {
    console.error('Daily carbon report failed:', error);
    throw error;
  }
};

export const getCarbonTrends = async (days = 30, vehicleType?: string): Promise<any> => {
  try {
    let url = `/api/carbon/trends?days=${days}`;
    if (vehicleType) {
      url += `&vehicle_type=${vehicleType}`;
    }
    const response: AxiosResponse<any> = await api.get(url);
    return response.data;
  } catch (error) {
    console.error('Carbon trends failed:', error);
    throw error;
  }
};

export const predictCarbon = async (predictionDate: string, scheduledDeliveries: any[]): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.post('/api/carbon/predict', {
      prediction_date: predictionDate,
      scheduled_deliveries: scheduledDeliveries,
      include_optimization_potential: true,
    });
    return response.data;
  } catch (error) {
    console.error('Carbon prediction failed:', error);
    throw error;
  }
};

// ===== Blockchain APIs =====
export const createCertificate = async (
  routeId: string,
  vehicleId: string,
  carbonSaved: number,
  costSaved: number,
  distanceKm: number,
  optimizationScore: number
): Promise<Certificate> => {
  try {
    const response: AxiosResponse<Certificate> = await api.post('/api/blockchain/certificate', {
      route_id: routeId,
      vehicle_id: vehicleId,
      carbon_saved: carbonSaved,
      cost_saved: costSaved,
      distance_km: distanceKm,
      optimization_score: optimizationScore,
      delivery_count: 1,
      time_saved_minutes: 0,
      metadata: {},
      issuer: 'QuantumEco Intelligence',
    });
    return response.data;
  } catch (error) {
    console.error('Certificate creation failed:', error);
    throw error;
  }
};

export const getCertificate = async (certificateId: string): Promise<Certificate> => {
  try {
    const response: AxiosResponse<Certificate> = await api.get(`/api/blockchain/certificate/${certificateId}`);
    return response.data;
  } catch (error) {
    console.error('Get certificate failed:', error);
    throw error;
  }
};

export const getRecentCertificates = async (limit = 10): Promise<Certificate[]> => {
  try {
    const response: AxiosResponse<Certificate[]> = await api.get(`/api/blockchain/certificates/recent?limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error('Get recent certificates failed:', error);
    throw error;
  }
};

export const verifyCertificate = async (certificateId: string): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.post('/api/blockchain/verify', {
      certificate_id: certificateId,
      check_expiration: true,
    });
    return response.data;
  } catch (error) {
    console.error('Certificate verification failed:', error);
    throw error;
  }
};

export const createETT = async (
  routeId: string,
  trustScore: number,
  carbonImpact: number,
  sustainabilityRating: number
): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.post('/api/blockchain/ett/create', {
      route_id: routeId,
      trust_score: trustScore,
      carbon_impact: carbonImpact,
      sustainability_rating: sustainabilityRating,
      verification_level: 'standard',
    });
    return response.data;
  } catch (error) {
    console.error('ETT creation failed:', error);
    throw error;
  }
};

export const getTransactionDetails = async (transactionHash: string): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.get(`/api/blockchain/transaction/${transactionHash}`);
    return response.data;
  } catch (error) {
    console.error('Get transaction details failed:', error);
    throw error;
  }
};

export const getBlockchainExplorer = async (): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.get('/api/blockchain/explorer');
    return response.data;
  } catch (error) {
    console.error('Blockchain explorer failed:', error);
    throw error;
  }
};

export const createCarbonCredit = async (
  routeId: string,
  carbonAmountKg: number,
  valueUsd: number,
  vintageYear: number
): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.post('/api/blockchain/carbon-credit', {
      route_id: routeId,
      carbon_amount_kg: carbonAmountKg,
      value_usd: valueUsd,
      issuer: 'QuantumEco Intelligence',
      credit_type: 'verified_reduction',
      verification_standard: 'VCS',
      vintage_year: vintageYear,
    });
    return response.data;
  } catch (error) {
    console.error('Carbon credit creation failed:', error);
    throw error;
  }
};

// ===== Demo APIs =====
export const getWalmartNYCDemo = async (): Promise<WalmartNYCResponse> => {
  try {
    const response: AxiosResponse<WalmartNYCResponse> = await api.get('/api/demo/walmart-nyc');
    return response.data;
  } catch (error) {
    console.error('Walmart NYC demo failed:', error);
    throw error;
  }
};

export const getDemoScenarios = async (): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.get('/api/demo/scenarios');
    return response.data;
  } catch (error) {
    console.error('Demo scenarios failed:', error);
    throw error;
  }
};

export const generateCustomDemo = async (
  numLocations: number,
  numVehicles: number,
  area: string,
  vehicleTypes: string[]
): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.post('/api/demo/generate', {
      num_locations: numLocations,
      num_vehicles: numVehicles,
      area,
      location_density: 'urban',
      vehicle_types: vehicleTypes,
      capacity_range: { min: 500, max: 1500 },
      optimization_goals: { cost: 0.4, carbon: 0.4, time: 0.2 },
      include_weather_factors: true,
      include_traffic_factors: true,
      complexity_level: 'medium',
    });
    return response.data;
  } catch (error) {
    console.error('Custom demo generation failed:', error);
    throw error;
  }
};

export const getPerformanceShowcase = async (): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.get('/api/demo/performance-showcase');
    return response.data;
  } catch (error) {
    console.error('Performance showcase failed:', error);
    throw error;
  }
};

// ===== Simulation APIs =====
export const runSimulation = async (
  numDeliveries: number,
  numVehicles: number,
  optimizationGoals: OptimizationGoals
): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.post('/api/analytics/simulate', {
      num_deliveries: numDeliveries,
      num_vehicles: numVehicles,
      optimization_goals: optimizationGoals,
      simulation_type: 'standard',
      include_weather: true,
      include_traffic: true,
      geographic_area: 'urban',
    });
    return response.data;
  } catch (error) {
    console.error('Simulation failed:', error);
    throw error;
  }
};

export const getEfficiencyTrends = async (days = 30, metric = 'overall'): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.get(`/api/analytics/efficiency/trends?days=${days}&metric=${metric}`);
    return response.data;
  } catch (error) {
    console.error('Efficiency trends failed:', error);
    throw error;
  }
};

export const compareOptimizationMethodsAnalytics = async (sampleSize = 100): Promise<any> => {
  try {
    const response: AxiosResponse<any> = await api.get(`/api/analytics/compare/methods?sample_size=${sampleSize}`);
    return response.data;
  } catch (error) {
    console.error('Method comparison analytics failed:', error);
    throw error;
  }
};

// ===== Utility Functions =====
export const formatApiError = (error: any): string => {
  if (axios.isAxiosError(error)) {
    if (error.response?.data?.detail) {
      if (Array.isArray(error.response.data.detail)) {
        return error.response.data.detail.map((item: any) => item.msg || item).join(', ');
      }
      return error.response.data.detail;
    }
    if (error.response?.data?.message) {
      return error.response.data.message;
    }
    if (error.response?.status === 404) {
      return 'Resource not found';
    }
    if (error.response?.status === 500) {
      return 'Internal server error';
    }
    if (error.response?.status === 422) {
      return 'Invalid input data';
    }
    return error.message || 'Network error occurred';
  }
  return 'An unexpected error occurred';
};

export const isApiAvailable = async (): Promise<boolean> => {
  try {
    await getHealthCheck();
    return true;
  } catch (error) {
    console.error('API availability check failed:', error);
    return false;
  }
};

export const testRouteOptimizer = async (): Promise<boolean> => {
  try {
    const testLocations: Location[] = [
      {
        id: 'depot',
        name: 'Test Depot',
        address: 'Test Address',
        latitude: 40.7128,
        longitude: -74.0060,
        demand_kg: 0,
      },
      {
        id: 'loc1',
        name: 'Test Location 1',
        address: 'Test Address 1',
        latitude: 40.7589,
        longitude: -73.9851,
        demand_kg: 50,
      },
    ];

    const testVehicles: Vehicle[] = [
      {
        id: 'test_vehicle',
        type: 'electric_van',
        capacity_kg: 500,
        cost_per_km: 0.65,
        emission_factor: 0.05,
      },
    ];

    const result = await optimizeRoutes(testLocations, testVehicles);
    return result.status === 'completed';
  } catch (error) {
    console.error('Route optimizer test failed:', error);
    return false;
  }
};

// Export the axios instance for custom requests if needed
export { api };

// Legacy compatibility functions
export const optimizeRoute = optimizeRoutes; // Backward compatibility
export const getOptimizationHistory = getDashboardData; // Backward compatibility
export const getRouteOptimizationDetails = getRouteDetails; // Backward compatibility
