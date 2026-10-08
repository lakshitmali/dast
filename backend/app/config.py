"""
DAST Platform — Application Configuration
Uses pydantic-settings to load from .env file.
"""

import os
from pydantic_settings import BaseSettings
from functools import lru_cache

# Resolve .env path relative to this file so it works from any working directory
_ENV_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://dast:dast_secret@localhost:5432/dast_db"
    DATABASE_URL_SYNC: str = "postgresql+psycopg://dast:dast_secret@localhost:5432/dast_db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # OWASP ZAP
    ZAP_API_URL: str = "http://localhost:8080"
    ZAP_API_KEY: str = "changeme"

    # Nuclei
    NUCLEI_PATH: str = r"C:\Web Application Vulnerability Scanner\backend\nuclei.exe"

    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Application
    APP_NAME: str = "DAST Platform"
    BACKEND_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:3000"
    DEBUG: bool = True
    # Development-only escape hatch for authorized local lab targets.
    ALLOW_LOCAL_TARGETS: bool = False

    # Fuzzer
    FUZZER_THREADS: int = 30
    FUZZER_TIMEOUT: int = 5
    FUZZER_RATE_LIMIT: float = 0.0

    model_config = {
        "env_file": _ENV_FILE,
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


@lru_cache()
def get_settings() -> Settings:
    return Settings()
