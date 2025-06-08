import axios from 'axios'
import { type OptimizationResponse, type Certificate, type DashboardData, type Location, type Vehicle } from '../Services/types'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Route Optimization APIs
export const optimizeRoutes = async (
  locations: Location[],
  vehicles: Vehicle[],
  optimization_goals = { cost: 0.4, carbon: 0.4, time: 0.2 }
): Promise<OptimizationResponse> => {
  const response = await api.post('/routes/optimize', {
    locations,
    vehicles,
    optimization_goals,
    traffic_enabled: true,
    weather_enabled: true,
    create_certificate: true,
  })
  return response.data
}

export const compareRoutes = async (
  locations: Location[],
  vehicles: Vehicle[]
): Promise<{
  quantum_inspired_result: any
  traditional_result: any
  improvements: any
}> => {
  const response = await api.post('/routes/compare', {
    locations,
    vehicles,
    optimization_goals: { cost: 0.4, carbon: 0.4, time: 0.2 },
  })
  return response.data
}

export const getRouteDetails = async (routeId: string): Promise<any> => {
  const response = await api.get(`/routes/route/${routeId}`)
  return response.data
}

export const getVehicleProfiles = async (): Promise<Vehicle[]> => {
  const response = await api.get('/routes/vehicles')
  return response.data
}

// Carbon APIs
export const getCarbonTrends = async (days = 30): Promise<any> => {
  const response = await api.get(`/carbon/trends?days=${days}`)
  return response.data
}

export const calculateCarbonSavings = async (
  originalRoute: string,
  optimizedRoute: string
): Promise<any> => {
  const response = await api.post('/carbon/savings', {
    original_route: originalRoute,
    optimized_route: optimizedRoute,
  })
  return response.data
}

// Blockchain APIs
export const getRecentCertificates = async (limit = 10): Promise<Certificate[]> => {
  const response = await api.get(`/blockchain/certificates/recent?limit=${limit}`)
  return response.data
}

export const getCertificate = async (certificateId: string): Promise<Certificate> => {
  const response = await api.get(`/blockchain/certificate/${certificateId}`)
  return response.data
}

export const getBlockchainExplorer = async (): Promise<any> => {
  const response = await api.get('/blockchain/explorer')
  return response.data
}

// Analytics APIs
export const getDashboardData = async (timeRange = '24h'): Promise<DashboardData> => {
  const response = await api.get(`/analytics/dashboard?time_range=${timeRange}`)
  return response.data
}

export const getWalmartImpactReport = async (): Promise<any> => {
  const response = await api.get('/analytics/walmart/impact')
  return response.data
}

// Demo APIs
export const getWalmartNYCDemo = async (): Promise<OptimizationResponse> => {
  const response = await api.get('/demo/walmart-nyc')
  return response.data
}
