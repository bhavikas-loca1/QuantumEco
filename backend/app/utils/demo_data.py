import random
import time
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import logging
from app.utils.helpers import (
    generate_demo_id, generate_route_id, calculate_distance,
    generate_random_coordinates, generate_hash
)

class DemoDataGenerator:
    """Generate realistic demo data for QuantumEco Intelligence platform"""
    
    def __init__(self):
        # NYC area coordinates
        self.nyc_center = (40.7128, -74.0060)
        self.nyc_radius = 50  # km
        
        # Vehicle types with realistic specifications
        self.vehicle_types = {
            "diesel_truck": {
                "capacity_kg": 1000,
                "cost_per_km": 0.85,
                "emission_factor": 0.27,
                "efficiency_rating": "C",
                "max_range_km": 800
            },
            "electric_van": {
                "capacity_kg": 500,
                "cost_per_km": 0.65,
                "emission_factor": 0.05,
                "efficiency_rating": "A+",
                "max_range_km": 300
            },
            "hybrid_delivery": {
                "capacity_kg": 750,
                "cost_per_km": 0.75,
                "emission_factor": 0.12,
                "efficiency_rating": "B+",
                "max_range_km": 600
            },
            "gas_truck": {
                "capacity_kg": 800,
                "cost_per_km": 0.80,
                "emission_factor": 0.23,
                "efficiency_rating": "C+",
                "max_range_km": 700
            },
            "cargo_bike": {
                "capacity_kg": 50,
                "cost_per_km": 0.25,
                "emission_factor": 0.01,
                "efficiency_rating": "A++",
                "max_range_km": 80
            }
        }
        
        # NYC borough data
        self.nyc_boroughs = {
            "Manhattan": {"center": (40.7831, -73.9712), "radius": 15},
            "Brooklyn": {"center": (40.6782, -73.9442), "radius": 20},
            "Queens": {"center": (40.7282, -73.7949), "radius": 25},
            "Bronx": {"center": (40.8448, -73.8648), "radius": 18},
            "Staten Island": {"center": (40.5795, -74.1502), "radius": 15}
        }
        
        # Street names for realistic addresses
        self.street_names = [
            "Broadway", "Main St", "Park Ave", "First Ave", "Second Ave",
            "Third Ave", "Lexington Ave", "Madison Ave", "Fifth Ave",
            "Sixth Ave", "Seventh Ave", "Eighth Ave", "Ninth Ave",
            "Wall St", "Canal St", "Houston St", "14th St", "23rd St",
            "34th St", "42nd St", "57th St", "72nd St", "86th St",
            "96th St", "110th St", "125th St", "Atlantic Ave",
            "Flatbush Ave", "Ocean Ave", "Kings Highway", "Bay Ridge Ave"
        ]
        
        # Company names for delivery destinations
        self.company_names = [
            "Acme Corp", "Global Industries", "Tech Solutions Inc",
            "Metro Services", "Urban Logistics", "City Markets",
            "Downtown Retail", "Midtown Office", "Financial Center",
            "Medical Plaza", "Shopping Center", "Business Park",
            "Industrial Complex", "Residential Tower", "Hotel Chain",
            "Restaurant Group", "Pharmacy Network", "Grocery Chain"
        ]
    
    def generate_walmart_nyc_scenario(self, num_locations: int = 50, 
                                    num_vehicles: int = 5) -> Dict[str, Any]:
        """Generate comprehensive Walmart NYC delivery scenario"""
        
        # Configure logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger('WalmartNYCScenario')
        
        try:
            logger.info(f"Starting Walmart NYC scenario generation with {num_locations} locations and {num_vehicles} vehicles")
            
            # Input validation
            if num_locations <= 0 or num_vehicles <= 0:
                raise ValueError("Number of locations and vehicles must be positive")
            
            if num_vehicles > num_locations:
                raise ValueError("Number of vehicles cannot exceed number of locations")
            
            scenario_id = generate_demo_id()
            logger.debug(f"Generated scenario ID: {scenario_id}")
            
            try:
                logger.info("Generating NYC delivery locations...")
                locations = self._generate_nyc_locations(num_locations)
                logger.debug(f"Successfully generated {len(locations)} locations")
            except Exception as e:
                logger.error(f"Failed to generate locations: {str(e)}")
                raise
            
            try:
                logger.info("Generating Walmart vehicle fleet...")
                vehicles = self._generate_walmart_fleet(num_vehicles)
                logger.debug(f"Successfully generated {len(vehicles)} vehicles")
            except Exception as e:
                logger.error(f"Failed to generate vehicle fleet: {str(e)}")
                raise
            
            logger.info("Starting optimization simulations...")
            try:
                traditional_result = self._simulate_traditional_optimization(locations, vehicles)
                logger.debug(f"Traditional optimization complete. Score: {traditional_result.get('optimization_score')}")
            except Exception as e:
                logger.error(f"Traditional optimization failed: {str(e)}")
                raise
                
            try:
                quantum_result = self._simulate_quantum_optimization(locations, vehicles)
                logger.debug(f"Quantum optimization complete. Score: {quantum_result.get('optimization_score')}")
            except Exception as e:
                logger.error(f"Quantum optimization failed: {str(e)}")
                raise
            
            logger.info("Calculating analytics...")
            try:
                savings_analysis = self._calculate_savings_analysis(traditional_result, quantum_result)
                logger.debug(f"Savings analysis complete. Efficiency score: {savings_analysis.get('efficiency_score')}")
                
                certificates = self._generate_demo_certificates(quantum_result["routes"])
                logger.debug(f"Generated {len(certificates)} blockchain certificates")
                
                environmental_impact = self._calculate_environmental_impact(
                    savings_analysis["carbon_saved_kg"]
                )
                logger.debug(f"Environmental impact calculated. Trees equivalent: {environmental_impact.get('trees_planted_equivalent')}")
                
                walmart_projection = self._calculate_walmart_scale_projection(savings_analysis)
                logger.debug("Walmart scale projection complete")
            except Exception as e:
                logger.error(f"Analytics calculation failed: {str(e)}")
                raise
            
            result = {
                "scenario_id": scenario_id,
                "scenario_name": "Walmart NYC Delivery Optimization",
                "description": f"{num_locations} deliveries across NYC using {num_vehicles} vehicles",
                "locations": locations,
                "vehicles": vehicles,
                "traditional_optimization": traditional_result,
                "quantum_optimization": quantum_result,
                "savings_analysis": savings_analysis,
                "blockchain_certificates": certificates,
                "environmental_impact": environmental_impact,
                "walmart_scale_projection": walmart_projection,
                "generated_at": datetime.utcnow().isoformat()
            }
            
            logger.info("Successfully completed Walmart NYC scenario generation")
            return result
            
        except Exception as e:
            logger.critical(f"Fatal error in scenario generation: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to generate Walmart NYC scenario: {str(e)}")
    
    def _generate_nyc_locations(self, count: int) -> List[Dict[str, Any]]:
        """Generate realistic NYC delivery locations"""
        logger = logging.getLogger('NYCLocationsGenerator')
        logger.info(f"Starting NYC locations generation for {count} locations")
        
        locations = []
        
        try:
            for i in range(count):
                logger.debug(f"Generating location {i+1}/{count}")
                
                # Randomly select borough
                borough = random.choice(list(self.nyc_boroughs.keys()))
                borough_data = self.nyc_boroughs[borough]
                logger.debug(f"Selected borough: {borough}")
                
                try:
                    # Generate coordinates within borough
                    logger.debug(f"Generating coordinates for {borough} with center {borough_data['center']} and radius {borough_data['radius']}")
                    coords = generate_random_coordinates(
                        borough_data["center"][0],
                        borough_data["center"][1],
                        borough_data["radius"],
                        1
                    )[0]
                    logger.debug(f"Generated coordinates: {coords}")
                except Exception as e:
                    logger.error(f"Failed to generate coordinates for {borough}: {str(e)}")
                    raise
                
                try:
                    # Generate realistic address
                    street_number = random.randint(100, 9999)
                    street_name = random.choice(self.street_names)
                    company_name = random.choice(self.company_names)
                    logger.debug(f"Generated address components: {street_number} {street_name}, {company_name}")
                    
                    location = {
                        "id": f"nyc_loc_{i+1:03d}",
                        "name": f"{company_name} - {borough}",
                        "address": f"{street_number} {street_name}, {borough}, NY",
                        "latitude": coords[0],
                        "longitude": coords[1],
                        "demand_kg": random.randint(10, 200),
                        "priority": random.randint(1, 5),
                        "time_window_start": "08:00",
                        "time_window_end": "18:00",
                        "delivery_type": random.choice(["standard", "express", "same_day"]),
                        "borough": borough
                    }
                    logger.debug(f"Created location object: {location['id']}")
                    locations.append(location)
                except Exception as e:
                    logger.error(f"Failed to create location object for index {i}: {str(e)}")
                    raise
                
            logger.info(f"Successfully generated {len(locations)} NYC locations")
            return locations
            
        except Exception as e:
            logger.critical(f"Fatal error during NYC locations generation: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to generate NYC locations: {str(e)}")
    
    def _generate_walmart_fleet(self, count: int) -> List[Dict[str, Any]]:
        """Generate realistic Walmart vehicle fleet"""
        # Configure logging
        logger = logging.getLogger('WalmartFleetGenerator')
        logger.info(f"Starting Walmart fleet generation for {count} vehicles")

        vehicles = []
        
        try:
            # Walmart distribution center (realistic location)
            depot_location = {
                "latitude": 40.7589,
                "longitude": -73.9851,
                "address": "Walmart Distribution Center, Manhattan, NY"
            }
            logger.debug(f"Using depot location: {depot_location}")
            
            for i in range(count):
                logger.debug(f"Generating vehicle {i+1}/{count}")
                try:
                    # Select vehicle type based on realistic distribution
                    if i < count * 0.4:  # 40% diesel trucks
                        vehicle_type = "diesel_truck"
                    elif i < count * 0.6:  # 20% electric vans
                        vehicle_type = "electric_van"
                    elif i < count * 0.8:  # 20% hybrid vehicles
                        vehicle_type = "hybrid_delivery"
                    else:  # 20% gas trucks
                        vehicle_type = "gas_truck"
                    
                    logger.debug(f"Selected vehicle type: {vehicle_type}")
                    
                    # Validate vehicle type exists in specifications
                    if vehicle_type not in self.vehicle_types:
                        logger.error(f"Invalid vehicle type: {vehicle_type}")
                        raise ValueError(f"Vehicle type {vehicle_type} not found in specifications")
                    
                    vehicle_spec = self.vehicle_types[vehicle_type]
                    logger.debug(f"Retrieved vehicle specifications: {vehicle_spec}")
                    
                    # Generate vehicle data
                    vehicle_id = f"walmart_vehicle_{i+1:03d}"
                    license_plate = f"WMT{random.randint(1000, 9999)}"
                    
                    vehicle = {
                        "id": vehicle_id,
                        "type": vehicle_type,
                        "license_plate": license_plate,
                        "capacity_kg": vehicle_spec["capacity_kg"],
                        "cost_per_km": vehicle_spec["cost_per_km"],
                        "emission_factor": vehicle_spec["emission_factor"],
                        "efficiency_rating": vehicle_spec["efficiency_rating"],
                        "max_range_km": vehicle_spec["max_range_km"],
                        "driver_id": f"driver_{i+1:03d}",
                        "current_location": depot_location,
                        "availability_start": "06:00",
                        "availability_end": "20:00",
                        "fuel_level": round(random.uniform(0.7, 1.0), 2)
                    }
                    
                    logger.debug(f"Created vehicle object: {vehicle_id}")
                    logger.debug(f"Vehicle details: {vehicle}")
                    
                    vehicles.append(vehicle)
                    logger.info(f"Successfully added vehicle {vehicle_id} to fleet")
                    
                except Exception as e:
                    logger.error(f"Failed to generate vehicle {i+1}: {str(e)}", exc_info=True)
                    raise
            
            logger.info(f"Successfully generated {len(vehicles)} vehicles for Walmart fleet")
            logger.debug(f"Fleet composition: {[v['type'] for v in vehicles]}")
            return vehicles
            
        except Exception as e:
            logger.critical(f"Fatal error during Walmart fleet generation: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to generate Walmart fleet: {str(e)}")
    
    def _simulate_traditional_optimization(self, locations: List[Dict], 
                                         vehicles: List[Dict]) -> Dict[str, Any]:
        """Simulate traditional route optimization results"""
        logger = logging.getLogger('TraditionalOptimization')
        logger.info("Starting traditional optimization simulation")
        
        try:
            # Input validation
            if not locations or not vehicles:
                logger.error("Empty locations or vehicles list provided")
                raise ValueError("Locations and vehicles lists cannot be empty")
                
            logger.debug(f"Input validation passed: {len(locations)} locations, {len(vehicles)} vehicles")
            
            routes = []
            total_distance = 0
            total_time = 0 
            total_cost = 0
            total_carbon = 0
            
            # Calculate locations per vehicle
            locations_per_vehicle = len(locations) // len(vehicles)
            logger.debug(f"Locations per vehicle: {locations_per_vehicle}")
            
            # Process each vehicle
            for i, vehicle in enumerate(vehicles):
                logger.info(f"Processing vehicle {i+1}/{len(vehicles)}: {vehicle['id']}")
                
                try:
                    # Calculate location indices
                    start_idx = i * locations_per_vehicle
                    end_idx = start_idx + locations_per_vehicle
                    if i == len(vehicles) - 1:
                        end_idx = len(locations)
                        logger.debug(f"Last vehicle gets remaining locations: {end_idx - start_idx} locations")
                    
                    vehicle_locations = locations[start_idx:end_idx]
                    logger.debug(f"Assigned {len(vehicle_locations)} locations to vehicle {vehicle['id']}")
                    
                    # Calculate route metrics
                    logger.debug(f"Calculating metrics for route {i+1}")
                    try:
                        route_distance = self._calculate_route_distance(vehicle_locations)
                        logger.debug(f"Route distance calculated: {route_distance:.2f} km")
                        
                        route_time = route_distance * random.uniform(2.5, 3.5)
                        logger.debug(f"Route time calculated: {route_time:.1f} minutes")
                        
                        route_cost = route_distance * vehicle["cost_per_km"]
                        logger.debug(f"Route cost calculated: ${route_cost:.2f}")
                        
                        route_carbon = route_distance * vehicle["emission_factor"]
                        logger.debug(f"Route carbon emissions calculated: {route_carbon:.2f} kg")
                        
                    except Exception as e:
                        logger.error(f"Failed to calculate route metrics: {str(e)}", exc_info=True)
                        raise
                    
                    # Create route object
                    try:
                        route = {
                            "route_id": generate_route_id(),
                            "vehicle_id": vehicle["id"],
                            "vehicle_type": vehicle["type"],
                            "locations": vehicle_locations,
                            "distance_km": round(route_distance, 2),
                            "time_minutes": round(route_time, 1),
                            "cost_usd": round(route_cost, 2),
                            "carbon_kg": round(route_carbon, 2),
                            "optimization_score": random.randint(65, 75)
                        }
                        logger.debug(f"Route object created: {route['route_id']}")
                        
                        routes.append(route)
                        
                        # Update totals
                        total_distance += route_distance
                        total_time += route_time
                        total_cost += route_cost
                        total_carbon += route_carbon
                        logger.debug("Updated running totals")
                        
                    except Exception as e:
                        logger.error(f"Failed to create route object: {str(e)}", exc_info=True)
                        raise
                        
                except Exception as e:
                    logger.error(f"Failed processing vehicle {vehicle['id']}: {str(e)}", exc_info=True)
                    raise
            
            # Prepare final result
            logger.info("Preparing final optimization result")
            try:
                result = {
                    "method": "traditional",
                    "routes": routes,
                    "total_distance": round(total_distance, 2),
                    "total_time": round(total_time, 1),
                    "total_cost": round(total_cost, 2),
                    "total_carbon": round(total_carbon, 2),
                    "processing_time_seconds": random.uniform(2, 5),
                    "optimization_score": random.randint(65, 75)
                }
                logger.debug(f"Final result prepared: {len(routes)} routes")
                logger.info("Traditional optimization simulation completed successfully")
                return result
                
            except Exception as e:
                logger.error(f"Failed to prepare final result: {str(e)}", exc_info=True)
                raise
                
        except Exception as e:
            logger.critical(f"Fatal error in traditional optimization: {str(e)}", exc_info=True)
            raise RuntimeError(f"Traditional optimization failed: {str(e)}")
    
    def _simulate_quantum_optimization(self, locations: List[Dict], 
                                     vehicles: List[Dict]) -> Dict[str, Any]:
        """Simulate quantum-inspired optimization results (improved)"""
        # Configure logging
        logger = logging.getLogger('QuantumOptimization')
        logger.info("Starting quantum-inspired optimization simulation")
        
        try:
            # Input validation
            if not locations or not vehicles:
                logger.error("Empty locations or vehicles list provided")
                raise ValueError("Locations and vehicles lists cannot be empty")
            
            logger.debug(f"Input validation passed: {len(locations)} locations, {len(vehicles)} vehicles")
            
            # Get traditional results as baseline
            logger.info("Calculating traditional optimization baseline")
            try:
                traditional = self._simulate_traditional_optimization(locations, vehicles)
                logger.debug(f"Traditional baseline calculated with score: {traditional.get('optimization_score')}")
            except Exception as e:
                logger.error(f"Failed to calculate traditional baseline: {str(e)}")
                raise
            
            # Generate improvement factors
            logger.info("Generating quantum improvement factors")
            try:
                improvement_factors = {
                    "distance": random.uniform(0.70, 0.80),    # 20-30% improvement
                    "time": random.uniform(0.68, 0.78),        # 22-32% improvement
                    "cost": random.uniform(0.70, 0.80),        # 20-30% improvement
                    "carbon": random.uniform(0.60, 0.75)       # 25-40% improvement
                }
                logger.debug(f"Improvement factors generated: {improvement_factors}")
            except Exception as e:
                logger.error(f"Failed to generate improvement factors: {str(e)}")
                raise
            
            # Process routes with quantum improvements
            routes = []
            logger.info("Starting route improvement processing")
            
            for idx, route in enumerate(traditional["routes"]):
                logger.debug(f"Processing route {idx+1}/{len(traditional['routes'])}")
                try:
                    improved_route = {
                        "route_id": generate_route_id(),
                        "vehicle_id": route["vehicle_id"],
                        "vehicle_type": route["vehicle_type"],
                        "locations": route["locations"],
                        "distance_km": round(route["distance_km"] * improvement_factors["distance"], 2),
                        "time_minutes": round(route["time_minutes"] * improvement_factors["time"], 1),
                        "cost_usd": round(route["cost_usd"] * improvement_factors["cost"], 2),
                        "carbon_kg": round(route["carbon_kg"] * improvement_factors["carbon"], 2),
                        "optimization_score": random.randint(88, 97),
                        "quantum_improvement": True
                    }
                    logger.debug(f"Route {improved_route['route_id']} improved - "
                               f"Distance reduction: {route['distance_km'] - improved_route['distance_km']:.2f}km, "
                               f"Cost reduction: ${route['cost_usd'] - improved_route['cost_usd']:.2f}")
                    
                    routes.append(improved_route)
                except Exception as e:
                    logger.error(f"Failed to improve route {idx+1}: {str(e)}")
                    raise
            
            # Calculate final totals
            logger.info("Calculating final optimization totals")
            try:
                total_distance = sum(route["distance_km"] for route in routes)
                total_time = sum(route["time_minutes"] for route in routes)
                total_cost = sum(route["cost_usd"] for route in routes)
                total_carbon = sum(route["carbon_kg"] for route in routes)
                
                logger.debug(f"Final totals calculated - "
                           f"Distance: {total_distance:.2f}km, "
                           f"Time: {total_time:.1f}min, "
                           f"Cost: ${total_cost:.2f}, "
                           f"Carbon: {total_carbon:.2f}kg")
            except Exception as e:
                logger.error(f"Failed to calculate final totals: {str(e)}")
                raise
            
            # Prepare final result
            logger.info("Preparing final quantum optimization result")
            try:
                result = {
                    "method": "quantum_inspired",
                    "routes": routes,
                    "total_distance": round(total_distance, 2),
                    "total_time": round(total_time, 1),
                    "total_cost": round(total_cost, 2),
                    "total_carbon": round(total_carbon, 2),
                    "processing_time_seconds": random.uniform(8, 15),
                    "optimization_score": random.randint(88, 97),
                    "quantum_iterations": random.randint(50, 120),
                    "convergence_score": random.uniform(0.90, 0.98)
                }
                
                logger.debug(f"Final result prepared with {len(routes)} optimized routes")
                logger.info("Quantum optimization simulation completed successfully")
                
                # Log improvement percentages
                improvements = {
                    "distance": ((traditional["total_distance"] - result["total_distance"]) / 
                               traditional["total_distance"] * 100),
                    "cost": ((traditional["total_cost"] - result["total_cost"]) / 
                            traditional["total_cost"] * 100),
                    "carbon": ((traditional["total_carbon"] - result["total_carbon"]) / 
                             traditional["total_carbon"] * 100)
                }
                logger.info(f"Achieved improvements - "
                          f"Distance: {improvements['distance']:.1f}%, "
                          f"Cost: {improvements['cost']:.1f}%, "
                          f"Carbon: {improvements['carbon']:.1f}%")
                
                return result
                
            except Exception as e:
                logger.error(f"Failed to prepare final result: {str(e)}")
                raise
                
        except Exception as e:
            logger.critical(f"Fatal error in quantum optimization: {str(e)}", exc_info=True)
            raise RuntimeError(f"Quantum optimization failed: {str(e)}")
    
    def _calculate_route_distance(self, locations: List[Dict]) -> float:
        """Calculate total distance for a route"""
        logger = logging.getLogger('RouteDistanceCalculator')
        logger.info("Starting route distance calculation")
        
        try:
            # Input validation
            if not locations:
                logger.warning("Empty locations list provided")
                return 0
                
            if len(locations) < 2:
                logger.debug(f"Only {len(locations)} location provided - returning 0 distance")
                return 0
                
            logger.debug(f"Processing {len(locations)} locations for distance calculation")
            
            total_distance = 0
            
            for i in range(len(locations) - 1):
                try:
                    loc1 = locations[i]
                    loc2 = locations[i + 1]
                    
                    distance = calculate_distance(
                        loc1["latitude"], loc1["longitude"],
                        loc2["latitude"], loc2["longitude"]
                    )
                    
                    logger.debug(f"Calculated segment distance: {distance:.2f}km")
                    
                    if distance < 0 or distance > 1000:  # Sanity check
                        logger.warning(f"Unusual distance value ({distance:.2f}km) detected between points {i} and {i+1}")
                    
                    total_distance += distance
                    logger.debug(f"Running total distance: {total_distance:.2f}km")
                    
                except KeyError as e:
                    logger.error(f"Missing required coordinate data: {str(e)}", exc_info=True)
                    raise
                except ValueError as e:
                    logger.error(f"Invalid coordinate values: {str(e)}", exc_info=True)
                    raise
                except Exception as e:
                    logger.error(f"Unexpected error calculating segment distance: {str(e)}", exc_info=True)
                    raise
            
            logger.info(f"Route distance calculation completed. Total distance: {total_distance:.2f}km")
            return total_distance
            
        except Exception as e:
            logger.critical(f"Fatal error in route distance calculation: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to calculate route distance: {str(e)}")
    
    def _calculate_savings_analysis(self, traditional: Dict, quantum: Dict) -> Dict[str, Any]:
        """Calculate savings between traditional and quantum optimization"""
        # Configure logging
        logger = logging.getLogger('SavingsAnalysis')
        logger.info("Starting savings analysis calculation")

        try:
            # Input validation
            logger.debug(f"Validating input traditional data: {traditional.keys()}")
            logger.debug(f"Validating input quantum data: {quantum.keys()}")

            required_keys = ["total_cost", "total_carbon", "total_time", "total_distance"]
            for key in required_keys:
                if key not in traditional or key not in quantum:
                    logger.error(f"Missing required key: {key}")
                    raise KeyError(f"Missing required key in input data: {key}")

            logger.info("Input validation passed, calculating savings metrics")

            try:
                # Calculate cost savings
                cost_saved = traditional["total_cost"] - quantum["total_cost"]
                logger.debug(f"Cost saved calculation: {traditional['total_cost']} - {quantum['total_cost']} = {cost_saved}")

                # Calculate carbon savings
                carbon_saved = traditional["total_carbon"] - quantum["total_carbon"]
                logger.debug(f"Carbon saved calculation: {traditional['total_carbon']} - {quantum['total_carbon']} = {carbon_saved}")

                # Calculate time savings
                time_saved = traditional["total_time"] - quantum["total_time"]
                logger.debug(f"Time saved calculation: {traditional['total_time']} - {quantum['total_time']} = {time_saved}")

                # Calculate distance savings
                distance_saved = traditional["total_distance"] - quantum["total_distance"]
                logger.debug(f"Distance saved calculation: {traditional['total_distance']} - {quantum['total_distance']} = {distance_saved}")

            except Exception as e:
                logger.error(f"Error during savings calculations: {str(e)}", exc_info=True)
                raise

            logger.info("Basic savings calculated, computing improvement percentages")

            try:
                # Calculate improvement percentages
                cost_improvement = (cost_saved / traditional["total_cost"]) * 100
                logger.debug(f"Cost improvement %: ({cost_saved} / {traditional['total_cost']}) * 100 = {cost_improvement}")

                carbon_improvement = (carbon_saved / traditional["total_carbon"]) * 100
                logger.debug(f"Carbon improvement %: ({carbon_saved} / {traditional['total_carbon']}) * 100 = {carbon_improvement}")

                time_improvement = (time_saved / traditional["total_time"]) * 100
                logger.debug(f"Time improvement %: ({time_saved} / {traditional['total_time']}) * 100 = {time_improvement}")

                distance_improvement = (distance_saved / traditional["total_distance"]) * 100
                logger.debug(f"Distance improvement %: ({distance_saved} / {traditional['total_distance']}) * 100 = {distance_improvement}")

            except ZeroDivisionError as e:
                logger.error("Division by zero encountered in percentage calculations", exc_info=True)
                raise
            except Exception as e:
                logger.error(f"Error calculating improvement percentages: {str(e)}", exc_info=True)
                raise

            logger.info("Calculating overall efficiency score")

            try:
                # Calculate efficiency score
                efficiency_components = [
                    cost_saved / traditional["total_cost"],
                    carbon_saved / traditional["total_carbon"],
                    time_saved / traditional["total_time"]
                ]
                efficiency_score = sum(efficiency_components) / 3 * 100
                logger.debug(f"Efficiency score calculation: {efficiency_components} -> {efficiency_score}")

                # Prepare final result
                result = {
                    "cost_saved_usd": round(cost_saved, 2),
                    "cost_improvement_percent": round(cost_improvement, 1),
                    "carbon_saved_kg": round(carbon_saved, 2),
                    "carbon_improvement_percent": round(carbon_improvement, 1),
                    "time_saved_minutes": round(time_saved, 1),
                    "time_improvement_percent": round(time_improvement, 1),
                    "distance_saved_km": round(distance_saved, 2),
                    "distance_improvement_percent": round(distance_improvement, 1),
                    "efficiency_score": round(efficiency_score, 1)
                }

                logger.debug(f"Final result prepared: {result}")
                logger.info("Savings analysis calculation completed successfully")

                # Validate results are within expected ranges
                for key, value in result.items():
                    if isinstance(value, (int, float)):
                        if value < 0:
                            logger.warning(f"Negative value detected in results: {key}={value}")
                        if value > 100 and 'percent' in key:
                            logger.warning(f"Unusually high percentage detected: {key}={value}")

                return result

            except Exception as e:
                logger.error(f"Error in final result preparation: {str(e)}", exc_info=True)
                raise

        except Exception as e:
            logger.critical(f"Fatal error in savings analysis: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to calculate savings analysis: {str(e)}")
    
    def _generate_demo_certificates(self, routes: List[Dict]) -> List[Dict[str, Any]]:
        """Generate blockchain certificates for demo routes"""
        logger = logging.getLogger('DemoCertificatesGenerator')
        logger.info("Starting demo certificates generation")
        
        certificates = []
        
        try:
            # Input validation
            if not routes:
                logger.error("Empty routes list provided")
                raise ValueError("Routes list cannot be empty")
                
            logger.debug(f"Processing {len(routes)} routes for certificate generation")
            
            for idx, route in enumerate(routes):
                logger.debug(f"Processing route {idx+1}/{len(routes)}: {route.get('route_id')}")
                
                try:
                    # Generate certificate values
                    carbon_saved = round(random.uniform(15, 45), 2)
                    cost_saved = round(random.uniform(25, 85), 2)
                    verification_hash = generate_hash(f"{route['route_id']}{time.time()}")
                    tx_hash = f"0x{generate_hash(f'tx_{route['route_id']}')[:64]}"
                    
                    logger.debug(f"Generated values for route {route['route_id']}: "
                               f"Carbon saved={carbon_saved}kg, Cost saved=${cost_saved}, "
                               f"Hash={verification_hash[:8]}...")
                    
                    certificate = {
                        "certificate_id": f"cert_{generate_hash(route['route_id'])[:12]}",
                        "route_id": route["route_id"],
                        "vehicle_id": route["vehicle_id"],
                        "carbon_saved_kg": carbon_saved,
                        "cost_saved_usd": cost_saved,
                        "optimization_score": route["optimization_score"],
                        "verification_hash": verification_hash,
                        "transaction_hash": tx_hash,
                        "block_number": random.randint(1000000, 2000000),
                        "verified": True,
                        "created_at": datetime.utcnow().isoformat(),
                        "blockchain_network": "ganache_local"
                    }
                    
                    logger.debug(f"Created certificate {certificate['certificate_id']} "
                               f"for route {route['route_id']}")
                    
                    certificates.append(certificate)
                    logger.info(f"Successfully added certificate {idx+1}/{len(routes)}")
                    
                except KeyError as e:
                    logger.error(f"Missing required route data for index {idx}: {str(e)}", 
                               exc_info=True)
                    raise
                except Exception as e:
                    logger.error(f"Failed to generate certificate for route {idx}: {str(e)}", 
                               exc_info=True)
                    raise
            
            logger.info(f"Successfully generated {len(certificates)} certificates")
            return certificates
            
        except Exception as e:
            logger.critical(f"Fatal error in certificate generation: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to generate demo certificates: {str(e)}")
    
    def _calculate_environmental_impact(self, carbon_saved_kg: float) -> Dict[str, Any]:
        """Calculate environmental impact equivalents"""
        logger = logging.getLogger('EnvironmentalImpactCalculator')
        logger.info("Starting environmental impact calculation")
        
        try:
            # Input validation
            if not isinstance(carbon_saved_kg, (int, float)):
                logger.error(f"Invalid carbon_saved_kg type: {type(carbon_saved_kg)}")
                raise TypeError("carbon_saved_kg must be numeric")
                
            if carbon_saved_kg < 0:
                logger.error(f"Negative carbon_saved_kg value: {carbon_saved_kg}")
                raise ValueError("carbon_saved_kg cannot be negative")
            
            logger.debug(f"Calculating impact equivalents for {carbon_saved_kg}kg CO2")
            
            try:
                # Calculate equivalents
                trees = round(carbon_saved_kg / 21.77, 1)
                cars = round(carbon_saved_kg / 12.6, 1)
                homes = round(carbon_saved_kg / 0.83, 1)
                miles = round(carbon_saved_kg / 0.404, 1)
                gallons = round(carbon_saved_kg / 8.89, 1)
                
                logger.debug(f"Calculated equivalents: "
                           f"Trees={trees}, Cars={cars}, "
                           f"Homes={homes}, Miles={miles}, "
                           f"Gallons={gallons}")
                
                result = {
                    "trees_planted_equivalent": trees,
                    "cars_off_road_days": cars,
                    "homes_powered_hours": homes,
                    "miles_not_driven": miles,
                    "gallons_fuel_saved": gallons
                }
                
                # Validate results
                for key, value in result.items():
                    if value < 0:
                        logger.warning(f"Negative value in results: {key}={value}")
                    if value > 1000000:
                        logger.warning(f"Unusually high value: {key}={value}")
                
                logger.info("Environmental impact calculation completed successfully")
                return result
                
            except ZeroDivisionError as e:
                logger.error("Division by zero in impact calculations", exc_info=True)
                raise
            except Exception as e:
                logger.error(f"Error during impact calculations: {str(e)}", exc_info=True)
                raise
                
        except Exception as e:
            logger.critical(f"Fatal error in environmental impact calculation: {str(e)}", 
                          exc_info=True)
            raise RuntimeError(f"Failed to calculate environmental impact: {str(e)}")
    
    def _calculate_walmart_scale_projection(self, savings: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate Walmart-scale impact projections"""
        # Configure logging
        logger = logging.getLogger('WalmartScaleProjection')
        logger.info("Starting Walmart scale projection calculations")

        try:
            # Input validation
            logger.debug(f"Validating input savings data: {savings}")
            required_keys = ["cost_saved_usd", "carbon_saved_kg"]
            for key in required_keys:
                if key not in savings:
                    logger.error(f"Missing required key in savings data: {key}")
                    raise KeyError(f"Missing required savings data: {key}")

            # Define scale multipliers
            logger.info("Setting up scale multipliers")
            try:
                daily_multiplier = 2_625_000  # Daily deliveries across all stores
                annual_multiplier = daily_multiplier * 365
                logger.debug(f"Multipliers set - Daily: {daily_multiplier:,}, Annual: {annual_multiplier:,}")
            except Exception as e:
                logger.error(f"Error setting up multipliers: {str(e)}")
                raise

            # Calculate daily projections
            logger.info("Calculating daily projections")
            try:
                daily_cost_savings = savings["cost_saved_usd"] * daily_multiplier
                daily_carbon_reduction = savings["carbon_saved_kg"] * daily_multiplier
                logger.debug(f"Daily projections calculated - Cost: ${daily_cost_savings:,.2f}, Carbon: {daily_carbon_reduction:,.2f}kg")
            except Exception as e:
                logger.error(f"Error calculating daily projections: {str(e)}")
                raise

            # Calculate annual projections
            logger.info("Calculating annual projections")
            try:
                annual_cost_savings = savings["cost_saved_usd"] * annual_multiplier
                annual_carbon_reduction_tons = (savings["carbon_saved_kg"] * annual_multiplier) / 1000
                logger.debug(f"Annual projections calculated - Cost: ${annual_cost_savings:,.2f}, Carbon: {annual_carbon_reduction_tons:,.2f}tons")
            except Exception as e:
                logger.error(f"Error calculating annual projections: {str(e)}")
                raise

            # Calculate ROI projections
            logger.info("Calculating ROI projections")
            try:
                implementation_cost = 350_000_000
                annual_benefits = annual_cost_savings
                payback_months = round((implementation_cost / annual_benefits) * 12)
                npv = 4_200_000_000

                logger.debug(f"ROI metrics calculated:"
                            f"\nImplementation Cost: ${implementation_cost:,.2f}"
                            f"\nAnnual Benefits: ${annual_benefits:,.2f}"
                            f"\nPayback Period: {payback_months} months"
                            f"\nNPV: ${npv:,.2f}")

                # Validate ROI calculations
                if payback_months <= 0:
                    logger.warning(f"Invalid payback period calculated: {payback_months} months")
                if annual_benefits <= 0:
                    logger.warning(f"Invalid annual benefits calculated: ${annual_benefits:,.2f}")
            except Exception as e:
                logger.error(f"Error calculating ROI projections: {str(e)}")
                raise

            # Prepare final result
            logger.info("Preparing final projection result")
            try:
                result = {
                    "daily_cost_savings_usd": round(daily_cost_savings, 2),
                    "annual_cost_savings_usd": round(annual_cost_savings, 2),
                    "daily_carbon_reduction_kg": round(daily_carbon_reduction, 2),
                    "annual_carbon_reduction_tons": round(annual_carbon_reduction_tons, 2),
                    "stores_impacted": 10_500,
                    "confidence_level": 0.89,
                    "roi_projection": {
                        "implementation_cost_usd": implementation_cost,
                        "annual_benefits_usd": round(annual_benefits, 2),
                        "payback_period_months": payback_months,
                        "net_present_value_usd": npv
                    }
                }

                # Validate final results
                logger.debug("Validating final results")
                for key, value in result.items():
                    if isinstance(value, (int, float)) and not isinstance(value, bool):
                        if value < 0:
                            logger.warning(f"Negative value in final results: {key}={value}")
                        if value > 1e12:  # Greater than 1 trillion
                            logger.warning(f"Unusually high value in results: {key}={value}")

                logger.info("Walmart scale projection completed successfully")
                return result

            except Exception as e:
                logger.error(f"Error preparing final result: {str(e)}")
                raise

        except Exception as e:
            logger.critical(f"Fatal error in Walmart scale projection: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to calculate Walmart scale projection: {str(e)}")
    
    def generate_performance_showcase_data(self) -> Dict[str, Any]:
        """Generate impressive performance numbers for demo"""
        return {
            "quantum_vs_traditional": {
                "cost_improvement_percent": 25.3,
                "carbon_reduction_percent": 35.7,
                "time_savings_percent": 28.1,
                "efficiency_score_improvement": 42.5
            },
            "walmart_scale_impact": {
                "annual_cost_savings_usd": 1_580_000_000,
                "annual_carbon_reduction_tons": 2_340_000,
                "stores_impacted": 10_500,
                "daily_deliveries_optimized": 2_625_000
            },
            "technical_performance": {
                "optimization_speed_ms": 1_250,
                "accuracy_percent": 99.2,
                "scalability_factor": 1000,
                "blockchain_verification_time_ms": 850
            },
            "competitive_advantages": {
                "faster_than_traditional_percent": 340,
                "more_accurate_than_competitors_percent": 15,
                "carbon_reduction_vs_industry_percent": 280,
                "cost_efficiency_vs_market_percent": 45
            }
        }
    
    def generate_custom_scenario(self, area: str, num_locations: int, 
                               num_vehicles: int, vehicle_types: List[str]) -> Dict[str, Any]:
        """Generate custom demo scenario"""
        # Configure logging
        logger = logging.getLogger('CustomScenarioGenerator')
        logger.info(f"Starting custom scenario generation for {area} with {num_locations} locations and {num_vehicles} vehicles")
        
        try:
            # Input validation
            logger.debug("Validating input parameters")
            if not area or not isinstance(area, str):
                logger.error(f"Invalid area parameter: {area}")
                raise ValueError("Area must be a non-empty string")
                
            if num_locations <= 0 or num_vehicles <= 0:
                logger.error(f"Invalid counts: locations={num_locations}, vehicles={num_vehicles}")
                raise ValueError("Location and vehicle counts must be positive")
                
            if not vehicle_types:
                logger.error("Empty vehicle_types list provided")
                raise ValueError("Vehicle types list cannot be empty")
            
            logger.debug(f"Input validation passed. Vehicle types: {vehicle_types}")
            
            # Generate scenario ID
            scenario_id = generate_demo_id()
            logger.debug(f"Generated scenario ID: {scenario_id}")
            
            # Area centers setup
            logger.info("Setting up area coordinates")
            area_centers = {
                "new_york": (40.7128, -74.0060),
                "chicago": (41.8781, -87.6298),
                "los_angeles": (34.0522, -118.2437),
                "houston": (29.7604, -95.3698),
                "phoenix": (33.4484, -112.0740)
            }
            
            center = area_centers.get(area.lower())
            if not center:
                logger.warning(f"Unknown area: {area}, defaulting to New York coordinates")
                center = area_centers["new_york"]
            
            logger.debug(f"Using center coordinates: {center}")
            
            # Generate locations
            logger.info(f"Generating {num_locations} locations")
            locations = []
            try:
                coordinates = generate_random_coordinates(center[0], center[1], 30, num_locations)
                logger.debug(f"Generated {len(coordinates)} coordinate pairs")
                
                for i, coord in enumerate(coordinates):
                    try:
                        location = {
                            "id": f"{area}_loc_{i+1:03d}",
                            "name": f"{random.choice(self.company_names)} - {area.title()}",
                            "address": f"{random.randint(100, 9999)} {random.choice(self.street_names)}, {area.title()}",
                            "latitude": coord[0],
                            "longitude": coord[1],
                            "demand_kg": random.randint(10, 150),
                            "priority": random.randint(1, 5),
                            "time_window_start": "08:00",
                            "time_window_end": "18:00",
                            "delivery_type": "standard"
                        }
                        locations.append(location)
                        logger.debug(f"Created location {i+1}/{num_locations}: {location['id']}")
                    except Exception as e:
                        logger.error(f"Failed to generate location {i+1}: {str(e)}")
                        raise
                        
            except Exception as e:
                logger.error(f"Location generation failed: {str(e)}")
                raise
            
            # Generate vehicles
            logger.info(f"Generating {num_vehicles} vehicles")
            vehicles = []
            try:
                for i in range(num_vehicles):
                    try:
                        vehicle_type = random.choice(vehicle_types)
                        vehicle_spec = self.vehicle_types.get(vehicle_type)
                        
                        if not vehicle_spec:
                            logger.warning(f"Unknown vehicle type: {vehicle_type}, using diesel_truck")
                            vehicle_spec = self.vehicle_types["diesel_truck"]
                        
                        vehicle = {
                            "id": f"{area}_vehicle_{i+1:03d}",
                            "type": vehicle_type,
                            "capacity_kg": vehicle_spec["capacity_kg"],
                            "cost_per_km": vehicle_spec["cost_per_km"],
                            "emission_factor": vehicle_spec["emission_factor"],
                            "efficiency_rating": vehicle_spec["efficiency_rating"]
                        }
                        vehicles.append(vehicle)
                        logger.debug(f"Created vehicle {i+1}/{num_vehicles}: {vehicle['id']} ({vehicle_type})")
                        
                    except Exception as e:
                        logger.error(f"Failed to generate vehicle {i+1}: {str(e)}")
                        raise
                        
            except Exception as e:
                logger.error(f"Vehicle generation failed: {str(e)}")
                raise
            
            # Generate optimization results
            logger.info("Starting optimization simulations")
            try:
                logger.debug("Running traditional optimization")
                traditional_result = self._simulate_traditional_optimization(locations, vehicles)
                logger.debug(f"Traditional optimization complete. Score: {traditional_result.get('optimization_score')}")
                
                logger.debug("Running quantum optimization")
                quantum_result = self._simulate_quantum_optimization(locations, vehicles)
                logger.debug(f"Quantum optimization complete. Score: {quantum_result.get('optimization_score')}")
                
            except Exception as e:
                logger.error(f"Optimization simulation failed: {str(e)}")
                raise
            
            # Calculate savings
            logger.info("Calculating final savings analysis")
            try:
                savings_analysis = self._calculate_savings_analysis(traditional_result, quantum_result)
                logger.debug(f"Savings analysis complete. Cost saved: ${savings_analysis.get('cost_saved_usd', 0):.2f}")
            except Exception as e:
                logger.error(f"Savings analysis failed: {str(e)}")
                raise
            
            # Prepare final result
            logger.info("Preparing final scenario result")
            try:
                result = {
                    "scenario_id": scenario_id,
                    "scenario_name": f"Custom {area.title()} Delivery Scenario",
                    "description": f"Custom scenario with {num_locations} locations and {num_vehicles} vehicles",
                    "locations": locations,
                    "vehicles": vehicles,
                    "traditional_optimization": traditional_result,
                    "quantum_optimization": quantum_result,
                    "savings_analysis": savings_analysis,
                    "generated_at": datetime.utcnow().isoformat()
                }
                
                logger.debug("Validating final result structure")
                for key in ["locations", "vehicles", "traditional_optimization", "quantum_optimization", "savings_analysis"]:
                    if key not in result:
                        logger.warning(f"Missing key in final result: {key}")
                
                logger.info("Custom scenario generation completed successfully")
                return result
                
            except Exception as e:
                logger.error(f"Failed to prepare final result: {str(e)}")
                raise
                
        except Exception as e:
            logger.critical(f"Fatal error in custom scenario generation: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to generate custom scenario: {str(e)}")

# Global demo data generator instance
demo_generator = DemoDataGenerator()
