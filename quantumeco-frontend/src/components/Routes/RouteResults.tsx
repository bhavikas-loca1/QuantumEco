import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  Divider,
  Alert,
  LinearProgress,
  Avatar,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Collapse,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import {
  TrendingUp,
  ScienceOutlined,
  AttachMoneyOutlined,
  AccessTimeOutlined,
  LocalShippingOutlined,
  StarOutlined,
  CheckCircleOutlined,
  RouteOutlined,
  CompareArrows,
  ExpandMore,
  Visibility,
  ExpandLess,
  Co2Outlined,
} from '@mui/icons-material';
import type {
  RouteOptimizationResponse,
  RouteComparisonResponse,
  Location,
  Vehicle,
} from '../../Services/types';

interface RouteResultsProps {
  optimizationResult?: RouteOptimizationResponse | null;
  comparisonResult?: RouteComparisonResponse | null;
  locations: Location[];
  vehicles: Vehicle[];
}

// ONLY FIX: Safe toFixed function to handle JavaScript rounding errors
const safeToFixed = (value: any, decimals: number = 2): string => {
  if (value === null || value === undefined || typeof value !== 'number' || isNaN(value)) {
    return '0.00';
  }
  
  // Fix for JavaScript toFixed() rounding errors
  const valueStr = value.toString();
  if (valueStr.includes('.')) {
    const fixedValue = Number(valueStr + '1').toFixed(decimals);
    return fixedValue;
  }
  
  return value.toFixed(decimals);
};

/**
 * RouteResults Component  
 * Purpose: Display optimization results matching actual backend RouteOptimizer response
 * Features: Results visualization, performance metrics, route details with location indices
 */
const RouteResults: React.FC<RouteResultsProps> = ({
  optimizationResult,
  comparisonResult,
  locations,
  vehicles,
}) => {
  const [showRouteDetails, setShowRouteDetails] = useState(false);
  const [expandedRoute, setExpandedRoute] = useState<string | null>(null);

  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = Math.round(minutes % 60);
    return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
  };

  const formatDistance = (km: number) => {
    return `${safeToFixed(km, 1)} km`;
  };

  const formatCurrency = (amount: number) => {
    return `$${safeToFixed(amount, 2)}`;
  };

  // ✅ Fixed: Handle location lookup by index (as returned by backend)
  const getLocationName = (locationIndex: number) => {
    if (typeof locationIndex === 'number' && locations[locationIndex]) {
      return locations[locationIndex].name || locations[locationIndex].address || `Location ${locationIndex}`;
    }
    return `Location ${locationIndex}`;
  };

  const getVehicleName = (vehicleId: string) => {
    const vehicle = vehicles.find(v => v.id === vehicleId || vehicleId.includes(v.id));
    return vehicle?.type.replace('_', ' ').toUpperCase() || vehicleId;
  };

  // ✅ Fixed: Get routes from actual backend structure
  const getOptimizedRoutes = () => {
    if (optimizationResult?.optimized_routes) return optimizationResult.optimized_routes;
    if (comparisonResult?.quantum_inspired_result?.optimized_routes) return comparisonResult.quantum_inspired_result.optimized_routes;
    return [];
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
      {/* Single Optimization Results */}
      {optimizationResult && (
        <Card>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
              <Typography variant="h5" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <StarOutlined color="primary" />
                Quantum-Inspired Optimization Results
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                <Chip 
                  label={optimizationResult.status} 
                  color={optimizationResult.status === 'completed' ? 'success' : 'warning'} 
                  icon={<CheckCircleOutlined />}
                />
                <Chip 
                  label={`${safeToFixed(optimizationResult.processing_time, 1)}s`} 
                  variant="outlined" 
                  icon={<AccessTimeOutlined />}
                />
                <Chip 
                  label={optimizationResult.method || 'quantum_inspired'} 
                  variant="outlined" 
                  color="secondary"
                />
              </Box>
            </Box>

            {/* Overall Metrics Cards */}
            <Box
              sx={{
                display: 'flex',
                flexDirection: { xs: 'column', sm: 'row' },
                gap: 2,
                mb: 4,
              }}
            >
              <Card variant="outlined" sx={{ flex: 1 }}>
                <CardContent sx={{ textAlign: 'center', py: 2 }}>
                  <Avatar sx={{ bgcolor: 'success.main', mx: 'auto', mb: 1, width: 48, height: 48 }}>
                    <AttachMoneyOutlined />
                  </Avatar>
                  <Typography variant="h4" color="success.main" sx={{ fontWeight: 'bold' }}>
                    {formatCurrency(optimizationResult.total_cost)}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total Cost
                  </Typography>
                </CardContent>
              </Card>

              <Card variant="outlined" sx={{ flex: 1 }}>
                <CardContent sx={{ textAlign: 'center', py: 2 }}>
                  <Avatar sx={{ bgcolor: 'info.main', mx: 'auto', mb: 1, width: 48, height: 48 }}>
                    <Co2Outlined />
                  </Avatar>
                  <Typography variant="h4" color="info.main" sx={{ fontWeight: 'bold' }}>
                    {safeToFixed(optimizationResult.total_carbon, 1)} kg
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Carbon Emissions
                  </Typography>
                </CardContent>
              </Card>

              <Card variant="outlined" sx={{ flex: 1 }}>
                <CardContent sx={{ textAlign: 'center', py: 2 }}>
                  <Avatar sx={{ bgcolor: 'warning.main', mx: 'auto', mb: 1, width: 48, height: 48 }}>
                    <AccessTimeOutlined />
                  </Avatar>
                  <Typography variant="h4" color="warning.main" sx={{ fontWeight: 'bold' }}>
                    {formatDuration(optimizationResult.total_time)}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total Time
                  </Typography>
                </CardContent>
              </Card>

              <Card variant="outlined" sx={{ flex: 1 }}>
                <CardContent sx={{ textAlign: 'center', py: 2 }}>
                  <Avatar sx={{ bgcolor: 'primary.main', mx: 'auto', mb: 1, width: 48, height: 48 }}>
                    <RouteOutlined />
                  </Avatar>
                  <Typography variant="h4" color="primary.main" sx={{ fontWeight: 'bold' }}>
                    {formatDistance(optimizationResult.total_distance)}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total Distance
                  </Typography>
                </CardContent>
              </Card>
            </Box>

            {/* Quantum Improvement Score */}
            {typeof optimizationResult.quantum_improvement_score === 'number' && (
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <ScienceOutlined />
                  Quantum Improvement Analysis
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
                  <LinearProgress
                    variant="determinate"
                    value={Math.min(optimizationResult.quantum_improvement_score, 100)}
                    sx={{ 
                      flex: 1, 
                      height: 12, 
                      borderRadius: 6,
                      bgcolor: 'grey.200',
                      '& .MuiLinearProgress-bar': {
                        bgcolor: optimizationResult.quantum_improvement_score >= 90 ? 'success.main' : 
                                optimizationResult.quantum_improvement_score >= 75 ? 'info.main' : 'warning.main'
                      }
                    }}
                  />
                  <Typography variant="h6" color="primary.main" sx={{ minWidth: 80 }}>
                    {safeToFixed(optimizationResult.quantum_improvement_score, 1)}%
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Quantum enhancement score showing improvement over traditional routing methods
                </Typography>
              </Box>
            )}

            {/* Savings Analysis */}
            {optimizationResult.savings_analysis && (
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <TrendingUp />
                  Savings Analysis
                </Typography>
                <Box
                  sx={{
                    display: 'flex',
                    flexDirection: { xs: 'column', md: 'row' },
                    gap: 2,
                  }}
                >
                  <Card variant="outlined" sx={{ flex: 1, bgcolor: 'success.50' }}>
                    <CardContent sx={{ py: 2 }}>
                      <Typography variant="h5" color="success.main" sx={{ fontWeight: 'bold' }}>
                        {formatCurrency(optimizationResult.savings_analysis.cost_saved_usd)}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Cost Saved ({safeToFixed(optimizationResult.savings_analysis.cost_improvement_percent, 1)}% improvement)
                      </Typography>
                    </CardContent>
                  </Card>

                  <Card variant="outlined" sx={{ flex: 1, bgcolor: 'info.50' }}>
                    <CardContent sx={{ py: 2 }}>
                      <Typography variant="h5" color="info.main" sx={{ fontWeight: 'bold' }}>
                        {safeToFixed(optimizationResult.savings_analysis.carbon_saved_kg, 1)} kg
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Carbon Saved ({safeToFixed(optimizationResult.savings_analysis.carbon_improvement_percent, 1)}% improvement)
                      </Typography>
                    </CardContent>
                  </Card>

                  <Card variant="outlined" sx={{ flex: 1, bgcolor: 'warning.50' }}>
                    <CardContent sx={{ py: 2 }}>
                      <Typography variant="h5" color="warning.main" sx={{ fontWeight: 'bold' }}>
                        {formatDuration(optimizationResult.savings_analysis.time_saved_minutes)}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Time Saved ({safeToFixed(optimizationResult.savings_analysis.time_improvement_percent, 1)}% improvement)
                      </Typography>
                    </CardContent>
                  </Card>
                </Box>
              </Box>
            )}
          </CardContent>
        </Card>
      )}

      {/* Method Comparison Results */}
      {comparisonResult && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <CompareArrows />
              Optimization Method Comparison
            </Typography>
            
            <Box
              sx={{
                display: 'flex',
                flexDirection: { xs: 'column', lg: 'row' },
                gap: 3,
                mt: 2,
              }}
            >
              {/* Traditional Method Results */}
              <Card variant="outlined" sx={{ flex: 1 }}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                    <Typography variant="h6" color="text.secondary">
                      Traditional Routing
                    </Typography>
                    <Chip 
                      label={comparisonResult.traditional_result.status} 
                      size="small"
                      color={comparisonResult.traditional_result.status === 'success' ? 'default' : 'error'}
                    />
                  </Box>
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2" color="text.secondary">Cost:</Typography>
                      <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                        {formatCurrency(comparisonResult.traditional_result.total_cost || 0)}
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2" color="text.secondary">Carbon:</Typography>
                      <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                        {safeToFixed(comparisonResult.traditional_result.total_carbon || 0, 1)} kg
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2" color="text.secondary">Time:</Typography>
                      <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                        {formatDuration(comparisonResult.traditional_result.total_time || 0)}
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2" color="text.secondary">Distance:</Typography>
                      <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                        {formatDistance(comparisonResult.traditional_result.total_distance || 0)}
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2" color="text.secondary">Processing:</Typography>
                      <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                        {safeToFixed(comparisonResult.traditional_result.processing_time || 0, 1)}s
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>

              {/* Quantum Method Results */}
              <Card variant="outlined" sx={{ flex: 1, bgcolor: 'primary.50', border: '2px solid', borderColor: 'primary.main' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                    <Typography variant="h6" color="primary.main" sx={{ fontWeight: 'bold' }}>
                      Quantum-Inspired Routing
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <Chip 
                        label={comparisonResult.quantum_inspired_result.status} 
                        size="small"
                        color={comparisonResult.quantum_inspired_result.status === 'success' ? 'success' : 'error'}
                      />
                      {comparisonResult.winner === 'quantum_inspired' && (
                        <Chip label="WINNER" size="small" color="success" icon={<StarOutlined />} />
                      )}
                    </Box>
                  </Box>
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2" color="text.secondary">Cost:</Typography>
                      <Typography variant="body2" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                        {formatCurrency(comparisonResult.quantum_inspired_result.total_cost || 0)}
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2" color="text.secondary">Carbon:</Typography>
                      <Typography variant="body2" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                        {safeToFixed(comparisonResult.quantum_inspired_result.total_carbon || 0, 1)} kg
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2" color="text.secondary">Time:</Typography>
                      <Typography variant="body2" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                        {formatDuration(comparisonResult.quantum_inspired_result.total_time || 0)}
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2" color="text.secondary">Distance:</Typography>
                      <Typography variant="body2" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                        {formatDistance(comparisonResult.quantum_inspired_result.total_distance || 0)}
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2" color="text.secondary">Processing:</Typography>
                      <Typography variant="body2" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                        {safeToFixed(comparisonResult.quantum_inspired_result.processing_time || 0, 1)}s
                      </Typography>
                    </Box>
                    {comparisonResult.quantum_inspired_result.quantum_score && (
                      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                        <Typography variant="body2" color="text.secondary">Quantum Score:</Typography>
                        <Chip 
                          label={`${safeToFixed(comparisonResult.quantum_inspired_result.quantum_score, 0)}%`} 
                          size="small" 
                          color="success"
                        />
                      </Box>
                    )}
                  </Box>
                </CardContent>
              </Card>

              {/* Improvements Summary */}
              {comparisonResult.improvements && (
                <Card variant="outlined" sx={{ flex: 1, bgcolor: 'success.50' }}>
                  <CardContent>
                    <Typography variant="h6" color="success.main" gutterBottom sx={{ fontWeight: 'bold' }}>
                      Quantum Improvements
                    </Typography>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                        <Typography variant="body2" color="text.secondary">Cost Improvement:</Typography>
                        <Typography variant="body2" sx={{ fontWeight: 'bold', color: 'success.main' }}>
                          {safeToFixed(comparisonResult.improvements.cost_improvement_percent, 1)}%
                        </Typography>
                      </Box>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                        <Typography variant="body2" color="text.secondary">Carbon Reduction:</Typography>
                        <Typography variant="body2" sx={{ fontWeight: 'bold', color: 'success.main' }}>
                          {safeToFixed(comparisonResult.improvements.carbon_improvement_percent, 1)}%
                        </Typography>
                      </Box>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                        <Typography variant="body2" color="text.secondary">Time Reduction:</Typography>
                        <Typography variant="body2" sx={{ fontWeight: 'bold', color: 'success.main' }}>
                          {safeToFixed(comparisonResult.improvements.time_improvement_percent, 1)}%
                        </Typography>
                      </Box>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                        <Typography variant="body2" color="text.secondary">Distance Saved:</Typography>
                        <Typography variant="body2" sx={{ fontWeight: 'bold', color: 'success.main' }}>
                          {safeToFixed(comparisonResult.improvements.distance_improvement_percent, 1)}%
                        </Typography>
                      </Box>
                      <Divider sx={{ my: 1 }} />
                      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                        <Typography variant="body2" color="text.secondary">Overall:</Typography>
                        <Chip 
                          label={`${safeToFixed(comparisonResult.improvements.overall_improvement_percent, 1)}% better`} 
                          size="small" 
                          color="success"
                          icon={<TrendingUp />}
                        />
                      </Box>
                    </Box>
                  </CardContent>
                </Card>
              )}
            </Box>

            {/* Algorithm Details */}
            {comparisonResult.algorithm_details && (
              <Box sx={{ mt: 3 }}>
                <Accordion>
                  <AccordionSummary expandIcon={<ExpandMore />}>
                    <Typography variant="subtitle1" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <ScienceOutlined />
                      Quantum Algorithm Details
                    </Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
                      <Box sx={{ flex: 1 }}>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          Quantum Iterations: <strong>{comparisonResult.algorithm_details.quantum_iterations}</strong>
                        </Typography>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          Tunnel Probability: <strong>{safeToFixed(comparisonResult.algorithm_details.quantum_tunnel_probability * 100, 1)}%</strong>
                        </Typography>
                      </Box>
                      <Box sx={{ flex: 1 }}>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          Annealing Temperature: <strong>{safeToFixed(comparisonResult.algorithm_details.annealing_temperature, 1)}°</strong>
                        </Typography>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          Convergence: <strong>{comparisonResult.algorithm_details.convergence_achieved ? 'Achieved' : 'Partial'}</strong>
                        </Typography>
                      </Box>
                    </Box>
                  </AccordionDetails>
                </Accordion>
              </Box>
            )}
          </CardContent>
        </Card>
      )}

      {/* ✅ FIXED: Route Details Table - Using actual backend response structure */}
      {getOptimizedRoutes().length > 0 && (
        <Card>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
              <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <LocalShippingOutlined />
                Optimized Route Details ({getOptimizedRoutes().length} routes)
              </Typography>
              <Button
                variant="outlined"
                size="small"
                startIcon={showRouteDetails ? <ExpandLess /> : <Visibility />}
                onClick={() => setShowRouteDetails(!showRouteDetails)}
              >
                {showRouteDetails ? 'Hide Details' : 'Show Details'}
              </Button>
            </Box>
            
            <Collapse in={showRouteDetails}>
              <TableContainer component={Paper} variant="outlined">
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell><strong>Vehicle</strong></TableCell>
                      <TableCell><strong>Route Path</strong></TableCell>
                      <TableCell align="right"><strong>Distance</strong></TableCell>
                      <TableCell align="right"><strong>Time</strong></TableCell>
                      <TableCell align="right"><strong>Cost</strong></TableCell>
                      <TableCell align="right"><strong>Carbon</strong></TableCell>
                      <TableCell align="right"><strong>Load</strong></TableCell>
                      <TableCell align="right"><strong>Utilization</strong></TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {getOptimizedRoutes().map((route, index) => (
                      <TableRow key={route.vehicle_id || index}>
                        <TableCell>
                          <Box>
                            <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                              {getVehicleName(route.vehicle_id)}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              {route.vehicle_id}
                            </Typography>
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Box sx={{ maxWidth: 200 }}>
                            <Button
                              size="small"
                              variant="text"
                              onClick={() => setExpandedRoute(expandedRoute === route.vehicle_id ? null : route.vehicle_id)}
                              sx={{ p: 0, textTransform: 'none' }}
                            >
                              {/* ✅ FIXED: Use 'route' field (array of location indices) from backend */}
                              {route.route ? `${route.route.length} stops` : 'View Route'}
                            </Button>
                            <Collapse in={expandedRoute === route.vehicle_id}>
                              <Box sx={{ mt: 1, pl: 1, borderLeft: '2px solid', borderColor: 'primary.main' }}>
                                {/* ✅ FIXED: Map over route array (location indices) */}
                                {route.route?.map((locationIndex, idx) => (
                                  <Typography key={idx} variant="caption" display="block" color="text.secondary">
                                    {idx + 1}. {getLocationName(locationIndex)}
                                  </Typography>
                                ))}
                              </Box>
                            </Collapse>
                          </Box>
                        </TableCell>
                        <TableCell align="right">{formatDistance(route.distance_km)}</TableCell>
                        <TableCell align="right">{formatDuration(route.time_minutes)}</TableCell>
                        <TableCell align="right">{formatCurrency(route.cost_usd)}</TableCell>
                        <TableCell align="right">{safeToFixed(route.carbon_kg, 1)} kg</TableCell>
                        <TableCell align="right">
                          <Typography variant="body2">{route.load_kg || 0} kg</Typography>
                        </TableCell>
                        <TableCell align="right">
                          <Box>
                            <LinearProgress
                              variant="determinate"
                              value={route.utilization_percent}
                              sx={{ mb: 0.5, height: 4 }}
                              color={route.utilization_percent > 90 ? 'error' : route.utilization_percent > 70 ? 'warning' : 'success'}
                            />
                            <Typography variant="caption" color="text.secondary">
                              {safeToFixed(route.utilization_percent, 0)}%
                            </Typography>
                          </Box>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Collapse>
          </CardContent>
        </Card>
      )}

      {/* Success Message */}
      {(optimizationResult || comparisonResult) && (
        <Alert severity="success" sx={{ mt: 2 }}>
          <Typography variant="h6" gutterBottom>
            ✅ Optimization Complete!
          </Typography>
          <Typography variant="body2">
            {optimizationResult && (
              <>Your routes have been optimized using quantum-inspired algorithms. </>
            )}
            {comparisonResult && (
              <>Method comparison shows quantum-inspired routing outperformed traditional methods by {safeToFixed(comparisonResult.improvements?.overall_improvement_percent || 0, 1)}%. </>
            )}
            {optimizationResult?.certificates && optimizationResult.certificates.length > 0 && 
              `${optimizationResult.certificates.length} blockchain certificate(s) have been generated for verification.`
            }
          </Typography>
        </Alert>
      )}
    </Box>
  );
};

export default RouteResults;
