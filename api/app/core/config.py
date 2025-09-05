"""Configuration settings for RCM GCC API."""

import os
from typing import List


class Config:
    """Application configuration."""
    
    # Flask settings
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = os.getenv("APP_ENV", "dev") == "dev"
    
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL", 
        "postgresql+psycopg://postgres:postgres@localhost:5432/rcm"
    )
    
    # AI/LLM settings
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-pro")
    
    # CORS
    ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", "*").split(",")
    
    # API settings
    API_VERSION = "v1"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Timeouts
    REQUEST_TIMEOUT = 30
    AI_TIMEOUT = 60


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    
    # Override with production settings
    def __init__(self):
        super().__init__()
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY must be set in production")


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/rcm_test"
