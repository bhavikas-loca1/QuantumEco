from pydantic_settings import BaseSettings
from typing import Any, Dict, Optional, List
import os
from pathlib import Path

class Settings(BaseSettings):
    """
    Application configuration settings for QuantumEco Intelligence
    Uses Pydantic BaseSettings for environment variable management
    """
    
    # ===== API Configuration =====
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "QuantumEco Intelligence"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "Quantum-inspired logistics optimization with blockchain verification"
    DEBUG: bool = False
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "*"  # Allow all origins for hackathon demo
    ]
    
    # ===== Database Configuration =====
    # SQLite for development (no setup required)
    DATABASE_URL: str = "sqlite:///./quantumeco.db"
    DATABASE_ECHO: bool = False  # Set to True for SQL query logging
    
    # PostgreSQL for production (optional)
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_PORT: int = 5432
    
    @property
    def postgres_database_url(self) -> Optional[str]:
        """Generate PostgreSQL database URL if credentials are provided"""
        if all([self.POSTGRES_SERVER, self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_DB]):
            return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return None
    
    # ===== Blockchain Configuration =====
    # Ganache local blockchain settings
    BLOCKCHAIN_URL: str = "http://127.0.0.1:8545"
    BLOCKCHAIN_NETWORK_ID: int = 1337  # Ganache default
    
    # Smart contract addresses (set after deployment)
    DELIVERY_CONTRACT_ADDRESS: Optional[str] = None
    CARBON_CONTRACT_ADDRESS: Optional[str] = None
    ETT_CONTRACT_ADDRESS: Optional[str] = None
    
    # Blockchain transaction settings
    DEFAULT_GAS_LIMIT: int = 300000
    DEFAULT_GAS_PRICE: int = 20000000000  # 20 Gwei
    TRANSACTION_TIMEOUT: int = 60  # seconds
    
    # Account settings (for demo - in production use secure key management)
    PRIVATE_KEY: Optional[str] = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"  # Ganache default
    DEFAULT_ACCOUNT: Optional[str] = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"  # Ganache default
    
    # ===== External API Keys =====
    # OpenRouteService (free tier: 2000 requests/day)
    OPENROUTESERVICE_API_KEY: Optional[str] = None
    OPENROUTESERVICE_BASE_URL: str = "https://api.openrouteservice.org"
    
    # OpenWeatherMap (free tier: 1000 calls/day)
    OPENWEATHER_API_KEY: Optional[str] = None
    OPENWEATHER_BASE_URL: str = "https://api.openweathermap.org/data/2.5"
    
    # Google Maps API
    GOOGLE_MAPS_API_KEY: Optional[str] = None
    GOOGLE_MAPS_BASE_URL: str = "https://maps.googleapis.com/maps/api"
    
    # Nominatim for geocoding (free, no API key required)
    NOMINATIM_BASE_URL: str = "https://nominatim.openstreetmap.org"
    
    # ===== Optimization Parameters =====
    # General optimization settings
    OPTIMIZATION_TIMEOUT: int = 30  # seconds
    MAX_LOCATIONS_PER_REQUEST: int = 100
    MAX_VEHICLES_PER_REQUEST: int = 20
    MAX_BATCH_SCENARIOS: int = 10
    
    # Quantum-inspired algorithm parameters
    QUANTUM_POPULATION_SIZE: int = 50
    QUANTUM_MAX_ITERATIONS: int = 100
    QUANTUM_TUNNEL_PROBABILITY: float = 0.15
    QUANTUM_SUPERPOSITION_FACTOR: float = 0.8
    QUANTUM_ENTANGLEMENT_STRENGTH: float = 0.3
    
    # Analytics and demo configuration:
    CACHE_EXPIRY_MINUTES: int = 5
    MAX_SIMULATION_SIZE: int = 100000  
    DEMO_COMPLEXITY_LIMITS: dict = {"low": 50, "medium": 100, "high": 200}

    # Simulated annealing parameters
    ANNEALING_START_TEMP: float = 1000.0
    ANNEALING_ALPHA: float = 0.995
    ANNEALING_MIN_TEMP: float = 0.01
    
    # Genetic algorithm parameters
    GA_CROSSOVER_PROBABILITY: float = 0.8
    GA_MUTATION_PROBABILITY: float = 0.02
    GA_ELITE_PERCENTAGE: float = 0.1
    
    # Multi-objective optimization weights
    DEFAULT_COST_WEIGHT: float = 0.4
    DEFAULT_CARBON_WEIGHT: float = 0.4
    DEFAULT_TIME_WEIGHT: float = 0.2
    
    # ===== Carbon Calculation Settings =====
    # Carbon pricing (USD per ton CO2)
    CARBON_PRICE_PER_TON: float = 50.0
    
    # Environmental equivalents (for impact visualization)
    TREE_CO2_ABSORPTION_KG_PER_YEAR: float = 21.77
    CAR_ANNUAL_EMISSIONS_KG: float = 4600
    HOME_ANNUAL_EMISSIONS_KG: float = 7300
    GALLON_GASOLINE_EMISSIONS_KG: float = 8.89
    
    # Calculation precision
    EMISSION_CALCULATION_PRECISION: int = 3
    COST_CALCULATION_PRECISION: int = 2
    
    # ===== Performance and Caching =====
    # Cache settings
    CACHE_EXPIRY_MINUTES: int = 30
    MAX_CACHE_SIZE: int = 1000
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    RATE_LIMIT_BURST: int = 20
    
    # ===== Demo and Development Settings =====
    # Demo mode settings
    ENABLE_DEMO_MODE: bool = True
    DEMO_DATA_SIZE: int = 1000
    GENERATE_DEMO_CERTIFICATES: bool = True
    
    # Walmart-specific demo parameters
    WALMART_STORES_COUNT: int = 10500
    WALMART_DAILY_DELIVERIES_PER_STORE: int = 250
    
    # ===== Logging Configuration =====
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: Optional[str] = None  # Set to file path to enable file logging
    
    # ===== Security Settings =====
    # JWT settings (if implementing authentication)
    SECRET_KEY: str = "quantum-eco-intelligence-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ===== File Storage =====
    # Upload settings
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = [".json", ".csv", ".xlsx"]
    
    # ===== Monitoring and Health Checks =====
    HEALTH_CHECK_INTERVAL: int = 60  # seconds
    SERVICE_TIMEOUT: int = 30  # seconds
    
    # ===== Environment-Specific Overrides =====
    ENVIRONMENT: str = "development"  # development, staging, production
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT.lower() == "development"
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"
    
    # ===== Derived Properties =====
    @property
    def database_url_to_use(self) -> str:
        """Return the appropriate database URL based on environment"""
        if self.is_production and self.postgres_database_url:
            return self.postgres_database_url
        return self.DATABASE_URL
    
    @property
    def walmart_total_daily_deliveries(self) -> int:
        """Calculate total daily deliveries across all Walmart stores"""
        return self.WALMART_STORES_COUNT * self.WALMART_DAILY_DELIVERIES_PER_STORE
    
    # ===== Validation Methods =====
    def validate_api_keys(self) -> Dict[str, bool]:
        """Validate which external API keys are configured"""
        return {
            "openrouteservice": bool(self.OPENROUTESERVICE_API_KEY),
            "openweather": bool(self.OPENWEATHER_API_KEY),
            "google_maps": bool(self.GOOGLE_MAPS_API_KEY)
        }
    
    def get_optimization_weights(self) -> Dict[str, float]:
        """Get default optimization weights"""
        return {
            "cost": self.DEFAULT_COST_WEIGHT,
            "carbon": self.DEFAULT_CARBON_WEIGHT,
            "time": self.DEFAULT_TIME_WEIGHT
        }
    
    # ===== Pydantic Configuration =====
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        
        # Allow extra fields for flexibility
        extra = "allow"

# Global settings instance
settings = Settings()

# ===== Helper Functions =====
def get_project_root() -> Path:
    """Get the project root directory"""
    return Path(__file__).parent.parent

def ensure_directories():
    """Ensure required directories exist"""
    directories = [
        settings.UPLOAD_DIR,
        "logs",
        "data",
        "exports"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def get_database_url() -> str:
    """Get the appropriate database URL"""
    return settings.database_url_to_use

def is_api_key_configured(service: str) -> bool:
    """Check if a specific API key is configured"""
    api_keys = settings.validate_api_keys()
    return api_keys.get(service, False)

def get_blockchain_config() -> Dict[str, Any]:
    """Get blockchain configuration"""
    return {
        "url": settings.BLOCKCHAIN_URL,
        "network_id": settings.BLOCKCHAIN_NETWORK_ID,
        "gas_limit": settings.DEFAULT_GAS_LIMIT,
        "gas_price": settings.DEFAULT_GAS_PRICE,
        "private_key": settings.PRIVATE_KEY,
        "default_account": settings.DEFAULT_ACCOUNT
    }

def get_optimization_config() -> Dict[str, Any]:
    """Get optimization algorithm configuration"""
    return {
        "timeout": settings.OPTIMIZATION_TIMEOUT,
        "quantum": {
            "population_size": settings.QUANTUM_POPULATION_SIZE,
            "max_iterations": settings.QUANTUM_MAX_ITERATIONS,
            "tunnel_probability": settings.QUANTUM_TUNNEL_PROBABILITY,
            "superposition_factor": settings.QUANTUM_SUPERPOSITION_FACTOR,
            "entanglement_strength": settings.QUANTUM_ENTANGLEMENT_STRENGTH
        },
        "annealing": {
            "start_temp": settings.ANNEALING_START_TEMP,
            "alpha": settings.ANNEALING_ALPHA,
            "min_temp": settings.ANNEALING_MIN_TEMP
        },
        "genetic": {
            "crossover_prob": settings.GA_CROSSOVER_PROBABILITY,
            "mutation_prob": settings.GA_MUTATION_PROBABILITY,
            "elite_percent": settings.GA_ELITE_PERCENTAGE
        },
        "weights": settings.get_optimization_weights()
    }

# Initialize directories on import
ensure_directories()

# Export commonly used configurations
__all__ = [
    "settings",
    "get_project_root",
    "get_database_url",
    "is_api_key_configured",
    "get_blockchain_config",
    "get_optimization_config"
]
