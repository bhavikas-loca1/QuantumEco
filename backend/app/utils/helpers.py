import uuid
import hashlib
import math
import random
import re
from datetime import datetime, date, timedelta
from typing import List, Tuple, Optional, Any, Dict
import string

def generate_demo_id() -> str:
    """Generate a unique demo identifier"""
    timestamp = int(datetime.utcnow().timestamp())
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"demo_{timestamp}_{random_suffix}"

def generate_route_id() -> str:
    """Generate a unique route identifier"""
    timestamp = int(datetime.utcnow().timestamp())
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"route_{timestamp}_{random_suffix}"

def generate_calculation_id() -> str:
    """Generate a unique calculation identifier"""
    return f"calc_{uuid.uuid4().hex[:12]}"

def generate_certificate_id() -> str:
    """Generate a unique certificate identifier"""
    timestamp = int(datetime.utcnow().timestamp())
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return f"cert_{timestamp}_{random_suffix}"

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on earth using Haversine formula
    Returns distance in kilometers
    """
    # Convert decimal degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = (math.sin(dlat / 2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    R = 6371
    distance = R * c
    
    return round(distance, 3)

def validate_coordinates(latitude: float, longitude: float) -> bool:
    """Validate latitude and longitude coordinates"""
    try:
        lat = float(latitude)
        lon = float(longitude)
        
        # Check latitude range
        if not -90 <= lat <= 90:
            return False
        
        # Check longitude range
        if not -180 <= lon <= 180:
            return False
        
        return True
    except (ValueError, TypeError):
        return False

def validate_date_format(date_string: str, format_string: str = "%Y-%m-%d") -> bool:
    """Validate date string format"""
    try:
        datetime.strptime(date_string, format_string)
        return True
    except ValueError:
        return False

def validate_ethereum_address(address: str) -> bool:
    """Validate Ethereum address format"""
    if not address:
        return False
    
    # Check if it starts with 0x and has correct length
    if not address.startswith('0x'):
        return False
    
    if len(address) != 42:
        return False
    
    # Check if all characters after 0x are valid hex
    try:
        int(address[2:], 16)
        return True
    except ValueError:
        return False

def validate_date_range(start_date: str, end_date: str, format_string: str = "%Y-%m-%d") -> bool:
    """Validate that start_date is before end_date"""
    try:
        start = datetime.strptime(start_date, format_string)
        end = datetime.strptime(end_date, format_string)
        return start <= end
    except ValueError:
        return False

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change between two values"""
    if old_value == 0:
        return 100.0 if new_value > 0 else 0.0
    
    change = ((new_value - old_value) / abs(old_value)) * 100
    return round(change, 2)

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency amount with proper symbols"""
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥"
    }
    
    symbol = currency_symbols.get(currency, currency)
    
    if amount >= 1_000_000:
        return f"{symbol}{amount / 1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"{symbol}{amount / 1_000:.1f}K"
    else:
        return f"{symbol}{amount:.2f}"

def format_weight(weight_kg: float, unit: str = "kg") -> str:
    """Format weight with appropriate units"""
    if unit.lower() == "tons" or unit.lower() == "tonnes":
        if weight_kg >= 1000:
            return f"{weight_kg / 1000:.2f} tons"
        else:
            return f"{weight_kg:.2f} kg"
    elif unit.lower() == "lbs":
        weight_lbs = weight_kg * 2.20462
        return f"{weight_lbs:.2f} lbs"
    else:
        return f"{weight_kg:.2f} kg"

def format_distance(distance_km: float, unit: str = "km") -> str:
    """Format distance with appropriate units"""
    if unit.lower() == "miles":
        distance_miles = distance_km * 0.621371
        return f"{distance_miles:.2f} miles"
    else:
        return f"{distance_km:.2f} km"

def generate_hash(data: str) -> str:
    """Generate SHA-256 hash of data"""
    return hashlib.sha256(data.encode()).hexdigest()

def generate_short_hash(data: str, length: int = 8) -> str:
    """Generate short hash for display purposes"""
    full_hash = generate_hash(data)
    return full_hash[:length]

def sanitize_string(input_string: str, max_length: int = 255) -> str:
    """Sanitize string input for database storage"""
    if not input_string:
        return ""
    
    # Remove special characters and limit length
    sanitized = re.sub(r'[^\w\s\-\.]', '', input_string)
    return sanitized[:max_length].strip()

def generate_random_coordinates(center_lat: float, center_lon: float, 
                              radius_km: float, count: int) -> List[Tuple[float, float]]:
    """Generate random coordinates within a radius of a center point"""
    coordinates = []
    
    for _ in range(count):
        # Convert radius from km to degrees (approximate)
        radius_deg = radius_km / 111.0  # 1 degree ≈ 111 km
        
        # Generate random angle and distance
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, radius_deg)
        
        # Calculate new coordinates
        lat = center_lat + distance * math.cos(angle)
        lon = center_lon + distance * math.sin(angle) / math.cos(math.radians(center_lat))
        
        # Ensure coordinates are valid
        lat = max(-90, min(90, lat))
        lon = max(-180, min(180, lon))
        
        coordinates.append((round(lat, 6), round(lon, 6)))
    
    return coordinates

def calculate_route_geometry(locations: List[Tuple[float, float]]) -> List[List[float]]:
    """Calculate simple route geometry (straight lines between points)"""
    if len(locations) < 2:
        return []
    
    geometry = []
    
    for i in range(len(locations) - 1):
        start_lat, start_lon = locations[i]
        end_lat, end_lon = locations[i + 1]
        
        # Add intermediate points for smoother lines
        steps = 5
        for step in range(steps + 1):
            ratio = step / steps
            lat = start_lat + (end_lat - start_lat) * ratio
            lon = start_lon + (end_lon - start_lon) * ratio
            geometry.append([lat, lon])
    
    return geometry

def estimate_travel_time(distance_km: float, vehicle_type: str = "truck", 
                        traffic_factor: float = 1.0) -> float:
    """Estimate travel time in minutes based on distance and vehicle type"""
    # Average speeds by vehicle type (km/h)
    speeds = {
        "truck": 45,
        "van": 50,
        "car": 55,
        "bike": 25,
        "walking": 5
    }
    
    base_speed = speeds.get(vehicle_type, 45)
    adjusted_speed = base_speed / traffic_factor
    
    # Time in hours, converted to minutes
    time_hours = distance_km / adjusted_speed
    return round(time_hours * 60, 1)

def calculate_fuel_cost(distance_km: float, fuel_efficiency: float, 
                       fuel_price_per_liter: float = 1.5) -> float:
    """Calculate fuel cost for a given distance"""
    # fuel_efficiency in km per liter
    liters_needed = distance_km / fuel_efficiency
    return round(liters_needed * fuel_price_per_liter, 2)

def generate_time_series_data(start_date: datetime, end_date: datetime, 
                             interval_hours: int = 1) -> List[datetime]:
    """Generate time series data points between two dates"""
    time_points = []
    current = start_date
    
    while current <= end_date:
        time_points.append(current)
        current += timedelta(hours=interval_hours)
    
    return time_points

def calculate_carbon_equivalent(carbon_kg: float, equivalent_type: str) -> float:
    """Calculate carbon equivalent in different units"""
    equivalents = {
        "trees_planted": carbon_kg / 21.77,  # kg CO2 absorbed per tree per year
        "cars_off_road_days": carbon_kg / 12.6,  # kg CO2 per car per day
        "homes_powered_hours": carbon_kg / 0.83,  # kg CO2 per home per hour
        "miles_not_driven": carbon_kg / 0.404,  # kg CO2 per mile
        "gallons_fuel_saved": carbon_kg / 8.89  # kg CO2 per gallon gasoline
    }
    
    return round(equivalents.get(equivalent_type, 0), 2)

def validate_vehicle_capacity(demand_kg: float, capacity_kg: float, 
                            load_factor: float = 1.0) -> bool:
    """Validate if vehicle capacity can handle the demand"""
    effective_capacity = capacity_kg * load_factor
    return demand_kg <= effective_capacity

def generate_optimization_id() -> str:
    """Generate unique optimization identifier"""
    return f"opt_{uuid.uuid4().hex[:16]}"

def calculate_efficiency_score(actual_value: float, optimal_value: float) -> float:
    """Calculate efficiency score as percentage"""
    if optimal_value == 0:
        return 100.0
    
    efficiency = (optimal_value / actual_value) * 100
    return min(100.0, max(0.0, round(efficiency, 1)))

def format_duration(minutes: float) -> str:
    """Format duration in human-readable format"""
    if minutes < 60:
        return f"{minutes:.0f} minutes"
    elif minutes < 1440:  # Less than 24 hours
        hours = minutes / 60
        return f"{hours:.1f} hours"
    else:
        days = minutes / 1440
        return f"{days:.1f} days"

def validate_optimization_goals(goals: Dict[str, float]) -> bool:
    """Validate optimization goals sum to approximately 1.0"""
    total = sum(goals.values())
    return abs(total - 1.0) <= 0.01

def generate_mock_weather_data() -> Dict[str, Any]:
    """Generate mock weather data for testing"""
    conditions = ["clear", "cloudy", "rain", "snow", "fog"]
    
    return {
        "condition": random.choice(conditions),
        "temperature": random.randint(-10, 35),
        "humidity": random.randint(30, 90),
        "wind_speed": random.randint(0, 30),
        "visibility": random.uniform(1, 10)
    }

def calculate_bounding_box(coordinates: List[Tuple[float, float]], 
                          padding: float = 0.01) -> Dict[str, float]:
    """Calculate bounding box for a list of coordinates"""
    if not coordinates:
        return {"north": 0, "south": 0, "east": 0, "west": 0}
    
    lats = [coord[0] for coord in coordinates]
    lons = [coord[1] for coord in coordinates]
    
    return {
        "north": max(lats) + padding,
        "south": min(lats) - padding,
        "east": max(lons) + padding,
        "west": min(lons) - padding
    }

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is zero"""
    if denominator == 0:
        return default
    return numerator / denominator

def clamp(value: float, min_value: float, max_value: float) -> float:
    """Clamp value between min and max"""
    return max(min_value, min(max_value, value))

def generate_tracking_id() -> str:
    """Generate unique tracking identifier"""
    return f"track_{uuid.uuid4().hex[:12]}"

def format_percentage(value: float, decimal_places: int = 1) -> str:
    """Format percentage with proper symbol"""
    return f"{value:.{decimal_places}f}%"
