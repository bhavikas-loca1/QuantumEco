import asyncio
import random
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import numpy as np

class DemoDataService:
    """Service for generating demo data and scenarios"""
    
    def __init__(self):
        self.nyc_locations = [
            {"name": "Walmart Supercenter - Bronx", "lat": 40.8448, "lng": -73.8648},
            {"name": "Walmart Neighborhood Market - Manhattan", "lat": 40.7589, "lng": -73.9851},
            {"name": "Walmart Supercenter - Queens", "lat": 40.7282, "lng": -73.7949},
            {"name": "Walmart Supercenter - Brooklyn", "lat": 40.6892, "lng": -73.9442},
            {"name": "Walmart Supercenter - Staten Island", "lat": 40.5795, "lng": -74.1502}
        ]
        
        self.delivery_addresses = [
            {"address": "Times Square, NY", "lat": 40.7580, "lng": -73.9855},
            {"address": "Central Park, NY", "lat": 40.7829, "lng": -73.9654},
            {"address": "Brooklyn Bridge, NY", "lat": 40.7061, "lng": -73.9969},
            {"address": "Statue of Liberty, NY", "lat": 40.6892, "lng": -74.0445},
            {"address": "Empire State Building, NY", "lat": 40.7484, "lng": -73.9857},
            {"address": "One World Trade Center, NY", "lat": 40.7127, "lng": -74.0134},
            {"address": "High Line, NY", "lat": 40.7480, "lng": -74.0048},
            {"address": "Coney Island, NY", "lat": 40.5749, "lng": -73.9857},
            {"address": "Yankee Stadium, NY", "lat": 40.8296, "lng": -73.9262},
            {"address": "JFK Airport, NY", "lat": 40.6413, "lng": -73.7781}
        ]
        
        self.vehicle_types = [
            {"type": "diesel_truck", "capacity": 1000, "emission_factor": 0.27, "cost_per_km": 0.85},
            {"type": "electric_van", "capacity": 500, "emission_factor": 0.05, "cost_per_km": 0.65},
            {"type": "hybrid_delivery", "capacity": 750, "emission_factor": 0.12, "cost_per_km": 0.75},
            {"type": "gas_truck", "capacity": 800, "emission_factor": 0.23, "cost_per_km": 0.80}
        ]
    
    async def simulate_traditional_optimization(self, locations: List[Dict], vehicles: List[Dict]) -> Dict[str, Any]:
        """Simulate traditional optimization results (less efficient)"""
        print(f"[DEBUG] Starting traditional optimization with {len(locations)} locations and {len(vehicles)} vehicles")
        try:
            print("[INFO] Simulating processing time...")
            await asyncio.sleep(random.uniform(1, 3))
            
            total_distance = 0
            total_time = 0
            total_cost = 0
            total_carbon = 0
            
            # Simple simulation - distribute locations evenly among vehicles
            locations_per_vehicle = len(locations) // len(vehicles)
            print(f"[DEBUG] Calculated {locations_per_vehicle} locations per vehicle")
            
            routes = []
            for i, vehicle in enumerate(vehicles):
                print(f"[DEBUG] Processing vehicle {i+1}/{len(vehicles)}")
                start_idx = i * locations_per_vehicle
                end_idx = start_idx + locations_per_vehicle
                if i == len(vehicles) - 1:  # Last vehicle gets remaining locations
                    end_idx = len(locations)
                
                vehicle_locations = locations[start_idx:end_idx]
                print(f"[INFO] Vehicle {i+1} assigned {len(vehicle_locations)} locations")
                
                # Calculate route metrics (simplified)
                route_distance = len(vehicle_locations) * random.uniform(12, 20)  # km per delivery
                route_time = route_distance * random.uniform(4, 6)  # minutes per km
                route_cost = route_distance * vehicle.get("cost_per_km", 0.8)
                route_carbon = route_distance * vehicle.get("emission_factor", 0.2)
                
                total_distance += route_distance
                total_time += route_time
                total_cost += route_cost
                total_carbon += route_carbon
                
                routes.append({
                    "route_id": f"trad_route_{i+1:03d}_{int(time.time())}",
                    "vehicle_id": vehicle.get("id", f"vehicle_{i+1}"),
                    "vehicle_type": vehicle.get("type", "diesel_truck"),
                    "locations": vehicle_locations,
                    "distance_km": round(route_distance, 2),
                    "time_minutes": round(route_time, 2),
                    "cost_usd": round(route_cost, 2),
                    "carbon_emissions_kg": round(route_carbon, 2),
                    "optimization_score": random.randint(65, 75)
                })
            
            print(f"[INFO] Optimization completed successfully. Total routes: {len(routes)}")
            print(f"[DEBUG] Final metrics - Total Distance: {total_distance:.2f}km, Total Time: {total_time:.2f}min, "
                  f"Total Cost: ${total_cost:.2f}, Total Carbon: {total_carbon:.2f}kg")
            
            return {
                "method": "traditional",
                "routes": routes,
                "total_distance": round(total_distance, 2),
                "total_time": round(total_time, 2),
                "total_cost": round(total_cost, 2),
                "total_cost": round(total_cost, 2),
                "total_carbon": round(total_carbon, 2),
                "processing_time": random.uniform(2, 5),
                "success_rate": 100
            }
            
        except Exception as e:
            print(f"[ERROR] Critical failure in traditional optimization: {str(e)}")
            print(f"[ERROR] Stack trace: ", e.__traceback__)
            return {"error": str(e), "method": "traditional"}
    
    async def simulate_quantum_optimization(self, locations: List[Dict], vehicles: List[Dict]) -> Dict[str, Any]:
        """Simulate quantum-inspired optimization results (more efficient)"""
        print(f"[DEBUG] Starting quantum optimization with {len(locations)} locations and {len(vehicles)} vehicles")
        try:
            print("[INFO] Initializing quantum simulation processing time...")
            await asyncio.sleep(random.uniform(3, 8))
            
            print("[DEBUG] Fetching traditional optimization results as baseline...")
            traditional = await self.simulate_traditional_optimization(locations, vehicles)
            print(f"[INFO] Traditional optimization baseline received with {len(traditional.get('routes', []))} routes")
            
            print("[DEBUG] Calculating quantum improvement factors...")
            improvement_factors = {
                "distance": random.uniform(0.70, 0.80),    # 20-30% improvement
                "time": random.uniform(0.68, 0.78),        # 22-32% improvement
                "cost_usd": random.uniform(0.70, 0.80),   # 20-30% improvement
                "carbon": random.uniform(0.60, 0.75)       # 25-40% improvement
            }
            
            routes = []
            for idx, route in enumerate(traditional["routes"]):
                optimized_route = {
                    "route_id": f"quantum_route_{int(time.time())}",
                    "vehicle_id": route["vehicle_id"],
                    "vehicle_type": route["vehicle_type"],
                    "locations": route["locations"],
                    "distance_km": round(route["distance_km"] * improvement_factors["distance"], 2),
                    "time_minutes": round(route["time_minutes"] * improvement_factors["time"], 2),
                    "cost_usd": round(route["cost_usd"] * improvement_factors["cost_usd"], 2),
                    "carbon_emissions_kg": round(route["carbon_emissions_kg"] * improvement_factors["carbon"], 2),
                    "quantum_improvement_score": random.randint(88, 97),
                    "optimization_score": random.randint(88, 97)
                }
                routes.append(optimized_route)
            
            # Calculate totals
            total_distance = sum(route["distance_km"] for route in routes)
            total_time = sum(route["time_minutes"] for route in routes)
            total_cost = sum(route["cost_usd"] for route in routes)
            total_carbon = sum(route["carbon_emissions_kg"] for route in routes)
            
            return {
                "method": "quantum_inspired",
                "routes": routes,
                "total_distance": round(total_distance, 2),
                "total_time": round(total_time, 2),
                "total_cost": round(total_cost, 2),
                "total_cost": round(total_cost, 2),
                "total_carbon": round(total_carbon, 2),
                "processing_time": random.uniform(8, 15),
                "quantum_iterations": random.randint(50, 120),
                "convergence_score": random.uniform(0.90, 0.98),
                "quantum_improvement_score": random.randint(88, 97)
            }
            
        except Exception as e:
            return {"error": str(e), "method": "quantum_inspired"}
    
    async def run_custom_optimization(self, locations: List[Dict], vehicles: List[Dict], 
                                    optimization_goals: Dict[str, float], 
                                    include_weather: bool = True, 
                                    include_traffic: bool = True) -> Dict[str, Any]:
        """Run custom optimization with specified parameters"""
        print(f"[DEBUG] Starting custom optimization with {len(locations)} locations and {len(vehicles)} vehicles")
        print(f"[DEBUG] Optimization goals: {optimization_goals}")
        print(f"[DEBUG] Weather included: {include_weather}, Traffic included: {include_traffic}")
        
        try:
            # Simulate processing based on complexity
            complexity_factor = len(locations) * len(vehicles) / 100
            processing_time = min(20, max(5, complexity_factor))
            print(f"[INFO] Calculated complexity factor: {complexity_factor:.2f}, processing time: {processing_time:.2f}s")
            await asyncio.sleep(min(3, processing_time * 0.2))
            
            # Base calculations
            print("[DEBUG] Starting base calculations...")
            avg_distance_per_location = random.uniform(8, 25)
            total_base_distance = len(locations) * avg_distance_per_location
            print(f"[DEBUG] Average distance per location: {avg_distance_per_location:.2f}km")
            print(f"[DEBUG] Total base distance: {total_base_distance:.2f}km")
            
            # Apply optimization goals
            print("[INFO] Applying optimization weights...")
            cost_weight = optimization_goals.get('cost', 0.4)
            carbon_weight = optimization_goals.get('carbon', 0.4)
            time_weight = optimization_goals.get('time', 0.2)
            print(f"[DEBUG] Weights - Cost: {cost_weight}, Carbon: {carbon_weight}, Time: {time_weight}")
            
            # Calculate optimization efficiency
            print("[INFO] Calculating efficiency factors...")
            efficiency_factor = 0.6 + (carbon_weight * 0.3) + (cost_weight * 0.2) + (time_weight * 0.1)
            print(f"[DEBUG] Calculated efficiency factor: {efficiency_factor:.3f}")
            
            # Weather and traffic impacts
            weather_factor = 1.1 if include_weather else 1.0
            traffic_factor = 1.15 if include_traffic else 1.0
            print(f"[DEBUG] Applied factors - Weather: {weather_factor}, Traffic: {traffic_factor}")
            
            # Calculate final metrics
            print("[INFO] Computing final metrics...")
            total_distance = total_base_distance * efficiency_factor
            total_time = total_distance * 3.5 * traffic_factor
            total_cost = total_distance * 0.8 * weather_factor
            total_carbon = total_distance * 0.2 * efficiency_factor
            print(f"[DEBUG] Final totals - Distance: {total_distance:.2f}km, Time: {total_time:.2f}min")
            print(f"[DEBUG] Final totals - Cost: ${total_cost:.2f}, Carbon: {total_carbon:.2f}kg")
            
            # Generate routes
            print("[INFO] Generating individual vehicle routes...")
            routes = []
            locations_per_vehicle = len(locations) // len(vehicles)
            print(f"[DEBUG] Locations per vehicle: {locations_per_vehicle}")
            
            for i, vehicle in enumerate(vehicles):
                start_idx = i * locations_per_vehicle
                end_idx = min(start_idx + locations_per_vehicle, len(locations))
                vehicle_locations = locations[start_idx:end_idx]
                
                vehicle_distance = len(vehicle_locations) * avg_distance_per_location * efficiency_factor
                vehicle_time = vehicle_distance * 3.5 * traffic_factor
                vehicle_cost = vehicle_distance * vehicle.get("cost_per_km", 0.8) * weather_factor
                vehicle_carbon = vehicle_distance * vehicle.get("emission_factor", 0.2)
                
                routes.append({
                    "vehicle_id": vehicle.get("id", f"vehicle_{i+1}"),
                    "vehicle_type": vehicle.get("type", "diesel_truck"),
                    "locations": vehicle_locations,
                    "distance_km": round(vehicle_distance, 2),
                    "time_minutes": round(vehicle_time, 2),
                    "cost_usd": round(vehicle_cost, 2),
                    "carbon_kg": round(vehicle_carbon, 2),
                    "optimization_score": random.randint(80, 95)
                })
            
            return {
                "method": "custom_quantum_inspired",
                "routes": routes,
                "total_distance": round(total_distance, 2),
                "total_time": round(total_time, 2),
                "total_cost": round(total_cost, 2),
                "total_cost": round(total_cost, 2),
                "total_carbon": round(total_carbon, 2),
                "processing_time": round(processing_time, 2),
                "optimization_goals_applied": optimization_goals,
                "weather_included": include_weather,
                "traffic_included": include_traffic,
                "efficiency_factor": round(efficiency_factor, 3)
            }
            
        except Exception as e:
            print(f"[ERROR] Critical failure in custom optimization: {str(e)}")
            print(f"[ERROR] Stack trace: ", e.__traceback__)
            return {"error": str(e), "method": "custom"}
