import React, { useState, useEffect } from 'react'
import {
  Container,
  Typography,
  Paper,
  Box,
  Button,
  Alert,
} from '@mui/material'
import { PlayArrow } from '@mui/icons-material'
import KPICards from './KPICards'
import CarbonSavingsChart from './CarbonSavingsChart'
import RecentActivity from './RecentActivity'
import LoadingSpinner from '../Common/LoadingSpinner'
import { getDashboardData, getWalmartNYCDemo } from '../../Services/api'
import { type DashboardData, type OptimizationResponse } from '../../Services/types' 

const Dashboard: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [demoRunning, setDemoRunning] = useState(false)
  const [demoResult, setDemoResult] = useState<OptimizationResponse | null>(null)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      const data = await getDashboardData()
      setDashboardData(data)
    } catch (err) {
      setError('Failed to load dashboard data')
      console.error('Dashboard error:', err)
    } finally {
      setLoading(false)
    }
  }

  const runWalmartDemo = async () => {
    try {
      setDemoRunning(true)
      const result = await getWalmartNYCDemo()
      setDemoResult(result)
      // Refresh dashboard data after demo
      await loadDashboardData()
    } catch (err) {
      setError('Failed to run demo')
      console.error('Demo error:', err)
    } finally {
      setDemoRunning(false)
    }
  }

  if (loading) return <LoadingSpinner />

  return (
    <Container maxWidth="xl">
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          QuantumEco Intelligence Dashboard
        </Typography>
        <Button
          variant="contained"
          size="large"
          startIcon={<PlayArrow />}
          onClick={runWalmartDemo}
          disabled={demoRunning}
        >
          {demoRunning ? 'Running Demo...' : 'Run Walmart NYC Demo'}
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {demoResult && (
        <Alert severity="success" sx={{ mb: 3 }}>
          Demo completed! Saved ${demoResult.savings_analysis.cost_saved.toFixed(2)} and {demoResult.savings_analysis.carbon_saved.toFixed(1)} kg CO²
        </Alert>
      )}

      {/* Main Dashboard Layout - Flexbox Container */}
      <Box 
        sx={{ 
          display: 'flex', 
          flexDirection: 'column', 
          gap: 3 
        }}
      >
        {/* KPI Cards - Full Width */}
        <Box sx={{ width: '100%' }}>
          <KPICards data={dashboardData} />
        </Box>

        {/* Chart and Activity Row */}
        <Box 
          sx={{ 
            display: 'flex', 
            flexDirection: { xs: 'column', md: 'row' },
            gap: 3,
            width: '100%'
          }}
        >
          {/* Carbon Savings Chart - 8/12 width on desktop */}
          <Box sx={{ flex: { xs: '1 1 100%', md: '2 1 0' } }}>
            <CarbonSavingsChart data={dashboardData?.carbonTrends || []} />
          </Box>

          {/* Recent Activity - 4/12 width on desktop */}
          <Box sx={{ flex: { xs: '1 1 100%', md: '1 1 0' } }}>
            <RecentActivity optimizations={dashboardData?.recentOptimizations || []} />
          </Box>
        </Box>

        {/* Walmart Scale Impact - Full Width */}
        <Box sx={{ width: '100%' }}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Walmart Scale Impact Projection
            </Typography>
            {dashboardData?.totalSavings && (
              <Box 
                sx={{ 
                  display: 'flex', 
                  flexDirection: { xs: 'column', md: 'row' },
                  gap: 3,
                  mt: 2
                }}
              >
                {/* Cost Savings */}
                <Box sx={{ flex: '1 1 0', textAlign: 'center' }}>
                  <Typography variant="h3" color="success.main">
                    ${(dashboardData.totalSavings.cost * 365 * 10500).toLocaleString()}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Annual Cost Savings (All Stores)
                  </Typography>
                </Box>

                {/* Carbon Reduction */}
                <Box sx={{ flex: '1 1 0', textAlign: 'center' }}>
                  <Typography variant="h3" color="success.main">
                    {(dashboardData.totalSavings.carbon * 365 * 10500 / 1000).toLocaleString()} tons
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Annual Carbon Reduction
                  </Typography>
                </Box>

                {/* Time Savings */}
                <Box sx={{ flex: '1 1 0', textAlign: 'center' }}>
                  <Typography variant="h3" color="primary.main">
                    {(dashboardData.totalSavings.time * 365 * 10500 / 60).toLocaleString()} hours
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Annual Time Savings
                  </Typography>
                </Box>
              </Box>
            )}
          </Paper>
        </Box>
      </Box>
    </Container>
  )
}

export default Dashboard

