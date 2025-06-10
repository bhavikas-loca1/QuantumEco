from typing import Dict, Any

class TestScenarios:
    @staticmethod
    def basic_optimization_test() -> Dict[str, Any]:
        return {
            "name": "Basic Route Optimization",
            "input": {
                "locations": [
                    {"id": "depot", "lat": 40.7128, "lng": -74.0060, "weight_kg": 0},
                    {"id": "loc1", "lat": 40.7589, "lng": -73.9851, "weight_kg": 50}
                ],
                "vehicles": [
                    {"id": "truck1", "type": "diesel_truck", "capacity_kg": 1000}
                ]
            },
            "expected": {
                "total_distance_km": {"min": 8, "max": 12},
                "total_cost_usd": {"min": 6, "max": 10}
            }
        }

    @staticmethod
    def carbon_calculation_test() -> Dict[str, Any]:
        return {
            "name": "Carbon Calculation Validation",
            "input": {
                "routes": [
                    {"distance_km": 100, "vehicle_type": "diesel_truck"}
                ]
            },
            "expected": {
                "carbon_kg": {"min": 25, "max": 30}
            }
        }

    @staticmethod
    def blockchain_verification_test() -> Dict[str, Any]:
        return {
            "name": "Blockchain Certificate Verification",
            "input": {
                "route_id": "test_route_001",
                "carbon_saved_kg": 25.5,
                "cost_saved_usd": 45.75
            },
            "expected": {
                "transaction_status": "verified",
                "block_confirmation": {"min": 3, "max": 10}
            }
        }

    @staticmethod
    def full_system_test() -> Dict[str, Any]:
        return {
            "name": "Full System Integration Test",
            "input": {
                "locations": 10,
                "vehicles": 2
            },
            "expected": {
                "optimization_time_sec": {"min": 5, "max": 15},
                "cost_saving_percent": {"min": 20, "max": 35}
            }
        }
