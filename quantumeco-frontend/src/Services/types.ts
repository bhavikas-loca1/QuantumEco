export interface Location {
  id: string
  latitude: number
  longitude: number
  address: string
  demand?: number
  priority?: number
}

export interface Vehicle {
  id: string
  type: string
  capacity: number
  cost_per_km: number
  emission_factor: number
}

export interface OptimizedRoute {
  vehicle_id: string
  locations: Location[]
  total_distance: number
  total_time: number
  total_cost: number
  carbon_emissions: number
}

export interface OptimizationResponse {
  optimization_id: string
  status: string
  optimized_routes: OptimizedRoute[]
  total_distance: number
  total_time: number
  total_cost: number
  total_carbon_emissions: number
  savings_analysis: {
    cost_saved: number
    time_saved: number
    distance_saved: number
    carbon_saved: number
    cost_improvement_percent: number
    time_improvement_percent: number
    carbon_improvement_percent: number
  }
  optimization_method: string
  optimization_time: number
  quantum_improvement_score: number
  created_at: string
}

export interface Certificate {
  certificate_id: string
  route_id: string
  vehicle_id: string
  carbon_saved: number
  cost_saved: number
  optimization_score: number
  verification_hash: string
  transaction_hash: string
  block_number: number
  timestamp: number
  verified: boolean
}

export interface DashboardData {
  carbonTrends: Array<{
    date: string
    savings: number
    emissions: number
  }>
  recentOptimizations: OptimizationResponse[]
  totalSavings: {
    cost: number
    carbon: number
    time: number
  }
}



