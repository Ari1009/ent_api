"""
Configuration settings for Movies & Anime API
"""
import os
from typing import List
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # API Configuration
    API_TITLE: str = "Movies & Anime API"
    API_VERSION: str = "2.0.0"
    API_DESCRIPTION: str = "A comprehensive API for movies, TV shows, and anime content"
    
    # Server Configuration
    HOST: str = "127.0.0.1"
    PORT: int = 8080
    DEBUG: bool = False
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "https://your-frontend-domain.com"
    ]
    
    # Cache Configuration
    CACHE_TTL: int = 300  # 5 minutes
    MAX_CACHE_SIZE: int = 1000
    
    # Request Configuration
    REQUEST_TIMEOUT: int = 10
    MAX_RETRIES: int = 3
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # External APIs
    GOGOANIME_BASE_URL: str = "https://gogoanime.ai/"
    LOOKMOVIES_BASE_URL: str = "https://lookmoviess.com"
    
    # Security
    ALLOWED_HOSTS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()