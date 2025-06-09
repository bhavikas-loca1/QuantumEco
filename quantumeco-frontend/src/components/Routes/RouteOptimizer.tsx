import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Alert,
  IconButton,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import {
  Add,
  Delete,
  ExpandMore,
  CompareArrows,
  LocationOn,
  LocalShipping,
  Science,
  TrendingUp,
  Refresh,
} from '@mui/icons-material';
import LoadingSpinner from '../Common/LoadingSpinner';
import RouteResults from './RouteResults';
import {
  optimizeRoutes,
  compareOptimizationMethods,
  getVehicleProfiles, // ✅ Now actually used
  formatApiError,
} from '../../Services/api';
import type {
  Location,
  Vehicle,
  OptimizationGoals,
  RouteOptimizationResponse,
  VehicleType,
  RouteComparisonResponse,
  VehicleProfileResponse, // ✅ Now used
} from '../../Services/types';

/**
 * RouteOptimizer Component
 * Purpose: Main interface for route optimization with dynamic vehicle profile loading
 * Features: Dynamic form inputs, optimization goals, method comparison, real vehicle profiles
 */
const RouteOptimizer: React.FC = () => {
  // State management
  const [locations, setLocations] = useState<Location[]>([
    {
      id: 'depot',
      name: 'Distribution Center',
      address: 'Walmart Distribution Center, Manhattan, NY',
      latitude: 40.7589,
      longitude: -73.9851,
      demand_kg: 0,
      priority: 1,
      time_window_start: '06:00',
      time_window_end: '22:00',
      delivery_type: 'standard',
    }
  ]);
  
  const [vehicles, setVehicles] = useState<Vehicle[]>([
    {
      id: 'vehicle_001',
      type: 'electric_van',
      capacity_kg: 500,
      cost_per_km: 0.65,
      emission_factor: 0.05,
      max_range_km: 300,
      availability_start: '08:00',
      availability_end: '18:00',
    }
  ]);

  const [optimizationGoals, setOptimizationGoals] = useState<OptimizationGoals>({
    cost: 0.4,
    carbon: 0.4,
    time: 0.2,
  });

  // ✅ NEW: Vehicle profiles state
  const [vehicleProfiles, setVehicleProfiles] = useState<VehicleProfileResponse | null>(null);
  const [profilesLoading, setProfilesLoading] = useState(false);
  const [profilesError, setProfilesError] = useState<string | null>(null);

  const [optimizing, setOptimizing] = useState(false);
  const [comparing, setComparing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [optimizationResult, setOptimizationResult] = useState<RouteOptimizationResponse | null>(null);
  const [comparisonResult, setComparisonResult] = useState<RouteComparisonResponse | null>(null);
  const [availableVehicleTypes] = useState<VehicleType[]>([
    'diesel_truck',
    'electric_van', 
    'hybrid_delivery',
    'gas_truck',
    'cargo_bike'
  ]);

  // ✅ NEW: Load vehicle profiles on component mount
  useEffect(() => {
    loadVehicleProfiles();
  }, []);

  // ✅ NEW: Function to load vehicle profiles from backend
  const loadVehicleProfiles = async () => {
    try {
      setProfilesLoading(true);
      setProfilesError(null);
      
      const profiles = await getVehicleProfiles();
      setVehicleProfiles(profiles);
      
      console.log('✅ Vehicle profiles loaded successfully:', profiles);
    } catch (err: any) {
      const errorMessage = formatApiError(err);
      setProfilesError(`Failed to load vehicle profiles: ${errorMessage}`);
      console.error('❌ Vehicle profiles loading failed:', err);
    } finally {
      setProfilesLoading(false);
    }
  };

  // Demo locations for NYC
  const demoLocations: Partial<Location>[] = [
    { name: 'Times Square Store', address: '1515 Broadway, New York, NY', latitude: 40.7580, longitude: -73.9855, demand_kg: 75 },
    { name: 'Brooklyn Heights', address: '100 Montague St, Brooklyn, NY', latitude: 40.6958, longitude: -73.9958, demand_kg: 50 },
    { name: 'Queens Center', address: '90-15 Queens Blvd, Elmhurst, NY', latitude: 40.7370, longitude: -73.8756, demand_kg: 85 },
    { name: 'Bronx Plaza', address: '610 Exterior St, Bronx, NY', latitude: 40.8176, longitude: -73.9182, demand_kg: 60 },
    { name: 'Staten Island Mall', address: '2655 Richmond Ave, Staten Island, NY', latitude: 40.5795, longitude: -74.1502, demand_kg: 45 },
  ];

  // Add demo locations
  const addDemoLocations = () => {
    const newLocations = demoLocations.map((demo, index) => ({
      id: `demo_loc_${index + 1}`,
      name: demo.name || `Location ${index + 1}`,
      address: demo.address || 'NYC Location',
      latitude: demo.latitude || 40.7128,
      longitude: demo.longitude || -74.0060,
      demand_kg: demo.demand_kg || 50,
      priority: Math.floor(Math.random() * 5) + 1,
      time_window_start: '09:00',
      time_window_end: '17:00',
      delivery_type: 'standard' as const,
    }));
    
    setLocations(prev => [...prev, ...newLocations]);
  };

  // Add new location
  const addLocation = () => {
    const newLocation: Location = {
      id: `loc_${Date.now()}`,
      name: `Location ${locations.length}`,
      address: 'Enter address',
      latitude: 40.7128,
      longitude: -74.0060,
      demand_kg: 50,
      priority: 1,
      time_window_start: '09:00',
      time_window_end: '17:00',
      delivery_type: 'standard',
    };
    setLocations([...locations, newLocation]);
  };

  // Remove location
  const removeLocation = (id: string) => {
    if (locations.length > 1) {
      setLocations(locations.filter(loc => loc.id !== id));
    }
  };

  // Update location
  const updateLocation = (id: string, field: keyof Location, value: any) => {
    setLocations(locations.map(loc => 
      loc.id === id ? { ...loc, [field]: value } : loc
    ));
  };

  // Add new vehicle
  const addVehicle = () => {
    const newVehicle: Vehicle = {
      id: `vehicle_${Date.now()}`,
      type: 'electric_van',
      capacity_kg: 500,
      cost_per_km: 0.65,
      emission_factor: 0.05,
      max_range_km: 300,
      availability_start: '08:00',
      availability_end: '18:00',
    };
    setVehicles([...vehicles, newVehicle]);
  };

  // Remove vehicle
  const removeVehicle = (id: string) => {
    if (vehicles.length > 1) {
      setVehicles(vehicles.filter(veh => veh.id !== id));
    }
  };

  // Update vehicle
  const updateVehicle = (id: string, field: keyof Vehicle, value: any) => {
    setVehicles(vehicles.map(veh => 
      veh.id === id ? { ...veh, [field]: value } : veh
    ));
  };

  // ✅ NEW: Get vehicle specifications from loaded profiles or fallback to hardcoded
  const getVehicleSpecs = (type: VehicleType) => {
    // Try to use loaded vehicle profiles first
    if (vehicleProfiles?.vehicle_profiles?.[type]) {
      const profile = vehicleProfiles.vehicle_profiles[type];
      return {
        capacity: profile.capacity_kg,
        cost: profile.cost_per_km,
        emission: profile.emission_factor,
        range: profile.max_range_km || 300,
      };
    }

    // Fallback to hardcoded specs if profiles not loaded
    const fallbackSpecs = {
      diesel_truck: { capacity: 1000, cost: 0.85, emission: 0.27, range: 800 },
      electric_van: { capacity: 500, cost: 0.65, emission: 0.05, range: 300 },
      hybrid_delivery: { capacity: 750, cost: 0.75, emission: 0.12, range: 600 },
      gas_truck: { capacity: 800, cost: 0.80, emission: 0.23, range: 700 },
      cargo_bike: { capacity: 50, cost: 0.25, emission: 0.01, range: 80 },
    };
    
    return fallbackSpecs[type];
  };

  // ✅ NEW: Get vehicle display name from profiles
  const getVehicleDisplayName = (type: VehicleType) => {
    if (vehicleProfiles?.vehicle_profiles?.[type]) {
      return vehicleProfiles.vehicle_profiles[type].display_name;
    }
    return type.replace('_', ' ').toUpperCase();
  };

  // ✅ NEW: Get vehicle environmental impact from profiles
  const getVehicleEnvironmentalInfo = (type: VehicleType) => {
    if (vehicleProfiles?.vehicle_profiles?.[type]) {
      const profile = vehicleProfiles.vehicle_profiles[type];
      return {
        efficiency: profile.efficiency_rating,
        impact: profile.environmental_impact,
        fuelType: profile.fuel_type,
      };
    }
    return {
      efficiency: 'Standard',
      impact: 'Medium environmental impact',
      fuelType: 'Mixed',
    };
  };

  // Update vehicle type with dynamic specs
  const updateVehicleType = (id: string, type: VehicleType) => {
    const specs = getVehicleSpecs(type);
    setVehicles(vehicles.map(veh => 
      veh.id === id ? {
        ...veh,
        type,
        capacity_kg: specs.capacity,
        cost_per_km: specs.cost,
        emission_factor: specs.emission,
        max_range_km: specs.range,
      } : veh
    ));
  };

  // Run optimization
  const runOptimization = async () => {
    try {
      setOptimizing(true);
      setError(null);
      
      const result = await optimizeRoutes(locations, vehicles, optimizationGoals);
      setOptimizationResult(result);
    } catch (err: any) {
      const errorMessage = formatApiError(err);
      setError(`Optimization failed: ${errorMessage}`);
    } finally {
      setOptimizing(false);
    }
  };

  // Compare methods
  const runComparison = async () => {
    try {
      setComparing(true);
      setError(null);
      
      const result = await compareOptimizationMethods(locations, vehicles);
      setComparisonResult(result);
    } catch (err: any) {
      const errorMessage = formatApiError(err);
      setError(`Comparison failed: ${errorMessage}`);
    } finally {
      setComparing(false);
    }
  };

  // Validate optimization goals sum to 1.0
  const updateOptimizationGoal = (key: keyof OptimizationGoals, value: number) => {
    const newGoals = { ...optimizationGoals, [key]: value };
    const total = Object.values(newGoals).reduce((sum, val) => sum + val, 0);
    
    if (Math.abs(total - 1.0) <= 0.01) {
      setOptimizationGoals(newGoals);
    }
  };

  return (
    <Container maxWidth="xl" sx={{ py: 3 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', mb: 1 }}>
          🛣️ Quantum Route Optimizer
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Configure locations and vehicles for quantum-inspired route optimization
        </Typography>
        
        {/* ✅ NEW: Vehicle Profiles Status */}
        <Box sx={{ mt: 2, display: 'flex', alignItems: 'center', gap: 2 }}>
          {profilesLoading && (
            <Chip 
              label="Loading vehicle profiles..." 
              color="info" 
              size="small" 
              icon={<LoadingSpinner />} 
            />
          )}
          {vehicleProfiles && !profilesLoading && (
            <Chip 
              label={`✅ ${vehicleProfiles.total_profiles || 5} vehicle profiles loaded`} 
              color="success" 
              size="small" 
            />
          )}
          {profilesError && (
            <Chip 
              label="Using fallback vehicle specs" 
              color="warning" 
              size="small" 
            />
          )}
          <Button
            size="small"
            startIcon={<Refresh />}
            onClick={loadVehicleProfiles}
            disabled={profilesLoading}
          >
            Refresh Profiles
          </Button>
        </Box>
      </Box>

      {/* Error Alerts */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {profilesError && (
        <Alert severity="warning" sx={{ mb: 3 }} onClose={() => setProfilesError(null)}>
          {profilesError}
        </Alert>
      )}

      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
        {/* Quick Demo Section */}
        <Card>
          <CardContent>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">🎯 Quick Demo Setup</Typography>
              <Button
                variant="outlined"
                startIcon={<Add />}
                onClick={addDemoLocations}
                disabled={optimizing || comparing}
              >
                Add NYC Demo Locations
              </Button>
            </Box>
            <Typography variant="body2" color="text.secondary">
              Quickly add realistic NYC delivery locations for demonstration
            </Typography>
          </CardContent>
        </Card>

        {/* Optimization Goals */}
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <TrendingUp />
              Optimization Goals (must sum to 1.0)
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3, mt: 2 }}>
              <TextField
                label="Cost Weight"
                type="number"
                value={optimizationGoals.cost}
                onChange={(e) => updateOptimizationGoal('cost', parseFloat(e.target.value) || 0)}
                inputProps={{ min: 0, max: 1, step: 0.1 }}
                sx={{ flex: 1 }}
              />
              <TextField
                label="Carbon Weight"
                type="number"
                value={optimizationGoals.carbon}
                onChange={(e) => updateOptimizationGoal('carbon', parseFloat(e.target.value) || 0)}
                inputProps={{ min: 0, max: 1, step: 0.1 }}
                sx={{ flex: 1 }}
              />
              <TextField
                label="Time Weight"
                type="number"
                value={optimizationGoals.time}
                onChange={(e) => updateOptimizationGoal('time', parseFloat(e.target.value) || 0)}
                inputProps={{ min: 0, max: 1, step: 0.1 }}
                sx={{ flex: 1 }}
              />
            </Box>
            <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
              Total: {Object.values(optimizationGoals).reduce((sum, val) => sum + val, 0).toFixed(2)}
            </Typography>
          </CardContent>
        </Card>

        {/* Locations Configuration */}
        <Card>
          <CardContent>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
              <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <LocationOn />
                Delivery Locations ({locations.length})
              </Typography>
              <Button
                variant="outlined"
                startIcon={<Add />}
                onClick={addLocation}
                disabled={optimizing || comparing}
              >
                Add Location
              </Button>
            </Box>

            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              {locations.map((location, index) => (
                <Accordion key={location.id} defaultExpanded={index === 0}>
                  <AccordionSummary expandIcon={<ExpandMore />}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
                      <Typography sx={{ fontWeight: 'bold' }}>
                        {location.name || `Location ${index + 1}`}
                      </Typography>
                      <Chip 
                        label={`${location.demand_kg}kg`} 
                        size="small" 
                        color="primary" 
                        variant="outlined" 
                      />
                      {location.id === 'depot' && (
                        <Chip label="Depot" size="small" color="success" />
                      )}
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2 }}>
                        <TextField
                          label="Location Name"
                          value={location.name}
                          onChange={(e) => updateLocation(location.id, 'name', e.target.value)}
                          sx={{ flex: 1 }}
                        />
                        <TextField
                          label="Address"
                          value={location.address}
                          onChange={(e) => updateLocation(location.id, 'address', e.target.value)}
                          sx={{ flex: 2 }}
                        />
                      </Box>
                      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2 }}>
                        <TextField
                          label="Latitude"
                          type="number"
                          value={location.latitude}
                          onChange={(e) => updateLocation(location.id, 'latitude', parseFloat(e.target.value))}
                          sx={{ flex: 1 }}
                        />
                        <TextField
                          label="Longitude"
                          type="number"
                          value={location.longitude}
                          onChange={(e) => updateLocation(location.id, 'longitude', parseFloat(e.target.value))}
                          sx={{ flex: 1 }}
                        />
                        <TextField
                          label="Demand (kg)"
                          type="number"
                          value={location.demand_kg}
                          onChange={(e) => updateLocation(location.id, 'demand_kg', parseFloat(e.target.value))}
                          sx={{ flex: 1 }}
                        />
                        <TextField
                          label="Priority"
                          type="number"
                          value={location.priority}
                          onChange={(e) => updateLocation(location.id, 'priority', parseInt(e.target.value))}
                          inputProps={{ min: 1, max: 5 }}
                          sx={{ flex: 1 }}
                        />
                      </Box>
                      {location.id !== 'depot' && (
                        <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                          <IconButton
                            color="error"
                            onClick={() => removeLocation(location.id)}
                            disabled={optimizing || comparing}
                          >
                            <Delete />
                          </IconButton>
                        </Box>
                      )}
                    </Box>
                  </AccordionDetails>
                </Accordion>
              ))}
            </Box>
          </CardContent>
        </Card>

        {/* ✅ ENHANCED: Vehicles Configuration with Dynamic Profiles */}
        <Card>
          <CardContent>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
              <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <LocalShipping />
                Vehicle Fleet ({vehicles.length})
              </Typography>
              <Button
                variant="outlined"
                startIcon={<Add />}
                onClick={addVehicle}
                disabled={optimizing || comparing}
              >
                Add Vehicle
              </Button>
            </Box>

            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              {vehicles.map((vehicle, index) => {
                const envInfo = getVehicleEnvironmentalInfo(vehicle.type);
                
                return (
                  <Accordion key={vehicle.id}>
                    <AccordionSummary expandIcon={<ExpandMore />}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        <Typography sx={{ fontWeight: 'bold' }}>
                          Vehicle {index + 1} ({getVehicleDisplayName(vehicle.type)})
                        </Typography>
                        <Chip 
                          label={`${vehicle.capacity_kg}kg capacity`} 
                          size="small" 
                          color="primary" 
                          variant="outlined" 
                        />
                        <Chip 
                          label={`$${vehicle.cost_per_km}/km`} 
                          size="small" 
                          color="secondary" 
                          variant="outlined" 
                        />
                        <Chip 
                          label={envInfo.efficiency} 
                          size="small" 
                          color="success" 
                          variant="outlined" 
                        />
                      </Box>
                    </AccordionSummary>
                    <AccordionDetails>
                      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                        <FormControl sx={{ flex: 1 }}>
                          <InputLabel>Vehicle Type</InputLabel>
                          <Select
                            value={vehicle.type}
                            label="Vehicle Type"
                            onChange={(e) => updateVehicleType(vehicle.id, e.target.value as VehicleType)}
                          >
                            {availableVehicleTypes.map((type) => (
                              <MenuItem key={type} value={type}>
                                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                                  <Typography>{getVehicleDisplayName(type)}</Typography>
                                  <Typography variant="caption" color="text.secondary">
                                    {getVehicleEnvironmentalInfo(type).impact}
                                  </Typography>
                                </Box>
                              </MenuItem>
                            ))}
                          </Select>
                        </FormControl>

                        {/* ✅ NEW: Environmental Impact Display */}
                        <Box sx={{ 
                          p: 2, 
                          bgcolor: 'success.50', 
                          borderRadius: 1,
                          border: '1px solid',
                          borderColor: 'success.200'
                        }}>
                          <Typography variant="subtitle2" color="success.main" gutterBottom>
                            🌱 Environmental Profile
                          </Typography>
                          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                            <Chip label={`Fuel: ${envInfo.fuelType}`} size="small" />
                            <Chip label={`Efficiency: ${envInfo.efficiency}`} size="small" />
                            <Chip label={`${vehicle.emission_factor} kg CO₂/km`} size="small" />
                          </Box>
                          <Typography variant="caption" sx={{ mt: 1, display: 'block' }}>
                            {envInfo.impact}
                          </Typography>
                        </Box>

                        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2 }}>
                          <TextField
                            label="Capacity (kg)"
                            type="number"
                            value={vehicle.capacity_kg}
                            onChange={(e) => updateVehicle(vehicle.id, 'capacity_kg', parseFloat(e.target.value))}
                            sx={{ flex: 1 }}
                          />
                          <TextField
                            label="Cost per km ($)"
                            type="number"
                            value={vehicle.cost_per_km}
                            onChange={(e) => updateVehicle(vehicle.id, 'cost_per_km', parseFloat(e.target.value))}
                            sx={{ flex: 1 }}
                          />
                          <TextField
                            label="Emission Factor"
                            type="number"
                            value={vehicle.emission_factor}
                            onChange={(e) => updateVehicle(vehicle.id, 'emission_factor', parseFloat(e.target.value))}
                            sx={{ flex: 1 }}
                          />
                          <TextField
                            label="Max Range (km)"
                            type="number"
                            value={vehicle.max_range_km}
                            onChange={(e) => updateVehicle(vehicle.id, 'max_range_km', parseFloat(e.target.value))}
                            sx={{ flex: 1 }}
                          />
                        </Box>
                        <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                          <IconButton
                            color="error"
                            onClick={() => removeVehicle(vehicle.id)}
                            disabled={optimizing || comparing || vehicles.length === 1}
                          >
                            <Delete />
                          </IconButton>
                        </Box>
                      </Box>
                    </AccordionDetails>
                  </Accordion>
                );
              })}
            </Box>
          </CardContent>
        </Card>

        {/* Action Buttons */}
        <Card>
          <CardContent>
            <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3, alignItems: 'center' }}>
              <Button
                variant="contained"
                size="large"
                startIcon={optimizing ? <LoadingSpinner /> : <Science />}
                onClick={runOptimization}
                disabled={optimizing || comparing || locations.length < 2}
                sx={{ flex: 1, py: 2 }}
              >
                {optimizing ? 'Optimizing Routes...' : 'Run Quantum Optimization'}
              </Button>
              
              <Button
                variant="outlined"
                size="large"
                startIcon={comparing ? <LoadingSpinner /> : <CompareArrows />}
                onClick={runComparison}
                disabled={optimizing || comparing || locations.length < 2}
                sx={{ flex: 1, py: 2 }}
              >
                {comparing ? 'Comparing Methods...' : 'Compare Methods'}
              </Button>
            </Box>
            
            <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', mt: 2 }}>
              Minimum 2 locations required for optimization
            </Typography>
          </CardContent>
        </Card>

        {/* Results */}
        {(optimizationResult || comparisonResult) && (
          <RouteResults 
            optimizationResult={optimizationResult}
            comparisonResult={comparisonResult}
            locations={locations}
            vehicles={vehicles}
          />
        )}
      </Box>
    </Container>
  );
};

export default RouteOptimizer;
