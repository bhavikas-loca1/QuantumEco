import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  Alert,
  Chip,
  Card,
  CardContent,
  Divider,
  CircularProgress,
} from '@mui/material';
import {
  PlayArrow,
  TrendingUp,
  HealthAndSafety,
  Refresh,
  Timeline,
  AssessmentOutlined,
  Co2Outlined,
  AttachMoneyOutlined,
  AccessTimeOutlined,
  WarningAmberOutlined,
} from '@mui/icons-material';
import KPICards from './KPICards';
import CarbonSavingsCertificate from './CarbonSavingsChart';
import RecentActivity from './RecentActivity';
import LoadingSpinner from '../Common/LoadingSpinner';
import {
  getDashboardData,
  getWalmartNYCDemo,
  getQuickDemo,
  getHealthCheck,
  getWalmartImpactReport,
  formatApiError,
} from '../../Services/api';
import type {
  DashboardDataResponse,
  WalmartNYCResponse,
  WalmartImpactResponse,
  HealthCheckResponse,
} from '../../Services/types';

interface SystemStatus {
  status: 'healthy' | 'degraded' | 'unhealthy';
  lastCheck: string;
}

/**
 * Dashboard Component
 * Purpose: Main orchestrator that fetches and displays all dashboard data
 * Features: Auto-refresh, demo execution, system health monitoring, error handling
 */
const Dashboard: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardDataResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [demoRunning, setDemoRunning] = useState(false);
  const [demoResult, setDemoResult] = useState<WalmartNYCResponse | null>(null);
  const [walmartImpact, setWalmartImpact] = useState<WalmartImpactResponse | null>(null);
  const [systemStatus, setSystemStatus] = useState<SystemStatus>({
    status: 'healthy',
    lastCheck: new Date().toISOString(),
  });
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadInitialData();
    
    // Set up auto-refresh every 30 seconds
    const interval = setInterval(() => {
      if (!demoRunning && !refreshing) {
        loadDashboardData();
        checkSystemHealth();
      }
    }, 30000);

    return () => clearInterval(interval);
  }, [demoRunning, refreshing]);

  const loadInitialData = async () => {
    await Promise.all([
      loadDashboardData(),
      checkSystemHealth(),
      loadWalmartImpact(),
    ]);
  };

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getDashboardData();
      setDashboardData(data);
    } catch (err: any) {
      const errorMessage = formatApiError(err);
      setError(`Failed to load dashboard data: ${errorMessage}`);
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  const checkSystemHealth = async () => {
    try {
      const health: HealthCheckResponse = await getHealthCheck();
      setSystemStatus({
        status: health.status || 'healthy',
        lastCheck: new Date().toISOString(),
      });
    } catch (err) {
      setSystemStatus({
        status: 'unhealthy',
        lastCheck: new Date().toISOString(),
      });
      console.error('Health check error:', err);
    }
  };

  const loadWalmartImpact = async () => {
    try {
      const impact = await getWalmartImpactReport();
      setWalmartImpact(impact);
    } catch (err) {
      console.error('Walmart impact error:', err);
    }
  };

  const runWalmartDemo = async () => {
    try {
      setDemoRunning(true);
      setError(null);
      const result = await getWalmartNYCDemo();
      setDemoResult(result);
      await loadDashboardData(); // Refresh dashboard after demo
    } catch (err: any) {
      const errorMessage = formatApiError(err);
      setError(`Failed to run Walmart demo: ${errorMessage}`);
      console.error('Demo error:', err);
    } finally {
      setDemoRunning(false);
    }
  };

  const runQuickDemo = async () => {
    try {
      setDemoRunning(true);
      setError(null);
      const result = await getQuickDemo();
      console.log('Quick demo result:', result);
      await loadDashboardData(); // Refresh dashboard after demo
    } catch (err: any) {
      const errorMessage = formatApiError(err);
      setError(`Failed to run quick demo: ${errorMessage}`);
      console.error('Quick demo error:', err);
    } finally {
      setDemoRunning(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await Promise.all([
      loadDashboardData(),
      checkSystemHealth(),
    ]);
    setRefreshing(false);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'success';
      case 'degraded':
        return 'warning';
      case 'unhealthy':
        return 'error';
      default:
        return 'default';
    }
  };

  if (loading && !dashboardData) {
    return <LoadingSpinner />;
  }

  return (
    <Container maxWidth="xl" sx={{ py: 3 }}>
      {/* Header Section */}
      <Box
        sx={{
          display: 'flex',
          flexDirection: { xs: 'column', md: 'row' },
          justifyContent: 'space-between',
          alignItems: { xs: 'flex-start', md: 'center' },
          mb: 4,
          gap: 2,
        }}
      >
        <Box>
          <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', mb: 1 }}>
            🚀 QuantumEco Intelligence Dashboard
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flexWrap: 'wrap' }}>
            <Chip
              icon={<HealthAndSafety />}
              label={`System ${systemStatus.status}`}
              color={getStatusColor(systemStatus.status)}
              size="small"
            />
            <Typography variant="body2" color="text.secondary">
              Updated: {dashboardData?.last_updated 
                ? new Date(dashboardData.last_updated).toLocaleTimeString() 
                : 'Never'}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Range: {dashboardData?.time_range || '24h'}
            </Typography>
            {dashboardData?.total_optimizations_today !== undefined && (
              <Chip
                label={`${dashboardData.total_optimizations_today} optimizations today`}
                size="small"
                variant="outlined"
                color="primary"
              />
            )}
            {dashboardData?.active_routes !== undefined && dashboardData.active_routes > 0 && (
              <Chip
                label={`${dashboardData.active_routes} active routes`}
                size="small"
                variant="outlined"
                color="info"
              />
            )}
          </Box>
        </Box>

        <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
          <Button
            variant="outlined"
            startIcon={refreshing ? <CircularProgress size={16} /> : <Refresh />}
            onClick={handleRefresh}
            disabled={refreshing || loading || demoRunning}
          >
            {refreshing ? 'Refreshing...' : 'Refresh'}
          </Button>
          <Button
            variant="outlined"
            startIcon={<Timeline />}
            onClick={runQuickDemo}
            disabled={demoRunning}
            color="secondary"
          >
            Quick Demo
          </Button>
          <Button
            variant="contained"
            size="large"
            startIcon={demoRunning ? <CircularProgress size={16} color="inherit" /> : <PlayArrow />}
            onClick={runWalmartDemo}
            disabled={demoRunning}
            sx={{ minWidth: 220 }}
          >
            {demoRunning ? 'Running Walmart Demo...' : 'Run Walmart NYC Demo'}
          </Button>
        </Box>
      </Box>

      {/* Error Alert */}
      {error && (
        <Alert 
          severity="error" 
          sx={{ mb: 3 }} 
          onClose={() => setError(null)}
          icon={<WarningAmberOutlined />}
          action={
            <Button color="inherit" size="small" onClick={handleRefresh}>
              Retry
            </Button>
          }
        >
          {error}
        </Alert>
      )}

      {/* Demo Result Alert */}
      {demoResult && (
        <Alert 
          severity="success" 
          sx={{ mb: 3 }} 
          onClose={() => setDemoResult(null)}
        >
          <Typography variant="h6" gutterBottom>
            🎉 {demoResult.scenario_name} Completed Successfully!
          </Typography>
          <Box
            sx={{
              display: 'flex',
              flexDirection: { xs: 'column', md: 'row' },
              gap: 3,
              mt: 1,
            }}
          >
            <Typography variant="body2" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <AttachMoneyOutlined fontSize="small" color="success" />
              <strong>Cost Saved:</strong> ${demoResult.savings_analysis.cost_saved_usd.toFixed(2)} 
              ({demoResult.savings_analysis.cost_improvement_percent.toFixed(1)}% improvement)
            </Typography>
            <Typography variant="body2" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Co2Outlined fontSize="small" color="success" />
              <strong>Carbon Reduced:</strong> {demoResult.savings_analysis.carbon_saved_kg.toFixed(1)} kg CO₂ 
              ({demoResult.savings_analysis.carbon_improvement_percent.toFixed(1)}% improvement)
            </Typography>
            <Typography variant="body2" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <AccessTimeOutlined fontSize="small" color="primary" />
              <strong>Time Saved:</strong> {demoResult.savings_analysis.time_saved_minutes.toFixed(1)} minutes
            </Typography>
          </Box>
        </Alert>
      )}

      {/* Main Dashboard Content */}
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
        {/* KPI Cards Section */}
        <Box>
          <Typography variant="h5" sx={{ mb: 3, fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 1 }}>
            <AssessmentOutlined />
            Key Performance Indicators
          </Typography>
          <KPICards 
            metrics={dashboardData?.kpi_metrics || []} 
            loading={loading}
          />
        </Box>

        {/* Charts and Certificates Section */}
        <Box
          sx={{
            display: 'flex',
            flexDirection: { xs: 'column', lg: 'row' },
            gap: 4,
          }}
        >
          {/* Performance Analytics Section */}
          <Box sx={{ flex: { xs: '1 1 100%', lg: '2 1 0' } }}>
            <Typography variant="h5" sx={{ mb: 3, fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 1 }}>
              <TrendingUp />
              Performance Analytics
            </Typography>
            <Card sx={{ height: '500px' }}>
              <CardContent sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <Typography variant="h6" gutterBottom>
                  Optimization Trends & System Performance
                </Typography>
                
                <Box sx={{ 
                  flex: 1,
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'center',
                  flexDirection: 'column',
                  gap: 2
                }}>
                  <TrendingUp sx={{ fontSize: 64, color: 'primary.main', opacity: 0.6 }} />
                  <Typography variant="body1" color="text.secondary" sx={{ textAlign: 'center' }}>
                    📊 Chart visualization component integration point
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center' }}>
                    Data points available: {dashboardData?.chart_data?.length || 0} | 
                    System health: {dashboardData?.system_health?.overall_score?.toFixed(1) || 'N/A'}%
                  </Typography>
                  {dashboardData?.chart_data && dashboardData.chart_data.length > 0 && (
                    <Typography variant="body2" color="primary.main" sx={{ textAlign: 'center' }}>
                      Latest efficiency score: {dashboardData.chart_data[dashboardData.chart_data.length - 1]?.efficiency_score?.toFixed(1) || 'N/A'}
                    </Typography>
                  )}
                </Box>
              </CardContent>
            </Card>
          </Box>

          {/* Recent Activity Section */}
          <Box sx={{ flex: { xs: '1 1 100%', lg: '1 1 0' } }}>
            <Typography variant="h5" sx={{ mb: 3, fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 1 }}>
              <AssessmentOutlined />
              System Activity
            </Typography>
            <RecentActivity
              activities={dashboardData?.recent_activities || []}
              loading={loading}
            />
          </Box>
        </Box>

        {/* Blockchain Certificates Section */}
        <Box>
          <Typography variant="h5" sx={{ mb: 3, fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 1 }}>
            <Co2Outlined />
            Blockchain Verification & Environmental Impact
          </Typography>
          <CarbonSavingsCertificate
            certificates={demoResult?.blockchain_certificates || []}
            environmentalImpact={demoResult?.environmental_impact}
            loading={loading}
          />
        </Box>

        {/* Walmart Scale Impact Section */}
        {walmartImpact && (
          <Box>
            <Typography variant="h5" sx={{ mb: 3, fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 1 }}>
              <AttachMoneyOutlined />
              Walmart Scale Impact Projection
            </Typography>
            <Card
              sx={{
                background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
              }}
            >
              <CardContent sx={{ p: 4 }}>
                <Box
                  sx={{
                    display: 'flex',
                    flexDirection: { xs: 'column', md: 'row' },
                    gap: 4,
                    mb: 3,
                  }}
                >
                  <Box sx={{ flex: 1, textAlign: 'center' }}>
                    <Typography variant="h3" color="success.main" sx={{ fontWeight: 'bold' }}>
                      ${(walmartImpact.annual_cost_savings_usd / 1000000).toFixed(1)}M
                    </Typography>
                    <Typography variant="h6" color="text.secondary">
                      Annual Cost Savings
                    </Typography>
                  </Box>
                  <Divider orientation="vertical" flexItem />
                  <Box sx={{ flex: 1, textAlign: 'center' }}>
                    <Typography variant="h3" color="success.main" sx={{ fontWeight: 'bold' }}>
                      {(walmartImpact.annual_carbon_reduction_kg / 1000000).toFixed(1)}M
                    </Typography>
                    <Typography variant="h6" color="text.secondary">
                      Annual CO₂ Reduction (kg)
                    </Typography>
                  </Box>
                  <Divider orientation="vertical" flexItem />
                  <Box sx={{ flex: 1, textAlign: 'center' }}>
                    <Typography variant="h3" color="primary.main" sx={{ fontWeight: 'bold' }}>
                      {(walmartImpact.annual_time_savings_hours / 1000000).toFixed(1)}M
                    </Typography>
                    <Typography variant="h6" color="text.secondary">
                      Annual Time Savings (hours)
                    </Typography>
                  </Box>
                </Box>

                {/* Additional Metrics */}
                <Box
                  sx={{
                    display: 'flex',
                    flexDirection: { xs: 'column', md: 'row' },
                    justifyContent: 'space-around',
                    gap: 2,
                    p: 2,
                    bgcolor: 'rgba(255,255,255,0.8)',
                    borderRadius: 2,
                  }}
                >
                  <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h6" color="info.main">
                      {walmartImpact.roi_percent.toFixed(1)}%
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      ROI
                    </Typography>
                  </Box>
                  <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h6" color="info.main">
                      {walmartImpact.payback_period_months} months
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Payback Period
                    </Typography>
                  </Box>
                  <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h6" color="info.main">
                      {walmartImpact.stores_impacted.toLocaleString()}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Stores Impacted
                    </Typography>
                  </Box>
                  <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h6" color="info.main">
                      {(walmartImpact.confidence_level * 100).toFixed(0)}%
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Confidence Level
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Box>
        )}
      </Box>
    </Container>
  );
};

export default Dashboard;
