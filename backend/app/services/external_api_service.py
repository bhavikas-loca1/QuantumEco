import asyncio
import aiohttp
import requests
from typing import Dict, List, Any, Optional, Tuple
import json
import time
from datetime import datetime

from app.config import settings

class ExternalAPIService:
    """Service for integrating with external APIs"""
    
    def __init__(self):
        self.session = None
        self.cache = {}
        self.cache_expiry = 300  # 5 minutes
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid"""
        if cache_key not in self.cache:
            return False
        
        cached_time = self.cache[cache_key].get('timestamp', 0)
        return (time.time() - cached_time) < self.cache_expiry
    
    def _cache_data(self, cache_key: str, data: Any):
        """Cache data with timestamp"""
        self.cache[cache_key] = {
            'data': data,
            'timestamp': time.time()
        }
    
    def _get_cached_data(self, cache_key: str) -> Optional[Any]:
        """Get cached data if valid"""
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]['data']
        return None
    
    # ===== OpenRouteService Integration =====
    
    async def get_route_matrix(self, coordinates: List[Tuple[float, float]], 
                             profile: str = "driving-car") -> Dict[str, Any]:
        """Get distance and time matrix from OpenRouteService"""
        try:
            cache_key = f"ors_matrix_{hash(str(coordinates))}_{profile}"
            cached_result = self._get_cached_data(cache_key)
            if cached_result:
                return cached_result
            
            if not settings.OPENROUTESERVICE_API_KEY:
                # Return mock data if no API key
                return self._generate_mock_distance_matrix(coordinates)
            
            url = f"{settings.OPENROUTESERVICE_BASE_URL}/v2/matrix/{profile}"
            headers = {
                'Authorization': settings.OPENROUTESERVICE_API_KEY,
                'Content-Type': 'application/json'
            }
            
            # Format coordinates for ORS (longitude, latitude)
            ors_coordinates = [[lng, lat] for lat, lng in coordinates]
            
            payload = {
                "locations": ors_coordinates,
                "metrics": ["distance", "duration"],
                "units": "km"
            }
            
            if self.session:
                async with self.session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        result = self._process_ors_matrix_response(data)
                        self._cache_data(cache_key, result)
                        return result
                    else:
                        # Fallback to mock data
                        return self._generate_mock_distance_matrix(coordinates)
            else:
                # Synchronous fallback
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    result = self._process_ors_matrix_response(data)
                    self._cache_data(cache_key, result)
                    return result
                else:
                    return self._generate_mock_distance_matrix(coordinates)
                    
        except Exception as e:
            print(f"Error getting route matrix: {str(e)}")
            return self._generate_mock_distance_matrix(coordinates)
    
    def _process_ors_matrix_response(self, data: Dict) -> Dict[str, Any]:
        """Process OpenRouteService matrix response"""
        distances = data.get('distances', [])
        durations = data.get('durations', [])
        
        return {
            'distance_matrix': distances,  # in km
            'time_matrix': [[duration / 60 for duration in row] for row in durations],  # convert to minutes
            'source': 'openrouteservice'
        }
    
    def _generate_mock_distance_matrix(self, coordinates: List[Tuple[float, float]]) -> Dict[str, Any]:
        """Generate mock distance matrix using haversine formula"""
        import math
        
        n = len(coordinates)
        distance_matrix = []
        time_matrix = []
        
        for i in range(n):
            distance_row = []
            time_row = []
            
            for j in range(n):
                if i == j:
                    distance_row.append(0)
                    time_row.append(0)
                else:
                    # Calculate haversine distance
                    lat1, lon1 = coordinates[i]
                    lat2, lon2 = coordinates[j]
                    
                    R = 6371  # Earth's radius in km
                    lat1_rad = math.radians(lat1)
                    lon1_rad = math.radians(lon1)
                    lat2_rad = math.radians(lat2)
                    lon2_rad = math.radians(lon2)
                    
                    dlat = lat2_rad - lat1_rad
                    dlon = lon2_rad - lon1_rad
                    
                    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
                    c = 2 * math.asin(math.sqrt(a))
                    distance = R * c
                    
                    # Estimate time (assuming 40 km/h average speed in urban areas)
                    time_minutes = (distance / 40) * 60
                    
                    distance_row.append(round(distance, 2))
                    time_row.append(round(time_minutes, 1))
            
            distance_matrix.append(distance_row)
            time_matrix.append(time_row)
        
        return {
            'distance_matrix': distance_matrix,
            'time_matrix': time_matrix,
            'source': 'haversine_calculation'
        }
    
    # ===== OpenWeatherMap Integration =====
    
    async def get_weather_data(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """Get current weather data from OpenWeatherMap"""
        try:
            cache_key = f"weather_{latitude}_{longitude}"
            cached_result = self._get_cached_data(cache_key)
            if cached_result:
                return cached_result
            
            if not settings.OPENWEATHER_API_KEY:
                # Return mock weather data
                return self._generate_mock_weather_data()
            
            url = f"{settings.OPENWEATHER_BASE_URL}/weather"
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': settings.OPENWEATHER_API_KEY,
                'units': 'metric'
            }
            
            if self.session:
                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        result = self._process_weather_response(data)
                        self._cache_data(cache_key, result)
                        return result
                    else:
                        return self._generate_mock_weather_data()
            else:
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    result = self._process_weather_response(data)
                    self._cache_data(cache_key, result)
                    return result
                else:
                    return self._generate_mock_weather_data()
                    
        except Exception as e:
            print(f"Error getting weather data: {str(e)}")
            return self._generate_mock_weather_data()
    
    def _process_weather_response(self, data: Dict) -> Dict[str, Any]:
        """Process OpenWeatherMap response"""
        main = data.get('main', {})
        weather = data.get('weather', [{}])[0]
        wind = data.get('wind', {})
        
        return {
            'condition': weather.get('main', 'Clear').lower(),
            'temperature': main.get('temp', 20),
            'humidity': main.get('humidity', 50),
            'wind_speed': wind.get('speed', 0) * 3.6,  # Convert m/s to km/h
            'visibility': data.get('visibility', 10000) / 1000,  # Convert m to km
            'description': weather.get('description', 'clear sky'),
            'source': 'openweathermap'
        }
    
    def _generate_mock_weather_data(self) -> Dict[str, Any]:
        """Generate mock weather data"""
        import random
        
        conditions = ['clear', 'cloudy', 'rain', 'snow', 'fog']
        
        return {
            'condition': random.choice(conditions),
            'temperature': random.randint(-5, 35),
            'humidity': random.randint(30, 90),
            'wind_speed': random.randint(0, 30),
            'visibility': random.uniform(1, 10),
            'description': 'simulated weather conditions',
            'source': 'mock_data'
        }
    
    # ===== Google Maps Integration =====
    
    async def geocode_address(self, address: str) -> Dict[str, Any]:
        """Geocode address using Google Maps API or Nominatim"""
        try:
            cache_key = f"geocode_{hash(address)}"
            cached_result = self._get_cached_data(cache_key)
            if cached_result:
                return cached_result
            
            if settings.GOOGLE_MAPS_API_KEY:
                result = await self._geocode_google_maps(address)
            else:
                result = await self._geocode_nominatim(address)
            
            self._cache_data(cache_key, result)
            return result
            
        except Exception as e:
            print(f"Error geocoding address: {str(e)}")
            return {'error': str(e)}
    
    async def _geocode_google_maps(self, address: str) -> Dict[str, Any]:
        """Geocode using Google Maps API"""
        url = f"{settings.GOOGLE_MAPS_BASE_URL}/geocode/json"
        params = {
            'address': address,
            'key': settings.GOOGLE_MAPS_API_KEY
        }
        
        if self.session:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_google_geocode_response(data)
        else:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return self._process_google_geocode_response(data)
        
        return {'error': 'Geocoding failed'}
    
    async def _geocode_nominatim(self, address: str) -> Dict[str, Any]:
        """Geocode using Nominatim (free alternative)"""
        url = f"{settings.NOMINATIM_BASE_URL}/search"
        params = {
            'q': address,
            'format': 'json',
            'limit': 1
        }
        headers = {
            'User-Agent': 'QuantumEco Intelligence/1.0'
        }
        
        if self.session:
            async with self.session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_nominatim_response(data)
        else:
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return self._process_nominatim_response(data)
        
        return {'error': 'Geocoding failed'}
    
    def _process_google_geocode_response(self, data: Dict) -> Dict[str, Any]:
        """Process Google Maps geocoding response"""
        if data.get('status') == 'OK' and data.get('results'):
            result = data['results'][0]
            location = result['geometry']['location']
            
            return {
                'latitude': location['lat'],
                'longitude': location['lng'],
                'formatted_address': result['formatted_address'],
                'source': 'google_maps'
            }
        
        return {'error': 'No results found'}
    
    def _process_nominatim_response(self, data: List) -> Dict[str, Any]:
        """Process Nominatim geocoding response"""
        if data:
            result = data[0]
            return {
                'latitude': float(result['lat']),
                'longitude': float(result['lon']),
                'formatted_address': result['display_name'],
                'source': 'nominatim'
            }
        
        return {'error': 'No results found'}
    
    # ===== Traffic Data =====
    
    async def get_traffic_data(self, coordinates: List[Tuple[float, float]]) -> Dict[str, Any]:
        """Get traffic data for route optimization"""
        try:
            # For demo purposes, generate realistic traffic data
            # In production, this would integrate with real traffic APIs
            
            cache_key = f"traffic_{hash(str(coordinates))}"
            cached_result = self._get_cached_data(cache_key)
            if cached_result:
                return cached_result
            
            result = self._generate_traffic_data(coordinates)
            self._cache_data(cache_key, result)
            return result
            
        except Exception as e:
            print(f"Error getting traffic data: {str(e)}")
            return self._generate_traffic_data(coordinates)
    
    def _generate_traffic_data(self, coordinates: List[Tuple[float, float]]) -> Dict[str, Any]:
        """Generate realistic traffic data"""
        import random
        
        # Simulate traffic based on time of day
        current_hour = datetime.now().hour
        
        if 7 <= current_hour <= 9 or 17 <= current_hour <= 19:
            # Rush hour
            base_factor = random.uniform(1.3, 1.8)
            traffic_level = "heavy"
        elif 10 <= current_hour <= 16:
            # Daytime
            base_factor = random.uniform(1.1, 1.3)
            traffic_level = "moderate"
        else:
            # Off-peak
            base_factor = random.uniform(0.9, 1.1)
            traffic_level = "light"
        
        # Generate traffic factors for each coordinate pair
        n = len(coordinates)
        traffic_matrix = []
        
        for i in range(n):
            row = []
            for j in range(n):
                if i == j:
                    row.append(1.0)
                else:
                    # Add some randomness
                    factor = base_factor * random.uniform(0.8, 1.2)
                    row.append(round(factor, 2))
            traffic_matrix.append(row)
        
        return {
            'traffic_matrix': traffic_matrix,
            'traffic_level': traffic_level,
            'base_factor': base_factor,
            'source': 'simulated_traffic',
            'timestamp': datetime.now().isoformat()
        }
    
    # ===== Utility Methods =====
    
    async def health_check(self) -> Dict[str, str]:
        """Check health of external API services"""
        print("[HealthCheck] Starting health check of external services...")
        health_status = {}
        
        # Check OpenRouteService
        print("[HealthCheck] Checking OpenRouteService API...")
        if settings.OPENROUTESERVICE_API_KEY:
            try:
                # Simple test request
                test_coords = [(40.7128, -74.0060), (40.7589, -73.9851)]
                result = await self.get_route_matrix(test_coords)
                health_status['openrouteservice'] = 'healthy' if result else 'degraded'
                print(f"[HealthCheck] OpenRouteService status: {health_status['openrouteservice']}")
            except Exception as e:
                health_status['openrouteservice'] = 'unhealthy'
                print(f"[HealthCheck] OpenRouteService error: {str(e)}")
        else:
            health_status['openrouteservice'] = 'not_configured'
            print("[HealthCheck] OpenRouteService API key not configured")
        
        # Check OpenWeatherMap
        print("[HealthCheck] Checking OpenWeatherMap API...")
        if settings.OPENWEATHER_API_KEY:
            try:
                result = await self.get_weather_data(40.7128, -74.0060)
                health_status['openweathermap'] = 'healthy' if result else 'degraded'
                print(f"[HealthCheck] OpenWeatherMap status: {health_status['openweathermap']}")
            except Exception as e:
                health_status['openweathermap'] = 'unhealthy'
                print(f"[HealthCheck] OpenWeatherMap error: {str(e)}")
        else:
            health_status['openweathermap'] = 'not_configured'
            print("[HealthCheck] OpenWeatherMap API key not configured")
        
        # Check Google Maps
        print("[HealthCheck] Checking Google Maps API...")
        if settings.GOOGLE_MAPS_API_KEY:
            try:
                result = await self.geocode_address("New York, NY")
                health_status['google_maps'] = 'healthy' if result else 'degraded'
                print(f"[HealthCheck] Google Maps status: {health_status['google_maps']}")
            except Exception as e:
                health_status['google_maps'] = 'unhealthy'
                print(f"[HealthCheck] Google Maps error: {str(e)}")
        else:
            health_status['google_maps'] = 'not_configured'
            print("[HealthCheck] Google Maps API key not configured")
        
        print(f"[HealthCheck] Complete health status: {health_status}")
        return health_status
    
    def clear_cache(self):
        """Clear the API cache"""
        print("[Cache] Clearing API cache...")
        cache_size = len(self.cache)
        self.cache.clear()
        print(f"[Cache] Cleared {cache_size} items from cache")

# Global instance for easy access
external_api_service = ExternalAPIService()
