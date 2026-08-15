# ============================================
# CAMPUSOS - CONFIGURATION
# ============================================
"""
Environment-based configuration using Pydantic Settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Database
    DATABASE_URL: str

    # JWT Authentication
    ALGORITHM: str
    EXPIRY_MINUTES: int
    SECRET_KEY: str

    # Application
    APP_NAME: str = "CampusOS"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    # Model config - reads from .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


# Create singleton instance
settings = Settings()
