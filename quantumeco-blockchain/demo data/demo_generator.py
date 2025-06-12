import json
import random
import time
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Any

class DemoDataGenerator:
    def __init__(self):
        self.vehicle_types = [
            {"type": "diesel_truck", "emission_factor": 0.27, "cost_per_km": 0.85},
            {"type": "electric_van", "emission_factor": 0.05, "cost_per_km": 0.65},
            {"type": "hybrid_delivery", "emission_factor": 0.12, "cost_per_km": 0.75}
        ]
        
        self.nyc_locations = [
            {"name": "Walmart NYC Distribution Center", "lat": 40.7128, "lng": -74.0060},
            {"name": "Manhattan Store", "lat": 40.7589, "lng": -73.9851},
            {"name": "Brooklyn Store", "lat": 40.6892, "lng": -73.9442}
        ]

    def generate_delivery_scenario(self, num_locations=50, num_vehicles=5) -> Dict[str, Any]:
        """Generate complete demo scenario with optimized routes and blockchain data"""
        scenario = {
            "scenario_id": f"scenario_{int(time.time())}",
            "name": "Walmart NYC Quantum Optimization",
            "description": f"{num_locations} deliveries optimized using quantum-inspired algorithms",
            "generated_at": datetime.utcnow().isoformat(),
            "locations": self._generate_locations(num_locations),
            "vehicles": self._generate_vehicles(num_vehicles),
            "optimization_results": {},
            "blockchain_certificates": []
        }
        
        # Generate traditional and quantum results
        scenario["optimization_results"] = {
            "traditional": self._simulate_traditional_routing(scenario),
            "quantum": self._simulate_quantum_optimization(scenario)
        }
        
        # Generate blockchain certificates
        scenario["blockchain_certificates"] = self._generate_blockchain_data(scenario)
        
        return scenario

    def _generate_locations(self, count: int) -> List[Dict[str, Any]]:
        """Generate delivery locations around NYC"""
        locations = []
        for i in range(count):
            base = random.choice(self.nyc_locations)
            locations.append({
                "id": f"loc_{i+1}",
                "name": f"Delivery {i+1}",
                "lat": base["lat"] + random.uniform(-0.1, 0.1),
                "lng": base["lng"] + random.uniform(-0.1, 0.1),
                "priority": random.choice(["high", "medium", "low"]),
                "weight_kg": random.randint(10, 200),
                "time_window": self._random_time_window()
            })
        return locations

    def _generate_vehicles(self, count: int) -> List[Dict[str, Any]]:
        """Generate delivery vehicles with different profiles"""
        vehicles = []
        for i in range(count):
            vehicle_type = random.choice(self.vehicle_types)
            vehicles.append({
                "id": f"vehicle_{i+1}",
                "type": vehicle_type["type"],
                "capacity_kg": 1000 if vehicle_type["type"] == "diesel_truck" else 500,
                "base_location": random.choice(self.nyc_locations),
                "cost_per_km": vehicle_type["cost_per_km"],
                "emission_factor": vehicle_type["emission_factor"]
            })
        return vehicles

    def _simulate_traditional_routing(self, scenario: Dict) -> Dict[str, Any]:
        """Simulate traditional routing results"""
        return {
            "total_distance": round(random.uniform(500, 800), 2),
            "total_time_hrs": round(random.uniform(12, 18), 1),
            "total_cost_usd": round(random.uniform(850, 1200), 2),
            "total_carbon": round(random.uniform(250, 400), 2),
            "routes_used": len(scenario["vehicles"]) + random.randint(0, 2)
        }

    def _simulate_quantum_optimization(self, scenario: Dict) -> Dict[str, Any]:
        """Simulate quantum-inspired optimization results"""
        traditional = scenario["optimization_results"]["traditional"]
        return {
            "total_distance": round(traditional["total_distance"] * 0.75, 2),
            "total_time_hrs": round(traditional["total_time_hrs"] * 0.72, 1),
            "total_cost_usd": round(traditional["total_cost_usd"] * 0.75, 2),
            "total_carbon": round(traditional["total_carbon"] * 0.65, 2),
            "routes_used": len(scenario["vehicles"]) - random.randint(0, 2),
            "optimization_time_sec": round(random.uniform(8, 15), 1),
            "quantum_score": random.randint(85, 95)
        }

    def _generate_blockchain_data(self, scenario: Dict) -> List[Dict[str, Any]]:
        """Generate blockchain certificates for all routes"""
        certificates = []
        for i in range(scenario["optimization_results"]["quantum"]["routes_used"]):
            cert_id = hashlib.sha256(f"{scenario['scenario_id']}_route_{i}".encode()).hexdigest()
            certificates.append({
                "certificate_id": cert_id,
                "route_id": f"route_{i+1}",
                "vehicle_id": scenario["vehicles"][i % len(scenario["vehicles"])]["id"],
                "carbon_saved_kg": round(
                    scenario["optimization_results"]["traditional"]["total_carbon"] -
                    scenario["optimization_results"]["quantum"]["total_carbon"], 2
                ),
                "cost_saved_usd": round(
                    scenario["optimization_results"]["traditional"]["total_cost_usd"] -
                    scenario["optimization_results"]["quantum"]["total_cost_usd"], 2
                ),
                "transaction_hash": f"0x{hashlib.sha256(cert_id.encode()).hexdigest()[:64]}",
                "block_number": random.randint(1000000, 2000000),
                "timestamp": datetime.utcnow().isoformat()
            })
        return certificates

    def save_sample_data(self, filename="sample_data.json"):
        """Generate and save sample data scenario"""
        data = self.generate_delivery_scenario()
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        return data

    def _random_time_window(self) -> Dict[str, str]:
        """Generate random delivery time window"""
        start_hour = random.randint(8, 12)
        return {
            "start": f"{start_hour:02d}:00",
            "end": f"{start_hour + 4:02d}:00"
        }

if __name__ == "__main__":
    generator = DemoDataGenerator()
    sample_data = generator.save_sample_data()
    print(f"Generated sample data with {len(sample_data['locations'])} locations and {len(sample_data['vehicles'])} vehicles")
