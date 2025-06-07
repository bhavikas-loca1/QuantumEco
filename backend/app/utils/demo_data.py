import random
import time
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
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
        scenario_id = generate_demo_id()
        
        # Generate delivery locations across NYC boroughs
        locations = self._generate_nyc_locations(num_locations)
        
        # Generate Walmart vehicle fleet
        vehicles = self._generate_walmart_fleet(num_vehicles)
        
        # Generate traditional optimization results
        traditional_result = self._simulate_traditional_optimization(locations, vehicles)
        
        # Generate quantum-inspired optimization results
        quantum_result = self._simulate_quantum_optimization(locations, vehicles)
        
        # Calculate savings analysis
        savings_analysis = self._calculate_savings_analysis(traditional_result, quantum_result)
        
        # Generate blockchain certificates
        certificates = self._generate_demo_certificates(quantum_result["routes"])
        
        # Calculate environmental impact
        environmental_impact = self._calculate_environmental_impact(
            savings_analysis["carbon_saved_kg"]
        )
        
        # Calculate Walmart scale projection
        walmart_projection = self._calculate_walmart_scale_projection(savings_analysis)
        
        return {
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
    
    def _generate_nyc_locations(self, count: int) -> List[Dict[str, Any]]:
        """Generate realistic NYC delivery locations"""
        locations = []
        
        for i in range(count):
            # Randomly select borough
            borough = random.choice(list(self.nyc_boroughs.keys()))
            borough_data = self.nyc_boroughs[borough]
            
            # Generate coordinates within borough
            coords = generate_random_coordinates(
                borough_data["center"][0],
                borough_data["center"][1],
                borough_data["radius"],
                1
            )[0]
            
            # Generate realistic address
            street_number = random.randint(100, 9999)
            street_name = random.choice(self.street_names)
            company_name = random.choice(self.company_names)
            
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
            locations.append(location)
        
        return locations
    
    def _generate_walmart_fleet(self, count: int) -> List[Dict[str, Any]]:
        """Generate realistic Walmart vehicle fleet"""
        vehicles = []
        
        # Walmart distribution center (realistic location)
        depot_location = {
            "latitude": 40.7589,
            "longitude": -73.9851,
            "address": "Walmart Distribution Center, Manhattan, NY"
        }
        
        for i in range(count):
            # Select vehicle type based on realistic distribution
            if i < count * 0.4:  # 40% diesel trucks for heavy loads
                vehicle_type = "diesel_truck"
            elif i < count * 0.6:  # 20% electric vans for eco-friendly delivery
                vehicle_type = "electric_van"
            elif i < count * 0.8:  # 20% hybrid vehicles
                vehicle_type = "hybrid_delivery"
            else:  # 20% gas trucks
                vehicle_type = "gas_truck"
            
            vehicle_spec = self.vehicle_types[vehicle_type]
            
            vehicle = {
                "id": f"walmart_vehicle_{i+1:03d}",
                "type": vehicle_type,
                "license_plate": f"WMT{random.randint(1000, 9999)}",
                "capacity_kg": vehicle_spec["capacity_kg"],
                "cost_per_km": vehicle_spec["cost_per_km"],
                "emission_factor": vehicle_spec["emission_factor"],
                "efficiency_rating": vehicle_spec["efficiency_rating"],
                "max_range_km": vehicle_spec["max_range_km"],
                "driver_id": f"driver_{i+1:03d}",
                "current_location": depot_location,
                "availability_start": "06:00",
                "availability_end": "20:00",
                "fuel_level": random.uniform(0.7, 1.0)
            }
            vehicles.append(vehicle)
        
        return vehicles
    
    def _simulate_traditional_optimization(self, locations: List[Dict], 
                                         vehicles: List[Dict]) -> Dict[str, Any]:
        """Simulate traditional route optimization results"""
        routes = []
        total_distance = 0
        total_time = 0
        total_cost = 0
        total_carbon = 0
        
        # Simple round-robin assignment (traditional approach)
        locations_per_vehicle = len(locations) // len(vehicles)
        
        for i, vehicle in enumerate(vehicles):
            start_idx = i * locations_per_vehicle
            end_idx = start_idx + locations_per_vehicle
            if i == len(vehicles) - 1:  # Last vehicle gets remaining locations
                end_idx = len(locations)
            
            vehicle_locations = locations[start_idx:end_idx]
            
            # Calculate route metrics (simplified but realistic)
            route_distance = self._calculate_route_distance(vehicle_locations)
            route_time = route_distance * random.uniform(2.5, 3.5)  # minutes per km
            route_cost = route_distance * vehicle["cost_per_km"]
            route_carbon = route_distance * vehicle["emission_factor"]
            
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
            routes.append(route)
            
            total_distance += route_distance
            total_time += route_time
            total_cost += route_cost
            total_carbon += route_carbon
        
        return {
            "method": "traditional",
            "routes": routes,
            "total_distance_km": round(total_distance, 2),
            "total_time_minutes": round(total_time, 1),
            "total_cost_usd": round(total_cost, 2),
            "total_carbon_kg": round(total_carbon, 2),
            "processing_time_seconds": random.uniform(2, 5),
            "optimization_score": random.randint(65, 75)
        }
    
    def _simulate_quantum_optimization(self, locations: List[Dict], 
                                     vehicles: List[Dict]) -> Dict[str, Any]:
        """Simulate quantum-inspired optimization results (improved)"""
        # Start with traditional results
        traditional = self._simulate_traditional_optimization(locations, vehicles)
        
        # Apply quantum-inspired improvements
        improvement_factors = {
            "distance": random.uniform(0.70, 0.80),    # 20-30% improvement
            "time": random.uniform(0.68, 0.78),        # 22-32% improvement
            "cost": random.uniform(0.70, 0.80),        # 20-30% improvement
            "carbon": random.uniform(0.60, 0.75)       # 25-40% improvement
        }
        
        routes = []
        for route in traditional["routes"]:
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
            routes.append(improved_route)
        
        # Calculate improved totals
        total_distance = sum(route["distance_km"] for route in routes)
        total_time = sum(route["time_minutes"] for route in routes)
        total_cost = sum(route["cost_usd"] for route in routes)
        total_carbon = sum(route["carbon_kg"] for route in routes)
        
        return {
            "method": "quantum_inspired",
            "routes": routes,
            "total_distance_km": round(total_distance, 2),
            "total_time_minutes": round(total_time, 1),
            "total_cost_usd": round(total_cost, 2),
            "total_carbon_kg": round(total_carbon, 2),
            "processing_time_seconds": random.uniform(8, 15),
            "optimization_score": random.randint(88, 97),
            "quantum_iterations": random.randint(50, 120),
            "convergence_score": random.uniform(0.90, 0.98)
        }
    
    def _calculate_route_distance(self, locations: List[Dict]) -> float:
        """Calculate total distance for a route"""
        if len(locations) < 2:
            return 0
        
        total_distance = 0
        for i in range(len(locations) - 1):
            loc1 = locations[i]
            loc2 = locations[i + 1]
            distance = calculate_distance(
                loc1["latitude"], loc1["longitude"],
                loc2["latitude"], loc2["longitude"]
            )
            total_distance += distance
        
        return total_distance
    
    def _calculate_savings_analysis(self, traditional: Dict, quantum: Dict) -> Dict[str, Any]:
        """Calculate savings between traditional and quantum optimization"""
        cost_saved = traditional["total_cost_usd"] - quantum["total_cost_usd"]
        carbon_saved = traditional["total_carbon_kg"] - quantum["total_carbon_kg"]
        time_saved = traditional["total_time_minutes"] - quantum["total_time_minutes"]
        distance_saved = traditional["total_distance_km"] - quantum["total_distance_km"]
        
        return {
            "cost_saved_usd": round(cost_saved, 2),
            "cost_improvement_percent": round((cost_saved / traditional["total_cost_usd"]) * 100, 1),
            "carbon_saved_kg": round(carbon_saved, 2),
            "carbon_improvement_percent": round((carbon_saved / traditional["total_carbon_kg"]) * 100, 1),
            "time_saved_minutes": round(time_saved, 1),
            "time_improvement_percent": round((time_saved / traditional["total_time_minutes"]) * 100, 1),
            "distance_saved_km": round(distance_saved, 2),
            "distance_improvement_percent": round((distance_saved / traditional["total_distance_km"]) * 100, 1),
            "efficiency_score": round(((cost_saved / traditional["total_cost_usd"]) + 
                                     (carbon_saved / traditional["total_carbon_kg"]) + 
                                     (time_saved / traditional["total_time_minutes"])) / 3 * 100, 1)
        }
    
    def _generate_demo_certificates(self, routes: List[Dict]) -> List[Dict[str, Any]]:
        """Generate blockchain certificates for demo routes"""
        certificates = []
        
        for route in routes:
            certificate = {
                "certificate_id": f"cert_{generate_hash(route['route_id'])[:12]}",
                "route_id": route["route_id"],
                "vehicle_id": route["vehicle_id"],
                "carbon_saved_kg": round(random.uniform(15, 45), 2),
                "cost_saved_usd": round(random.uniform(25, 85), 2),
                "optimization_score": route["optimization_score"],
                "verification_hash": generate_hash(f"{route['route_id']}{time.time()}"),
                "transaction_hash": f"0x{generate_hash(f'tx_{route['route_id']}')[:64]}",
                "block_number": random.randint(1000000, 2000000),
                "verified": True,
                "created_at": datetime.utcnow().isoformat(),
                "blockchain_network": "ganache_local"
            }
            certificates.append(certificate)
        
        return certificates
    
    def _calculate_environmental_impact(self, carbon_saved_kg: float) -> Dict[str, Any]:
        """Calculate environmental impact equivalents"""
        return {
            "trees_planted_equivalent": round(carbon_saved_kg / 21.77, 1),
            "cars_off_road_days": round(carbon_saved_kg / 12.6, 1),
            "homes_powered_hours": round(carbon_saved_kg / 0.83, 1),
            "miles_not_driven": round(carbon_saved_kg / 0.404, 1),
            "gallons_fuel_saved": round(carbon_saved_kg / 8.89, 1)
        }
    
    def _calculate_walmart_scale_projection(self, savings: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate Walmart-scale impact projections"""
        # Walmart scale: 10,500 stores, ~2.6M daily deliveries
        daily_multiplier = 2_625_000  # Daily deliveries across all stores
        annual_multiplier = daily_multiplier * 365
        
        return {
            "daily_cost_savings_usd": savings["cost_saved_usd"] * daily_multiplier,
            "annual_cost_savings_usd": savings["cost_saved_usd"] * annual_multiplier,
            "daily_carbon_reduction_kg": savings["carbon_saved_kg"] * daily_multiplier,
            "annual_carbon_reduction_tons": (savings["carbon_saved_kg"] * annual_multiplier) / 1000,
            "stores_impacted": 10_500,
            "confidence_level": 0.89,
            "roi_projection": {
                "implementation_cost_usd": 350_000_000,  # $350M over 3 years
                "annual_benefits_usd": savings["cost_saved_usd"] * annual_multiplier,
                "payback_period_months": 8,
                "net_present_value_usd": 4_200_000_000  # $4.2B over 5 years
            }
        }
    
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
        scenario_id = generate_demo_id()
        
        # Area centers for different cities
        area_centers = {
            "new_york": (40.7128, -74.0060),
            "chicago": (41.8781, -87.6298),
            "los_angeles": (34.0522, -118.2437),
            "houston": (29.7604, -95.3698),
            "phoenix": (33.4484, -112.0740)
        }
        
        center = area_centers.get(area.lower(), area_centers["new_york"])
        
        # Generate locations
        locations = []
        coordinates = generate_random_coordinates(center[0], center[1], 30, num_locations)
        
        for i, coord in enumerate(coordinates):
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
        
        # Generate vehicles
        vehicles = []
        for i in range(num_vehicles):
            vehicle_type = random.choice(vehicle_types)
            vehicle_spec = self.vehicle_types.get(vehicle_type, self.vehicle_types["diesel_truck"])
            
            vehicle = {
                "id": f"{area}_vehicle_{i+1:03d}",
                "type": vehicle_type,
                "capacity_kg": vehicle_spec["capacity_kg"],
                "cost_per_km": vehicle_spec["cost_per_km"],
                "emission_factor": vehicle_spec["emission_factor"],
                "efficiency_rating": vehicle_spec["efficiency_rating"]
            }
            vehicles.append(vehicle)
        
        # Generate optimization results
        traditional_result = self._simulate_traditional_optimization(locations, vehicles)
        quantum_result = self._simulate_quantum_optimization(locations, vehicles)
        
        return {
            "scenario_id": scenario_id,
            "scenario_name": f"Custom {area.title()} Delivery Scenario",
            "description": f"Custom scenario with {num_locations} locations and {num_vehicles} vehicles",
            "locations": locations,
            "vehicles": vehicles,
            "traditional_optimization": traditional_result,
            "quantum_optimization": quantum_result,
            "savings_analysis": self._calculate_savings_analysis(traditional_result, quantum_result),
            "generated_at": datetime.utcnow().isoformat()
        }

# Global demo data generator instance
demo_generator = DemoDataGenerator()
